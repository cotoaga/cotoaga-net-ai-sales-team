#!/usr/bin/env python3
"""
KHAOS Lead Library CLI
A command-line interface for managing and analyzing leads
"""

import os
import sys
from datetime import datetime
import argparse
from collections import Counter
from dotenv import load_dotenv
from notion_client import Client

# Add the parent directory to the sys.path to find modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

load_dotenv()

class LeadManager:
    """Manager for lead generation database operations"""
    
    def __init__(self):
        self.notion = Client(auth=os.getenv("LEAD_SECURITY_TOKEN"))
        self.database_id = os.getenv("LEAD_DATABASE_ID")
        
        if not self.database_id:
            print("❌ LEAD_DATABASE_ID not found in .env")
            print("Please add your database ID to the .env file")
            return
    
    def get_database_info(self):
        """Get basic information about the database"""
        try:
            db = self.notion.databases.retrieve(database_id=self.database_id)
            return {
                "title": db['title'][0]['plain_text'] if db.get('title') and db['title'] else "Untitled",
                "properties": list(db['properties'].keys())
            }
        except Exception as e:
            print(f"❌ Error retrieving database info: {e}")
            return None
    
    def count_leads_by_stage(self):
        """Count leads in each processing stage"""
        try:
            # Get the database to determine if the Processing Stage property exists
            db = self.notion.databases.retrieve(database_id=self.database_id)
            
            # Check if Processing Stage property exists
            has_stage_property = "Processing Stage" in db['properties']
            
            # Query the database for all entries
            response = self.notion.databases.query(
                database_id=self.database_id,
                page_size=100  # Adjust if you have more than 100 leads
            )
            
            total_count = len(response['results'])
            
            # If Processing Stage doesn't exist, just return total count
            if not has_stage_property:
                return {
                    "total": total_count,
                    "stages": {"Not configured": total_count}
                }
            
            # Count entries by processing stage
            stages = Counter()
            
            for page in response['results']:
                stage_prop = page['properties'].get('Processing Stage', {})
                stage = stage_prop.get('select', {}).get('name') if stage_prop else None
                stages[stage or "Unset"] += 1
            
            return {
                "total": total_count,
                "stages": dict(stages)
            }
        except Exception as e:
            print(f"❌ Error counting leads: {e}")
            return {"total": 0, "stages": {}}

    def count_leads_by_status(self):
        """Count leads in each status category"""
        try:
            # Query the database for all entries
            response = self.notion.databases.query(
                database_id=self.database_id,
                page_size=100
            )
            
            statuses = Counter()
            
            for page in response['results']:
                status_prop = page['properties'].get('Status', {})
                status = status_prop.get('select', {}).get('name') if status_prop else None
                statuses[status or "Unset"] += 1
            
            return dict(statuses)
        except Exception as e:
            print(f"❌ Error counting leads by status: {e}")
            return {}

    def count_leads_by_priority(self):
        """Count leads in each priority level"""
        try:
            response = self.notion.databases.query(
                database_id=self.database_id,
                page_size=100
            )
            
            priorities = Counter()
            
            for page in response['results']:
                priority_prop = page['properties'].get('Priority', {})
                priority = priority_prop.get('select', {}).get('name') if priority_prop else None
                priorities[priority or "Unset"] += 1
            
            return dict(priorities)
        except Exception as e:
            print(f"❌ Error counting leads by priority: {e}")
            return {}
            
    def get_recent_leads(self, limit=5):
        """Get the most recently added leads"""
        try:
            # Query the database for the most recent entries
            response = self.notion.databases.query(
                database_id=self.database_id,
                sorts=[
                    {
                        "timestamp": "created_time",
                        "direction": "descending"
                    }
                ],
                page_size=limit
            )
            
            leads = []
            
            for page in response['results']:
                # Get the title property name 
                title_property_name = None
                for prop_name, prop in page['properties'].items():
                    if prop['type'] == 'title':
                        title_property_name = prop_name
                        break
                
                if not title_property_name:
                    continue
                
                # Extract lead data
                lead_data = {
                    "id": page['id'],
                    "name": page['properties'][title_property_name]['title'][0]['plain_text'] if page['properties'][title_property_name]['title'] else "",
                    "created": page['created_time']
                }
                
                # Add company if available
                if 'Company' in page['properties'] and page['properties']['Company'].get('rich_text'):
                    lead_data["company"] = page['properties']['Company']['rich_text'][0]['plain_text']
                else:
                    lead_data["company"] = ""
                
                # Add processing stage if available
                if 'Processing Stage' in page['properties'] and page['properties']['Processing Stage'].get('select'):
                    lead_data["stage"] = page['properties']['Processing Stage']['select']['name']
                else:
                    lead_data["stage"] = "Unset"
                
                leads.append(lead_data)
            
            return leads
        except Exception as e:
            print(f"❌ Error retrieving recent leads: {e}")
            return []

def show_overview():
    """Show an overview of the leads database"""
    manager = LeadManager()
    
    # Get database info
    db_info = manager.get_database_info()
    if not db_info:
        print("❌ Failed to get database information")
        return
    
    # Get lead counts by stage
    stage_counts = manager.count_leads_by_stage()
    status_counts = manager.count_leads_by_status()
    priority_counts = manager.count_leads_by_priority()
    recent_leads = manager.get_recent_leads(5)  # Get 5 most recent leads
    
    # Print overview
    print("\n" + "=" * 60)
    print(f"📊 KHAOS LEAD GENERATION OVERVIEW - {db_info['title']}")
    print("=" * 60)
    
    print(f"\n📋 Total Leads: {stage_counts['total']}")
    
    # Print processing stage counts
    print("\n🔄 Leads by Processing Stage:")
    print("-" * 40)
    for stage, count in stage_counts['stages'].items():
        print(f"{stage:<20} | {count:>5} | {'█' * min(count, 20)}")
    
    # Print status counts
    if status_counts:
        print("\n📈 Leads by Status:")
        print("-" * 40)
        for status, count in status_counts.items():
            print(f"{status:<20} | {count:>5} | {'█' * min(count, 20)}")
    
    # Print priority counts
    if priority_counts:
        print("\n🔥 Leads by Priority:")
        print("-" * 40)
        for priority, count in priority_counts.items():
            print(f"{priority:<20} | {count:>5} | {'█' * min(count, 20)}")
    
    # Print recent leads
    if recent_leads:
        print("\n🆕 Recently Added Leads:")
        print("-" * 60)
        for lead in recent_leads:
            created = datetime.fromisoformat(lead['created'].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M')
            company = f" ({lead['company']})" if lead['company'] else ""
            stage = f" - {lead['stage']}" if lead['stage'] != "Unset" else ""
            
            print(f"{created} | {lead['name']}{company}{stage}")
    
    print("\n" + "=" * 60)
    print("Generate more leads using the lead generation pipeline:")
    print("Raw Import → Basic Cleaning → LinkedIn Enriched → AI Scored → Personalized → Campaign Ready → Contacted")
    print("=" * 60)

def show_stats_by_field(field):
    """Show statistics for a specific field"""
    manager = LeadManager()
    
    if field.lower() == "stage":
        counts = manager.count_leads_by_stage()
        print("\n🔄 Leads by Processing Stage:")
        print("-" * 40)
        for stage, count in counts['stages'].items():
            print(f"{stage:<20} | {count:>5} | {'█' * min(count, 20)}")
        print(f"\nTotal: {counts['total']} leads")
        
    elif field.lower() == "status":
        counts = manager.count_leads_by_status()
        print("\n📈 Leads by Status:")
        print("-" * 40)
        for status, count in counts.items():
            print(f"{status:<20} | {count:>5} | {'█' * min(count, 20)}")
        
    elif field.lower() == "priority":
        counts = manager.count_leads_by_priority()
        print("\n🔥 Leads by Priority:")
        print("-" * 40)
        for priority, count in counts.items():
            print(f"{priority:<20} | {count:>5} | {'█' * min(count, 20)}")
    
    else:
        print(f"❌ Unknown field: {field}")
        print("Available fields: stage, status, priority")

def show_recent(limit=10):
    """Show most recently added leads"""
    manager = LeadManager()
    recent_leads = manager.get_recent_leads(limit)
    
    if not recent_leads:
        print("❌ No leads found or error retrieving leads")
        return
        
    print("\n🆕 Recently Added Leads:")
    print("-" * 70)
    for lead in recent_leads:
        created = datetime.fromisoformat(lead['created'].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M')
        company = f" ({lead['company']})" if lead['company'] else ""
        stage = f" - {lead['stage']}" if lead['stage'] != "Unset" else ""
        
        print(f"{created} | {lead['name']}{company}{stage}")

def main():
    parser = argparse.ArgumentParser(description="KHAOS Lead Generation Tool")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Overview command (default)
    overview_parser = subparsers.add_parser("overview", help="Show database overview")
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show statistics by field")
    stats_parser.add_argument("field", choices=["stage", "status", "priority"], help="Field to analyze")
    
    # Recent command
    recent_parser = subparsers.add_parser("recent", help="Show recent leads")
    recent_parser.add_argument("--limit", type=int, default=10, help="Number of leads to show")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Check if we're properly configured
    if not os.getenv("LEAD_DATABASE_ID") or not os.getenv("LEAD_SECURITY_TOKEN"):
        print("❌ Error: Lead generation environment variables not set")
        print("Please add the following to your .env file:")
        print("LEAD_SECURITY_TOKEN=your_notion_integration_token")
        print("LEAD_DATABASE_ID=your_prospects_database_id")
        sys.exit(1)
    
    # Execute the appropriate command
    if args.command == "stats" and hasattr(args, "field"):
        show_stats_by_field(args.field)
    elif args.command == "recent":
        show_recent(args.limit)
    else:
        # Default to overview
        show_overview()

if __name__ == "__main__":
    main()