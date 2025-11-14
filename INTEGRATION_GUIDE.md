# 🚀 Integration Guide - AI-Powered Loan Eligibility Advisory System

## Overview
This document provides a complete integration checklist for connecting AWS services, Supabase, and other third-party services to the Loan Eligibility AI System.

---

## 📋 Integration Checklist

### 1. **AWS Services Setup**

#### ✅ Amazon Bedrock (Conversational AI)
**Current Status:** Mock implementation in `chat_service.py`

**Integration Steps:**
1. Install AWS SDK: `pip install boto3`
2. Configure AWS credentials in `.env`:
   ```
   AWS_ACCESS_KEY_ID=your_key
   AWS_SECRET_ACCESS_KEY=your_secret
   AWS_REGION=us-east-1
   BEDROCK_MODEL_ID=anthropic.claude-v2
   ```
3. Update `chat_service.py` to use Bedrock:
   ```python
   import boto3
   bedrock = boto3.client('bedrock-runtime', region_name=AWS_REGION)
   response = bedrock.invoke_model(modelId=BEDROCK_MODEL_ID, body=json.dumps(...))
   ```

**File to Update:** `backend/chat_service.py` (Line ~20)

---

#### ✅ Amazon Textract (Document OCR)
**Current Status:** Mock implementation in `document_service.py`

**Integration Steps:**
1. Install AWS SDK (already in requirements)
2. Add to `.env`:
   ```
   AWS_REGION=us-east-1
   S3_BUCKET_NAME=your-loan-bucket
   ```
3. Update `document_service.py`:
   ```python
   import boto3
   textract = boto3.client('textract', region_name=AWS_REGION)
   response = textract.detect_document_text(Document={'S3Object': {'Bucket': bucket, 'Name': key}})
   ```

**File to Update:** `backend/document_service.py`

---

#### ✅ Amazon SageMaker (ML Model Deployment)
**Current Status:** Rule-based scoring in `ml_service.py`

**Integration Steps:**
1. Train and deploy your XGBoost model on SageMaker
2. Get endpoint name from SageMaker console
3. Add to `.env`:
   ```
   SAGEMAKER_ENDPOINT_NAME=loan-eligibility-endpoint
   SAGEMAKER_REGION=us-east-1
   ```
4. Update `ml_service.py`:
   ```python
   import boto3
   sagemaker_client = boto3.client('sagemaker-runtime', region_name=AWS_REGION)
   response = sagemaker_client.invoke_endpoint(
       EndpointName=ENDPOINT_NAME,
       ContentType='application/json',
       Body=json.dumps(features)
   )
   ```

**File to Update:** `backend/ml_service.py`

---

#### ✅ Amazon S3 (Document Storage)
**Current Status:** Mock presigned URLs in `main.py`

**Integration Steps:**
1. Create S3 bucket for documents
2. Enable CORS on the bucket
3. Add to `.env`:
   ```
   S3_BUCKET_NAME=loan-documents-bucket
   AWS_REGION=us-east-1
   AWS_ACCESS_KEY_ID=your_key
   AWS_SECRET_ACCESS_KEY=your_secret
   ```
4. Update `/upload-url` endpoint in `main.py`:
   ```python
   import boto3
   s3 = boto3.client('s3')
   presigned_url = s3.generate_presigned_post(
       Bucket=S3_BUCKET_NAME,
       Key=f'{session_id}/{file_type}'
   )
   ```

**File to Update:** `backend/main.py` (Line ~115)

---

#### ✅ Amazon Connect (Voice Integration)
**Current Status:** Mock webhook in `main.py` endpoint `/voice-webhook`

**Integration Steps:**
1. Set up Amazon Connect contact center
2. Create contact flow with Lambda integration
3. Add webhook URL to Connect: `https://your-domain.com/voice-webhook`
4. Update `/voice-webhook` endpoint to parse Connect payload
5. Integrate with Lex for intent recognition

**File to Update:** `backend/main.py` (Line ~104)

**Connect Lambda Integration:**
```python
def lambda_handler(event, context):
    transcript = event['Details']['ContactData']['Attributes']['transcript']
    response = requests.post(f'{API_URL}/voice-webhook', json={
        'session_id': event['Details']['ContactData']['ContactId'],
        'transcript': transcript
    })
    return response.json()
```

---

#### ✅ Amazon Voice ID (Voice Authentication)
**Current Status:** Not implemented

**Integration Steps:**
1. Enable Voice ID in Amazon Connect
2. Add Voice ID verification in voice flow:
   ```python
   voiceid = boto3.client('voiceid')
   response = voiceid.evaluate_session(
       DomainId='your-domain-id',
       SessionNameOrId=session_id
   )
   ```

**File to Create:** `backend/voice_service.py`

---

#### ✅ Amazon SNS (Notifications)
**Current Status:** Not implemented

**Integration Steps:**
1. Create SNS topics for SMS/Email notifications
2. Add to `.env`:
   ```
   SNS_REGION=us-east-1
   SNS_TOPIC_ARN_SMS=arn:aws:sns:region:account:loan-sms
   SNS_TOPIC_ARN_EMAIL=arn:aws:sns:region:account:loan-email
   ```
3. Create `backend/notification_service.py`:
   ```python
   sns = boto3.client('sns')
   sns.publish(TopicArn=TOPIC_ARN, Message='Application Status Update')
   ```

**File to Create:** `backend/notification_service.py`

---

#### ✅ Amazon CloudWatch (Monitoring)
**Current Status:** Not implemented

**Integration Steps:**
1. Enable CloudWatch logging in Bedrock/Textract/SageMaker
2. Add CloudWatch agent to FastAPI app:
   ```python
   import watchtower
   import logging
   logging.basicConfig(handlers=[watchtower.CloudWatchLogHandler()])
   ```

**File to Create:** `backend/logging_service.py`

---

### 2. **Database Setup**

#### ✅ Supabase (PostgreSQL)
**Current Status:** Integrated, but needs table verification

**Setup Steps:**
1. Create Supabase project
2. Add credentials to `.env`:
   ```
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-key
   ```
3. Run migrations from `supabase/migrations/`
4. Enable Row Level Security (RLS) on all tables

**Tables to Verify:**
- `loan_applications` - Main application data
- `managers` - Manager credentials
- `chat_history` - Chat conversation history

**Migration File:** `supabase/migrations/20251107102354_create_loan_application_system.sql`

---

### 3. **Frontend Configuration**

#### ✅ Environment Variables
Create `.env` file in root:
```
VITE_API_URL=http://localhost:8000
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
```

---

#### ✅ API Service Configuration
**File:** `src/services/api.ts`

**Status:** Ready for integration
- All endpoints defined
- Token-based authentication ready
- Error handling in place

---

### 4. **Backend Environment Setup**

Create `backend/.env`:
```
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key

# JWT
JWT_SECRET=your-secret-key-change-this
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# AWS Services
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1

# AWS Bedrock
BEDROCK_MODEL_ID=anthropic.claude-v2

# AWS SageMaker
SAGEMAKER_ENDPOINT_NAME=loan-eligibility-endpoint

# AWS S3
S3_BUCKET_NAME=loan-documents-bucket

# AWS SNS (Optional)
SNS_REGION=us-east-1
SNS_TOPIC_ARN_SMS=arn:aws:sns:region:account:loan-sms
SNS_TOPIC_ARN_EMAIL=arn:aws:sns:region:account:loan-email

# Server
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO
```

---

## 🔄 Workflow Integration Map

```
User Flow:
┌─────────────────────────────────────────────────────────────┐
│                    Landing Page (/)                         │
│              Choose: Chat or Voice Assistant                │
└──────────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┴─────────────────────┐
        ↓                                            ↓
┌───────────────────┐                    ┌──────────────────────┐
│   Chat Flow       │                    │   Voice Flow         │
│   (/chat)         │                    │   (Amazon Connect)    │
└───────────────────┘                    └──────────────────────┘
        ↓                                            ↓
┌───────────────────────────────────────────────────────────────┐
│  Collect User Info via:                                       │
│  - Bedrock (Chat) or Lex (Voice)                             │
│  - Questions: Name, Income, Loan, Employment, Credit Score   │
└───────────────────────────────────────────────────────────────┘
        ↓
┌───────────────────────────────────────────────────────────────┐
│     Upload Documents (/upload-documents)                      │
│     - Aadhaar: Upload to S3 → Textract → Extract Data        │
│     - Bank Statement: Upload to S3 → Textract → Extract Income│
└───────────────────────────────────────────────────────────────┘
        ↓
┌───────────────────────────────────────────────────────────────┐
│     Verify Documents (/verify-aadhaar)                       │
│     - Validate extracted data                                │
│     - Cross-check with user input                           │
└───────────────────────────────────────────────────────────────┘
        ↓
┌───────────────────────────────────────────────────────────────┐
│     ML Prediction (/predict)                                 │
│     - Send features to SageMaker                             │
│     - Get eligibility score + SHAP explanation              │
└───────────────────────────────────────────────────────────────┘
        ↓
┌───────────────────────────────────────────────────────────────┐
│     Show Results (/result)                                   │
│     - Display eligibility score                              │
│     - Show SHAP explanation factors                         │
└───────────────────────────────────────────────────────────────┘
        ↓
┌───────────────────────────────────────────────────────────────┐
│     Manager Review (/manager-dashboard)                      │
│     - Manager login (/manager-login)                        │
│     - Review applications                                    │
│     - Approve/Reject → SNS Notification                     │
└───────────────────────────────────────────────────────────────┘
```

---

## 📁 Files to Update - Priority Order

### High Priority (Core Functionality)
1. ✅ `backend/requirements.txt` - Add boto3
2. ✅ `backend/.env.example` - Document all env vars
3. ✅ `backend/chat_service.py` - Bedrock integration
4. ✅ `backend/document_service.py` - Textract integration
5. ✅ `backend/ml_service.py` - SageMaker integration
6. ✅ `backend/main.py` - S3 upload URLs

### Medium Priority (Enhanced Features)
7. 📝 `backend/notification_service.py` - SNS notifications
8. 📝 `backend/voice_service.py` - Voice ID integration
9. 📝 `backend/logging_service.py` - CloudWatch logging
10. 📝 `backend/database.py` - RLS configuration

### Low Priority (Nice-to-Have)
11. 📝 `src/services/api.ts` - Add S3 upload handler
12. 📝 Frontend error handling improvements

---

## 🧪 Testing Checklist

- [ ] Local development with mock services works
- [ ] Supabase connection established
- [ ] JWT authentication working
- [ ] Chat flow collects all required data
- [ ] Document upload endpoint returns mock URLs
- [ ] ML prediction returns valid scores
- [ ] Manager login/dashboard functional
- [ ] AWS Bedrock integration tested
- [ ] AWS Textract integration tested
- [ ] AWS SageMaker integration tested
- [ ] AWS S3 upload working
- [ ] AWS SNS notifications sending
- [ ] Error handling and logging working

---

## 🔐 Security Checklist

- [ ] All credentials in `.env`, not in code
- [ ] JWT secret is strong and unique
- [ ] CORS properly configured
- [ ] Rate limiting implemented
- [ ] Input validation on all endpoints
- [ ] Row Level Security enabled on Supabase
- [ ] S3 bucket has restricted access policy
- [ ] Database backups configured
- [ ] Error messages don't expose sensitive info
- [ ] API keys rotated regularly

---

## 📞 Support & Debugging

### Common Issues:

**1. Bedrock Connection Error**
```
Solution: Verify AWS credentials, region, and model ID
Check: BEDROCK_MODEL_ID in .env matches available models
```

**2. Textract Document Extraction Fails**
```
Solution: Ensure document format is supported (PDF, JPEG, PNG)
Check: S3 bucket permissions for Textract role
```

**3. SageMaker Endpoint Not Found**
```
Solution: Verify endpoint is in ACTIVE state
Check: SAGEMAKER_ENDPOINT_NAME matches deployed endpoint
```

**4. Supabase Connection Timeout**
```
Solution: Check network connectivity
Check: SUPABASE_URL and SUPABASE_KEY are correct
```

---

## 🎯 Next Steps

1. **Phase 1:** Set up Supabase and verify database schema
2. **Phase 2:** Integrate AWS Bedrock for chat
3. **Phase 3:** Integrate AWS Textract for document processing
4. **Phase 4:** Deploy ML model to SageMaker
5. **Phase 5:** Integrate S3 for document storage
6. **Phase 6:** Add SNS notifications
7. **Phase 7:** Implement voice integration with Amazon Connect
8. **Phase 8:** Add monitoring with CloudWatch
9. **Phase 9:** Deploy to production

---

## 📞 Quick Reference

| Service | Status | File | Priority |
|---------|--------|------|----------|
| Supabase | ✅ Ready | `backend/database.py` | High |
| Bedrock | 🔄 Mock | `backend/chat_service.py` | High |
| Textract | 🔄 Mock | `backend/document_service.py` | High |
| SageMaker | 🔄 Mock | `backend/ml_service.py` | High |
| S3 | 🔄 Mock | `backend/main.py` | High |
| Connect | 🔄 Mock | `backend/main.py` | Medium |
| Voice ID | ❌ None | TBD | Medium |
| SNS | ❌ None | TBD | Low |
| CloudWatch | ❌ None | TBD | Low |

---

## 🎓 Learning Resources

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Amazon Textract Guide](https://docs.aws.amazon.com/textract/)
- [SageMaker Real-Time Inference](https://docs.aws.amazon.com/sagemaker/latest/dg/realtime-endpoints.html)
- [Supabase Docs](https://supabase.com/docs)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)

