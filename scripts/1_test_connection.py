#!/usr/bin/env python3
"""
Test Notion connection and basic operations.
"""

import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

def test_notion_connection():
    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    
    try:
        # Test 1: List databases to verify connection
        print("🔍 Testing Notion connection...")
        databases = notion.search(filter={"property": "object", "value": "database"})
        print(f"✅ Connection successful! Found {len(databases['results'])} databases")
        
        # Test 2: Check if prospects database exists
        db_id = os.getenv("NOTION_PROSPECTS_DB_ID")
        if db_id:
            print(f"🔍 Testing prospects database access...")
            database = notion.databases.retrieve(database_id=db_id)
            print(f"✅ Prospects database found: {database['title'][0]['plain_text']}")
            
            # Test 3: Create a test entry
            print("🔍 Testing database write access...")
            test_page = notion.pages.create(
                parent={"database_id": db_id},
                properties={
                    "Name": {"title": [{"text": {"content": "Test Prospect"}}]},
                    "Company": {"rich_text": [{"text": {"content": "Test Company"}}]},
                    "Score": {"number": 85},
                    "Status": {"select": {"name": "New"}},
                    "Priority": {"select": {"name": "Medium"}},
                    "Source": {"select": {"name": "VIP List"}}
                }
            )
            print(f"✅ Test entry created: {test_page['id']}")
            
            # Test 4: Read the entry back
            print("🔍 Testing database read access...")
            retrieved = notion.pages.retrieve(page_id=test_page['id'])
            print(f"✅ Test entry retrieved successfully")
            
            # Test 5: Clean up test entry
            notion.pages.update(
                page_id=test_page['id'],
                archived=True
            )
            print("✅ Test entry archived/cleaned up")
            
        else:
            print("⚠️  NOTION_PROSPECTS_DB_ID not found in .env")
            print("Run 0_setup_notion.py first to create the database")
            
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        print("Check your NOTION_TOKEN in .env file")

if __name__ == "__main__":
    test_notion_connection()