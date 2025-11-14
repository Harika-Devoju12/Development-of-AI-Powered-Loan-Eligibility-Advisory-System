import random
from typing import Dict, Any, List

class LoanMLService:
    """
    ML Service for loan eligibility prediction.
    TODO: Replace with actual SageMaker endpoint or trained model (loan_model.pkl)
    """

    def __init__(self):
        pass

    def predict_eligibility(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict loan eligibility based on applicant features.

        Args:
            features: Dictionary containing:
                - credit_score: int
                - income_extracted: float
                - loan_amount: float
                - emi_detected: float
                - employment_type: str

        Returns:
            Dictionary with eligibility_score, eligible flag, and SHAP explanation
        """
        credit_score = features.get("credit_score", 0)
        income = features.get("income_extracted", 0)
        loan_amount = features.get("loan_amount", 0)
        emi = features.get("emi_detected", 0)
        employment_type = features.get("employment_type", "")

        eligibility_score = 0.0
        factors = []

        if credit_score >= 750:
            eligibility_score += 0.35
            factors.append({"feature": "Credit Score", "impact": 0.35, "value": credit_score, "direction": "positive"})
        elif credit_score >= 700:
            eligibility_score += 0.25
            factors.append({"feature": "Credit Score", "impact": 0.25, "value": credit_score, "direction": "positive"})
        elif credit_score >= 650:
            eligibility_score += 0.15
            factors.append({"feature": "Credit Score", "impact": 0.15, "value": credit_score, "direction": "neutral"})
        else:
            eligibility_score += 0.05
            factors.append({"feature": "Credit Score", "impact": -0.25, "value": credit_score, "direction": "negative"})

        if income > 0 and loan_amount > 0:
            debt_to_income = loan_amount / (income * 12)
            if debt_to_income < 3:
                eligibility_score += 0.25
                factors.append({"feature": "Debt-to-Income Ratio", "impact": 0.25, "value": round(debt_to_income, 2), "direction": "positive"})
            elif debt_to_income < 4:
                eligibility_score += 0.15
                factors.append({"feature": "Debt-to-Income Ratio", "impact": 0.15, "value": round(debt_to_income, 2), "direction": "neutral"})
            else:
                factors.append({"feature": "Debt-to-Income Ratio", "impact": -0.15, "value": round(debt_to_income, 2), "direction": "negative"})

        if income > 0 and emi > 0:
            emi_ratio = emi / income
            if emi_ratio < 0.3:
                eligibility_score += 0.20
                factors.append({"feature": "EMI-to-Income Ratio", "impact": 0.20, "value": round(emi_ratio, 2), "direction": "positive"})
            elif emi_ratio < 0.4:
                eligibility_score += 0.10
                factors.append({"feature": "EMI-to-Income Ratio", "impact": 0.10, "value": round(emi_ratio, 2), "direction": "neutral"})
            else:
                factors.append({"feature": "EMI-to-Income Ratio", "impact": -0.20, "value": round(emi_ratio, 2), "direction": "negative"})

        if employment_type.lower() in ["salaried", "permanent"]:
            eligibility_score += 0.15
            factors.append({"feature": "Employment Type", "impact": 0.15, "value": employment_type, "direction": "positive"})
        elif employment_type.lower() in ["self-employed", "business"]:
            eligibility_score += 0.10
            factors.append({"feature": "Employment Type", "impact": 0.10, "value": employment_type, "direction": "neutral"})
        else:
            eligibility_score += 0.05
            factors.append({"feature": "Employment Type", "impact": 0.05, "value": employment_type, "direction": "neutral"})

        if income >= 50000:
            eligibility_score += 0.10
            factors.append({"feature": "Monthly Income", "impact": 0.10, "value": income, "direction": "positive"})
        elif income >= 30000:
            eligibility_score += 0.05
            factors.append({"feature": "Monthly Income", "impact": 0.05, "value": income, "direction": "neutral"})

        eligibility_score = min(eligibility_score, 1.0)

        eligible = eligibility_score >= 0.65 and credit_score >= 650

        return {
            "eligibility_score": round(eligibility_score, 2),
            "eligible": eligible,
            "shap_explanation": factors
        }


ml_service = LoanMLService()
