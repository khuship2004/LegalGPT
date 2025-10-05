import React, { useState, useEffect } from 'react';
import { MessageSquare, Plus, Archive, Bookmark, Clock, ChevronRight, Trash2 } from 'lucide-react';

const ChatHistory = ({ 
  user, 
  token, 
  currentSessionId, 
  onSelectSession, 
  onNewChat,
  isCollapsed,
  onToggleCollapse,
  refreshTrigger 
}) => {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user && token) {
      fetchChatSessions();
    }
  }, [user, token, refreshTrigger]);

  const fetchChatSessions = async () => {
    try {
      const response = await fetch('http://localhost:8000/chat/sessions', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        setSessions(data);
      } else {
        console.error('Failed to fetch chat sessions');
      }
    } catch (error) {
      console.error('Error fetching chat sessions:', error);
    } finally {
      setLoading(false);
    }
  };

  const createNewSession = async () => {
    try {
      const response = await fetch('http://localhost:8000/chat/sessions', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_name: `Legal Chat - ${new Date().toLocaleDateString()}`,
          topic: null
        }),
      });

      if (response.ok) {
        const newSession = await response.json();
        setSessions([newSession, ...sessions]);
        onSelectSession(newSession.id);
        onNewChat();
      } else {
        console.error('Failed to create new session');
      }
    } catch (error) {
      console.error('Error creating new session:', error);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 1) return 'Today';
    if (diffDays === 2) return 'Yesterday';
    if (diffDays <= 7) return `${diffDays - 1} days ago`;
    return date.toLocaleDateString();
  };

  if (isCollapsed) {
    return (
      <div className="w-16 bg-gray-50 border-r border-gray-200 flex flex-col items-center py-4">
        <button
          onClick={onToggleCollapse}
          className="p-2 hover:bg-gray-100 rounded-md mb-4"
          title="Expand sidebar"
        >
          <ChevronRight className="h-5 w-5 text-gray-600" />
        </button>
        
        <button
          onClick={createNewSession}
          className="p-2 hover:bg-gray-100 rounded-md mb-4"
          title="New chat"
        >
          <Plus className="h-5 w-5 text-gray-600" />
        </button>

        <div className="flex flex-col space-y-2">
          {sessions.slice(0, 5).map((session) => (
            <button
              key={session.id}
              onClick={() => onSelectSession(session.id)}
              className={`p-2 rounded-md transition-colors ${
                currentSessionId === session.id
                  ? 'bg-indigo-100 text-indigo-600'
                  : 'hover:bg-gray-100 text-gray-600'
              }`}
              title={session.session_name}
            >
              <MessageSquare className="h-4 w-4" />
            </button>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="w-80 bg-gray-50 border-r border-gray-200 flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900">Chat History</h2>
          <button
            onClick={onToggleCollapse}
            className="p-1 hover:bg-gray-100 rounded-md"
            title="Collapse sidebar"
          >
            <ChevronRight className="h-4 w-4 text-gray-600 rotate-180" />
          </button>
        </div>
        
        <button
          onClick={createNewSession}
          className="w-full flex items-center justify-center px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition-colors"
        >
          <Plus className="h-4 w-4 mr-2" />
          New Legal Chat
        </button>
      </div>

      {/* User Info */}
      <div className="px-4 py-3 bg-white border-b border-gray-200">
        <div className="flex items-center">
          <div className="w-8 h-8 bg-indigo-100 rounded-full flex items-center justify-center">
            <span className="text-sm font-medium text-indigo-600">
              {user.username.charAt(0).toUpperCase()}
            </span>
          </div>
          <div className="ml-3">
            <p className="text-sm font-medium text-gray-900">{user.username}</p>
            <p className="text-xs text-gray-500">{user.email}</p>
          </div>
        </div>
      </div>

      {/* Sessions List */}
      <div className="flex-1 overflow-y-auto">
        {loading ? (
          <div className="p-4 text-center">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-indigo-600 mx-auto"></div>
            <p className="text-sm text-gray-500 mt-2">Loading chat history...</p>
          </div>
        ) : sessions.length === 0 ? (
          <div className="p-4 text-center">
            <MessageSquare className="h-8 w-8 text-gray-400 mx-auto mb-2" />
            <p className="text-sm text-gray-500">No chat history yet</p>
            <p className="text-xs text-gray-400 mt-1">Start a new conversation to see it here</p>
          </div>
        ) : (
          <div className="p-2">
            {sessions.map((session) => (
              <button
                key={session.id}
                onClick={() => onSelectSession(session.id)}
                className={`w-full p-3 mb-2 text-left rounded-lg transition-colors ${
                  currentSessionId === session.id
                    ? 'bg-indigo-100 border-indigo-200 border'
                    : 'hover:bg-gray-100'
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {session.session_name}
                    </p>
                    {session.topic && (
                      <p className="text-xs text-gray-500 mt-1 truncate">
                        {session.topic}
                      </p>
                    )}
                    <div className="flex items-center mt-2">
                      <Clock className="h-3 w-3 text-gray-400 mr-1" />
                      <span className="text-xs text-gray-400">
                        {formatDate(session.created_at)}
                      </span>
                      {session.query_count > 0 && (
                        <>
                          <span className="text-xs text-gray-300 mx-1">•</span>
                          <span className="text-xs text-gray-400">
                            {session.query_count} messages
                          </span>
                        </>
                      )}
                    </div>
                  </div>
                  
                  {currentSessionId === session.id && (
                    <div className="ml-2">
                      <div className="w-2 h-2 bg-indigo-600 rounded-full"></div>
                    </div>
                  )}
                </div>
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Footer Stats */}
      <div className="p-4 border-t border-gray-200 bg-white">
        <div className="text-xs text-gray-500 space-y-1">
          <div className="flex justify-between">
            <span>Total Conversations:</span>
            <span className="font-medium">{sessions.length}</span>
          </div>
          <div className="flex justify-between">
            <span>This Month:</span>
            <span className="font-medium">
              {sessions.filter(s => {
                const sessionDate = new Date(s.created_at);
                const now = new Date();
                return sessionDate.getMonth() === now.getMonth() && 
                       sessionDate.getFullYear() === now.getFullYear();
              }).length}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatHistory;