#!/usr/bin/env python3
"""
Database Explorer for LegalGPT
View database structure and data
"""

import sqlite3
import pandas as pd
from datetime import datetime
import os

def explore_database():
    """Explore the LegalGPT database structure and contents"""
    
    # Database file path
    db_path = "legal_ai_database.db"
    
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        return
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 LegalGPT Database Explorer")
        print("=" * 50)
        
        # 1. Show all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"\n📋 Database Tables ({len(tables)} total):")
        for table in tables:
            print(f"  • {table[0]}")
        
        print("\n" + "=" * 50)
        
        # 2. Show table structures and data
        for table in tables:
            table_name = table[0]
            print(f"\n🏷️  TABLE: {table_name}")
            print("-" * 30)
            
            # Get table structure
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            print("📊 Structure:")
            for col in columns:
                col_name, col_type = col[1], col[2]
                is_pk = " (PRIMARY KEY)" if col[5] else ""
                print(f"  • {col_name}: {col_type}{is_pk}")
            
            # Count records
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"📈 Records: {count}")
            
            # Show sample data (first 3 records)
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3;")
                records = cursor.fetchall()
                
                print("🔍 Sample Data:")
                col_names = [desc[1] for desc in columns]
                
                for i, record in enumerate(records, 1):
                    print(f"  Record {i}:")
                    for j, value in enumerate(record):
                        # Truncate long values
                        display_value = str(value)
                        if len(display_value) > 50:
                            display_value = display_value[:47] + "..."
                        print(f"    {col_names[j]}: {display_value}")
                    print()
            
            print("-" * 30)
        
        # 3. Show relationship summary
        print(f"\n🔗 Key Relationships:")
        print("  • Users → ChatSessions (1-to-many)")
        print("  • ChatSessions → LegalQueries (1-to-many)")
        print("  • Users → UserFeedback (1-to-many)")
        print("  • LegalDocuments (standalone reference)")
        print("  • SystemAnalytics (global metrics)")
        
        conn.close()
        print(f"\n✅ Database exploration completed!")
        
    except Exception as e:
        print(f"❌ Error exploring database: {e}")

def show_recent_activity():
    """Show recent chat activity"""
    
    db_path = "legal_ai_database.db"
    
    try:
        conn = sqlite3.connect(db_path)
        
        print(f"\n📈 Recent Activity Summary")
        print("=" * 40)
        
        # Recent queries
        query = '''
        SELECT u.username, lq.query_text, lq.query_category, lq.created_at
        FROM legal_queries lq
        JOIN users u ON lq.user_id = u.id
        ORDER BY lq.created_at DESC
        LIMIT 5
        '''
        
        df = pd.read_sql_query(query, conn)
        
        if not df.empty:
            print("🕒 Recent Legal Questions:")
            for _, row in df.iterrows():
                query_text = row['query_text'][:60] + "..." if len(row['query_text']) > 60 else row['query_text']
                print(f"  • {row['username']}: '{query_text}' ({row['query_category']})")
        else:
            print("No queries found yet.")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error showing activity: {e}")

if __name__ == "__main__":
    print("🚀 Starting Database Explorer...")
    explore_database()
    show_recent_activity()