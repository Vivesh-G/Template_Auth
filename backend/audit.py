from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base
from datetime import datetime
from sqlalchemy.orm import Session

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=True) # Nullable for failed logins or unregistered actions
    action = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String, nullable=True)
    details = Column(String, nullable=True)

def log_action(db: Session, action: str, user_id: int = None, ip_address: str = None, details: str = None):
    """
    Logs an action to the audit_logs table.
    """
    log_entry = AuditLog(
        user_id=user_id,
        action=action,
        ip_address=ip_address,
        details=details,
        timestamp=datetime.utcnow()
    )
    db.add(log_entry)
    try:
        db.commit()
        db.refresh(log_entry)
    except Exception as e:
        print(f"Failed to save audit log: {e}")
        db.rollback()
    return log_entry
