"""
AWS Services Integration Module
Provides interfaces to AWS services: Bedrock, Textract, SageMaker, S3, SNS, CloudWatch
"""

import boto3
import json
import logging
from typing import Dict, Any, Optional
from config import settings

logger = logging.getLogger(__name__)


class BedrockService:
    """
    AWS Bedrock Integration for Conversational AI
    Used for chat and voice conversation logic
    """
    def __init__(self):
        self.client = None
        self.model_id = settings.BEDROCK_MODEL_ID
        if not settings.USE_MOCK_BEDROCK:
            try:
                self.client = boto3.client(
                    'bedrock-runtime',
                    region_name=settings.BEDROCK_REGION,
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                )
                logger.info(f"Bedrock client initialized with model: {self.model_id}")
            except Exception as e:
                logger.error(f"Failed to initialize Bedrock client: {e}")
                self.client = None

    async def get_response(self, prompt: str, conversation_history: Optional[list] = None) -> str:
        """
        Get AI response from Bedrock for given prompt
        
        Args:
            prompt: User message
            conversation_history: Previous conversation messages
            
        Returns:
            AI response string
        """
        if settings.USE_MOCK_BEDROCK or self.client is None:
            return self._mock_bedrock_response(prompt)
        
        try:
            # Prepare messages for Claude
            messages = conversation_history or []
            messages.append({"role": "user", "content": prompt})
            
            body = json.dumps({
                "anthropic_version": "bedrock-2023-06-01",
                "max_tokens": 1024,
                "messages": messages,
                "system": """You are a helpful loan assistant. Your role is to collect loan application details from users through conversation.
                Ask for: name, monthly income, loan amount, employment type, and credit score.
                Be polite and professional. Validate all inputs and ask for clarification if needed."""
            })
            
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=body
            )
            
            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text']
        
        except Exception as e:
            logger.error(f"Bedrock API error: {e}")
            return self._mock_bedrock_response(prompt)

    def _mock_bedrock_response(self, prompt: str) -> str:
        """Mock response for development/testing"""
        return f"Mock Bedrock Response: Understood. {prompt[:30]}... Processing..."


class TextractService:
    """
    AWS Textract Integration for Document OCR
    Used for Aadhaar and bank statement extraction
    """
    def __init__(self):
        self.client = None
        if not settings.USE_MOCK_TEXTRACT:
            try:
                self.client = boto3.client(
                    'textract',
                    region_name=settings.TEXTRACT_REGION,
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                )
                logger.info("Textract client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Textract client: {e}")
                self.client = None

    async def extract_text_from_s3(self, bucket: str, key: str) -> Dict[str, Any]:
        """
        Extract text from document in S3 using Textract
        
        Args:
            bucket: S3 bucket name
            key: S3 object key
            
        Returns:
            Dictionary with extracted text and metadata
        """
        if settings.USE_MOCK_TEXTRACT or self.client is None:
            return self._mock_textract_extraction()
        
        try:
            response = self.client.detect_document_text(
                Document={
                    'S3Object': {
                        'Bucket': bucket,
                        'Name': key
                    }
                }
            )
            
            extracted_text = []
            for item in response['Blocks']:
                if item['BlockType'] == 'LINE':
                    extracted_text.append(item['Text'])
            
            return {
                "success": True,
                "extracted_text": "\n".join(extracted_text),
                "confidence": response['Blocks'][0].get('Confidence', 0.95)
            }
        
        except Exception as e:
            logger.error(f"Textract API error: {e}")
            return self._mock_textract_extraction()

    def _mock_textract_extraction(self) -> Dict[str, Any]:
        """Mock extraction for development"""
        return {
            "success": True,
            "extracted_text": "Mock Textract Extraction: Name: John Doe\nIncome: 50000\nEMI: 5000",
            "confidence": 0.95
        }


class SageMakerService:
    """
    AWS SageMaker Integration for ML Model Inference
    Used for loan eligibility prediction
    """
    def __init__(self):
        self.client = None
        self.endpoint_name = settings.SAGEMAKER_ENDPOINT_NAME
        self.use_local_model = settings.USE_LOCAL_ML_MODEL
        
        if not settings.USE_MOCK_SAGEMAKER and not self.use_local_model:
            try:
                self.client = boto3.client(
                    'sagemaker-runtime',
                    region_name=settings.SAGEMAKER_REGION,
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                )
                logger.info(f"SageMaker client initialized with endpoint: {self.endpoint_name}")
            except Exception as e:
                logger.error(f"Failed to initialize SageMaker client: {e}")
                self.client = None

    async def predict_eligibility(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get eligibility prediction from SageMaker
        
        Args:
            features: Dictionary with credit_score, income, loan_amount, emi, employment_type
            
        Returns:
            Dictionary with eligibility_score, eligible flag, and explanation
        """
        if settings.USE_MOCK_SAGEMAKER or self.client is None:
            return self._mock_prediction(features)
        
        try:
            # Prepare features in format expected by model
            feature_vector = [
                features.get('credit_score', 0),
                features.get('income_extracted', 0),
                features.get('loan_amount', 0),
                features.get('emi_detected', 0)
            ]
            
            response = self.client.invoke_endpoint(
                EndpointName=self.endpoint_name,
                ContentType='application/json',
                Body=json.dumps({'instances': [feature_vector]})
            )
            
            result = json.loads(response['Body'].read().decode())
            
            return {
                "eligibility_score": result.get('predictions', [[0.5]])[0][0],
                "eligible": result.get('predictions', [[0.5]])[0][0] >= 0.65
            }
        
        except Exception as e:
            logger.error(f"SageMaker API error: {e}")
            return self._mock_prediction(features)

    def _mock_prediction(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Mock prediction for development"""
        score = min(0.5 + (features.get('credit_score', 0) / 1000), 1.0)
        return {
            "eligibility_score": round(score, 2),
            "eligible": score >= 0.65
        }


class S3Service:
    """
    AWS S3 Integration for Document Storage
    Used for uploading and managing Aadhaar and bank statements
    """
    def __init__(self):
        self.client = None
        self.bucket_name = settings.S3_BUCKET_NAME
        if not settings.USE_MOCK_S3:
            try:
                self.client = boto3.client(
                    's3',
                    region_name=settings.S3_REGION,
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                )
                logger.info(f"S3 client initialized with bucket: {self.bucket_name}")
            except Exception as e:
                logger.error(f"Failed to initialize S3 client: {e}")
                self.client = None

    async def generate_presigned_upload_url(self, session_id: str, file_type: str) -> Dict[str, Any]:
        """
        Generate presigned URL for direct upload to S3
        
        Args:
            session_id: Application session ID
            file_type: Type of file (aadhaar, bank_statement)
            
        Returns:
            Dictionary with upload URL and metadata
        """
        if settings.USE_MOCK_S3 or self.client is None:
            return self._mock_presigned_url(session_id, file_type)
        
        try:
            key = f"applications/{session_id}/{file_type}/document.pdf"
            
            url = self.client.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': key
                },
                ExpiresIn=settings.S3_UPLOAD_EXPIRATION
            )
            
            return {
                "upload_url": url,
                "bucket": self.bucket_name,
                "key": key,
                "expires_in": settings.S3_UPLOAD_EXPIRATION
            }
        
        except Exception as e:
            logger.error(f"S3 presigned URL generation error: {e}")
            return self._mock_presigned_url(session_id, file_type)

    def _mock_presigned_url(self, session_id: str, file_type: str) -> Dict[str, Any]:
        """Mock presigned URL for development"""
        return {
            "upload_url": f"https://mock-s3-{settings.S3_BUCKET_NAME}.s3.amazonaws.com/{session_id}/{file_type}",
            "bucket": settings.S3_BUCKET_NAME,
            "key": f"applications/{session_id}/{file_type}/document.pdf",
            "expires_in": settings.S3_UPLOAD_EXPIRATION
        }


class SNSService:
    """
    AWS SNS Integration for Notifications
    Sends SMS and email notifications
    """
    def __init__(self):
        self.client = None
        if not settings.USE_MOCK_SNS and (settings.ENABLE_SMS_NOTIFICATIONS or settings.ENABLE_EMAIL_NOTIFICATIONS):
            try:
                self.client = boto3.client(
                    'sns',
                    region_name=settings.SNS_REGION,
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                )
                logger.info("SNS client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize SNS client: {e}")
                self.client = None

    async def send_sms(self, phone_number: str, message: str) -> bool:
        """Send SMS notification"""
        if not settings.ENABLE_SMS_NOTIFICATIONS:
            logger.info(f"SMS notifications disabled. Message not sent to {phone_number}")
            return False
        
        if settings.USE_MOCK_SNS or self.client is None:
            logger.info(f"Mock SNS SMS to {phone_number}: {message}")
            return True
        
        try:
            self.client.publish(
                TopicArn=settings.SNS_TOPIC_ARN_SMS,
                Message=message,
                PhoneNumber=phone_number
            )
            logger.info(f"SMS sent to {phone_number}")
            return True
        except Exception as e:
            logger.error(f"SNS SMS error: {e}")
            return False

    async def send_email(self, email: str, subject: str, message: str) -> bool:
        """Send email notification"""
        if not settings.ENABLE_EMAIL_NOTIFICATIONS:
            logger.info(f"Email notifications disabled. Message not sent to {email}")
            return False
        
        if settings.USE_MOCK_SNS or self.client is None:
            logger.info(f"Mock SNS Email to {email} - Subject: {subject}")
            return True
        
        try:
            self.client.publish(
                TopicArn=settings.SNS_TOPIC_ARN_EMAIL,
                Subject=subject,
                Message=message
            )
            logger.info(f"Email sent to {email}")
            return True
        except Exception as e:
            logger.error(f"SNS Email error: {e}")
            return False


class CloudWatchService:
    """
    AWS CloudWatch Integration for Logging and Monitoring
    """
    def __init__(self):
        self.client = None
        if not settings.ENABLE_CLOUDWATCH_LOGGING:
            return
        
        try:
            import watchtower
            self.client = watchtower.CloudWatchLogHandler(
                log_group=settings.CLOUDWATCH_LOG_GROUP,
                stream_name='loan-eligibility-api'
            )
            logger.info("CloudWatch logging initialized")
        except Exception as e:
            logger.error(f"Failed to initialize CloudWatch: {e}")
            self.client = None

    def log_event(self, message: str, level: str = "INFO"):
        """Log event to CloudWatch"""
        if self.client is None:
            return
        
        logger.log(getattr(logging, level), message)


# Initialize all services
bedrock_service = BedrockService()
textract_service = TextractService()
sagemaker_service = SageMakerService()
s3_service = S3Service()
sns_service = SNSService()
cloudwatch_service = CloudWatchService()
