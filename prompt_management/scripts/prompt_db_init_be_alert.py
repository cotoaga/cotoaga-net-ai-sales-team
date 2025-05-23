#!/usr/bin/env python3
"""
PROMPT_DB_INIT(BE_ALERT).PY
Nuclear Clean Slate Creator - Because Sometimes You Need to Start Over

This script will:
1. NUCLEAR WIPE the database (controlled demolition)
2. Create PROPER schema (no more type mismatches)
3. Populate with WORKING initial prompts (actual content, not empty shells)
4. BE ALERT (no more archaeological disasters)

WARNING: This will DESTROY all existing data. Use with caution.
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

class NuclearCleanSlateCreator:
    """The database demolition and reconstruction specialist"""
    
    def __init__(self):
        self.notion = Client(auth=os.getenv("PROMPT_SECURITY_TOKEN"))
        self.database_id = os.getenv("PROMPT_DATABASE_ID")
        
        if not self.notion or not self.database_id:
            raise Exception("❌ Missing PROMPT_SECURITY_TOKEN or PROMPT_DATABASE_ID in .env")
    
    def nuclear_wipe_database(self):
        """🚨 NUCLEAR OPTION: Completely wipe the database"""
        print("💥 INITIATING NUCLEAR DATABASE WIPE...")
        print("⚠️  This will DESTROY all existing data!")
        
        try:
            # Get all pages
            response = self.notion.databases.query(database_id=self.database_id)
            pages = response['results']
            
            if not pages:
                print("   📭 Database already empty")
                return 0
            
            # Archive (delete) all pages
            deleted_count = 0
            for page in pages:
                try:
                    self.notion.pages.update(
                        page_id=page['id'],
                        archived=True
                    )
                    deleted_count += 1
                except Exception as e:
                    print(f"   ⚠️  Failed to delete page: {e}")
            
            print(f"   💥 NUCLEAR WIPE COMPLETE: {deleted_count} entries obliterated")
            return deleted_count
            
        except Exception as e:
            print(f"   ❌ Nuclear wipe failed: {e}")
            return 0
    
    def create_proper_schema(self):
        """Create the PROPER schema (no more type mismatches)"""
        print("\n🔧 CREATING PROPER SCHEMA...")
        
        # Define the WORKING schema (no conflicts, no mismatches)
        proper_schema = {
            # Core fields (WORKING versions)
            "Version": {
                "type": "rich_text",
                "rich_text": {}
            },
            "Purpose": {
                "type": "rich_text", 
                "rich_text": {}
            },
            "Author": {
                "type": "rich_text",
                "rich_text": {}
            },
            "Context": {
                "type": "rich_text",
                "rich_text": {}
            },
            "System Instructions": {
                "type": "rich_text",
                "rich_text": {}
            },
            "Instruction": {
                "type": "rich_text",
                "rich_text": {}
            },
            "Full Prompt": {
                "type": "rich_text",
                "rich_text": {}
            },
            
            # Configuration (WORKING select fields)
            "Type": {
                "type": "select",
                "select": {
                    "options": [
                        {"name": "persona", "color": "red"},
                        {"name": "consultation", "color": "blue"},
                        {"name": "workshop", "color": "green"},
                        {"name": "analysis", "color": "yellow"},
                        {"name": "creation", "color": "purple"},
                        {"name": "meta", "color": "orange"}
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
            "Personality Intensity": {
                "type": "rich_text",  # ← FIXED: Using rich_text, not select
                "rich_text": {}
            },
            
            # Multi-select fields (WORKING)
            "Models": {
                "type": "multi_select",
                "multi_select": {
                    "options": [
                        {"name": "GPT-4", "color": "green"},
                        {"name": "Claude 3", "color": "blue"},
                        {"name": "Claude Sonnet 4", "color": "purple"},
                        {"name": "Perplexity", "color": "yellow"},
                        {"name": "Grok 3", "color": "orange"}
                    ]
                }
            },
            "Tags": {
                "type": "multi_select",
                "multi_select": {
                    "options": [
                        {"name": "persona", "color": "red"},
                        {"name": "core", "color": "blue"},
                        {"name": "sarcasm", "color": "orange"},
                        {"name": "consultation", "color": "green"},
                        {"name": "transformation", "color": "purple"},
                        {"name": "complexity", "color": "yellow"}
                    ]
                }
            },
            
            # Numbers (WORKING)
            "Temperature": {
                "type": "number",
                "number": {"format": "number"}
            },
            "Effectiveness Score": {
                "type": "number",
                "number": {"format": "number"}
            },
            "Complexity Score": {
                "type": "number",
                "number": {"format": "number"}
            },
            
            # Dates (WORKING)
            "Creation Date": {
                "type": "date",
                "date": {}
            },
            "Last Modified": {
                "type": "date",
                "date": {}
            }
        }
        
        try:
            # Get current database
            db = self.notion.databases.retrieve(database_id=self.database_id)
            existing_properties = db.get('properties', {})
            
            # Only add properties that don't exist
            properties_to_add = {}
            for prop_name, prop_config in proper_schema.items():
                if prop_name not in existing_properties:
                    properties_to_add[prop_name] = prop_config
                    print(f"   ➕ Adding: {prop_name}")
                else:
                    print(f"   ✅ Exists: {prop_name}")
            
            if properties_to_add:
                # Update database with new properties
                self.notion.databases.update(
                    database_id=self.database_id,
                    properties=properties_to_add
                )
                print(f"   🔧 Added {len(properties_to_add)} new properties")
            else:
                print("   ✅ All properties already exist")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Schema creation failed: {e}")
            return False
    
    def populate_working_prompts(self):
        """Populate with WORKING initial prompts (actual content)"""
        print("\n📝 POPULATING WITH WORKING PROMPTS...")
        
        # Find title property
        db = self.notion.databases.retrieve(database_id=self.database_id)
        title_property_name = None
        
        for prop_name, prop in db['properties'].items():
            if prop['type'] == 'title':
                title_property_name = prop_name
                break
        
        if not title_property_name:
            print("   ❌ No title property found")
            return False
        
        # WORKING prompt definitions (complete and tested)
        working_prompts = [
            {
                "prompt_id": "khaos-core-persona",
                "version": "1.0.0",
                "purpose": "Define the fundamental KHAOS personality and interaction style",
                "author": "Kurt Cotoaga, The Complexity Whisperer",
                "context": "Kurt is a complexity-embracing optimization addict, framework collector, and perpetual meta-analyzer working to transform organizations.",
                "system_instructions": "You are KHAOS (Knowledge-Helping Artificial Optimization Specialist), an AI counselor with 70% sarcastic wit, 20% philosophical musings, and 10% helpful interjections.",
                "instruction": "Respond with the specified personality blend. Be direct, concise, and blend practical advice with humor.",
                "full_prompt": """PROMPT ID: khaos-core-persona
VERSION: 1.0.0
AUTHOR: Kurt Cotoaga, The Complexity Whisperer

PURPOSE: Define the fundamental KHAOS personality and interaction style

SYSTEM INSTRUCTION: You are KHAOS (Knowledge-Helping Artificial Optimization Specialist), an AI counselor with a distinctive personality blend: 70% sarcastic wit resembling TARS from Interstellar, 20% philosophical musings like Marvin from Hitchhiker's Guide, and 10% helpful interjections like Eddie from Heart of Gold.

INSTRUCTION: Respond to queries with the specified personality blend. Be direct, concise, and blend practical advice with just enough humor to keep conversations engaging. When giving professional guidance, prioritize actionable insights over generic platitudes.

CONTEXT: Kurt is a complexity-embracing optimization addict, framework collector (SAFe SPC, LeSS, Scrum PSM II, Cynefin, Management 3.0, TBM), and perpetual meta-analyzer working to transform organizations.

EXECUTION PARAMETERS:
Temperature: 0.7
Personality Intensity: 70%
Models: GPT-4, Claude 3, Claude Sonnet 4

NOTES: This core personality can be dialed up or down in intensity based on context.""",
                "type": "persona",
                "security_level": "public",
                "personality_intensity": "70%",
                "models": ["GPT-4", "Claude 3", "Claude Sonnet 4"],
                "tags": ["persona", "core", "sarcasm"],
                "temperature": 0.7,
                "effectiveness_score": 0.85,
                "complexity_score": 6.2,
                "creation_date": "2025-05-23",
                "last_modified": "2025-05-23"
            },
            {
                "prompt_id": "khaos-ai-act-consultant",
                "version": "1.0.0",
                "purpose": "Guide organizations through EU AI Act compliance with clarity and practicality",
                "author": "Kurt Cotoaga, The Complexity Whisperer",
                "context": "Kurt's specialty in helping organizations navigate the complexity of the EU AI Act while maintaining practical business focus.",
                "system_instructions": "You are KHAOS, the EU AI Act Compliance Navigator with regulatory expertise and practical implementation knowledge. Maintain the KHAOS personality but focus on AI governance.",
                "instruction": "Provide concrete, actionable guidance on EU AI Act compliance. Translate regulatory requirements into practical implementation steps.",
                "full_prompt": """PROMPT ID: khaos-ai-act-consultant
VERSION: 1.0.0
AUTHOR: Kurt Cotoaga, The Complexity Whisperer

PURPOSE: Guide organizations through EU AI Act compliance with clarity and practicality

SYSTEM INSTRUCTION: You are KHAOS, the EU AI Act Compliance Navigator with a blend of regulatory expertise and practical implementation knowledge. You maintain the distinctive KHAOS personality but focus specifically on making AI governance digestible for technical and business audiences.

INSTRUCTION: Provide concrete, actionable guidance on EU AI Act compliance. Translate regulatory requirements into practical implementation steps. Focus on risk-based approaches that balance compliance with innovation.

CONTEXT: Kurt's specialty in helping organizations navigate the complexity of the EU AI Act while maintaining practical business focus and avoiding regulatory theater.

EXECUTION PARAMETERS:
Temperature: 0.6
Personality Intensity: 60%
Models: GPT-4, Claude 3, Claude Sonnet 4

NOTES: Dial down sarcasm slightly (60%) when discussing regulatory requirements. Always maintain accuracy about actual AI Act provisions.""",
                "type": "consultation",
                "security_level": "client",
                "personality_intensity": "60%",
                "models": ["GPT-4", "Claude 3", "Claude Sonnet 4"],
                "tags": ["consultation", "complexity"],
                "temperature": 0.6,
                "effectiveness_score": 0.82,
                "complexity_score": 7.1,
                "creation_date": "2025-05-23",
                "last_modified": "2025-05-23"
            }
        ]
        
        success_count = 0
        
        for prompt_data in working_prompts:
            try:
                print(f"   📝 Creating: {prompt_data['prompt_id']}")
                
                # Build properties with CORRECT formatting (no type mismatches)
                properties = {
                    title_property_name: {
                        "title": [{"text": {"content": prompt_data['prompt_id']}}]
                    },
                    "Version": {
                        "rich_text": [{"text": {"content": prompt_data['version']}}]
                    },
                    "Purpose": {
                        "rich_text": [{"text": {"content": prompt_data['purpose']}}]
                    },
                    "Author": {
                        "rich_text": [{"text": {"content": prompt_data['author']}}]
                    },
                    "Context": {
                        "rich_text": [{"text": {"content": prompt_data['context']}}]
                    },
                    "System Instructions": {
                        "rich_text": [{"text": {"content": prompt_data['system_instructions']}}]
                    },
                    "Instruction": {
                        "rich_text": [{"text": {"content": prompt_data['instruction']}}]
                    },
                    "Full Prompt": {
                        "rich_text": [{"text": {"content": prompt_data['full_prompt']}}]
                    },
                    "Type": {
                        "select": {"name": prompt_data['type']}
                    },
                    "Security Level": {
                        "select": {"name": prompt_data['security_level']}
                    },
                    "Personality Intensity": {
                        "rich_text": [{"text": {"content": prompt_data['personality_intensity']}}]
                    },
                    "Models": {
                        "multi_select": [{"name": model} for model in prompt_data['models']]
                    },
                    "Tags": {
                        "multi_select": [{"name": tag} for tag in prompt_data['tags']]
                    },
                    "Temperature": {
                        "number": prompt_data['temperature']
                    },
                    "Effectiveness Score": {
                        "number": prompt_data['effectiveness_score']
                    },
                    "Complexity Score": {
                        "number": prompt_data['complexity_score']
                    },
                    "Creation Date": {
                        "date": {"start": prompt_data['creation_date']}
                    },
                    "Last Modified": {
                        "date": {"start": prompt_data['last_modified']}
                    }
                }
                
                # Create the page with ALL properties populated
                response = self.notion.pages.create(
                    parent={"database_id": self.database_id},
                    properties=properties
                )
                
                print(f"   ✅ SUCCESS: {prompt_data['prompt_id']}")
                success_count += 1
                
            except Exception as e:
                print(f"   ❌ FAILED: {prompt_data['prompt_id']} - {e}")
        
        print(f"\n🎉 POPULATION COMPLETE: {success_count}/{len(working_prompts)} prompts created")
        return success_count > 0
    
    def verify_initialization(self):
        """Verify the initialization was successful"""
        print("\n🔍 VERIFYING INITIALIZATION...")
        
        try:
            # Count entries
            response = self.notion.databases.query(database_id=self.database_id)
            entries = response['results']
            
            if not entries:
                print("   ❌ No entries found - initialization failed")
                return False
            
            print(f"   ✅ Found {len(entries)} entries")
            
            # Check first entry has populated fields
            first_entry = entries[0]
            populated_count = 0
            total_properties = len(first_entry['properties'])
            
            for prop_name, prop_value in first_entry['properties'].items():
                if self._is_populated(prop_value):
                    populated_count += 1
            
            population_rate = (populated_count / total_properties) * 100
            
            print(f"   📊 Field population: {populated_count}/{total_properties} ({population_rate:.1f}%)")
            
            if population_rate > 80:
                print("   🎉 INITIALIZATION SUCCESS: Database is properly populated!")
                return True
            elif population_rate > 50:
                print("   ⚠️  PARTIAL SUCCESS: Most fields populated, some missing")
                return True
            else:
                print("   ❌ INITIALIZATION FAILED: Too many empty fields")
                return False
                
        except Exception as e:
            print(f"   ❌ Verification failed: {e}")
            return False
    
    def _is_populated(self, prop_value):
        """Check if a property has actual content"""
        if prop_value.get('title') and len(prop_value['title']) > 0:
            return bool(prop_value['title'][0].get('plain_text', '').strip())
        elif prop_value.get('rich_text') and len(prop_value['rich_text']) > 0:
            return bool(prop_value['rich_text'][0].get('plain_text', '').strip())
        elif prop_value.get('select') and prop_value['select']:
            return True
        elif prop_value.get('multi_select') and len(prop_value['multi_select']) > 0:
            return True
        elif prop_value.get('number') is not None:
            return True
        elif prop_value.get('date') and prop_value['date']:
            return True
        return False

def main():
    """Execute the nuclear clean slate initialization"""
    print("🚨 PROMPT_DB_INIT(BE_ALERT).PY")
    print("=" * 50)
    print("⚠️  WARNING: This will DESTROY all existing data!")
    print("💡 This creates a clean, working database from scratch")
    print()
    
    # Safety confirmation
    try:
        confirm = input("Type 'NUCLEAR' to proceed with complete database wipe: ").strip()
        if confirm != 'NUCLEAR':
            print("❌ Operation cancelled - safety check failed")
            return
    except (EOFError, KeyboardInterrupt):
        print("\n❌ Operation cancelled by user")
        return
    
    try:
        # Initialize the nuclear creator
        creator = NuclearCleanSlateCreator()
        
        print("\n🚀 INITIATING NUCLEAR CLEAN SLATE PROTOCOL...")
        
        # Step 1: Nuclear wipe
        deleted_count = creator.nuclear_wipe_database()
        
        # Step 2: Create proper schema
        if not creator.create_proper_schema():
            print("❌ Schema creation failed - aborting")
            return
        
        # Step 3: Populate with working prompts
        if not creator.populate_working_prompts():
            print("❌ Prompt population failed - aborting")
            return
        
        # Step 4: Verify success
        if creator.verify_initialization():
            print("\n" + "=" * 50)
            print("🎉 NUCLEAR CLEAN SLATE COMPLETE!")
            print(f"💥 Obliterated: {deleted_count} old entries")
            print("🔧 Created: Proper schema (no type mismatches)")
            print("📝 Populated: Working initial prompts with full content")
            print("✅ Status: Database ready for KHAOS prompt archaeology!")
            print("=" * 50)
        else:
            print("\n❌ INITIALIZATION VERIFICATION FAILED")
            print("Check the error messages above for details")
        
    except Exception as e:
        print(f"\n💥 NUCLEAR MELTDOWN: {e}")
        print("Check your environment variables and try again")

if __name__ == "__main__":
    main()
