"""
Notion API wrapper for lead generation pipeline.
"""

import os
from typing import List, Dict, Optional
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

class NotionLeadManager:
    def __init__(self):
        self.client = Client(auth=os.getenv("NOTION_TOKEN"))
        self.database_id = os.getenv("NOTION_PROSPECTS_DB_ID")
    
    def create_prospect(self, prospect_data: Dict) -> str:
        """Create a new prospect in the database."""
        properties = self._format_properties(prospect_data)
        
        page = self.client.pages.create(
            parent={"database_id": self.database_id},
            properties=properties
        )
        return page["id"]
    
    def update_prospect(self, page_id: str, updates: Dict) -> bool:
        """Update an existing prospect."""
        properties = self._format_properties(updates)
        
        try:
            self.client.pages.update(
                page_id=page_id,
                properties=properties
            )
            return True
        except Exception as e:
            print(f"Error updating prospect {page_id}: {e}")
            return False
    
    def get_prospects(self, status: Optional[str] = None) -> List[Dict]:
        """Retrieve prospects, optionally filtered by status."""
        filter_criteria = {}
        if status:
            filter_criteria = {
                "property": "Status",
                "select": {"equals": status}
            }
        
        results = self.client.databases.query(
            database_id=self.database_id,
            filter=filter_criteria if status else None
        )
        
        return [self._parse_prospect(page) for page in results["results"]]
    
    def _format_properties(self, data: Dict) -> Dict:
        """Format data for Notion properties."""
        properties = {}
        
        # Map common fields
        field_mapping = {
            "name": ("Name", "title"),
            "company": ("Company", "rich_text"),
            "job_title": ("Job Title", "rich_text"),
            "email": ("Email", "email"),
            "score": ("Score", "number"),
            "status": ("Status", "select"),
            "priority": ("Priority", "select"),
            "source": ("Source", "select"),
            "country": ("Country", "select"),
            "linkedin_url": ("LinkedIn URL", "url"),
            "notes": ("Notes", "rich_text"),
            "last_contact": ("Last Contact", "date"),
            "next_followup": ("Next Follow-up", "date")
        }
        
        for key, (notion_key, notion_type) in field_mapping.items():
            if key in data:
                value = data[key]
                if notion_type == "title":
                    properties[notion_key] = {"title": [{"text": {"content": str(value)}}]}
                elif notion_type == "rich_text":
                    properties[notion_key] = {"rich_text": [{"text": {"content": str(value)}}]}
                elif notion_type == "email":
                    properties[notion_key] = {"email": str(value)}
                elif notion_type == "number":
                    properties[notion_key] = {"number": float(value)}
                elif notion_type == "select":
                    properties[notion_key] = {"select": {"name": str(value)}}
                elif notion_type == "url":
                    properties[notion_key] = {"url": str(value)}
                elif notion_type == "date":
                    properties[notion_key] = {"date": {"start": str(value)}}
        
        return properties
    
    def _parse_prospect(self, page: Dict) -> Dict:
        """Parse Notion page into prospect data."""
        props = page["properties"]
        
        return {
            "id": page["id"],
            "name": self._get_text(props.get("Name")),
            "company": self._get_text(props.get("Company")),
            "job_title": self._get_text(props.get("Job Title")),
            "email": props.get("Email", {}).get("email"),
            "score": props.get("Score", {}).get("number"),
            "status": self._get_select(props.get("Status")),
            "priority": self._get_select(props.get("Priority")),
            "source": self._get_select(props.get("Source")),
            "country": self._get_select(props.get("Country")),
            "linkedin_url": props.get("LinkedIn URL", {}).get("url"),
            "notes": self._get_text(props.get("Notes")),
            "created": props.get("Created", {}).get("created_time"),
            "modified": props.get("Modified", {}).get("last_edited_time")
        }
    
    def _get_text(self, prop: Dict) -> str:
        """Extract text from Notion text property."""
        if not prop:
            return ""
        
        if prop["type"] == "title":
            return "".join([t["plain_text"] for t in prop["title"]])
        elif prop["type"] == "rich_text":
            return "".join([t["plain_text"] for t in prop["rich_text"]])
        
        return ""
    
    def _get_select(self, prop: Dict) -> str:
        """Extract value from Notion select property."""
        if not prop or not prop.get("select"):
            return ""
        return prop["select"]["name"]