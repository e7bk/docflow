from shared.database import init_database, SessionLocal
from auth.models import User
from werkzeug.security import generate_password_hash

def create_test_user():
    """Create a test user for API testing"""
    
    init_database()
    db = SessionLocal()
    
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.id == 1).first()
        if existing_user:
            print(f"✅ Test user already exists: {existing_user.username}")
            return
        
        # Create test user
        test_user = User(
            username="testuser",
            email="test@docflow.com",
            password_hash=generate_password_hash("password123")
        )
        db.add(test_user)
        db.commit()
        
        print(f"✅ Created test user: {test_user.username} (ID: {test_user.id})")
        
    except Exception as e:
        print(f"❌ Failed to create test user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()
