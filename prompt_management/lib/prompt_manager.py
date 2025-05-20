#!/usr/bin/env python3
"""
KHAOS Prompt Manager - CRUD operations for prompt libraries
"""

import os
import sys  # Added this import

# Add the parent directory to the sys.path to find modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
import json
import re
from dotenv import load_dotenv
from notion_client import Client
from datetime import datetime

load_dotenv()

class PromptManager:
    def __init__(self):
        self.notion = Client(auth=os.getenv("PROMPT_SECURITY_TOKEN"))
        self.database_id = os.getenv("PROMPT_DATABASE_ID")
        
        if not self.database_id:
            print("❌ PROMPT_DATABASE_ID not found in .env")
            print("Please add your database ID to the .env file")
            print("Example: PROMPT_DATABASE_ID=bf9c35d5e8a646c7b5476c57a91234ef")
            return
    
    def setup_database(self):
        """Creates or updates the prompt library database schema."""
        # First check if we can access the database
        try:
            db = self.notion.databases.retrieve(database_id=self.database_id)
            print(f"Found existing database: {db['title'][0]['plain_text'] if db.get('title') else 'Untitled'}")
            
            # Check if title property exists and is named correctly
            title_found = False
            for prop_name, prop in db['properties'].items():
                if prop['type'] == 'title':
                    title_found = True
                    if prop_name != "Prompt ID":
                        print(f"Warning: Title property is named '{prop_name}' instead of 'Prompt ID'")
                        print("Note: Title properties cannot be renamed through the API")
                    break
                    
            if not title_found:
                print("❌ Error: Database doesn't have a title property")
                return False
                
        except Exception as e:
            print(f"❌ Error accessing database: {e}")
            print("Please check your PROMPT_SECURITY_TOKEN and PROMPT_DATABASE_ID")
            return False
            
        # Define new properties to add (except title property which can't be modified)
        new_properties = {
            "Version": {
                "type": "rich_text",
                "rich_text": {}
            },
            "Type": {
                "type": "select",
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
                "type": "rich_text",
                "rich_text": {}
            },
            "Core Message": {
                "type": "rich_text", 
                "rich_text": {}
            },
            "Viral Hooks": {
                "type": "multi_select",
                "multi_select": {
                    "options": [
                        {"name": "Schrödinger's Agile", "color": "blue"},
                        {"name": "Complexity Whisperer", "color": "green"},
                        {"name": "AI Act Navigator", "color": "orange"},
                        {"name": "Meme Machine", "color": "red"}
                    ]
                }
            },
            "Models": {
                "type": "multi_select",
                "multi_select": {
                    "options": [
                        {"name": "GPT-4", "color": "green"},
                        {"name": "Claude 3", "color": "blue"},
                        {"name": "Claude 3.7 Sonnet", "color": "purple"},
                        {"name": "Perplexity", "color": "yellow"},
                        {"name": "Grok 3", "color": "orange"},
                        {"name": "Gemini 2.5 Pro", "color": "pink"}
                    ]
                }
            },
            "Creation Date": {
                "type": "date",
                "date": {}
            },
            "Last Modified": {
                "type": "date",
                "date": {}
            },
            "Parent Prompt": {
                "type": "relation",
                "relation": {
                    "database_id": self.database_id,
                    "single_property": {}
                }
            },
            "Temperature": {
                "type": "number",
                "number": {"format": "number"}
            },
            "Personality Intensity": {
                "type": "select",
                "select": {
                    "options": [
                        {"name": "40%", "color": "gray"},
                        {"name": "50%", "color": "blue"},
                        {"name": "60%", "color": "green"},
                        {"name": "70%", "color": "yellow"},
                        {"name": "80%", "color": "red"}
                    ]
                }
            },
            "Security Level": {
                "type": "select",
                "select": {
                    "options": [
                        {"name": "public", "color": "green"},
                        {"name": "client", "color": "blue"},
                        {"name": "private", "color": "orange"},
                        {"name": "classified", "color": "red"}
                    ]
                }
            },
            "Full Prompt": {
                "type": "rich_text",
                "rich_text": {}
            },
            "Usage Contexts": {
                "type": "multi_select",
                "multi_select": {
                    "options": [
                        {"name": "EU AI Act", "color": "blue"},
                        {"name": "Workshops", "color": "green"},
                        {"name": "Coding", "color": "purple"},
                        {"name": "Sales", "color": "yellow"},
                        {"name": "Content Creation", "color": "orange"}
                    ]
                }
            },
            "Tags": {
                "type": "multi_select",
                "multi_select": {
                    "options": []  # Will be populated dynamically
                }
            },
            "Generation": {
                "type": "number",
                "number": {"format": "number"}
            }
        }
        
        try:
            print("🔍 Setting up prompt library database schema...")
            
            # Get current properties 
            db = self.notion.databases.retrieve(database_id=self.database_id)
            current_properties = db.get('properties', {})
            
            # Add only properties that don't exist yet
            properties_to_add = {}
            for prop_name, prop_config in new_properties.items():
                if prop_name not in current_properties:
                    properties_to_add[prop_name] = prop_config
                    print(f"Adding property: {prop_name}")
            
            if not properties_to_add:
                print("✅ All required properties already exist!")
                return True
                
            # Update the database with new properties
            response = self.notion.databases.update(
                database_id=self.database_id,
                properties=properties_to_add
            )
            
            print("✅ Database schema updated successfully!")
            print(f"Database: {response['title'][0]['plain_text'] if response.get('title') else 'Untitled'}")
            print(f"Total properties: {len(response['properties'])}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating database: {e}")
            return False
    
    def parse_prompt_file(self, file_path):
        """Parse a prompt file into structured data."""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Extract key sections using regex
            prompt_data = {}
            
            # Extract basic metadata
            prompt_data['Prompt ID'] = re.search(r'PROMPT_ID:\s*(.+)', content).group(1).strip()
            prompt_data['Version'] = re.search(r'VERSION:\s*(.+)', content).group(1).strip()
            prompt_data['Purpose'] = re.search(r'PURPOSE:\s*(.+)', content).group(1).strip()
            
            # Try to extract other fields, some might be missing
            try:
                prompt_data['Type'] = re.search(r'PROMPT_TYPE:\s*(.+)', content).group(1).strip()
            except:
                prompt_data['Type'] = "meta"  # Default
                
            # Extract date information
            try:
                creation_date = re.search(r'CREATION_DATE:\s*(.+)', content).group(1).strip()
                if creation_date == '@Today':
                    creation_date = datetime.now().strftime('%Y-%m-%d')
                prompt_data['Creation Date'] = creation_date
            except:
                prompt_data['Creation Date'] = datetime.now().strftime('%Y-%m-%d')
                
            try:
                modified_date = re.search(r'LAST_MODIFIED_DATE:\s*(.+)', content).group(1).strip()
                if modified_date.startswith('@'):
                    modified_date = datetime.now().strftime('%Y-%m-%d')
                prompt_data['Last Modified'] = modified_date
            except:
                prompt_data['Last Modified'] = datetime.now().strftime('%Y-%m-%d')
            
            # Extract complex fields
            try:
                models_section = re.search(r'MODELS:\s*(.+)', content).group(1).strip()
                prompt_data['Models'] = [m.strip() for m in models_section.split(',')]
            except:
                prompt_data['Models'] = ["GPT-4", "Claude 3"]
                
            # Store full content
            prompt_data['Full Prompt'] = content
            
            return prompt_data
            
        except Exception as e:
            print(f"❌ Error parsing prompt file: {e}")
            return None
    
    def create_prompt(self, file_path):
        """Create a new prompt in the database from a file."""
        prompt_data = self.parse_prompt_file(file_path)
        
        if not prompt_data:
            return False
        
        try:
            # Get the database to determine the title property name
            db = self.notion.databases.retrieve(database_id=self.database_id)
            title_property_name = None
            
            # Find the title property
            for prop_name, prop in db['properties'].items():
                if prop['type'] == 'title':
                    title_property_name = prop_name
                    break
            
            if not title_property_name:
                print("❌ Error: No title property found in the database")
                return False
                
            # Prepare properties for Notion
            properties = {
                title_property_name: {
                    "title": [{"text": {"content": prompt_data['Prompt ID']}}]
                },
                "Version": {
                    "rich_text": [{"text": {"content": prompt_data['Version']}}]
                },
                "Purpose": {
                    "rich_text": [{"text": {"content": prompt_data['Purpose']}}]
                }
            }
            
            # Add optional properties if they exist
            if 'Type' in prompt_data:
                properties["Type"] = {"select": {"name": prompt_data['Type']}}
                
            if 'Creation Date' in prompt_data:
                properties["Creation Date"] = {"date": {"start": prompt_data['Creation Date']}}
                
            if 'Last Modified' in prompt_data:
                properties["Last Modified"] = {"date": {"start": prompt_data['Last Modified']}}
                
            if 'Models' in prompt_data:
                properties["Models"] = {
                    "multi_select": [{"name": model} for model in prompt_data['Models']]
                }
                
            if 'Full Prompt' in prompt_data:
                # Truncate if needed as Notion has limits
                full_prompt = prompt_data['Full Prompt']
                if len(full_prompt) > 2000:
                    full_prompt = full_prompt[:1997] + "..."
                    
                properties["Full Prompt"] = {
                    "rich_text": [{"text": {"content": full_prompt}}]
                }
            
            # Create the page
            response = self.notion.pages.create(
                parent={"database_id": self.database_id},
                properties=properties
            )
            
            print(f"✅ Created prompt: {prompt_data['Prompt ID']}")
            return response['id']
            
        except Exception as e:
            print(f"❌ Error creating prompt: {e}")
            return False
    
    def read_prompt(self, prompt_id):
        """Retrieve a prompt from the database by ID."""
        try:
            # Get the database to determine the title property name
            db = self.notion.databases.retrieve(database_id=self.database_id)
            title_property_name = None
            
            # Find the title property
            for prop_name, prop in db['properties'].items():
                if prop['type'] == 'title':
                    title_property_name = prop_name
                    break
            
            if not title_property_name:
                print("❌ Error: No title property found in the database")
                return False
            
            # Query the database for the prompt
            response = self.notion.databases.query(
                database_id=self.database_id,
                filter={
                    "property": title_property_name,
                    "title": {
                        "equals": prompt_id
                    }
                }
            )
            
            if not response['results']:
                print(f"❌ Prompt not found: {prompt_id}")
                return None
                
            page = response['results'][0]
            
            # Extract data from the page
            extracted_data = {
                "id": page['id'],
                "Prompt ID": page['properties'][title_property_name]['title'][0]['plain_text'] if page['properties'][title_property_name]['title'] else "",
                "Full Prompt": page['properties']['Full Prompt']['rich_text'][0]['plain_text'] if page['properties']['Full Prompt']['rich_text'] else ""
            }
            
            print(f"✅ Retrieved prompt: {prompt_id}")
            return extracted_data
            
        except Exception as e:
            print(f"❌ Error reading prompt: {e}")
            return None
    
    def update_prompt(self, prompt_id, file_path=None, prompt_data=None):
        """Update an existing prompt in the database."""
        # First get the existing prompt
        existing_record = self.read_prompt(prompt_id)
        
        if not existing_record:
            print(f"Cannot update non-existent prompt: {prompt_id}")
            return False
            
        # If file provided, parse it
        if file_path:
            prompt_data = self.parse_prompt_file(file_path)
            
        if not prompt_data:
            print("No data provided for update")
            return False
            
        try:
            # Prepare properties for update
            properties = {}
            
            if 'Version' in prompt_data:
                properties["Version"] = {
                    "rich_text": [{"text": {"content": prompt_data['Version']}}]
                }
                
            if 'Purpose' in prompt_data:
                properties["Purpose"] = {
                    "rich_text": [{"text": {"content": prompt_data['Purpose']}}]
                }
                
            if 'Type' in prompt_data:
                properties["Type"] = {"select": {"name": prompt_data['Type']}}
                
            if 'Last Modified' in prompt_data:
                properties["Last Modified"] = {"date": {"start": prompt_data['Last Modified']}}
            else:
                # Always update last modified date
                properties["Last Modified"] = {"date": {"start": datetime.now().strftime('%Y-%m-%d')}}
                
            if 'Models' in prompt_data:
                properties["Models"] = {
                    "multi_select": [{"name": model} for model in prompt_data['Models']]
                }
                
            if 'Full Prompt' in prompt_data:
                # Truncate if needed as Notion has limits
                full_prompt = prompt_data['Full Prompt']
                if len(full_prompt) > 2000:
                    full_prompt = full_prompt[:1997] + "..."
                    
                properties["Full Prompt"] = {
                    "rich_text": [{"text": {"content": full_prompt}}]
                }
            
            # Update the page
            self.notion.pages.update(
                page_id=existing_record['id'],
                properties=properties
            )
            
            print(f"✅ Updated prompt: {prompt_id}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating prompt: {e}")
            return False
    
    def delete_prompt(self, prompt_id):
        """Delete (archive) a prompt from the database."""
        # First get the existing prompt
        existing_record = self.read_prompt(prompt_id)
        
        if not existing_record:
            print(f"Cannot delete non-existent prompt: {prompt_id}")
            return False
            
        try:
            # Archive the page (Notion's way of deleting)
            self.notion.pages.update(
                page_id=existing_record['id'],
                archived=True
            )
            
            print(f"✅ Deleted prompt: {prompt_id}")
            return True
            
        except Exception as e:
            print(f"❌ Error deleting prompt: {e}")
            return False
    
    def list_prompts(self, filter_type=None):
        """List all prompts in the database, optionally filtered by type."""
        try:
            filter_obj = {}
            if filter_type:
                filter_obj = {
                    "property": "Type",
                    "select": {
                        "equals": filter_type
                    }
                }
                
            query_params = {
                "database_id": self.database_id
            }
            
            # Only add sort if we're confident the property exists
            try:
                # Check if the database has the Last Modified property
                db = self.notion.databases.retrieve(database_id=self.database_id)
                if "Last Modified" in db["properties"]:
                    query_params["sorts"] = [
                        {
                            "property": "Last Modified",
                            "direction": "descending"
                        }
                    ]
            except Exception:
                # Skip sorting if there's an error checking the properties
                pass
            
            if filter_obj:
                query_params["filter"] = filter_obj
                
            response = self.notion.databases.query(**query_params)
            
            # Get the database to determine the title property name
            db = self.notion.databases.retrieve(database_id=self.database_id)
            title_property_name = None
            
            # Find the title property
            for prop_name, prop in db['properties'].items():
                if prop['type'] == 'title':
                    title_property_name = prop_name
                    break
            
            if not title_property_name:
                print("❌ Error: No title property found in the database")
                return []
                
            prompts = []
            for page in response['results']:
                prompt_data = {
                    "id": page['id'],
                    "Prompt ID": page['properties'][title_property_name]['title'][0]['plain_text'] if page['properties'][title_property_name]['title'] else "",
                }
                
                # Add optional properties if they exist
                if 'Version' in page['properties'] and page['properties']['Version'].get('rich_text'):
                    prompt_data["Version"] = page['properties']['Version']['rich_text'][0]['plain_text']
                else:
                    prompt_data["Version"] = ""
                    
                if 'Type' in page['properties'] and page['properties']['Type'].get('select'):
                    prompt_data["Type"] = page['properties']['Type']['select']['name']
                else:
                    prompt_data["Type"] = ""
                    
                if 'Last Modified' in page['properties'] and page['properties']['Last Modified'].get('date'):
                    prompt_data["Last Modified"] = page['properties']['Last Modified']['date']['start']
                else:
                    prompt_data["Last Modified"] = ""
                    
                prompts.append(prompt_data)
                
            print(f"✅ Retrieved {len(prompts)} prompts")
            return prompts
            
        except Exception as e:
            print(f"❌ Error listing prompts: {e}")
            return []

if __name__ == "__main__":
    # Example usage
    manager = PromptManager()
    
    # Setup the database schema (only needed once)
    # manager.setup_database()
    
    # Create a prompt from a file
    # manager.create_prompt("prompts/khaos-coding-companion.txt")
    
    # Read a prompt
    # prompt = manager.read_prompt("khaos-coding-companion")
    
    # Update a prompt
    # manager.update_prompt("khaos-coding-companion", "prompts/khaos-coding-companion-updated.txt")
    
    # List all prompts
    # prompts = manager.list_prompts()
    # for p in prompts:
    #     print(f"{p['Prompt ID']} (v{p['Version']}) - {p['Type']} - Last modified: {p['Last Modified']}")
    
    # Delete a prompt
    # manager.delete_prompt("khaos-test-prompt")
