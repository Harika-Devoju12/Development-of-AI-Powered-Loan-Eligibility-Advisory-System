from dotenv import load_dotenv
import os

# Load environment variables FIRST before any other imports
load_dotenv()

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uuid
from datetime import datetime

from models import (
    SessionCreate, SessionResponse, ChatInput, ChatResponse,
    VoiceWebhook, AadhaarVerifyRequest, AadhaarVerifyResponse,
    BankStatementRequest, BankStatementResponse, PredictRequest,
    PredictResponse, ManagerLogin, ManagerLoginResponse,
    ApplicationSummary, ApplicationDetail, ApprovalRequest,
    UploadUrlRequest
)
from database import get_supabase
from auth import authenticate_manager, create_access_token, verify_token
from chat_service import chat_service
from document_service import document_service
from ml_service import ml_service

app = FastAPI(title="Loan Eligibility AI System API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def verify_manager_token(authorization: Optional[str] = Header(None)) -> dict:
    """Verify JWT token for manager authentication"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = authorization.replace("Bearer ", "")
    payload = verify_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload

@app.get("/")
async def root():
    return {"message": "Loan Eligibility AI System API", "version": "1.0.0"}

@app.post("/start-session", response_model=SessionResponse)
async def start_session(session_data: SessionCreate):
    """
    Create a new loan application session.
    Channel can be 'chat' or 'voice'
    """
    supabase = get_supabase()

    session_id = str(uuid.uuid4())

    supabase.table("loan_applications").insert({
        "session_id": session_id,
        "final_status": "pending"
    }).execute()

    if session_data.channel == "chat":
        initial_message = "Hello! Welcome to our loan application system. What is your name?"
    else:
        initial_message = "Voice session started. Please provide your information."

    supabase.table("chat_history").insert({
        "session_id": session_id,
        "role": "assistant",
        "message": initial_message
    }).execute()

    return SessionResponse(
        session_id=session_id,
        message=initial_message
    )

@app.post("/chat-input", response_model=ChatResponse)
async def chat_input(chat_data: ChatInput):
    """
    Process chat input from user.
    Manages conversation flow and collects loan application data.
    """
    result = await chat_service.process_message(chat_data.session_id, chat_data.message)

    return ChatResponse(
        response=result["response"],
        next_step=result.get("next_step")
    )

@app.post("/voice-webhook", response_model=ChatResponse)
async def voice_webhook(voice_data: VoiceWebhook):
    """
    Webhook endpoint for Amazon Connect voice integration.
    Receives transcript and returns text response.
    TODO: Integrate with Amazon Connect, Lex, and Voice ID
    """
    result = await chat_service.process_message(voice_data.session_id, voice_data.transcript)

    return ChatResponse(
        response=result["response"],
        next_step=result.get("next_step")
    )

@app.post("/upload-url")
async def get_upload_url(request: UploadUrlRequest):
    """
    Generate presigned URL for document upload.
    TODO: Integrate with AWS S3 for secure document storage
    Currently returns mock URL
    """
    return {
        "upload_url": f"https://mock-s3-bucket.s3.amazonaws.com/{request.session_id}/{request.file_type}",
        "document_id": str(uuid.uuid4()),
        "message": "Mock upload URL generated. Implement S3 presigned URL in production."
    }

@app.post("/verify-aadhaar", response_model=AadhaarVerifyResponse)
async def verify_aadhaar(request: AadhaarVerifyRequest):
    """
    Verify Aadhaar document using OCR.
    TODO: Replace with AWS Textract integration
    """
    supabase = get_supabase()

    result = document_service.verify_aadhaar(request.document_text)

    supabase.table("loan_applications").update({
        "aadhaar_verified": result["verified"]
    }).eq("session_id", request.session_id).execute()

    return AadhaarVerifyResponse(
        verified=result["verified"],
        message=result["message"],
        extracted_data=result["extracted_data"]
    )

@app.post("/process-bank-statement", response_model=BankStatementResponse)
async def process_bank_statement(request: BankStatementRequest):
    """
    Process bank statement to extract income and EMI.
    TODO: Replace with AWS Textract + intelligent parsing
    """
    supabase = get_supabase()

    result = document_service.process_bank_statement(request.document_text)

    supabase.table("loan_applications").update({
        "income_extracted": result["income_extracted"],
        "emi_detected": result["emi_detected"],
        "documents_verified": True
    }).eq("session_id", request.session_id).execute()

    return BankStatementResponse(
        income_extracted=result["income_extracted"],
        emi_detected=result["emi_detected"],
        message=result["message"]
    )

@app.post("/predict", response_model=PredictResponse)
async def predict_eligibility(request: PredictRequest):
    """
    Run ML model to predict loan eligibility.
    TODO: Replace with SageMaker endpoint or load loan_model.pkl
    """
    supabase = get_supabase()

    result = supabase.table("loan_applications").select("*").eq("session_id", request.session_id).maybe_single().execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Application not found")

    application = result.data

    features = {
        "credit_score": application.get("credit_score", 0),
        "income_extracted": application.get("income_extracted", 0),
        "loan_amount": application.get("loan_amount", 0),
        "emi_detected": application.get("emi_detected", 0),
        "employment_type": application.get("employment_type", "")
    }

    prediction = ml_service.predict_eligibility(features)

    supabase.table("loan_applications").update({
        "eligibility_score": prediction["eligibility_score"],
        "shap_explanation": prediction["shap_explanation"],
        "final_status": "eligible" if prediction["eligible"] else "needs_review"
    }).eq("session_id", request.session_id).execute()

    message = "Congratulations! You are eligible for the loan." if prediction["eligible"] else \
              "Your application needs further review. Consider improving your credit score or reducing existing EMIs."

    return PredictResponse(
        eligibility_score=prediction["eligibility_score"],
        eligible=prediction["eligible"],
        message=message,
        shap_explanation=prediction["shap_explanation"]
    )

@app.post("/save-report")
async def save_report(request: dict):
    """
    Save final application report.
    This endpoint is called after all processing is complete.
    """
    supabase = get_supabase()

    session_id = request.get("session_id")

    supabase.table("loan_applications").update({
        "updated_at": datetime.utcnow().isoformat()
    }).eq("session_id", session_id).execute()

    return {"message": "Report saved successfully"}

@app.post("/manager/login", response_model=ManagerLoginResponse)
async def manager_login(credentials: ManagerLogin):
    """
    Authenticate manager and return JWT token.
    """
    manager = await authenticate_manager(credentials.email, credentials.password)

    if not manager:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"email": manager["email"], "id": manager["id"]})

    return ManagerLoginResponse(
        token=token,
        name=manager["name"],
        email=manager["email"]
    )

@app.get("/manager/applications")
async def get_applications(manager: dict = Depends(verify_manager_token)):
    """
    Get all loan applications for manager review.
    """
    supabase = get_supabase()

    result = supabase.table("loan_applications").select("*").order("created_at", desc=True).execute()

    applications = [
        ApplicationSummary(
            id=app["id"],
            session_id=app["session_id"],
            name=app.get("name"),
            income_claimed=app.get("income_claimed"),
            loan_amount=app.get("loan_amount"),
            credit_score=app.get("credit_score"),
            final_status=app["final_status"],
            created_at=app["created_at"]
        )
        for app in result.data
    ]

    return {"applications": applications}

@app.get("/manager/application/{application_id}")
async def get_application_detail(application_id: str, manager: dict = Depends(verify_manager_token)):
    """
    Get detailed information for a specific application.
    """
    supabase = get_supabase()

    result = supabase.table("loan_applications").select("*").eq("id", application_id).maybe_single().execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Application not found")

    app = result.data

    return ApplicationDetail(
        id=app["id"],
        session_id=app["session_id"],
        name=app.get("name"),
        income_claimed=app.get("income_claimed"),
        income_extracted=app.get("income_extracted"),
        loan_amount=app.get("loan_amount"),
        credit_score=app.get("credit_score"),
        employment_type=app.get("employment_type"),
        emi_detected=app.get("emi_detected"),
        aadhaar_verified=app.get("aadhaar_verified", False),
        documents_verified=app.get("documents_verified", False),
        eligibility_score=app.get("eligibility_score"),
        final_status=app["final_status"],
        shap_explanation=app.get("shap_explanation"),
        aadhaar_document_url=app.get("aadhaar_document_url"),
        bank_statement_url=app.get("bank_statement_url"),
        created_at=app["created_at"],
        updated_at=app["updated_at"]
    )

@app.post("/manager/approve")
async def approve_application(request: ApprovalRequest, manager: dict = Depends(verify_manager_token)):
    """
    Approve a loan application.
    """
    supabase = get_supabase()

    supabase.table("loan_applications").update({
        "final_status": "approved",
        "updated_at": datetime.utcnow().isoformat()
    }).eq("id", request.application_id).execute()

    return {"message": "Application approved successfully"}

@app.post("/manager/reject")
async def reject_application(request: ApprovalRequest, manager: dict = Depends(verify_manager_token)):
    """
    Reject a loan application.
    """
    supabase = get_supabase()

    supabase.table("loan_applications").update({
        "final_status": "rejected",
        "updated_at": datetime.utcnow().isoformat()
    }).eq("id", request.application_id).execute()

    return {"message": "Application rejected successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
