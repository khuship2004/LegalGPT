import requests
import json
import sqlite3
import os
from typing import List, Dict, Any
import asyncio
from datetime import datetime

class LegalDataService:
    """Service for fetching and storing legal data from external APIs and sources"""
    
    def __init__(self):
        self.db_path = "legal_database.db"
        self.initialize_database()
        
    def initialize_database(self):
        """Initialize SQLite database for storing legal documents"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS legal_documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                source TEXT NOT NULL,
                section TEXT NOT NULL,
                category TEXT NOT NULL,
                keywords TEXT NOT NULL,
                url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                base_url TEXT NOT NULL,
                api_key TEXT,
                last_sync TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                response TEXT,
                sources_used TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                response_time_ms INTEGER
            )
        ''')
        
        conn.commit()
        conn.close()
        
    async def fetch_from_india_code_api(self):
        """Fetch legal documents from India Code API (if available)"""
        try:
            # This is a hypothetical API - India Code doesn't have a public API yet
            # But this shows how you would integrate real APIs
            
            base_url = "https://api.indiacode.nic.in"  # Hypothetical
            
            acts_to_fetch = [
                "constitution-of-india",
                "indian-penal-code-1860", 
                "indian-contract-act-1872",
                "consumer-protection-act-2019",
                "companies-act-2013",
                "motor-vehicles-act-1988"
            ]
            
            documents = []
            
            for act in acts_to_fetch:
                # Simulated API call structure
                response = await self._make_api_request(f"{base_url}/acts/{act}")
                if response:
                    documents.extend(self._parse_legal_document(response, act))
            
            return documents
            
        except Exception as e:
            print(f"Error fetching from India Code API: {e}")
            return []
    
    async def fetch_from_legislative_assembly_apis(self):
        """Fetch from state legislative assembly APIs"""
        try:
            # Example: Some states have APIs for their legislative documents
            state_apis = [
                {"state": "Maharashtra", "url": "https://api.maharashtra.gov.in/legislative"},
                {"state": "Karnataka", "url": "https://api.karnataka.gov.in/acts"},
                # Add more states as they become available
            ]
            
            documents = []
            
            for state_api in state_apis:
                response = await self._make_api_request(state_api["url"])
                if response:
                    docs = self._parse_state_documents(response, state_api["state"])
                    documents.extend(docs)
            
            return documents
            
        except Exception as e:
            print(f"Error fetching from state APIs: {e}")
            return []
    
    async def fetch_from_supreme_court_api(self):
        """Fetch judgments from Supreme Court API"""
        try:
            # Supreme Court of India has some digital initiatives
            # This is how you'd integrate when APIs become available
            
            api_url = "https://api.sci.gov.in/judgments"  # Hypothetical
            
            # Fetch recent important judgments
            params = {
                "category": "constitutional",
                "limit": 100,
                "date_from": "2020-01-01"
            }
            
            response = await self._make_api_request(api_url, params)
            
            if response:
                return self._parse_court_judgments(response)
            
            return []
            
        except Exception as e:
            print(f"Error fetching Supreme Court data: {e}")
            return []
    
    async def _make_api_request(self, url: str, params: Dict = None) -> Dict:
        """Make HTTP API request with proper error handling"""
        try:
            # In a real implementation, you'd use aiohttp for async requests
            # For now, this is a placeholder that returns None (API not available)
            print(f"API call to: {url}")
            return None  # APIs not available yet
            
        except Exception as e:
            print(f"API request failed: {e}")
            return None
    
    def _parse_legal_document(self, api_response: Dict, act_name: str) -> List[Dict]:
        """Parse legal document from API response"""
        # This would parse the actual API response format
        documents = []
        
        # Example parsing logic (would depend on actual API format)
        if api_response and "sections" in api_response:
            for section in api_response["sections"]:
                doc = {
                    "title": f"{act_name} - {section['number']}",
                    "content": section["text"],
                    "source": act_name,
                    "section": section["number"],
                    "category": section.get("category", "General"),
                    "keywords": section.get("keywords", []),
                    "url": section.get("official_url", "")
                }
                documents.append(doc)
        
        return documents
    
    def _parse_state_documents(self, api_response: Dict, state: str) -> List[Dict]:
        """Parse state legislative documents"""
        documents = []
        
        # Parse state-specific legal documents
        # Implementation would depend on state API format
        
        return documents
    
    def _parse_court_judgments(self, api_response: Dict) -> List[Dict]:
        """Parse Supreme Court judgments"""
        documents = []
        
        # Parse court judgments into searchable format
        # Implementation would depend on court API format
        
        return documents
    
    def store_documents(self, documents: List[Dict]):
        """Store documents in SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for doc in documents:
            cursor.execute('''
                INSERT OR REPLACE INTO legal_documents 
                (title, content, source, section, category, keywords, url)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                doc["title"],
                doc["content"],
                doc["source"],
                doc["section"],
                doc["category"],
                json.dumps(doc["keywords"]),
                doc.get("url", "")
            ))
        
        conn.commit()
        conn.close()
    
    def load_documents_from_db(self) -> List[Dict]:
        """Load all documents from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM legal_documents')
        rows = cursor.fetchall()
        
        documents = []
        for row in rows:
            doc = {
                "id": row[0],
                "title": row[1],
                "content": row[2],
                "source": row[3],
                "section": row[4],
                "category": row[5],
                "keywords": json.loads(row[6]) if row[6] else [],
                "url": row[7],
                "created_at": row[8],
                "updated_at": row[9]
            }
            documents.append(doc)
        
        conn.close()
        return documents
    
    def log_user_query(self, query: str, response: str, sources: List[str], response_time: int):
        """Log user queries for analytics and improvement"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO user_queries (query, response, sources_used, response_time_ms)
            VALUES (?, ?, ?, ?)
        ''', (query, response, json.dumps(sources), response_time))
        
        conn.commit()
        conn.close()
    
    def get_popular_queries(self, limit: int = 10) -> List[Dict]:
        """Get most popular user queries"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT query, COUNT(*) as count 
            FROM user_queries 
            GROUP BY query 
            ORDER BY count DESC 
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [{"query": row[0], "count": row[1]} for row in results]
    
    async def sync_all_sources(self):
        """Sync data from all available API sources"""
        print("Starting sync from external sources...")
        
        all_documents = []
        
        # Fetch from various sources
        india_code_docs = await self.fetch_from_india_code_api()
        state_docs = await self.fetch_from_legislative_assembly_apis()
        court_docs = await self.fetch_from_supreme_court_api()
        
        all_documents.extend(india_code_docs)
        all_documents.extend(state_docs)
        all_documents.extend(court_docs)
        
        if all_documents:
            self.store_documents(all_documents)
            print(f"Synced {len(all_documents)} documents from external sources")
        else:
            print("No external APIs available, using local data")
        
        return len(all_documents)