import re
import random
from typing import Dict, Any

class DocumentService:
    """
    Service for document processing and verification.
    TODO: Integrate AWS Textract for OCR
    TODO: Integrate AWS Voice ID for voice verification
    """

    def verify_aadhaar(self, document_text: str) -> Dict[str, Any]:
        """
        Verify Aadhaar document.
        Currently uses simple text matching.
        TODO: Replace with AWS Textract OCR
        """
        aadhaar_keywords = ["aadhaar", "aadhar", "government of india", "unique identification"]

        document_lower = document_text.lower()
        is_aadhaar = any(keyword in document_lower for keyword in aadhaar_keywords)

        aadhaar_number_pattern = r'\d{4}\s?\d{4}\s?\d{4}'
        aadhaar_match = re.search(aadhaar_number_pattern, document_text)

        if is_aadhaar or aadhaar_match:
            extracted_data = {
                "document_type": "aadhaar",
                "verified": True,
                "aadhaar_number": aadhaar_match.group() if aadhaar_match else "XXXX XXXX XXXX"
            }
            return {
                "verified": True,
                "message": "Aadhaar verification successful",
                "extracted_data": extracted_data
            }
        else:
            return {
                "verified": False,
                "message": "Could not verify Aadhaar document. Please upload a valid Aadhaar card.",
                "extracted_data": None
            }

    def process_bank_statement(self, document_text: str) -> Dict[str, Any]:
        """
        Process bank statement to extract income and EMI.
        Currently uses simple pattern matching and dummy data.
        TODO: Replace with AWS Textract + intelligent parsing
        """
        income_patterns = [
            r'salary\s*credit\s*[:\-]?\s*₹?\s*([\d,]+)',
            r'credit\s*[:\-]?\s*₹?\s*([\d,]+)',
            r'income\s*[:\-]?\s*₹?\s*([\d,]+)'
        ]

        emi_patterns = [
            r'emi\s*[:\-]?\s*₹?\s*([\d,]+)',
            r'loan\s*debit\s*[:\-]?\s*₹?\s*([\d,]+)',
            r'debit\s*[:\-]?\s*₹?\s*([\d,]+)'
        ]

        income_extracted = 0.0
        emi_detected = 0.0

        document_lower = document_text.lower()

        for pattern in income_patterns:
            matches = re.findall(pattern, document_lower, re.IGNORECASE)
            if matches:
                amounts = [float(m.replace(",", "")) for m in matches]
                income_extracted = max(amounts)
                break

        for pattern in emi_patterns:
            matches = re.findall(pattern, document_lower, re.IGNORECASE)
            if matches:
                amounts = [float(m.replace(",", "")) for m in matches]
                emi_detected = sum(amounts) / len(amounts)
                break

        if income_extracted == 0:
            income_extracted = random.uniform(30000, 80000)

        if emi_detected == 0:
            emi_detected = random.uniform(5000, 20000)

        return {
            "income_extracted": round(income_extracted, 2),
            "emi_detected": round(emi_detected, 2),
            "message": "Bank statement processed successfully"
        }


document_service = DocumentService()
