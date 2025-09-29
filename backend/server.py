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
    predefined_answers: List[str] = []
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
    
    # Get all questions with domain info, sorted domain by domain
    domains = await db.domains.find({}, {"_id": 0}).sort("order").to_list(length=None)
    questions = await db.questions.find({}, {"_id": 0}).sort([("domain_id", 1), ("order", 1)]).to_list(length=None)
    
    # Group questions by domain for domain-by-domain progression
    domain_questions = {}
    for domain in domains:
        domain_questions[domain["id"]] = []
    
    for question in questions:
        if question["domain_id"] in domain_questions:
            domain_questions[question["domain_id"]].append(question)
    
    # Flatten questions in domain order
    ordered_questions = []
    for domain in domains:
        ordered_questions.extend(domain_questions[domain["id"]])
    
    # Get existing answers
    answers = await db.answers.find({"assessment_id": assessment_id}, {"_id": 0}).to_list(length=None)
    answer_map = {answer["question_id"]: answer for answer in answers}
    
    # Build response with domain-grouped structure
    domain_map = {domain["id"]: domain for domain in domains}
    
    questions_with_answers = []
    for question in ordered_questions:
        domain = domain_map.get(question["domain_id"])
        question_data = {
            "id": question["id"],
            "code": question["code"],
            "text": question["text"],
            "help_text": question.get("help_text"),
            "predefined_answers": question.get("predefined_answers", []),
            "domain_name": domain["name"] if domain else "Unknown",
            "domain_id": question["domain_id"],
            "domain_order": domain["order"] if domain else 0,
            "order": question["order"],
            "answer": answer_map.get(question["id"])
        }
        questions_with_answers.append(question_data)
    
    # Remove _id from assessment
    if "_id" in assessment:
        del assessment["_id"]
    
    return {
        "assessment": assessment,
        "questions": questions_with_answers,
        "domains": domains,
        "progress": f"{len(answers)}/{len(questions)}"
    }

@api_router.get("/assessments/{assessment_id}/status")
async def get_assessment_status(assessment_id: str, current_user: User = Depends(get_current_user)):
    """Get simplified status overview for all questions"""
    assessment = await db.assessments.find_one({"id": assessment_id, "user_id": current_user.id})
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Get domains and questions
    domains = await db.domains.find({}, {"_id": 0}).sort("order").to_list(length=None)
    questions = await db.questions.find({}, {"_id": 0}).sort([("domain_id", 1), ("order", 1)]).to_list(length=None)
    
    # Get answers
    answers = await db.answers.find({"assessment_id": assessment_id}, {"_id": 0}).to_list(length=None)
    answered_question_ids = {answer["question_id"] for answer in answers}
    
    # Build status overview
    domain_map = {domain["id"]: domain for domain in domains}
    status_overview = []
    
    for domain in domains:
        domain_questions = [q for q in questions if q["domain_id"] == domain["id"]]
        domain_status = {
            "domain_name": domain["name"],
            "domain_order": domain["order"],
            "questions": []
        }
        
        for question in domain_questions:
            question_status = {
                "question_id": question["id"],
                "question_code": question["code"],
                "answered": question["id"] in answered_question_ids
            }
            domain_status["questions"].append(question_status)
        
        status_overview.append(domain_status)
    
    return {
        "status_overview": status_overview,
        "total_questions": len(questions),
        "answered_questions": len(answers),
        "completion_percentage": round((len(answers) / len(questions)) * 100, 1) if questions else 0
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
    domains = await db.domains.find({}, {"_id": 0}).sort("order").to_list(length=None)
    questions = await db.questions.find({}, {"_id": 0}).to_list(length=None)
    answers = await db.answers.find({"assessment_id": assessment_id}, {"_id": 0}).to_list(length=None)
    
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
    
    # Complete question set - all 88 questions from the spreadsheet
    questions_data = [
        # Fairness Domain (FA-1 to FA-8)
        {
            "domain_id": domains[0].id,
            "code": "FA-1",
            "text": "What measures have you implemented to identify and mitigate biases in your AI system?",
            "help_text": "Bias in AI systems can lead to unfair treatment or exclusion of certain groups, undermining the credibility and effectiveness of the system.",
            "order": 1
        },
        {
            "domain_id": domains[0].id,
            "code": "FA-2",
            "text": "How do you ensure the training data represents all relevant demographics or groups?",
            "help_text": "Representative training data is crucial for ensuring fair outcomes across different demographic groups.",
            "order": 2
        },
        {
            "domain_id": domains[0].id,
            "code": "FA-3",
            "text": "Have you evaluated the system's outputs for potential disparities across user groups?",
            "help_text": "Regular evaluation of system outputs helps identify and address potential disparities that may affect different user groups unfairly.",
            "order": 3
        },
        {
            "domain_id": domains[0].id,
            "code": "FA-4",
            "text": "How do you measure fairness in your AI system's outputs?",
            "help_text": "Quantitative fairness metrics help objectively assess whether the AI system treats different groups equitably.",
            "order": 4
        },
        {
            "domain_id": domains[0].id,
            "code": "FA-5",
            "text": "Have you tested the system for potential biases in real-world scenarios?",
            "help_text": "Real-world testing helps identify biases that may not be apparent in controlled environments but emerge in practical applications.",
            "order": 5
        },
        {
            "domain_id": domains[0].id,
            "code": "FA-6",
            "text": "Are you using any frameworks or tools (e.g., Fairlearn) to assess and mitigate bias?",
            "help_text": "Specialized tools and frameworks provide systematic approaches to bias detection and mitigation in AI systems.",
            "order": 6
        },
        {
            "domain_id": domains[0].id,
            "code": "FA-7",
            "text": "How do you ensure fairness in decision-making for minority or underserved groups?",
            "help_text": "Special attention to minority and underserved groups helps prevent AI systems from perpetuating or amplifying existing inequalities.",
            "order": 7
        },
        {
            "domain_id": domains[0].id,
            "code": "FA-8",
            "text": "Is fairness embedded in your AI model's design process, or is it addressed post-deployment?",
            "help_text": "Integrating fairness considerations early in the design process is more effective than addressing fairness issues after deployment.",
            "order": 8
        },
        
        # Transparency Domain (TR-1 to TR-8)
        {
            "domain_id": domains[1].id,
            "code": "TR-1",
            "text": "What level of detail about the AI system's functionality and limitations is communicated to users or stakeholders?",
            "help_text": "Clear communication about system capabilities and limitations helps users understand what to expect and how to use the system appropriately.",
            "order": 1
        },
        {
            "domain_id": domains[1].id,
            "code": "TR-2",
            "text": "How do you document the data sources, algorithms, and processes used in your AI system?",
            "help_text": "Comprehensive documentation ensures traceability and enables others to understand, validate, and reproduce the AI system's behavior.",
            "order": 2
        },
        {
            "domain_id": domains[1].id,
            "code": "TR-3",
            "text": "Are there mechanisms for external parties (e.g., regulators or customers) to understand how your AI system works?",
            "help_text": "External transparency mechanisms enable regulatory compliance and build trust with customers and stakeholders.",
            "order": 3
        },
        {
            "domain_id": domains[1].id,
            "code": "TR-4",
            "text": "How is information about your AI system shared with internal teams and external stakeholders?",
            "help_text": "Structured information sharing ensures that all relevant parties have appropriate access to AI system information.",
            "order": 4
        },
        {
            "domain_id": domains[1].id,
            "code": "TR-5",
            "text": "Are there any \"black-box\" components in your system that could impede transparency?",
            "help_text": "Black-box components can reduce system transparency and make it difficult to understand how decisions are made.",
            "order": 5
        },
        {
            "domain_id": domains[1].id,
            "code": "TR-6",
            "text": "How do you disclose the sources of data and algorithms used in the AI system?",
            "help_text": "Disclosure of data sources and algorithms helps stakeholders understand the foundation and methodology behind AI decisions.",
            "order": 6
        },
        {
            "domain_id": domains[1].id,
            "code": "TR-7",
            "text": "Are users made aware when they are interacting with an AI system?",
            "help_text": "User awareness of AI interaction is important for informed consent and appropriate expectations about system capabilities.",
            "order": 7
        },
        {
            "domain_id": domains[1].id,
            "code": "TR-8",
            "text": "Do you publish any transparency reports or documentation for regulators or customers?",
            "help_text": "Regular transparency reports demonstrate commitment to openness and provide stakeholders with systematic information about AI governance.",
            "order": 8
        },
        
        # Explainability Domain (EX-1 to EX-8)
        {
            "domain_id": domains[2].id,
            "code": "EX-1",
            "text": "How do you decide the level of explainability required for your AI system?",
            "help_text": "The required level of explainability should be determined based on the system's impact, audience, and potential for harm.",
            "order": 1
        },
        {
            "domain_id": domains[2].id,
            "code": "EX-2",
            "text": "What methods are used to test whether explanations are understandable by non-technical users?",
            "help_text": "Testing explanation comprehensibility ensures that AI system explanations are accessible to their intended audiences.",
            "order": 2
        },
        {
            "domain_id": domains[2].id,
            "code": "EX-3",
            "text": "Do you provide explanations in different formats (e.g., visualizations, text summaries) for different audiences?",
            "help_text": "Different audiences may require different explanation formats to effectively understand AI system behavior and decisions.",
            "order": 3
        },
        {
            "domain_id": domains[2].id,
            "code": "EX-4",
            "text": "How do you evaluate the accuracy and completeness of the explanations provided?",
            "help_text": "Explanation accuracy and completeness are crucial for building trust and enabling proper understanding of AI decisions.",
            "order": 4
        },
        {
            "domain_id": domains[2].id,
            "code": "EX-5",
            "text": "Are there trade-offs between model complexity and explainability in your system design?",
            "help_text": "Understanding and managing trade-offs between model performance and explainability is important for system design decisions.",
            "order": 5
        },
        {
            "domain_id": domains[2].id,
            "code": "EX-6",
            "text": "How do you ensure the decisions made by your AI system are interpretable by users?",
            "help_text": "Interpretable AI decisions help users understand the reasoning behind outcomes and build confidence in the system.",
            "order": 6
        },
        {
            "domain_id": domains[2].id,
            "code": "EX-7",
            "text": "What tools or techniques (e.g., SHAP, LIME) do you use to make complex models more explainable?",
            "help_text": "Explainability tools and techniques can help make complex AI models more interpretable and trustworthy.",
            "order": 7
        },
        {
            "domain_id": domains[2].id,
            "code": "EX-8",
            "text": "Are there specific groups (e.g., end-users, regulators, or internal teams) for whom explanations of AI outputs are tailored?",
            "help_text": "Tailored explanations for different stakeholder groups ensure that each audience receives appropriate and useful information.",
            "order": 8
        },
        
        # Accountability Domain (AC-1 to AC-8)
        {
            "domain_id": domains[3].id,
            "code": "AC-1",
            "text": "How is accountability for AI system failures managed within your organization?",
            "help_text": "Clear accountability structures ensure that responsibility for AI system failures is properly assigned and managed.",
            "order": 1
        },
        {
            "domain_id": domains[3].id,
            "code": "AC-2",
            "text": "What governance structures (e.g., AI oversight boards) are in place to monitor AI outcomes?",
            "help_text": "Governance structures provide systematic oversight and monitoring of AI system outcomes and ethical implications.",
            "order": 2
        },
        {
            "domain_id": domains[3].id,
            "code": "AC-3",
            "text": "Are there policies for escalating issues identified in the AI system?",
            "help_text": "Clear escalation policies ensure that AI system issues are promptly addressed by appropriate personnel.",
            "order": 3
        },
        {
            "domain_id": domains[3].id,
            "code": "AC-4",
            "text": "How do you handle customer complaints or disputes related to AI outputs?",
            "help_text": "Effective complaint handling processes ensure fair resolution of disputes related to AI system decisions.",
            "order": 4
        },
        {
            "domain_id": domains[3].id,
            "code": "AC-5",
            "text": "Are roles and responsibilities for AI governance clearly defined across teams?",
            "help_text": "Clear role definitions ensure that all aspects of AI governance are properly covered and accountable.",
            "order": 5
        },
        {
            "domain_id": domains[3].id,
            "code": "AC-6",
            "text": "Who is responsible for monitoring and managing the AI system throughout its lifecycle?",
            "help_text": "Designated responsibility for AI system lifecycle management ensures continuous oversight and maintenance.",
            "order": 6
        },
        {
            "domain_id": domains[3].id,
            "code": "AC-7",
            "text": "Are there audit trails or logs that document the AI system's decision-making process?",
            "help_text": "Audit trails enable reconstruction and understanding of AI system decisions for accountability and debugging purposes.",
            "order": 7
        },
        {
            "domain_id": domains[3].id,
            "code": "AC-8",
            "text": "What mechanisms are in place to address disputes or concerns about the system's outcomes?",
            "help_text": "Formal mechanisms for addressing disputes ensure that stakeholders have recourse when they disagree with AI system outcomes.",
            "order": 8
        },
        
        # Data Integrity Domain (DI-1 to DI-8)
        {
            "domain_id": domains[4].id,
            "code": "DI-1",
            "text": "How do you validate the accuracy, completeness, and quality of the data used in your AI systems?",
            "help_text": "Data validation ensures that AI systems are built on reliable and high-quality information foundations.",
            "order": 1
        },
        {
            "domain_id": domains[4].id,
            "code": "DI-2",
            "text": "What processes do you have for managing data lineage and tracking changes to data over time?",
            "help_text": "Data lineage management enables traceability and understanding of how data flows through AI systems.",
            "order": 2
        },
        {
            "domain_id": domains[4].id,
            "code": "DI-3",
            "text": "Are there governance policies for data collection, usage, retention, and disposal?",
            "help_text": "Data governance policies ensure proper management of data throughout its lifecycle in AI systems.",
            "order": 3
        },
        {
            "domain_id": domains[4].id,
            "code": "DI-4",
            "text": "How do you ensure the data used in your AI systems is up-to-date and accurate?",
            "help_text": "Current and accurate data is essential for maintaining AI system performance and relevance.",
            "order": 4
        },
        {
            "domain_id": domains[4].id,
            "code": "DI-5",
            "text": "What processes are in place to address missing or incomplete data?",
            "help_text": "Proper handling of missing data prevents AI systems from making decisions based on incomplete information.",
            "order": 5
        },
        {
            "domain_id": domains[4].id,
            "code": "DI-6",
            "text": "How do you manage data preprocessing (e.g., cleaning, normalization)?",
            "help_text": "Consistent data preprocessing ensures that AI models receive properly formatted and cleaned input data.",
            "order": 6
        },
        {
            "domain_id": domains[4].id,
            "code": "DI-7",
            "text": "Are third-party data sources evaluated for quality and reliability?",
            "help_text": "Evaluation of external data sources helps ensure that AI systems are not compromised by poor-quality third-party data.",
            "order": 7
        },
        {
            "domain_id": domains[4].id,
            "code": "DI-8",
            "text": "How do you track data lineage to ensure traceability across the AI lifecycle?",
            "help_text": "Data lineage tracking enables full traceability of data from origin through processing to AI system deployment.",
            "order": 8
        },
        
        # Reliability Domain (RE-1 to RE-8)
        {
            "domain_id": domains[5].id,
            "code": "RE-1",
            "text": "How do you test the AI system to ensure consistent performance under different conditions?",
            "help_text": "Comprehensive testing across various conditions helps ensure that AI systems perform reliably in real-world scenarios.",
            "order": 1
        },
        {
            "domain_id": domains[5].id,
            "code": "RE-2",
            "text": "Have you conducted stress tests or simulations to evaluate the system's robustness?",
            "help_text": "Stress testing helps identify potential failure points and evaluate system behavior under extreme conditions.",
            "order": 2
        },
        {
            "domain_id": domains[5].id,
            "code": "RE-3",
            "text": "What mechanisms are in place to monitor the system for issues like model drift or degradation?",
            "help_text": "Continuous monitoring helps detect when AI system performance degrades or when the model becomes less accurate over time.",
            "order": 3
        },
        {
            "domain_id": domains[5].id,
            "code": "RE-4",
            "text": "How do you define success metrics for the reliability of your AI system?",
            "help_text": "Clear reliability metrics help objectively assess and track AI system performance over time.",
            "order": 4
        },
        {
            "domain_id": domains[5].id,
            "code": "RE-5",
            "text": "Have you identified potential failure points in the system?",
            "help_text": "Identifying potential failure points enables proactive measures to prevent or mitigate system failures.",
            "order": 5
        },
        {
            "domain_id": domains[5].id,
            "code": "RE-6",
            "text": "How do you ensure the system performs consistently under varying conditions (e.g., edge cases)?",
            "help_text": "Consistent performance across varying conditions, including edge cases, is crucial for reliable AI systems.",
            "order": 6
        },
        {
            "domain_id": domains[5].id,
            "code": "RE-7",
            "text": "Are there mechanisms for detecting and addressing system downtime or errors?",
            "help_text": "Rapid detection and response to system issues minimize the impact of downtime and errors on users.",
            "order": 7
        },
        {
            "domain_id": domains[5].id,
            "code": "RE-8",
            "text": "How often is the AI model tested and retrained to maintain reliability?",
            "help_text": "Regular testing and retraining help maintain AI system performance as data and conditions change over time.",
            "order": 8
        },
        
        # Security Domain (SE-1 to SE-8)
        {
            "domain_id": domains[6].id,
            "code": "SE-1",
            "text": "What measures are in place to protect your AI models and data from unauthorized access or tampering?",
            "help_text": "Comprehensive security measures protect AI assets from unauthorized access and malicious tampering.",
            "order": 1
        },
        {
            "domain_id": domains[6].id,
            "code": "SE-2",
            "text": "How do you handle adversarial risks, such as attacks designed to manipulate the AI's outputs?",
            "help_text": "Adversarial attack protection helps prevent malicious actors from manipulating AI system outputs.",
            "order": 2
        },
        {
            "domain_id": domains[6].id,
            "code": "SE-3",
            "text": "Do you conduct regular security audits or penetration testing on your AI systems?",
            "help_text": "Regular security assessments help identify and address vulnerabilities in AI systems before they can be exploited.",
            "order": 3
        },
        {
            "domain_id": domains[6].id,
            "code": "SE-4",
            "text": "How do you secure the AI model during training, deployment, and operation?",
            "help_text": "End-to-end security across the AI lifecycle protects against threats at every stage of system development and operation.",
            "order": 4
        },
        {
            "domain_id": domains[6].id,
            "code": "SE-5",
            "text": "Are there safeguards to prevent unauthorized modifications to the AI model?",
            "help_text": "Model integrity safeguards prevent unauthorized changes that could compromise AI system performance or security.",
            "order": 5
        },
        {
            "domain_id": domains[6].id,
            "code": "SE-6",
            "text": "What measures are in place to protect the system against adversarial attacks (e.g., input manipulation)?",
            "help_text": "Input validation and adversarial defenses help protect AI systems from attacks that manipulate inputs to cause incorrect outputs.",
            "order": 6
        },
        {
            "domain_id": domains[6].id,
            "code": "SE-7",
            "text": "How do you protect sensitive data in your AI pipelines (e.g., encryption, tokenization)?",
            "help_text": "Data protection throughout AI pipelines ensures that sensitive information remains secure during processing.",
            "order": 7
        },
        {
            "domain_id": domains[6].id,
            "code": "SE-8",
            "text": "Are there regular vulnerability assessments and penetration tests performed on the AI system?",
            "help_text": "Ongoing security testing helps maintain system security as threats and vulnerabilities evolve.",
            "order": 8
        },
        
        # Privacy Domain (PR-1 to PR-8)
        {
            "domain_id": domains[7].id,
            "code": "PR-1",
            "text": "How do you ensure compliance with data privacy laws, such as GDPR or the Australian Privacy Act?",
            "help_text": "Privacy law compliance is essential for legal operation and protecting individual privacy rights in AI systems.",
            "order": 1
        },
        {
            "domain_id": domains[7].id,
            "code": "PR-2",
            "text": "What techniques (e.g., anonymization, pseudonymization) do you use to protect personal data in your AI workflows?",
            "help_text": "Privacy-preserving techniques help protect personal data while still enabling AI system functionality.",
            "order": 2
        },
        {
            "domain_id": domains[7].id,
            "code": "PR-3",
            "text": "How do you manage user consent for data collection and processing?",
            "help_text": "Proper consent management ensures that personal data is collected and used only with appropriate user permission.",
            "order": 3
        },
        {
            "domain_id": domains[7].id,
            "code": "PR-4",
            "text": "How do you ensure that personal data is not used beyond its original purpose?",
            "help_text": "Purpose limitation prevents misuse of personal data and maintains user trust in AI systems.",
            "order": 4
        },
        {
            "domain_id": domains[7].id,
            "code": "PR-5",
            "text": "What methods do you use to anonymize or pseudonymize personal data?",
            "help_text": "Effective anonymization and pseudonymization techniques help protect individual privacy while preserving data utility.",
            "order": 5
        },
        {
            "domain_id": domains[7].id,
            "code": "PR-6",
            "text": "How do you monitor and prevent privacy violations during system operation?",
            "help_text": "Continuous privacy monitoring helps detect and prevent privacy violations before they impact individuals.",
            "order": 6
        },
        {
            "domain_id": domains[7].id,
            "code": "PR-7",
            "text": "Are privacy risks evaluated during both the development and deployment phases?",
            "help_text": "Privacy risk assessment throughout the AI lifecycle helps identify and mitigate privacy concerns early.",
            "order": 7
        },
        {
            "domain_id": domains[7].id,
            "code": "PR-8",
            "text": "What steps are taken to ensure compliance with cross-border data protection laws?",
            "help_text": "Cross-border compliance ensures that AI systems meet privacy requirements across different jurisdictions.",
            "order": 8
        },
        
        # Safety Domain (SA-1 to SA-8)
        {
            "domain_id": domains[8].id,
            "code": "SA-1",
            "text": "Have you conducted a safety impact assessment for the AI system?",
            "help_text": "Safety impact assessments help identify potential risks and harms associated with AI system deployment.",
            "order": 1
        },
        {
            "domain_id": domains[8].id,
            "code": "SA-2",
            "text": "How do you ensure that the system does not cause harm in unintended ways?",
            "help_text": "Proactive harm prevention measures help ensure that AI systems do not cause unintended negative consequences.",
            "order": 2
        },
        {
            "domain_id": domains[8].id,
            "code": "SA-3",
            "text": "Are there monitoring tools in place to detect unsafe system behavior in real-time?",
            "help_text": "Real-time safety monitoring enables rapid detection and response to potentially harmful AI system behavior.",
            "order": 3
        },
        {
            "domain_id": domains[8].id,
            "code": "SA-4",
            "text": "How do you handle situations where the system's actions conflict with human safety requirements?",
            "help_text": "Clear protocols for safety conflicts ensure that human safety is prioritized when AI decisions may cause harm.",
            "order": 4
        },
        {
            "domain_id": domains[8].id,
            "code": "SA-5",
            "text": "Are there emergency protocols for shutting down the system in case of unsafe behavior?",
            "help_text": "Emergency shutdown procedures ensure that dangerous AI systems can be quickly deactivated to prevent harm.",
            "order": 5
        },
        {
            "domain_id": domains[8].id,
            "code": "SA-6",
            "text": "What steps have you taken to identify and mitigate potential risks or harm caused by the AI system?",
            "help_text": "Systematic risk identification and mitigation help prevent AI systems from causing harm to users or society.",
            "order": 6
        },
        {
            "domain_id": domains[8].id,
            "code": "SA-7",
            "text": "Are there fail-safe mechanisms or redundancies in place to address unexpected system behaviors?",
            "help_text": "Fail-safe mechanisms provide backup protections when AI systems behave unexpectedly or experience failures.",
            "order": 7
        },
        {
            "domain_id": domains[8].id,
            "code": "SA-8",
            "text": "Have you conducted safety testing in realistic or high-risk scenarios?",
            "help_text": "Realistic safety testing helps validate that AI systems can operate safely in challenging real-world conditions.",
            "order": 8
        },
        
        # Inclusivity Domain (IN-1 to IN-8)
        {
            "domain_id": domains[9].id,
            "code": "IN-1",
            "text": "How do you ensure your AI system is accessible to a diverse range of users, including those with disabilities or in underserved populations?",
            "help_text": "Accessibility design ensures that AI systems can be used effectively by people with diverse abilities and backgrounds.",
            "order": 1
        },
        {
            "domain_id": domains[9].id,
            "code": "IN-2",
            "text": "Were diverse perspectives considered during the design and development of the system?",
            "help_text": "Diverse perspectives in development help create AI systems that work well for different user groups and use cases.",
            "order": 2
        },
        {
            "domain_id": domains[9].id,
            "code": "IN-3",
            "text": "Have you audited the system for potential exclusionary outcomes or unintended impacts?",
            "help_text": "Regular audits help identify when AI systems may inadvertently exclude or negatively impact certain user groups.",
            "order": 3
        },
        {
            "domain_id": domains[9].id,
            "code": "IN-4",
            "text": "How do you ensure your AI system accounts for accessibility requirements (e.g., for users with disabilities)?",
            "help_text": "Accessibility requirements ensure that AI systems can be used by people with various disabilities and assistive technologies.",
            "order": 4
        },
        {
            "domain_id": domains[9].id,
            "code": "IN-5",
            "text": "Are stakeholders from diverse backgrounds involved in the design and testing of the system?",
            "help_text": "Diverse stakeholder involvement helps ensure that AI systems meet the needs of different user communities.",
            "order": 5
        },
        {
            "domain_id": domains[9].id,
            "code": "IN-6",
            "text": "What steps are taken to ensure that the AI system serves underrepresented communities effectively?",
            "help_text": "Specific measures for underrepresented communities help prevent AI systems from perpetuating or amplifying existing inequalities.",
            "order": 6
        },
        {
            "domain_id": domains[9].id,
            "code": "IN-7",
            "text": "Are language, cultural, or regional differences considered in system design?",
            "help_text": "Cultural and linguistic considerations help ensure that AI systems work effectively across diverse global populations.",
            "order": 7
        },
        {
            "domain_id": domains[9].id,
            "code": "IN-8",
            "text": "How do you evaluate whether the system is unintentionally excluding certain user groups?",
            "help_text": "Regular evaluation for exclusion helps identify and correct AI system behaviors that may inadvertently discriminate.",
            "order": 8
        },
        
        # Sustainability Domain (SU-1 to SU-8)
        {
            "domain_id": domains[10].id,
            "code": "SU-1",
            "text": "What is the environmental impact of training and deploying your AI system (e.g., energy usage, carbon footprint)?",
            "help_text": "Understanding environmental impact helps organizations make informed decisions about AI system development and deployment.",
            "order": 1
        },
        {
            "domain_id": domains[10].id,
            "code": "SU-2",
            "text": "Have you explored opportunities to optimize algorithms for greater computational efficiency?",
            "help_text": "Algorithm optimization can reduce computational resources required and minimize environmental impact of AI systems.",
            "order": 2
        },
        {
            "domain_id": domains[10].id,
            "code": "SU-3",
            "text": "Are you using cloud services or infrastructure that prioritizes renewable energy sources?",
            "help_text": "Choosing renewable energy infrastructure helps reduce the carbon footprint of AI system operations.",
            "order": 3
        },
        {
            "domain_id": domains[10].id,
            "code": "SU-4",
            "text": "What is the estimated carbon footprint of training and deploying your AI system?",
            "help_text": "Quantifying carbon footprint helps organizations understand and manage the environmental impact of their AI systems.",
            "order": 4
        },
        {
            "domain_id": domains[10].id,
            "code": "SU-5",
            "text": "Have you optimized your algorithms to reduce computational resource requirements?",
            "help_text": "Resource optimization reduces both costs and environmental impact while maintaining AI system performance.",
            "order": 5
        },
        {
            "domain_id": domains[10].id,
            "code": "SU-6",
            "text": "Are you using hardware or cloud platforms that prioritize energy efficiency?",
            "help_text": "Energy-efficient platforms help reduce the overall environmental impact of AI system operations.",
            "order": 6
        },
        {
            "domain_id": domains[10].id,
            "code": "SU-7",
            "text": "How do you balance sustainability goals with performance requirements?",
            "help_text": "Balancing sustainability and performance helps ensure that environmental considerations don't compromise system effectiveness.",
            "order": 7
        },
        {
            "domain_id": domains[10].id,
            "code": "SU-8",
            "text": "Do you track the environmental impact of your AI systems over time?",
            "help_text": "Ongoing environmental tracking enables continuous improvement in AI system sustainability practices.",
            "order": 8
        }
    ]
    
    for question_data in questions_data:
        question = Question(**question_data)
        await db.questions.insert_one(question.dict())
    
    logger.info(f"Database seeded with {len(domains)} domains and {len(questions_data)} questions")
