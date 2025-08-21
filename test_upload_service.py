
import os
import tempfile
from io import BytesIO
from sqlalchemy.orm import sessionmaker
from shared.database import engine, init_database
from auth.models import User
from documents.models import Document
from werkzeug.security import generate_password_hash

# Simple mock for UploadFile to avoid FastAPI dependency in tests
class MockUploadFile:
    def __init__(self, filename: str, content: bytes, content_type: str):
        self.filename = filename
        self.file = BytesIO(content)
        self.content_type = content_type

def test_upload_service():
    """Test your upload service logic without FastAPI dependencies"""
    
    # Setup test database
    init_database()
    Session = sessionmaker(bind=engine)
    db = Session()
    
    try:
        # Create test user
        test_user = User(
            username="testuser",
            email="test@example.com", 
            password_hash=generate_password_hash("password")
        )
        db.add(test_user)
        db.commit()
        
        print("=== Testing Document Upload Service ===\n")
        
        # Import here to avoid early import issues
        from documents.service import DocumentService, MAX_FILE_SIZE, ALLOWED_MIME_TYPES
        
        service = DocumentService(db)
        
        # Test 1: Valid PDF upload (should work)
        print("Test 1: Valid PDF upload")
        try:
            pdf_content = b"%PDF-1.4 fake pdf content for testing"
            pdf_file = MockUploadFile("test_document.pdf", pdf_content, "application/pdf")
            
            document = service.upload_document(test_user.id, pdf_file)
            print(f"✅ Success: {document.filename} uploaded")
            print(f"   File path: {document.file_path}")
            print(f"   Status: {document.status}")
            print(f"   Size: {document.file_size} bytes")
            
        except Exception as e:
            print(f"❌ Failed: {e}")
        
        print()
        
        # Test 2: File too large (should fail - your size check)
        print("Test 2: Oversized file (should fail)")
        try:
            # Create file bigger than your 10MB limit
            large_content = b"x" * (MAX_FILE_SIZE + 1000)
            large_file = MockUploadFile("huge.pdf", large_content, "application/pdf")
            
            document = service.upload_document(test_user.id, large_file)
            print("❌ ERROR: Large file was accepted!")
            
        except Exception as e:
            if "File too large" in str(e):
                print(f"✅ Correctly rejected: {e}")
            else:
                print(f"❌ Unexpected error: {e}")
        
        print()
        
        # Test 3: Invalid file type (should fail - your type check)
        print("Test 3: Invalid file type (should fail)")
        try:
            exe_content = b"fake executable content"
            exe_file = MockUploadFile("malware.exe", exe_content, "application/x-executable")
            
            document = service.upload_document(test_user.id, exe_file)
            print("❌ ERROR: Invalid file type was accepted!")
            
        except Exception as e:
            if "File type not supported" in str(e):
                print(f"✅ Correctly rejected: {e}")
            else:
                print(f"❌ Unexpected error: {e}")
        
        print()
        
        # Test 4: MIME type mismatch (should fail - your security enhancement)
        print("Test 4: Extension/MIME mismatch (should fail)")
        try:
            fake_content = b"this is not really a PDF"
            fake_file = MockUploadFile("fake.pdf", fake_content, "text/plain")  # Wrong MIME type!
            
            document = service.upload_document(test_user.id, fake_file)
            print("❌ ERROR: MIME/extension mismatch was accepted!")
            
        except Exception as e:
            if "doesn't match file type" in str(e):
                print(f"✅ Correctly rejected: {e}")
            else:
                print(f"❌ Unexpected error: {e}")
        
        print()
        
        # Test 5: Valid Excel file (test multiple file types)
        print("Test 5: Valid Excel file")
        try:
            excel_content = b"fake excel content for testing"
            excel_file = MockUploadFile("spreadsheet.xlsx", excel_content, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            
            document = service.upload_document(test_user.id, excel_file)
            print(f"✅ Success: {document.filename} uploaded")
            print(f"   MIME type: {document.mime_type}")
            
        except Exception as e:
            print(f"❌ Failed: {e}")
        
        print("\n🎉 Upload service testing complete!")
        
        # Show all uploaded documents
        documents = db.query(Document).filter(Document.user_id == test_user.id).all()
        print(f"\nTotal documents uploaded: {len(documents)}")
        for doc in documents:
            print(f"  - {doc.filename} ({doc.file_size} bytes)")
        
        # Show the actual file structure created
        print(f"\nFiles created in uploads directory:")
        upload_dir = f"./uploads/user_{test_user.id}"
        if os.path.exists(upload_dir):
            for file in os.listdir(upload_dir):
                file_path = os.path.join(upload_dir, file)
                size = os.path.getsize(file_path)
                print(f"  - {file} ({size} bytes)")
        
    except Exception as e:
        print(f"❌ Test setup failed: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_upload_service()
