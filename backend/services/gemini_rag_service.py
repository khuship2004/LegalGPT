import os
import json
import re
from typing import List, Dict, Any
import asyncio
import google.generativeai as genai
from datetime import datetime

class GeminiRAGService:
    """Enhanced RAG service using Google Gemini API for intelligent responses"""
    
    def __init__(self):
        print("🚀 Initializing Gemini-powered Legal AI...")
        
        # Initialize Gemini API
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            # Use the latest working model
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            print("✅ Gemini API configured successfully!")
        else:
            print("⚠️  GEMINI_API_KEY not found, will use fallback mode")
            self.model = None
        
        # Legal knowledge base for context
        self.legal_context = self._build_legal_context()
        print(f"📚 Loaded legal context with {len(self.legal_context)} areas")
    
    def _build_legal_context(self) -> str:
        """Build comprehensive legal context for better responses"""
        return """
# INDIAN LEGAL SYSTEM CONTEXT

## Constitutional Law
- Constitution of India (1950) - Supreme law of India
- Fundamental Rights (Articles 12-35): Right to Equality, Right to Freedom, Right against Exploitation, Right to Freedom of Religion, Cultural and Educational Rights, Right to Constitutional Remedies
- Directive Principles of State Policy (Articles 36-51)
- Fundamental Duties (Article 51A)

## Criminal Law
- Indian Penal Code (IPC) 1860 - Main criminal law statute
- Code of Criminal Procedure (CrPC) 1973 - Criminal procedure
- Indian Evidence Act 1872 - Rules of evidence
- Major offenses: Murder (S.302), Rape (S.375), Theft (S.378), Assault (S.351)

## Civil Law
- Indian Contract Act 1872 - Contract law
- Transfer of Property Act 1882 - Property transactions  
- Indian Partnership Act 1932 - Business partnerships
- Specific Relief Act 1963 - Civil remedies

## Special Laws
- Consumer Protection Act 2019 - Consumer rights
- Companies Act 2013 - Corporate law
- Motor Vehicles Act 1988 - Traffic regulations
- Right to Information Act 2005 - Transparency in governance

## Court System
- Supreme Court of India - Apex court
- High Courts - State level courts
- District Courts - Local jurisdiction
- Specialized tribunals

## Legal Procedures
- Public Interest Litigation (PIL) - Court cases for public good
- First Information Report (FIR) - Initial police complaint
- Writ Petitions - Constitutional remedies
- Appeals and revisions

## Recent Developments
- Digital India Act initiatives
- Data Protection laws
- Environmental regulations
- Women safety laws
"""

    async def generate_response(self, query: str, conversation_history: List = None, include_sources: bool = True) -> Dict[str, Any]:
        """Generate intelligent response using Gemini AI"""
        
        try:
            if self.model:
                # Use Gemini API for intelligent responses
                response = await self._generate_gemini_response(query)
                sources = self._extract_relevant_sources(query, response)
            else:
                # Fallback to enhanced local responses
                response = self._generate_enhanced_fallback(query)
                sources = self._extract_relevant_sources(query, response)
            
            return {
                "answer": response,
                "sources": sources if include_sources else [],
                "context_used": True,
                "ai_powered": self.model is not None
            }
            
        except Exception as e:
            print(f"❌ Error in response generation: {str(e)}")
            return {
                "answer": self._generate_error_response(query, str(e)),
                "sources": [],
                "context_used": False,
                "ai_powered": False
            }
    
    async def _generate_gemini_response(self, query: str) -> str:
        """Generate response using Gemini AI with source integration"""
        
        # Get relevant sources first
        relevant_sources = self._extract_relevant_sources(query)
        source_context = ""
        
        if relevant_sources:
            source_context = "\n\nRELEVANT LEGAL SOURCES:\n"
            for source in relevant_sources:
                source_context += f"- {source['title']}: {source['content']} ({source['source']})\n"
        
        prompt = f"""
You are an expert AI assistant specializing in Indian law. Provide accurate, helpful information about Indian legal matters.

LEGAL CONTEXT: {self.legal_context}
{source_context}

USER QUESTION: {query}

INSTRUCTIONS:
1. Provide clear, accurate information about Indian law
2. Include specific legal provisions, sections, or articles when relevant
3. Cite appropriate laws, acts, or constitutional provisions mentioned in the sources
4. Explain legal procedures step-by-step when asked
5. Include recent legal developments if relevant
6. Reference the specific acts and sections from the provided sources when applicable
7. Always add appropriate legal disclaimers
8. If you don't have specific information, suggest where to find authoritative sources

FORMAT YOUR RESPONSE AS:
- **Direct Answer**: Clear response to the question
- **Legal Provisions**: Specific acts, sections, and articles
- **Practical Guidance**: Step-by-step procedures if applicable
- **Key Points**: Important highlights
- **Legal Disclaimer**: Educational purposes notice

REMEMBER: Reference the specific legal sources provided above when relevant to the query.
"""

        try:
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            answer = response.text
            
            # Add legal disclaimer if not present
            if "disclaimer" not in answer.lower():
                answer += "\n\n**⚖️ Legal Disclaimer:** This information is for educational purposes only and does not constitute legal advice. Please consult with a qualified legal professional for specific legal matters."
            
            return answer
            
        except Exception as e:
            print(f"🔄 Gemini API error: {str(e)}, falling back to local response")
            return self._generate_enhanced_fallback(query)
    
    def _generate_enhanced_fallback(self, query: str) -> str:
        """Enhanced fallback responses for specific legal topics"""
        
        query_lower = query.lower()
        
        # PIL (Public Interest Litigation) - specific response for your query
        if "pil" in query_lower or "public interest litigation" in query_lower:
            return """**Public Interest Litigation (PIL)**

**Definition:**
PIL is a legal mechanism that allows any citizen to approach the court for the protection of public interest, even if they are not directly affected by the issue.

**Key Features:**
• **Locus Standi:** Any concerned citizen can file PIL, not just affected parties
• **Public Welfare:** Cases must involve matters of public importance
• **Constitutional Remedy:** Based on Article 32 (Supreme Court) and Article 226 (High Court)

**Who Can File PIL:**
• Any citizen of India
• Social organizations and NGOs
• Legal professionals (as amicus curiae)
• The court can also take suo motu (on its own) cognizance

**Types of Issues Covered:**
• Environmental protection
• Human rights violations
• Corruption in public offices
• Poor implementation of government schemes
• Violation of consumer rights
• Women and child safety issues

**Procedure to File PIL:**
1. **Draft the Petition:** Clearly state the public issue and legal violations
2. **Gather Evidence:** Collect supporting documents and evidence
3. **File in Appropriate Court:** Supreme Court (Article 32) or High Court (Article 226)
4. **Pay Court Fees:** Minimal fees for genuine PIL cases
5. **Serve Notice:** Court issues notice to respondents
6. **Hearing Process:** Court examines the case and may appoint committees

**Important PIL Landmarks:**
• **Vishaka Guidelines** - Workplace sexual harassment (1997)
• **M.C. Mehta cases** - Environmental protection
• **Olga Tellis case** - Right to livelihood
• **Bandhua Mukti Morcha** - Bonded labor cases

**Legal Provisions:**
• **Article 32:** Right to Constitutional Remedies (Supreme Court)
• **Article 226:** High Court's writ jurisdiction
• **Supreme Court Rules, 2013:** Procedure for filing

**Recent Developments:**
• Courts have become stricter about frivolous PILs
• Emphasis on genuine public interest issues
• Monetary penalties for misuse of PIL provisions

**⚠️ Important Notes:**
• PIL should not be for personal gain or publicity
• Courts may impose costs for frivolous petitions
• Proper research and documentation essential
• Consider approaching appropriate authorities first

**⚖️ Legal Disclaimer:** This information is for educational purposes only. For filing PIL or specific legal matters, consult with qualified legal professionals."""

        # Fundamental Rights
        elif any(term in query_lower for term in ["fundamental rights", "constitutional rights", "basic rights"]):
            return """**Fundamental Rights under Indian Constitution**

**Six Categories of Fundamental Rights (Articles 12-35):**

**1. Right to Equality (Articles 14-18):**
• Article 14: Equality before law
• Article 15: Prohibition of discrimination
• Article 16: Equality of opportunity in public employment
• Article 17: Abolition of untouchability
• Article 18: Abolition of titles

**2. Right to Freedom (Articles 19-22):**
• Article 19: Six freedoms including speech, assembly, movement
• Article 20: Protection against ex-post facto laws
• Article 21: Right to life and personal liberty
• Article 21A: Right to education (added in 2002)
• Article 22: Protection against arbitrary arrest

**3. Right against Exploitation (Articles 23-24):**
• Article 23: Prohibition of trafficking and forced labor
• Article 24: Prohibition of child labor

**4. Right to Freedom of Religion (Articles 25-28):**
• Article 25: Freedom of conscience and religion
• Article 26: Freedom to manage religious affairs
• Article 27: Freedom from paying taxes for promotion of religion
• Article 28: Freedom from religious instruction in state institutions

**5. Cultural and Educational Rights (Articles 29-30):**
• Article 29: Protection of language, script and culture of minorities
• Article 30: Right of minorities to establish educational institutions

**6. Right to Constitutional Remedies (Article 32):**
• Called "Heart and Soul" of Constitution by Dr. B.R. Ambedkar
• Right to approach Supreme Court directly for enforcement of fundamental rights
• Writs: Habeas Corpus, Mandamus, Prohibition, Certiorari, Quo-warranto"""

        # Criminal procedure
        elif any(term in query_lower for term in ["fir", "first information report", "police complaint"]):
            return """**FIR (First Information Report) - Complete Guide**

**What is FIR?**
FIR is the written document prepared by police when they receive information about a cognizable offense.

**Legal Basis:**
• **Section 154, CrPC 1973:** Mandatory registration of FIR for cognizable offenses
• **Section 166A, IPC:** Penalty for police officer who refuses to register FIR

**Step-by-Step Procedure:**
1. **Go to Police Station:** Visit the station having jurisdiction over the crime location
2. **Provide Information:** Give complete details of the incident
3. **Written Recording:** Police must reduce oral complaint to writing
4. **Reading Back:** The FIR must be read back to you for verification
5. **Sign the FIR:** Put your signature after confirming accuracy
6. **Get Free Copy:** You're entitled to a free copy immediately
7. **Note FIR Number:** Keep the FIR number for future reference

**What to Include:**
• Date, time, and place of occurrence
• Detailed description of the incident
• Names and addresses if known
• Description of accused persons
• Loss or damage details
• Names of witnesses

**Your Rights:**
• Police cannot refuse to register FIR for cognizable offenses
• FIR copy must be provided free of cost
• You can lodge FIR from any police station (if jurisdictional issues)
• Online FIR facility available in many states

**What if Police Refuse:**
1. **Meet Senior Officer:** Approach SP/DCP/Commissioner
2. **Written Complaint:** Submit written application to senior officers
3. **Magistrate Approach:** File complaint before local magistrate
4. **Legal Action:** Police refusal is punishable offense under Section 166A IPC"""

        # Contract law
        elif any(term in query_lower for term in ["contract", "agreement", "breach"]):
            return """**Indian Contract Law - Key Provisions**

**Definition (Section 2(h), Indian Contract Act 1872):**
"An agreement enforceable by law is a contract"

**Essential Elements (Section 10):**
1. **Offer and Acceptance:** Clear proposal and unqualified acceptance
2. **Free Consent:** Agreement without coercion, undue influence, fraud, misrepresentation, or mistake
3. **Competent Parties:** Major, sound mind, not disqualified by law
4. **Lawful Consideration:** Something of value exchanged legally
5. **Lawful Object:** Purpose must not be illegal or immoral
6. **Not Expressly Void:** Not declared void by law

**Types of Contracts:**
• **Valid Contract:** Enforceable by law
• **Void Contract:** Not enforceable from beginning
• **Voidable Contract:** Can be avoided by one party
• **Unenforceable Contract:** Valid but cannot be enforced in court

**Breach of Contract:**
• **Actual Breach:** Failure to perform when due
• **Anticipatory Breach:** Declaration of intention not to perform

**Remedies for Breach:**
1. **Damages:** Monetary compensation
2. **Specific Performance:** Court orders actual performance
3. **Injunction:** Court restrains breach
4. **Rescission:** Contract cancelled
5. **Quantum Meruit:** Payment for work done"""

        # General fallback
        else:
            return f"""**Legal Information Request: {query}**

I understand you're seeking information about "{query}". While I don't have specific details about this exact topic in my current database, I can provide some general guidance:

**For Indian Legal Information, Consider These Resources:**

**Primary Sources:**
• **Constitution of India** - Fundamental law and rights
• **Indian Penal Code (IPC)** - Criminal law provisions  
• **Code of Civil Procedure (CPC)** - Civil court procedures
• **Indian Evidence Act** - Rules for legal evidence

**Government Resources:**
• **India Code Portal** (www.indiacode.nic.in) - All central acts
• **Supreme Court of India** (sci.gov.in) - Apex court judgments
• **Law Ministry Website** - Latest legal developments
• **State Government Legal Departments** - State-specific laws

**Professional Help:**
• **Consult Legal Professionals:** Advocates, solicitors, legal consultants
• **Legal Aid Services:** Free legal aid for eligible persons
• **Bar Council of India** - Find registered lawyers
• **District Legal Services Authority** - Local legal support

**Suggested Actions:**
1. Research the specific law or act related to your query
2. Check recent Supreme Court/High Court judgments
3. Consult with qualified legal professionals
4. Verify information from official government sources

**⚖️ Important:** This is general information only. For specific legal matters, always consult qualified legal professionals."""

    def _extract_relevant_sources(self, query: str, response: str = None) -> List[Dict]:
        """Extract relevant legal sources based on query and AI response with intelligent matching"""
        
        query_lower = query.lower()
        response_lower = (response or "").lower() if response else ""
        combined_text = f"{query_lower} {response_lower}"
        sources = []
        
        # Surrogacy law
        if any(term in combined_text for term in ["surrogacy", "surrogate"]):
            sources.extend([
                {
                    "title": "Surrogacy (Regulation) Act, 2021",
                    "content": "Comprehensive law regulating surrogacy arrangements in India",
                    "source": "Surrogacy (Regulation) Act, 2021",
                    "section": "Sections 1-58",
                    "url": "https://www.indiacode.nic.in/handle/123456789/16471"
                },
                {
                    "title": "Assisted Reproductive Technology (Regulation) Act, 2021",
                    "content": "Regulation of assisted reproductive technology clinics and banks",
                    "source": "ART (Regulation) Act, 2021",
                    "section": "Various Sections",
                    "url": "https://www.indiacode.nic.in/handle/123456789/16470"
                }
            ])
        
        # Constitutional matters
        elif any(term in combined_text for term in ["constitution", "fundamental", "article", "pil", "rights"]):
            sources.append({
                "title": "Constitution of India",
                "content": "Supreme law of India containing fundamental rights, directive principles, and government structure",
                "source": "Constitution of India, 1950",
                "section": "Relevant Articles",
                "url": "https://www.india.gov.in/my-government/constitution-india/constitution-india-full-text"
            })
        
        # Criminal law matters
        elif any(term in combined_text for term in ["criminal", "ipc", "murder", "theft", "fir", "police", "crime"]):
            sources.extend([
                {
                    "title": "Indian Penal Code",
                    "content": "Primary criminal law statute defining offenses and punishments",
                    "source": "Indian Penal Code, 1860",
                    "section": "Relevant Sections",
                    "url": "https://www.indiacode.nic.in/handle/123456789/2263"
                },
                {
                    "title": "Code of Criminal Procedure",
                    "content": "Procedural law for criminal cases in India",
                    "source": "CrPC, 1973",
                    "section": "Relevant Sections",
                    "url": "https://www.indiacode.nic.in/handle/123456789/2264"
                }
            ])
        
        # Family law
        elif any(term in combined_text for term in ["marriage", "divorce", "custody", "maintenance", "family"]):
            sources.extend([
                {
                    "title": "Hindu Marriage Act",
                    "content": "Law governing Hindu marriages and divorce",
                    "source": "Hindu Marriage Act, 1955",
                    "section": "Relevant Sections",
                    "url": "https://www.indiacode.nic.in/handle/123456789/2277"
                },
                {
                    "title": "Indian Christian Marriage Act",
                    "content": "Law governing Christian marriages in India",
                    "source": "Indian Christian Marriage Act, 1872",
                    "section": "Relevant Sections",
                    "url": "https://www.indiacode.nic.in/handle/123456789/2272"
                }
            ])
        
        # Property law
        elif any(term in combined_text for term in ["property", "land", "real estate", "ownership"]):
            sources.extend([
                {
                    "title": "Transfer of Property Act",
                    "content": "Law governing transfer of property in India",
                    "source": "Transfer of Property Act, 1882",
                    "section": "Relevant Sections",
                    "url": "https://www.indiacode.nic.in/handle/123456789/2281"
                },
                {
                    "title": "Registration Act",
                    "content": "Law governing registration of documents",
                    "source": "Registration Act, 1908",
                    "section": "Relevant Sections",
                    "url": "https://www.indiacode.nic.in/handle/123456789/2279"
                }
            ])
        
        # Contract law
        elif any(term in combined_text for term in ["contract", "agreement", "breach"]):
            sources.append({
                "title": "Indian Contract Act",
                "content": "Law governing contracts and agreements in India",
                "source": "Indian Contract Act, 1872", 
                "section": "Relevant Sections",
                "url": "https://www.indiacode.nic.in/handle/123456789/2268"
            })
        
        # Consumer law
        elif any(term in combined_text for term in ["consumer", "protection", "goods", "services"]):
            sources.append({
                "title": "Consumer Protection Act",
                "content": "Law protecting consumer rights and providing redressal mechanisms",
                "source": "Consumer Protection Act, 2019",
                "section": "Relevant Sections", 
                "url": "https://www.indiacode.nic.in/handle/123456789/15397"
            })
        
        # Labor law
        elif any(term in query_lower for term in ["labor", "labour", "employment", "worker", "employee"]):
            sources.extend([
                {
                    "title": "Industrial Disputes Act",
                    "content": "Law governing industrial relations and labor disputes",
                    "source": "Industrial Disputes Act, 1947",
                    "section": "Relevant Sections",
                    "url": "https://www.indiacode.nic.in/handle/123456789/2285"
                },
                {
                    "title": "Employees' Provident Funds Act",
                    "content": "Law governing provident fund for employees",
                    "source": "EPF Act, 1952",
                    "section": "Relevant Sections",
                    "url": "https://www.indiacode.nic.in/handle/123456789/2287"
                }
            ])
        
        # Cyber law
        elif any(term in query_lower for term in ["cyber", "internet", "digital", "online", "data protection"]):
            sources.extend([
                {
                    "title": "Information Technology Act",
                    "content": "Law governing cyber crimes and digital transactions",
                    "source": "IT Act, 2000",
                    "section": "Relevant Sections",
                    "url": "https://www.indiacode.nic.in/handle/123456789/2289"
                },
                {
                    "title": "Digital Personal Data Protection Act",
                    "content": "Law governing data protection and privacy",
                    "source": "DPDP Act, 2023",
                    "section": "Relevant Sections",
                    "url": "https://www.indiacode.nic.in/handle/123456789/16573"
                }
            ])
        
        # Default fallback - add general legal resources
        if not sources:
            sources.extend([
                {
                    "title": "India Code Portal",
                    "content": "Official repository of all Central Acts and Rules",
                    "source": "Government of India",
                    "section": "All Acts",
                    "url": "https://www.indiacode.nic.in/"
                },
                {
                    "title": "Supreme Court of India",
                    "content": "Apex court judgments and legal precedents",
                    "source": "Supreme Court of India",
                    "section": "Court Judgments",
                    "url": "https://main.sci.gov.in/"
                }
            ])
        
        return sources
    
    def _generate_error_response(self, query: str, error: str) -> str:
        """Generate response when there's an error"""
        
        return f"""I apologize, but I encountered an error while processing your question about "{query}".

**Error Details:** {error}

**What You Can Do:**
1. **Try Rephrasing:** Ask the question in a different way
2. **Check Internet Connection:** Some features require online access
3. **Consult Official Sources:** Visit government legal portals
4. **Contact Legal Professionals:** For specific legal advice

**Alternative Resources:**
• India Code Portal: www.indiacode.nic.in
• Supreme Court of India: sci.gov.in  
• Legal Services Authority: nalsa.gov.in

**⚖️ Legal Disclaimer:** For specific legal matters, please consult with qualified legal professionals."""

    async def health_check(self) -> bool:
        """Check if the service is healthy"""
        try:
            if self.model:
                # Test Gemini API
                test_response = await asyncio.to_thread(
                    self.model.generate_content, 
                    "What is law? (Reply in one sentence)"
                )
                return bool(test_response.text)
            return True
        except Exception as e:
            print(f"Health check failed: {str(e)}")
            return False
    
    async def get_document_list(self) -> List[Dict]:
        """Get list of available legal areas"""
        return [
            {"title": "Constitutional Law", "source": "Constitution of India", "section": "Articles 1-395", "category": "Constitutional Law"},
            {"title": "Criminal Law", "source": "Indian Penal Code", "section": "Sections 1-511", "category": "Criminal Law"},
            {"title": "Contract Law", "source": "Indian Contract Act", "section": "Sections 1-238", "category": "Contract Law"},
            {"title": "Consumer Law", "source": "Consumer Protection Act", "section": "Various Sections", "category": "Consumer Law"},
            {"title": "Corporate Law", "source": "Companies Act", "section": "Various Sections", "category": "Corporate Law"},
            {"title": "Evidence Law", "source": "Indian Evidence Act", "section": "Sections 1-167", "category": "Evidence Law"}
        ]