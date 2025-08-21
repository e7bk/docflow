import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from documents.models import Document

# File upload limits and allowed types
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB - for personal reasons
UPLOAD_BASE_DIR = "./uploads"

# Only allow document files - learnt this prevents loads of security problems
ALLOWED_MIME_TYPES = {
    "application/pdf": ".pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "application/msword": ".doc",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
    "application/vnd.ms-excel": ".xls",
    "text/csv": ".csv"
}

class DocumentService:
    def __init__(self, db: Session):
        self.db = db
    
    def upload_document(self, user_id: int, upload_file: UploadFile) -> Document:
        """Upload a document with your validation strategy"""
        
        # Check size first - quickest way to reject any massive files
        file_size = self._validate_file_size(upload_file)
        
        # Make sure file type is allowed and not spoofed
        self._validate_file_type(upload_file)
        
        # Create unique username to avoid any conflicts
        unique_filename = self._generate_unique_filename(upload_file.filename)
        
        # Save to users own folder
        file_path = self._save_file_to_storage(user_id, upload_file, unique_filename)
        
        # Create database record - (THIS TOOK ME AGES TO GET RIGHT)
        document = self._create_document_record(user_id, upload_file, unique_filename, file_path, file_size)
        
        return document
    
    def _validate_file_size(self, upload_file: UploadFile):
        """Check file size before doing anything else - learned that this stops wasting processing time"""
        # Get file size by seeking to end and checking position
        upload_file.file.seek(0, 2)
        file_size = upload_file.file.tell()
        upload_file.file.seek(0) # Reset position
        
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB"
            )
        
        return file_size
    
    def _validate_file_type(self, upload_file: UploadFile):
        """Validate both MIME type and file extension"""
        # First check if MIME type is allowed
        if upload_file.content_type not in ALLOWED_MIME_TYPES:
            allowed_types = ", ".join(ALLOWED_MIME_TYPES.values())
            raise HTTPException(
                status_code=400,
                detail=f"File type not supported. Allowed types: {allowed_types}"
            )
        # Then check extension matches MIME TYPE (security bit)
        expected_extension = ALLOWED_MIME_TYPES[upload_file.content_type]
        actual_extension = os.path.splitext(upload_file.filename)[1].lower()
        
        if actual_extension != expected_extension:
            raise HTTPException(
                status_code=400,
                detail=f"File extension '{actual_extension}' doesn't match file type. Expected '{expected_extension}'"
            )
    
    def _sanitize_filename(self, filename: str) -> str:
        """Clean filename of dangerous characters"""
        import re
        # Replace characters that are not allowed with underscores
        safe_filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        safe_filename = safe_filename.replace('..', '_') # To provent directory traversal
        
        # Keep filename at a reasonable length to avoid conflicts
        if len(safe_filename) > 80:
            name, ext = os.path.splitext(safe_filename)
            safe_filename = name[:80-len(ext)] + ext
        
        return safe_filename
    
    def _generate_unique_filename(self, original_filename: str) -> str:
        """Generate unique filename with timestamp"""
        safe_filename = self._sanitize_filename(original_filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name, ext = os.path.splitext(safe_filename)
        unique_filename = f"{name}_{timestamp}{ext}"
        return unique_filename
    
    def _save_file_to_storage(self, user_id: int, upload_file: UploadFile, unique_filename: str) -> str:
        """Save file to user directory"""
        # Create user directory if it does not exist
        user_dir = Path(UPLOAD_BASE_DIR) / f"user_{user_id}"
        user_dir.mkdir(parents=True, exist_ok=True)
        file_path = user_dir / unique_filename
        
        # Automatically save the file
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
        
        return str(file_path)
    
    def _create_document_record(self, user_id: int, upload_file: UploadFile, unique_filename: str, file_path: str, file_size: int) -> Document:
        """Create database record"""
        document = Document(
            user_id=user_id,
            filename=unique_filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=upload_file.content_type,
            status="uploaded"
        )
        
        # Save to database with error handling
        try:
            self.db.add(document)
            self.db.commit()
            self.db.refresh(document)
            return document
        except Exception as e:
            # Clean up file if database fails
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(status_code=500, detail=f"Failed to create document record: {str(e)}")













