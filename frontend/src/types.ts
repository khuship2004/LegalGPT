export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  sources?: Source[];
  isError?: boolean;
}

export interface Source {
  title: string;
  content: string;
  source: string;
  section: string;
  url?: string;
  similarity_score?: number;
}

export interface ChatResponse {
  message: string;
  conversation_id: string;
  sources: Source[];
  disclaimer: string;
}