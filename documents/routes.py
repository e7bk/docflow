from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from shared.database import get_db
from documents.service import DocumentService
from documents.models import Document

# API endpoints for document operations
router = APIRouter()

@router.post("/", status_code=201)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Handle file uploads with validation
    
    - Checks file size and type
    - Prevents dodgy file extensions
    - Saves to user folders
    - Creates database record
    """
    
    # Using test user for now - proper auth would go here
    test_user_id = 1
    
    try:
        # Let the service handle all the validation logic
        service = DocumentService(db)
        document = service.upload_document(test_user_id, file)
        
        # Return useful info about the uploaded file
        return {
            "document_id": document.id,
            "filename": document.filename,
            "file_size": document.file_size,
            "mime_type": document.mime_type,
            "status": document.status,
            "uploaded_at": document.uploaded_at,
            "message": "Upload successful!"
        }
        
    except HTTPException as e:
        # Service already creates proper error responses
        raise e
    except Exception as e:
        # Catch anything unexpected
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/", response_model=List[dict])
async def list_documents(
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get list of documents, optionally filter by status
    
    Can filter like: /documents?status=completed
    """
    
    # Still using test user
    test_user_id = 1
    
    try:
        # Start with base query for this user
        query = db.query(Document).filter(Document.user_id == test_user_id)
        
        # Add status filter if requested
        if status:
            query = query.filter(Document.status == status)
        
        documents = query.all()
        
        # Return clean list of document info
        return [
            {
                "document_id": doc.id,
                "filename": doc.filename,
                "file_size": doc.file_size,
                "mime_type": doc.mime_type,
                "status": doc.status,
                "uploaded_at": doc.uploaded_at,
                "processed_at": doc.processed_at
            }
            for doc in documents
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list documents: {str(e)}")

@router.get("/{document_id}")
async def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """Get details for a specific document"""
    
    test_user_id = 1
    
    try:
        # Look for document belonging to this user
        document = db.query(Document).filter(
            Document.id == document_id,
            Document.user_id == test_user_id
        ).first()
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Return all the document details
        return {
            "document_id": document.id,
            "filename": document.filename,
            "file_size": document.file_size,
            "mime_type": document.mime_type,
            "status": document.status,
            "uploaded_at": document.uploaded_at,
            "processed_at": document.processed_at,
            "file_path": document.file_path
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get document: {str(e)}")

@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """Delete document and its file - cleans up properly"""
    
    test_user_id = 1
    
    try:
        # Find the document
        document = db.query(Document).filter(
            Document.id == document_id,
            Document.user_id == test_user_id
        ).first()
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Remove actual file first
        import os
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
        
        # Then remove database record
        db.delete(document)
        db.commit()
        
        return {
            "message": f"Document {document.filename} deleted successfully",
            "document_id": document_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        # Rollback database if something goes wrong
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {str(e)}")
