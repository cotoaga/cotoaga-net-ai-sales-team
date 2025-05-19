#!/usr/bin/env python3
"""
Guinea Pig Test: Read back a contact from Notion to verify our data pipeline.
"""

import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

def find_guinea_pig():
    """Find and display our guinea pig contact."""
    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    database_id = os.getenv("NOTION_PROSPECTS_DB_ID")
    
    try:
        # Search for guinea pig
        print("🔍 Searching for Mr. Guine Pig...")
        
        results = notion.databases.query(
            database_id=database_id,
            filter={
                "property": "Name",
                "title": {
                    "contains": "Guine"
                }
            }
        )
        
        if not results["results"]:
            print("❌ Guinea pig not found! Make sure you've created him in Notion.")
            return None
        
        guinea_pig = results["results"][0]
        
        # Parse all properties
        props = guinea_pig["properties"]
        
        print("🐹 GUINEA PIG DISCOVERED!")
        print("=" * 40)
        
        # Required fields from macOS contacts
        print("📱 macOS Contact Fields:")
        print(f"  Name: {get_title(props.get('Name'))}")
        print(f"  Company: {get_rich_text(props.get('Company'))}")
        print(f"  Job Title: {get_rich_text(props.get('Job Title'))}")
        print(f"  Email: {props.get('Email', {}).get('email', 'N/A')}")
        print(f"  Phone: {props.get('Phone', {}).get('phone_number', 'N/A')}")
        print(f"  Notes: {get_rich_text(props.get('Notes'))}")
        
        # Lead generation fields (won't be in macOS)
        print("\n🚀 Lead Gen Enhancement Fields:")
        print(f"  Processing Stage: {get_select(props.get('Processing Stage'))}")
        print(f"  Source: {get_select(props.get('Source'))}")
        print(f"  Status: {get_select(props.get('Status'))}")
        print(f"  Priority: {get_select(props.get('Priority'))}")
        print(f"  Country: {get_select(props.get('Country'))}")
        print(f"  Industry: {get_select(props.get('Industry'))}")
        print(f"  Company Size: {get_select(props.get('Company Size'))}")
        print(f"  LinkedIn URL: {props.get('LinkedIn URL', {}).get('url', 'N/A')}")
        
        # Multi-select fields
        print(f"  Workshop Interest: {get_multi_select(props.get('Workshop Interest'))}")
        print(f"  Pain Points: {get_multi_select(props.get('Pain Points'))}")
        print(f"  Tags: {get_multi_select(props.get('Tags'))}")
        
        print(f"\n📝 Internal Notes: {get_rich_text(props.get('Internal Notes'))}")
        
        return guinea_pig
        
    except Exception as e:
        print(f"❌ Error finding guinea pig: {e}")
        return None

def get_title(prop):
    """Extract title text."""
    if not prop or not prop.get("title"):
        return ""
    return "".join([t["plain_text"] for t in prop["title"]])

def get_rich_text(prop):
    """Extract rich text."""
    if not prop or not prop.get("rich_text"):
        return ""
    return "".join([t["plain_text"] for t in prop["rich_text"]])

def get_select(prop):
    """Extract select value."""
    if not prop or not prop.get("select"):
        return "N/A"
    return prop["select"]["name"]

def get_multi_select(prop):
    """Extract multi-select values."""
    if not prop or not prop.get("multi_select"):
        return "N/A"
    return ", ".join([opt["name"] for opt in prop["multi_select"]])

def test_update_guinea_pig(guinea_pig_id):
    """Test updating the guinea pig's properties."""
    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    
    print("\n🧪 Testing update capabilities...")
    
    try:
        # Update some properties
        notion.pages.update(
            page_id=guinea_pig_id,
            properties={
                "Processing Stage": {"select": {"name": "Basic Cleaning"}},
                "Score": {"number": 42},
                "Internal Notes": {
                    "rich_text": [{"text": {"content": "Updated by guinea pig test script!"}}]
                }
            }
        )
        
        print("✅ Successfully updated guinea pig!")
        print("  - Processing Stage → Basic Cleaning")
        print("  - Score → 42")
        print("  - Internal Notes → Updated")
        
    except Exception as e:
        print(f"❌ Update test failed: {e}")

def plan_macos_extraction():
    """Plan the macOS contact extraction based on guinea pig test."""
    print("\n" + "=" * 50)
    print("📋 EXTRACTION PLAN BASED ON GUINEA PIG TEST")
    print("=" * 50)
    
    print("\n✅ Fields we CAN extract from macOS:")
    print("  • Name (First + Last)")
    print("  • Company/Organization")  
    print("  • Job Title")
    print("  • Email Address")
    print("  • Phone Number")
    print("  • Notes")
    
    print("\n🚀 Fields we'll ADD during processing:")
    print("  • Processing Stage: 'Raw Import'")
    print("  • Source: 'macOS Contacts'")
    print("  • Status: 'New'")
    print("  • Priority: 'Low' (until scored)")
    print("  • Score: Blank (until AI scoring)")
    
    print("\n🔄 Fields for FUTURE enrichment:")
    print("  • Country (detect from phone/email)")
    print("  • Industry (LinkedIn scraping)")
    print("  • Company Size (LinkedIn/web research)")
    print("  • LinkedIn URL (search + match)")
    print("  • Workshop Interest (AI analysis of notes)")
    print("  • Pain Points (AI analysis of context)")
    
    print("\n🎯 RECOMMENDED APPROACH:")
    print("1. Extract basic fields from macOS")
    print("2. Import as 'Raw Import' stage")
    print("3. Build enrichment pipeline to fill gaps")
    print("4. Progressive enhancement through processing stages")

if __name__ == "__main__":
    print("🐹 GUINEA PIG PIPELINE TEST")
    print("=" * 40)
    
    guinea_pig = find_guinea_pig()
    
    if guinea_pig:
        test_update_guinea_pig(guinea_pig["id"])
        plan_macos_extraction()
        
        print("\n🎉 Guinea pig test complete!")
        print("Pipeline is ready for macOS contact extraction.")
    else:
        print("\n❌ Guinea pig test failed.")
        print("Create guinea pig in Notion first, then re-run test.")