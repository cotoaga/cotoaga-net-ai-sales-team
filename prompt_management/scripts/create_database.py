#!/usr/bin/env python3
"""
Create a new Notion database for KHAOS prompts
Run this once to set up a brand new database
"""

import os
import sys
import re
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

def create_prompts_database():
    """Create a new Notion database for KHAOS prompts and return the database ID"""
    database_id = None
    # Check for required environment variables
    notion_token = os.getenv("PROMPT_SECURITY_TOKEN")
    
    if not notion_token:
        print("❌ Missing environment variables.")
        print("Please ensure PROMPT_SECURITY_TOKEN is set in .env")
        sys.exit(1)
    
    # Check for parent page ID in environment or ask for it
    parent_page_id = os.getenv("NOTION_PARENT_PAGE_ID")
    if not parent_page_id:
        try:
            parent_page_id = input("Enter Notion parent page ID to create the database in: ")
            if not parent_page_id:
                print("❌ Parent page ID is required.")
                return None
        except EOFError:
            print("❌ Cannot create database: Parent page ID required but not provided in environment")
            print("Please set NOTION_PARENT_PAGE_ID in your .env file")
            return None
        
    # Check if PROMPT_DATABASE_ID already exists
    existing_prompts_db = os.getenv("PROMPT_DATABASE_ID")
    if existing_prompts_db:
        print("⚠️ PROMPT_DATABASE_ID is already set in your .env file.")
        try:
            confirm = input("Do you still want to create a new prompts database? (y/n): ")
            if confirm.lower() != 'y':
                print("Operation cancelled.")
                return None
        except EOFError:
            # In non-interactive mode, don't replace existing DB
            print("Operation cancelled in non-interactive mode.")
            return existing_prompts_db
    
    # Initialize Notion client
    notion = Client(auth=notion_token)
    
    # Basic properties for the database
    initial_properties = {
        "Prompt ID": {
            "title": {}
        },
        "Version": {
            "rich_text": {}
        },
        "Type": {
            "select": {
                "options": [
                    {"name": "meta", "color": "red"},
                    {"name": "consultation", "color": "blue"},
                    {"name": "workshop", "color": "green"},
                    {"name": "analysis", "color": "yellow"},
                    {"name": "creation", "color": "purple"},
                    {"name": "viral", "color": "orange"},
                    {"name": "coding-companion", "color": "pink"}
                ]
            }
        },
        "Purpose": {
            "rich_text": {}
        }
    }
    
    try:
        # Create the database
        response = notion.databases.create(
            parent={"page_id": parent_page_id},
            title=[{
                "type": "text",
                "text": {
                    "content": "KHAOS Prompt Library"
                }
            }],
            properties=initial_properties,
            icon={
                "type": "emoji",
                "emoji": "🧠"
            },
            cover={
                "type": "external",
                "external": {
                    "url": "https://images.unsplash.com/photo-1664447972879-5ce98ef76d71"
                }
            }
        )
        
        # Extract the database ID
        database_id = response["id"]
        
        print("✅ Prompt library database created successfully!")
        print(f"Database ID: {database_id}")
        print("\nUpdating .env file with new database ID...")
        
        # Update the .env file with the new database ID
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
        updated_env_content = ""
        
        try:
            with open(env_path, 'r') as env_file:
                env_content = env_file.read()
                if "PROMPT_DATABASE_ID=" in env_content:
                    # Replace existing database ID
                    updated_env_content = re.sub(
                        r'PROMPT_DATABASE_ID=.*\n', 
                        f'PROMPT_DATABASE_ID={database_id}\n', 
                        env_content
                    )
                else:
                    # Add new database ID under the prompt management section
                    updated_env_content = env_content.replace(
                        "# NOTION AI DB PROMPT MANAGEMENT SYSTEM\n# ==============================================\n", 
                        "# NOTION AI DB PROMPT MANAGEMENT SYSTEM\n# ==============================================\nPROMPT_DATABASE_ID={database_id}\n"
                    )
                    
            with open(env_path, 'w') as env_file:
                env_file.write(updated_env_content)
                print("✅ Updated .env file with new database ID")
        except Exception as e:
            print(f"❌ Error updating .env file: {e}")
            print("\nPlease manually add this to your .env file:")
            print(f"PROMPT_DATABASE_ID={database_id}")
        
        # Now create an initial page with instructions
        notion.pages.create(
            parent={"database_id": database_id},
            properties={
                "Prompt ID": {
                    "title": [{"text": {"content": "khaos-meta-template"}}]
                },
                "Version": {
                    "rich_text": [{"text": {"content": "1.0.0"}}]
                },
                "Type": {
                    "select": {"name": "meta"}
                },
                "Purpose": {
                    "rich_text": [{"text": {"content": "The meta-template for all KHAOS prompts"}}]
                }
            },
            children=[
                {
                    "object": "block",
                    "heading_1": {
                        "rich_text": [{"text": {"content": "KHAOS Prompt Library"}}]
                    }
                },
                {
                    "object": "block",
                    "paragraph": {
                        "rich_text": [{"text": {"content": "Welcome to your Prompt Library. This database stores all your KHAOS prompts in a structured format."}}]
                    }
                },
                {
                    "object": "block",
                    "paragraph": {
                        "rich_text": [{"text": {"content": "Use the CLI tools to manage your prompts:"}}]
                    }
                },
                {
                    "object": "block",
                    "code": {
                        "rich_text": [{"text": {"content": "# List all prompts\npython prompt_cli.py list\n\n# Create a new prompt\npython prompt_cli.py create prompts/khaos-new-prompt.txt\n\n# Read a prompt\npython prompt_cli.py read khaos-meta-template"}}],
                        "language": "bash"
                    }
                }
            ]
        )
        
        print("\n🎯 Created example page in the database")
        print(f"\nView your database at: https://notion.so/{database_id.replace('-', '')}")
        return database_id
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return None

if __name__ == "__main__":
    db_id = create_prompts_database()
    if not db_id:
        sys.exit(1)
