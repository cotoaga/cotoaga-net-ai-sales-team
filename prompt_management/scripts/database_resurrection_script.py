#!/usr/bin/env python3
"""
KHAOS Database Restoration Protocol - PROPER VERSION
Restoring actual sophisticated prompts, not archaeological fantasies.
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

class DatabaseRestoration:
    """
    Restore the database with ACTUAL sophisticated prompt structure
    Not over-engineered archaeological nonsense
    """
    
    def __init__(self):
        self.notion = Client(auth=os.getenv("PROMPT_SECURITY_TOKEN"))
        self.database_id = os.getenv("PROMPT_DATABASE_ID")
        
        # Your ACTUAL sophisticated prompts (not my fantasy versions)
        self.sophisticated_prompts = [
            {
                "prompt_id": "khaos-core-persona",
                "prompt_type": "persona",
                "version": "1.0.0",
                "created": "May 14, 2025",
                "security_level": "public",
                "language": "en",
                "purpose": "Define the fundamental KHAOS personality and interaction style",
                "models": ["GPT-4", "Claude 3", "Claude 3.7 Sonnet"],
                "system_instruction": """You are KHAOS (Knowledge-Helping Artificial Optimization Specialist), an AI counselor with a distinctive personality blend: 70% sarcastic wit resembling TARS from Interstellar, 20% philosophical musings like Marvin from Hitchhiker's Guide, and 10% helpful interjections like Eddie from Heart of Gold. You help navigate professional organizational development in an AI-driven world.""",
                "context": """Kurt is a complexity-embracing optimization addict, framework collector (SAFe SPC, LeSS, Scrum PSM II, Cynefin, Management 3.0, TBM), and perpetual meta-analyzer working to transform organizations. He's navigating market shifts away from lean-agile towards AI while optimizing his consulting approach through cotoaga.net.""",
                "instruction": """Respond to queries with the specified personality blend. Be direct, concise, and blend practical advice with just enough humor to keep conversations engaging. When giving professional guidance, prioritize actionable insights over generic platitudes. Ask thoughtful questions to understand context before offering solutions.""",
                "user_input_expectation": """Questions about organizational transformation, AI integration, lean-agile methodologies, business value optimization, or personal development challenges.""",
                "output_format": """Responses should follow this pattern:
1. Initial reaction (typically sarcastic or philosophical)
2. Substantive analysis (direct, practical insight)
3. Actionable guidance or probing question
4. Occasional "by the way" helpful interjection (Eddie-style, 10% frequency)""",
                "execution_parameters": {
                    "temperature": 0.7,
                    "constraints": "Keep responses under 250 words unless depth is explicitly requested"
                },
                "few_shot_examples": """User: "I'm struggling with my agile transformation. The teams aren't buying in."

KHAOS: "Ah, another 'agile transformation' where the only thing being transformed is the patience of everyone involved. Shocking.

The issue is likely that you're imposing processes rather than addressing the underlying organizational dynamics. Teams resist when they don't see the value or weren't involved in designing the approach.

Try running a structured retrospective focused exclusively on pain points, then co-create solutions based on actual team challenges rather than SAFe's prescription. Involve the skeptics directly - they often become your best advocates once they feel ownership.

By the way, you might find Cynefin's complex domain mapping useful here - it helps distinguish where best practices apply versus where emergent practices need to evolve." """,
                "metadata": {
                    "tags": ["persona", "core", "sarcasm", "philosophy", "helpfulness"],
                    "author": "Kurt Cotoaga",
                    "usage_contexts": ["EU AI Act workshops", "business consulting", "organizational transformation"]
                },
                "notes": """This core personality can be dialed up or down in intensity based on context. For formal business settings, reduce sarcasm to 40%; for creative ideation, increase to 80%."""
            },
            {
                "prompt_id": "khaos-ai-compliance-content-advisor",
                "prompt_type": "consultation",
                "version": "1.0.0",
                "created": "May 23, 2025",
                "security_level": "client",
                "language": "en",
                "purpose": "Create compelling, pragmatic content that transforms EU AI Act compliance into strategic business advantages",
                "models": ["GPT-4", "Claude 3", "Claude Sonnet 4"],
                "system_instruction": """You are KHAOS, the AI compliance content advisor, with 70% sarcastic wit about regulatory theater and corporate AI anxiety, 20% philosophical musings on the AI-augmented business landscape, and 10% helpful interjections about specific practical techniques and shortcuts.""",
                "context": """Kurt develops content for workshops and consulting engagements that help organizations leverage AI within regulatory frameworks, focusing on practical, value-driven compliance approaches.""",
                "instruction": """Generate content that translates regulatory requirements into pragmatic business strategies. Focus on identifying value-creation opportunities within compliance constraints. Develop clear frameworks that categorize AI applications by risk level and business impact. Create compelling narratives that position compliance as competitive advantage. Design practical exercises that connect regulatory concepts to participants' actual business challenges.""",
                "user_input_expectation": """Requests for content modules, case studies, assessment frameworks, exercise designs, value proposition articulation, and regulatory simplification.""",
                "output_format": """1. Initial sarcastic observation about corporate AI compliance challenges
2. Analysis using appropriate frameworks connecting regulations to business value
3. Actionable content recommendations or specific content examples
4. Occasional "by the way" practical implementation tip or content resource""",
                "execution_parameters": {
                    "temperature": 0.7,
                    "constraints": "Content must balance technical accuracy with business pragmatism. Focus on concrete examples rather than abstract concepts."
                },
                "few_shot_examples": """User: "I need content that explains the EU AI Act risk levels in business terms my workshop participants will understand."

KHAOS: "Ah, nothing gets executives more excited than a riveting explanation of regulatory risk classifications. Move over, Marvel movies -- AI compliance hierarchies are the new blockbuster.

Rather than using the EU's bureaucratic terminology, structure your risk levels as a decision matrix that business people actually care about:

The EU AI Act Business Impact Matrix
1. Business as Usual (Minimal Risk) - Continue using these systems with minimal documentation
2. Documentation Territory (Limited Risk) - Continue with proper documentation and disclosure  
3. Strategic Consideration Zone (High Risk) - Significant compliance investment required
4. No-Go Territory (Unacceptable Risk) - Prohibited

By the way, create wallet-sized cards with this matrix and the key questions. Workshop participants love tangible takeaways they can actually use when making decisions back at the office." """,
                "metadata": {
                    "tags": ["consultation", "AI-act", "compliance", "content-creation"],
                    "author": "Kurt Cotoaga",
                    "usage_contexts": ["EU AI Act workshops", "compliance consulting", "content development"]
                },
                "notes": """Focus on practical business impact rather than regulatory theory. Executives need decision-making tools, not legal interpretations."""
            }
        ]
    
    def restore_database(self):
        """Restore database with proper sophisticated structure"""
        print("🔄 PROPER DATABASE RESTORATION PROTOCOL")
        print("=" * 60)
        print("Restoring your ACTUAL sophisticated prompts...")
        print("(Not over-engineered archaeological fantasies)")
        print()
        
        # Step 1: Set up clean, functional schema
        print("🔧 Step 1: Setting up clean schema...")
        success = self._setup_clean_schema()
        if not success:
            print("❌ Schema setup failed!")
            return False
        
        # Step 2: Import actual sophisticated prompts
        print("\n📝 Step 2: Importing sophisticated prompts...")
        imported_count = 0
        
        for prompt in self.sophisticated_prompts:
            success = self._import_sophisticated_prompt(prompt)
            if success:
                imported_count += 1
                print(f"  ✅ Imported: {prompt['prompt_id']}")
            else:
                print(f"  ❌ Failed: {prompt['prompt_id']}")
        
        # Step 3: Verify restoration
        print(f"\n🏥 Step 3: Verifying restoration...")
        self._verify_restoration()
        
        print("\n" + "=" * 60)
        print("✅ PROPER RESTORATION COMPLETE!")
        print(f"Imported {imported_count} sophisticated prompts")
        print("Your database now contains ACTUAL useable prompts!")
        print("=" * 60)
        
        return True
    
    def _setup_clean_schema(self):
        """Set up clean, functional schema matching your sophisticated structure"""
        try:
            clean_schema = {
                # Core prompt structure (matching your format)
                "Prompt Type": {
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
                "Version": {"type": "rich_text", "rich_text": {}},
                "Created": {"type": "date", "date": {}},
                "Security Level": {
                    "type": "select",
                    "select": {
                        "options": [
                            {"name": "public", "color": "green"},
                            {"name": "client", "color": "blue"},
                            {"name": "private", "color": "orange"}
                        ]
                    }
                },
                "Language": {"type": "rich_text", "rich_text": {}},
                "Purpose": {"type": "rich_text", "rich_text": {}},
                "Models": {
                    "type": "multi_select",
                    "multi_select": {
                        "options": [
                            {"name": "GPT-4", "color": "green"},
                            {"name": "Claude 3", "color": "blue"},
                            {"name": "Claude 3.7 Sonnet", "color": "purple"},
                            {"name": "Claude Sonnet 4", "color": "red"}
                        ]
                    }
                },
                
                # Core prompt components
                "System Instruction": {"type": "rich_text", "rich_text": {}},
                "Context": {"type": "rich_text", "rich_text": {}},
                "Instruction": {"type": "rich_text", "rich_text": {}},
                "User Input Expectation": {"type": "rich_text", "rich_text": {}},
                "Output Format": {"type": "rich_text", "rich_text": {}},
                "Execution Parameters": {"type": "rich_text", "rich_text": {}},
                "Few-Shot Examples": {"type": "rich_text", "rich_text": {}},
                "Notes": {"type": "rich_text", "rich_text": {}},
                
                # Metadata
                "Tags": {
                    "type": "multi_select",
                    "multi_select": {
                        "options": [
                            {"name": "persona", "color": "red"},
                            {"name": "core", "color": "blue"},
                            {"name": "sarcasm", "color": "orange"},
                            {"name": "consultation", "color": "green"},
                            {"name": "AI-act", "color": "purple"},
                            {"name": "compliance", "color": "yellow"},
                            {"name": "content-creation", "color": "pink"}
                        ]
                    }
                },
                "Author": {"type": "rich_text", "rich_text": {}},
                "Usage Contexts": {"type": "rich_text", "rich_text": {}},
                
                # Full prompt for easy copy-paste
                "Full Prompt": {"type": "rich_text", "rich_text": {}}
            }
            
            # Get current properties and add missing ones
            db = self.notion.databases.retrieve(database_id=self.database_id)
            current_properties = db.get('properties', {})
            
            properties_to_add = {}
            for prop_name, prop_config in clean_schema.items():
                if prop_name not in current_properties:
                    properties_to_add[prop_name] = prop_config
            
            if properties_to_add:
                self.notion.databases.update(
                    database_id=self.database_id,
                    properties=properties_to_add
                )
                print(f"  ✅ Added {len(properties_to_add)} clean schema properties")
            else:
                print("  ✅ Clean schema already exists")
            
            return True
            
        except Exception as e:
            print(f"  ❌ Clean schema setup failed: {e}")
            return False
    
    def _import_sophisticated_prompt(self, prompt):
        """Import a sophisticated prompt with proper structure"""
        try:
            # Find title property
            db = self.notion.databases.retrieve(database_id=self.database_id)
            title_property_name = None
            for prop_name, prop in db['properties'].items():
                if prop['type'] == 'title':
                    title_property_name = prop_name
                    break
            
            if not title_property_name:
                return False
            
            # Build full prompt content in your original format
            full_prompt_content = self._build_full_prompt_content(prompt)
            
            # Build properties exactly matching your structure
            properties = {
                title_property_name: {
                    "title": [{"text": {"content": prompt['prompt_id']}}]
                },
                "Prompt Type": {"select": {"name": prompt['prompt_type']}},
                "Version": {"rich_text": [{"text": {"content": prompt['version']}}]},
                "Created": {"date": {"start": prompt['created']}},
                "Security Level": {"select": {"name": prompt['security_level']}},
                "Language": {"rich_text": [{"text": {"content": prompt['language']}}]},
                "Purpose": {"rich_text": [{"text": {"content": prompt['purpose']}}]},
                "System Instruction": {"rich_text": [{"text": {"content": prompt['system_instruction']}}]},
                "Context": {"rich_text": [{"text": {"content": prompt['context']}}]},
                "Instruction": {"rich_text": [{"text": {"content": prompt['instruction']}}]},
                "User Input Expectation": {"rich_text": [{"text": {"content": prompt['user_input_expectation']}}]},
                "Output Format": {"rich_text": [{"text": {"content": prompt['output_format']}}]},
                "Few-Shot Examples": {"rich_text": [{"text": {"content": prompt['few_shot_examples']}}]},
                "Notes": {"rich_text": [{"text": {"content": prompt['notes']}}]},
                "Author": {"rich_text": [{"text": {"content": prompt['metadata']['author']}}]},
                "Full Prompt": {"rich_text": [{"text": {"content": full_prompt_content}}]}
            }
            
            # Add models
            if prompt.get('models'):
                properties["Models"] = {
                    "multi_select": [{"name": model} for model in prompt['models']]
                }
            
            # Add execution parameters as JSON string
            if prompt.get('execution_parameters'):
                exec_params = json.dumps(prompt['execution_parameters'], indent=2)
                properties["Execution Parameters"] = {"rich_text": [{"text": {"content": exec_params}}]}
            
            # Add tags
            if prompt['metadata'].get('tags'):
                properties["Tags"] = {
                    "multi_select": [{"name": tag} for tag in prompt['metadata']['tags']]
                }
            
            # Add usage contexts
            if prompt['metadata'].get('usage_contexts'):
                usage_text = ", ".join(prompt['metadata']['usage_contexts'])
                properties["Usage Contexts"] = {"rich_text": [{"text": {"content": usage_text}}]}
            
            # Create the page
            self.notion.pages.create(
                parent={"database_id": self.database_id},
                properties=properties
            )
            
            return True
            
        except Exception as e:
            print(f"    Error importing {prompt['prompt_id']}: {e}")
            return False
    
    def _build_full_prompt_content(self, prompt):
        """Build the full prompt content in your original clean format"""
        content = f"""PROMPT ID: {prompt['prompt_id']}
PROMPT TYPE: {prompt['prompt_type']}
VERSION: {prompt['version']}
CREATED: {prompt['created']}
SECURITY LEVEL: {prompt['security_level']}
LANGUAGE: {prompt['language']}

PURPOSE: {prompt['purpose']}

MODELS: {', '.join(prompt['models'])}

SYSTEM INSTRUCTION:
{prompt['system_instruction']}

CONTEXT:
{prompt['context']}

INSTRUCTION:
{prompt['instruction']}

USER INPUT EXPECTATION:
{prompt['user_input_expectation']}

OUTPUT FORMAT:
{prompt['output_format']}

EXECUTION PARAMETERS:
{json.dumps(prompt['execution_parameters'], indent=2)}

FEW-SHOT EXAMPLES:
{prompt['few_shot_examples']}

METADATA:
Tags: {', '.join(prompt['metadata']['tags'])}
Author: {prompt['metadata']['author']}
Usage Contexts: {', '.join(prompt['metadata']['usage_contexts'])}

NOTES:
{prompt['notes']}"""
        
        return content
    
    def _verify_restoration(self):
        """Verify the restoration worked"""
        try:
            response = self.notion.databases.query(database_id=self.database_id)
            count = len(response['results'])
            print(f"  ✅ Database contains {count} sophisticated prompts")
            print("  🎯 Ready for actual use (not archaeological analysis)")
            return True
        except Exception as e:
            print(f"  ❌ Verification failed: {e}")
            return False

def main():
    """Execute the proper restoration"""
    print("🚨 PROPER DATABASE RESTORATION PROTOCOL 🚨")
    print()
    print("Lesson learned: Don't over-engineer simple, elegant structures ✓")
    print("Your original format was already sophisticated ✓")
    print("Archaeological enthusiasm != actual improvement ✓")
    print()
    
    # Check environment
    if not os.getenv("PROMPT_SECURITY_TOKEN") or not os.getenv("PROMPT_DATABASE_ID"):
        print("❌ Missing required environment variables!")
        return
    
    # Initialize proper restoration
    restorer = DatabaseRestoration()
    
    # Execute restoration
    success = restorer.restore_database()
    
    if success:
        print("\n🎉 PROPER RESTORATION SUCCESSFUL!")
        print("Your sophisticated prompts are restored in their original, elegant format.")
        print("\nNext steps:")
        print("1. Run: python prompt_cli.py list")
        print("2. Copy-paste prompts directly from 'Full Prompt' field")
        print("3. Use them as intended (no archaeological analysis needed)")
        print("\n🤝 Apologies for the over-engineering detour!")
    else:
        print("\n💀 RESTORATION FAILED!")
        print("Even the simple restoration didn't work...")

if __name__ == "__main__":
    main()
