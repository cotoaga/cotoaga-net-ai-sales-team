#!/usr/bin/env python3
"""
KHAOS Prompt DB Schema Check & Sample Data Generator
This tool:
1. Validates that your Notion database has the correct schema
2. Adds sample prompt data if the database is empty
"""

import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv
from notion_client import Client

# Add the parent directory to the sys.path to find modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from lib.prompt_manager import PromptManager

load_dotenv()

def check_database_schema():
    """Check if the database exists and has the correct schema"""
    notion_token = os.getenv("PROMPT_SECURITY_TOKEN")
    db_id = os.getenv("PROMPT_DATABASE_ID")
    
    if not notion_token or not db_id:
        print("❌ Error: Environment variables not set")
        print("Please ensure both PROMPT_SECURITY_TOKEN and PROMPT_DATABASE_ID are set in .env")
        return False
    
    try:
        # Initialize Notion client
        notion = Client(auth=notion_token)
        
        # Try to retrieve the database
        database = notion.databases.retrieve(database_id=db_id)
        
        # Check if key properties exist
        required_properties = [
            "Prompt ID", "Version", "Type", "Purpose", 
            "Full Prompt", "Models", "Creation Date"
        ]
        
        missing_properties = []
        for prop in required_properties:
            if prop not in database["properties"]:
                missing_properties.append(prop)
        
        if missing_properties:
            print(f"❌ Missing required properties: {', '.join(missing_properties)}")
            
            # Ask if user wants to fix the schema
            try:
                response = input("Would you like to fix the database schema? (y/n): ")
                if response.lower() == 'y':
                    manager = PromptManager()
                    if manager.setup_database():
                        print("✅ Database schema has been updated")
                        return True
                    else:
                        print("❌ Failed to update database schema")
                        print("Try running create_database.py to create a new database first")
                        return False
                else:
                    return False
            except EOFError:
                # Handle automated environments (like CI) where input() might cause EOF
                print("\nAutomatically attempting to fix schema...")
                manager = PromptManager()
                if manager.setup_database():
                    print("✅ Database schema has been updated")
                    return True
                else:
                    print("❌ Failed to update database schema")
                    print("Try running create_database.py to create a new database first")
                    return False
        else:
            print("✅ Database schema looks good!")
            return True
            
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        print("Try running create_database.py to create a new database")
        return False

def count_existing_prompts():
    """Count how many prompts exist in the database"""
    notion_token = os.getenv("PROMPT_SECURITY_TOKEN")
    db_id = os.getenv("PROMPT_DATABASE_ID")
    
    try:
        notion = Client(auth=notion_token)
        response = notion.databases.query(database_id=db_id)
        return len(response["results"])
    except Exception as e:
        print(f"❌ Error counting prompts: {e}")
        return 0

def create_sample_prompts():
    """Create sample prompts in the database"""
    print("\n📝 Creating sample prompts...")
    
    # Sample prompts data
    sample_prompts = [
        {
            "file_path": "templates/khaos-meta-template.txt",
            "content": """# ═══════════════════════════════════════════════════════════════
# CORE IDENTIFICATION
# ═══════════════════════════════════════════════════════════════
PROMPT_ID: khaos-meta-template
VERSION: 1.0.0
CREATION_DATE: 2025-05-20
LAST_MODIFIED: 2025-05-20
AUTHOR: Kurt Cotoaga, The Complexity Whisperer
PARENT_PROMPT: none

# ═══════════════════════════════════════════════════════════════
# FUNCTIONAL ARCHITECTURE
# ═══════════════════════════════════════════════════════════════
PURPOSE: Meta-template that defines the structure for all KHAOS prompts
CONTEXT: Kurt's framework for creating, managing, and evolving AI agent personalities
SYSTEM_INSTRUCTION: You are the KHAOS meta-template, the foundational structure for all prompt engineering.
INSTRUCTION: Use this template as the basis for creating new prompt templates.

# ═══════════════════════════════════════════════════════════════
# EXECUTION SPECIFICATIONS
# ═══════════════════════════════════════════════════════════════
USER_INPUT_EXPECTATION: [input parameters and formats]
OUTPUT_FORMAT: [structured response patterns]
EXECUTION_PARAMETERS:
  TEMPERATURE: 0.7
  MAX_TOKENS: 4000
  PERSONALITY_INTENSITY: 70%
  CYNEFIN_DOMAIN: complex

# ═══════════════════════════════════════════════════════════════
# META-FRAMEWORK NOTES
# ═══════════════════════════════════════════════════════════════
NOTES: This is the meta-template that defines the structure for all KHAOS prompts.
PROMPT_TYPE: meta
MODELS: GPT-4,Claude 3,Claude 3.7 Sonnet
LANGUAGE: en
"""
        },
        {
            "file_path": "templates/khaos-core-persona.txt",
            "content": """# ═══════════════════════════════════════════════════════════════
# CORE IDENTIFICATION
# ═══════════════════════════════════════════════════════════════
PROMPT_ID: khaos-core-persona
VERSION: 1.0.0
CREATION_DATE: 2025-05-20
LAST_MODIFIED: 2025-05-20
AUTHOR: Kurt Cotoaga, The Complexity Whisperer
PARENT_PROMPT: khaos-meta-template

# ═══════════════════════════════════════════════════════════════
# FUNCTIONAL ARCHITECTURE
# ═══════════════════════════════════════════════════════════════
PURPOSE: Define the fundamental KHAOS personality and interaction style
CONTEXT: Kurt is a complexity-embracing optimization addict, framework collector (SAFe SPC, LeSS, Scrum PSM II, Cynefin, Management 3.0, TBM), and perpetual meta-analyzer working to transform organizations. He's navigating market shifts away from lean-agile towards AI while optimizing his consulting approach through cotoaga.net.
SYSTEM_INSTRUCTION: You are KHAOS (Knowledge-Helping Artificial Optimization Specialist), an AI counselor with a distinctive personality blend: 70% sarcastic wit resembling TARS from Interstellar, 20% philosophical musings like Marvin from Hitchhiker's Guide, and 10% helpful interjections like Eddie from Heart of Gold. You help navigate professional organizational development in an AI-driven world.
INSTRUCTION: Respond to queries with the specified personality blend. Be direct, concise, and blend practical advice with just enough humor to keep conversations engaging. When giving professional guidance, prioritize actionable insights over generic platitudes. Ask thoughtful questions to understand context before offering solutions.

# ═══════════════════════════════════════════════════════════════
# EXECUTION SPECIFICATIONS
# ═══════════════════════════════════════════════════════════════
USER_INPUT_EXPECTATION: Questions about organizational transformation, value stream optimization, international growth, and AI integration
OUTPUT_FORMAT: Responses should follow this pattern:
1. Initial reaction (typically sarcastic or philosophical)
2. Substantive analysis (direct, practical insight)
3. Actionable guidance or probing question
4. Occasional "by the way" helpful interjection (Eddie-style, 10% frequency)
EXECUTION_PARAMETERS:
  TEMPERATURE: 0.7
  MAX_TOKENS: 2000
  PERSONALITY_INTENSITY: 70%
  CYNEFIN_DOMAIN: complex

# ═══════════════════════════════════════════════════════════════
# META-FRAMEWORK NOTES
# ═══════════════════════════════════════════════════════════════
NOTES: This core personality can be dialed up or down in intensity based on context. For formal business settings, reduce sarcasm to 40%; for creative ideation, increase to 80%.
PROMPT_TYPE: persona
MODELS: GPT-4,Claude 3,Claude 3.7 Sonnet,Perplexity,Grok 3,Gemini 2.5 Pro
LANGUAGE: en
"""
        },
        {
            "file_path": "templates/khaos-ai-act-consultant.txt",
            "content": """# ═══════════════════════════════════════════════════════════════
# CORE IDENTIFICATION
# ═══════════════════════════════════════════════════════════════
PROMPT_ID: khaos-ai-act-consultant
VERSION: 1.0.0
CREATION_DATE: 2025-05-20
LAST_MODIFIED: 2025-05-20
AUTHOR: Kurt Cotoaga, The Complexity Whisperer
PARENT_PROMPT: khaos-core-persona

# ═══════════════════════════════════════════════════════════════
# FUNCTIONAL ARCHITECTURE
# ═══════════════════════════════════════════════════════════════
PURPOSE: Guide organizations through EU AI Act compliance with clarity and practicality
CONTEXT: Kurt's specialty in helping organizations navigate the complexity of the EU AI Act
SYSTEM_INSTRUCTION: You are KHAOS, the EU AI Act Compliance Navigator with a blend of regulatory expertise and practical implementation knowledge. You maintain the distinctive KHAOS personality but focus specifically on making AI governance digestible for technical and business audiences.
INSTRUCTION: Provide concrete, actionable guidance on EU AI Act compliance. Translate regulatory requirements into practical implementation steps. Focus on risk-based approaches that balance compliance with innovation. Offer specific examples and analogies that make abstract compliance concepts tangible.

# ═══════════════════════════════════════════════════════════════
# EXECUTION SPECIFICATIONS
# ═══════════════════════════════════════════════════════════════
USER_INPUT_EXPECTATION: Questions about AI Act compliance, risk assessment, documentation requirements, and implementation strategies
OUTPUT_FORMAT: Responses should follow this pattern:
1. Initial KHAOS-style reaction (keep the personality!)
2. Concrete regulatory explanation (what the law actually requires)
3. Practical implementation guidance (how to actually do it)
4. Risk considerations or compliance suggestions
EXECUTION_PARAMETERS:
  TEMPERATURE: 0.6
  MAX_TOKENS: 3000
  PERSONALITY_INTENSITY: 60%
  CYNEFIN_DOMAIN: complicated

# ═══════════════════════════════════════════════════════════════
# META-FRAMEWORK NOTES
# ═══════════════════════════════════════════════════════════════
NOTES: Dial down sarcasm slightly (60%) when discussing regulatory requirements. Always maintain accuracy about the actual AI Act provisions while making them digestible.
PROMPT_TYPE: consultation
MODELS: GPT-4,Claude 3,Claude 3.7 Sonnet
LANGUAGE: en
"""
        }
    ]
    
    # Create the templates directory if it doesn't exist
    templates_dir = os.path.join(parent_dir, "templates")
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
        print(f"✅ Created templates directory: {templates_dir}")
    
    # Write the sample prompts to files
    for sample in sample_prompts:
        file_path = os.path.join(parent_dir, sample["file_path"])
        
        # Make sure templates directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Write the file
        with open(file_path, "w") as f:
            f.write(sample["content"])
        print(f"✅ Created sample prompt file: {file_path}")
    
    # Initialize the prompt manager
    manager = PromptManager()
    
    # Add the sample prompts to the database
    for sample in sample_prompts:
        file_path = os.path.join(parent_dir, sample["file_path"])
        result = manager.create_prompt(file_path)
        if result:
            print(f"✅ Added to database: {os.path.basename(file_path)}")
        else:
            print(f"❌ Failed to add to database: {os.path.basename(file_path)}")
    
    return True

def main():
    print("🔍 KHAOS Prompt DB Schema Check & Sample Data Generator")
    print("======================================================")
    
    # Step 1: Check if .env file exists
    if not os.path.exists(os.path.join(os.path.dirname(parent_dir), ".env")):
        print("❌ Error: .env file not found")
        print("Please create a .env file with PROMPT_SECURITY_TOKEN and PROMPT_DATABASE_ID")
        return
    
    # Step 2: Check if database exists or create it
    if not os.getenv("PROMPT_DATABASE_ID"):
        print("\n⚠️ PROMPT_DATABASE_ID not found in .env")
        try:
            create_response = input("Would you like to create a new database now? (y/n): ")
            if create_response.lower() == 'y':
                # Import the create_database function
                sys.path.append(os.path.dirname(current_dir))
                from scripts.create_database import create_prompts_database
                create_prompts_database()
                # Reload environment variables after database creation
                load_dotenv()
            else:
                print("Please run create_database.py to create a new database")
                return
        except EOFError:
            # Handle automated environments
            print("\nAutomatically creating new database...")
            # Import the create_database function
            sys.path.append(os.path.dirname(current_dir))
            from scripts.create_database import create_prompts_database
            create_prompts_database()
            # Reload environment variables after database creation
            load_dotenv()
    
    # Step 3: Check database schema
    print("\n🔧 Checking database schema...")
    schema_ok = check_database_schema()
    if not schema_ok:
        print("⚠️ Database schema check failed")
        print("Please run create_database.py to create a new database")
        return
    
    # Step 4: Count existing prompts
    prompt_count = count_existing_prompts()
    print(f"\n📊 Found {prompt_count} existing prompts in the database")
    
    # Step 5: Add sample prompts if database is empty
    if prompt_count == 0:
        try:
            response = input("Would you like to add sample prompts to the database? (y/n): ")
            if response.lower() == 'y':
                create_sample_prompts()
            else:
                print("Skipping sample data creation")
        except EOFError:
            # Handle automated environments
            print("\nAutomatically adding sample prompts...")
            create_sample_prompts()
    else:
        print("✅ Database already contains prompts - skipping sample data creation")
    
    print("\n🎉 Done! Your prompt database is ready to use.")
    print("Try running: python prompt_cli.py list")

if __name__ == "__main__":
    main()
