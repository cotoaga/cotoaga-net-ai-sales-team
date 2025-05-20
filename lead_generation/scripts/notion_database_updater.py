#!/usr/bin/env python3
"""
Updates an existing Notion database with the full prospects schema.
For when you've already created a database but need to add all the properties.
"""

import os

# Add the parent directory to the sys.path to find modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
import json
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

def update_database_schema():
    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    database_id = os.getenv("NOTION_PROSPECTS_DB_ID")
    
    if not database_id:
        print("❌ NOTION_PROSPECTS_DB_ID not found in .env")
        print("Please add your database ID to the .env file")
        return
    
    # Define all the properties we want to add
    new_properties = {
        "Company": {
            "type": "rich_text",
            "rich_text": {}
        },
        "Job Title": {
            "type": "rich_text", 
            "rich_text": {}
        },
        "Email": {
            "type": "email",
            "email": {}
        },
        "Score": {
            "type": "number",
            "number": {
                "format": "number"
            }
        },
        "Status": {
            "type": "select",
            "select": {
                "options": [
                    {"name": "New", "color": "gray"},
                    {"name": "Qualified", "color": "blue"},
                    {"name": "Contacted", "color": "yellow"},
                    {"name": "Responded", "color": "green"},
                    {"name": "Scheduled", "color": "purple"},
                    {"name": "Closed-Won", "color": "green"},
                    {"name": "Closed-Lost", "color": "red"}
                ]
            }
        },
        "Priority": {
            "type": "select",
            "select": {
                "options": [
                    {"name": "VIP", "color": "red"},
                    {"name": "High", "color": "orange"},
                    {"name": "Medium", "color": "yellow"},
                    {"name": "Low", "color": "gray"}
                ]
            }
        },
        "Source": {
            "type": "select",
            "select": {
                "options": [
                    {"name": "macOS Contacts", "color": "blue"},
                    {"name": "LinkedIn", "color": "purple"},
                    {"name": "VIP List", "color": "red"},
                    {"name": "Referral", "color": "green"},
                    {"name": "Website", "color": "brown"},
                    {"name": "Cold Outreach", "color": "pink"}
                ]
            }
        },
        "Country": {
            "type": "select",
            "select": {
                "options": [
                    {"name": "Germany", "color": "yellow"},
                    {"name": "France", "color": "blue"},
                    {"name": "Italy", "color": "green"},
                    {"name": "Netherlands", "color": "orange"},
                    {"name": "Spain", "color": "red"},
                    {"name": "Sweden", "color": "purple"},
                    {"name": "Denmark", "color": "pink"},
                    {"name": "Austria", "color": "brown"},
                    {"name": "Belgium", "color": "gray"},
                    {"name": "Switzerland", "color": "default"}
                ]
            }
        },
        "Industry": {
            "type": "select", 
            "select": {
                "options": [
                    {"name": "Technology", "color": "blue"},
                    {"name": "Financial Services", "color": "green"},
                    {"name": "Healthcare", "color": "red"},
                    {"name": "Manufacturing", "color": "orange"},
                    {"name": "Automotive", "color": "purple"},
                    {"name": "Consulting", "color": "yellow"},
                    {"name": "Government", "color": "gray"},
                    {"name": "Education", "color": "brown"},
                    {"name": "Retail", "color": "pink"},
                    {"name": "Other", "color": "default"}
                ]
            }
        },
        "Company Size": {
            "type": "select",
            "select": {
                "options": [
                    {"name": "1-10", "color": "gray"},
                    {"name": "11-50", "color": "brown"},
                    {"name": "51-100", "color": "orange"},
                    {"name": "101-500", "color": "yellow"},
                    {"name": "501-1000", "color": "green"},
                    {"name": "1001-5000", "color": "blue"},
                    {"name": "5000+", "color": "purple"}
                ]
            }
        },
        "Last Contact": {
            "type": "date",
            "date": {}
        },
        "Next Follow-up": {
            "type": "date", 
            "date": {}
        },
        "LinkedIn URL": {
            "type": "url",
            "url": {}
        },
        "Company Website": {
            "type": "url",
            "url": {}
        },
        "Phone": {
            "type": "phone_number",
            "phone_number": {}
        },
        "Email Opens": {
            "type": "number",
            "number": {"format": "number"}
        },
        "Email Clicks": {
            "type": "number", 
            "number": {"format": "number"}
        },
        "Email Responses": {
            "type": "checkbox",
            "checkbox": {}
        },
        "Meeting Scheduled": {
            "type": "checkbox",
            "checkbox": {}
        },
        "Workshop Interest": {
            "type": "multi_select",
            "multi_select": {
                "options": [
                    {"name": "EU AI Act Fundamentals", "color": "blue"},
                    {"name": "Risk Assessment Workshop", "color": "red"},
                    {"name": "Implementation Planning", "color": "green"},
                    {"name": "Executive Briefing", "color": "purple"},
                    {"name": "Technical Deep Dive", "color": "orange"}
                ]
            }
        },
        "Pain Points": {
            "type": "multi_select",
            "multi_select": {
                "options": [
                    {"name": "GDPR Complexity", "color": "red"},
                    {"name": "AI Ethics Concerns", "color": "orange"},
                    {"name": "Resource Constraints", "color": "yellow"},
                    {"name": "Technical Implementation", "color": "green"},
                    {"name": "Regulatory Confusion", "color": "blue"},
                    {"name": "Risk Assessment", "color": "purple"},
                    {"name": "Documentation Requirements", "color": "pink"},
                    {"name": "Board Pressure", "color": "gray"}
                ]
            }
        },
        "Notes": {
            "type": "rich_text",
            "rich_text": {}
        },
        "Internal Notes": {
            "type": "rich_text",
            "rich_text": {}
        },
        "Tags": {
            "type": "multi_select",
            "multi_select": {
                "options": [
                    {"name": "Hot Lead", "color": "red"},
                    {"name": "Decision Maker", "color": "green"},
                    {"name": "Influencer", "color": "blue"},
                    {"name": "Budget Holder", "color": "purple"},
                    {"name": "Technical Contact", "color": "orange"},
                    {"name": "Gatekeeper", "color": "gray"}
                ]
            }
        }
    }
    
    try:
        print("🔍 Updating database schema...")
        
        # Update the database with new properties
        response = notion.databases.update(
            database_id=database_id,
            properties=new_properties
        )
        
        print("✅ Database schema updated successfully!")
        print(f"Database: {response['title'][0]['plain_text']}")
        print(f"Total properties: {len(response['properties'])}")
        
        # List all properties for confirmation
        print("\n📋 Properties added:")
        for prop_name in new_properties.keys():
            print(f"  ✓ {prop_name}")
            
        print(f"\n🔗 Database URL: https://notion.so/{database_id.replace('-', '')}")
        
    except Exception as e:
        print(f"❌ Error updating database: {e}")
        print("\nMake sure:")
        print("1. Your integration has write access to the database")
        print("2. The database ID in .env is correct")

def test_database_access():
    """Test that we can read and write to the updated database."""
    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    database_id = os.getenv("NOTION_PROSPECTS_DB_ID")
    
    try:
        print("\n🔍 Testing database access...")
        
        # Create a test prospect
        test_page = notion.pages.create(
            parent={"database_id": database_id},
            properties={
                "Name": {
                    "title": [{"text": {"content": "Test Prospect - Kurt's AI Sales Team"}}]
                },
                "Company": {
                    "rich_text": [{"text": {"content": "ACME Corp"}}]
                },
                "Job Title": {
                    "rich_text": [{"text": {"content": "Chief AI Officer"}}]
                },
                "Email": {
                    "email": "test@acme.com"
                },
                "Score": {
                    "number": 85
                },
                "Status": {
                    "select": {"name": "New"}
                },
                "Priority": {
                    "select": {"name": "High"}
                },
                "Source": {
                    "select": {"name": "VIP List"}
                },
                "Country": {
                    "select": {"name": "Germany"}
                },
                "Industry": {
                    "select": {"name": "Technology"}
                },
                "Company Size": {
                    "select": {"name": "501-1000"}
                },
                "Workshop Interest": {
                    "multi_select": [
                        {"name": "EU AI Act Fundamentals"},
                        {"name": "Risk Assessment Workshop"}
                    ]
                },
                "Pain Points": {
                    "multi_select": [
                        {"name": "Regulatory Confusion"},
                        {"name": "Technical Implementation"}
                    ]
                },
                "Tags": {
                    "multi_select": [
                        {"name": "Decision Maker"},
                        {"name": "Hot Lead"}
                    ]
                },
                "Notes": {
                    "rich_text": [{"text": {"content": "Test prospect created by setup script. Safe to delete."}}]
                }
            }
        )
        
        print(f"✅ Test prospect created: {test_page['id']}")
        
        # Read it back to confirm
        retrieved = notion.pages.retrieve(page_id=test_page['id'])
        print("✅ Test prospect retrieved successfully")
        
        # Archive the test entry (don't delete, just archive)
        notion.pages.update(
            page_id=test_page['id'],
            archived=True
        )
        print("✅ Test prospect archived")
        
        print("\n🎉 Database is ready for lead generation!")
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Check if we have the database ID
    database_id = os.getenv("NOTION_PROSPECTS_DB_ID")
    
    if not database_id:
        print("❌ NOTION_PROSPECTS_DB_ID not found in .env")
        print("Please make sure your .env file contains:")
        print("NOTION_PROSPECTS_DB_ID=your_database_id_here")
        exit(1)
    
    print(f"🎯 Using database ID: {database_id}")
    
    # Now update the schema
    update_database_schema()
    
    # Test the database
    test_database_access()