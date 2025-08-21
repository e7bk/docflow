from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from shared.database import get_db
from documents.service import DocumentService
from documents.models import Document

# Create the router for document endpoints
router = APIRouter()

@router.post("/", status_code=201)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a document - YOUR DESIGN IN ACTION!
    
    - Validates file size (10MB limit)
    - Validates file type (PDF, Word, Excel, CSV)
    - Validates MIME/extension match (security)
    - Saves to user directory structure
    - Creates database record
    """
    
    # For now, we'll use a test user (we'll add real auth later)
    test_user_id = 1
    
    try:
        # Use your upload service!
        service = DocumentService(db)
        document = service.upload_document(test_user_id, file)
        
        # Return success response (your API design)
        return {
            "document_id": document.id,
            "filename": document.filename,
            "file_size": document.file_size,
            "mime_type": document.mime_type,
            "status": document.status,
            "uploaded_at": document.uploaded_at,
            "message": "Upload successful! Your validation logic worked perfectly!"
        }
        
    except HTTPException as e:
        # Your service already creates proper HTTP exceptions
        raise e
    except Exception as e:
        # Catch any unexpected errors
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/", response_model=List[dict])
async def list_documents(
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    List documents with optional status filtering
    
    - GET /documents - All documents
    - GET /documents?status=completed - Only completed
    - GET /documents?status=uploaded - Only uploaded
    """
    
    # For now, use test user
    test_user_id = 1
    
    try:
        query = db.query(Document).filter(Document.user_id == test_user_id)
        
        # Apply status filter if provided
        if status:
            query = query.filter(Document.status == status)
        
        documents = query.all()
        
        # Return document list
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
    """
    Get specific document details
    """
    
    # For now, use test user
    test_user_id = 1
    
    try:
        document = db.query(Document).filter(
            Document.id == document_id,
            Document.user_id == test_user_id
        ).first()
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
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
    """
    Delete a document (removes both file and database record)
    """
    
    # For now, use test user
    test_user_id = 1
    
    try:
        document = db.query(Document).filter(
            Document.id == document_id,
            Document.user_id == test_user_id
        ).first()
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Delete file from storage
        import os
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
        
        # Delete database record
        db.delete(document)
        db.commit()
        
        return {
            "message": f"Document {document.filename} deleted successfully",
            "document_id": document_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {str(e)}")
