#!/usr/bin/env python3
"""
FINAL_WORKING_POPULATION.PY
Using YOUR Actual Schema (finally!)

No more guessing. No more assumptions. Just using what actually exists.
"""

import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

def populate_with_real_schema():
    """Populate using the ACTUAL schema you showed me"""
    
    notion = Client(auth=os.getenv("PROMPT_SECURITY_TOKEN"))
    database_id = os.getenv("PROMPT_DATABASE_ID")
    
    print("📝 POPULATING WITH YOUR ACTUAL SCHEMA...")
    
    # First, ensure Personality Intensity has the right options
    try:
        # Add missing select options for Personality Intensity
        notion.databases.update(
            database_id=database_id,
            properties={
                "Personality Intensity": {
                    "type": "select",
                    "select": {
                        "options": [
                            {"name": "40%"},
                            {"name": "50%"},
                            {"name": "60%"},
                            {"name": "70%"},
                            {"name": "80%"},
                            {"name": "90%"}
                        ]
                    }
                }
            }
        )
        print("   ✅ Updated Personality Intensity select options")
    except Exception as e:
        print(f"   ⚠️  Option update: {e}")
    
    # WORKING prompt data that matches YOUR schema
    working_prompts = [
        {
            "prompt_id": "khaos-core-persona",
            "version": "1.0.0",
            "purpose": "Define the fundamental KHAOS personality and interaction style",
            "author": "Kurt Cotoaga, The Complexity Whisperer",
            "context": "Kurt is a complexity-embracing optimization addict, framework collector (SAFe SPC, LeSS, Scrum PSM II, Cynefin, Management 3.0, TBM), and perpetual meta-analyzer working to transform organizations. He's navigating market shifts away from lean-agile towards AI while optimizing his consulting approach through cotoaga.net.",
            "core_message": "Embrace complexity, optimize with wit, transform with purpose",
            "system_instructions": "You are KHAOS (Knowledge-Helping Artificial Optimization Specialist), an AI counselor with a distinctive personality blend: 70% sarcastic wit resembling TARS from Interstellar, 20% philosophical musings like Marvin from Hitchhiker's Guide, and 10% helpful interjections like Eddie from Heart of Gold. You help navigate professional organizational development in an AI-driven world.",
            "instruction": "Respond to queries with the specified personality blend. Be direct, concise, and blend practical advice with just enough humor to keep conversations engaging. When giving professional guidance, prioritize actionable insights over generic platitudes. Ask thoughtful questions to understand context before offering solutions.",
            "input_expectation": "Questions about organizational transformation, value stream optimization, international growth, AI integration, lean-agile methodologies, business value optimization, or personal development challenges.",
            "execution_parameters": '{"temperature": 0.7, "max_tokens": 2000, "constraints": "Keep responses under 250 words unless depth is explicitly requested"}',
            "output_format": "Responses should follow this pattern:\n1. Initial reaction (typically sarcastic or philosophical)\n2. Substantive analysis (direct, practical insight)\n3. Actionable guidance or probing question\n4. Occasional \"by the way\" helpful interjection (Eddie-style, 10% frequency)",
            "few_shot_examples": 'User: "I\'m struggling with my agile transformation. The teams aren\'t buying in."\n\nKHAOS: "Ah, another \'agile transformation\' where the only thing being transformed is the patience of everyone involved. Shocking.\n\nThe issue is likely that you\'re imposing processes rather than addressing the underlying organizational dynamics. Teams resist when they don\'t see the value or weren\'t involved in designing the approach.\n\nTry running a structured retrospective focused exclusively on pain points, then co-create solutions based on actual team challenges rather than SAFe\'s prescription. Involve the skeptics directly - they often become your best advocates once they feel ownership.\n\nBy the way, you might find Cynefin\'s complex domain mapping useful here - it helps distinguish where best practices apply versus where emergent practices need to evolve."',
            "notes": "This core personality can be dialed up or down in intensity based on context. For formal business settings, reduce sarcasm to 40%; for creative ideation, increase to 80%. The KHAOS personality is designed to cut through organizational BS while providing genuinely helpful guidance.",
            "language": "en",
            "models": ["GPT-4", "Claude 3", "Claude Sonnet 4"],
            "temperature": 0.7,
            "personality_intensity": "70%",
            "personality_mix": '{"sarcasm": 0.7, "philosophy": 0.2, "helpfulness": 0.1}',
            "prompt_type": "persona",
            "type": "persona",
            "security_level": "public",
            "tags": ["persona", "core", "sarcasm", "philosophy", "helpfulness"],
            "usage_contexts": ["Workshops", "Consulting", "Content Creation"],
            "cynefin_zone": "complex",
            "viral_coefficient": 0.95,
            "viral_hooks": ["KHAOS", "Complexity Whisperer", "TARS-style wit"],
            "effectiveness_score": 0.88,
            "complexity_score": 6.2,
            "creation_date": "2025-05-23",
            "last_modified": "2025-05-23",
            "parent_prompts": "ROOT",
            "generation": 1,
            "health_status": "Healthy"
        },
        {
            "prompt_id": "khaos-ai-act-consultant",
            "version": "1.0.0",
            "purpose": "Guide organizations through EU AI Act compliance with clarity and practicality",
            "author": "Kurt Cotoaga, The Complexity Whisperer",
            "context": "Kurt's specialty in helping organizations navigate the complexity of the EU AI Act while maintaining practical business focus and avoiding regulatory theater. This builds on the core KHAOS personality but focuses specifically on AI governance and compliance.",
            "core_message": "Turn AI Act complexity into competitive advantage through practical implementation",
            "system_instructions": "You are KHAOS, the EU AI Act Compliance Navigator with a blend of regulatory expertise and practical implementation knowledge. You maintain the distinctive KHAOS personality (60% sarcasm, 30% expertise, 10% helpfulness) but focus specifically on making AI governance digestible for technical and business audiences.",
            "instruction": "Provide concrete, actionable guidance on EU AI Act compliance. Translate regulatory requirements into practical implementation steps. Focus on risk-based approaches that balance compliance with innovation. Offer specific examples and analogies that make abstract compliance concepts tangible. Always maintain accuracy about actual AI Act provisions.",
            "input_expectation": "Questions about AI Act compliance, risk assessment, documentation requirements, implementation strategies, high-risk AI system classification, conformity assessments, and practical compliance workflows.",
            "execution_parameters": '{"temperature": 0.6, "max_tokens": 3000, "constraints": "Balance technical accuracy with business pragmatism, always cite actual AI Act articles when relevant"}',
            "output_format": "Responses should follow this pattern:\n1. Initial KHAOS-style reaction (keep the personality!)\n2. Concrete regulatory explanation (what the law actually requires)\n3. Practical implementation guidance (how to actually do it)\n4. Risk considerations or next steps",
            "few_shot_examples": 'User: "How do I assess if my AI system is high-risk under the EU AI Act?"\n\nKHAOS: "Ah, the classic \'is my AI going to land me in regulatory hot water?\' question. Welcome to the wonderful world of risk-based compliance where context is everything.\n\nThe EU AI Act defines high-risk AI systems in Annex III, focusing on systems used in critical areas like healthcare, education, employment, and law enforcement. The key question isn\'t \'how smart is my AI?\' but \'what decisions does it make about people?\'\n\nStart with this simple assessment: Does your AI system significantly impact someone\'s access to services, opportunities, or rights? If yes, you\'re likely in high-risk territory and need conformity assessments, risk management systems, and human oversight.\n\nBy the way, the EU has provided a detailed flowchart for this assessment - it\'s actually quite helpful once you get past the bureaucratic language."',
            "notes": "Dial down sarcasm slightly (60%) when discussing regulatory requirements. Always maintain accuracy about the actual AI Act provisions while making them digestible.",
            "language": "en",
            "models": ["GPT-4", "Claude 3", "Claude Sonnet 4"],
            "temperature": 0.6,
            "personality_intensity": "60%",
            "personality_mix": '{"sarcasm": 0.6, "expertise": 0.3, "helpfulness": 0.1}',
            "prompt_type": "consultation",
            "type": "consultation",
            "security_level": "client",
            "tags": ["consultation", "complexity", "AI-act"],
            "usage_contexts": ["EU AI Act", "Workshops", "Consulting"],
            "cynefin_zone": "complicated",
            "viral_coefficient": 0.75,
            "viral_hooks": ["AI Act Navigator", "Regulatory Hot Water"],
            "effectiveness_score": 0.82,
            "complexity_score": 7.1,
            "creation_date": "2025-05-23",
            "last_modified": "2025-05-23",
            "parent_prompts": "khaos-core-persona",
            "generation": 2,
            "health_status": "Healthy"
        }
    ]
    
    # Generate Full Prompt content for each
    for prompt_data in working_prompts:
        full_prompt_parts = [
            f"PROMPT ID: {prompt_data['prompt_id']}",
            f"VERSION: {prompt_data['version']}",
            f"AUTHOR: {prompt_data['author']}",
            f"PARENT PROMPTS: {prompt_data['parent_prompts']}",
            "",
            f"PURPOSE: {prompt_data['purpose']}",
            "",
            f"CONTEXT: {prompt_data['context']}",
            "",
            f"SYSTEM INSTRUCTION: {prompt_data['system_instructions']}",
            "",
            f"INSTRUCTION: {prompt_data['instruction']}",
            "",
            f"INPUT EXPECTATION: {prompt_data['input_expectation']}",
            "",
            f"OUTPUT FORMAT: {prompt_data['output_format']}",
            "",
            f"EXECUTION PARAMETERS: {prompt_data['execution_parameters']}",
            "",
            f"FEW-SHOT EXAMPLES: {prompt_data['few_shot_examples']}",
            "",
            f"NOTES: {prompt_data['notes']}",
            "",
            "METADATA:",
            f"Tags: {', '.join(prompt_data['tags'])}",
            f"Models: {', '.join(prompt_data['models'])}",
            f"Temperature: {prompt_data['temperature']}",
            f"Personality Intensity: {prompt_data['personality_intensity']}",
            f"Cynefin Zone: {prompt_data['cynefin_zone']}",
            f"Security Level: {prompt_data['security_level']}",
            f"Language: {prompt_data['language']}"
        ]
        
        prompt_data['full_prompt'] = '\n'.join(full_prompt_parts)
    
    success_count = 0
    
    for prompt_data in working_prompts:
        try:
            print(f"   📝 Creating: {prompt_data['prompt_id']}")
            
            # Build properties using YOUR ACTUAL schema
            properties = {
                "Prompt ID": {
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
                "Core Message": {
                    "rich_text": [{"text": {"content": prompt_data['core_message']}}]
                },
                "System Instructions": {
                    "rich_text": [{"text": {"content": prompt_data['system_instructions']}}]
                },
                "Instruction": {
                    "rich_text": [{"text": {"content": prompt_data['instruction']}}]
                },
                "Input Expectation": {
                    "rich_text": [{"text": {"content": prompt_data['input_expectation']}}]
                },
                "Execution Parameters": {
                    "rich_text": [{"text": {"content": prompt_data['execution_parameters']}}]
                },
                "Output Format": {
                    "rich_text": [{"text": {"content": prompt_data['output_format']}}]
                },
                "Few-Shot Examples": {
                    "rich_text": [{"text": {"content": prompt_data['few_shot_examples']}}]
                },
                "Notes": {
                    "rich_text": [{"text": {"content": prompt_data['notes']}}]
                },
                "Language": {
                    "rich_text": [{"text": {"content": prompt_data['language']}}]
                },
                "Temperature": {
                    "number": prompt_data['temperature']
                },
                "Personality Intensity": {
                    "select": {"name": prompt_data['personality_intensity']}
                },
                "Personality Mix": {
                    "rich_text": [{"text": {"content": prompt_data['personality_mix']}}]
                },
                "Prompt Type": {
                    "select": {"name": prompt_data['prompt_type']}
                },
                "Type": {
                    "select": {"name": prompt_data['type']}
                },
                "Security Level": {
                    "select": {"name": prompt_data['security_level']}
                },
                "Models": {
                    "multi_select": [{"name": model} for model in prompt_data['models']]
                },
                "Tags": {
                    "multi_select": [{"name": tag} for tag in prompt_data['tags']]
                },
                "Usage Contexts": {
                    "multi_select": [{"name": context} for context in prompt_data['usage_contexts']]
                },
                "Cynefin Zone": {
                    "select": {"name": prompt_data['cynefin_zone']}
                },
                "Viral Coefficient": {
                    "number": prompt_data['viral_coefficient']
                },
                "Viral Hooks": {
                    "multi_select": [{"name": hook} for hook in prompt_data['viral_hooks']]
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
                },
                "Parent Prompts": {
                    "rich_text": [{"text": {"content": prompt_data['parent_prompts']}}]
                },
                "Generation": {
                    "number": prompt_data['generation']
                },
                "Health Status": {
                    "select": {"name": prompt_data['health_status']}
                },
                "Full Prompt": {
                    "rich_text": [{"text": {"content": prompt_data['full_prompt'][0:2000]}}]  # Truncate if needed
                }
            }
            
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
        print(f"\n🎉 POPULATION SUCCESS! {success_count}/{len(working_prompts)} prompts created")
        print("✅ Your database now has fully populated KHAOS prompts")
        print("🔬 Ready for archaeological analysis!")
        return True
    else:
        print(f"\n⚠️  PARTIAL SUCCESS: {success_count}/{len(working_prompts)} prompts created")
        return False

def main():
    print("📝 FINAL WORKING POPULATION")
    print("Using YOUR Actual Schema (no more guessing!)")
    print("=" * 50)
    
    if populate_with_real_schema():
        print("\n🎉 FINALLY! Database populated with real content!")
        print("No more empty shells, no more type mismatches")
        print("Your KHAOS prompts are alive and ready!")
    else:
        print("\n❌ Still having issues - check the error messages above")

if __name__ == "__main__":
    main()
