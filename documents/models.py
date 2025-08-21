from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Float, ForeignKey, CheckConstraint
from sqlalchemy.sql import func
from shared.database import Base

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    filename = Column(String(100), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False, default="uploaded")
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Database constraint for status validation
    __table_args__ = (
        CheckConstraint("status IN ('uploaded', 'processing', 'completed', 'failed')", 
                       name='valid_status'),
    )
    
    def __repr__(self):
        return f"<Document(id={self.id}, filename='{self.filename}', status='{self.status}')>"
