from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi import status as http_status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import StreamingResponse, FileResponse
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
import tempfile
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
    SUPER_ADMIN = "SUPER_ADMIN"
    ORG_ADMIN = "ORG_ADMIN"
    ADMIN = "ADMIN"  # Keep for backward compatibility
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
    is_active: bool = True
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
    assessment_type: str = "System"  # "System", "Readiness", or "Organisation"
    status: AssessmentStatus = AssessmentStatus.INCOMPLETE
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    progress: int = 0  # Number of questions answered
    system_info: Optional[dict] = None  # Pre-assessment system information

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
    is_active: bool
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
    assessment_type: str = "System"
    status: str
    started_at: datetime
    completed_at: Optional[datetime]
    progress: int
    total_questions: int
    system_info: Optional[dict] = None

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
        is_active=user.is_active,
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
@api_router.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: UserResponse = Depends(get_current_user)):
    return current_user

# Assessment endpoints
@api_router.post("/assessments", response_model=AssessmentResponse)
async def create_assessment(current_user: UserResponse = Depends(get_current_user)):
    # Generate initial assessment name with format: [Type] – [TBD] – Started YYYY-MM-DD
    started_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    assessment_name = f"System – [TBD] – Started {started_date}"
    
    assessment = Assessment(
        org_id=current_user.org_id,
        user_id=current_user.id,
        name=assessment_name,
        assessment_type="System"
    )
    
    await db.assessments.insert_one(assessment.dict())
    
    # Get total questions count
    total_questions = await db.questions.count_documents({})
    
    return AssessmentResponse(
        id=assessment.id,
        name=assessment.name,
        assessment_type=assessment.assessment_type,
        status=assessment.status,
        started_at=assessment.started_at,
        completed_at=assessment.completed_at,
        progress=assessment.progress,
        total_questions=total_questions,
        system_info=assessment.system_info
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
            assessment_type=assessment.get("assessment_type", "System"),
            status=assessment["status"],
            started_at=assessment["started_at"],
            completed_at=assessment.get("completed_at"),
            progress=assessment["progress"],
            total_questions=total_questions,
            system_info=assessment.get("system_info")
        )
        for assessment in assessments
    ]

@api_router.delete("/assessments/{assessment_id}")
async def delete_assessment(
    assessment_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    # Verify assessment belongs to user's organization
    assessment = await db.assessments.find_one({"id": assessment_id, "org_id": current_user.org_id})
    
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Delete all answers associated with the assessment
    await db.answers.delete_many({"assessment_id": assessment_id})
    
    # Delete the assessment
    await db.assessments.delete_one({"id": assessment_id})
    
    return {"success": True, "message": "Assessment deleted successfully"}

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
        assessment_type=assessment.get("assessment_type", "System"),
        status=assessment["status"],
        started_at=assessment["started_at"],
        completed_at=assessment.get("completed_at"),
        progress=assessment["progress"],
        total_questions=total_questions,
        system_info=assessment.get("system_info")
    )

@api_router.put("/assessments/{assessment_id}/system-info")
async def update_system_info(
    assessment_id: str,
    system_info: dict,
    current_user: UserResponse = Depends(get_current_user)
):
    # Verify assessment belongs to user's organization
    assessment = await db.assessments.find_one({"id": assessment_id, "org_id": current_user.org_id})
    
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Update the assessment name with the target name from system_info
    updated_name = assessment["name"]
    if system_info.get("systemName"):
        # Extract the assessment type and date from current name
        assessment_type = assessment.get("assessment_type", "System")
        started_date = assessment["started_at"].strftime("%Y-%m-%d")
        # Generate new name: [Type] – [Target Name] – Started YYYY-MM-DD
        updated_name = f"{assessment_type} – {system_info['systemName']} – Started {started_date}"
    
    # Update both system_info and name
    await db.assessments.update_one(
        {"id": assessment_id},
        {"$set": {"system_info": system_info, "name": updated_name}}
    )
    
    return {"success": True, "message": "System information updated"}


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
    
    # Updated maturity tiers aligned with new scale
    if overall_percentage >= 86:
        overall_maturity = "Leading"
    elif overall_percentage >= 66:
        overall_maturity = "Established"
    elif overall_percentage >= 41:
        overall_maturity = "Developing"
    else:
        overall_maturity = "Foundational"
    
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
            url=f"/reports/{filename}",
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
        raise
    except Exception as e:
        logger.error(f"Error generating DOCX report: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate DOCX report: {str(e)}")


@api_router.get("/assessments/{assessment_id}/executive-summary-pdf")
async def generate_executive_summary_pdf(
    assessment_id: str, 
    current_user: UserResponse = Depends(get_current_user)
):
    """Generate executive summary PDF with exact specifications"""
    try:
        from playwright.async_api import async_playwright
        
        # Set Playwright browser path
        os.environ['PLAYWRIGHT_BROWSERS_PATH'] = '/pw-browsers'
        
        # Verify assessment belongs to user's organization
        assessment = await db.assessments.find_one({"id": assessment_id, "org_id": current_user.org_id})
        if not assessment:
            raise HTTPException(status_code=404, detail="Assessment not found")
        
        # Get frontend URL from environment (this points to external URL)
        frontend_url = os.environ.get('REACT_APP_BACKEND_URL', 'http://localhost:3000')
        frontend_url = frontend_url.replace(':8001', ':3000')  # Ensure we're hitting frontend port
        
        # Construct results page URL
        results_url = f"{frontend_url}/results/{assessment_id}"
        
        logger.info(f"Generating PDF for URL: {results_url}")
        
        logger.info(f"Generating PDF for URL: {results_url}")
        
        # Create temporary file for PDF
        temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_pdf_path = temp_pdf.name
        temp_pdf.close()
        
        async with async_playwright() as p:
            # Launch browser with explicit executable path
            browser = await p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                java_script_enabled=True
            )
            
            page = await context.new_page()
            
            # Generate auth token
            auth_token = jwt.encode(
                {'sub': current_user.id, 'exp': datetime.now(timezone.utc) + timedelta(minutes=5)}, 
                SECRET_KEY, 
                algorithm=ALGORITHM
            )
            
            # Navigate to the app first to set localStorage
            logger.info(f"Navigating to base URL to set auth")
            await page.goto(frontend_url, wait_until='domcontentloaded', timeout=30000)
            
            # Inject authentication token into localStorage
            user_json = {
                "id": current_user.id,
                "email": current_user.email,
                "organization_name": current_user.organization_name
            }
            import json
            user_json_str = json.dumps(user_json).replace("'", "\\'")
            
            await page.evaluate(f"""
                localStorage.setItem('token', '{auth_token}');
                localStorage.setItem('user', '{user_json_str}');
            """)
            
            logger.info(f"Auth token set, navigating to {results_url}")
            
            # Now navigate to results page with authentication
            response = await page.goto(results_url, wait_until='networkidle', timeout=60000)
            logger.info(f"Page loaded with status: {response.status}")
            
            # Wait a bit more for dynamic content and charts to render
            await page.wait_for_timeout(3000)
            
            # Verify we're on the right page (not login)
            page_title = await page.title()
            logger.info(f"Page title: {page_title}")
            
            # Check if we're on login page
            login_check = await page.query_selector('text=Login') or await page.query_selector('text=Sign In')
            if login_check:
                logger.error("Still on login page after setting token!")
                raise Exception("Authentication failed - redirected to login page")
            
            # Take screenshot for debugging (optional)
            # await page.screenshot(path='/tmp/debug.png', full_page=True)
            
            # Generate PDF with exact specifications
            await page.pdf(
                path=temp_pdf_path,
                format='A4',
                landscape=True,
                scale=0.68,
                print_background=True,
                margin={
                    'top': '1cm',
                    'right': '1cm',
                    'bottom': '1cm',
                    'left': '1cm'
                }
            )
            
            logger.info(f"PDF generated at: {temp_pdf_path}")
            await browser.close()
        
        # Generate filename - sanitize for HTTP headers (latin-1 compatible)
        assessment_name = assessment.get('name', 'Assessment')
        # Replace special characters with ASCII equivalents
        assessment_name = assessment_name.replace('–', '-')  # en-dash to hyphen
        assessment_name = assessment_name.replace('—', '-')  # em-dash to hyphen
        assessment_name = assessment_name.replace(' ', '_')
        # Remove any non-ASCII characters
        assessment_name = assessment_name.encode('ascii', 'ignore').decode('ascii')
        filename = f"Executive_Summary_{assessment_name}.pdf"
        
        # Return PDF file
        return FileResponse(
            temp_pdf_path,
            media_type='application/pdf',
            filename=filename,
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"'
            }
        )
        
    except Exception as e:
        logger.error(f"Error generating executive summary PDF: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")


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
    
    # Update the assessment name to replace "Started" with "Completed"
    completed_date = datetime.now(timezone.utc)
    current_name = assessment["name"]
    
    # Replace "Started YYYY-MM-DD" with "Completed YYYY-MM-DD"
    if "Started" in current_name:
        # Extract everything before the date part
        parts = current_name.split(" – ")
        if len(parts) >= 3:
            # parts[0] = Type, parts[1] = Target Name, parts[2] = "Started YYYY-MM-DD"
            updated_name = f"{parts[0]} – {parts[1]} – Completed {completed_date.strftime('%Y-%m-%d')}"
        else:
            updated_name = current_name
    else:
        updated_name = current_name
    
    # Mark assessment as completed
    await db.assessments.update_one(
        {"id": assessment_id},
        {
            "$set": {
                "status": AssessmentStatus.COMPLETED,
                "completed_at": completed_date,
                "progress": total_questions,
                "name": updated_name
            }
        }
    )
    
    return {
        "status": "success",
        "message": "Assessment submitted successfully",
        "assessment_id": assessment_id,
        "completed_at": completed_date.isoformat()
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