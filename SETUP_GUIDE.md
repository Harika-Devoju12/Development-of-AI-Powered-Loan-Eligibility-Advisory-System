# 🚀 Setup & Integration Guide

Complete step-by-step guide to set up and integrate the Loan Eligibility AI System.

## Prerequisites

- Node.js 18+
- Python 3.9+
- AWS Account (with Bedrock, Textract, SageMaker, S3, SNS access)
- Supabase Account
- Git

## Part 1: Frontend Setup

### 1.1 Install Frontend Dependencies

```bash
npm install
```

### 1.2 Create Frontend Environment File

```bash
cp .env.example .env
```

Edit `.env`:
```
VITE_API_URL=http://localhost:8000
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key-here
VITE_ENABLE_VOICE=true
```

### 1.3 Run Frontend Development Server

```bash
npm run dev
```

Access at: `http://localhost:5173`

---

## Part 2: Backend Setup

### 2.1 Create Python Virtual Environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2.2 Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2.3 Create Backend Environment File

```bash
cp .env.example .env
```

### 2.4 Configure Environment Variables

Edit `backend/.env` with your credentials:

**Critical (Required to run):**
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
```

**Optional (AWS Services - for full integration):**
```
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_REGION=us-east-1
```

### 2.5 Run Backend Server

```bash
uvicorn main:app --reload
```

API Documentation: `http://localhost:8000/docs`

---

## Part 3: Database Setup (Supabase)

### 3.1 Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Copy `SUPABASE_URL` and `SUPABASE_KEY` to `.env` files

### 3.2 Run Migrations

1. Go to Supabase Dashboard → SQL Editor
2. Run the migration SQL from: `supabase/migrations/20251107102354_create_loan_application_system.sql`
3. Verify tables are created:
   - `loan_applications`
   - `managers`
   - `chat_history`

### 3.3 Create Default Manager

In Supabase SQL Editor, run:

```sql
INSERT INTO managers (email, name, password_hash, created_at)
VALUES (
  'admin@loanbank.com',
  'Admin Manager',
  '$2b$12$your_bcrypt_hash_here',  -- Use bcrypt hash of 'admin123'
  NOW()
);
```

Or create via Python:
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed = pwd_context.hash("admin123")
print(hashed)
```

---

## Part 4: AWS Integration

### 4.1 AWS Bedrock Setup (Chat AI)

**Status:** Optional (mock available)

1. Navigate to AWS Console → Amazon Bedrock
2. Enable models: `Anthropic Claude v2` or `Claude 3`
3. Add credentials to `.env`:

```
BEDROCK_MODEL_ID=anthropic.claude-v2
AWS_REGION=us-east-1
USE_MOCK_BEDROCK=False  # When ready to use real Bedrock
```

**Test:**
```python
# In backend directory
python3 -c "from aws_services import bedrock_service; print('Bedrock ready')"
```

### 4.2 AWS Textract Setup (Document OCR)

**Status:** Optional (mock available)

1. In AWS Console, Textract service is usually auto-enabled
2. Set up S3 bucket for document storage
3. Configure IAM role with Textract permissions

Add to `.env`:
```
S3_BUCKET_NAME=your-bucket-name
TEXTRACT_REGION=us-east-1
USE_MOCK_TEXTRACT=False
```

### 4.3 AWS S3 Setup (Document Storage)

**Status:** Optional (mock available)

1. Create S3 bucket: `loan-documents-bucket`
2. Enable CORS on bucket with:

```json
[
  {
    "AllowedHeaders": ["*"],
    "AllowedMethods": ["PUT", "POST", "GET"],
    "AllowedOrigins": ["http://localhost:5173", "http://localhost:3000"],
    "ExposeHeaders": ["ETag"]
  }
]
```

3. Add to `.env`:

```
S3_BUCKET_NAME=loan-documents-bucket
S3_REGION=us-east-1
USE_MOCK_S3=False  # When ready
```

### 4.4 AWS SageMaker Setup (ML Model)

**Status:** Optional (uses rule-based scoring by default)

1. Train your XGBoost model in SageMaker
2. Deploy as real-time endpoint
3. Get endpoint name from SageMaker console

Add to `.env`:
```
SAGEMAKER_ENDPOINT_NAME=loan-eligibility-endpoint
SAGEMAKER_REGION=us-east-1
USE_MOCK_SAGEMAKER=False  # When ready
```

**Alternative: Use Local Model**
```
USE_LOCAL_ML_MODEL=True
ML_MODEL_PATH=./loan_model.pkl
```

### 4.5 AWS SNS Setup (Notifications) - Optional

1. Create SNS topics in AWS
2. Configure subscriptions (Email, SMS)
3. Add to `.env`:

```
SNS_TOPIC_ARN_SMS=arn:aws:sns:region:account:topic
ENABLE_SMS_NOTIFICATIONS=True
```

### 4.6 Amazon Connect Setup (Voice) - Optional

This is complex - see detailed setup below.

---

## Part 5: Testing

### 5.1 Quick Test

Frontend:
```bash
npm run typecheck
npm run lint
```

Backend:
```bash
python -m pytest tests/  # If tests exist
```

### 5.2 Manual Testing

1. **Chat Flow:**
   - Go to `http://localhost:5173`
   - Click "Start Chat"
   - Answer all questions
   - Upload documents

2. **Manager Dashboard:**
   - Go to `http://localhost:5173/manager-login`
   - Login with: `admin@loanbank.com` / `admin123`
   - Review applications

3. **API Testing:**
   - Visit `http://localhost:8000/docs` (Swagger UI)
   - Try endpoints

---

## Part 6: Troubleshooting

### Backend Won't Start

```bash
# Check Python version
python3 --version  # Should be 3.9+

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check environment variables
echo $SUPABASE_URL
```

### Frontend API Connection Error

```bash
# Check backend is running
curl http://localhost:8000/

# Verify VITE_API_URL in .env
cat .env

# Clear cache and rebuild
rm -rf node_modules
npm install
npm run dev
```

### Supabase Connection Failed

```bash
# Verify credentials
echo $SUPABASE_URL
echo $SUPABASE_KEY

# Test connection
python3 -c "from database import get_supabase; print(get_supabase())"
```

### AWS Service Errors

```bash
# Check AWS credentials
aws sts get-caller-identity

# Check boto3 installation
pip show boto3

# Enable mock services while debugging
USE_MOCK_BEDROCK=True
USE_MOCK_S3=True
```

---

## Part 7: Production Deployment

### 7.1 Environment Variables

**NEVER commit `.env` to git!**

Use:
- AWS Secrets Manager
- Environment variables in deployment platform
- Secure vaults (HashiCorp Vault, etc.)

### 7.2 Frontend Deployment

**Netlify/Vercel:**
```bash
npm run build
# Upload dist/ folder
```

**AWS S3 + CloudFront:**
```bash
npm run build
aws s3 sync dist/ s3://your-bucket/ --delete
```

### 7.3 Backend Deployment

**AWS Elastic Beanstalk:**
```bash
eb create loan-eligibility-api
eb deploy
```

**AWS Lambda + API Gateway:**
```bash
pip install zappa
zappa init
zappa deploy production
```

**Docker:**
```bash
docker build -t loan-api .
docker run -p 8000:8000 --env-file .env loan-api
```

### 7.4 Database Backup

```sql
-- In Supabase: Database → Backups
-- Enable automatic backups
```

---

## Part 8: Monitoring & Logging

### Check Logs

Frontend errors: Browser console (F12)
Backend errors: Terminal output or CloudWatch

### Monitor Performance

- Supabase: Dashboard → Metrics
- AWS CloudWatch: Logs & monitoring
- Application: Use `/docs` API endpoint for testing

---

## Quick Commands Reference

```bash
# Frontend
cd .
npm install
npm run dev        # Development
npm run build      # Production build
npm run lint       # Linting
npm run typecheck  # Type checking

# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload  # Development

# Database
# In Supabase console - SQL Editor
# Run migration file
```

---

## 📞 Support

For issues:
1. Check logs in terminal
2. Review `INTEGRATION_GUIDE.md`
3. Check API docs: `http://localhost:8000/docs`
4. Check AWS CloudWatch logs

---

## Next Steps

1. ✅ Set up frontend and backend locally
2. ✅ Configure Supabase database
3. ✅ Test chat flow and manager dashboard
4. 📋 Integrate AWS Bedrock (when ready)
5. 📋 Integrate AWS Textract (when ready)
6. 📋 Deploy to production

**Good luck! 🚀**
