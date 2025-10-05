import React, { useState, useEffect, useRef } from 'react';
import { Send, MessageCircle, Scale, AlertCircle, BookOpen, Loader2, X, TrendingUp, Database, Search } from 'lucide-react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

// Enhanced chat service with new endpoints
const chatService = {
  async sendMessage(message, conversationId) {
    try {
      const response = await axios.post(`${API_BASE_URL}/chat`, {
        message,
        conversation_id: conversationId,
        include_sources: true,
      });
      return response.data;
    } catch (error) {
      console.error('Error calling chat API:', error);
      
      // Enhanced demo response
      return {
        message: `I understand you're asking about: "${message}". 

**Enhanced LegalGPT System** - Currently running in demo mode since the backend may not be connected.

**New Features Available:**
🎯 **Enhanced Search Algorithm** - Better legal document matching
📊 **Analytics & Insights** - Query tracking and popular questions
💾 **Database Storage** - Persistent legal document storage
🌐 **External API Integration** - Ready for real legal data sources
🏷️ **Question Classification** - Automatic categorization (Constitutional, Criminal, Civil, etc.)
📚 **Comprehensive Coverage** - Constitution, IPC, Contract Act, Consumer Protection, and more

**Sample Enhanced Response:**
Based on your query about "${message}", the enhanced system would:
- Search through 15+ legal document categories
- Provide confidence scores for answers
- Show related legal provisions
- Track popular queries for insights
- Log interactions for system improvement

**To connect to the enhanced backend:**
1. \`cd backend && python main_enhanced.py\`  
2. The system now includes SQLite database storage
3. Ready for integration with India Code API when available`,
        conversation_id: conversationId || 'demo-conversation-' + Date.now(),
        sources: [
          {
            title: "Constitution of India - Article 14 (Right to Equality)",
            content: "The State shall not deny to any person equality before the law or the equal protection of the laws within the territory of India.",
            source: "Constitution of India",
            section: "Article 14", 
            url: "https://www.indiacode.nic.in/constitution-of-india"
          },
          {
            title: "Indian Penal Code - Section 302 (Murder)",
            content: "Whoever commits murder shall be punished with death, or imprisonment for life, and shall also be liable to fine.",
            source: "Indian Penal Code 1860",
            section: "Section 302",
            url: "https://www.indiacode.nic.in/indian-penal-code-1860"
          },
          {
            title: "Consumer Protection Act 2019 - Consumer Rights",
            content: "Every consumer has the right to be protected against marketing of goods and services which are hazardous to life and property.",
            source: "Consumer Protection Act 2019",
            section: "Section 2(9)",
            url: "https://www.indiacode.nic.in/consumer-protection-act-2019"
          }
        ],
        confidence: 0.85,
        question_type: "general",
        legal_references: [
          {
            title: "Constitution of India - Article 14",
            source: "Constitution of India", 
            section: "Article 14",
            url: "https://www.indiacode.nic.in/constitution-of-india"
          }
        ],
        disclaimer: "This information is for educational purposes only. Please consult with a qualified lawyer for specific legal advice."
      };
    }
  },

  async getAnalytics() {
    try {
      const response = await axios.get(`${API_BASE_URL}/analytics`);
      return response.data;
    } catch (error) {
      return {
        total_documents: 15,
        popular_queries: [
          { query: "Article 14 equality", count: 25 },
          { query: "IPC murder section", count: 18 },
          { query: "consumer rights", count: 12 }
        ],
        categories: ["Constitutional Law", "Criminal Law", "Consumer Law", "Contract Law"],
        sources: ["Constitution of India", "Indian Penal Code 1860", "Consumer Protection Act 2019"]
      };
    }
  },

  async searchDocuments(query) {
    try {
      const response = await axios.get(`${API_BASE_URL}/search?q=${encodeURIComponent(query)}&limit=5`);
      return response.data;
    } catch (error) {
      return {
        query,
        results: [],
        total_found: 0
      };
    }
  }
};

function App() {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const [selectedSources, setSelectedSources] = useState([]);
  const [showSourcePanel, setShowSourcePanel] = useState(false);
  const [showAnalytics, setShowAnalytics] = useState(false);
  const [analytics, setAnalytics] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Load analytics on component mount
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    try {
      const data = await chatService.getAnalytics();
      setAnalytics(data);
    } catch (error) {
      console.error('Error loading analytics:', error);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    
    try {
      const results = await chatService.searchDocuments(searchQuery);
      setSearchResults(results);
    } catch (error) {
      console.error('Error searching:', error);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await chatService.sendMessage(inputMessage, conversationId);
      
      if (!conversationId) {
        setConversationId(response.conversation_id);
      }

      const assistantMessage = {
        role: 'assistant',
        content: response.message,
        timestamp: new Date().toISOString(),
        sources: response.sources || [],
        confidence: response.confidence || 0,
        question_type: response.question_type || 'general',
        legal_references: response.legal_references || [],
        disclaimer: response.disclaimer
      };

      setMessages(prev => [...prev, assistantMessage]);
      
      // Update analytics after each query
      loadAnalytics();
      
    } catch (error) {
      console.error('Error sending message:', error);
      
      const errorMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error while processing your request. Please try again or check if the backend server is running.',
        timestamp: new Date().toISOString(),
        sources: [],
        isError: true
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const openSourcePanel = (sources) => {
    setSelectedSources(sources);
    setShowSourcePanel(true);
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return 'text-green-600';
    if (confidence >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getQuestionTypeColor = (type) => {
    const colors = {
      'constitutional': 'bg-blue-100 text-blue-800',
      'criminal': 'bg-red-100 text-red-800',
      'civil': 'bg-green-100 text-green-800',
      'contract': 'bg-purple-100 text-purple-800',
      'consumer': 'bg-orange-100 text-orange-800',
      'corporate': 'bg-indigo-100 text-indigo-800',
      'general': 'bg-gray-100 text-gray-800'
    };
    return colors[type] || colors.general;
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-white shadow-sm border-b px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Scale className="h-8 w-8 text-blue-600" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">LegalGPT Enhanced</h1>
                <p className="text-sm text-gray-500">AI-powered Legal Assistant with Advanced Analytics</p>
              </div>
            </div>
            <div className="flex space-x-2">
              <button
                onClick={() => setShowAnalytics(!showAnalytics)}
                className="flex items-center space-x-2 px-3 py-2 bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-colors"
              >
                <TrendingUp className="h-4 w-4" />
                <span>Analytics</span>
              </button>
              <button
                onClick={() => setShowSourcePanel(!showSourcePanel)}
                className="flex items-center space-x-2 px-3 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
              >
                <Database className="h-4 w-4" />
                <span>Sources</span>
              </button>
            </div>
          </div>
        </div>

        {/* Analytics Panel */}
        {showAnalytics && analytics && (
          <div className="bg-white border-b px-6 py-4">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-blue-50 p-3 rounded-lg">
                <div className="text-sm text-blue-600 font-medium">Total Documents</div>
                <div className="text-2xl font-bold text-blue-900">{analytics.total_documents}</div>
              </div>
              <div className="bg-green-50 p-3 rounded-lg">
                <div className="text-sm text-green-600 font-medium">Categories</div>
                <div className="text-2xl font-bold text-green-900">{analytics.categories?.length || 0}</div>
              </div>
              <div className="bg-purple-50 p-3 rounded-lg">
                <div className="text-sm text-purple-600 font-medium">Legal Sources</div>
                <div className="text-2xl font-bold text-purple-900">{analytics.sources?.length || 0}</div>
              </div>
              <div className="bg-orange-50 p-3 rounded-lg">
                <div className="text-sm text-orange-600 font-medium">Popular Queries</div>
                <div className="text-2xl font-bold text-orange-900">{analytics.popular_queries?.length || 0}</div>
              </div>
            </div>
          </div>
        )}

        {/* Search Panel */}
        <div className="bg-white border-b px-6 py-3">
          <div className="flex space-x-2">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                placeholder="Search legal documents directly..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <button
              onClick={handleSearch}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Search
            </button>
          </div>
          
          {/* Search Results */}
          {searchResults && (
            <div className="mt-3 p-3 bg-gray-50 rounded-lg">
              <div className="text-sm font-medium text-gray-700 mb-2">
                Found {searchResults.total_found} results for "{searchResults.query}"
              </div>
              {searchResults.results?.slice(0, 3).map((result, idx) => (
                <div key={idx} className="text-xs text-gray-600 mb-1">
                  • {result.document?.title} (Score: {result.score})
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
          {messages.length === 0 && (
            <div className="text-center py-12">
              <MessageCircle className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-700 mb-2">Welcome to Enhanced LegalGPT!</h3>
              <p className="text-gray-500 max-w-md mx-auto">
                Ask questions about Indian law and get comprehensive answers with sources, confidence scores, and legal references.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-6 max-w-2xl mx-auto">
                <button
                  onClick={() => setInputMessage("What are fundamental rights in Indian Constitution?")}
                  className="p-3 text-left bg-blue-50 border border-blue-200 rounded-lg hover:bg-blue-100 transition-colors"
                >
                  <div className="font-medium text-blue-900">Constitutional Law</div>
                  <div className="text-sm text-blue-700">Fundamental rights and duties</div>
                </button>
                <button
                  onClick={() => setInputMessage("What is the punishment for theft under IPC?")}
                  className="p-3 text-left bg-red-50 border border-red-200 rounded-lg hover:bg-red-100 transition-colors"
                >
                  <div className="font-medium text-red-900">Criminal Law</div>
                  <div className="text-sm text-red-700">IPC sections and punishments</div>
                </button>
                <button
                  onClick={() => setInputMessage("What are consumer rights in India?")}
                  className="p-3 text-left bg-green-50 border border-green-200 rounded-lg hover:bg-green-100 transition-colors"
                >
                  <div className="font-medium text-green-900">Consumer Law</div>
                  <div className="text-sm text-green-700">Consumer protection rights</div>
                </button>
                <button
                  onClick={() => setInputMessage("What are the essentials of a valid contract?")}
                  className="p-3 text-left bg-purple-50 border border-purple-200 rounded-lg hover:bg-purple-100 transition-colors"
                >
                  <div className="font-medium text-purple-900">Contract Law</div>
                  <div className="text-sm text-purple-700">Contract formation and breach</div>
                </button>
              </div>
            </div>
          )}

          {messages.map((message, index) => (
            <div key={index} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-3xl rounded-lg px-4 py-3 ${
                message.role === 'user' 
                  ? 'bg-blue-600 text-white' 
                  : message.isError
                  ? 'bg-red-50 border border-red-200 text-red-800'
                  : 'bg-white border border-gray-200'
              }`}>
                {message.role === 'assistant' && (
                  <div className="flex items-center space-x-2 mb-2">
                    <Scale className="h-4 w-4 text-blue-600" />
                    <span className="text-sm font-medium text-gray-700">LegalGPT Enhanced</span>
                    {message.confidence !== undefined && (
                      <span className={`text-xs font-medium ${getConfidenceColor(message.confidence)}`}>
                        {(message.confidence * 100).toFixed(0)}% confidence
                      </span>
                    )}
                    {message.question_type && (
                      <span className={`text-xs px-2 py-1 rounded-full font-medium ${getQuestionTypeColor(message.question_type)}`}>
                        {message.question_type}
                      </span>
                    )}
                  </div>
                )}
                
                <div className="whitespace-pre-wrap">{message.content}</div>
                
                {message.role === 'assistant' && message.sources && message.sources.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-gray-200">
                    <button
                      onClick={() => openSourcePanel(message.sources)}
                      className="flex items-center space-x-2 text-blue-600 hover:text-blue-800 text-sm"
                    >
                      <BookOpen className="h-4 w-4" />
                      <span>View {message.sources.length} legal source{message.sources.length !== 1 ? 's' : ''}</span>
                    </button>
                  </div>
                )}

                {message.disclaimer && (
                  <div className="mt-3 pt-3 border-t border-gray-200">
                    <div className="flex items-start space-x-2 text-xs text-gray-600">
                      <AlertCircle className="h-3 w-3 mt-0.5 flex-shrink-0" />
                      <span>{message.disclaimer}</span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex justify-start">
              <div className="max-w-xs bg-white border border-gray-200 rounded-lg px-4 py-3">
                <div className="flex items-center space-x-2">
                  <Loader2 className="h-4 w-4 animate-spin text-blue-600" />
                  <span className="text-gray-600">LegalGPT is analyzing your query...</span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="bg-white border-t px-6 py-4">
          <div className="flex space-x-4">
            <div className="flex-1 relative">
              <textarea
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask any question about Indian law..."
                className="w-full p-3 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows="2"
                disabled={isLoading}
              />
            </div>
            <button
              onClick={sendMessage}
              disabled={!inputMessage.trim() || isLoading}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Send className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>

      {/* Sources Panel */}
      {showSourcePanel && (
        <div className="w-80 bg-white border-l border-gray-200 flex flex-col">
          <div className="p-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-900">Legal Sources</h3>
              <button
                onClick={() => setShowSourcePanel(false)}
                className="p-1 hover:bg-gray-100 rounded"
              >
                <X className="h-5 w-5 text-gray-500" />
              </button>
            </div>
          </div>
          
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {selectedSources.length === 0 ? (
              <div className="text-center py-8">
                <BookOpen className="h-8 w-8 text-gray-400 mx-auto mb-2" />
                <p className="text-gray-500">No sources selected</p>
              </div>
            ) : (
              selectedSources.map((source, index) => (
                <div key={index} className="border border-gray-200 rounded-lg p-3">
                  <div className="flex items-start justify-between mb-2">
                    <h4 className="font-medium text-gray-900 text-sm">{source.title}</h4>
                  </div>
                  <p className="text-xs text-gray-600 mb-2">{source.content}</p>
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-gray-500">{source.source} - {source.section}</span>
                    {source.url && (
                      <a
                        href={source.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:text-blue-800"
                      >
                        View Full Text
                      </a>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;