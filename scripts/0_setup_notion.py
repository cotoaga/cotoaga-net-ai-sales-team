#!/usr/bin/env python3
"""
Initial Notion setup script.
Creates the prospects database and configures properties.
"""

import os
import json
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

def create_prospects_database():
    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    
    # Load schema from config
    with open("config/notion_schema.json", "r") as f:
        schema = json.load(f)
    
    try:
        # Create database
        database = notion.databases.create(
            parent={"type": "page_id", "page_id": os.getenv("NOTION_PARENT_PAGE_ID")},
            title=[{"type": "text", "text": {"content": schema["title"]}}],
            properties=schema["properties"]
        )
        
        database_id = database["id"]
        print(f"✅ Database created successfully!")
        print(f"Database ID: {database_id}")
        print(f"URL: https://notion.so/{database_id.replace('-', '')}")
        
        # Update .env file with database ID
        env_file = ".env"
        with open(env_file, "r") as f:
            env_content = f.read()
        
        if "NOTION_PROSPECTS_DB_ID=" in env_content:
            # Replace existing line
            lines = env_content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith("NOTION_PROSPECTS_DB_ID="):
                    lines[i] = f"NOTION_PROSPECTS_DB_ID={database_id}"
                    break
            env_content = '\n'.join(lines)
        else:
            # Add new line
            env_content += f"\nNOTION_PROSPECTS_DB_ID={database_id}\n"
        
        with open(env_file, "w") as f:
            f.write(env_content)
        
        print("✅ .env file updated with database ID")
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        print("Make sure you have:")
        print("1. Valid NOTION_TOKEN in .env")
        print("2. NOTION_PARENT_PAGE_ID (the page where database will be created)")

if __name__ == "__main__":
    create_prospects_database()