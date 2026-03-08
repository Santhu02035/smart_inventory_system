from pydantic import BaseModel
from datetime import datetime

class AuditLogResponse(BaseModel):
    id: int
    username: str
    action: str
    entity: str
    details: str
    timestamp: datetime

    class Config:
        orm_mode = True