from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Float, ForeignKey, CheckConstraint
from sqlalchemy.sql import func
from shared.database import Base

class Document(Base):
    __tablename__ = "documents"
    
    # Basic document info
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)  # Links to user who uploaded it
    filename = Column(String(100), nullable=False)  # What the user sees
    file_path = Column(String(500), nullable=False)  # Where it's actually stored
    file_size = Column(Integer, nullable=False)  # Size in bytes
    mime_type = Column(String(50), nullable=False)  # application/pdf etc
    
    # Status tracking - took me a while to get these states right
    status = Column(String(20), nullable=False, default="uploaded")
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())  # Auto timestamp
    processed_at = Column(DateTime(timezone=True), nullable=True)  # When processing finished
    
    # Database constraint to prevent invalid status values - learned this prevents data corruption
    __table_args__ = (
        CheckConstraint("status IN ('uploaded', 'processing', 'completed', 'failed')", 
                       name='valid_status'),
    )
    
    def __repr__(self):
        # Useful for debugging - shows key info when you print the object
        return f"<Document(id={self.id}, filename='{self.filename}', status='{self.status}')>"
