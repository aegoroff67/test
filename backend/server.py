from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
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

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
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

class AnswerOption(str, Enum):
    NON_IDEAL = "NON_IDEAL"
    BASIC = "BASIC"
    GOOD = "GOOD"
    IDEAL = "IDEAL"
    OTHER = "OTHER"

# Scoring map
SCORING_MAP = {
    AnswerOption.NON_IDEAL: 0,
    AnswerOption.BASIC: 1,
    AnswerOption.GOOD: 2,
    AnswerOption.IDEAL: 3,
    AnswerOption.OTHER: 0
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
    note: Optional[str] = None
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
    # Truncate password to 72 bytes for bcrypt compatibility
    password_bytes = password.encode('utf-8')[:72]
    return pwd_context.hash(password_bytes.decode('utf-8'))

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Truncate password to 72 bytes for bcrypt compatibility
    password_bytes = plain_password.encode('utf-8')[:72]
    return pwd_context.verify(password_bytes.decode('utf-8'), hashed_password)

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
            raise HTTPException(status_code=401, detail="Invalid token")
        user = await db.users.find_one({"id": user_id})
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return User(**user)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_maturity_level(percentage: float) -> str:
    if percentage < 30:
        return "LOW"
    elif percentage < 70:
        return "MODERATE"
    else:
        return "HIGH"

# Auth endpoints
@api_router.post("/auth/signup", response_model=Token)
async def signup(user_data: UserSignUp):
    # Check if user exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create organization
    org = Organization(
        name=user_data.organization_name,
        industry=user_data.industry
    )
    await db.organizations.insert_one(org.dict())
    
    # Create user
    user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        name=user_data.name,
        org_id=org.id,
        role=Role.MEMBER
    )
    await db.users.insert_one(user.dict())
    
    # Create token
    access_token = create_access_token(data={"sub": user.id})
    
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
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    org = await db.organizations.find_one({"id": user["org_id"]})
    
    access_token = create_access_token(data={"sub": user["id"]})
    
    user_response = UserResponse(
        id=user["id"],
        email=user["email"],
        name=user["name"],
        org_id=user["org_id"],
        role=user["role"],
        organization_name=org["name"] if org else "",
        industry=org["industry"] if org else ""
    )
    
    return Token(access_token=access_token, token_type="bearer", user=user_response)

@api_router.get("/auth/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    org = await db.organizations.find_one({"id": current_user.org_id})
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        org_id=current_user.org_id,
        role=current_user.role,
        organization_name=org["name"] if org else "",
        industry=org["industry"] if org else ""
    )

# Assessment endpoints
@api_router.post("/assessments", response_model=dict)
async def create_assessment(current_user: User = Depends(get_current_user)):
    org = await db.organizations.find_one({"id": current_user.org_id})
    org_name = org["name"] if org else "Unknown"
    
    # Generate assessment name: <Org>_<YYYY-MM-DD_HHMM>
    now = datetime.now(timezone.utc)
    assessment_name = f"{org_name}_{now.strftime('%Y-%m-%d_%H%M')}"
    
    assessment = Assessment(
        org_id=current_user.org_id,
        user_id=current_user.id,
        name=assessment_name
    )
    
    await db.assessments.insert_one(assessment.dict())
    return {"id": assessment.id, "name": assessment_name}

@api_router.get("/assessments", response_model=List[AssessmentResponse])
async def get_assessments(current_user: User = Depends(get_current_user)):
    assessments = await db.assessments.find({"user_id": current_user.id}).to_list(length=None)
    
    # Get total questions count
    total_questions = await db.questions.count_documents({})
    
    result = []
    for assessment in assessments:
        result.append(AssessmentResponse(
            id=assessment["id"],
            name=assessment["name"],
            status=assessment["status"],
            started_at=assessment["started_at"],
            completed_at=assessment.get("completed_at"),
            progress=assessment["progress"],
            total_questions=total_questions
        ))
    
    return result

@api_router.get("/assessments/{assessment_id}")
async def get_assessment(assessment_id: str, current_user: User = Depends(get_current_user)):
    assessment = await db.assessments.find_one({"id": assessment_id, "user_id": current_user.id})
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Get all questions with domain info
    questions = await db.questions.find().sort("order").to_list(length=None)
    domains = await db.domains.find().sort("order").to_list(length=None)
    
    # Get existing answers
    answers = await db.answers.find({"assessment_id": assessment_id}).to_list(length=None)
    answer_map = {answer["question_id"]: answer for answer in answers}
    
    # Build response
    domain_map = {domain["id"]: domain for domain in domains}
    
    questions_with_answers = []
    for question in questions:
        domain = domain_map.get(question["domain_id"])
        question_data = {
            "id": question["id"],
            "code": question["code"],
            "text": question["text"],
            "help_text": question.get("help_text"),
            "domain_name": domain["name"] if domain else "Unknown",
            "domain_id": question["domain_id"],
            "order": question["order"],
            "answer": answer_map.get(question["id"])
        }
        questions_with_answers.append(question_data)
    
    return {
        "assessment": assessment,
        "questions": questions_with_answers,
        "domains": domains,
        "progress": f"{len(answers)}/{len(questions)}"
    }

@api_router.patch("/assessments/{assessment_id}/answer")
async def save_answer(assessment_id: str, answer_data: AnswerSubmit, current_user: User = Depends(get_current_user)):
    # Verify assessment belongs to user
    assessment = await db.assessments.find_one({"id": assessment_id, "user_id": current_user.id})
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Verify question exists
    question = await db.questions.find_one({"id": answer_data.question_id})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Calculate numeric score
    numeric_score = SCORING_MAP[answer_data.option]
    
    # Upsert answer
    answer = Answer(
        assessment_id=assessment_id,
        question_id=answer_data.question_id,
        option=answer_data.option,
        numeric_score=numeric_score,
        note=answer_data.note
    )
    
    await db.answers.replace_one(
        {"assessment_id": assessment_id, "question_id": answer_data.question_id},
        answer.dict(),
        upsert=True
    )
    
    # Update assessment progress
    total_answers = await db.answers.count_documents({"assessment_id": assessment_id})
    await db.assessments.update_one(
        {"id": assessment_id},
        {"$set": {"progress": total_answers}}
    )
    
    return {"saved": True, "score": numeric_score}

@api_router.post("/assessments/{assessment_id}/submit")
async def submit_assessment(assessment_id: str, current_user: User = Depends(get_current_user)):
    # Verify assessment belongs to user
    assessment = await db.assessments.find_one({"id": assessment_id, "user_id": current_user.id})
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Check if all questions are answered
    total_questions = await db.questions.count_documents({})
    total_answers = await db.answers.count_documents({"assessment_id": assessment_id})
    
    if total_answers < total_questions:
        raise HTTPException(status_code=400, detail=f"Please answer all questions ({total_answers}/{total_questions} completed)")
    
    # Update assessment status
    await db.assessments.update_one(
        {"id": assessment_id},
        {
            "$set": {
                "status": AssessmentStatus.COMPLETED,
                "completed_at": datetime.now(timezone.utc)
            }
        }
    )
    
    return {"status": "COMPLETED"}

@api_router.get("/assessments/{assessment_id}/summary", response_model=AssessmentSummary)
async def get_assessment_summary(assessment_id: str, current_user: User = Depends(get_current_user)):
    # Verify assessment belongs to user and is completed
    assessment = await db.assessments.find_one({"id": assessment_id, "user_id": current_user.id})
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Get all domains, questions, and answers
    domains = await db.domains.find().sort("order").to_list(length=None)
    questions = await db.questions.find().to_list(length=None)
    answers = await db.answers.find({"assessment_id": assessment_id}).to_list(length=None)
    
    # Group questions by domain
    domain_questions = {}
    for question in questions:
        domain_id = question["domain_id"]
        if domain_id not in domain_questions:
            domain_questions[domain_id] = []
        domain_questions[domain_id].append(question)
    
    # Group answers by question
    answer_map = {answer["question_id"]: answer for answer in answers}
    
    # Calculate domain scores
    domain_scores = []
    total_score = 0
    total_max_score = 0
    
    for domain in domains:
        domain_id = domain["id"]
        domain_questions_list = domain_questions.get(domain_id, [])
        
        if not domain_questions_list:
            continue
            
        domain_score = 0
        domain_max_score = len(domain_questions_list) * 3  # Max score per question is 3
        
        for question in domain_questions_list:
            answer = answer_map.get(question["id"])
            if answer:
                domain_score += answer["numeric_score"]
        
        domain_percentage = (domain_score / domain_max_score * 100) if domain_max_score > 0 else 0
        
        domain_scores.append(DomainScore(
            domain_id=domain_id,
            domain_name=domain["name"],
            score=domain_score,
            max_score=domain_max_score,
            percentage=round(domain_percentage, 1)
        ))
        
        total_score += domain_score
        total_max_score += domain_max_score
    
    # Calculate overall percentage
    overall_percentage = (total_score / total_max_score * 100) if total_max_score > 0 else 0
    overall_maturity = get_maturity_level(overall_percentage)
    
    # Sort domains by score (descending)
    domain_scores.sort(key=lambda x: x.percentage, reverse=True)
    
    return AssessmentSummary(
        overall_percentage=round(overall_percentage, 1),
        overall_maturity=overall_maturity,
        domain_scores=domain_scores,
        total_questions=len(questions),
        answered_questions=len(answers)
    )

@api_router.post("/reports/{assessment_id}/pdf")
async def generate_pdf_report(assessment_id: str, current_user: User = Depends(get_current_user)):
    # Verify assessment belongs to user
    assessment = await db.assessments.find_one({"id": assessment_id, "user_id": current_user.id})
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # For MVP, return static PDF link
    static_pdf_url = "https://example.com/static-sample-report.pdf"
    
    # Save report record
    report = Report(
        assessment_id=assessment_id,
        url=static_pdf_url
    )
    
    await db.reports.insert_one(report.dict())
    
    return {"url": static_pdf_url}

# Admin endpoints
@api_router.get("/domains", response_model=List[Domain])
async def get_domains():
    domains = await db.domains.find().sort("order").to_list(length=None)
    return [Domain(**domain) for domain in domains]

@api_router.get("/questions")
async def get_questions(domain_id: Optional[str] = None):
    query = {"domain_id": domain_id} if domain_id else {}
    questions = await db.questions.find(query).sort("order").to_list(length=None)
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
    
    logger.info("Seeding database with initial data...")
    
    # Pre-defined industries
    industries = [
        "Technology", "Healthcare", "Financial Services", "Manufacturing", 
        "Education", "Government", "Retail", "Consulting", "Other"
    ]
    
    # Seed domains (MVP subset)
    domains_data = [
        {"name": "Fairness", "order": 1, "description": "Bias identification and mitigation in AI systems"},
        {"name": "Accountability", "order": 2, "description": "Governance structures and responsibility frameworks"},
        {"name": "Security", "order": 3, "description": "Protection against threats and vulnerabilities"}
    ]
    
    domains = []
    for domain_data in domains_data:
        domain = Domain(**domain_data)
        domains.append(domain)
        await db.domains.insert_one(domain.dict())
    
    # Seed questions (4 per domain for MVP)
    questions_data = [
        # Fairness Domain
        {
            "domain_id": domains[0].id,
            "code": "FA-1",
            "text": "What measures have you implemented to identify and mitigate biases in your AI system?",
            "help_text": "Bias in AI systems can lead to unfair treatment or exclusion of certain groups. This question seeks to determine what proactive steps you've taken to identify and reduce biases.",
            "order": 1
        },
        {
            "domain_id": domains[0].id,
            "code": "FA-2",
            "text": "How do you ensure your training data is representative of the populations your AI system serves?",
            "help_text": "Representative training data is crucial for fair AI outcomes across different demographic groups.",
            "order": 2
        },
        {
            "domain_id": domains[0].id,
            "code": "FA-3",
            "text": "What processes are in place to regularly audit your AI system for fairness across different user groups?",
            "help_text": "Regular fairness audits help ensure your AI system continues to treat all users fairly over time.",
            "order": 3
        },
        {
            "domain_id": domains[0].id,
            "code": "FA-4",
            "text": "How do you handle cases where fairness conflicts with other objectives like accuracy or efficiency?",
            "help_text": "Trade-offs between fairness and other metrics require careful consideration and clear policies.",
            "order": 4
        },
        
        # Accountability Domain
        {
            "domain_id": domains[1].id,
            "code": "AC-1",
            "text": "What governance structures are in place to monitor AI outcomes and decisions?",
            "help_text": "Governance structures provide oversight and ensure AI systems operate within ethical and legal standards.",
            "order": 1
        },
        {
            "domain_id": domains[1].id,
            "code": "AC-2",
            "text": "How are roles and responsibilities defined for AI system development and deployment?",
            "help_text": "Clear roles and responsibilities ensure accountability throughout the AI lifecycle.",
            "order": 2
        },
        {
            "domain_id": domains[1].id,
            "code": "AC-3",
            "text": "What documentation and audit trails are maintained for AI decision-making processes?",
            "help_text": "Proper documentation enables accountability and supports compliance requirements.",
            "order": 3
        },
        {
            "domain_id": domains[1].id,
            "code": "AC-4",
            "text": "How do you handle complaints or appeals related to AI-driven decisions?",
            "help_text": "A clear process for handling complaints ensures users have recourse when AI decisions affect them.",
            "order": 4
        },
        
        # Security Domain
        {
            "domain_id": domains[2].id,
            "code": "SE-1",
            "text": "What security measures protect your AI models from adversarial attacks?",
            "help_text": "Adversarial attacks can manipulate AI models to produce incorrect or harmful outputs.",
            "order": 1
        },
        {
            "domain_id": domains[2].id,
            "code": "SE-2",
            "text": "How do you secure the data used for training and inference in your AI systems?",
            "help_text": "Data security is crucial to prevent unauthorized access and maintain system integrity.",
            "order": 2
        },
        {
            "domain_id": domains[2].id,
            "code": "SE-3",
            "text": "What access controls and authentication mechanisms are implemented for your AI systems?",
            "help_text": "Proper access controls prevent unauthorized use and potential security breaches.",
            "order": 3
        },
        {
            "domain_id": domains[2].id,
            "code": "SE-4",
            "text": "How do you monitor and respond to security incidents involving your AI systems?",
            "help_text": "Incident response procedures ensure quick action when security threats are detected.",
            "order": 4
        }
    ]
    
    for question_data in questions_data:
        question = Question(**question_data)
        await db.questions.insert_one(question.dict())
    
    logger.info(f"Database seeded with {len(domains)} domains and {len(questions_data)} questions")
