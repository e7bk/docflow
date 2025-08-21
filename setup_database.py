from shared.database import init_database, SessionLocal, engine
from auth.models import User
from documents.models import Document
from werkzeug.security import generate_password_hash

def setup_complete_database():
    """Set up complete database with all tables and test data"""
    
    print("🗄️ Setting up DocFlow database...")
    
    try:
        # Create all tables (this ensures proper order)
        print("Creating all database tables...")
        init_database()
        print("✅ All tables created successfully")
        
        # Create session
        db = SessionLocal()
        
        try:
            # Check if test user exists
            existing_user = db.query(User).filter(User.id == 1).first()
            if existing_user:
                print(f"✅ Test user already exists: {existing_user.username}")
            else:
                # Create test user
                test_user = User(
                    username="testuser",
                    email="test@docflow.com",
                    password_hash=generate_password_hash("password123")
                )
                db.add(test_user)
                db.commit()
                print(f"✅ Created test user: {test_user.username} (ID: {test_user.id})")
            
            print("🎉 Database setup complete!")
            print("🚀 Ready to start DocFlow API!")
            
        except Exception as e:
            print(f"❌ Error setting up test data: {e}")
            db.rollback()
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        print("💡 This might be a dependency issue between tables")

if __name__ == "__main__":
    setup_complete_database()
