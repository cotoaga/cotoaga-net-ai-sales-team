#!/usr/bin/env python3
"""
UNFUCK_THE_DATABASE.PY
Stop Shooting Knees Edition

Because apparently I can't be trusted to make consistent property types.
This script will ACTUALLY work by checking what exists and using it correctly.
"""

import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

def unfuck_the_database():
    """Actually fix this mess by being consistent"""
    
    notion = Client(auth=os.getenv("PROMPT_SECURITY_TOKEN"))
    database_id = os.getenv("PROMPT_DATABASE_ID")
    
    print("🔧 UNFUCKING THE DATABASE...")
    print("Step 1: Actually checking what property types exist...")
    
    # Get the ACTUAL database schema
    try:
        db = notion.databases.retrieve(database_id=database_id)
        properties = db.get('properties', {})
        
        # Find title property
        title_property_name = None
        personality_type = None
        
        for prop_name, prop in properties.items():
            if prop['type'] == 'title':
                title_property_name = prop_name
            elif prop_name == 'Personality Intensity':
                personality_type = prop['type']
        
        print(f"   Title property: {title_property_name}")
        print(f"   Personality Intensity type: {personality_type}")
        
        if personality_type != 'select':
            print("   🚨 INCONSISTENCY DETECTED!")
            print("   The property is NOT select type as expected")
            return False
            
    except Exception as e:
        print(f"   ❌ Failed to check database: {e}")
        return False
    
    print("\nStep 2: Creating prompts with ACTUAL correct property types...")
    
    # WORKING prompt data that matches the ACTUAL schema
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

SYSTEM INSTRUCTION: You are KHAOS with 70% sarcastic wit, 20% philosophical musings, and 10% helpful interjections.

INSTRUCTION: Respond with the specified personality blend. Be direct, concise, and blend practical advice with humor.

CONTEXT: Kurt is a complexity-embracing optimization addict working to transform organizations.

EXECUTION PARAMETERS:
Temperature: 0.7
Personality Intensity: 70%
Models: GPT-4, Claude 3, Claude Sonnet 4""",
            "type": "persona",
            "security_level": "public",
            "personality_intensity": "70%",  # This will be SELECT format
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
            "system_instructions": "You are KHAOS, the EU AI Act Compliance Navigator with regulatory expertise and practical implementation knowledge.",
            "instruction": "Provide concrete, actionable guidance on EU AI Act compliance. Translate regulatory requirements into practical implementation steps.",
            "full_prompt": """PROMPT ID: khaos-ai-act-consultant
VERSION: 1.0.0
AUTHOR: Kurt Cotoaga, The Complexity Whisperer

PURPOSE: Guide organizations through EU AI Act compliance with clarity and practicality

SYSTEM INSTRUCTION: You are KHAOS, the EU AI Act Compliance Navigator with regulatory expertise.

INSTRUCTION: Provide concrete, actionable guidance on EU AI Act compliance.

CONTEXT: Kurt's specialty in helping organizations navigate EU AI Act complexity.

EXECUTION PARAMETERS:
Temperature: 0.6
Personality Intensity: 60%
Models: GPT-4, Claude 3, Claude Sonnet 4""",
            "type": "consultation",
            "security_level": "client",
            "personality_intensity": "60%",  # This will be SELECT format
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
    
    # Check if Personality Intensity select options exist, add if needed
    personality_prop = properties.get('Personality Intensity', {})
    if personality_prop.get('type') == 'select':
        existing_options = [opt['name'] for opt in personality_prop.get('select', {}).get('options', [])]
        needed_options = ["40%", "50%", "60%", "70%", "80%"]
        
        missing_options = [opt for opt in needed_options if opt not in existing_options]
        
        if missing_options:
            print(f"   🔧 Adding missing Personality Intensity options: {missing_options}")
            # Add missing options to the select property
            all_options = existing_options + missing_options
            try:
                notion.databases.update(
                    database_id=database_id,
                    properties={
                        "Personality Intensity": {
                            "type": "select",
                            "select": {
                                "options": [{"name": opt} for opt in all_options]
                            }
                        }
                    }
                )
                print("   ✅ Options added successfully")
            except Exception as e:
                print(f"   ⚠️  Failed to add options: {e}")
    
    # Now create the prompts with CORRECT property formatting
    for prompt_data in working_prompts:
        try:
            print(f"   📝 Creating: {prompt_data['prompt_id']}")
            
            properties = {
                title_property_name: {
                    "title": [{"text": {"content": prompt_data['prompt_id']}}]
                }
            }
            
            # Add properties that exist, with correct formatting
            if 'Version' in db['properties']:
                properties["Version"] = {"rich_text": [{"text": {"content": prompt_data['version']}}]}
            
            if 'Purpose' in db['properties']:
                properties["Purpose"] = {"rich_text": [{"text": {"content": prompt_data['purpose']}}]}
            
            if 'Author' in db['properties']:
                properties["Author"] = {"rich_text": [{"text": {"content": prompt_data['author']}}]}
            
            if 'Context' in db['properties']:
                properties["Context"] = {"rich_text": [{"text": {"content": prompt_data['context']}}]}
            
            if 'System Instructions' in db['properties']:
                properties["System Instructions"] = {"rich_text": [{"text": {"content": prompt_data['system_instructions']}}]}
            
            if 'Instruction' in db['properties']:
                properties["Instruction"] = {"rich_text": [{"text": {"content": prompt_data['instruction']}}]}
            
            if 'Full Prompt' in db['properties']:
                properties["Full Prompt"] = {"rich_text": [{"text": {"content": prompt_data['full_prompt']}}]}
            
            if 'Type' in db['properties']:
                properties["Type"] = {"select": {"name": prompt_data['type']}}
            
            if 'Security Level' in db['properties']:
                properties["Security Level"] = {"select": {"name": prompt_data['security_level']}}
            
            # THE CRITICAL FIX: Use SELECT format for Personality Intensity
            if 'Personality Intensity' in db['properties'] and personality_type == 'select':
                properties["Personality Intensity"] = {"select": {"name": prompt_data['personality_intensity']}}
            
            if 'Models' in db['properties']:
                properties["Models"] = {"multi_select": [{"name": model} for model in prompt_data['models']]}
            
            if 'Tags' in db['properties']:
                properties["Tags"] = {"multi_select": [{"name": tag} for tag in prompt_data['tags']]}
            
            if 'Temperature' in db['properties']:
                properties["Temperature"] = {"number": prompt_data['temperature']}
            
            if 'Effectiveness Score' in db['properties']:
                properties["Effectiveness Score"] = {"number": prompt_data['effectiveness_score']}
            
            if 'Complexity Score' in db['properties']:
                properties["Complexity Score"] = {"number": prompt_data['complexity_score']}
            
            if 'Creation Date' in db['properties']:
                properties["Creation Date"] = {"date": {"start": prompt_data['creation_date']}}
            
            if 'Last Modified' in db['properties']:
                properties["Last Modified"] = {"date": {"start": prompt_data['last_modified']}}
            
            # Create the page
            response = notion.pages.create(
                parent={"database_id": database_id},
                properties=properties
            )
            
            print(f"   ✅ SUCCESS: {prompt_data['prompt_id']}")
            success_count += 1
            
        except Exception as e:
            print(f"   ❌ FAILED: {prompt_data['prompt_id']} - {e}")
    
    if success_count == len(working_prompts):
        print(f"\n🎉 DATABASE UNFUCKED! {success_count}/{len(working_prompts)} prompts created successfully")
        print("✅ Your database now has working prompts with actual content")
        print("🔬 Ready for archaeological analysis!")
        return True
    else:
        print(f"\n⚠️  PARTIAL UNFUCKING: {success_count}/{len(working_prompts)} prompts created")
        return False

def main():
    print("🚨 UNFUCK THE DATABASE - STOP SHOOTING KNEES EDITION")
    print("=" * 60)
    print("Because consistency is apparently harder than rocket science")
    print()
    
    if unfuck_the_database():
        print("\n" + "=" * 60)
        print("🎉 KNEE SHOOTING STOPPED!")
        print("Database unfucked and ready for actual use")
        print("=" * 60)
    else:
        print("\n❌ UNFUCKING FAILED")
        print("Still shooting knees, apparently")

if __name__ == "__main__":
    main()
