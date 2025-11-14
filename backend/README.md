# Loan Eligibility AI System - Backend

FastAPI backend for the Loan Eligibility AI System.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your Supabase credentials
```

3. Run the server:
```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Database

The system uses Supabase (PostgreSQL) for data storage. The database schema includes:

- `loan_applications`: Store all loan application data
- `managers`: Store manager credentials
- `chat_history`: Store chat conversation history

## Endpoints

### Public Endpoints

- `POST /start-session`: Create a new loan application session
- `POST /chat-input`: Send chat messages
- `POST /voice-webhook`: Receive voice call transcripts (Amazon Connect integration)
- `POST /upload-url`: Get presigned URL for document upload
- `POST /verify-aadhaar`: Verify Aadhaar document
- `POST /process-bank-statement`: Process bank statement
- `POST /predict`: Run ML eligibility prediction
- `POST /save-report`: Save final report

### Manager Endpoints (Requires JWT Authentication)

- `POST /manager/login`: Manager authentication
- `GET /manager/applications`: List all applications
- `GET /manager/application/{id}`: Get application details
- `POST /manager/approve`: Approve application
- `POST /manager/reject`: Reject application

## Integration Points (TODO)

### AWS Services to Integrate:

1. **Amazon Textract**: Replace `document_service.py` OCR logic
   - Extract text from Aadhaar cards
   - Parse bank statements

2. **Amazon Bedrock**: Replace `chat_service.py` conversation logic
   - Natural language understanding
   - Conversational AI for chat and voice

3. **Amazon Connect**: Integrate with `voice-webhook` endpoint
   - Voice call handling
   - Speech-to-text transcription

4. **Amazon Lex**: Voice agent intelligence
   - Intent recognition
   - Dialog management

5. **Amazon Voice ID**: Voice authentication
   - Caller verification
   - Fraud detection

6. **Amazon S3**: Replace mock upload URLs in `/upload-url`
   - Secure document storage
   - Presigned URL generation

7. **Amazon SageMaker**: Replace `ml_service.py` prediction logic
   - Deploy trained model
   - Real-time inference

## Default Manager Credentials

For testing purposes, a default manager account is created:

- Email: admin@loanbank.com
- Password: admin123

**Important**: Change this password in production!

## Security Notes

- JWT tokens expire after 24 hours (configurable)
- All manager endpoints require Bearer token authentication
- Row Level Security (RLS) is enabled on all database tables
- Passwords are hashed using bcrypt

## ML Model

Currently uses a rule-based scoring system. To integrate a trained model:

1. Place your trained model file (e.g., `loan_model.pkl`) in the backend directory
2. Update `ml_service.py` to load and use the model
3. Ensure the model expects the same feature set:
   - credit_score
   - income_extracted
   - loan_amount
   - emi_detected
   - employment_type
