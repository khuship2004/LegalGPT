import os
import json
import re
from typing import List, Dict, Any
import asyncio

class SimpleRAGService:
    """Simplified RAG service using keyword matching instead of ML models"""
    
    def __init__(self):
        print("Initializing Simple RAG Service...")
        
        # Simple document storage
        self.documents = []
        self.document_metadata = []
        
        # Initialize with sample data
        self._initialize_sample_data()
        print(f"Loaded {len(self.documents)} legal documents")
    
    def _initialize_sample_data(self):
        """Initialize with sample Indian legal documents"""
        sample_documents = [
            {
                "title": "Constitution of India - Article 14",
                "content": "Article 14: Equality before law. The State shall not deny to any person equality before the law or the equal protection of the laws within the territory of India. This fundamental right ensures that all citizens are treated equally regardless of religion, race, caste, sex or place of birth.",
                "source": "Constitution of India",
                "section": "Article 14",
                "category": "Fundamental Rights",
                "keywords": ["equality", "fundamental rights", "constitution", "discrimination", "equal protection"],
                "url": "https://www.india.gov.in/my-government/constitution-india/constitution-india-full-text"
            },
            {
                "title": "Constitution of India - Article 21",
                "content": "Article 21: Protection of life and personal liberty. No person shall be deprived of his life or personal liberty except according to procedure established by law. This article is the heart of fundamental rights and has been interpreted broadly by the Supreme Court.",
                "source": "Constitution of India",
                "section": "Article 21",
                "category": "Fundamental Rights",
                "keywords": ["life", "liberty", "fundamental rights", "constitution", "protection", "due process"],
                "url": "https://www.india.gov.in/my-government/constitution-india/constitution-india-full-text"
            },
            {
                "title": "Indian Penal Code - Section 302",
                "content": "Section 302: Punishment for murder. Whoever commits murder shall be punished with death, or imprisonment for life, and shall also be liable to fine. Murder is defined as causing death with intention or knowledge that the act is likely to cause death.",
                "source": "Indian Penal Code, 1860",
                "section": "Section 302",
                "category": "Criminal Law",
                "keywords": ["murder", "death penalty", "life imprisonment", "criminal", "punishment", "homicide"],
                "url": "https://www.indiacode.nic.in/handle/123456789/2263"
            },
            {
                "title": "Indian Contract Act - Section 10",
                "content": "Section 10: What agreements are contracts. All agreements are contracts if they are made by the free consent of parties competent to contract, for a lawful consideration and with a lawful object, and are not hereby expressly declared to be void. Essential elements include offer, acceptance, consideration, and legal capacity.",
                "source": "Indian Contract Act, 1872",
                "section": "Section 10",
                "category": "Contract Law",
                "keywords": ["contract", "agreement", "consent", "consideration", "offer", "acceptance", "legal capacity"],
                "url": "https://www.indiacode.nic.in/handle/123456789/2268"
            },
            {
                "title": "Consumer Protection Act - Section 2(1)",
                "content": "Section 2(1): Consumer definition. Consumer means any person who buys any goods for a consideration which has been paid or promised, and includes any user of such goods. This excludes persons who obtain goods for resale or commercial purpose. Consumer rights include right to safety, information, choice, and redressal.",
                "source": "Consumer Protection Act, 2019",
                "section": "Section 2(1)",
                "category": "Consumer Law",
                "keywords": ["consumer", "buyer", "goods", "services", "consumer rights", "protection", "commercial"],
                "url": "https://www.indiacode.nic.in/handle/123456789/15397"
            },
            {
                "title": "Companies Act - Section 2(20)",
                "content": "Section 2(20): Company definition. Company means a company incorporated under this Act or under any previous company law. It includes private companies, public companies, one person companies, and foreign companies operating in India.",
                "source": "Companies Act, 2013",
                "section": "Section 2(20)",
                "category": "Corporate Law",
                "keywords": ["company", "incorporation", "corporate", "business", "private company", "public company"],
                "url": "https://www.mca.gov.in/content/mca/global/en/acts-rules/acts/companies-act-2013.html"
            },
            {
                "title": "Right to Information Act - Section 2(f)",
                "content": "Section 2(f): Information definition. Information means any material in any form, including records, documents, memos, e-mails, opinions, advices, press releases, circulars, orders, logbooks, contracts, reports, papers, samples, models, data material held in any electronic form. RTI promotes transparency and accountability in governance.",
                "source": "Right to Information Act, 2005",
                "section": "Section 2(f)",
                "category": "Administrative Law",
                "keywords": ["information", "RTI", "transparency", "documents", "records", "public information", "governance"],
                "url": "https://www.indiacode.nic.in/handle/123456789/1362"
            },
            {
                "title": "Indian Evidence Act - Section 3",
                "content": "Section 3: Interpretation clause. Evidence means and includes all statements which the Court permits or requires to be made before it by witnesses, in relation to matters of fact under inquiry. It includes documentary evidence and all documents including electronic records.",
                "source": "Indian Evidence Act, 1872",
                "section": "Section 3",
                "category": "Evidence Law",
                "keywords": ["evidence", "witness", "testimony", "documents", "court", "proof", "electronic records"],
                "url": "https://www.indiacode.nic.in/handle/123456789/2034"
            },
            {
                "title": "Code of Criminal Procedure - Section 154",
                "content": "Section 154: Information in cognizable cases. Every information relating to the commission of a cognizable offence, if given orally to an officer in charge of a police station, shall be reduced to writing by him or under his direction, and be read over to the informant. Such information is called First Information Report (FIR).",
                "source": "Code of Criminal Procedure, 1973",
                "section": "Section 154",
                "category": "Criminal Procedure",
                "keywords": ["fir", "first information report", "police", "cognizable", "complaint", "criminal procedure"],
                "url": "https://www.indiacode.nic.in/handle/123456789/2263"
            },
            {
                "title": "Constitution of India - Article 19",
                "content": "Article 19: Protection of certain rights regarding freedom of speech etc. All citizens shall have the right to freedom of speech and expression, to assemble peaceably and without arms, to form associations or unions, to move freely throughout India, and to practice any profession or carry on any occupation, trade or business.",
                "source": "Constitution of India",
                "section": "Article 19", 
                "category": "Fundamental Rights",
                "keywords": ["freedom of speech", "expression", "assembly", "movement", "profession", "fundamental rights"],
                "url": "https://www.india.gov.in/my-government/constitution-india/constitution-india-full-text"
            },
            {
                "title": "Indian Penal Code - Section 375",
                "content": "Section 375: Rape. A man is said to commit rape if he has sexual intercourse with a woman under circumstances falling under any of the descriptions given in this section without her consent or against her will, or with her consent when obtained by putting her in fear of death or hurt.",
                "source": "Indian Penal Code, 1860",
                "section": "Section 375",
                "category": "Criminal Law",
                "keywords": ["rape", "sexual offence", "consent", "women safety", "criminal", "punishment"],
                "url": "https://www.indiacode.nic.in/handle/123456789/2263"
            },
            {
                "title": "Motor Vehicles Act - Section 185",
                "content": "Section 185: Driving by a drunken person or under the influence of drugs. Whoever, while driving a motor vehicle, has in his blood alcohol exceeding 30 mg per 100 ml of blood detected in a test, shall be punishable with imprisonment of either description for a term which may extend to six months, or with fine which may extend to two thousand rupees, or with both.",
                "source": "Motor Vehicles Act, 1988",
                "section": "Section 185",
                "category": "Traffic Law",
                "keywords": ["drunk driving", "alcohol", "driving", "motor vehicle", "traffic offence", "punishment"],
                "url": "https://www.indiacode.nic.in/handle/123456789/1361"
            }
        ]
        
        self.documents = [doc["content"] for doc in sample_documents]
        self.document_metadata = sample_documents
    
    def _simple_text_search(self, query: str, top_k: int = 3) -> List[Dict]:
        """Enhanced keyword-based search with better matching"""
        query_lower = query.lower()
        query_words = set(re.findall(r'\w+', query_lower))
        
        # Remove common stop words
        stop_words = {'the', 'is', 'are', 'was', 'were', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'what', 'how', 'when', 'where', 'why', 'who'}
        query_words = query_words - stop_words
        
        scored_docs = []
        
        for i, doc_meta in enumerate(self.document_metadata):
            score = 0
            
            # Exact phrase matching (highest weight)
            content_lower = doc_meta['content'].lower()
            title_lower = doc_meta['title'].lower()
            
            # Check for exact phrases
            if query_lower in content_lower:
                score += 10
            if query_lower in title_lower:
                score += 15
            
            # Check keywords (high weight)
            for keyword in doc_meta['keywords']:
                if keyword.lower() in query_lower:
                    score += 5
                # Partial keyword match
                for word in query_words:
                    if word in keyword.lower() or keyword.lower() in word:
                        score += 2
            
            # Check individual words in content
            for word in query_words:
                if len(word) > 2:  # Ignore very short words
                    if word in content_lower:
                        score += 1
                    if word in title_lower:
                        score += 2
                    if word in doc_meta['section'].lower():
                        score += 3
                    if word in doc_meta['category'].lower():
                        score += 2
            
            # Boost score for specific legal terms
            legal_terms = {
                'constitution': 8, 'article': 6, 'fundamental': 6, 'rights': 6,
                'ipc': 8, 'section': 4, 'penal': 6, 'criminal': 6, 'murder': 8,
                'contract': 8, 'agreement': 6, 'consideration': 6,
                'consumer': 8, 'protection': 6, 'goods': 4,
                'company': 8, 'corporate': 6, 'incorporation': 6,
                'evidence': 8, 'witness': 6, 'court': 4,
                'information': 6, 'rti': 8, 'transparency': 4
            }
            
            for term, weight in legal_terms.items():
                if term in query_lower and term in content_lower:
                    score += weight
            
            # Bonus for category matching
            if any(cat_word in query_lower for cat_word in doc_meta['category'].lower().split()):
                score += 3
            
            if score > 0:
                doc_copy = doc_meta.copy()
                doc_copy['similarity_score'] = min(score / 20.0, 1.0)  # Normalize and cap at 1.0
                doc_copy['rank'] = 0  # Will be set after sorting
                scored_docs.append(doc_copy)
        
        # Sort by score and return top_k
        scored_docs.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        # Set ranks
        for i, doc in enumerate(scored_docs[:top_k]):
            doc['rank'] = i + 1
        
        return scored_docs[:top_k]
    
    async def retrieve_relevant_docs(self, query: str, top_k: int = 3) -> List[Dict]:
        """Retrieve most relevant documents for a query"""
        return self._simple_text_search(query, top_k)
    
    async def generate_response(self, query: str, conversation_history: List = None, include_sources: bool = True) -> Dict[str, Any]:
        """Generate response using simple template-based approach"""
        
        # Retrieve relevant documents
        relevant_docs = await self.retrieve_relevant_docs(query, top_k=3)
        
        # Prepare context from retrieved documents
        sources = []
        
        if relevant_docs:
            for doc in relevant_docs:
                sources.append({
                    "title": doc['title'],
                    "content": doc['content'][:300] + "..." if len(doc['content']) > 300 else doc['content'],
                    "source": doc['source'],
                    "section": doc['section'],
                    "url": doc.get('url', ''),
                    "similarity_score": doc['similarity_score']
                })
        
        # Generate structured response
        answer = self._create_structured_response(query, relevant_docs)
        
        return {
            "answer": answer,
            "sources": sources if include_sources else [],
            "context_used": len(relevant_docs) > 0
        }
    
    def _create_structured_response(self, query: str, relevant_docs: List[Dict]) -> str:
        """Create a dynamic, question-specific response based on retrieved documents"""
        
        if not relevant_docs:
            return self._generate_no_match_response(query)
        
        # Analyze query to determine what type of question it is
        query_lower = query.lower()
        question_type = self._classify_question(query_lower)
        
        # Get the most relevant document
        primary_doc = relevant_docs[0]
        
        # Generate contextual response based on question type and content
        if question_type == "definition":
            response = self._generate_definition_response(query, primary_doc, relevant_docs)
        elif question_type == "procedure":
            response = self._generate_procedure_response(query, primary_doc, relevant_docs)
        elif question_type == "rights":
            response = self._generate_rights_response(query, primary_doc, relevant_docs)
        elif question_type == "punishment":
            response = self._generate_punishment_response(query, primary_doc, relevant_docs)
        else:
            response = self._generate_general_response(query, primary_doc, relevant_docs)
        
        # Add disclaimer
        response += "\n\n**⚖️ Legal Disclaimer:** This information is for educational purposes only and does not constitute legal advice. For specific legal matters, please consult with a qualified legal professional."
        
        return response
    
    def _classify_question(self, query_lower: str) -> str:
        """Classify the type of legal question being asked"""
        if any(word in query_lower for word in ["what is", "define", "meaning", "definition"]):
            return "definition"
        elif any(word in query_lower for word in ["procedure", "process", "how to", "steps", "filing"]):
            return "procedure"
        elif any(word in query_lower for word in ["rights", "fundamental rights", "constitutional rights"]):
            return "rights"
        elif any(word in query_lower for word in ["punishment", "penalty", "sentence", "jail", "imprisonment"]):
            return "punishment"
        else:
            return "general"
    
    def _generate_definition_response(self, query: str, primary_doc: Dict, relevant_docs: List[Dict]) -> str:
        """Generate response for definition-type questions"""
        content = primary_doc['content']
        
        response_parts = [
            f"**Definition Query:** {query}\n",
            f"According to **{primary_doc['section']}** of the **{primary_doc['source']}**:\n",
            f"*{content}*\n",
            "**Key Points:**"
        ]
        
        # Extract key information from the content
        if "fundamental right" in primary_doc.get('keywords', []):
            response_parts.append("• This is a fundamental right guaranteed by the Indian Constitution")
        if "criminal" in primary_doc.get('category', '').lower():
            response_parts.append("• This falls under criminal law provisions")
        if "contract" in primary_doc.get('keywords', []):
            response_parts.append("• This relates to contract law and business agreements")
        
        if len(relevant_docs) > 1:
            response_parts.append(f"\n**Related Provisions:**")
            for doc in relevant_docs[1:3]:  # Show up to 2 additional docs
                response_parts.append(f"• {doc['section']} of {doc['source']}")
        
        return "\n".join(response_parts)
    
    def _generate_procedure_response(self, query: str, primary_doc: Dict, relevant_docs: List[Dict]) -> str:
        """Generate response for procedure-type questions"""
        
        if "fir" in query.lower():
            return """**Procedure for Filing an FIR (First Information Report):**

**What is FIR?**
An FIR is the first step in criminal proceedings and must be filed when you become aware of a cognizable offense.

**Steps to File an FIR:**
1. **Go to the Police Station** - Visit the nearest police station in whose jurisdiction the crime occurred
2. **Provide Details** - Give complete information about the incident, including:
   - Date, time, and place of occurrence
   - Names and addresses of persons involved
   - Description of the incident
3. **Written Complaint** - The police will record your complaint in writing
4. **Get FIR Copy** - You are entitled to a free copy of the FIR
5. **FIR Number** - Note down the FIR number for future reference

**Legal Basis:**
• Section 154 of Code of Criminal Procedure (CrPC) mandates police to register FIR
• Section 166A of IPC makes it mandatory for police to record information about cognizable offenses

**Important Rights:**
• Police cannot refuse to register FIR for cognizable offenses
• FIR copy must be provided free of cost
• If police refuse, you can approach higher authorities or court"""

        # Default procedure response
        content = primary_doc['content']
        response_parts = [
            f"**Procedure Query:** {query}\n",
            f"Based on **{primary_doc['section']}** of the **{primary_doc['source']}**:\n",
            f"{content}\n",
            "**General Legal Procedure:**",
            "• Consult with a qualified legal professional",
            "• Gather all relevant documents and evidence",
            "• Follow the prescribed legal process",
            "• Maintain proper records of all proceedings"
        ]
        
        return "\n".join(response_parts)
    
    def _generate_rights_response(self, query: str, primary_doc: Dict, relevant_docs: List[Dict]) -> str:
        """Generate response for rights-related questions"""
        
        response_parts = [
            f"**Rights Query:** {query}\n"
        ]
        
        # Check if it's about fundamental rights
        if "fundamental" in query.lower():
            response_parts.extend([
                "**Fundamental Rights under the Indian Constitution:**\n",
                "The Constitution of India guarantees several fundamental rights to all citizens:\n"
            ])
            
            for doc in relevant_docs:
                if "fundamental" in doc.get('keywords', []):
                    response_parts.append(f"**{doc['section']}:** {doc['content']}\n")
        else:
            # Specific right query
            content = primary_doc['content']
            response_parts.extend([
                f"According to **{primary_doc['section']}** of the **{primary_doc['source']}**:\n",
                f"{content}\n"
            ])
        
        response_parts.extend([
            "**Key Aspects of These Rights:**",
            "• These rights are enforceable by courts",
            "• They can only be suspended during national emergency",
            "• They apply to all citizens equally",
            "• Violation can be challenged in court through writ petitions"
        ])
        
        return "\n".join(response_parts)
    
    def _generate_punishment_response(self, query: str, primary_doc: Dict, relevant_docs: List[Dict]) -> str:
        """Generate response for punishment-related questions"""
        content = primary_doc['content']
        
        response_parts = [
            f"**Legal Punishment Query:** {query}\n",
            f"According to **{primary_doc['section']}** of the **{primary_doc['source']}**:\n",
            f"*{content}*\n"
        ]
        
        # Add specific punishment details if available
        if "death" in content.lower():
            response_parts.append("**⚠️ Capital Punishment:** This offense may carry the death penalty")
        if "imprisonment for life" in content.lower():
            response_parts.append("**🔒 Life Imprisonment:** This is one of the most serious punishments under Indian law")
        if "fine" in content.lower():
            response_parts.append("**💰 Fine:** Monetary penalty may also be imposed along with imprisonment")
        
        response_parts.extend([
            "\n**Important Legal Notes:**",
            "• Actual punishment depends on specific circumstances of the case",
            "• Courts consider various factors while sentencing",
            "• Legal representation is crucial for serious offenses",
            "• Alternative punishments may be available based on case merits"
        ])
        
        return "\n".join(response_parts)
    
    def _generate_general_response(self, query: str, primary_doc: Dict, relevant_docs: List[Dict]) -> str:
        """Generate response for general legal questions"""
        content = primary_doc['content']
        
        response_parts = [
            f"**Legal Information:** {query}\n",
            f"Based on **{primary_doc['section']}** of the **{primary_doc['source']}**:\n",
            f"{content}\n"
        ]
        
        # Add relevant additional information
        if len(relevant_docs) > 1:
            response_parts.append("**Related Legal Provisions:**")
            for doc in relevant_docs[1:3]:
                response_parts.append(f"• **{doc['section']}:** {doc['content'][:150]}...")
        
        response_parts.extend([
            "\n**For More Information:**",
            f"• Refer to the complete text of {primary_doc['source']}",
            "• Consult legal commentaries and case law",
            "• Seek guidance from qualified legal professionals"
        ])
        
        return "\n".join(response_parts)
    
    def _generate_no_match_response(self, query: str) -> str:
        """Generate response when no relevant documents are found"""
        
        # Suggest relevant areas based on query keywords
        suggestions = []
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["criminal", "crime", "murder", "theft", "assault"]):
            suggestions.append("• **Indian Penal Code (IPC)** - for criminal law matters")
        if any(word in query_lower for word in ["contract", "agreement", "business"]):
            suggestions.append("• **Indian Contract Act, 1872** - for contract-related issues")
        if any(word in query_lower for word in ["rights", "constitutional", "fundamental"]):
            suggestions.append("• **Constitution of India** - for fundamental rights and constitutional law")
        if any(word in query_lower for word in ["consumer", "goods", "services"]):
            suggestions.append("• **Consumer Protection Act** - for consumer rights and disputes")
        if any(word in query_lower for word in ["company", "corporate", "business"]):
            suggestions.append("• **Companies Act, 2013** - for corporate and business law")
        
        response_parts = [
            f"**Query:** {query}\n",
            "I couldn't find specific information about this topic in my current legal database. However, based on your question, you may want to consult:\n"
        ]
        
        if suggestions:
            response_parts.extend(suggestions)
        else:
            response_parts.extend([
                "• **Constitution of India** - for fundamental rights and constitutional matters",
                "• **Indian Penal Code** - for criminal law questions",
                "• **Code of Civil Procedure** - for civil law procedures",
                "• **Indian Contract Act** - for contract and agreement issues"
            ])
        
        response_parts.extend([
            "\n**Recommended Actions:**",
            "• Consult with a qualified legal professional for specific advice",
            "• Check the latest legal databases and official government sources", 
            "• Consider contacting relevant government departments",
            "• Refer to recent Supreme Court and High Court judgments"
        ])
        
        return "\n".join(response_parts)
    
    async def health_check(self) -> bool:
        """Check if the service is healthy"""
        try:
            # Test simple search
            test_docs = self._simple_text_search("constitution", 1)
            return len(test_docs) > 0
        except Exception as e:
            raise Exception(f"Simple RAG service health check failed: {str(e)}")
    
    async def get_document_list(self) -> List[Dict]:
        """Get list of available documents"""
        return [
            {
                "title": doc["title"],
                "source": doc["source"],
                "section": doc["section"],
                "category": doc["category"]
            }
            for doc in self.document_metadata
        ]