import React from 'react';
import { BookOpen } from 'lucide-react';
import { Message } from '../types';

interface ChatMessageProps {
  message: Message;
  onSourceClick?: () => void;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message, onSourceClick }) => {
  const isUser = message.role === 'user';
  
  return (
    <div className={`flex mb-4 ${isUser ? 'justify-end' : 'justify-start'} chat-message`}>
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

export default ChatMessage;