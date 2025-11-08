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
import re
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

# Helper Functions
def normalize_org_name(raw_name: str) -> str:
    """
    Normalize organization name for matching and deduplication.
    Rules:
    1. Convert to lowercase
    2. Trim whitespace
    3. Remove punctuation: , . ' " ! ? & - ( )
    4. Collapse multiple spaces to single space
    5. Remove common legal suffixes
    """
    if not raw_name:
        return ""
    
    # Step 1 & 2: lowercase and trim
    normalized = raw_name.lower().strip()
    
    # Step 3: Remove specific punctuation
    punctuation_to_remove = [',', '.', "'", '"', '!', '?', '&', '-', '(', ')']
    for char in punctuation_to_remove:
        normalized = normalized.replace(char, ' ')
    
    # Step 4: Collapse multiple spaces
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    
    # Step 5: Remove common legal suffixes (configurable per locale)
    legal_suffixes = [
        'pty ltd', 'pty limited', 'limited', 'ltd', 'llc', 'inc', 'incorporated',
        'corp', 'corporation', 'gmbh', 'plc', 'sa', 'bv', 'nv', 'ag', 'spa'
    ]
    for suffix in legal_suffixes:
        # Match suffix at end of string with optional spaces before
        pattern = r'\s+' + re.escape(suffix) + r'$'
        normalized = re.sub(pattern, '', normalized)
    
    return normalized.strip()

def is_corporate_domain(email: str) -> bool:
    """
    Check if email domain is a corporate domain (not free email provider).
    Returns True if corporate, False if free email service.
    """
    if not email or '@' not in email:
        return False
    
    domain = email.split('@')[1].lower()
    
    # List of common free email providers
    free_email_domains = [
        'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com',
        'aol.com', 'mail.com', 'protonmail.com', 'proton.me', 'zoho.com',
        'gmx.com', 'yandex.com', 'live.com', 'msn.com', 'inbox.com',
        'me.com', 'mac.com', 'fastmail.com', 'tutanota.com', 'mailinator.com'
    ]
    
    return domain not in free_email_domains

def extract_email_domain(email: str) -> str:
    """Extract domain from email address."""
    if not email or '@' not in email:
        return ""
    return email.split('@')[1].lower()

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

class ReviewStatus(str, Enum):
    APPROVED = "APPROVED"
    PENDING_REVIEW = "PENDING_REVIEW"

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
    name: str  # Display name (will be renamed to display_name)
    display_name: Optional[str] = None  # Human-readable official name
    name_normalised: Optional[str] = None  # Normalized for matching
    industry: Optional[str] = None  # Keep for backward compatibility
    primary_industry: Optional[str] = None  # Admin-set primary industry
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class OrganizationDomain(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    organisation_id: str  # FK to Organization
    email_domain: str  # e.g., "acme.com"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    email_domain: Optional[str] = None  # Extracted domain for quick lookup
    hashed_password: str
    name: str
    org_id: str
    role: Role = Role.MEMBER
    is_active: bool = True
    default_industry: Optional[str] = None  # User's default industry preference
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

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
    overall_percentage: Optional[float] = None  # Overall score percentage
    pending_review_count: int = 0  # Number of answers pending review
    industry_selected: Optional[str] = None  # Industry snapshot at creation time

class Answer(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    assessment_id: str
    question_id: str
    option: AnswerOption
    numeric_score: int
    other_text: Optional[str] = None  # For "Other" responses
    note: Optional[str] = None
    review_status: str = "APPROVED"  # APPROVED or PENDING_REVIEW
    answered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Report(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    assessment_id: str
    url: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Notification(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: str  # e.g., "PENDING_REVIEW"
    title: str
    message: str
    assessment_id: str
    assessment_name: str
    pending_count: int
    is_read: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    org_id: str

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
    industry: str  # Keep for backward compatibility - organization's industry
    default_industry: Optional[str] = None  # User's personal industry preference

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class AssessmentCreate(BaseModel):
    industry_override: Optional[str] = None  # Optional industry override

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
    pending_review_count: int = 0

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
        
        # Check if user is active
        if not user.get("is_active", True):
            raise HTTPException(
                status_code=http_status.HTTP_403_FORBIDDEN,
                detail="User account is disabled"
            )
        
        org = await db.organizations.find_one({"id": user["org_id"]})
        
        return UserResponse(
            id=user["id"],
            email=user["email"],
            name=user["name"],
            org_id=user["org_id"],
            role=user["role"],
            is_active=user.get("is_active", True),
            organization_name=org["display_name"] or org["name"] if org else "Unknown",
            industry=org.get("primary_industry") or org.get("industry") if org else "Unknown",
            default_industry=user.get("default_industry")
        )
        
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
    
    # Extract email domain
    email_domain = extract_email_domain(user_data.email)
    is_corporate = is_corporate_domain(user_data.email)
    
    # Organization matching flow
    org_id = None
    org = None
    
    # Step 1: Try domain auto-match (only for corporate domains)
    if is_corporate and email_domain:
        domain_match = await db.organization_domains.find_one({"email_domain": email_domain})
        if domain_match:
            org_id = domain_match["organisation_id"]
            org = await db.organizations.find_one({"id": org_id})
            logger.info(f"User {user_data.email} matched to org {org['name']} via domain")
    
    # Step 2: Try name normalization match
    if not org_id:
        normalized_name = normalize_org_name(user_data.organization_name)
        org = await db.organizations.find_one({"name_normalised": normalized_name})
        if org:
            org_id = org["id"]
            logger.info(f"User {user_data.email} matched to org {org['name']} via normalized name")
    
    # Step 3: Create new organization
    if not org_id:
        normalized_name = normalize_org_name(user_data.organization_name)
        new_org = Organization(
            name=user_data.organization_name,
            display_name=user_data.organization_name,
            name_normalised=normalized_name,
            industry=user_data.industry,  # Keep for backward compatibility
            primary_industry=None  # Admin will set this later
        )
        await db.organizations.insert_one(new_org.dict())
        org_id = new_org.id
        logger.info(f"Created new org {new_org.name} for user {user_data.email}")
        
        # Fetch the org back from database to get it as a dict
        org = await db.organizations.find_one({"id": org_id})
        
        # Optionally create organization_domain entry for corporate emails
        if is_corporate and email_domain:
            org_domain = OrganizationDomain(
                organisation_id=org_id,
                email_domain=email_domain
            )
            await db.organization_domains.insert_one(org_domain.dict())
            logger.info(f"Created org domain mapping: {email_domain} → {new_org.name}")
    
    # Create user
    user = User(
        email=user_data.email,
        email_domain=email_domain,
        name=user_data.name,
        hashed_password=hash_password(user_data.password),
        org_id=org_id,
        role=Role.MEMBER,  # New users start as MEMBER
        default_industry=user_data.industry  # Store user's industry preference
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
        organization_name=org.get("display_name") or org.get("name"),
        industry=org.get("primary_industry") or org.get("industry"),
        default_industry=user_data.industry
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
        is_active=user.get("is_active", True),
        organization_name=org["name"] if org else "Unknown",
        industry=org["industry"] if org else "Unknown"
    )
    
    return Token(access_token=access_token, token_type="bearer", user=user_response)

# Helper functions to check user roles
async def require_super_admin(current_user: UserResponse = Depends(get_current_user)):
    if current_user.role != Role.SUPER_ADMIN.value:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="Super admin access required"
        )
    return current_user

async def require_org_admin(current_user: UserResponse = Depends(get_current_user)):
    """Require ORG_ADMIN or higher (ORG_ADMIN or SUPER_ADMIN)"""
    if current_user.role not in [Role.ORG_ADMIN.value, Role.SUPER_ADMIN.value]:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="Organization admin access required"
        )
    return current_user

async def require_admin(current_user: UserResponse = Depends(get_current_user)):
    """Require ADMIN or higher (ADMIN, ORG_ADMIN, or SUPER_ADMIN)"""
    if current_user.role not in [Role.ADMIN.value, Role.ORG_ADMIN.value, Role.SUPER_ADMIN.value]:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

@api_router.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: UserResponse = Depends(get_current_user)):
    return current_user

# Admin endpoints
@api_router.get("/admin/users", response_model=List[UserResponse])
async def get_all_users(admin: UserResponse = Depends(require_super_admin)):
    """Get all users (Super Admin only)"""
    users = await db.users.find({}).to_list(length=None)
    
    user_responses = []
    for user in users:
        org = await db.organizations.find_one({"id": user["org_id"]})
        user_responses.append(UserResponse(
            id=user["id"],
            email=user["email"],
            name=user["name"],
            org_id=user["org_id"],
            role=user["role"],
            is_active=user.get("is_active", True),
            organization_name=org["display_name"] or org["name"] if org else "Unknown",
            industry=org.get("primary_industry") or org.get("industry") if org else "Unknown",
            default_industry=user.get("default_industry")
        ))
    
    return user_responses

@api_router.put("/admin/users/{user_id}/role")
async def update_user_role(
    user_id: str, 
    new_role: Role,
    admin: UserResponse = Depends(require_super_admin)
):
    """Update user role (Super Admin only)"""
    result = await db.users.update_one(
        {"id": user_id},
        {"$set": {"role": new_role.value}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"success": True, "message": f"User role updated to {new_role.value}"}

@api_router.put("/admin/users/{user_id}/toggle-active")
async def toggle_user_active(
    user_id: str,
    admin: UserResponse = Depends(require_super_admin)
):
    """Enable/disable user account (Super Admin only)"""
    user = await db.users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_status = not user.get("is_active", True)
    
    await db.users.update_one(
        {"id": user_id},
        {"$set": {"is_active": new_status}}
    )
    
    return {"success": True, "is_active": new_status}

@api_router.delete("/admin/users/{user_id}")
async def delete_user(
    user_id: str,
    admin: UserResponse = Depends(require_super_admin)
):
    """Delete user account (Super Admin only)"""
    # Don't allow deleting yourself
    if user_id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    
    result = await db.users.delete_one({"id": user_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"success": True, "message": "User deleted successfully"}

@api_router.post("/admin/users/{user_id}/reset-password")
async def reset_user_password(
    user_id: str,
    admin: UserResponse = Depends(require_super_admin)
):
    """Generate temporary password for user (Super Admin only)"""
    import secrets
    import string
    
    # Generate random 12-character password
    alphabet = string.ascii_letters + string.digits
    temp_password = ''.join(secrets.choice(alphabet) for i in range(12))
    
    # Update user password
    hashed = hash_password(temp_password)
    result = await db.users.update_one(
        {"id": user_id},
        {"$set": {"hashed_password": hashed}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "success": True,
        "temporary_password": temp_password,
        "message": "Password reset successfully. Share this temporary password with the user."
    }

# Organization management endpoints (ORG_ADMIN level)
@api_router.get("/org/users", response_model=List[UserResponse])
async def get_org_users(current_user: UserResponse = Depends(require_org_admin)):
    """Get all users in the current user's organization (ORG_ADMIN or SUPER_ADMIN)"""
    # SUPER_ADMIN can see all users, ORG_ADMIN sees only their org
    if current_user.role == Role.SUPER_ADMIN.value:
        users = await db.users.find({}).to_list(length=None)
    else:
        users = await db.users.find({"org_id": current_user.org_id}).to_list(length=None)
    
    user_responses = []
    for user in users:
        org = await db.organizations.find_one({"id": user["org_id"]})
        user_responses.append(UserResponse(
            id=user["id"],
            email=user["email"],
            name=user["name"],
            org_id=user["org_id"],
            role=user["role"],
            is_active=user.get("is_active", True),
            organization_name=org["display_name"] or org["name"] if org else "Unknown",
            industry=org.get("primary_industry") or org.get("industry") if org else "Unknown",
            default_industry=user.get("default_industry")
        ))
    
    return user_responses

@api_router.put("/org/users/{user_id}/role")
async def update_org_user_role(
    user_id: str, 
    new_role: Role,
    current_user: UserResponse = Depends(require_org_admin)
):
    """Update user role within organization (ORG_ADMIN can only set MEMBER, ADMIN, ORG_ADMIN)"""
    # Find the target user
    target_user = await db.users.find_one({"id": user_id})
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # ORG_ADMIN can only manage users in their own organization
    if current_user.role == Role.ORG_ADMIN.value:
        if target_user["org_id"] != current_user.org_id:
            raise HTTPException(status_code=403, detail="Cannot manage users outside your organization")
        
        # ORG_ADMIN cannot promote users to SUPER_ADMIN
        if new_role == Role.SUPER_ADMIN:
            raise HTTPException(status_code=403, detail="Cannot assign SUPER_ADMIN role")
    
    result = await db.users.update_one(
        {"id": user_id},
        {"$set": {"role": new_role.value}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"success": True, "message": f"User role updated to {new_role.value}"}

@api_router.put("/org/users/{user_id}/toggle-active")
async def toggle_org_user_active(
    user_id: str,
    current_user: UserResponse = Depends(require_org_admin)
):
    """Enable/disable user account within organization (ORG_ADMIN)"""
    target_user = await db.users.find_one({"id": user_id})
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # ORG_ADMIN can only manage users in their own organization
    if current_user.role == Role.ORG_ADMIN.value:
        if target_user["org_id"] != current_user.org_id:
            raise HTTPException(status_code=403, detail="Cannot manage users outside your organization")
    
    new_status = not target_user.get("is_active", True)
    
    await db.users.update_one(
        {"id": user_id},
        {"$set": {"is_active": new_status}}
    )
    
    return {"success": True, "is_active": new_status}

@api_router.post("/org/users/{user_id}/reset-password")
async def reset_org_user_password(
    user_id: str,
    current_user: UserResponse = Depends(require_org_admin)
):
    """Generate temporary password for user within organization (ORG_ADMIN)"""
    target_user = await db.users.find_one({"id": user_id})
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # ORG_ADMIN can only manage users in their own organization
    if current_user.role == Role.ORG_ADMIN.value:
        if target_user["org_id"] != current_user.org_id:
            raise HTTPException(status_code=403, detail="Cannot manage users outside your organization")
    
    import secrets
    import string
    
    # Generate random 12-character password
    alphabet = string.ascii_letters + string.digits
    temp_password = ''.join(secrets.choice(alphabet) for i in range(12))
    
    # Update user password
    hashed = hash_password(temp_password)
    result = await db.users.update_one(
        {"id": user_id},
        {"$set": {"hashed_password": hashed}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "success": True,
        "temporary_password": temp_password,
        "message": "Password reset successfully. Share this temporary password with the user."
    }

@api_router.delete("/org/users/{user_id}")
async def delete_org_user(
    user_id: str,
    current_user: UserResponse = Depends(require_org_admin)
):
    """Delete user account within organization (ORG_ADMIN)"""
    # Don't allow deleting yourself
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    
    target_user = await db.users.find_one({"id": user_id})
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # ORG_ADMIN can only manage users in their own organization
    if current_user.role == Role.ORG_ADMIN.value:
        if target_user["org_id"] != current_user.org_id:
            raise HTTPException(status_code=403, detail="Cannot manage users outside your organization")
    
    result = await db.users.delete_one({"id": user_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"success": True, "message": "User deleted successfully"}

# Organization analytics endpoint (ADMIN level - read only)
@api_router.get("/org/analytics")
async def get_org_analytics(current_user: UserResponse = Depends(require_admin)):
    """Get organization-wide analytics (ADMIN, ORG_ADMIN, or SUPER_ADMIN)"""
    # SUPER_ADMIN can see all assessments, others see only their org
    if current_user.role == Role.SUPER_ADMIN.value:
        assessments = await db.assessments.find({}).to_list(length=None)
    else:
        assessments = await db.assessments.find({"org_id": current_user.org_id}).to_list(length=None)
    
    # Get all organizations for SUPER_ADMIN
    orgs = {}
    if current_user.role == Role.SUPER_ADMIN.value:
        all_orgs = await db.organizations.find({}).to_list(length=None)
        orgs = {org["id"]: org["name"] for org in all_orgs}
    
    # Calculate analytics
    total_assessments = len(assessments)
    completed_assessments = len([a for a in assessments if a.get("status") == "COMPLETED"])
    incomplete_assessments = total_assessments - completed_assessments
    
    # Get average score for completed assessments
    completed_with_scores = [a for a in assessments if a.get("status") == "COMPLETED" and a.get("overall_percentage")]
    avg_score = sum([a.get("overall_percentage", 0) for a in completed_with_scores]) / len(completed_with_scores) if completed_with_scores else 0
    
    return {
        "total_assessments": total_assessments,
        "completed_assessments": completed_assessments,
        "incomplete_assessments": incomplete_assessments,
        "average_score": round(avg_score, 2),
        "assessments": [
            {
                "id": a["id"],
                "name": a.get("name", "Unnamed Assessment"),
                "status": a.get("status", "INCOMPLETE"),
                "assessment_type": a.get("assessment_type", "System"),
                "org_id": a.get("org_id"),
                "organization_name": orgs.get(a.get("org_id"), current_user.organization_name),
                "overall_percentage": a.get("overall_percentage"),
                "started_at": a.get("started_at"),
                "completed_at": a.get("completed_at"),
                "pending_review_count": a.get("pending_review_count", 0)
            }
            for a in assessments
        ]
    }

@api_router.post("/org/assessments/bulk-delete")
async def bulk_delete_assessments(
    assessment_ids: List[str],
    current_user: UserResponse = Depends(require_admin)
):
    """Bulk delete assessments (ADMIN, ORG_ADMIN, or SUPER_ADMIN)"""
    if not assessment_ids:
        raise HTTPException(status_code=400, detail="No assessment IDs provided")
    
    # Verify all assessments exist and belong to the user's org (or SUPER_ADMIN)
    deleted_count = 0
    failed_ids = []
    
    for assessment_id in assessment_ids:
        assessment = await db.assessments.find_one({"id": assessment_id})
        
        if not assessment:
            failed_ids.append(assessment_id)
            continue
        
        # Check permissions
        if current_user.role != Role.SUPER_ADMIN.value:
            if assessment["org_id"] != current_user.org_id:
                failed_ids.append(assessment_id)
                continue
        
        # Delete answers associated with the assessment
        await db.answers.delete_many({"assessment_id": assessment_id})
        
        # Delete the assessment
        result = await db.assessments.delete_one({"id": assessment_id})
        if result.deleted_count > 0:
            deleted_count += 1
    
    return {
        "success": True,
        "deleted_count": deleted_count,
        "failed_ids": failed_ids,
        "message": f"Successfully deleted {deleted_count} assessment(s)"
    }

# Pending Review Management endpoints (SUPER_ADMIN only)
@api_router.get("/admin/assessments/pending-reviews")
async def get_assessments_with_pending_reviews(admin: UserResponse = Depends(require_super_admin)):
    """Get all assessments that have pending review answers (SUPER_ADMIN only)"""
    assessments = await db.assessments.find({"pending_review_count": {"$gt": 0}}).to_list(length=None)
    
    # Get organization info
    org_ids = list(set(a["org_id"] for a in assessments))
    orgs = await db.organizations.find({"id": {"$in": org_ids}}).to_list(length=None)
    org_lookup = {org["id"]: org["name"] for org in orgs}
    
    return [
        {
            "id": a["id"],
            "name": a.get("name", "Unnamed Assessment"),
            "organization_name": org_lookup.get(a["org_id"], "Unknown"),
            "assessment_type": a.get("assessment_type", "System"),
            "pending_review_count": a.get("pending_review_count", 0),
            "completed_at": a.get("completed_at"),
            "overall_percentage": a.get("overall_percentage")
        }
        for a in assessments
    ]

@api_router.get("/admin/assessments/{assessment_id}/pending-answers")
async def get_pending_review_answers(assessment_id: str, admin: UserResponse = Depends(require_super_admin)):
    """Get all pending review answers for an assessment (SUPER_ADMIN only)"""
    # Verify assessment exists
    assessment = await db.assessments.find_one({"id": assessment_id})
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Get pending review answers
    answers = await db.answers.find({
        "assessment_id": assessment_id,
        "review_status": ReviewStatus.PENDING_REVIEW.value
    }).to_list(length=None)
    
    # Get questions and domains for context
    question_ids = [a["question_id"] for a in answers]
    questions = await db.questions.find({"id": {"$in": question_ids}}).to_list(length=None)
    question_lookup = {q["id"]: q for q in questions}
    
    domain_ids = list(set(q["domain_id"] for q in questions))
    domains = await db.domains.find({"id": {"$in": domain_ids}}).to_list(length=None)
    domain_lookup = {d["id"]: d for d in domains}
    
    return [
        {
            "answer_id": a["id"],
            "question_id": a["question_id"],
            "question_code": question_lookup.get(a["question_id"], {}).get("code", "Unknown"),
            "question_text": question_lookup.get(a["question_id"], {}).get("text", "Unknown question"),
            "domain_name": domain_lookup.get(question_lookup.get(a["question_id"], {}).get("domain_id"), {}).get("name", "Unknown"),
            "other_text": a.get("other_text", ""),
            "current_score": a.get("numeric_score", 0)
        }
        for a in answers
    ]

@api_router.put("/admin/assessments/{assessment_id}/answers/{answer_id}/score")
async def score_pending_answer(
    assessment_id: str,
    answer_id: str,
    score: int,
    admin: UserResponse = Depends(require_super_admin)
):
    """Score a pending review answer (SUPER_ADMIN only)"""
    # Validate score
    if score < 0 or score > 3:
        raise HTTPException(status_code=400, detail="Score must be between 0 and 3")
    
    # Find the answer
    answer = await db.answers.find_one({"id": answer_id, "assessment_id": assessment_id})
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    
    if answer.get("review_status") != ReviewStatus.PENDING_REVIEW.value:
        raise HTTPException(status_code=400, detail="Answer is not pending review")
    
    # Update the answer
    await db.answers.update_one(
        {"id": answer_id},
        {
            "$set": {
                "numeric_score": score,
                "review_status": ReviewStatus.APPROVED.value
            }
        }
    )
    
    # Recalculate assessment score and pending count
    assessment = await db.assessments.find_one({"id": assessment_id})
    answers = await db.answers.find({"assessment_id": assessment_id}).to_list(length=None)
    
    pending_review_count = sum(1 for a in answers if a.get("review_status") == ReviewStatus.PENDING_REVIEW.value)
    approved_answers = [a for a in answers if a.get("review_status") == ReviewStatus.APPROVED.value]
    total_score = sum(a.get("numeric_score", 0) for a in approved_answers)
    max_score = len(approved_answers) * 3
    overall_percentage = (total_score / max_score * 100) if max_score > 0 else 0
    
    await db.assessments.update_one(
        {"id": assessment_id},
        {
            "$set": {
                "pending_review_count": pending_review_count,
                "overall_percentage": round(overall_percentage, 1)
            }
        }
    )
    
    return {
        "success": True,
        "message": "Answer scored successfully",
        "remaining_pending": pending_review_count
    }

# Notification endpoints
@api_router.get("/admin/notifications")
async def get_notifications(admin: UserResponse = Depends(require_super_admin)):
    """Get all notifications for Super Admin"""
    notifications = await db.notifications.find({}, {"_id": 0}).sort("created_at", -1).to_list(length=None)
    return notifications

@api_router.get("/admin/notifications/unread-count")
async def get_unread_notification_count(admin: UserResponse = Depends(require_super_admin)):
    """Get count of unread notifications"""
    count = await db.notifications.count_documents({"is_read": False})
    return {"count": count}

@api_router.put("/admin/notifications/{notification_id}/mark-read")
async def mark_notification_read(notification_id: str, admin: UserResponse = Depends(require_super_admin)):
    """Mark a notification as read"""
    result = await db.notifications.update_one(
        {"id": notification_id},
        {"$set": {"is_read": True}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"success": True}

@api_router.put("/admin/notifications/mark-all-read")
async def mark_all_notifications_read(admin: UserResponse = Depends(require_super_admin)):
    """Mark all notifications as read"""
    await db.notifications.update_many(
        {"is_read": False},
        {"$set": {"is_read": True}}
    )
    return {"success": True}

@api_router.delete("/admin/notifications/{notification_id}")
async def delete_notification(notification_id: str, admin: UserResponse = Depends(require_super_admin)):
    """Delete a notification"""
    result = await db.notifications.delete_one({"id": notification_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"success": True}

@api_router.post("/admin/notifications/bulk-delete")
async def bulk_delete_notifications(notification_ids: List[str], admin: UserResponse = Depends(require_super_admin)):
    """Bulk delete notifications"""
    result = await db.notifications.delete_many({"id": {"$in": notification_ids}})
    return {"success": True, "deleted_count": result.deleted_count}

@api_router.get("/admin/metadata-fields")
async def get_all_metadata_fields(admin: UserResponse = Depends(require_super_admin)):
    """Get all metadata fields from all collections with usage information"""
    metadata = {}
    
    # Get sample documents from each collection to extract field names
    collections = ["users", "assessments", "answers", "organizations", "questions", "domains", "reports", "notifications"]
    
    for collection_name in collections:
        collection = db[collection_name]
        
        # Get one sample document to see all fields
        sample = await collection.find_one({})
        
        if sample:
            # Remove MongoDB _id field
            if "_id" in sample:
                del sample["_id"]
            
            # Get field names and example values
            fields = {}
            for field_name, field_value in sample.items():
                fields[field_name] = {
                    "type": type(field_value).__name__,
                    "example": str(field_value)[:100] if field_value else None  # Truncate long values
                }
            
            # Count total documents in collection
            count = await collection.count_documents({})
            
            metadata[collection_name] = {
                "total_documents": count,
                "fields": fields
            }
        else:
            metadata[collection_name] = {
                "total_documents": 0,
                "fields": {}
            }
    
    return metadata

# Assessment endpoints
@api_router.post("/assessments", response_model=AssessmentResponse)
async def create_assessment(
    assessment_data: AssessmentCreate = None,
    current_user: UserResponse = Depends(get_current_user)
):
    # Get user and organization data
    user = await db.users.find_one({"id": current_user.id})
    org = await db.organizations.find_one({"id": current_user.org_id})
    
    # Determine industry_selected based on precedence
    industry_selected = None
    if assessment_data and assessment_data.industry_override:
        # Priority 1: Override in request
        industry_selected = assessment_data.industry_override
    elif user.get("default_industry"):
        # Priority 2: User's default industry
        industry_selected = user["default_industry"]
    elif org.get("primary_industry"):
        # Priority 3: Organization's primary industry
        industry_selected = org["primary_industry"]
    # else: remains None
    
    # Generate initial assessment name with format: [Type]_[TBD]_In-Progress_YYYY-MM-DD
    started_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    assessment_name = f"System_[TBD]_In-Progress_{started_date}"
    
    assessment = Assessment(
        org_id=current_user.org_id,
        user_id=current_user.id,
        name=assessment_name,
        assessment_type="System",
        industry_selected=industry_selected
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
        system_info=assessment.system_info,
        pending_review_count=assessment.pending_review_count
    )

@api_router.get("/assessments", response_model=List[AssessmentResponse])
async def get_assessments(current_user: UserResponse = Depends(get_current_user)):
    """Get assessments filtered by user role"""
    # MEMBER: Only see their own assessments
    # ADMIN/ORG_ADMIN: See all assessments in their organization
    # SUPER_ADMIN: See all assessments
    
    if current_user.role == Role.SUPER_ADMIN.value:
        # SUPER_ADMIN sees everything
        assessments = await db.assessments.find({}).to_list(length=None)
    elif current_user.role in [Role.ADMIN.value, Role.ORG_ADMIN.value]:
        # ADMIN and ORG_ADMIN see all assessments in their organization
        assessments = await db.assessments.find({"org_id": current_user.org_id}).to_list(length=None)
    else:
        # MEMBER sees only their own assessments
        assessments = await db.assessments.find({"user_id": current_user.id}).to_list(length=None)
    
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
            system_info=assessment.get("system_info"),
            pending_review_count=assessment.get("pending_review_count", 0)
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
        # Generate new name: [Type]_[Target Name]_In-Progress_YYYY-MM-DD
        updated_name = f"{assessment_type}_{system_info['systemName']}_In-Progress_{started_date}"
    
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
    
    # Determine review status and score
    if answer_data.option == AnswerOption.OTHER:
        review_status = ReviewStatus.PENDING_REVIEW.value
        numeric_score = 0  # Default score for pending review, will be updated by admin
    else:
        review_status = ReviewStatus.APPROVED.value
        numeric_score = SCORING_MAP[answer_data.option]
    
    answer = Answer(
        assessment_id=assessment_id,
        question_id=answer_data.question_id,
        option=answer_data.option,
        numeric_score=numeric_score,
        other_text=answer_data.other_text,
        note=answer_data.note,
        review_status=review_status
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

@api_router.get("/assessments/{assessment_id}/first-pending-question")
async def get_first_pending_question(assessment_id: str, current_user: UserResponse = Depends(get_current_user)):
    """Get the first question with a pending review answer"""
    # Verify assessment belongs to user's organization (or is Super Admin)
    if current_user.role != Role.SUPER_ADMIN.value:
        assessment = await db.assessments.find_one({"id": assessment_id, "org_id": current_user.org_id})
        if not assessment:
            raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Get first pending review answer
    pending_answer = await db.answers.find_one(
        {"assessment_id": assessment_id, "review_status": ReviewStatus.PENDING_REVIEW.value}
    )
    
    if not pending_answer:
        return {"question_id": None}
    
    return {"question_id": pending_answer["question_id"]}

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
            answer = answer_lookup.get(question["id"])
            question_status = {
                "question_id": question["id"],
                "question_code": question["code"],
                "question_text": question["text"],
                "answered": question["id"] in answer_lookup,
                "review_status": answer.get("review_status") if answer else None
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
    
    # Allow re-submission for SUPER_ADMIN or if assessment is not completed
    is_resubmission = assessment.get("status") == AssessmentStatus.COMPLETED
    if is_resubmission and current_user.role != Role.SUPER_ADMIN.value:
        raise HTTPException(status_code=403, detail="Only Super Admin can re-submit completed assessments")
    
    # Get total questions and answered questions count
    total_questions = await db.questions.count_documents({})
    answered_questions = await db.answers.count_documents({"assessment_id": assessment_id})
    
    # Verify all questions are answered
    if answered_questions < total_questions:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot submit assessment. {total_questions - answered_questions} questions remain unanswered."
        )
    
    # Get all answers and count pending reviews
    answers = await db.answers.find({"assessment_id": assessment_id}).to_list(length=None)
    pending_review_count = sum(1 for answer in answers if answer.get("review_status") == ReviewStatus.PENDING_REVIEW.value)
    
    # Calculate overall percentage (excluding pending review answers)
    approved_answers = [a for a in answers if a.get("review_status") == ReviewStatus.APPROVED.value]
    total_score = sum(answer.get("numeric_score", 0) for answer in approved_answers)
    max_score = len(approved_answers) * 3  # Maximum score per question is 3
    overall_percentage = (total_score / max_score * 100) if max_score > 0 else 0
    
    # Update the assessment name
    completed_date = datetime.now(timezone.utc)
    current_name = assessment["name"]
    
    # Handle name updates based on current state
    if "Pending Review" in current_name or "Pending_Review" in current_name or "Pending-Review" in current_name:
        # Re-submission of pending review assessment
        # Extract parts: [Type]_[Target Name]_Pending-Review_YYYY-MM-DD
        parts = current_name.replace("Pending Review", "Pending-Review").replace("Pending_Review", "Pending-Review").split("_")
        
        # Find where "Pending-Review" is in the parts
        if "Pending-Review" in parts:
            pending_idx = parts.index("Pending-Review")
            if pending_idx >= 2:
                # parts[0] = Type, parts[1:pending_idx] = Target Name components, parts[pending_idx] = "Pending-Review", parts[pending_idx+1] = Date
                assessment_type = parts[0]
                target_name = "_".join(parts[1:pending_idx])
                date_str = parts[pending_idx + 1] if len(parts) > pending_idx + 1 else completed_date.strftime('%Y-%m-%d')
                
                if pending_review_count > 0:
                    # Still has pending reviews
                    updated_name = f"{assessment_type}_{target_name}_Pending-Review_{date_str}"
                else:
                    # All reviews completed, change status to Completed
                    updated_name = f"{assessment_type}_{target_name}_Completed_{date_str}"
            else:
                updated_name = current_name
        else:
            # Old format with status at beginning - convert to new format
            parts = current_name.replace("Pending Review_", "").replace("Pending_Review_", "").replace("Pending-Review_", "").split("_")
            if len(parts) >= 3:
                assessment_type = parts[0]
                target_name = parts[1]
                date_str = parts[2] if len(parts) > 2 else completed_date.strftime('%Y-%m-%d')
                
                if pending_review_count > 0:
                    updated_name = f"{assessment_type}_{target_name}_Pending-Review_{date_str}"
                else:
                    updated_name = f"{assessment_type}_{target_name}_Completed_{date_str}"
            else:
                updated_name = current_name
    elif "Started" in current_name or "In-Progress" in current_name:
        # First submission - handle old formats and new format
        if " – " in current_name:
            # Old format: [Type] – [Target Name] – Started YYYY-MM-DD
            parts = current_name.split(" – ")
            if len(parts) >= 3:
                assessment_type = parts[0]
                target_name = parts[1]
                date_str = completed_date.strftime('%Y-%m-%d')
                
                if pending_review_count > 0:
                    updated_name = f"{assessment_type}_{target_name}_Pending-Review_{date_str}"
                else:
                    updated_name = f"{assessment_type}_{target_name}_Completed_{date_str}"
            else:
                updated_name = current_name
        else:
            # New format: [Type]_[Target Name]_In-Progress_YYYY-MM-DD or [Type]_[Target Name]_Started_YYYY-MM-DD
            parts = current_name.split("_")
            if len(parts) >= 4:
                # parts[0] = Type, parts[1] = Target Name, parts[2] = "In-Progress" or "Started", parts[3] = YYYY-MM-DD
                assessment_type = parts[0]
                target_name = parts[1]
                date_str = completed_date.strftime('%Y-%m-%d')
                
                # Format: Pending-Review_[Type]_[Target Name]_[Date]
                # or: Completed_[Type]_[Target Name]_[Date] if no pending reviews
                if pending_review_count > 0:
                    updated_name = f"{assessment_type}_{target_name}_Pending-Review_{date_str}"
                else:
                    updated_name = f"{assessment_type}_{target_name}_Completed_{date_str}"
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
                "completed_at": completed_date if not is_resubmission else assessment.get("completed_at"),
                "progress": total_questions,
                "name": updated_name,
                "overall_percentage": round(overall_percentage, 1),
                "pending_review_count": pending_review_count
            }
        }
    )
    
    # Create notification for SUPER_ADMIN if there are pending reviews (only on first submission)
    if pending_review_count > 0 and not is_resubmission:
        notification = Notification(
            type="PENDING_REVIEW",
            title="Assessment Pending Review",
            message=f"{pending_review_count} answer(s) need review in assessment: {updated_name}",
            assessment_id=assessment_id,
            assessment_name=updated_name,
            pending_count=pending_review_count,
            org_id=current_user.org_id
        )
        await db.notifications.insert_one(notification.dict())
        logger.info(f"NOTIFICATION CREATED: Assessment {assessment_id} completed with {pending_review_count} answer(s) pending review")
    
    return {
        "status": "success",
        "message": "Assessment submitted successfully",
        "assessment_id": assessment_id,
        "completed_at": completed_date.isoformat(),
        "pending_review_count": pending_review_count
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

# Download PDF endpoint
@api_router.get("/download/testing-checklist")
async def download_testing_checklist():
    """Download the testing checklist PDF"""
    file_path = Path("/app/backend/AM_AI_SAFE_Testing_Checklist.pdf")
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename="AM_AI_SAFE_Testing_Checklist.pdf"
    )

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