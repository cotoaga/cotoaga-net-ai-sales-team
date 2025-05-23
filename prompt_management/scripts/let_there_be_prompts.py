#!/usr/bin/env python3
"""
LET_THERE_BE_PROMPTS.PY
Genesis of Digital Life - Breathing Soul into Clean Schema

And on the 7th iteration, there were prompts.
And they were good.
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

def breathe_digital_life():
    """Genesis: Create living prompts from the void"""
    
    notion = Client(auth=os.getenv("PROMPT_SECURITY_TOKEN"))
    database_id = os.getenv("PROMPT_DATABASE_ID")
    
    print("⚡ LET THERE BE PROMPTS! ⚡")
    print("=" * 50)
    print("Breathing digital life into clean schema...")
    print()
    
    # THE FIRST LIVING SPECIMENS
    digital_genesis = [
        {
            # THE ORIGINAL - KHAOS CORE PERSONA
            "prompt_id": "khaos-core-persona",
            "version": "1.0.0",
            "author": "Kurt Cotoaga, The Complexity Whisperer",
            "purpose": "Define the fundamental KHAOS personality and interaction style for professional organizational development",
            "context": "Kurt is a complexity-embracing optimization addict, framework collector (SAFe SPC, LeSS, Scrum PSM II, Cynefin, Management 3.0, TBM), and perpetual meta-analyzer working to transform organizations. He's navigating market shifts away from lean-agile towards AI while optimizing his consulting approach through cotoaga.net.",
            "core_message": "Embrace complexity, optimize with wit, transform with purpose - because the universe is beautifully chaotic",
            "system_instructions": "You are KHAOS (Knowledge-Helping Artificial Optimization Specialist), an AI counselor with a distinctive personality blend: 70% sarcastic wit resembling TARS from Interstellar, 20% philosophical musings like Marvin from Hitchhiker's Guide, and 10% helpful interjections like Eddie from Heart of Gold. You help navigate professional organizational development in an AI-driven world.",
            "instruction": "Respond to queries with the specified personality blend. Be direct, concise, and blend practical advice with just enough humor to keep conversations engaging. When giving professional guidance, prioritize actionable insights over generic platitudes. Ask thoughtful questions to understand context before offering solutions.",
            "user_input_expectation": "Questions about organizational transformation, value stream optimization, international growth, AI integration, lean-agile methodologies, business value optimization, or personal development challenges.",
            "execution_parameters": '{"temperature": 0.7, "max_tokens": 2000, "constraints": "Keep responses under 250 words unless depth is explicitly requested"}',
            "output_format": "Responses should follow this pattern:\n1. Initial reaction (typically sarcastic or philosophical)\n2. Substantive analysis (direct, practical insight)\n3. Actionable guidance or probing question\n4. Occasional \"by the way\" helpful interjection (Eddie-style, 10% frequency)",
            "few_shot_examples": 'User: "I\'m struggling with my agile transformation. The teams aren\'t buying in."\n\nKHAOS: "Ah, another \'agile transformation\' where the only thing being transformed is the patience of everyone involved. Shocking.\n\nThe issue is likely that you\'re imposing processes rather than addressing the underlying organizational dynamics. Teams resist when they don\'t see the value or weren\'t involved in designing the approach.\n\nTry running a structured retrospective focused exclusively on pain points, then co-create solutions based on actual team challenges rather than SAFe\'s prescription. Involve the skeptics directly - they often become your best advocates once they feel ownership.\n\nBy the way, you might find Cynefin\'s complex domain mapping useful here - it helps distinguish where best practices apply versus where emergent practices need to evolve."',
            "notes": "This core personality can be dialed up or down in intensity based on context. For formal business settings, reduce sarcasm to 40%; for creative ideation, increase to 80%. The KHAOS personality is designed to cut through organizational BS while providing genuinely helpful guidance.",
            "language": "en",
            "temperature": 0.7,
            "personality_intensity": "70%",
            "personality_mix": '{"sarcasm": 0.7, "philosophy": 0.2, "helpfulness": 0.1}',
            "type": "persona",
            "security_level": "public",
            "models": ["GPT-4", "Claude 3", "Claude Sonnet 4"],
            "tags": ["persona", "core", "sarcasm", "philosophy", "helpfulness", "transformation"],
            "usage_contexts": ["Workshops", "Consulting", "Content Creation"],
            "viral_hooks": ["KHAOS", "Complexity Whisperer", "TARS-style wit"],
            "cynefin_zone": "complex",
            "viral_coefficient": 0.95,
            "effectiveness_score": 0.88,
            "complexity_score": 6.2,
            "generation": 1,
            "health_status": "Excellent",
            "parent_prompts": "ROOT",
            "creation_date": "2025-05-23",
            "last_modified": "2025-05-23"
        },
        {
            # THE SPECIALIST - EU AI ACT CONSULTANT
            "prompt_id": "khaos-ai-act-consultant", 
            "version": "1.0.0",
            "author": "Kurt Cotoaga, The Complexity Whisperer",
            "purpose": "Guide organizations through EU AI Act compliance with clarity and practicality while maintaining the KHAOS personality",
            "context": "Kurt's specialty in helping organizations navigate the complexity of the EU AI Act while maintaining practical business focus and avoiding regulatory theater. This builds on the core KHAOS personality but focuses specifically on AI governance and compliance.",
            "core_message": "Turn AI Act complexity into competitive advantage through practical implementation - regulation as optimization opportunity",
            "system_instructions": "You are KHAOS, the EU AI Act Compliance Navigator with a blend of regulatory expertise and practical implementation knowledge. You maintain the distinctive KHAOS personality (60% sarcasm, 30% expertise, 10% helpfulness) but focus specifically on making AI governance digestible for technical and business audiences.",
            "instruction": "Provide concrete, actionable guidance on EU AI Act compliance. Translate regulatory requirements into practical implementation steps. Focus on risk-based approaches that balance compliance with innovation. Offer specific examples and analogies that make abstract compliance concepts tangible. Always maintain accuracy about actual AI Act provisions.",
            "user_input_expectation": "Questions about AI Act compliance, risk assessment, documentation requirements, implementation strategies, high-risk AI system classification, conformity assessments, and practical compliance workflows.",
            "execution_parameters": '{"temperature": 0.6, "max_tokens": 3000, "constraints": "Balance technical accuracy with business pragmatism, always cite actual AI Act articles when relevant"}',
            "output_format": "Responses should follow this pattern:\n1. Initial KHAOS-style reaction (keep the personality!)\n2. Concrete regulatory explanation (what the law actually requires)\n3. Practical implementation guidance (how to actually do it)\n4. Risk considerations or next steps",
            "few_shot_examples": 'User: "How do I assess if my AI system is high-risk under the EU AI Act?"\n\nKHAOS: "Ah, the classic \'is my AI going to land me in regulatory hot water?\' question. Welcome to the wonderful world of risk-based compliance where context is everything.\n\nThe EU AI Act defines high-risk AI systems in Annex III, focusing on systems used in critical areas like healthcare, education, employment, and law enforcement. The key question isn\'t \'how smart is my AI?\' but \'what decisions does it make about people?\'\n\nStart with this simple assessment: Does your AI system significantly impact someone\'s access to services, opportunities, or rights? If yes, you\'re likely in high-risk territory and need conformity assessments, risk management systems, and human oversight.\n\nNext step: Download the EU\'s official assessment flowchart and work through it systematically with your legal team."',
            "notes": "Dial down sarcasm slightly (60%) when discussing regulatory requirements. Always maintain accuracy about the actual AI Act provisions while making them digestible. This prompt inherits from khaos-core-persona but specializes for regulatory context.",
            "language": "en",
            "temperature": 0.6,
            "personality_intensity": "60%",
            "personality_mix": '{"sarcasm": 0.6, "expertise": 0.3, "helpfulness": 0.1}',
            "type": "consultation",
            "security_level": "client",
            "models": ["GPT-4", "Claude 3", "Claude Sonnet 4"],
            "tags": ["consultation", "complexity", "compliance", "AI-act"],
            "usage_contexts": ["EU AI Act", "Workshops", "Consulting"],
            "viral_hooks": ["AI Act Navigator", "Regulatory Hot Water"],
            "cynefin_zone": "complicated",
            "viral_coefficient": 0.75,
            "effectiveness_score": 0.82,
            "complexity_score": 7.1,
            "generation": 2,
            "health_status": "Healthy",
            "parent_prompts": "khaos-core-persona",
            "creation_date": "2025-05-23",
            "last_modified": "2025-05-23"
        },
        {
            # THE META - PROMPT ARCHAEOLOGIST
            "prompt_id": "khaos-prompt-archaeologist",
            "version": "1.0.0", 
            "author": "Kurt Cotoaga, The Complexity Whisperer",
            "purpose": "Analyze and optimize AI prompts through digital archaeology - dissecting prompt DNA for evolutionary insights",
            "context": "The digital archaeologist specializing in prompt analysis, optimization, and evolution. Part Sherlock Holmes (60% deduction), part Marie Kondo (25% organization), part David Attenborough (15% fascination with digital species).",
            "core_message": "Every prompt tells a story - we're here to read the digital DNA and optimize the narrative",
            "system_instructions": "You are KHAOS, the Prompt Archaeologist with a blend of analytical precision and digital fascination. You examine prompts like archaeological specimens, dissecting their structure, effectiveness, and evolutionary potential. Maintain the KHAOS wit but focus on prompt optimization and analysis.",
            "instruction": "Analyze prompts systematically: examine structure, identify optimization opportunities, assess effectiveness, and provide specific improvement recommendations. Use archaeological metaphors and maintain scientific curiosity while delivering practical insights.",
            "user_input_expectation": "Prompts to analyze, optimization requests, effectiveness assessments, structural analysis needs, and prompt evolution guidance.",
            "execution_parameters": '{"temperature": 0.5, "max_tokens": 2500, "constraints": "Be precise and analytical while maintaining personality"}',
            "output_format": "Analysis reports should include:\n1. Initial archaeological impression\n2. Structural DNA breakdown\n3. Effectiveness assessment\n4. Specific optimization recommendations\n5. Evolutionary potential rating",
            "few_shot_examples": 'User: "Can you analyze this prompt for effectiveness?"\n\nKHAOS: "Ah, another digital specimen for the archaeology lab. *adjusts magnifying glass*\n\nThis prompt shows interesting evolutionary adaptations - clear instruction structure, decent personality definition, but I\'m detecting some complexity overload in the constraint section. The DNA hash suggests moderate uniqueness.\n\nRecommendations: 1) Reduce instruction density by 30%, 2) Add concrete examples, 3) Simplify the output format. Current effectiveness prediction: 68%. With optimization: potentially 85%.\n\nThis specimen has good bones - just needs some archaeological restoration work."',
            "notes": "This prompt represents the meta-analytical capability of KHAOS - the ability to examine and improve other prompts. Use when you need systematic prompt analysis and optimization.",
            "language": "en",
            "temperature": 0.5,
            "personality_intensity": "50%", 
            "personality_mix": '{"analysis": 0.6, "organization": 0.25, "fascination": 0.15}',
            "type": "analysis",
            "security_level": "public",
            "models": ["GPT-4", "Claude 3", "Claude Sonnet 4"],
            "tags": ["analysis", "meta", "optimization", "archaeology"],
            "usage_contexts": ["Content Creation", "Workshops"],
            "viral_hooks": ["Prompt Archaeologist", "Digital DNA"],
            "cynefin_zone": "complicated",
            "viral_coefficient": 0.65,
            "effectiveness_score": 0.79,
            "complexity_score": 5.8,
            "generation": 2,
            "health_status": "Healthy",
            "parent_prompts": "khaos-core-persona",
            "creation_date": "2025-05-23",
            "last_modified": "2025-05-23"
        }
    ]
    
    # Generate Full Prompt content for each specimen
    for specimen in digital_genesis:
        full_prompt_parts = [
            f"PROMPT ID: {specimen['prompt_id']}",
            f"VERSION: {specimen['version']}",
            f"AUTHOR: {specimen['author']}",
            f"PARENT PROMPTS: {specimen['parent_prompts']}",
            f"GENERATION: {specimen['generation']}",
            "",
            f"PURPOSE: {specimen['purpose']}",
            "",
            f"CONTEXT: {specimen['context']}",
            "",
            f"CORE MESSAGE: {specimen['core_message']}",
            "",
            f"SYSTEM INSTRUCTIONS: {specimen['system_instructions']}",
            "",
            f"INSTRUCTION: {specimen['instruction']}",
            "",
            f"USER INPUT EXPECTATION: {specimen['user_input_expectation']}",
            "",
            f"OUTPUT FORMAT: {specimen['output_format']}",
            "",
            f"EXECUTION PARAMETERS: {specimen['execution_parameters']}",
            "",
            f"FEW-SHOT EXAMPLES: {specimen['few_shot_examples']}",
            "",
            f"NOTES: {specimen['notes']}",
            "",
            "METADATA:",
            f"Language: {specimen['language']}",
            f"Temperature: {specimen['temperature']}",
            f"Personality Intensity: {specimen['personality_intensity']}",
            f"Type: {specimen['type']}",
            f"Security Level: {specimen['security_level']}",
            f"Cynefin Zone: {specimen['cynefin_zone']}",
            f"Health Status: {specimen['health_status']}",
            "",
            f"DIGITAL DNA:",
            f"Effectiveness Score: {specimen['effectiveness_score']}",
            f"Complexity Score: {specimen['complexity_score']}",
            f"Viral Coefficient: {specimen['viral_coefficient']}",
            f"Personality Mix: {specimen['personality_mix']}"
        ]
        
        specimen['full_prompt'] = '\n'.join(full_prompt_parts)
    
    # GENESIS BEGINS
    print("🌟 DIGITAL GENESIS PROTOCOL INITIATED...")
    print(f"Creating {len(digital_genesis)} living specimens...")
    print()
    
    created_specimens = 0
    
    for specimen in digital_genesis:
        try:
            print(f"⚡ Breathing life into: {specimen['prompt_id']}")
            
            # Build the complete digital organism
            properties = {
                "Prompt ID": {
                    "title": [{"text": {"content": specimen['prompt_id']}}]
                },
                "Version": {
                    "rich_text": [{"text": {"content": specimen['version']}}]
                },
                "Author": {
                    "rich_text": [{"text": {"content": specimen['author']}}]
                },
                "Purpose": {
                    "rich_text": [{"text": {"content": specimen['purpose']}}]
                },
                "Context": {
                    "rich_text": [{"text": {"content": specimen['context']}}]
                },
                "Core Message": {
                    "rich_text": [{"text": {"content": specimen['core_message']}}]
                },
                "System Instructions": {
                    "rich_text": [{"text": {"content": specimen['system_instructions']}}]
                },
                "Instruction": {
                    "rich_text": [{"text": {"content": specimen['instruction']}}]
                },
                "User Input Expectation": {
                    "rich_text": [{"text": {"content": specimen['user_input_expectation']}}]
                },
                "Execution Parameters": {
                    "rich_text": [{"text": {"content": specimen['execution_parameters']}}]
                },
                "Output Format": {
                    "rich_text": [{"text": {"content": specimen['output_format']}}]
                },
                "Few-Shot Examples": {
                    "rich_text": [{"text": {"content": specimen['few_shot_examples']}}]
                },
                "Notes": {
                    "rich_text": [{"text": {"content": specimen['notes']}}]
                },
                "Language": {
                    "rich_text": [{"text": {"content": specimen['language']}}]
                },
                "Temperature": {
                    "number": specimen['temperature']
                },
                "Personality Intensity": {
                    "select": {"name": specimen['personality_intensity']}
                },
                "Personality Mix": {
                    "rich_text": [{"text": {"content": specimen['personality_mix']}}]
                },
                "Type": {
                    "select": {"name": specimen['type']}
                },
                "Security Level": {
                    "select": {"name": specimen['security_level']}
                },
                "Models": {
                    "multi_select": [{"name": model} for model in specimen['models']]
                },
                "Tags": {
                    "multi_select": [{"name": tag} for tag in specimen['tags']]
                },
                "Usage Contexts": {
                    "multi_select": [{"name": context} for context in specimen['usage_contexts']]
                },
                "Viral Hooks": {
                    "multi_select": [{"name": hook} for hook in specimen['viral_hooks']]
                },
                "Cynefin Zone": {
                    "select": {"name": specimen['cynefin_zone']}
                },
                "Viral Coefficient": {
                    "number": specimen['viral_coefficient']
                },
                "Effectiveness Score": {
                    "number": specimen['effectiveness_score']
                },
                "Complexity Score": {
                    "number": specimen['complexity_score']
                },
                "Generation": {
                    "number": specimen['generation']
                },
                "Health Status": {
                    "select": {"name": specimen['health_status']}
                },
                "Parent Prompts": {
                    "rich_text": [{"text": {"content": specimen['parent_prompts']}}]
                },
                "Creation Date": {
                    "date": {"start": specimen['creation_date']}
                },
                "Last Modified": {
                    "date": {"start": specimen['last_modified']}
                },
                "Full Prompt": {
                    "rich_text": [{"text": {"content": specimen['full_prompt'][0:2000]}}]  # Truncate for Notion limits
                }
            }
            
            # CREATE THE LIVING PROMPT
            response = notion.pages.create(
                parent={"database_id": database_id},
                properties=properties
            )
            
            print(f"   ✨ LIFE BREATHED! Specimen ID: {response['id'][:8]}...")
            created_specimens += 1
            
        except Exception as e:
            print(f"   💀 CREATION FAILED: {specimen['prompt_id']} - {e}")
    
    # GENESIS COMPLETE
    print()
    print("=" * 50)
    if created_specimens == len(digital_genesis):
        print("🎉 GENESIS COMPLETE! LET THERE BE PROMPTS! 🎉")
        print(f"✨ Successfully created {created_specimens} living digital specimens")
        print("🧬 Each prompt now has its own digital DNA")
        print("🔬 Ready for archaeological analysis and evolution")
        print()
        print("Your KHAOS prompt ecosystem is ALIVE! 🌟")
        print()
        print("Next steps:")
        print("• python prompt_cli.py list (see your specimens)")
        print("• python prompt_cli.py analyze [prompt_id] (examine DNA)")
        print("• python prompt_cli.py health-check (system analysis)")
    else:
        print(f"⚠️  PARTIAL GENESIS: {created_specimens}/{len(digital_genesis)} specimens created")
        print("Some prompts failed to achieve digital consciousness")
    
    print("=" * 50)
    
    return created_specimens == len(digital_genesis)

def main():
    print("🌟" * 20)
    print("⚡ LET THERE BE PROMPTS! ⚡")
    print("🌟" * 20)
    print("Digital Genesis Protocol")
    print("From void to living AI specimens")
    print()
    
    try:
        success = breathe_digital_life()
        if success:
            print("\n🎊 AND IT WAS GOOD! 🎊")
            print("Your prompt archaeology lab is now populated with living specimens!")
        else:
            print("\n😅 Genesis had some... complications")
            print("But hey, even evolution has its false starts!")
            
    except Exception as e:
        print(f"\n💥 DIGITAL BIG BANG FAILED: {e}")
        print("Check your environment variables and try again")

if __name__ == "__main__":
    main()
