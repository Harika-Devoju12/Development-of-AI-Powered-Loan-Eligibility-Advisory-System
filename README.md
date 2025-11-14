# Loan Eligibility AI System

A complete loan eligibility system with AI-powered chat and voice interfaces, document verification, and manager dashboard.

## 🎯 Quick Links

- 📖 [Setup Guide](./SETUP_GUIDE.md) - Complete setup instructions
- 🔗 [Integration Guide](./INTEGRATION_GUIDE.md) - AWS & third-party service integration
- 📋 [API Documentation](./backend/README.md) - Backend API reference
- 🧠 [Project Context](./copilot/context.md) - Project overview for AI

## Features

- **Chat Interface**: Interactive AI chatbot to collect loan application details
- **Voice Integration**: Voice call support via Amazon Connect (placeholder)
- **Document Processing**: Aadhaar verification and bank statement analysis
- **ML Prediction**: Loan eligibility scoring with SHAP explainability
- **Manager Dashboard**: Review applications, view documents, approve/reject loans

## Tech Stack

### Frontend
- React 18 with TypeScript
- Tailwind CSS for styling
- React Router for navigation
- Axios for API calls
- Lucide React for icons

### Backend
- FastAPI (Python)
- Supabase (PostgreSQL)
- JWT authentication
- Pydantic models
- scikit-learn for ML

### AWS Services (Optional)
- Amazon Bedrock - Conversational AI
- Amazon Textract - Document OCR
- Amazon SageMaker - ML model deployment
- Amazon S3 - Document storage
- Amazon SNS - Notifications
- Amazon Connect - Voice calls
- Amazon CloudWatch - Logging

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.9+
- Supabase account

### Frontend Setup

1. Install dependencies:
```bash
npm install
```

2. Create environment file:
```bash
cp .env.example .env
# Edit .env with your API URL and Supabase credentials
```

3. Run development server:
```bash
npm run dev
```

The app will be available at http://localhost:5173

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your Supabase credentials
```

5. Run the FastAPI server:
```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## Application Flow

1. **Landing Page** (`/`): User chooses between Chat or Voice interface
2. **Chat Interface** (`/chat`): AI collects user information through conversation
3. **Document Upload** (`/upload-documents`): User uploads Aadhaar and bank statement
4. **Verification** (`/verify-aadhaar`): Documents are verified
5. **Results** (`/result`): Eligibility score and SHAP explanation displayed
6. **Manager Review**: Manager approves or rejects the application

## Manager Dashboard

Access the manager dashboard at `/manager-login`

**Default credentials:**
- Email: admin@loanbank.com
- Password: admin123

⚠️ **Change these credentials in production!**

## Routes

| Route | Description |
|-------|-------------|
| `/` | Landing page - choose chat or voice |
| `/chat` | Chat interface with AI assistant |
| `/upload-documents` | Upload Aadhaar and bank statement |
| `/verify-aadhaar` | Document verification status |
| `/result` | Eligibility results with explanation |
| `/manager-login` | Manager login page |
| `/manager-dashboard` | Manager dashboard to review applications |

## API Endpoints

### Public Endpoints
- `POST /start-session` - Create new application session
- `POST /chat-input` - Send chat message
- `POST /voice-webhook` - Voice call webhook (Amazon Connect)
- `POST /verify-aadhaar` - Verify Aadhaar document
- `POST /process-bank-statement` - Process bank statement
- `POST /predict` - Get eligibility prediction

### Manager Endpoints (Authenticated)
- `POST /manager/login` - Manager login
- `GET /manager/applications` - List all applications
- `GET /manager/application/{id}` - Get application details
- `POST /manager/approve` - Approve application
- `POST /manager/reject` - Reject application

Full API docs available at: `http://localhost:8000/docs`

## Database Schema

### Tables

**loan_applications**
- Application data including income, loan amount, credit score
- Document verification status
- Eligibility score and SHAP explanation
- Final approval status

**managers**
- Manager credentials and profile

**chat_history**
- Chat conversation history for each session

## Configuration

### Environment Variables

Create `.env` files based on `.env.example`:

**Frontend** (.env):
```
VITE_API_URL=http://localhost:8000
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
```

**Backend** (backend/.env):
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-key
JWT_SECRET=your-secret-key
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
# ... other optional AWS configs
```

See `.env.example` and `backend/.env.example` for all available options.

## AWS Integration

The system is designed to integrate with AWS services. Currently, mock implementations are provided for development.

### Services Configuration

| Service | Status | Setup Required |
|---------|--------|-----------------|
| Amazon Bedrock | 🔄 Mock | Yes (optional) |
| Amazon Textract | 🔄 Mock | Yes (optional) |
| Amazon SageMaker | 🔄 Mock | Yes (optional) |
| Amazon S3 | 🔄 Mock | Yes (optional) |
| Amazon SNS | ❌ Not implemented | Manual setup |
| Amazon Connect | 🔄 Mock | Yes (optional) |

### Quick Integration Guide

To enable real AWS services:

1. Set up AWS credentials in `backend/.env`
2. Set feature flags to `False`:
   ```
   USE_MOCK_BEDROCK=False
   USE_MOCK_TEXTRACT=False
   USE_MOCK_SAGEMAKER=False
   USE_MOCK_S3=False
   ```
3. Configure service-specific variables
4. Restart backend server

See [INTEGRATION_GUIDE.md](./INTEGRATION_GUIDE.md) for detailed setup.

## ML Model

The system uses a rule-based eligibility model that considers:
- Credit score (weight: 35%)
- Debt-to-income ratio (weight: 25%)
- EMI-to-income ratio (weight: 20%)
- Employment type (weight: 15%)
- Monthly income (weight: 10%)

To integrate a trained model:
1. Place your `loan_model.pkl` in the backend directory
2. Update `backend/.env`:
   ```
   USE_LOCAL_ML_MODEL=True
   ML_MODEL_PATH=./loan_model.pkl
   ```
3. Or deploy to SageMaker and configure `SAGEMAKER_ENDPOINT_NAME`

## Build for Production

```bash
npm run build
```

Built files will be in the `dist` directory.

## Type Checking

```bash
npm run typecheck
```

## Linting

```bash
npm run lint
```

## Project Structure

```
.
├── src/
│   ├── components/        # Reusable components
│   ├── pages/            # Page components
│   ├── services/         # API service layer
│   └── App.tsx           # Main app with routing
├── backend/
│   ├── main.py           # FastAPI app
│   ├── models.py         # Pydantic models
│   ├── auth.py           # Authentication logic
│   ├── database.py       # Supabase client
│   ├── chat_service.py   # Chat conversation logic
│   ├── document_service.py  # Document processing
│   ├── ml_service.py     # ML prediction logic
│   ├── aws_services.py   # AWS integration
│   └── config.py         # Configuration
├── supabase/
│   └── migrations/       # Database migrations
├── INTEGRATION_GUIDE.md  # AWS integration guide
└── SETUP_GUIDE.md        # Complete setup guide
```

## Security Notes

- JWT tokens for manager authentication
- Row Level Security (RLS) enabled on all tables
- Password hashing with bcrypt
- Session-based application tracking
- All sensitive credentials in `.env` (not committed)

## Troubleshooting

### Backend won't connect to Supabase
- Verify `SUPABASE_URL` and `SUPABASE_KEY` in `.env`
- Check network connectivity
- Ensure Supabase project is running

### Frontend API errors
- Check `VITE_API_URL` in `.env`
- Ensure backend is running on `http://localhost:8000`
- Clear browser cache and reload

### AWS service errors
- Verify AWS credentials are correct
- Check service is enabled in AWS Console
- Review CloudWatch logs
- Use mock services while debugging

See [SETUP_GUIDE.md](./SETUP_GUIDE.md) for more troubleshooting.

## Future Enhancements

- [ ] Real-time voice call integration with Amazon Connect
- [ ] Advanced fraud detection
- [ ] Credit bureau integration
- [ ] Automated decision engine
- [ ] Multi-language support
- [ ] SMS/Email notifications via SNS
- [ ] Email reports
- [ ] Dashboard analytics and reporting

## Deployment

### Quick Deployment Checklist

- [ ] All environment variables configured
- [ ] Database migrations applied
- [ ] Credentials changed from defaults
- [ ] CORS origins updated
- [ ] SSL/HTTPS enabled
- [ ] Rate limiting configured
- [ ] Error logging configured
- [ ] Backups enabled

See [SETUP_GUIDE.md](./SETUP_GUIDE.md) for production deployment steps.

## License

Proprietary - All rights reserved

---

## 📞 Support & Documentation

- **Setup Issues?** → See [SETUP_GUIDE.md](./SETUP_GUIDE.md)
- **AWS Integration?** → See [INTEGRATION_GUIDE.md](./INTEGRATION_GUIDE.md)
- **API Reference?** → See [backend/README.md](./backend/README.md)
- **Project Context?** → See [copilot/context.md](./copilot/context.md)
