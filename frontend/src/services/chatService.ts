import { ChatResponse } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class ChatService {
  async sendMessage(message: string, conversationId?: string): Promise<ChatResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
          conversation_id: conversationId,
          include_sources: true,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error calling chat API:', error);
      
      // Return a mock response for demo purposes
      return {
        message: `I understand you're asking about: "${message}". 

This is currently running in demo mode. To connect to the full backend:
1. Start the backend server: cd backend && python main.py
2. Make sure your OpenAI API key is set in the .env file

The system would normally analyze your query against Indian legal documents and provide:
- Relevant sections from Constitution, IPC, and other acts
- Source citations with exact references
- Context-aware legal information

**Sample Response:** Based on your query, this would typically reference specific legal provisions like Constitutional Articles, IPC sections, or relevant case law from Indian courts.`,
        conversation_id: conversationId || 'demo-conversation-' + Date.now(),
        sources: [
          {
            title: "Constitution of India - Article 14",
            content: "The State shall not deny to any person equality before the law or the equal protection of the laws within the territory of India.",
            source: "Constitution of India",
            section: "Article 14",
            url: "https://www.india.gov.in/my-government/constitution-india/constitution-india-full-text",
            similarity_score: 0.85
          },
          {
            title: "Indian Penal Code - Section 302",
            content: "Whoever commits murder shall be punished with death, or imprisonment for life, and shall also be liable to fine.",
            source: "Indian Penal Code, 1860",
            section: "Section 302",
            url: "https://www.indiacode.nic.in/handle/123456789/2263",
            similarity_score: 0.78
          }
        ],
        disclaimer: "This is for informational purposes only and does not constitute legal advice. Please consult with qualified legal professionals for specific legal matters."
      };
    }
  }

  async getConversation(conversationId: string) {
    try {
      const response = await fetch(`${API_BASE_URL}/conversations/${conversationId}`);
      return await response.json();
    } catch (error) {
      console.error('Error fetching conversation:', error);
      throw error;
    }
  }

  async getDocuments() {
    try {
      const response = await fetch(`${API_BASE_URL}/legal-documents`);
      return await response.json();
    } catch (error) {
      console.error('Error fetching documents:', error);
      throw error;
    }
  }
}

export const chatService = new ChatService();