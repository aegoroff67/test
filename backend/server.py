from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi import status as http_status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import hashlib
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
import uuid
from enum import Enum
import io
from complete_questions import COMPLETE_QUESTIONS_DATA

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Security
security = HTTPBearer()
SECRET_KEY = os.environ.get('JWT_SECRET', 'your-secret-key-change-in-production')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Create the main app
app = FastAPI(title="AM AI SAFE API")
api_router = APIRouter(prefix="/api")

# Enums
class Role(str, Enum):
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"

class AssessmentStatus(str, Enum):
    INCOMPLETE = "INCOMPLETE"
    COMPLETED = "COMPLETED"

# AnswerOption enum needs to be defined before scoring map
class AnswerOption(str, Enum):
    IDEAL = "IDEAL"
    GOOD = "GOOD"
    BASIC = "BASIC"
    NON_IDEAL = "NON_IDEAL"
    OTHER = "OTHER"

# Standard scoring map
SCORING_MAP = {
    AnswerOption.IDEAL: 3,
    AnswerOption.GOOD: 2,
    AnswerOption.BASIC: 1,
    AnswerOption.NON_IDEAL: 0,
    AnswerOption.OTHER: 0  # Will be manually reviewed and scored later
}

# Models
class Organization(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    industry: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    hashed_password: str
    name: str
    org_id: str
    role: Role = Role.MEMBER
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Domain(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    order: int
    description: Optional[str] = None

class Question(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    domain_id: str
    code: str
    text: str
    help_text: Optional[str] = None
    explanation: Optional[str] = None
    ideal_answer: Optional[str] = None
    good_answer: Optional[str] = None
    basic_answer: Optional[str] = None
    non_ideal_answer: Optional[str] = None
    order: int

class Assessment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    org_id: str
    user_id: str
    name: str
    status: AssessmentStatus = AssessmentStatus.INCOMPLETE
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    progress: int = 0  # Number of questions answered

class Answer(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    assessment_id: str
    question_id: str
    option: AnswerOption
    numeric_score: int
    other_text: Optional[str] = None  # For "Other" responses
    note: Optional[str] = None
    needs_review: bool = False  # Flag for "Other" responses
    answered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Report(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    assessment_id: str
    url: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Request/Response models
class UserSignUp(BaseModel):
    name: str
    email: EmailStr
    password: str
    organization_name: str
    industry: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    org_id: str
    role: str
    organization_name: str
    industry: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class AssessmentCreate(BaseModel):
    pass  # Auto-generates name

class AssessmentResponse(BaseModel):
    id: str
    name: str
    status: str
    started_at: datetime
    completed_at: Optional[datetime]
    progress: int
    total_questions: int

class AnswerSubmit(BaseModel):
    question_id: str
    option: AnswerOption
    other_text: Optional[str] = None  # Required when option is OTHER
    note: Optional[str] = None

class DomainScore(BaseModel):
    domain_id: str
    domain_name: str
    score: float
    max_score: int
    percentage: float

class AssessmentSummary(BaseModel):
    overall_percentage: float
    overall_maturity: str
    domain_scores: List[DomainScore]
    total_questions: int
    answered_questions: int

# Helper functions
def hash_password(password: str) -> str:
    # Simple SHA-256 hashing for MVP (use bcrypt in production)
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=http_status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        
        user = await db.users.find_one({"id": user_id})
        if user is None:
            raise HTTPException(
                status_code=http_status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        org = await db.organizations.find_one({"id": user["org_id"]})
        user["organization_name"] = org["name"] if org else "Unknown"
        user["industry"] = org["industry"] if org else "Unknown"
        
        return UserResponse(**user)
        
    except JWTError:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

# Auth endpoints
@api_router.post("/auth/signup", response_model=Token)
async def signup(user_data: UserSignUp):
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Create organization
    org = Organization(
        name=user_data.organization_name,
        industry=user_data.industry
    )
    await db.organizations.insert_one(org.dict())
    
    # Create user
    user = User(
        email=user_data.email,
        name=user_data.name,
        hashed_password=hash_password(user_data.password),
        org_id=org.id,
        role=Role.ADMIN  # First user is admin
    )
    await db.users.insert_one(user.dict())
    
    # Create JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    
    user_response = UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        org_id=user.org_id,
        role=user.role,
        organization_name=org.name,
        industry=org.industry
    )
    
    return Token(access_token=access_token, token_type="bearer", user=user_response)

@api_router.post("/auth/login", response_model=Token)
async def login(user_data: UserLogin):
    # Temporary access control - only allow andrew@vciso.one
    if user_data.email != "andrew@vciso.one":
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="Access temporarily restricted"
        )
    
    user = await db.users.find_one({"email": user_data.email})
    if not user or not verify_password(user_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    org = await db.organizations.find_one({"id": user["org_id"]})
    
    # Create JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["id"]}, expires_delta=access_token_expires
    )
    
    user_response = UserResponse(
        id=user["id"],
        email=user["email"],
        name=user["name"],
        org_id=user["org_id"],
        role=user["role"],
        organization_name=org["name"] if org else "Unknown",
        industry=org["industry"] if org else "Unknown"
    )
    
    return Token(access_token=access_token, token_type="bearer", user=user_response)

# Assessment endpoints
@api_router.post("/assessments", response_model=AssessmentResponse)
async def create_assessment(current_user: UserResponse = Depends(get_current_user)):
    # Count existing assessments to generate name
    assessment_count = await db.assessments.count_documents({"org_id": current_user.org_id})
    assessment_name = f"Assessment {assessment_count + 1}"
    
    assessment = Assessment(
        org_id=current_user.org_id,
        user_id=current_user.id,
        name=assessment_name
    )
    
    await db.assessments.insert_one(assessment.dict())
    
    # Get total questions count
    total_questions = await db.questions.count_documents({})
    
    return AssessmentResponse(
        id=assessment.id,
        name=assessment.name,
        status=assessment.status,
        started_at=assessment.started_at,
        completed_at=assessment.completed_at,
        progress=assessment.progress,
        total_questions=total_questions
    )

@api_router.get("/assessments", response_model=List[AssessmentResponse])
async def get_assessments(current_user: UserResponse = Depends(get_current_user)):
    assessments = await db.assessments.find({"org_id": current_user.org_id}).to_list(length=None)
    
    # Get total questions count
    total_questions = await db.questions.count_documents({})
    
    return [
        AssessmentResponse(
            id=assessment["id"],
            name=assessment["name"],
            status=assessment["status"],
            started_at=assessment["started_at"],
            completed_at=assessment.get("completed_at"),
            progress=assessment["progress"],
            total_questions=total_questions
        )
        for assessment in assessments
    ]

@api_router.get("/assessments/{assessment_id}")
async def get_assessment(assessment_id: str, current_user: UserResponse = Depends(get_current_user)):
    assessment = await db.assessments.find_one({"id": assessment_id, "org_id": current_user.org_id})
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Get total questions count
    total_questions = await db.questions.count_documents({})
    
    return AssessmentResponse(
        id=assessment["id"],
        name=assessment["name"],
        status=assessment["status"],
        started_at=assessment["started_at"],
        completed_at=assessment.get("completed_at"),
        progress=assessment["progress"],
        total_questions=total_questions
    )

@api_router.post("/assessments/{assessment_id}/answer")
async def submit_answer(
    assessment_id: str, 
    answer_data: AnswerSubmit, 
    current_user: UserResponse = Depends(get_current_user)
):
    # Verify assessment belongs to user's organization
    assessment = await db.assessments.find_one({"id": assessment_id, "org_id": current_user.org_id})
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Check if answer already exists
    existing_answer = await db.answers.find_one({
        "assessment_id": assessment_id,
        "question_id": answer_data.question_id
    })
    
    # Validate "Other" option
    if answer_data.option == AnswerOption.OTHER and not answer_data.other_text:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail="other_text is required when option is OTHER"
        )
    
    answer = Answer(
        assessment_id=assessment_id,
        question_id=answer_data.question_id,
        option=answer_data.option,
        numeric_score=SCORING_MAP[answer_data.option],
        other_text=answer_data.other_text,
        note=answer_data.note,
        needs_review=(answer_data.option == AnswerOption.OTHER)
    )
    
    if existing_answer:
        # Update existing answer
        await db.answers.update_one(
            {"assessment_id": assessment_id, "question_id": answer_data.question_id},
            {"$set": answer.dict()}
        )
    else:
        # Insert new answer
        await db.answers.insert_one(answer.dict())
        
        # Update assessment progress (only for new answers)
        answered_count = await db.answers.count_documents({"assessment_id": assessment_id})
        await db.assessments.update_one(
            {"id": assessment_id},
            {"$set": {"progress": answered_count}}
        )
        
        # Don't auto-complete assessment - wait for explicit submission
        # Assessment remains INCOMPLETE until user clicks "Submit Assessment"
    
    return {"status": "success"}

@api_router.get("/assessments/{assessment_id}/questions")
async def get_assessment_questions(assessment_id: str, current_user: UserResponse = Depends(get_current_user)):
    # Verify assessment belongs to user's organization
    assessment = await db.assessments.find_one({"id": assessment_id, "org_id": current_user.org_id})
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Get domains with questions
    domains = await db.domains.find({}, {"_id": 0}).sort("order").to_list(length=None)
    questions = await db.questions.find({}, {"_id": 0}).sort([("domain_id", 1), ("order", 1)]).to_list(length=None)
    answers = await db.answers.find({"assessment_id": assessment_id}, {"_id": 0}).to_list(length=None)
    
    # Create answer lookup
    answer_lookup = {answer["question_id"]: answer for answer in answers}
    
    # Group questions by domain
    domain_questions = {}
    for domain in domains:
        domain_questions[domain["id"]] = {
            "domain": domain,
            "questions": []
        }
    
    for question in questions:
        if question["domain_id"] in domain_questions:
            question["answer"] = answer_lookup.get(question["id"])
            # Add predefined answers to the response
            question["predefined_answers"] = {
                "ideal": question.get("ideal_answer"),
                "good": question.get("good_answer"), 
                "basic": question.get("basic_answer"),
                "non_ideal": question.get("non_ideal_answer")
            }
            domain_questions[question["domain_id"]]["questions"].append(question)
    
    return [dq for dq in domain_questions.values() if dq["questions"]]

@api_router.get("/assessments/{assessment_id}/summary")
async def get_assessment_summary(assessment_id: str, current_user: UserResponse = Depends(get_current_user)):
    # Verify assessment belongs to user's organization
    assessment = await db.assessments.find_one({"id": assessment_id, "org_id": current_user.org_id})
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Get domains, questions and answers
    domains = await db.domains.find({}, {"_id": 0}).sort("order").to_list(length=None)
    questions = await db.questions.find({}, {"_id": 0}).to_list(length=None)
    answers = await db.answers.find({"assessment_id": assessment_id}, {"_id": 0}).to_list(length=None)
    
    # Create lookups
    domain_lookup = {domain["id"]: domain for domain in domains}
    question_lookup = {question["id"]: question for question in questions}
    
    # Calculate domain scores
    domain_scores = {}
    for answer in answers:
        question = question_lookup.get(answer["question_id"])
        if not question:
            continue
            
        domain_id = question["domain_id"]
        if domain_id not in domain_scores:
            domain_scores[domain_id] = {"score": 0, "max_score": 0}
        
        domain_scores[domain_id]["score"] += answer["numeric_score"]
        domain_scores[domain_id]["max_score"] += 3  # Maximum score per question
    
    # Build domain score list
    domain_score_list = []
    overall_score = 0
    overall_max_score = 0
    
    for domain_id, scores in domain_scores.items():
        domain = domain_lookup.get(domain_id)
        if domain:
            percentage = (scores["score"] / scores["max_score"] * 100) if scores["max_score"] > 0 else 0
            domain_score_list.append(DomainScore(
                domain_id=domain_id,
                domain_name=domain["name"],
                score=scores["score"],
                max_score=scores["max_score"],
                percentage=percentage
            ))
            overall_score += scores["score"]
            overall_max_score += scores["max_score"]
    
    # Calculate overall metrics
    overall_percentage = (overall_score / overall_max_score * 100) if overall_max_score > 0 else 0
    
    if overall_percentage >= 91:
        overall_maturity = "Excellent"
    elif overall_percentage >= 81:
        overall_maturity = "Good"
    elif overall_percentage >= 61:
        overall_maturity = "Moderate"
    elif overall_percentage >= 41:
        overall_maturity = "Low"
    else:
        overall_maturity = "Basic"
    
    return AssessmentSummary(
        overall_percentage=round(overall_percentage, 1),
        overall_maturity=overall_maturity,
        domain_scores=domain_score_list,
        total_questions=len(questions),
        answered_questions=len(answers)
    )

@api_router.get("/assessments/{assessment_id}/status")
async def get_assessment_status(assessment_id: str, current_user: UserResponse = Depends(get_current_user)):
    # Verify assessment belongs to user's organization
    assessment = await db.assessments.find_one({"id": assessment_id, "org_id": current_user.org_id})
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Get domains, questions and answers
    domains = await db.domains.find().sort("order").to_list(length=None)
    questions = await db.questions.find().to_list(length=None)
    answers = await db.answers.find({"assessment_id": assessment_id}).to_list(length=None)
    
    # Create lookups
    domain_lookup = {domain["id"]: domain for domain in domains}
    answer_lookup = {answer["question_id"]: answer for answer in answers}
    
    # Build status overview by domain
    status_overview = []
    total_questions = len(questions)
    answered_questions = len(answers)
    
    # Group questions by domain
    domain_questions = {}
    for domain in domains:
        domain_questions[domain["id"]] = {
            "domain": domain,
            "questions": []
        }
    
    for question in questions:
        if question["domain_id"] in domain_questions:
            question_status = {
                "question_id": question["id"],
                "question_code": question["code"],
                "question_text": question["text"],
                "answered": question["id"] in answer_lookup
            }
            domain_questions[question["domain_id"]]["questions"].append(question_status)
    
    # Build the status overview
    for domain_id, domain_data in domain_questions.items():
        if domain_data["questions"]:
            status_overview.append({
                "domain_id": domain_id,
                "domain_name": domain_data["domain"]["name"],
                "questions": domain_data["questions"]
            })
    
    # Calculate completion percentage
    completion_percentage = round((answered_questions / total_questions * 100) if total_questions > 0 else 0, 1)
    
    return {
        "assessment_id": assessment_id,
        "total_questions": total_questions,
        "answered_questions": answered_questions,
        "completion_percentage": completion_percentage,
        "status_overview": status_overview
    }

@api_router.get("/assessments/{assessment_id}/report")
async def generate_report_docx(assessment_id: str, current_user: UserResponse = Depends(get_current_user)):
    """Generate and download DOCX report for assessment using DOCX template."""
    from report_generator import AMReportGenerator
    
    try:
        # Initialize report generator
        report_generator = AMReportGenerator()
        
        # Generate report
        docx_bytes, filename = await report_generator.generate_report_for_assessment(
            assessment_id, db, current_user
        )
        
        # Store report record in database
        report = Report(
            assessment_id=assessment_id,
            url=f"/reports/{filename}",  # Store relative path
        )
        await db.reports.insert_one(report.dict())
        
        # Return DOCX as streaming response
        return StreamingResponse(
            io.BytesIO(docx_bytes),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition": f"attachment; filename=\"{filename}\"",
                "Content-Type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            }
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions to preserve status codes
        raise
    except Exception as e:
        print(f"Error generating DOCX report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")


@api_router.get("/assessments/{assessment_id}/report/pdf")
async def generate_report_pdf(assessment_id: str, current_user: UserResponse = Depends(get_current_user)):
    """Generate and download PDF report for assessment using DOCX template."""
    from report_generator import AMReportGenerator
    
    try:
        # Initialize report generator
        report_generator = AMReportGenerator()
        
        # Generate both DOCX and PDF
        docx_bytes, pdf_bytes = await report_generator.generate_report_full(
            assessment_id, db, current_user
        )
        
        # Generate PDF filename
        safe_org_name = "".join(c for c in current_user.organization_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_org_name = safe_org_name.replace(' ', '_') if safe_org_name else "Organization"
        
        # Get assessment date
        assessment = await db.assessments.find_one({"id": assessment_id, "org_id": current_user.org_id})
        filename = f"AM_AI_SAFE_Assessment_{safe_org_name}_{assessment.get('created_at', datetime.now(timezone.utc)).strftime('%Y-%m-%d')}.pdf"
        
        # Store report record in database
        report = Report(
            assessment_id=assessment_id,
            url=f"/reports/{filename}",  # Store relative path
        )
        await db.reports.insert_one(report.dict())
        
        # Return PDF as streaming response
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=\"{filename}\"",
                "Content-Type": "application/pdf"
            }
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions to preserve status codes
        raise
    except Exception as e:
        print(f"Error generating PDF report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")

@api_router.post("/assessments/{assessment_id}/submit")
async def submit_assessment(assessment_id: str, current_user: UserResponse = Depends(get_current_user)):
    # Verify assessment belongs to user's organization
    assessment = await db.assessments.find_one({"id": assessment_id, "org_id": current_user.org_id})
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Check if assessment is already completed
    if assessment.get("status") == AssessmentStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Assessment is already submitted")
    
    # Get total questions and answered questions count
    total_questions = await db.questions.count_documents({})
    answered_questions = await db.answers.count_documents({"assessment_id": assessment_id})
    
    # Verify all questions are answered
    if answered_questions < total_questions:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot submit assessment. {total_questions - answered_questions} questions remain unanswered."
        )
    
    # Mark assessment as completed
    await db.assessments.update_one(
        {"id": assessment_id},
        {
            "$set": {
                "status": AssessmentStatus.COMPLETED,
                "completed_at": datetime.now(timezone.utc),
                "progress": total_questions
            }
        }
    )
    
    return {
        "status": "success",
        "message": "Assessment submitted successfully",
        "assessment_id": assessment_id,
        "completed_at": datetime.now(timezone.utc).isoformat()
    }

# Admin endpoints
@api_router.get("/domains", response_model=List[Domain])
async def get_domains():
    domains = await db.domains.find({}, {"_id": 0}).sort("order").to_list(length=None)
    return [Domain(**domain) for domain in domains]

@api_router.get("/questions")
async def get_questions(domain_id: Optional[str] = None):
    query = {"domain_id": domain_id} if domain_id else {}
    questions = await db.questions.find(query, {"_id": 0}).sort("order").to_list(length=None)
    return questions

# Include router
app.include_router(api_router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

@app.on_event("startup")
async def startup_event():
    logger.info("Starting AM AI SAFE API")
    await seed_data()

async def seed_data():
    """Seed the database with initial data"""
    # Check if already seeded
    if await db.domains.count_documents({}) > 0:
        return
    
    logger.info("Seeding database with complete AM AI SAFE question set...")
    
    # All 11 domains from the spreadsheet
    domains_data = [
        {"name": "Fairness", "order": 1, "description": "Bias identification and mitigation in AI systems"},
        {"name": "Transparency", "order": 2, "description": "Openness and clear communication about AI system functionality"},
        {"name": "Explainability", "order": 3, "description": "Ability to understand and interpret AI decision-making processes"},
        {"name": "Accountability", "order": 4, "description": "Clear responsibility and governance structures for AI systems"},
        {"name": "Data Integrity", "order": 5, "description": "Quality, accuracy, and proper management of data throughout AI lifecycle"},
        {"name": "Reliability", "order": 6, "description": "Consistent and dependable performance of AI systems"},
        {"name": "Security", "order": 7, "description": "Protection against threats, attacks, and unauthorized access"},
        {"name": "Privacy", "order": 8, "description": "Protection of personal data and compliance with privacy regulations"},
        {"name": "Safety", "order": 9, "description": "Prevention of harm and implementation of safeguards in AI systems"},
        {"name": "Inclusivity", "order": 10, "description": "Ensuring AI systems are accessible and serve diverse user populations"},
        {"name": "Sustainability", "order": 11, "description": "Environmental responsibility and resource efficiency in AI systems"}
    ]
    
    domains = []
    for domain_data in domains_data:
        domain = Domain(**domain_data)
        domains.append(domain)
        await db.domains.insert_one(domain.dict())
    
    # Use complete question data from COMPLETE_QUESTIONS_DATA with explanations
    for question_data in COMPLETE_QUESTIONS_DATA:
        # Map domain order to domain ID
        domain_order = question_data.get("domain_order", 1)
        domain_id = domains[domain_order - 1].id  # Convert 1-based order to 0-based index
        
        question = Question(
            domain_id=domain_id,
            code=question_data["code"],
            text=question_data["text"],
            explanation=question_data.get("explanation"),
            order=question_data["order"],
            # Use specific pre-defined answers from question data, fallback to standard if not provided
            ideal_answer=question_data.get("ideal_answer", "Comprehensive implementation with best practices and full compliance"),
            good_answer=question_data.get("good_answer", "Solid implementation with room for improvement"), 
            basic_answer=question_data.get("basic_answer", "Minimal implementation, significant gaps exist"),
            non_ideal_answer=question_data.get("non_ideal_answer", "Little to no implementation or consideration")
        )
        await db.questions.insert_one(question.dict())
    
    logger.info(f"Database seeded with {len(domains)} domains and {len(COMPLETE_QUESTIONS_DATA)} questions with explanations")