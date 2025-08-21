# DocFlow - Document Processing System

A document upload system I built out of curiosity, which turned into quite the learning journey with FastAPI.

## Why I Built This
Started this project out of curiosity about how secure file uploads work. What began as a simple experiment turned into a proper learning journey with FastAPI, database design, and API security. The hardest part was getting the API working properly, but I really enjoyed building the file validation logic.

## 🚀 What It Does
- Handles file uploads with proper validation (PDF, Word, Excel, CSV)
- Checks file sizes and types to prevent dodgy uploads  
- Stores files safely in user-specific directories
- Built a REST API that documents itself (FastAPI magic)
- Database constraints to stop invalid data getting through
- File validation logic I'm quite proud of - catches extension spoofing attempts

## 🛠️ Technical Architecture
### Backend Stack
- **FastAPI**: Modern, fast web framework with automatic API documentation
- **SQLAlchemy**: Database ORM with advanced relationship management
- **SQLite**: Lightweight database with constraint enforcement
- **Uvicorn**: ASGI server for production deployment

### Key Engineering Decisions
- **Size-first validation**: Fast failure for oversized files (10MB limit)
- **MIME + extension validation**: Security-focused file type checking
- **User directory isolation**: Scalable file storage architecture
- **4-stage document lifecycle**: Clean status management (uploaded → processing → completed → failed)

## 📁 Project Structure
docflow/
├── auth/                 # User authentication models
├── documents/            # Document management (models, routes, services)
├── processing/           # Background processing logic
├── shared/              # Common utilities and database configuration
├── uploads/             # File storage directory
├── main.py              # FastAPI application entry point
└── requirements.txt     # Python dependencies
## 🔧 Installation & Setup

### Prerequisites
- Python 3.8+
- Virtual environment

### Quick Start
1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/docflow.git
   cd docflow
2. Set up Virtual environment
python -m venv docflow-env
source docflow-env/bin/activate  # On Windows: docflow-env\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. initialise database
python setup_database.py
5. Start the application
python main.py
6. Access the API
Main application: http://localhost:8000
Interactive API documentation: http://localhost:8000/docs
Alternative documentation: http://localhost:8000/redoc

📚 API Endpoints
Document Management

POST /documents/ → Upload new document with validation
GET /documents/ → List all documents (with optional filtering)
GET /documents/{id} → Retrieve specific document details
DELETE /documents/{id} → Delete document and associated file

System Information

GET / → API welcome message and feature overview
GET /health → System health check and configuration info

Query Parameters

GET /documents/?status=uploaded → Filter by document status
GET /documents/?status=completed → Show only processed documents
GET /documents/?status=processing → Show documents currently being processed
GET /documents/?status=failed → Show documents that failed processing

Security Features
File Validation Pipeline

    File Size Validation: Configurable upload size limits (default: 10MB)
    File Type Validation: Whitelist of allowed document formats
    MIME Type Verification: Prevents file type spoofing attacks
    Extension Matching: Ensures file extension matches declared type
    Path Traversal Protection: Sanitises filenames to prevent directory attacks

User Isolation

    Each user's files stored in separate directories
    Unique filename generation prevents conflicts
    Database constraints ensure data integrity

Supported File Types

    PDF: application/pdf
    Microsoft Word: application/vnd.openxmlformats-officedocument.wordprocessingml.document (.docx)
    Legacy Word: application/msword (.doc)
    Microsoft Excel: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet (.xlsx)
    Legacy Excel: application/vnd.ms-excel (.xls)
    CSV: text/csv

🧪 Testing

The system includes comprehensive validation testing:
bash

# Test upload validation logic
python clean_upload_test.py

# Test database setup and constraints
python setup_database.py

# Test complete upload workflow
python test_upload_service.py

Test Coverage

    File size validation (oversized file rejection)
    File type validation (unsupported format rejection)
    MIME/extension mismatch detection
    Database constraint enforcement
    Error recovery mechanisms

📊 Validation Pipeline

File Upload Request
        ↓
1. Size Check (Fast Failure)
        ↓
2. File Type Validation
        ↓
3. MIME/Extension Security Check
        ↓
4. Filename Sanitisation
        ↓
5. Unique Name Generation
        ↓
6. User Directory Storage
        ↓
7. Database Record Creation
        ↓
8. Success Response

🚀 Production Considerations
Scalability

    User-isolated storage structure supports horizontal scaling
    Database design allows for easy partitioning
    Stateless API design enables load balancing

Monitoring & Observability

    Comprehensive error logging with context
    Health check endpoints for monitoring
    Detailed API documentation for debugging

Security

    Multi-layered validation prevents common upload vulnerabilities
    Database constraints ensure data consistency
    Input sanitisation prevents injection attacks

Performance

    Size-first validation for fast rejection of invalid files
    Efficient file storage with user-based partitioning
    Database indexing on commonly queried fields

🛠️ Configuration
Environment Variables
bash

DATABASE_URL=sqlite:///./docflow.db    # Database connection string
UPLOAD_DIR=./uploads                   # File storage directory
MAX_FILE_SIZE=10485760                # Maximum file size in bytes (10MB)

Customisation

    Modify ALLOWED_MIME_TYPES in documents/service.py to add file types
    Adjust MAX_FILE_SIZE for different size limits
    Update database models for additional metadata fields

📖 Development
Architecture Patterns

    Service Layer Pattern: Business logic separated from API routing
    Repository Pattern: Data access abstraction
    Dependency Injection: Clean testing and modularity
    Error Handling: Consistent exception management

Code Quality

    Type hints throughout codebase
    Comprehensive docstrings
    Consistent naming conventions
    Separation of concerns

🤝 Contributing

This project demonstrates production-ready software engineering practices:

    Clean Architecture: Modular design with clear boundaries
    Security-First Approach: Multiple validation layers
    Error Recovery: Graceful failure handling
    Database Design: Proper constraints and relationships
    API Design: RESTful conventions with automatic documentation
    Testing Strategy: Comprehensive validation testing

🐛 Troubleshooting
Common Issues

Database Foreign Key Errors
bash

# Reset database if foreign key constraints fail
rm docflow.db
python setup_database.py

Import Errors
bash

# Ensure virtual environment is activated
source docflow-env/bin/activate
pip install -r requirements.txt

File Upload Failures

    Check file size (must be under 10MB)
    Verify file type is supported
    Ensure sufficient disk space

📄 Licence

This project is available under the MIT Licence.
🔗 Links

    FastAPI Documentation
    SQLAlchemy Documentation
    Python Type Hints

Built with modern Python and software engineering best practices
