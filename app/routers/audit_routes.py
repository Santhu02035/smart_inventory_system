from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.audit_log import AuditLog
from app.schemas.audit_log_schema import AuditLogResponse
from app.auth.dependencies import require_admin

router = APIRouter(prefix="/audit", tags=["Audit Logs"])


@router.get("/", response_model=list[AuditLogResponse])
def get_audit_logs(
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).all()