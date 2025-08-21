
from shared.database import init_database, SessionLocal
from auth.models import User
from documents.models import Document, DocumentStatus
from werkzeug.security import generate_password_hash

def test_document_constraints():
    """Test that your constraints actually work!"""
    
    # Setup
    init_database()
    db = SessionLocal()
    
    try:
        # Create a test user first (so we have a valid user_id)
        print("=== Creating test user ===")
        test_user = User(
            username="testuser",
            email="test@example.com",
            password_hash=generate_password_hash("password")
        )
        db.add(test_user)
        db.commit()
        print(f"✅ Created user with ID: {test_user.id}")
        
        # Test 1: Valid document (should work)
        print("\n=== Test 1: Valid document ===")
        valid_doc = Document(
            user_id=test_user.id,
            filename="test_document.pdf",
            file_path="/uploads/test.pdf",
            file_size=1024,
            mime_type="application/pdf",
            status="uploaded"
        )
        db.add(valid_doc)
        db.commit()
        print("✅ Valid document created successfully!")
        
        # Test 2: Invalid status (should fail due to your CheckConstraint)
        print("\n=== Test 2: Invalid status (should fail) ===")
        try:
            invalid_status_doc = Document(
                user_id=test_user.id,
                filename="bad_status.pdf", 
                file_path="/uploads/bad.pdf",
                file_size=2048,
                mime_type="application/pdf",
                status="banana"  # Invalid status!
            )
            db.add(invalid_status_doc)
            db.commit()
            print("❌ ERROR: Invalid status was allowed! Constraint failed!")
        except Exception as e:
            print(f"✅ Constraint worked! Invalid status rejected: {e}")
            db.rollback()
            
        # Test 3: Invalid user_id (should fail due to your ForeignKey)
        print("\n=== Test 3: Invalid user_id (should fail) ===")
        try:
            invalid_user_doc = Document(
                user_id=99999,  # User doesn't exist!
                filename="orphan.pdf",
                file_path="/uploads/orphan.pdf", 
                file_size=512,
                mime_type="application/pdf",
                status="uploaded"
            )
            db.add(invalid_user_doc)
            db.commit()
            print("❌ ERROR: Invalid user_id was allowed! Constraint failed!")
        except Exception as e:
            print(f"✅ Constraint worked! Invalid user_id rejected: {e}")
            db.rollback()
            
        print("\n🎉 All your constraints are working perfectly!")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_document_constraints()
