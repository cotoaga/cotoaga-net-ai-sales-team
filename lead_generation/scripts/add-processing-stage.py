#!/usr/bin/env python3
"""
Add Processing Stage property to track contact refinement levels.
From raw imports to AI-enhanced prospects.
"""

import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

def add_processing_stage_property():
    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    database_id = os.getenv("NOTION_PROSPECTS_DB_ID")
    
    # Define the new Processing Stage property
    processing_stage_property = {
        "Processing Stage": {
            "type": "select",
            "select": {
                "options": [
                    {"name": "Raw Import", "color": "red"},
                    {"name": "Basic Cleaning", "color": "orange"},
                    {"name": "LinkedIn Enriched", "color": "yellow"},
                    {"name": "AI Scored", "color": "green"},
                    {"name": "Personalized", "color": "blue"},
                    {"name": "Campaign Ready", "color": "purple"},
                    {"name": "Contacted", "color": "gray"}
                ]
            }
        }
    }
    
    try:
        print("🔄 Adding Processing Stage property...")
        
        # Update the database with the new property
        response = notion.databases.update(
            database_id=database_id,
            properties=processing_stage_property
        )
        
        print("✅ Processing Stage property added!")
        print("📋 Processing stages available:")
        for option in processing_stage_property["Processing Stage"]["select"]["options"]:
            print(f"  🔸 {option['name']} ({option['color']})")
            
        return True
        
    except Exception as e:
        print(f"❌ Error adding property: {e}")
        return False

def test_processing_stages():
    """Create test prospects at different processing stages."""
    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    database_id = os.getenv("NOTION_PROSPECTS_DB_ID")
    
    test_prospects = [
        {
            "name": "Raw Contact Test",
            "stage": "Raw Import",
            "company": "Unknown Corp",
            "notes": "Imported from macOS contacts - needs processing"
        },
        {
            "name": "Enriched Contact Test", 
            "stage": "LinkedIn Enriched",
            "company": "TechCorp GmbH",
            "job_title": "CTO",
            "score": 75,
            "notes": "LinkedIn data enriched, ready for AI scoring"
        },
        {
            "name": "Campaign Ready Test",
            "stage": "Campaign Ready", 
            "company": "AI Solutions AG",
            "job_title": "Head of AI Ethics",
            "score": 95,
            "status": "Qualified",
            "priority": "High",
            "notes": "Fully processed, personalized content ready"
        }
    ]
    
    try:
        print("\n🧪 Creating test prospects at different stages...")
        
        for prospect in test_prospects:
            # Build properties dict, skipping None values
            properties = {
                "Name": {"title": [{"text": {"content": prospect["name"]}}]},
                "Processing Stage": {"select": {"name": prospect["stage"]}},
                "Company": {"rich_text": [{"text": {"content": prospect["company"]}}]},
                "Status": {"select": {"name": prospect.get("status", "New")}},
                "Priority": {"select": {"name": prospect.get("priority", "Medium")}},
                "Source": {"select": {"name": "VIP List"}},
                "Notes": {"rich_text": [{"text": {"content": prospect["notes"]}}]}
            }
            
            # Add optional fields only if they have values
            if prospect.get("job_title"):
                properties["Job Title"] = {"rich_text": [{"text": {"content": prospect["job_title"]}}]}
                
            if prospect.get("score") is not None:
                properties["Score"] = {"number": prospect["score"]}
            
            page = notion.pages.create(
                parent={"database_id": database_id},
                properties=properties
            )
            print(f"  ✅ Created: {prospect['name']} - {prospect['stage']}")
        
        print("\n🎯 Test prospects created! Check your database to see the processing stages in action.")
        
    except Exception as e:
        print(f"❌ Error creating test prospects: {e}")

if __name__ == "__main__":
    print("🚀 FUSION REACTOR: Adding Processing Stage Tracking")
    print("=" * 50)
    
    # Add the processing stage property
    if add_processing_stage_property():
        # Create test examples
        test_processing_stages()
        
        print("\n" + "=" * 50)
        print("🎉 FUSION REACTOR ONLINE!")
        print("Your database can now track contact refinement from raw dirt to pure prospect gold!")
        print("\nProcessing Pipeline:")
        print("Raw Import → Basic Cleaning → LinkedIn Enriched → AI Scored → Personalized → Campaign Ready → Contacted")
    else:
        print("🚨 Fusion reactor startup failed. Check your Notion connection.")