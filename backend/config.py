from dotenv import load_dotenv
import os
from typing import Optional, List
import json

# Load environment variables from .env file
load_dotenv()

class Settings:
    # ====================
    # Server Configuration
    # ====================
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    PORT: int = int(os.getenv("PORT", "8000"))

    # ====================
    # Database - Supabase
    # ====================
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    SUPABASE_SERVICE_KEY: str = os.getenv("SUPABASE_SERVICE_KEY", "")

    # ====================
    # JWT Authentication
    # ====================
    JWT_SECRET: str = os.getenv("JWT_SECRET", "change-this-secret-key-in-production")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_HOURS: int = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))

    # Default manager (testing only - CHANGE IN PRODUCTION)
    DEFAULT_MANAGER_EMAIL: str = os.getenv("DEFAULT_MANAGER_EMAIL", "admin@loanbank.com")
    DEFAULT_MANAGER_PASSWORD: str = os.getenv("DEFAULT_MANAGER_PASSWORD", "admin123")
    DEFAULT_MANAGER_NAME: str = os.getenv("DEFAULT_MANAGER_NAME", "Admin Manager")

    # ====================
    # AWS General
    # ====================
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")

    # ====================
    # AWS Bedrock (Conversational AI)
    # ====================
    BEDROCK_REGION: str = os.getenv("BEDROCK_REGION", "us-east-1")
    BEDROCK_MODEL_ID: str = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-v2")

    # ====================
    # AWS Textract (Document OCR)
    # ====================
    TEXTRACT_REGION: str = os.getenv("TEXTRACT_REGION", "us-east-1")

    # ====================
    # AWS SageMaker (ML Model)
    # ====================
    SAGEMAKER_REGION: str = os.getenv("SAGEMAKER_REGION", "us-east-1")
    SAGEMAKER_ENDPOINT_NAME: str = os.getenv("SAGEMAKER_ENDPOINT_NAME", "loan-eligibility-endpoint")
    USE_LOCAL_ML_MODEL: bool = os.getenv("USE_LOCAL_ML_MODEL", "True").lower() == "true"
    ML_MODEL_PATH: str = os.getenv("ML_MODEL_PATH", "./loan_model.pkl")

    # ====================
    # AWS S3 (Document Storage)
    # ====================
    S3_REGION: str = os.getenv("S3_REGION", "us-east-1")
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME", "loan-documents-bucket")
    S3_UPLOAD_EXPIRATION: int = int(os.getenv("S3_UPLOAD_EXPIRATION", "3600"))

    # ====================
    # AWS Connect (Voice Integration)
    # ====================
    CONNECT_INSTANCE_ID: str = os.getenv("CONNECT_INSTANCE_ID", "")
    CONNECT_CONTACT_FLOW_ID: str = os.getenv("CONNECT_CONTACT_FLOW_ID", "")
    CONNECT_COUNTRY_CODE: str = os.getenv("CONNECT_COUNTRY_CODE", "+1")

    # ====================
    # AWS Voice ID (Voice Authentication)
    # ====================
    VOICE_ID_DOMAIN_ID: str = os.getenv("VOICE_ID_DOMAIN_ID", "")
    VOICE_ID_REGION: str = os.getenv("VOICE_ID_REGION", "us-east-1")

    # ====================
    # AWS SNS (Notifications)
    # ====================
    SNS_REGION: str = os.getenv("SNS_REGION", "us-east-1")
    SNS_TOPIC_ARN_SMS: str = os.getenv("SNS_TOPIC_ARN_SMS", "")
    SNS_TOPIC_ARN_EMAIL: str = os.getenv("SNS_TOPIC_ARN_EMAIL", "")
    ENABLE_SMS_NOTIFICATIONS: bool = os.getenv("ENABLE_SMS_NOTIFICATIONS", "False").lower() == "true"
    ENABLE_EMAIL_NOTIFICATIONS: bool = os.getenv("ENABLE_EMAIL_NOTIFICATIONS", "False").lower() == "true"

    # ====================
    # AWS CloudWatch
    # ====================
    CLOUDWATCH_REGION: str = os.getenv("CLOUDWATCH_REGION", "us-east-1")
    CLOUDWATCH_LOG_GROUP: str = os.getenv("CLOUDWATCH_LOG_GROUP", "/aws/loan-eligibility-api")
    ENABLE_CLOUDWATCH_LOGGING: bool = os.getenv("ENABLE_CLOUDWATCH_LOGGING", "False").lower() == "true"

    # ====================
    # Feature Flags
    # ====================
    USE_MOCK_BEDROCK: bool = os.getenv("USE_MOCK_BEDROCK", "True").lower() == "true"
    USE_MOCK_TEXTRACT: bool = os.getenv("USE_MOCK_TEXTRACT", "True").lower() == "true"
    USE_MOCK_SAGEMAKER: bool = os.getenv("USE_MOCK_SAGEMAKER", "True").lower() == "true"
    USE_MOCK_S3: bool = os.getenv("USE_MOCK_S3", "True").lower() == "true"
    USE_MOCK_SNS: bool = os.getenv("USE_MOCK_SNS", "True").lower() == "true"

    # ====================
    # CORS Configuration
    # ====================
    @property
    def CORS_ORIGINS(self) -> List[str]:
        origins_str = os.getenv("CORS_ORIGINS", '["http://localhost:5173","http://localhost:3000"]')
        try:
            return json.loads(origins_str)
        except:
            return ["http://localhost:5173", "http://localhost:3000"]

    # ====================
    # Security
    # ====================
    ALLOWED_UPLOAD_EXTENSIONS: List[str] = ["pdf", "jpg", "jpeg", "png"]
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", str(10 * 1024 * 1024)))  # 10MB
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    RATE_LIMIT_WINDOW_SECONDS: int = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))

settings = Settings()
