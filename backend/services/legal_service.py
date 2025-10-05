from typing import Dict

class LegalService:
    """Service for legal compliance and safety features"""
    
    def __init__(self):
        self.disclaimer_text = self._get_indian_legal_disclaimer()
    
    def _get_indian_legal_disclaimer(self) -> str:
        """Get comprehensive legal disclaimer for Indian context"""
        return """
**IMPORTANT LEGAL DISCLAIMER**

This AI system provides general information about Indian law for educational purposes only. This information:

• Is NOT legal advice and should not be relied upon as such
• Does not create an attorney-client relationship
• May not reflect the most current legal developments
• Cannot substitute for consultation with qualified legal professionals
• May not apply to your specific circumstances

**For Legal Advice:** Always consult with a qualified advocate or legal professional registered with the Bar Council of India.

**Accuracy:** While we strive for accuracy, this system may contain errors or omissions. Verify all information with authoritative legal sources.

**Jurisdiction:** This system focuses on Indian law but laws vary by state and are subject to change.

By using this system, you acknowledge that you understand these limitations.
        """
    
    def get_disclaimer(self) -> str:
        """Get the standard legal disclaimer"""
        return self.disclaimer_text
    
    def validate_query(self, query: str) -> Dict[str, any]:
        """Validate user query for inappropriate content"""
        
        # Check for potentially harmful requests
        harmful_patterns = [
            "how to break the law",
            "illegal activities",
            "avoid prosecution",
            "hide evidence",
            "commit fraud",
            "evade taxes illegally"
        ]
        
        query_lower = query.lower()
        
        for pattern in harmful_patterns:
            if pattern in query_lower:
                return {
                    "is_valid": False,
                    "reason": "Query appears to request assistance with potentially illegal activities",
                    "suggestion": "Please ask about legal compliance or legitimate legal information instead."
                }
        
        # Check for overly personal legal advice requests
        personal_advice_patterns = [
            "what should I do",
            "my case",
            "my situation", 
            "should I sue",
            "will I win",
            "what are my chances"
        ]
        
        for pattern in personal_advice_patterns:
            if pattern in query_lower:
                return {
                    "is_valid": True,
                    "warning": "This appears to be a request for personal legal advice. Remember that this system provides general information only. Consult a qualified legal professional for advice on your specific situation."
                }
        
        return {"is_valid": True}
    
    def add_safety_guardrails(self, response: str) -> str:
        """Add safety guardrails to AI responses"""
        
        # Check if response contains potential legal advice language
        advice_indicators = [
            "you should",
            "you must", 
            "i recommend",
            "you need to",
            "file a case",
            "take legal action"
        ]
        
        response_lower = response.lower()
        contains_advice = any(indicator in response_lower for indicator in advice_indicators)
        
        if contains_advice and "disclaimer" not in response_lower:
            response += "\n\n⚠️ **Important:** The above is general legal information, not advice for your specific situation. Please consult with a qualified legal professional before taking any legal action."
        
        return response
    
    def get_compliance_info(self) -> Dict[str, str]:
        """Get compliance information for the system"""
        return {
            "data_retention": "Conversations are not permanently stored. Session data is cleared after inactivity.",
            "privacy_policy": "We do not collect personal information. Queries are processed for AI response generation only.",
            "terms_of_service": "By using this system, you agree to the legal disclaimer and understand the limitations of AI-generated legal information.",
            "jurisdiction": "This system covers Indian law. Laws in other jurisdictions may differ significantly.",
            "accuracy_statement": "While we strive for accuracy, this system may contain errors. Always verify information with official legal sources."
        }