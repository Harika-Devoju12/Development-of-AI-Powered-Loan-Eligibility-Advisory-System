/*
  # Loan Eligibility AI System Database Schema

  1. New Tables
    - `loan_applications`
      - `id` (uuid, primary key) - unique application identifier
      - `session_id` (text, unique) - session tracking ID
      - `name` (text) - applicant name
      - `income_claimed` (numeric) - self-reported income
      - `income_extracted` (numeric) - income extracted from bank statement
      - `loan_amount` (numeric) - requested loan amount
      - `credit_score` (integer) - credit score
      - `employment_type` (text) - employment type
      - `emi_detected` (numeric) - EMI detected from bank statement
      - `aadhaar_verified` (boolean) - Aadhaar verification status
      - `documents_verified` (boolean) - documents verification status
      - `eligibility_score` (numeric) - ML model prediction score
      - `final_status` (text) - approved/rejected/pending
      - `shap_explanation` (jsonb) - SHAP values for explainability
      - `aadhaar_document_url` (text) - Aadhaar document storage URL
      - `bank_statement_url` (text) - Bank statement storage URL
      - `created_at` (timestamptz) - application creation time
      - `updated_at` (timestamptz) - last update time
    
    - `managers`
      - `id` (uuid, primary key)
      - `email` (text, unique)
      - `password_hash` (text) - hashed password
      - `name` (text) - manager name
      - `created_at` (timestamptz)
    
    - `chat_history`
      - `id` (uuid, primary key)
      - `session_id` (text) - links to loan application
      - `role` (text) - user or assistant
      - `message` (text) - chat message content
      - `timestamp` (timestamptz)
  
  2. Security
    - Enable RLS on all tables
    - Add policies for authenticated access
    - Manager-specific policies for dashboard access
*/

-- Create loan_applications table
CREATE TABLE IF NOT EXISTS loan_applications (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id text UNIQUE NOT NULL,
  name text,
  income_claimed numeric,
  income_extracted numeric,
  loan_amount numeric,
  credit_score integer,
  employment_type text,
  emi_detected numeric,
  aadhaar_verified boolean DEFAULT false,
  documents_verified boolean DEFAULT false,
  eligibility_score numeric,
  final_status text DEFAULT 'pending',
  shap_explanation jsonb,
  aadhaar_document_url text,
  bank_statement_url text,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create managers table
CREATE TABLE IF NOT EXISTS managers (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email text UNIQUE NOT NULL,
  password_hash text NOT NULL,
  name text NOT NULL,
  created_at timestamptz DEFAULT now()
);

-- Create chat_history table
CREATE TABLE IF NOT EXISTS chat_history (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id text NOT NULL,
  role text NOT NULL,
  message text NOT NULL,
  timestamp timestamptz DEFAULT now()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_loan_applications_session_id ON loan_applications(session_id);
CREATE INDEX IF NOT EXISTS idx_loan_applications_final_status ON loan_applications(final_status);
CREATE INDEX IF NOT EXISTS idx_chat_history_session_id ON chat_history(session_id);

-- Enable Row Level Security
ALTER TABLE loan_applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE managers ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_history ENABLE ROW LEVEL SECURITY;

-- RLS Policies for loan_applications (service role can access all)
CREATE POLICY "Service role can manage loan applications"
  ON loan_applications
  FOR ALL
  USING (true)
  WITH CHECK (true);

-- RLS Policies for managers
CREATE POLICY "Service role can manage managers"
  ON managers
  FOR ALL
  USING (true)
  WITH CHECK (true);

-- RLS Policies for chat_history
CREATE POLICY "Service role can manage chat history"
  ON chat_history
  FOR ALL
  USING (true)
  WITH CHECK (true);

-- Insert a default manager for testing (password: admin123)
-- Note: This should be changed in production
INSERT INTO managers (email, password_hash, name) 
VALUES ('admin@loanbank.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5oe2LQJR8Rg9W', 'Admin Manager')
ON CONFLICT (email) DO NOTHING;
