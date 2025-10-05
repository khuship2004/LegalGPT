import os
import json
from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import asyncio

class RAGService:
    def __init__(self):
        # Initialize models - using free Hugging Face models
        print("Loading embedding model...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        print("Loading language model...")
        # Using Microsoft DialoGPT for free conversational AI
        model_name = "microsoft/DialoGPT-medium"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.language_model = AutoModelForCausalLM.from_pretrained(model_name)
        
        # Create text generation pipeline
        self.text_generator = pipeline(
            "text-generation", 
            model=self.language_model,
            tokenizer=self.tokenizer,
            max_length=512,
            do_sample=True,
            temperature=0.7,
            pad_token_id=self.tokenizer.eos_token_id
        )
        
        # Load or create vector database
        self.index = None
        self.documents = []
        self.document_metadata = []
        
        # Initialize with sample data
        self._initialize_sample_data()
        self._build_vector_index()
    
    def _initialize_sample_data(self):
        """Initialize with sample Indian legal documents"""
        sample_documents = [
            {
                "title": "Constitution of India - Article 14",
                "content": "Article 14: Equality before law. The State shall not deny to any person equality before the law or the equal protection of the laws within the territory of India.",
                "source": "Constitution of India",
                "section": "Article 14",
                "category": "Fundamental Rights",
                "url": "https://www.india.gov.in/my-government/constitution-india/constitution-india-full-text"
            },
            {
                "title": "Constitution of India - Article 21",
                "content": "Article 21: Protection of life and personal liberty. No person shall be deprived of his life or personal liberty except according to procedure established by law.",
                "source": "Constitution of India",
                "section": "Article 21",
                "category": "Fundamental Rights",
                "url": "https://www.india.gov.in/my-government/constitution-india/constitution-india-full-text"
            },
            {
                "title": "Indian Penal Code - Section 302",
                "content": "Section 302: Punishment for murder. Whoever commits murder shall be punished with death, or imprisonment for life, and shall also be liable to fine.",
                "source": "Indian Penal Code, 1860",
                "section": "Section 302",
                "category": "Criminal Law",
                "url": "https://www.indiacode.nic.in/handle/123456789/2263"
            },
            {
                "title": "Indian Contract Act - Section 10",
                "content": "Section 10: What agreements are contracts. All agreements are contracts if they are made by the free consent of parties competent to contract, for a lawful consideration and with a lawful object, and are not hereby expressly declared to be void.",
                "source": "Indian Contract Act, 1872",
                "section": "Section 10",
                "category": "Contract Law",
                "url": "https://www.indiacode.nic.in/handle/123456789/2268"
            },
            {
                "title": "Consumer Protection Act - Section 2(1)",
                "content": "Section 2(1): Consumer means any person who buys any goods for a consideration which has been paid or promised or partly paid and partly promised, or under any system of deferred payment and includes any user of such goods other than the person who buys such goods for consideration paid or promised or partly paid and partly promised, or under any system of deferred payment when such use is made with the approval of such person, but does not include a person who obtains such goods for resale or for any commercial purpose.",
                "source": "Consumer Protection Act, 2019",
                "section": "Section 2(1)",
                "category": "Consumer Law",
                "url": "https://www.indiacode.nic.in/handle/123456789/15397"
            },
            {
                "title": "Companies Act - Section 2(20)",
                "content": "Section 2(20): Company means a company incorporated under this Act or under any previous company law.",
                "source": "Companies Act, 2013",
                "section": "Section 2(20)",
                "category": "Corporate Law",
                "url": "https://www.mca.gov.in/content/mca/global/en/acts-rules/acts/companies-act-2013.html"
            },
            {
                "title": "Right to Information Act - Section 2(f)",
                "content": "Section 2(f): Information means any material in any form, including records, documents, memos, e-mails, opinions, advices, press releases, circulars, orders, logbooks, contracts, reports, papers, samples, models, data material held in any electronic form and information relating to any private body which can be accessed by a public authority under any other law for the time being in force.",
                "source": "Right to Information Act, 2005",
                "section": "Section 2(f)",
                "category": "Administrative Law",
                "url": "https://www.indiacode.nic.in/handle/123456789/1362"
            }
        ]
        
        self.documents = [doc["content"] for doc in sample_documents]
        self.document_metadata = sample_documents
    
    def _build_vector_index(self):
        """Build FAISS vector index from documents"""
        if not self.documents:
            return
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(self.documents)
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings.astype('float32'))
        
        print(f"Built vector index with {len(self.documents)} documents")
    
    async def retrieve_relevant_docs(self, query: str, top_k: int = 3) -> List[Dict]:
        """Retrieve most relevant documents for a query"""
        if not self.index:
            return []
        
        # Encode query
        query_embedding = self.embedding_model.encode([query])
        
        # Search in index
        scores, indices = self.index.search(query_embedding.astype('float32'), top_k)
        
        # Return relevant documents with metadata
        relevant_docs = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx < len(self.document_metadata):
                doc = self.document_metadata[idx].copy()
                doc['similarity_score'] = float(1 / (1 + score))  # Convert L2 distance to similarity
                doc['rank'] = i + 1
                relevant_docs.append(doc)
        
        return relevant_docs
    
    async def generate_response(self, query: str, conversation_history: List = None, include_sources: bool = True) -> Dict[str, Any]:
        """Generate AI response using RAG"""
        
        # Retrieve relevant documents
        relevant_docs = await self.retrieve_relevant_docs(query, top_k=3)
        
        # Prepare context from retrieved documents
        context = ""
        sources = []
        
        if relevant_docs:
            context_parts = []
            for doc in relevant_docs:
                context_parts.append(f"Source: {doc['title']}\nContent: {doc['content']}\nReference: {doc['section']}")
                sources.append({
                    "title": doc['title'],
                    "content": doc['content'][:200] + "..." if len(doc['content']) > 200 else doc['content'],
                    "source": doc['source'],
                    "section": doc['section'],
                    "url": doc.get('url', ''),
                    "similarity_score": doc['similarity_score']
                })
            context = "\n\n".join(context_parts)
        
        # Create system prompt
        system_prompt = """You are an AI assistant specializing in Indian law. Your role is to provide helpful, accurate, and well-sourced information about Indian legal matters.

IMPORTANT GUIDELINES:
1. Always base your answers on the provided legal sources
2. Include specific references to sections, articles, or acts when citing law
3. If the question cannot be answered from the provided sources, say so clearly
4. Never provide direct legal advice - always include appropriate disclaimers
5. Be precise and cite the exact legal provisions
6. If multiple interpretations exist, mention them
7. Keep responses clear and accessible to non-lawyers

DISCLAIMER: Always remind users that this is informational only and not legal advice.

Context from legal documents:
{context}

Remember: You must cite sources and provide accurate legal information based only on the provided context."""
        
        # Create human prompt
        human_prompt = f"""Based on the provided legal sources, please answer this question about Indian law:

Question: {query}

Please provide:
1. A clear, direct answer based on the sources
2. Specific citations to relevant sections/articles
3. Any important clarifications or limitations
4. Appropriate legal disclaimer

Answer:"""
        
        # Generate response using free Hugging Face model
        full_prompt = f"""Legal AI Assistant Response:

Context: {context if context else 'No specific legal documents found for this query.'}

User Question: {query}

Based on the provided legal sources, here is a helpful response about Indian law:

"""
        
        try:
            # Use the text generation pipeline
            response = await asyncio.to_thread(
                self.text_generator,
                full_prompt,
                max_length=len(full_prompt.split()) + 150,
                num_return_sequences=1,
                do_sample=True,
                temperature=0.7
            )
            
            # Extract the generated text
            if response and len(response) > 0:
                generated_text = response[0]['generated_text']
                # Get only the new generated part
                answer = generated_text[len(full_prompt):].strip()
                
                # If the generated text is too short or incomplete, provide a structured response
                if len(answer) < 50 or not answer:
                    answer = self._create_structured_response(query, context, relevant_docs)
            else:
                answer = self._create_structured_response(query, context, relevant_docs)
            
            # Add disclaimer if not already present
            if "disclaimer" not in answer.lower() and "not legal advice" not in answer.lower():
                answer += "\n\n**Disclaimer:** This information is for educational purposes only and does not constitute legal advice. Please consult with a qualified legal professional for specific legal matters."
            
            return {
                "answer": answer,
                "sources": sources if include_sources else [],
                "context_used": bool(context)
            }
            
        except Exception as e:
            # Fallback response
            print(f"Error in text generation: {str(e)}")
            answer = self._create_structured_response(query, context, relevant_docs)
        
        # Add disclaimer if not already present
        if "disclaimer" not in answer.lower() and "not legal advice" not in answer.lower():
            answer += "\n\n**Disclaimer:** This information is for educational purposes only and does not constitute legal advice. Please consult with a qualified legal professional for specific legal matters."
        
        return {
            "answer": answer,
            "sources": sources if include_sources else [],
            "context_used": bool(context)
        }
    
    def _create_structured_response(self, query: str, context: str, relevant_docs: List[Dict]) -> str:
        """Create a structured response when AI generation fails or is insufficient"""
        
        if not relevant_docs:
            return f"""I understand you're asking about: "{query}"

Unfortunately, I couldn't find specific relevant legal documents in my current database for this query. However, I can suggest that for questions about Indian law, you should consult:

• The Constitution of India for fundamental rights and procedures
• The Indian Penal Code (IPC) for criminal law matters  
• The Indian Contract Act for contract-related questions
• Specific state laws if your question relates to state jurisdiction

For accurate legal information, please consult with a qualified legal professional or refer to official government legal resources."""

        # Create response based on retrieved documents
        response_parts = [
            f"Based on your question about '{query}', here's what I found from Indian legal sources:\n"
        ]
        
        for i, doc in enumerate(relevant_docs[:2], 1):  # Use top 2 most relevant docs
            response_parts.append(f"**{i}. {doc['title']}**")
            response_parts.append(f"According to {doc['section']} of the {doc['source']}:")
            response_parts.append(f'"{doc["content"][:300]}..."')
            response_parts.append("")  # Empty line for spacing
        
        if len(relevant_docs) > 2:
            response_parts.append(f"*Additional {len(relevant_docs)-2} related sources are available in the sources panel.*")
        
        response_parts.append("\n**Important Notes:**")
        response_parts.append("• This information is based on available legal documents")
        response_parts.append("• Laws may have been updated since the last data refresh")
        response_parts.append("• Always verify with current official sources")
        response_parts.append("• For legal advice, consult a qualified advocate")
        
        return "\n".join(response_parts)
    
    async def health_check(self) -> bool:
        """Check if the service is healthy"""
        try:
            # Test embedding model
            test_embedding = self.embedding_model.encode(["test"])
            
            # Test text generation pipeline with a simple query
            test_response = await asyncio.to_thread(
                self.text_generator,
                "What is law?",
                max_length=50,
                num_return_sequences=1
            )
            
            return True
        except Exception as e:
            raise Exception(f"RAG service health check failed: {str(e)}")
    
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