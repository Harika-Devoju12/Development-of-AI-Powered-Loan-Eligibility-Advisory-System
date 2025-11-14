from typing import Dict, Any, Optional
from database import get_supabase

class ChatService:
    """
    Service to handle chat conversation flow.
    TODO: Replace with Amazon Bedrock for conversational AI
    """

    def __init__(self):
        self.conversation_state = {}

    async def process_message(self, session_id: str, user_message: str) -> Dict[str, Any]:
        """
        Process user message and generate appropriate response.

        Conversation flow:
        1. Ask for name
        2. Ask for monthly income
        3. Ask for loan amount
        4. Ask for employment type
        5. Ask for credit score
        6. Complete → redirect to document upload
        """
        supabase = get_supabase()

        result = supabase.table("loan_applications").select("*").eq("session_id", session_id).maybe_single().execute()

        if not result.data:
            return {"response": "Session not found. Please start a new session.", "next_step": None}

        application = result.data

        supabase.table("chat_history").insert({
            "session_id": session_id,
            "role": "user",
            "message": user_message
        }).execute()

        response_text = ""
        next_step = None

        if not application.get("name"):
            supabase.table("loan_applications").update({"name": user_message}).eq("session_id", session_id).execute()
            response_text = f"Nice to meet you, {user_message}! What is your monthly income?"
        elif application.get("income_claimed") is None:
            try:
                income = float(user_message.replace(",", "").replace("₹", "").replace("$", "").strip())
                supabase.table("loan_applications").update({"income_claimed": income}).eq("session_id", session_id).execute()
                response_text = "Great! How much loan amount are you looking for?"
            except ValueError:
                response_text = "Please enter a valid income amount (e.g., 50000)"
        elif application.get("loan_amount") is None:
            try:
                loan_amount = float(user_message.replace(",", "").replace("₹", "").replace("$", "").strip())
                supabase.table("loan_applications").update({"loan_amount": loan_amount}).eq("session_id", session_id).execute()
                response_text = "What is your employment type? (e.g., Salaried, Self-Employed, Business)"
            except ValueError:
                response_text = "Please enter a valid loan amount (e.g., 500000)"
        elif not application.get("employment_type"):
            supabase.table("loan_applications").update({"employment_type": user_message}).eq("session_id", session_id).execute()
            response_text = "What is your credit score? (If you don't know, you can estimate between 300-900)"
        elif application.get("credit_score") is None:
            try:
                credit_score = int(user_message.strip())
                if 300 <= credit_score <= 900:
                    supabase.table("loan_applications").update({"credit_score": credit_score}).eq("session_id", session_id).execute()
                    response_text = "Thank you! I have collected all the information. Next, please upload your Aadhaar and bank statement for verification."
                    next_step = "upload_documents"
                else:
                    response_text = "Credit score should be between 300 and 900. Please enter a valid score."
            except ValueError:
                response_text = "Please enter a valid credit score (e.g., 750)"
        else:
            response_text = "Your information is complete. Please proceed to document upload."
            next_step = "upload_documents"

        supabase.table("chat_history").insert({
            "session_id": session_id,
            "role": "assistant",
            "message": response_text
        }).execute()

        return {"response": response_text, "next_step": next_step}

chat_service = ChatService()
