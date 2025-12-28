"""
Evidence Model

Represents a single piece of uploaded evidence that can be linked to one or more 
AM AI SAFE questions and controls.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
from uuid import uuid4


class EvidenceType(str, Enum):
    POLICY = "Policy"
    STANDARD = "Standard"
    PROCEDURE = "Procedure"
    PROCESS_DESCRIPTION = "Process Description"
    RISK_ASSESSMENT = "Risk Assessment"
    IMPACT_ASSESSMENT = "Impact Assessment"
    TECHNICAL_CONFIGURATION = "Technical Configuration"
    SYSTEM_ARCHITECTURE = "System Architecture"
    MODEL_DOCUMENTATION = "Model Documentation"
    TRAINING_MATERIAL = "Training Material"
    CONTRACT_SLA = "Contract / SLA"
    AUDIT_REPORT = "Audit Report"
    LOG_MONITORING_OUTPUT = "Log / Monitoring Output"
    SCREENSHOT_SNAPSHOT = "Screenshot / Snapshot"
    OTHER = "Other"
    UNSPECIFIED = "Unspecified"


class LifecyclePhase(str, Enum):
    DESIGN = "Design"
    DEVELOPMENT = "Development"
    TESTING = "Testing"
    DEPLOYMENT = "Deployment"
    OPERATION = "Operation"
    MONITORING = "Monitoring"
    DECOMMISSIONING = "Decommissioning"
    CROSS_LIFECYCLE = "Cross-Lifecycle"
    UNSPECIFIED = "Unspecified"


class TrustLevel(str, Enum):
    UNSPECIFIED = "Unspecified"
    DRAFT = "Draft"
    OPERATIONAL = "Operational"
    APPROVED = "Approved"
    INDEPENDENTLY_REVIEWED = "Independently Reviewed"
    REGULATOR_EXTERNAL_ASSURED = "Regulator / External Assured"


class AppliesToScope(str, Enum):
    ORGANISATION_WIDE = "Organisation-wide"
    SPECIFIC_AI_SYSTEM = "Specific AI System"
    SPECIFIC_MODEL = "Specific Model"
    SPECIFIC_USE_CASE = "Specific Use Case"
    THIRD_PARTY_VENDOR = "Third Party / Vendor"
    UNSPECIFIED = "Unspecified"


class EvidenceStatus(str, Enum):
    ACTIVE = "Active"
    ARCHIVED = "Archived"
    SUPERSEDED = "Superseded"


class EvidenceCreate(BaseModel):
    """Schema for creating new evidence"""
    evidence_title: str = Field(..., description="Title of the evidence, defaults to file name")
    evidence_description: Optional[str] = Field(None, description="Free text description")
    file_name: str = Field(..., description="Original file name")
    file_type: str = Field(..., description="MIME type or file extension")
    file_url: str = Field(..., description="Stored file reference/URL")
    evidence_type: Optional[EvidenceType] = Field(EvidenceType.UNSPECIFIED, description="Type of evidence")
    lifecycle_phase: Optional[LifecyclePhase] = Field(LifecyclePhase.UNSPECIFIED, description="AI lifecycle phase")
    trust_level: Optional[TrustLevel] = Field(TrustLevel.UNSPECIFIED, description="Trust/approval level")
    evidence_owner: Optional[str] = Field(None, description="Owner of the evidence")
    valid_from: Optional[datetime] = Field(None, description="Validity start date")
    valid_to: Optional[datetime] = Field(None, description="Validity end date")
    applies_to_scope: Optional[AppliesToScope] = Field(AppliesToScope.UNSPECIFIED, description="Scope of applicability")
    assessment_id: Optional[str] = Field(None, description="Assessment ID this evidence belongs to")
    linked_question_ids: List[str] = Field(..., min_length=1, description="At least one linked question ID required")
    linked_am_control_ids: Optional[List[str]] = Field(default_factory=list, description="Linked AM AI SAFE control IDs")
    notes: Optional[str] = Field(None, description="Additional notes")
    is_reusable: Optional[bool] = Field(False, description="Whether evidence can be reused across assessments")


class EvidenceUpdate(BaseModel):
    """Schema for updating existing evidence"""
    evidence_title: Optional[str] = None
    evidence_description: Optional[str] = None
    evidence_type: Optional[EvidenceType] = None
    lifecycle_phase: Optional[LifecyclePhase] = None
    trust_level: Optional[TrustLevel] = None
    evidence_owner: Optional[str] = None
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    applies_to_scope: Optional[AppliesToScope] = None
    linked_question_ids: Optional[List[str]] = None
    linked_am_control_ids: Optional[List[str]] = None
    notes: Optional[str] = None
    is_reusable: Optional[bool] = None
    status: Optional[EvidenceStatus] = None


class Evidence(BaseModel):
    """Full evidence model with all fields"""
    evidence_id: str = Field(default_factory=lambda: str(uuid4()), description="UUID auto-generated")
    evidence_title: str = Field(..., description="Title of the evidence")
    evidence_description: Optional[str] = Field(None, description="Free text description")
    file_name: str = Field(..., description="Original file name")
    file_type: str = Field(..., description="MIME type or file extension")
    file_url: str = Field(..., description="Stored file reference/URL")
    uploaded_by: str = Field(..., description="User identifier who uploaded")
    uploaded_date: datetime = Field(default_factory=lambda: datetime.now(), description="System generated upload date")
    last_updated_date: datetime = Field(default_factory=lambda: datetime.now(), description="Auto update on edit")
    evidence_type: EvidenceType = Field(EvidenceType.UNSPECIFIED, description="Type of evidence")
    lifecycle_phase: LifecyclePhase = Field(LifecyclePhase.UNSPECIFIED, description="AI lifecycle phase")
    trust_level: TrustLevel = Field(TrustLevel.UNSPECIFIED, description="Trust/approval level")
    evidence_owner: Optional[str] = Field(None, description="Owner of the evidence")
    valid_from: Optional[datetime] = Field(None, description="Validity start date")
    valid_to: Optional[datetime] = Field(None, description="Validity end date")
    applies_to_scope: AppliesToScope = Field(AppliesToScope.UNSPECIFIED, description="Scope of applicability")
    assessment_id: Optional[str] = Field(None, description="Assessment ID this evidence belongs to")
    linked_question_ids: List[str] = Field(..., min_length=1, description="At least one linked question ID required")
    linked_am_control_ids: List[str] = Field(default_factory=list, description="Linked AM AI SAFE control IDs")
    notes: Optional[str] = Field(None, description="Additional notes")
    is_reusable: bool = Field(False, description="Whether evidence can be reused across assessments")
    status: EvidenceStatus = Field(EvidenceStatus.ACTIVE, description="Evidence status")
    org_id: str = Field(..., description="Organization ID for multi-tenancy")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class EvidenceResponse(BaseModel):
    """Response model for evidence (excludes internal fields)"""
    evidence_id: str
    evidence_title: str
    evidence_description: Optional[str] = None
    file_name: str
    file_type: str
    file_url: str
    uploaded_by: str
    uploaded_date: str
    last_updated_date: str
    evidence_type: str
    lifecycle_phase: str
    trust_level: str
    evidence_owner: Optional[str] = None
    valid_from: Optional[str] = None
    valid_to: Optional[str] = None
    applies_to_scope: str
    assessment_id: Optional[str] = None
    linked_question_ids: List[str]
    linked_am_control_ids: List[str]
    notes: Optional[str] = None
    is_reusable: bool
    status: str
