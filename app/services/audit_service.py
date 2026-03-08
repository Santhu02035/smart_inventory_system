from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog


def create_audit_log(db: Session, username: str, action: str, entity: str, details: str):

    log = AuditLog(
        username=username,
        action=action,
        entity=entity,
        details=details
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log