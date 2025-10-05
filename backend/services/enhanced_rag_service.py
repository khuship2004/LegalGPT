import asyncio
import requests
import json
from typing import List, Dict, Any
import re
from datetime import datetime
from .legal_data_service import LegalDataService

class EnhancedRAGService:
    """Enhanced RAG service with external data sources and database storage"""
    
    def __init__(self):
        self.data_service = LegalDataService()
        self.documents = []
        self.legal_terms = {
            'constitutional': ['constitution', 'fundamental rights', 'directive principles', 'amendment', 'article'],
            'criminal': ['ipc', 'penal code', 'crime', 'offense', 'punishment', 'section', 'murder', 'theft'],
            'civil': ['contract', 'tort', 'property', 'civil procedure', 'damages', 'breach'],
            'corporate': ['company', 'director', 'shareholder', 'corporate governance', 'compliance'],
            'consumer': ['consumer protection', 'consumer rights', 'unfair trade', 'defective goods'],
            'family': ['marriage', 'divorce', 'custody', 'maintenance', 'succession'],
            'labour': ['employment', 'worker', 'industrial dispute', 'minimum wages', 'provident fund'],
            'tax': ['income tax', 'gst', 'tax evasion', 'assessment', 'penalty']
        }
        
        # Mark as not initialized yet
        self.is_initialized = False
    
    async def initialize(self):
        """Public method to initialize the service asynchronously"""
        if not self.is_initialized:
            await self._initialize_data()
            self.is_initialized = True
    
    async def _initialize_data(self):
        """Initialize data from both local and external sources"""
        # First, try to sync from external sources
        try:
            synced_count = await self.data_service.sync_all_sources()
            
            # Load from database
            db_documents = self.data_service.load_documents_from_db()
            
            if db_documents:
                self.documents = db_documents
                print(f"Loaded {len(self.documents)} documents from database")
            else:
                # Fallback to enhanced local data if no external sources available
                self._initialize_enhanced_local_data()
                
        except Exception as e:
            print(f"Error syncing external data: {e}")
            self._initialize_enhanced_local_data()
    
    def _initialize_enhanced_local_data(self):
        """Enhanced local legal database with more comprehensive coverage"""
        
        enhanced_documents = [
            # Constitution of India - Expanded
            {
                "title": "Constitution of India - Article 14 (Right to Equality)",
                "content": "The State shall not deny to any person equality before the law or the equal protection of the laws within the territory of India. This article guarantees equality before law and equal protection of laws to all persons, citizens and non-citizens alike. It prohibits discrimination and ensures that all are equal in the eyes of law.",
                "source": "Constitution of India",
                "section": "Article 14",
                "category": "Constitutional Law",
                "keywords": ["equality", "discrimination", "fundamental rights", "article 14"],
                "url": "https://www.indiacode.nic.in/constitution-of-india"
            },
            {
                "title": "Constitution of India - Article 15 (Prohibition of Discrimination)",
                "content": "The State shall not discriminate against any citizen on grounds only of religion, race, caste, sex, place of birth or any of them. This article prohibits discrimination by the State on grounds of religion, race, caste, sex or place of birth.",
                "source": "Constitution of India",
                "section": "Article 15",
                "category": "Constitutional Law", 
                "keywords": ["discrimination", "religion", "caste", "sex", "fundamental rights"],
                "url": "https://www.indiacode.nic.in/constitution-of-india"
            },
            {
                "title": "Constitution of India - Article 19 (Freedom of Speech and Expression)",
                "content": "All citizens shall have the right to freedom of speech and expression, to assemble peaceably and without arms, to form associations or unions, to move freely throughout India, and to practice any profession or carry on any occupation, trade or business.",
                "source": "Constitution of India",
                "section": "Article 19",
                "category": "Constitutional Law",
                "keywords": ["freedom of speech", "expression", "assembly", "movement", "profession"],
                "url": "https://www.indiacode.nic.in/constitution-of-india"
            },
            {
                "title": "Constitution of India - Article 21 (Right to Life and Personal Liberty)",
                "content": "No person shall be deprived of his life or personal liberty except according to procedure established by law. This fundamental right has been interpreted broadly to include right to live with dignity, right to education, right to health, etc.",
                "source": "Constitution of India", 
                "section": "Article 21",
                "category": "Constitutional Law",
                "keywords": ["right to life", "personal liberty", "due process", "dignity"],
                "url": "https://www.indiacode.nic.in/constitution-of-india"
            },
            
            # Indian Penal Code - Expanded
            {
                "title": "IPC Section 302 - Murder",
                "content": "Whoever commits murder shall be punished with death, or imprisonment for life, and shall also be liable to fine. Murder is defined as the act of causing death with the intention of causing death or knowledge that the act is likely to cause death.",
                "source": "Indian Penal Code 1860",
                "section": "Section 302",
                "category": "Criminal Law",
                "keywords": ["murder", "death", "life imprisonment", "intention", "criminal"],
                "url": "https://www.indiacode.nic.in/indian-penal-code-1860"
            },
            {
                "title": "IPC Section 379 - Theft",
                "content": "Whoever intends to take dishonestly any moveable property out of the possession of any person without that person's consent, moves that property in order to such taking, is said to commit theft. Punishment is imprisonment up to three years, or fine, or both.",
                "source": "Indian Penal Code 1860",
                "section": "Section 379", 
                "category": "Criminal Law",
                "keywords": ["theft", "dishonestly", "moveable property", "possession", "stealing"],
                "url": "https://www.indiacode.nic.in/indian-penal-code-1860"
            },
            {
                "title": "IPC Section 498A - Cruelty to Wife",
                "content": "Whoever, being the husband or the relative of the husband of a woman, subjects such woman to cruelty shall be punished with imprisonment for a term which may extend to three years and shall also be liable to fine.",
                "source": "Indian Penal Code 1860",
                "section": "Section 498A",
                "category": "Criminal Law",
                "keywords": ["cruelty", "wife", "husband", "dowry", "domestic violence"],
                "url": "https://www.indiacode.nic.in/indian-penal-code-1860"
            },
            
            # Contract Act - Expanded  
            {
                "title": "Indian Contract Act Section 10 - What Agreements are Contracts",
                "content": "All agreements are contracts if they are made by the free consent of parties competent to contract, for a lawful consideration and with a lawful object, and are not hereby expressly declared to be void.",
                "source": "Indian Contract Act 1872",
                "section": "Section 10",
                "category": "Contract Law",
                "keywords": ["contract", "agreement", "free consent", "consideration", "lawful object"],
                "url": "https://www.indiacode.nic.in/indian-contract-act-1872"
            },
            {
                "title": "Indian Contract Act Section 73 - Compensation for Breach",
                "content": "When a contract has been broken, the party who suffers by such breach is entitled to receive compensation for any loss or damage caused to him thereby which naturally arose in the usual course of things from such breach.",
                "source": "Indian Contract Act 1872",
                "section": "Section 73",
                "category": "Contract Law", 
                "keywords": ["breach of contract", "compensation", "damages", "loss"],
                "url": "https://www.indiacode.nic.in/indian-contract-act-1872"
            },
            
            # Consumer Protection Act 2019
            {
                "title": "Consumer Protection Act 2019 - Definition of Consumer",
                "content": "Consumer means any person who buys any goods for a consideration which has been paid or promised or partly paid and partly promised, or under any system of deferred payment and includes any user of such goods other than the person who buys such goods for resale or for any commercial purpose.",
                "source": "Consumer Protection Act 2019",
                "section": "Section 2(7)",
                "category": "Consumer Law",
                "keywords": ["consumer", "goods", "consideration", "commercial purpose", "buyer"],
                "url": "https://www.indiacode.nic.in/consumer-protection-act-2019"
            },
            
            # Companies Act 2013
            {
                "title": "Companies Act 2013 - Director's Duties",
                "content": "A director of a company shall act in accordance with the articles of the company, shall act in good faith in order to promote the objects of the company for the benefit of its members as a whole, and in the best interests of the company, its employees, shareholders, community and for the protection of environment.",
                "source": "Companies Act 2013",
                "section": "Section 166",
                "category": "Corporate Law",
                "keywords": ["director", "duties", "good faith", "shareholders", "fiduciary"],
                "url": "https://www.indiacode.nic.in/companies-act-2013"
            },
            
            # Motor Vehicles Act 1988
            {
                "title": "Motor Vehicles Act 1988 - Compulsory Insurance",
                "content": "No person shall use, except as a passenger, or cause or allow any other person to use, a motor vehicle in a public place, unless there is in force in relation to the use of the vehicle by that person or that other person, as the case may be, a policy of insurance complying with the requirements of this Chapter.",
                "source": "Motor Vehicles Act 1988", 
                "section": "Section 146",
                "category": "Motor Vehicle Law",
                "keywords": ["motor vehicle", "insurance", "compulsory", "public place", "policy"],
                "url": "https://www.indiacode.nic.in/motor-vehicles-act-1988"
            },
            
            # Information Technology Act 2000
            {
                "title": "IT Act 2000 - Cyber Crimes and Penalties",
                "content": "Whoever knowingly or intentionally accesses or secures access to any computer system or computer network without permission shall be liable to pay damages by way of compensation to the person so affected and penalty up to Rs. 1 crore.",
                "source": "Information Technology Act 2000",
                "section": "Section 43",
                "category": "Cyber Law",
                "keywords": ["cyber crime", "unauthorized access", "computer", "hacking", "penalty"],
                "url": "https://www.indiacode.nic.in/information-technology-act-2000"
            },
            
            # Right to Information Act 2005
            {
                "title": "RTI Act 2005 - Right to Information",
                "content": "All citizens shall have the right to information under this Act. It shall be the duty of the State to maintain all its records duly catalogued and indexed in a manner and the form which facilitates the right to information under this Act.",
                "source": "Right to Information Act 2005",
                "section": "Section 3",
                "category": "Administrative Law",
                "keywords": ["right to information", "RTI", "transparency", "public records", "citizens"],
                "url": "https://www.indiacode.nic.in/right-to-information-act-2005"
            },
            
            # Goods and Services Tax Act
            {
                "title": "GST Act - Tax Liability",
                "content": "Every supplier shall be liable to pay tax under this Act on all taxable supplies of goods or services or both made by him. The liability to pay tax on goods or services or both shall arise at the time of supply.",
                "source": "Central Goods and Services Tax Act 2017",
                "section": "Section 9",
                "category": "Tax Law",
                "keywords": ["GST", "tax liability", "supplier", "taxable supply", "goods and services"],
                "url": "https://www.indiacode.nic.in/central-goods-and-services-tax-act-2017"
            },
            
            # Recent Landmark Judgments
            {
                "title": "Privacy as Fundamental Right - K.S. Puttaswamy Case",
                "content": "The Supreme Court in K.S. Puttaswamy v. Union of India (2017) held that privacy is a fundamental right under Article 21. The right to privacy is protected as an intrinsic part of the right to life and personal liberty under Article 21 and as a part of the freedoms guaranteed by Part III of the Constitution.",
                "source": "Supreme Court Judgment",
                "section": "K.S. Puttaswamy v. Union of India (2017)",
                "category": "Constitutional Law",
                "keywords": ["privacy", "fundamental right", "Article 21", "Supreme Court", "Puttaswamy"],
                "url": "https://sci.gov.in"
            }
        ]
        
        # Store enhanced local data in database
        self.data_service.store_documents(enhanced_documents)
        self.documents = enhanced_documents
        
        print(f"Initialized with {len(self.documents)} enhanced legal documents")
    
    def search_documents(self, query: str) -> List[Dict[str, Any]]:
        """Enhanced search with better scoring and relevance"""
        query_lower = query.lower()
        results = []
        
        for doc in self.documents:
            score = 0
            
            # Title matching (highest weight)
            if any(word in doc["title"].lower() for word in query_lower.split()):
                score += 10
            
            # Content matching
            content_matches = sum(1 for word in query_lower.split() if word in doc["content"].lower())
            score += content_matches * 2
            
            # Keyword matching (high weight)  
            keyword_matches = sum(1 for keyword in doc["keywords"] if keyword in query_lower)
            score += keyword_matches * 5
            
            # Section matching
            if any(word in doc["section"].lower() for word in query_lower.split()):
                score += 3
            
            # Legal term category matching
            for category, terms in self.legal_terms.items():
                if any(term in query_lower for term in terms):
                    if category.lower() in doc["category"].lower():
                        score += 8
                    else:
                        score += 2
            
            if score > 0:
                results.append({
                    "document": doc,
                    "score": score,
                    "relevance": min(score / 20, 1.0)  # Normalize to 0-1
                })
        
        # Sort by score and return top 5
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:5]
    
    def classify_question(self, query: str) -> str:
        """Enhanced question classification"""
        query_lower = query.lower()
        
        # Check for specific legal areas
        if any(term in query_lower for term in ['constitution', 'fundamental right', 'article']):
            return 'constitutional'
        elif any(term in query_lower for term in ['crime', 'murder', 'theft', 'ipc', 'penal']):
            return 'criminal'
        elif any(term in query_lower for term in ['contract', 'breach', 'agreement', 'damages']):
            return 'contract'
        elif any(term in query_lower for term in ['consumer', 'defective', 'unfair trade']):
            return 'consumer'
        elif any(term in query_lower for term in ['company', 'director', 'corporate', 'shareholder']):
            return 'corporate'
        elif any(term in query_lower for term in ['motor vehicle', 'driving', 'license', 'traffic']):
            return 'motor_vehicle'
        elif any(term in query_lower for term in ['cyber', 'internet', 'computer', 'hacking']):
            return 'cyber'
        elif any(term in query_lower for term in ['tax', 'gst', 'income tax', 'assessment']):
            return 'tax'
        elif any(term in query_lower for term in ['information', 'rti', 'transparency']):
            return 'information'
        else:
            return 'general'
    
    async def get_response(self, query: str) -> Dict[str, Any]:
        """Generate enhanced response with logging"""
        # Ensure initialization before processing
        await self.initialize()
        
        start_time = datetime.now()
        
        # Search for relevant documents
        search_results = self.search_documents(query)
        question_type = self.classify_question(query)
        
        if not search_results:
            response = {
                "answer": "I couldn't find specific information about your query in the current legal database. However, I recommend consulting with a qualified lawyer for personalized legal advice. You can also check the official India Code website (https://www.indiacode.nic.in) for comprehensive legal information.",
                "sources": ["General Legal Advice"],
                "confidence": 0.1,
                "question_type": question_type,
                "suggestions": [
                    "Try rephrasing your question with more specific legal terms",
                    "Consult with a qualified legal professional",
                    "Check official government legal portals"
                ]
            }
        else:
            # Generate comprehensive response
            primary_doc = search_results[0]["document"]
            related_docs = [r["document"] for r in search_results[1:3]]
            
            response_text = f"Based on {primary_doc['source']}, {primary_doc['section']}:\n\n"
            response_text += f"{primary_doc['content']}\n\n"
            
            if related_docs:
                response_text += "Related provisions:\n"
                for doc in related_docs:
                    response_text += f"• {doc['source']}, {doc['section']}: {doc['title']}\n"
            
            response_text += "\n**Important:** This information is for educational purposes only. For specific legal advice applicable to your situation, please consult with a qualified lawyer."
            
            sources = [f"{doc['document']['source']} - {doc['document']['section']}" for doc in search_results]
            
            response = {
                "answer": response_text,
                "sources": sources,
                "confidence": search_results[0]["relevance"],
                "question_type": question_type,
                "legal_references": [
                    {
                        "title": doc["document"]["title"],
                        "source": doc["document"]["source"],
                        "section": doc["document"]["section"],
                        "url": doc["document"].get("url", "")
                    }
                    for doc in search_results[:3]
                ]
            }
        
        # Log the query and response
        end_time = datetime.now()
        response_time = int((end_time - start_time).total_seconds() * 1000)
        
        self.data_service.log_user_query(
            query=query,
            response=response["answer"][:500] + "..." if len(response["answer"]) > 500 else response["answer"],
            sources=response["sources"],
            response_time=response_time
        )
        
        return response
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get usage analytics"""
        popular_queries = self.data_service.get_popular_queries()
        
        return {
            "total_documents": len(self.documents),
            "popular_queries": popular_queries,
            "categories": list(set(doc["category"] for doc in self.documents)),
            "sources": list(set(doc["source"] for doc in self.documents))
        }