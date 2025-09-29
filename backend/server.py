from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi import status as http_status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
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
        
        # Check if assessment is complete
        total_questions = await db.questions.count_documents({})
        if answered_count >= total_questions:
            await db.assessments.update_one(
                {"id": assessment_id},
                {"$set": {
                    "status": AssessmentStatus.COMPLETED,
                    "completed_at": datetime.now(timezone.utc)
                }}
            )
    
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
            # No predefined answers available in cleaned dataset
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
    
    if overall_percentage >= 80:
        overall_maturity = "Mature"
    elif overall_percentage >= 60:
        overall_maturity = "Developing"
    elif overall_percentage >= 40:
        overall_maturity = "Basic"
    else:
        overall_maturity = "Initial"
    
    return AssessmentSummary(
        overall_percentage=round(overall_percentage, 1),
        overall_maturity=overall_maturity,
        domain_scores=domain_score_list,
        total_questions=len(questions),
        answered_questions=len(answers)
    )

@api_router.get("/assessments/{assessment_id}/report")
async def generate_report(assessment_id: str, current_user: UserResponse = Depends(get_current_user)):
    # Verify assessment belongs to user's organization  
    assessment = await db.assessments.find_one({"id": assessment_id, "org_id": current_user.org_id})
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # For MVP, return a static PDF URL
    static_pdf_url = "https://example.com/assessment-report.pdf"
    
    # Store report record
    report = Report(
        assessment_id=assessment_id,
        url=static_pdf_url
    )
    await db.reports.insert_one(report.dict())
    
    return {"url": static_pdf_url}

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
    
    # Complete question set - all 88 questions from the AMAISAFE_Qs_and_As.xlsx spreadsheet
    # Note: Original spreadsheet contains only question text, no explanations or pre-defined answers
    questions_data = [
        # Fairness Domain (FA-1 to FA-8)
        {"domain_id": domains[0].id, "code": "FA-1", "text": "What measures have you implemented to identify and mitigate biases in your AI system?", "order": 1},
        {"domain_id": domains[0].id, "code": "FA-2", "text": "How do you ensure the training data represents all relevant demographics or groups?", "order": 2},
        {"domain_id": domains[0].id, "code": "FA-3", "text": "Have you evaluated the system's outputs for potential disparities across user groups?", "order": 3},
        {"domain_id": domains[0].id, "code": "FA-4", "text": "How do you measure fairness in your AI system's outputs?", "order": 4},
        {"domain_id": domains[0].id, "code": "FA-5", "text": "Have you tested the system for potential biases in real-world scenarios?", "order": 5},
        {"domain_id": domains[0].id, "code": "FA-6", "text": "Are you using any frameworks or tools (e.g., Fairlearn) to assess and mitigate bias?", "order": 6},
        {"domain_id": domains[0].id, "code": "FA-7", "text": "How do you ensure fairness in decision-making for minority or underserved groups?", "order": 7},
        {"domain_id": domains[0].id, "code": "FA-8", "text": "Is fairness embedded in your AI model's design process, or is it addressed post-deployment?", "order": 8},
        
        # Transparency Domain (TR-1 to TR-8)
        {"domain_id": domains[1].id, "code": "TR-1", "text": "What level of detail about the AI system's functionality and limitations is communicated to users or stakeholders?", "order": 1},
        {"domain_id": domains[1].id, "code": "TR-2", "text": "How do you document the data sources, algorithms, and processes used in your AI system?", "order": 2},
        {"domain_id": domains[1].id, "code": "TR-3", "text": "Are there mechanisms for external parties (e.g., regulators or customers) to understand how your AI system works?", "order": 3},
        {"domain_id": domains[1].id, "code": "TR-4", "text": "How is information about your AI system shared with internal teams and external stakeholders?", "order": 4},
        {"domain_id": domains[1].id, "code": "TR-5", "text": "Are there any \"black-box\" components in your system that could impede transparency?", "order": 5},
        {"domain_id": domains[1].id, "code": "TR-6", "text": "How do you disclose the sources of data and algorithms used in the AI system?", "order": 6},
        {"domain_id": domains[1].id, "code": "TR-7", "text": "Are users made aware when they are interacting with an AI system?", "order": 7},
        {"domain_id": domains[1].id, "code": "TR-8", "text": "Do you publish any transparency reports or documentation for regulators or customers?", "order": 8},
        
        # Explainability Domain (EX-1 to EX-8)
        {"domain_id": domains[2].id, "code": "EX-1", "text": "How do you decide the level of explainability required for your AI system?", "order": 1},
        {"domain_id": domains[2].id, "code": "EX-2", "text": "What methods are used to test whether explanations are understandable by non-technical users?", "order": 2},
        {"domain_id": domains[2].id, "code": "EX-3", "text": "Do you provide explanations in different formats (e.g., visualizations, text summaries) for different audiences?", "order": 3},
        {"domain_id": domains[2].id, "code": "EX-4", "text": "How do you evaluate the accuracy and completeness of the explanations provided?", "order": 4},
        {"domain_id": domains[2].id, "code": "EX-5", "text": "Are there trade-offs between model complexity and explainability in your system design?", "order": 5},
        {"domain_id": domains[2].id, "code": "EX-6", "text": "How do you ensure the decisions made by your AI system are interpretable by users?", "order": 6},
        {"domain_id": domains[2].id, "code": "EX-7", "text": "What tools or techniques (e.g., SHAP, LIME) do you use to make complex models more explainable?", "order": 7},
        {"domain_id": domains[2].id, "code": "EX-8", "text": "Are there specific groups (e.g., end-users, regulators, or internal teams) for whom explanations of AI outputs are tailored?", "order": 8},
        
        # Accountability Domain (AC-1 to AC-8)
        {"domain_id": domains[3].id, "code": "AC-1", "text": "How is accountability for AI system failures managed within your organization?", "order": 1},
        {"domain_id": domains[3].id, "code": "AC-2", "text": "What governance structures (e.g., AI oversight boards) are in place to monitor AI outcomes?", "order": 2},
        {"domain_id": domains[3].id, "code": "AC-3", "text": "Are there policies for escalating issues identified in the AI system?", "order": 3},
        {"domain_id": domains[3].id, "code": "AC-4", "text": "How do you handle customer complaints or disputes related to AI outputs?", "order": 4},
        {"domain_id": domains[3].id, "code": "AC-5", "text": "Are roles and responsibilities for AI governance clearly defined across teams?", "order": 5},
        {"domain_id": domains[3].id, "code": "AC-6", "text": "Who is responsible for monitoring and managing the AI system throughout its lifecycle?", "order": 6},
        {"domain_id": domains[3].id, "code": "AC-7", "text": "Are there audit trails or logs that document the AI system's decision-making process?", "order": 7},
        {"domain_id": domains[3].id, "code": "AC-8", "text": "What mechanisms are in place to address disputes or concerns about the system's outcomes?", "order": 8},
        
        # Data Integrity Domain (DI-1 to DI-8)
        {"domain_id": domains[4].id, "code": "DI-1", "text": "How do you validate the accuracy, completeness, and quality of the data used in your AI systems?", "order": 1},
        {"domain_id": domains[4].id, "code": "DI-2", "text": "What processes do you have for managing data lineage and tracking changes to data over time?", "order": 2},
        {"domain_id": domains[4].id, "code": "DI-3", "text": "Are there governance policies for data collection, usage, retention, and disposal?", "order": 3},
        {"domain_id": domains[4].id, "code": "DI-4", "text": "How do you ensure the data used in your AI systems is up-to-date and accurate?", "order": 4},
        {"domain_id": domains[4].id, "code": "DI-5", "text": "What processes are in place to address missing or incomplete data?", "order": 5},
        {"domain_id": domains[4].id, "code": "DI-6", "text": "How do you manage data preprocessing (e.g., cleaning, normalization)?", "order": 6},
        {"domain_id": domains[4].id, "code": "DI-7", "text": "Are third-party data sources evaluated for quality and reliability?", "order": 7},
        {"domain_id": domains[4].id, "code": "DI-8", "text": "How do you track data lineage to ensure traceability across the AI lifecycle?", "order": 8},
        
        # Reliability Domain (RE-1 to RE-8)
        {"domain_id": domains[5].id, "code": "RE-1", "text": "How do you test the AI system to ensure consistent performance under different conditions?", "order": 1},
        {"domain_id": domains[5].id, "code": "RE-2", "text": "Have you conducted stress tests or simulations to evaluate the system's robustness?", "order": 2},
        {"domain_id": domains[5].id, "code": "RE-3", "text": "What mechanisms are in place to monitor the system for issues like model drift or degradation?", "order": 3},
        {"domain_id": domains[5].id, "code": "RE-4", "text": "How do you define success metrics for the reliability of your AI system?", "order": 4},
        {"domain_id": domains[5].id, "code": "RE-5", "text": "Have you identified potential failure points in the system?", "order": 5},
        {"domain_id": domains[5].id, "code": "RE-6", "text": "How do you ensure the system performs consistently under varying conditions (e.g., edge cases)?", "order": 6},
        {"domain_id": domains[5].id, "code": "RE-7", "text": "Are there mechanisms for detecting and addressing system downtime or errors?", "order": 7},
        {"domain_id": domains[5].id, "code": "RE-8", "text": "How often is the AI model tested and retrained to maintain reliability?", "order": 8},
        
        # Security Domain (SE-1 to SE-8)
        {"domain_id": domains[6].id, "code": "SE-1", "text": "What measures are in place to protect your AI models and data from unauthorized access or tampering?", "order": 1},
        {"domain_id": domains[6].id, "code": "SE-2", "text": "How do you handle adversarial risks, such as attacks designed to manipulate the AI's outputs?", "order": 2},
        {"domain_id": domains[6].id, "code": "SE-3", "text": "Do you conduct regular security audits or penetration testing on your AI systems?", "order": 3},
        {"domain_id": domains[6].id, "code": "SE-4", "text": "How do you secure the AI model during training, deployment, and operation?", "order": 4},
        {"domain_id": domains[6].id, "code": "SE-5", "text": "Are there safeguards to prevent unauthorized modifications to the AI model?", "order": 5},
        {"domain_id": domains[6].id, "code": "SE-6", "text": "What measures are in place to protect the system against adversarial attacks (e.g., input manipulation)?", "order": 6},
        {"domain_id": domains[6].id, "code": "SE-7", "text": "How do you protect sensitive data in your AI pipelines (e.g., encryption, tokenization)?", "order": 7},
        {"domain_id": domains[6].id, "code": "SE-8", "text": "Are there regular vulnerability assessments and penetration tests performed on the AI system?", "order": 8},
        
        # Privacy Domain (PR-1 to PR-8)
        {"domain_id": domains[7].id, "code": "PR-1", "text": "How do you ensure compliance with data privacy laws, such as GDPR or the Australian Privacy Act?", "order": 1},
        {"domain_id": domains[7].id, "code": "PR-2", "text": "What techniques (e.g., anonymization, pseudonymization) do you use to protect personal data in your AI workflows?", "order": 2},
        {"domain_id": domains[7].id, "code": "PR-3", "text": "How do you manage user consent for data collection and processing?", "order": 3},
        {"domain_id": domains[7].id, "code": "PR-4", "text": "How do you ensure that personal data is not used beyond its original purpose?", "order": 4},
        {"domain_id": domains[7].id, "code": "PR-5", "text": "What methods do you use to anonymize or pseudonymize personal data?", "order": 5},
        {"domain_id": domains[7].id, "code": "PR-6", "text": "How do you monitor and prevent privacy violations during system operation?", "order": 6},
        {"domain_id": domains[7].id, "code": "PR-7", "text": "Are privacy risks evaluated during both the development and deployment phases?", "order": 7},
        {"domain_id": domains[7].id, "code": "PR-8", "text": "What steps are taken to ensure compliance with cross-border data protection laws?", "order": 8},
        
        # Safety Domain (SA-1 to SA-8)
        {"domain_id": domains[8].id, "code": "SA-1", "text": "Have you conducted a safety impact assessment for the AI system?", "order": 1},
        {"domain_id": domains[8].id, "code": "SA-2", "text": "How do you ensure that the system does not cause harm in unintended ways?", "order": 2},
        {"domain_id": domains[8].id, "code": "SA-3", "text": "Are there monitoring tools in place to detect unsafe system behavior in real-time?", "order": 3},
        {"domain_id": domains[8].id, "code": "SA-4", "text": "How do you handle situations where the system's actions conflict with human safety requirements?", "order": 4},
        {"domain_id": domains[8].id, "code": "SA-5", "text": "Are there emergency protocols for shutting down the system in case of unsafe behavior?", "order": 5},
        {"domain_id": domains[8].id, "code": "SA-6", "text": "What steps have you taken to identify and mitigate potential risks or harm caused by the AI system?", "order": 6},
        {"domain_id": domains[8].id, "code": "SA-7", "text": "Are there fail-safe mechanisms or redundancies in place to address unexpected system behaviors?", "order": 7},
        {"domain_id": domains[8].id, "code": "SA-8", "text": "Have you conducted safety testing in realistic or high-risk scenarios?", "order": 8},
        
        # Inclusivity Domain (IN-1 to IN-8)
        {"domain_id": domains[9].id, "code": "IN-1", "text": "How do you ensure your AI system is accessible to a diverse range of users, including those with disabilities or in underserved populations?", "order": 1},
        {"domain_id": domains[9].id, "code": "IN-2", "text": "Were diverse perspectives considered during the design and development of the system?", "order": 2},
        {"domain_id": domains[9].id, "code": "IN-3", "text": "Have you audited the system for potential exclusionary outcomes or unintended impacts?", "order": 3},
        {"domain_id": domains[9].id, "code": "IN-4", "text": "How do you ensure your AI system accounts for accessibility requirements (e.g., for users with disabilities)?", "order": 4},
        {"domain_id": domains[9].id, "code": "IN-5", "text": "Are stakeholders from diverse backgrounds involved in the design and testing of the system?", "order": 5},
        {"domain_id": domains[9].id, "code": "IN-6", "text": "What steps are taken to ensure that the AI system serves underrepresented communities effectively?", "order": 6},
        {"domain_id": domains[9].id, "code": "IN-7", "text": "Are language, cultural, or regional differences considered in system design?", "order": 7},
        {"domain_id": domains[9].id, "code": "IN-8", "text": "How do you evaluate whether the system is unintentionally excluding certain user groups?", "order": 8},
        
        # Sustainability Domain (SU-1 to SU-8)
        {"domain_id": domains[10].id, "code": "SU-1", "text": "What is the environmental impact of training and deploying your AI system (e.g., energy usage, carbon footprint)?", "order": 1},
        {"domain_id": domains[10].id, "code": "SU-2", "text": "Have you explored opportunities to optimize algorithms for greater computational efficiency?", "order": 2},
        {"domain_id": domains[10].id, "code": "SU-3", "text": "Are you using cloud services or infrastructure that prioritizes renewable energy sources?", "order": 3},
        {"domain_id": domains[10].id, "code": "SU-4", "text": "What is the estimated carbon footprint of training and deploying your AI system?", "order": 4},
        {"domain_id": domains[10].id, "code": "SU-5", "text": "Have you optimized your algorithms to reduce computational resource requirements?", "order": 5},
        {"domain_id": domains[10].id, "code": "SU-6", "text": "Are you using hardware or cloud platforms that prioritize energy efficiency?", "order": 6},
        {"domain_id": domains[10].id, "code": "SU-7", "text": "How do you balance sustainability goals with performance requirements?", "order": 7},
        {"domain_id": domains[10].id, "code": "SU-8", "text": "Do you track the environmental impact of your AI systems over time?", "order": 8}
    ]
    
    for question_data in questions_data:
        question = Question(**question_data)
        await db.questions.insert_one(question.dict())
    
    logger.info(f"Database seeded with {len(domains)} domains and {len(questions_data)} questions")