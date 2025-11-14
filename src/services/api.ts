import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface SessionResponse {
  session_id: string;
  message: string;
}

export interface ChatResponse {
  response: string;
  next_step?: string;
}

export interface AadhaarVerifyResponse {
  verified: boolean;
  message: string;
  extracted_data?: any;
}

export interface BankStatementResponse {
  income_extracted: number;
  emi_detected: number;
  message: string;
}

export interface PredictResponse {
  eligibility_score: number;
  eligible: boolean;
  message: string;
  shap_explanation: Array<{
    feature: string;
    impact: number;
    value: any;
    direction: string;
  }>;
}

export interface ManagerLoginResponse {
  token: string;
  name: string;
  email: string;
}

export interface ApplicationSummary {
  id: string;
  session_id: string;
  name?: string;
  income_claimed?: number;
  loan_amount?: number;
  credit_score?: number;
  final_status: string;
  created_at: string;
}

export interface ApplicationDetail {
  id: string;
  session_id: string;
  name?: string;
  income_claimed?: number;
  income_extracted?: number;
  loan_amount?: number;
  credit_score?: number;
  employment_type?: string;
  emi_detected?: number;
  aadhaar_verified: boolean;
  documents_verified: boolean;
  eligibility_score?: number;
  final_status: string;
  shap_explanation?: any;
  aadhaar_document_url?: string;
  bank_statement_url?: string;
  created_at: string;
  updated_at: string;
}

export const apiService = {
  startSession: async (channel: string): Promise<SessionResponse> => {
    const response = await api.post('/start-session', { channel });
    return response.data;
  },

  sendChatMessage: async (session_id: string, message: string): Promise<ChatResponse> => {
    const response = await api.post('/chat-input', { session_id, message });
    return response.data;
  },

  verifyAadhaar: async (session_id: string, document_text: string): Promise<AadhaarVerifyResponse> => {
    const response = await api.post('/verify-aadhaar', { session_id, document_text });
    return response.data;
  },

  processBankStatement: async (session_id: string, document_text: string): Promise<BankStatementResponse> => {
    const response = await api.post('/process-bank-statement', { session_id, document_text });
    return response.data;
  },

  predictEligibility: async (session_id: string): Promise<PredictResponse> => {
    const response = await api.post('/predict', { session_id });
    return response.data;
  },

  saveReport: async (session_id: string): Promise<void> => {
    await api.post('/save-report', { session_id });
  },

  managerLogin: async (email: string, password: string): Promise<ManagerLoginResponse> => {
    const response = await api.post('/manager/login', { email, password });
    return response.data;
  },

  getApplications: async (token: string): Promise<{ applications: ApplicationSummary[] }> => {
    const response = await api.get('/manager/applications', {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  },

  getApplicationDetail: async (application_id: string, token: string): Promise<ApplicationDetail> => {
    const response = await api.get(`/manager/application/${application_id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  },

  approveApplication: async (application_id: string, manager_email: string, token: string): Promise<void> => {
    await api.post('/manager/approve',
      { application_id, manager_email },
      { headers: { Authorization: `Bearer ${token}` } }
    );
  },

  rejectApplication: async (application_id: string, manager_email: string, token: string): Promise<void> => {
    await api.post('/manager/reject',
      { application_id, manager_email },
      { headers: { Authorization: `Bearer ${token}` } }
    );
  },
};
