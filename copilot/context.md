# Project Context for GitHub Copilot

## 🏦 Project Title
AI-Powered Loan Eligibility Advisory System

## 🎯 Goal
To build an **AI-driven loan advisory system** that interacts with users through **chat or voice calls**, collects loan details, verifies identity & documents, predicts eligibility using an ML model, and provides a manager dashboard for manual approvals.

The entire system runs on **React (Frontend)** + **FastAPI (Backend)** + **AWS AI Services**.

---

## 💬 Core Idea
Both **Chatbot** (web UI) and **Voice Agent** (Amazon Connect) share the **same backend intelligence** and workflow.

They:
- Ask the same loan-related questions (name, income, credit score, loan amount, etc.)
- Verify documents and Aadhaar
- Use the same AI backend (FastAPI + Bedrock + SageMaker)
- Produce the same type of eligibility report
- Send results to the **Manager Dashboard**

---

## ⚙️ Backend Stack
**Language:** Python  
**Framework:** FastAPI  
**Core Integrations:**
- Amazon Bedrock → Conversation reasoning  
- Amazon SageMaker → ML model for eligibility scoring  
- Amazon Textract → Bank statement document extraction  
- Amazon Voice ID → Voice authentication  
- Amazon SNS → Notifications (SMS/email)  
- Amazon S3 → File storage (Aadhaar + bank statements)  
- RDS / DynamoDB → Data storage  
- CloudWatch → Monitoring & logs  

**Endpoints to maintain:**
/start-session
/chat-input
/voice-webhook
/upload-url
/verify-aadhaar
/process-bank-statement
/predict
/save-report
/manager/login
/manager/applications
/manager/approve
/manager/reject

yaml
Copy code

**Key files to expect:**
- `main.py` → FastAPI entry  
- `routes/` → individual route modules  
- `services/` → AWS & ML logic (Textract, SageMaker, Bedrock)  
- `models/` → DB schema  
- `utils/` → helpers (session, security, PDF reports)  

---

## 💻 Frontend Stack
**Framework:** React + TailwindCSS + Axios  
**Routing:** React Router DOM  
**Pages to include:**
| Route | Purpose |
|-------|----------|
| `/` | Landing Page — choose Chat or Voice |
| `/chat` | Chatbot conversation |
| `/upload-documents` | Aadhaar & Bank upload |
| `/verify-aadhaar` | Aadhaar verification result |
| `/result` | Eligibility score & explanation |
| `/manager-login` | Manager login page |
| `/manager-dashboard` | Manager approval dashboard |

**Landing Page Behavior**
Two options:
- 💬 Start Chat → `/chat`
- 🎤 Start Voice Assistant → shows Amazon Connect number or “Call Now” button

**Both use the same backend APIs**.

---

## 🧠 ML Component
- Model: XGBoost (loan eligibility)  
- Inputs:
  - income, credit_score, loan_amount, EMI, document_verified, voice_verified  
- Output:
  - eligibility_score (0–1)
  - SHAP explanation dict
- Deployed via SageMaker (or local joblib model during dev).

---

## 🧾 Features Summary
✅ Chatbot conversation flow  
✅ Voice call via Amazon Connect (same logic)  
✅ Aadhaar verification (OCR mock)  
✅ Bank statement analysis (Textract mock)  
✅ ML prediction & explainability  
✅ Manager dashboard with Approve/Reject  
✅ Notifications via SNS  
✅ Reports stored in S3  
✅ CloudWatch logging

---

## 🔄 Workflow Summary
User → chooses Chat or Voice
↓
Chat/Voice collects user details
↓
Aadhaar & Bank statement uploaded
↓
Textract extracts income/EMI → FastAPI
↓
FastAPI calls SageMaker model
↓
Prediction + SHAP explanation generated
↓
Report saved → Manager Dashboard
↓
Manager approves/rejects → SNS notification


## 💡 Copilot Instructions
When modifying code or generating functions, **follow these rules**:

1. Keep Chatbot and Voice Agent using **shared logic** (same backend endpoints).  
2. Never duplicate logic for chat and voice — just different input/output.  
3. When asked to add features, preserve AWS integrations and data schema.  
4. Always maintain FastAPI + React modular structure.  
5. Include comments like:  
   ```python
   # TODO: Integrate with Amazon Bedrock later
Use mock data if an AWS call is unavailable locally.

Keep design minimal, responsive, and accessible.