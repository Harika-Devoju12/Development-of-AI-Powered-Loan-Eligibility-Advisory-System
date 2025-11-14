from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class SessionCreate(BaseModel):
    channel: str = Field(..., description="chat or voice")

class SessionResponse(BaseModel):
    session_id: str
    message: str

class ChatInput(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
    next_step: Optional[str] = None

class VoiceWebhook(BaseModel):
    session_id: str
    transcript: str
    call_id: Optional[str] = None

class AadhaarVerifyRequest(BaseModel):
    session_id: str
    document_text: str

class AadhaarVerifyResponse(BaseModel):
    verified: bool
    message: str
    extracted_data: Optional[Dict[str, Any]] = None

class BankStatementRequest(BaseModel):
    session_id: str
    document_text: str

class BankStatementResponse(BaseModel):
    income_extracted: float
    emi_detected: float
    message: str

class PredictRequest(BaseModel):
    session_id: str

class PredictResponse(BaseModel):
    eligibility_score: float
    eligible: bool
    message: str
    shap_explanation: List[Dict[str, Any]]

class ManagerLogin(BaseModel):
    email: str
    password: str

class ManagerLoginResponse(BaseModel):
    token: str
    name: str
    email: str

class ApplicationSummary(BaseModel):
    id: str
    session_id: str
    name: Optional[str]
    income_claimed: Optional[float]
    loan_amount: Optional[float]
    credit_score: Optional[int]
    final_status: str
    created_at: str

class ApplicationDetail(BaseModel):
    id: str
    session_id: str
    name: Optional[str]
    income_claimed: Optional[float]
    income_extracted: Optional[float]
    loan_amount: Optional[float]
    credit_score: Optional[int]
    employment_type: Optional[str]
    emi_detected: Optional[float]
    aadhaar_verified: bool
    documents_verified: bool
    eligibility_score: Optional[float]
    final_status: str
    shap_explanation: Optional[Dict[str, Any]]
    aadhaar_document_url: Optional[str]
    bank_statement_url: Optional[str]
    created_at: str
    updated_at: str

class ApprovalRequest(BaseModel):
    application_id: str
    manager_email: str

class UploadUrlRequest(BaseModel):
    session_id: str
    file_type: str
