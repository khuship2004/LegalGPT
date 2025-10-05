import React, { useState, useEffect, useRef } from 'react';
import { Send, MessageCircle, Scale, AlertCircle, BookOpen, Loader2, X, LogOut, Menu } from 'lucide-react';
import axios from 'axios';
import AuthPage from './components/AuthPage';
import ChatHistory from './components/ChatHistory';

const API_BASE_URL = 'http://localhost:8000';

// Enhanced chat service with authentication
const chatService = {
  async sendMessage(message, sessionId, token) {
    try {
      const response = await axios.post(`${API_BASE_URL}/chat/message`, {
        message: message,
        chat_session_id: sessionId
      }, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error calling chat API:', error);
      
      // Return demo response
      return {
        message: `I understand you're asking about: "${message}". 

This is currently running in demo mode since the backend may not be connected. 

To connect to the full backend:
1. Start the backend server: cd backend && python main.py
2. The system uses free Hugging Face models (no API keys required!)

The system would normally analyze your query against Indian legal documents and provide:
- Relevant sections from Constitution, IPC, and other acts  
- Source citations with exact references
- Context-aware legal information

**Sample Response:** Based on your query about "${message}", this would typically reference specific legal provisions like Constitutional Articles, IPC sections, or relevant case law from Indian courts.`,
        conversation_id: conversationId || 'demo-conversation-' + Date.now(),
        sources: [
          {
            title: "Constitution of India - Article 14",
            content: "The State shall not deny to any person equality before the law or the equal protection of the laws within the territory of India.",
            source: "Constitution of India",
            section: "Article 14",
            url: "https://www.india.gov.in/my-government/constitution-india/constitution-india-full-text"
          },
          {
            title: "Indian Penal Code - Section 302", 
            content: "Whoever commits murder shall be punished with death, or imprisonment for life, and shall also be liable to fine.",
            source: "Indian Penal Code, 1860",
            section: "Section 302",
            url: "https://www.indiacode.nic.in/handle/123456789/2263"
          }
        ],
        disclaimer: "This is for informational purposes only and does not constitute legal advice."
      };
    }
  }
};

// Components
const ChatMessage = ({ message, onSourceClick }) => {
  const isUser = message.role === 'user';
  
  return (
    <div className={`flex mb-4 ${isUser ? 'justify-end' : 'justify-start'} animate-fade-in`}>
      <div className={`max-w-3xl px-4 py-3 rounded-lg ${
        isUser 
          ? 'bg-blue-600 text-white' 
          : message.isError 
            ? 'bg-red-50 border border-red-200 text-red-800'
            : 'bg-white shadow-sm border border-gray-200 text-gray-800'
      }`}>
        <div className="whitespace-pre-wrap">{message.content}</div>
        {message.sources && message.sources.length > 0 && (
          <button
            onClick={onSourceClick}
            className="mt-2 text-xs text-blue-600 hover:text-blue-800 font-medium flex items-center space-x-1"
          >
            <BookOpen className="h-3 w-3" />
            <span>View {message.sources.length} source{message.sources.length !== 1 ? 's' : ''}</span>
          </button>
        )}
        {message.timestamp && (
          <div className="mt-1 text-xs opacity-60">
            {message.timestamp.toLocaleTimeString()}
          </div>
        )}
      </div>
    </div>
  );
};

const SourcePanel = ({ sources, onClose }) => {
  return (
    <div className="fixed right-0 top-0 h-full w-80 bg-white shadow-lg border-l border-gray-200 z-50">
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-900">Legal Sources</h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
          >
            <X className="h-5 w-5" />
          </button>
        </div>
      </div>
      <div className="p-4 overflow-y-auto h-[calc(100vh-80px)]">
        {sources.map((source, index) => (
          <div key={index} className="mb-4 p-3 bg-gray-50 rounded-lg">
            <h4 className="font-medium text-gray-900 mb-2">{source.title}</h4>
            <p className="text-sm text-gray-600 mb-2">{source.content}</p>
            <div className="text-xs text-gray-500">
              <p>Source: {source.source}</p>
              <p>Section: {source.section}</p>
              {source.url && (
                <a 
                  href={source.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline"
                >
                  View Original
                </a>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

const WelcomeScreen = ({ onExampleClick }) => {
  const exampleQuestions = [
    "What are the fundamental rights under Indian Constitution?",
    "Explain Section 302 of Indian Penal Code", 
    "What is the definition of a contract under Indian Contract Act?",
    "What are consumer rights in India?",
    "Explain Article 21 of the Constitution",
    "What is the procedure for filing an FIR?"
  ];

  return (
    <div className="text-center py-12">
      <div className="mb-8">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full mb-4">
          <Scale className="h-8 w-8 text-white" />
        </div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Welcome to LegalGPT</h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Your AI-powered assistant for Indian legal information. Ask questions about laws, 
          statutes, and legal procedures to get accurate, source-cited answers.
        </p>
      </div>
      
      <div className="mb-8">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Try these example questions:</h2>
        <div className="grid gap-3 max-w-2xl mx-auto">
          {exampleQuestions.map((question, index) => (
            <button
              key={index}
              onClick={() => onExampleClick(question)}
              className="text-left p-4 bg-white rounded-lg border border-gray-200 hover:border-blue-300 hover:shadow-sm transition-all duration-200"
            >
              <div className="flex items-start space-x-3">
                <MessageCircle className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
                <span className="text-gray-700">{question}</span>
              </div>
            </button>
          ))}
        </div>
      </div>
      
      <div className="bg-blue-50 rounded-lg p-6 max-w-2xl mx-auto">
        <h3 className="font-semibold text-blue-900 mb-2">How it works:</h3>
        <ul className="text-left text-blue-800 space-y-1">
          <li>• Ask questions about Indian laws and legal procedures</li>
          <li>• Get AI-generated answers with source citations</li>
          <li>• Access information from Constitution, IPC, and other acts</li>
          <li>• Remember: This is information, not legal advice</li>
        </ul>
      </div>
    </div>
  );
};

// Main App component
const App = () => {
  // Authentication state
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  
  // Chat state
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentSessionId, setCurrentSessionId] = useState(null);
  const [sources, setSources] = useState([]);
  const [showSources, setShowSources] = useState(false);
  
  // UI state
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Check for existing auth on load
  useEffect(() => {
    const savedToken = localStorage.getItem('token');
    const savedUser = localStorage.getItem('user');
    
    if (savedToken && savedUser) {
      setToken(savedToken);
      setUser(JSON.parse(savedUser));
    }
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Authentication handlers
  const handleAuth = (userData, userToken) => {
    setUser(userData);
    setToken(userToken);
    localStorage.setItem('token', userToken);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  const handleLogout = () => {
    setUser(null);
    setToken(null);
    setMessages([]);
    setCurrentSessionId(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };

  // Session management
  const handleSelectSession = async (sessionId) => {
    setCurrentSessionId(sessionId);
    setMessages([]);
    setIsLoading(true);

    try {
      const history = await chatService.getChatHistory(sessionId, token);
      const formattedMessages = [];
      
      history.forEach(query => {
        formattedMessages.push({
          role: 'user',
          content: query.query_text,
          timestamp: query.created_at
        });
        formattedMessages.push({
          role: 'assistant',
          content: query.response_text,
          sources: query.sources || [],
          timestamp: query.created_at,
          queryId: query.id
        });
      });
      
      setMessages(formattedMessages);
    } catch (error) {
      console.error('Error loading chat history:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewChat = () => {
    setMessages([]);
    setCurrentSessionId(null);
  };

  const handleSendMessage = async () => {
    if (!input.trim() || isLoading || !user || !token) return;

    const userMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim(),
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await chatService.sendMessage(input.trim(), currentSessionId, token);
      
      // Update session ID if this was a new chat
      if (!currentSessionId && response.chat_session_id) {
        setCurrentSessionId(response.chat_session_id);
      }
      
      const assistantMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.message,
        timestamp: new Date(),
        sources: response.sources
      };

      setMessages(prev => [...prev, assistantMessage]);
      setConversationId(response.conversation_id);
      setSources(response.sources || []);
      
      if (response.sources && response.sources.length > 0) {
        setShowSources(true);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'I apologize, but I encountered an error processing your request. Please try again.',
        timestamp: new Date(),
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
      handleSendMessage();
    }
  };

  const startNewConversation = () => {
    setMessages([]);
    setConversationId('');
    setSources([]);
    setShowSources(false);
    inputRef.current?.focus();
  };

  const handleExampleQuestion = (question) => {
    setInput(question);
    inputRef.current?.focus();
  };

  // Show authentication page if not logged in
  if (!user || !token) {
    return <AuthPage onAuth={handleAuth} />;
  }

  return (
    <div className="min-h-screen bg-gray-100 flex">
      {/* Chat History Sidebar */}
      <ChatHistory
        user={user}
        token={token}
        currentSessionId={currentSessionId}
        onSelectSession={handleSelectSession}
        onNewChat={handleNewChat}
        isCollapsed={sidebarCollapsed}
        onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
      />

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-4">
              <div className="flex items-center space-x-3">
                {sidebarCollapsed && (
                  <button
                    onClick={() => setSidebarCollapsed(false)}
                    className="p-2 hover:bg-gray-100 rounded-md lg:hidden"
                  >
                    <Menu className="h-5 w-5 text-gray-600" />
                  </button>
                )}
                <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-2 rounded-lg">
                  <Scale className="h-6 w-6 text-white" />
                </div>
                <div>
                  <h1 className="text-xl font-bold text-gray-900">LegalGPT v2.0</h1>
                  <p className="text-sm text-gray-500">AI Legal Assistant with Chat History</p>
                </div>
              </div>
              
              <div className="flex items-center space-x-4">
                <div className="text-sm text-gray-500">
                  Welcome, {user.username}!
                </div>
                <button
                  onClick={() => setShowSources(!showSources)}
                  className="flex items-center space-x-2 px-3 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
                >
                  <BookOpen className="h-4 w-4" />
                  <span>Sources</span>
                {sources.length > 0 && (
                  <span className="bg-blue-600 text-white text-xs px-2 py-0.5 rounded-full">
                    {sources.length}
                  </span>
                )}
              </button>
              <button
                onClick={startNewConversation}
                className="flex items-center space-x-2 px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors"
              >
                <MessageCircle className="h-4 w-4" />
                <span>New Chat</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="flex h-[calc(100vh-80px)]">
        {/* Main Chat Area */}
        <div className={`flex-1 flex flex-col ${showSources ? 'lg:mr-80' : ''} transition-all duration-300`}>
          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto chat-container px-4 sm:px-6 lg:px-8 py-6">
            <div className="max-w-4xl mx-auto">
              {messages.length === 0 ? (
                <WelcomeScreen onExampleClick={handleExampleQuestion} />
              ) : (
                <>
                  {messages.map((message) => (
                    <ChatMessage 
                      key={message.id} 
                      message={message} 
                      onSourceClick={() => setShowSources(true)}
                    />
                  ))}
                  {isLoading && (
                    <div className="flex justify-start mb-4">
                      <div className="bg-white rounded-lg px-4 py-3 shadow-sm border border-gray-200 max-w-xs">
                        <div className="flex items-center space-x-2">
                          <Loader2 className="h-4 w-4 animate-spin text-blue-600" />
                          <span className="text-gray-600 text-sm">Thinking...</span>
                        </div>
                      </div>
                    </div>
                  )}
                </>
              )}
              <div ref={messagesEndRef} />
            </div>
          </div>

          {/* Legal Disclaimer */}
          <div className="px-4 sm:px-6 lg:px-8 py-2">
            <div className="max-w-4xl mx-auto">
              <div className="bg-amber-50 border border-amber-200 rounded-lg p-3">
                <div className="flex items-start space-x-2">
                  <AlertCircle className="h-4 w-4 text-amber-600 mt-0.5 flex-shrink-0" />
                  <p className="text-xs text-amber-800">
                    <strong>Disclaimer:</strong> This AI provides general legal information only, not legal advice. 
                    Always consult with qualified legal professionals for specific legal matters.
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Input Area */}
          <div className="bg-white border-t border-gray-200 px-4 sm:px-6 lg:px-8 py-4">
            <div className="max-w-4xl mx-auto">
              <div className="flex space-x-4">
                <div className="flex-1">
                  <textarea
                    ref={inputRef}
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Ask me about Indian law..."
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                    rows={1}
                    style={{ minHeight: '48px', maxHeight: '120px' }}
                    disabled={isLoading}
                  />
                </div>
                <button
                  onClick={handleSendMessage}
                  disabled={!input.trim() || isLoading}
                  className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
                >
                  <Send className="h-4 w-4" />
                  <span className="hidden sm:inline">Send</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Source Panel */}
        {showSources && (
          <SourcePanel 
            sources={sources} 
            onClose={() => setShowSources(false)} 
          />
        )}
      </div>
    </div>
  );
};

export default App;