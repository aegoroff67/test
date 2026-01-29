"""
Logging Service for AM AI SAFE
Handles Audit Logs, Analytics Events, and Error Logging
"""

from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any, List
from enum import Enum
import logging
import traceback
from motor.motor_asyncio import AsyncIOMotorDatabase

logger = logging.getLogger(__name__)

# ============================================================================
# ENUMS
# ============================================================================

class AuditAction(str, Enum):
    # Auth Events
    AUTH_LOGIN_SUCCESS = "auth_login_success"
    AUTH_LOGIN_FAILED = "auth_login_failed"
    AUTH_LOGOUT = "auth_logout"
    
    # Assessment Lifecycle
    ASSESSMENT_CREATED = "assessment_created"
    ASSESSMENT_STARTED = "assessment_started"
    ASSESSMENT_COMPLETED = "assessment_completed"
    ASSESSMENT_DELETED = "assessment_deleted"
    ASSESSMENT_UPDATED = "assessment_updated"
    
    # Report Generation
    REPORT_GENERATED = "report_generated"
    REPORT_DOWNLOADED = "report_downloaded"
    REPORT_GENERATION_FAILED = "report_generation_failed"
    
    # Evidence Actions
    EVIDENCE_UPLOADED = "evidence_uploaded"
    EVIDENCE_DELETED = "evidence_deleted"
    EVIDENCE_LINKED = "evidence_linked"
    
    # Admin Changes
    USER_CREATED = "user_created"
    USER_UPDATED = "user_updated"
    USER_ROLE_CHANGED = "user_role_changed"
    USER_DISABLED = "user_disabled"
    USER_DELETED = "user_deleted"
    SETTINGS_CHANGED = "settings_changed"
    ORG_CREATED = "org_created"
    ORG_UPDATED = "org_updated"


class AnalyticsEventType(str, Enum):
    # Funnel Events
    PAGE_VIEW = "page_view"
    ASSESSMENT_FUNNEL = "assessment_funnel"
    REPORT_FUNNEL = "report_funnel"
    
    # Engagement
    FEATURE_USED = "feature_used"
    HELP_ACCESSED = "help_accessed"
    
    # Friction Signals
    VALIDATION_ERROR = "validation_error"
    API_ERROR_SHOWN = "api_error_shown"


class ErrorSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ============================================================================
# AUDIT LOGGING
# ============================================================================

async def log_audit_event(
    db: AsyncIOMotorDatabase,
    action: AuditAction,
    actor_user_id: Optional[str] = None,
    actor_email: Optional[str] = None,
    tenant_id: Optional[str] = None,
    object_type: Optional[str] = None,
    object_id: Optional[str] = None,
    object_name: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    source_ip: Optional[str] = None,
    user_agent: Optional[str] = None,
    result: str = "success",
    reason: Optional[str] = None
):
    """
    Log an audit event to the audit_logs collection.
    This is append-only - no updates or deletes allowed.
    """
    try:
        audit_entry = {
            "timestamp": datetime.now(timezone.utc),
            "action": action.value if isinstance(action, AuditAction) else action,
            "actor_user_id": actor_user_id,
            "actor_email": actor_email,
            "tenant_id": tenant_id,
            "object_type": object_type,
            "object_id": object_id,
            "object_name": object_name,
            "details": details or {},
            "source_ip": source_ip,
            "user_agent": user_agent,
            "result": result,
            "reason": reason
        }
        
        await db.audit_logs.insert_one(audit_entry)
        logger.debug(f"Audit logged: {action} by {actor_email or actor_user_id}")
        
    except Exception as e:
        logger.error(f"Failed to log audit event: {str(e)}")


# ============================================================================
# ANALYTICS LOGGING
# ============================================================================

async def log_analytics_event(
    db: AsyncIOMotorDatabase,
    event_type: AnalyticsEventType,
    event_name: str,
    user_id: Optional[str] = None,
    tenant_id: Optional[str] = None,
    user_role: Optional[str] = None,
    assessment_id: Optional[str] = None,
    assessment_type: Optional[str] = None,
    properties: Optional[Dict[str, Any]] = None,
    duration_ms: Optional[int] = None
):
    """
    Log an analytics event for product insights.
    """
    try:
        analytics_entry = {
            "timestamp": datetime.now(timezone.utc),
            "event_type": event_type.value if isinstance(event_type, AnalyticsEventType) else event_type,
            "event_name": event_name,
            "user_id": user_id,
            "tenant_id": tenant_id,
            "user_role": user_role,
            "assessment_id": assessment_id,
            "assessment_type": assessment_type,
            "properties": properties or {},
            "duration_ms": duration_ms
        }
        
        await db.analytics_events.insert_one(analytics_entry)
        
    except Exception as e:
        logger.error(f"Failed to log analytics event: {str(e)}")


# ============================================================================
# ERROR LOGGING
# ============================================================================

async def log_error(
    db: AsyncIOMotorDatabase,
    error_type: str,
    error_message: str,
    endpoint: Optional[str] = None,
    method: Optional[str] = None,
    status_code: Optional[int] = None,
    user_id: Optional[str] = None,
    tenant_id: Optional[str] = None,
    assessment_id: Optional[str] = None,
    stack_trace: Optional[str] = None,
    request_data: Optional[Dict[str, Any]] = None,
    severity: ErrorSeverity = ErrorSeverity.MEDIUM,
    source_ip: Optional[str] = None
):
    """
    Log an error event for debugging and monitoring.
    """
    try:
        error_entry = {
            "timestamp": datetime.now(timezone.utc),
            "error_type": error_type,
            "error_message": error_message,
            "endpoint": endpoint,
            "method": method,
            "status_code": status_code,
            "user_id": user_id,
            "tenant_id": tenant_id,
            "assessment_id": assessment_id,
            "stack_trace": stack_trace,
            "request_data": request_data,
            "severity": severity.value if isinstance(severity, ErrorSeverity) else severity,
            "source_ip": source_ip,
            "resolved": False
        }
        
        await db.error_logs.insert_one(error_entry)
        logger.warning(f"Error logged: {error_type} - {error_message[:100]}")
        
    except Exception as e:
        logger.error(f"Failed to log error: {str(e)}")


# ============================================================================
# LOG RETRIEVAL
# ============================================================================

async def get_audit_logs(
    db: AsyncIOMotorDatabase,
    tenant_id: Optional[str] = None,
    action: Optional[str] = None,
    actor_user_id: Optional[str] = None,
    actor_email: Optional[str] = None,
    object_type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 50
) -> tuple[List[Dict], int]:
    """
    Retrieve audit logs with filters.
    Returns (logs, total_count)
    """
    query = {}
    
    if tenant_id:
        query["tenant_id"] = tenant_id
    if action:
        query["action"] = action
    if actor_user_id:
        query["actor_user_id"] = actor_user_id
    if actor_email:
        query["actor_email"] = actor_email
    if object_type:
        query["object_type"] = object_type
    if start_date or end_date:
        query["timestamp"] = {}
        if start_date:
            query["timestamp"]["$gte"] = start_date
        if end_date:
            query["timestamp"]["$lte"] = end_date
    
    total = await db.audit_logs.count_documents(query)
    
    cursor = db.audit_logs.find(query, {"_id": 0}).sort("timestamp", -1).skip(skip).limit(limit)
    logs = await cursor.to_list(length=limit)
    
    return logs, total


async def get_analytics_summary(
    db: AsyncIOMotorDatabase,
    tenant_id: Optional[str] = None,
    days: int = 30
) -> Dict[str, Any]:
    """
    Get analytics summary for the dashboard.
    """
    start_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    match_stage = {"timestamp": {"$gte": start_date}}
    if tenant_id:
        match_stage["tenant_id"] = tenant_id
    
    # Assessment funnel stats
    pipeline = [
        {"$match": match_stage},
        {"$group": {
            "_id": "$event_name",
            "count": {"$sum": 1}
        }}
    ]
    
    event_counts = {}
    async for doc in db.analytics_events.aggregate(pipeline):
        event_counts[doc["_id"]] = doc["count"]
    
    # Daily activity
    daily_pipeline = [
        {"$match": match_stage},
        {"$group": {
            "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$timestamp"}},
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id": 1}}
    ]
    
    daily_activity = []
    async for doc in db.analytics_events.aggregate(daily_pipeline):
        daily_activity.append({"date": doc["_id"], "count": doc["count"]})
    
    # Assessment type breakdown
    type_pipeline = [
        {"$match": {**match_stage, "assessment_type": {"$ne": None}}},
        {"$group": {
            "_id": "$assessment_type",
            "count": {"$sum": 1}
        }}
    ]
    
    assessment_types = {}
    async for doc in db.analytics_events.aggregate(type_pipeline):
        assessment_types[doc["_id"]] = doc["count"]
    
    return {
        "period_days": days,
        "event_counts": event_counts,
        "daily_activity": daily_activity,
        "assessment_types": assessment_types,
        "total_events": sum(event_counts.values())
    }


async def get_error_logs(
    db: AsyncIOMotorDatabase,
    tenant_id: Optional[str] = None,
    severity: Optional[str] = None,
    resolved: Optional[bool] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 50
) -> tuple[List[Dict], int]:
    """
    Retrieve error logs with filters.
    """
    query = {}
    
    if tenant_id:
        query["tenant_id"] = tenant_id
    if severity:
        query["severity"] = severity
    if resolved is not None:
        query["resolved"] = resolved
    if start_date or end_date:
        query["timestamp"] = {}
        if start_date:
            query["timestamp"]["$gte"] = start_date
        if end_date:
            query["timestamp"]["$lte"] = end_date
    
    total = await db.error_logs.count_documents(query)
    
    cursor = db.error_logs.find(query, {"_id": 0}).sort("timestamp", -1).skip(skip).limit(limit)
    logs = await cursor.to_list(length=limit)
    
    return logs, total


async def get_error_summary(
    db: AsyncIOMotorDatabase,
    tenant_id: Optional[str] = None,
    days: int = 7
) -> Dict[str, Any]:
    """
    Get error summary statistics.
    """
    start_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    match_stage = {"timestamp": {"$gte": start_date}}
    if tenant_id:
        match_stage["tenant_id"] = tenant_id
    
    # Error counts by severity
    severity_pipeline = [
        {"$match": match_stage},
        {"$group": {
            "_id": "$severity",
            "count": {"$sum": 1}
        }}
    ]
    
    severity_counts = {}
    async for doc in db.error_logs.aggregate(severity_pipeline):
        severity_counts[doc["_id"]] = doc["count"]
    
    # Error counts by type
    type_pipeline = [
        {"$match": match_stage},
        {"$group": {
            "_id": "$error_type",
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    
    top_errors = []
    async for doc in db.error_logs.aggregate(type_pipeline):
        top_errors.append({"type": doc["_id"], "count": doc["count"]})
    
    # Daily error trend
    daily_pipeline = [
        {"$match": match_stage},
        {"$group": {
            "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$timestamp"}},
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id": 1}}
    ]
    
    daily_errors = []
    async for doc in db.error_logs.aggregate(daily_pipeline):
        daily_errors.append({"date": doc["_id"], "count": doc["count"]})
    
    total_errors = sum(severity_counts.values())
    unresolved = await db.error_logs.count_documents({**match_stage, "resolved": False})
    
    return {
        "period_days": days,
        "total_errors": total_errors,
        "unresolved_count": unresolved,
        "severity_breakdown": severity_counts,
        "top_errors": top_errors,
        "daily_trend": daily_errors
    }


# ============================================================================
# CLEANUP
# ============================================================================

async def cleanup_old_logs(
    db: AsyncIOMotorDatabase,
    retention_days: int = 90
) -> Dict[str, int]:
    """
    Remove logs older than retention period.
    Returns count of deleted documents per collection.
    """
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=retention_days)
    
    results = {}
    
    # Clean audit logs
    audit_result = await db.audit_logs.delete_many({"timestamp": {"$lt": cutoff_date}})
    results["audit_logs"] = audit_result.deleted_count
    
    # Clean analytics events
    analytics_result = await db.analytics_events.delete_many({"timestamp": {"$lt": cutoff_date}})
    results["analytics_events"] = analytics_result.deleted_count
    
    # Clean error logs
    error_result = await db.error_logs.delete_many({"timestamp": {"$lt": cutoff_date}})
    results["error_logs"] = error_result.deleted_count
    
    logger.info(f"Log cleanup completed: {results}")
    
    return results


# ============================================================================
# INDEX CREATION
# ============================================================================

async def ensure_log_indexes(db: AsyncIOMotorDatabase):
    """
    Create indexes for efficient log queries.
    """
    # Audit logs indexes
    await db.audit_logs.create_index([("timestamp", -1)])
    await db.audit_logs.create_index([("tenant_id", 1), ("timestamp", -1)])
    await db.audit_logs.create_index([("action", 1), ("timestamp", -1)])
    await db.audit_logs.create_index([("actor_user_id", 1), ("timestamp", -1)])
    
    # Analytics events indexes
    await db.analytics_events.create_index([("timestamp", -1)])
    await db.analytics_events.create_index([("tenant_id", 1), ("timestamp", -1)])
    await db.analytics_events.create_index([("event_name", 1), ("timestamp", -1)])
    
    # Error logs indexes
    await db.error_logs.create_index([("timestamp", -1)])
    await db.error_logs.create_index([("tenant_id", 1), ("timestamp", -1)])
    await db.error_logs.create_index([("severity", 1), ("timestamp", -1)])
    await db.error_logs.create_index([("resolved", 1), ("timestamp", -1)])
    
    logger.info("Log indexes created/verified")
