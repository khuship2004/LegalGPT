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
      
      // Return demo response for development
      return {
        answer: `I understand you're asking about: "${message}". 

This is a demo response while the backend is being configured. Your LegalGPT system includes:

🏛️ **Constitutional Law**: Articles, fundamental rights, PIL procedures
⚖️ **Criminal Law**: IPC sections, FIR procedures, court processes  
📋 **Civil Law**: Contract law, property disputes, family matters
🛡️ **Consumer Protection**: Rights, complaint procedures, redressal
🏢 **Corporate Law**: Company registration, compliance, disputes

**⚖️ Legal Disclaimer**: This information is for educational purposes only and does not constitute legal advice. Please consult with qualified legal professionals for specific legal matters.`,
        sources: [
          {
            title: "Constitution of India",
            content: "Supreme law of India containing fundamental rights and duties",
            source: "Constitution of India, 1950",
            section: "Various Articles",
            url: "https://www.india.gov.in/my-government/constitution-india"
          }
        ],
        context_used: true,
        ai_powered: false
      };
    }
  },

  async getChatHistory(sessionId, token) {
    try {
      const response = await axios.get(`${API_BASE_URL}/chat/sessions/${sessionId}/queries`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching chat history:', error);
      return [];
    }
  }
};

// Source Panel Component
const SourcePanel = ({ sources, onClose }) => {
  return (
    <div className="fixed inset-y-0 right-0 w-96 bg-white shadow-xl border-l border-gray-200 z-50">
      <div className="flex items-center justify-between p-4 border-b border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900">Legal Sources</h3>
        <button
          onClick={onClose}
          className="p-1 hover:bg-gray-100 rounded-full"
        >
          <X className="h-5 w-5 text-gray-500" />
        </button>
      </div>
      
      <div className="p-4 space-y-4 overflow-y-auto h-full">
        {sources.map((source, index) => (
          <div key={index} className="bg-gray-50 p-4 rounded-lg">
            <h4 className="font-medium text-gray-900 mb-2">{source.title}</h4>
            <p className="text-sm text-gray-600 mb-2">{source.content}</p>
            <div className="text-xs text-gray-500 space-y-1">
              <p><strong>Source:</strong> {source.source}</p>
              {source.section && <p><strong>Section:</strong> {source.section}</p>}
              {source.url && (
                <a 
                  href={source.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-800 underline"
                >
                  View Official Document
                </a>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

// Enhanced Message Component with better formatting
const Message = ({ message }) => {
  const isUser = message.role === 'user';
  
  // Function to format assistant response
  const formatResponse = (content) => {
    if (isUser) return content;
    
    // Split content by common patterns and format
    const lines = content.split('\n');
    const formatted = [];
    
    lines.forEach((line, index) => {
      const trimmed = line.trim();
      if (!trimmed) return;
      
      // Headers (lines starting with ** or ##)
      if (trimmed.startsWith('**') && trimmed.endsWith('**')) {
        const headerText = trimmed.replace(/\*\*/g, '');
        formatted.push(
          <h3 key={index} className="font-semibold text-gray-900 mt-3 mb-2 text-base">
            {headerText}
          </h3>
        );
      }
      // Sub-headers (lines with single *)
      else if (trimmed.startsWith('*') && trimmed.endsWith('*') && !trimmed.includes('**')) {
        const subHeaderText = trimmed.replace(/\*/g, '');
        formatted.push(
          <h4 key={index} className="font-medium text-gray-800 mt-2 mb-1">
            {subHeaderText}
          </h4>
        );
      }
      // Bullet points
      else if (trimmed.startsWith('- ')) {
        formatted.push(
          <li key={index} className="ml-4 text-gray-700 mb-1">
            {trimmed.substring(2)}
          </li>
        );
      }
      // Numbered lists
      else if (/^\d+\./.test(trimmed)) {
        formatted.push(
          <li key={index} className="ml-4 text-gray-700 mb-1 list-decimal">
            {trimmed.replace(/^\d+\.\s*/, '')}
          </li>
        );
      }
      // Legal sections (Section XXX)
      else if (trimmed.includes('Section') || trimmed.includes('Article')) {
        formatted.push(
          <p key={index} className="text-gray-800 font-medium bg-blue-50 px-3 py-1 rounded mb-2">
            {trimmed}
          </p>
        );
      }
      // Important notes or disclaimers
      else if (trimmed.toLowerCase().includes('disclaimer') || trimmed.toLowerCase().includes('important')) {
        formatted.push(
          <div key={index} className="bg-yellow-50 border-l-4 border-yellow-400 px-3 py-2 my-2">
            <p className="text-yellow-800 text-sm font-medium">{trimmed}</p>
          </div>
        );
      }
      // Regular paragraphs
      else {
        formatted.push(
          <p key={index} className="text-gray-700 mb-2 leading-relaxed">
            {trimmed}
          </p>
        );
      }
    });
    
    return <div className="space-y-1">{formatted}</div>;
  };
  
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-6`}>
      <div className={`max-w-4xl px-5 py-4 rounded-lg ${
        isUser 
          ? 'bg-blue-600 text-white ml-12' 
          : 'bg-white shadow-sm border border-gray-200 mr-12'
      }`}>
        <div className="flex items-start space-x-4">
          {!isUser && (
            <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
              <Scale className="h-4 w-4 text-white" />
            </div>
          )}
          <div className="flex-1">
            <div className={`${isUser ? 'text-white' : 'text-gray-900'}`}>
              {formatResponse(message.content)}
            </div>
            {message.sources && message.sources.length > 0 && (
              <div className="mt-4 pt-3 border-t border-gray-200">
                <p className="text-sm font-medium text-gray-700 mb-2 flex items-center">
                  <BookOpen className="h-4 w-4 mr-1" />
                  Legal Sources:
                </p>
                <div className="space-y-2">
                  {message.sources.slice(0, 3).map((source, index) => (
                    <div key={index} className="bg-gray-50 rounded p-3 border-l-4 border-blue-500">
                      <p className="font-medium text-sm text-gray-800">{source.title}</p>
                      <p className="text-xs text-gray-600 mt-1">
                        Source: {source.source} {source.section && `• ${source.section}`}
                      </p>
                      {source.content && (
                        <p className="text-xs text-gray-600 mt-1 italic">
                          {source.content.substring(0, 100)}...
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
            {message.timestamp && (
              <div className={`text-xs mt-3 ${isUser ? 'text-blue-100' : 'text-gray-400'}`}>
                {new Date(message.timestamp).toLocaleTimeString()}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

// Main App Component
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
  const [refreshHistory, setRefreshHistory] = useState(0);
  
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
        // Trigger history refresh to show new session
        setRefreshHistory(prev => prev + 1);
      }
      
      const assistantMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.answer,
        sources: response.sources || [],
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
      setSources(response.sources || []);
      
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error while processing your request. Please try again.',
        timestamp: new Date()
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

  const handleSuggestionClick = async (suggestion) => {
    if (!user || !token || isLoading) return;

    const userMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: suggestion,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await chatService.sendMessage(suggestion, currentSessionId, token);
      
      // Update session ID if this was a new chat
      if (!currentSessionId && response.chat_session_id) {
        setCurrentSessionId(response.chat_session_id);
        // Trigger history refresh to show new session
        setRefreshHistory(prev => prev + 1);
      }
      
      const assistantMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.answer,
        sources: response.sources || [],
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
      setSources(response.sources || []);
      
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error while processing your request. Please try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
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
        refreshTrigger={refreshHistory}
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
                  onClick={handleLogout}
                  className="flex items-center space-x-2 px-3 py-2 text-gray-700 hover:text-red-600 hover:bg-red-50 rounded-md transition-colors"
                >
                  <LogOut className="h-4 w-4" />
                  <span className="hidden sm:inline">Logout</span>
                </button>
              </div>
            </div>
          </div>
        </header>

        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto p-4">
          <div className="max-w-4xl mx-auto">
            {messages.length === 0 ? (
              <div className="text-center py-12">
                <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-4 rounded-full w-16 h-16 mx-auto mb-4">
                  <Scale className="h-8 w-8 text-white" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  Welcome to LegalGPT v2.0
                </h3>
                <p className="text-gray-600 mb-4">
                  Ask me anything about Indian law, and I'll provide detailed information with proper sources.
                </p>
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 max-w-md mx-auto">
                  <p className="text-sm text-blue-800">
                    <strong>Try asking:</strong>
                  </p>
                  <ul className="text-sm mt-2 space-y-2">
                    <li>
                      <button 
                        onClick={() => handleSuggestionClick("What is PIL in Indian law?")}
                        className="text-blue-700 hover:text-blue-900 hover:bg-blue-100 px-2 py-1 rounded transition-colors cursor-pointer text-left w-full"
                      >
                        • "What is PIL in Indian law?"
                      </button>
                    </li>
                    <li>
                      <button 
                        onClick={() => handleSuggestionClick("How to file an FIR?")}
                        className="text-blue-700 hover:text-blue-900 hover:bg-blue-100 px-2 py-1 rounded transition-colors cursor-pointer text-left w-full"
                      >
                        • "How to file an FIR?"
                      </button>
                    </li>
                    <li>
                      <button 
                        onClick={() => handleSuggestionClick("Consumer protection rights in India")}
                        className="text-blue-700 hover:text-blue-900 hover:bg-blue-100 px-2 py-1 rounded transition-colors cursor-pointer text-left w-full"
                      >
                        • "Consumer protection rights in India"
                      </button>
                    </li>
                    <li>
                      <button 
                        onClick={() => handleSuggestionClick("Marriage laws in India")}
                        className="text-blue-700 hover:text-blue-900 hover:bg-blue-100 px-2 py-1 rounded transition-colors cursor-pointer text-left w-full"
                      >
                        • "Marriage laws in India"
                      </button>
                    </li>
                  </ul>
                </div>
              </div>
            ) : (
              messages.map((message, index) => (
                <Message key={index} message={message} />
              ))
            )}
            
            {isLoading && (
              <div className="flex justify-start mb-4">
                <div className="bg-white shadow-sm border border-gray-200 rounded-lg px-4 py-3 mr-12">
                  <div className="flex items-center space-x-3">
                    <div className="w-6 h-6 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center">
                      <Scale className="h-3 w-3 text-white" />
                    </div>
                    <div className="flex items-center space-x-2">
                      <Loader2 className="h-4 w-4 animate-spin text-blue-600" />
                      <span className="text-sm text-gray-600">Analyzing your legal query...</span>
                    </div>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input Area */}
        <div className="border-t border-gray-200 bg-white p-4">
          <div className="max-w-4xl mx-auto">
            <div className="flex space-x-4">
              <div className="flex-1 relative">
                <textarea
                  ref={inputRef}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask me about Indian law, legal procedures, rights, or any legal matter..."
                  className="w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  rows={1}
                  style={{ minHeight: '44px', maxHeight: '120px' }}
                />
                <button
                  onClick={handleSendMessage}
                  disabled={!input.trim() || isLoading}
                  className="absolute right-2 top-2 p-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  <Send className="h-4 w-4" />
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