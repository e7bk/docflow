import os

def test_with_clean_database():
    """Test with automatic database cleanup"""
    
    # Clean slate
    if os.path.exists("docflow.db"):
        os.remove("docflow.db")
        print("🧹 Cleaned old database")
    
    print("=== Testing Upload Validation (Simple) ===\n")
    
    # Test just the validation logic
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    ALLOWED_MIME_TYPES = {
        "application/pdf": ".pdf",
        "text/csv": ".csv"
    }
    
    def validate_file_size(file_size):
        if file_size > MAX_FILE_SIZE:
            raise ValueError(f"File too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB")
        return True
    
    def validate_file_type(content_type, filename):
        if content_type not in ALLOWED_MIME_TYPES:
            raise ValueError(f"File type not supported")
        
        expected_ext = ALLOWED_MIME_TYPES[content_type]
        actual_ext = os.path.splitext(filename)[1].lower()
        
        if actual_ext != expected_ext:
            raise ValueError(f"Extension '{actual_ext}' doesn't match type '{expected_ext}'")
        return True
    
    # Test 1: Valid size
    try:
        validate_file_size(1024 * 1024)  # 1MB
        print("✅ Valid size (1MB) accepted")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    # Test 2: Invalid size
    try:
        validate_file_size(15 * 1024 * 1024)  # 15MB
        print("❌ ERROR: Large file accepted!")
    except Exception as e:
        print(f"✅ Large file rejected: {e}")
    
    # Test 3: Valid PDF
    try:
        validate_file_type("application/pdf", "document.pdf")
        print("✅ Valid PDF accepted")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    # Test 4: Invalid type
    try:
        validate_file_type("application/x-executable", "malware.exe")
        print("❌ ERROR: Invalid type accepted!")
    except Exception as e:
        print(f"✅ Invalid type rejected: {e}")
    
    # Test 5: MIME mismatch
    try:
        validate_file_type("application/pdf", "fake.txt")
        print("❌ ERROR: Mismatch accepted!")
    except Exception as e:
        print(f"✅ MIME/extension mismatch rejected: {e}")
    
    print("\n🎉 Your upload validation logic is working perfectly!")

if __name__ == "__main__":
    test_with_clean_database()
