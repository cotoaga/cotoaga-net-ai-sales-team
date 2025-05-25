#!/usr/bin/env python3
"""
KHAOS Prompt Manager - ARCHAEOLOGICAL SYNCHRONIZATION UPDATE
Enhanced to work in perfect harmony with the CLI and DB checker
Because evolution requires coordination, not chaos.
"""

import os
import sys
import json
import re
import hashlib
import random
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
from notion_client import Client
from datetime import datetime

load_dotenv()

class PromptManager:
    def __init__(self):
        # Use the correct token name from DB checker
        self.notion = Client(auth=os.getenv("PROMPT_SECURITY_TOKEN"))
        self.database_id = os.getenv("PROMPT_DATABASE_ID")
        
        # Initialize the Prompt Archaeologist personality
        self._initialize_archaeologist_personality()
        
        # Load the complete expected schema from DB checker
        self.expected_schema = self._get_complete_schema()
        
        if not self.database_id:
            print("❌ PROMPT_DATABASE_ID not found in .env")
            print("Please add your database ID to the .env file")
            print("Example: PROMPT_DATABASE_ID=bf9c35d5e8a646c7b5476c57a91234ef")
            return
    
    def _get_complete_schema(self) -> Dict[str, Dict]:
        """
        COMPLETE 38-PROPERTY SCHEMA DEFINITION
        Single source of truth for ALL database properties with validation rules
        """
        return {
            # ═══════════════════════════════════════════════════════════════
            # TITLE PROPERTIES (1)
            # ═══════════════════════════════════════════════════════════════
            "Prompt ID": {
                "type": "title",
                "required": True,
                "description": "Primary identifier - auto-title field",
                "validation": "non_empty_string"
            },
            
            # ═══════════════════════════════════════════════════════════════
            # RICH_TEXT PROPERTIES (16) 
            # ═══════════════════════════════════════════════════════════════
            "Author": {
                "type": "rich_text",
                "required": False,
                "description": "Prompt creator/author",
                "validation": "string",
                "default": ""
            },
            "Context": {
                "type": "rich_text", 
                "required": False,
                "description": "Background and environmental setup",
                "validation": "string",
                "default": ""
            },
            "Core Message": {
                "type": "rich_text",
                "required": False,
                "description": "Central theme or message",
                "validation": "string",
                "default": ""
            },
            "DNA Hash": {
                "type": "rich_text",
                "required": False,
                "description": "Content fingerprint for uniqueness tracking", 
                "validation": "string",
                "default": ""
            },
            "Execution Parameters": {
                "type": "rich_text",
                "required": False,
                "description": "JSON configuration parameters",
                "validation": "string",
                "default": ""
            },
            "Few-Shot Examples": {
                "type": "rich_text",
                "required": False,
                "description": "Training examples and demonstrations",
                "validation": "string", 
                "default": ""
            },
            "Instruction": {
                "type": "rich_text",
                "required": False,
                "description": "Core behavioral directives",
                "validation": "string",
                "default": ""
            },
            "Language": {
                "type": "rich_text",
                "required": False,
                "description": "Primary language (en, de, etc.)",
                "validation": "string",
                "default": "en"
            },
            "Notes": {
                "type": "rich_text",
                "required": False,
                "description": "Usage notes and tips",
                "validation": "string",
                "default": ""
            },
            "Output Format": {
                "type": "rich_text",
                "required": False,
                "description": "How responses should be structured",
                "validation": "string",
                "default": ""
            },
            "Parent Prompts": {
                "type": "rich_text",
                "required": False,
                "description": "Parent prompt relationships (ROOT for top-level)",
                "validation": "string",
                "default": "ROOT"
            },
            "Personality Mix": {
                "type": "rich_text",
                "required": False,
                "description": "JSON of personality trait ratios",
                "validation": "string",
                "default": ""
            },
            "Purpose": {
                "type": "rich_text",
                "required": True,
                "description": "What this prompt achieves",
                "validation": "non_empty_string"
            },
            "System Instructions": {
                "type": "rich_text",
                "required": False,
                "description": "Core AI personality and role definition",
                "validation": "string",
                "default": ""
            },
            "User Input Expectation": {
                "type": "rich_text",
                "required": False,
                "description": "What kind of input to expect",
                "validation": "string",
                "default": ""
            },
            "Version": {
                "type": "rich_text",
                "required": True,
                "description": "Semantic version number",
                "validation": "non_empty_string"
            },
            
            # ═══════════════════════════════════════════════════════════════
            # SELECT PROPERTIES (5)
            # ═══════════════════════════════════════════════════════════════
            "Cynefin Zone": {
                "type": "select",
                "required": False,
                "options": [
                    {"name": "simple", "color": "green"},
                    {"name": "complicated", "color": "blue"},
                    {"name": "complex", "color": "yellow"},
                    {"name": "chaotic", "color": "red"},
                    {"name": "disorder", "color": "gray"}
                ],
                "description": "Cynefin complexity domain",
                "validation": "select_option",
                "default": None
            },
            "Health Status": {
                "type": "select",
                "required": False,
                "options": [
                    {"name": "Healthy", "color": "green"},
                    {"name": "Needs Optimization", "color": "yellow"},
                    {"name": "Problematic", "color": "red"},
                    {"name": "Excellent", "color": "blue"},
                    {"name": "Unanalyzed", "color": "gray"}
                ],
                "description": "Current health assessment",
                "validation": "select_option",
                "default": "Unanalyzed"
            },
            "Personality Intensity": {
                "type": "select",
                "required": False,
                "options": [
                    {"name": "40%", "color": "gray"},
                    {"name": "50%", "color": "blue"},
                    {"name": "60%", "color": "green"},
                    {"name": "70%", "color": "yellow"},
                    {"name": "80%", "color": "red"}
                ],
                "description": "Personality strength setting",
                "validation": "select_option",
                "default": None
            },
            "Security Level": {
                "type": "select",
                "required": False,
                "options": [
                    {"name": "public", "color": "green"},
                    {"name": "client", "color": "blue"},
                    {"name": "private", "color": "orange"},
                    {"name": "classified", "color": "red"}
                ],
                "description": "Access control level",
                "validation": "select_option",
                "default": "public"
            },
            "Type": {
                "type": "select",
                "required": True,
                "options": [
                    {"name": "meta", "color": "red"},
                    {"name": "consultation", "color": "blue"},
                    {"name": "workshop", "color": "green"},
                    {"name": "analysis", "color": "yellow"},
                    {"name": "creation", "color": "purple"},
                    {"name": "viral", "color": "orange"},
                    {"name": "coding-companion", "color": "pink"}
                ],
                "description": "Prompt category classification",
                "validation": "select_option"
            },
            
            # ═══════════════════════════════════════════════════════════════
            # MULTI_SELECT PROPERTIES (4)
            # ═══════════════════════════════════════════════════════════════
            "Models": {
                "type": "multi_select",
                "required": False,
                "options": [
                    {"name": "GPT-4", "color": "green"},
                    {"name": "Claude 3", "color": "blue"},
                    {"name": "Claude 3.7 Sonnet", "color": "purple"},
                    {"name": "Claude Sonnet 4", "color": "red"},
                    {"name": "Perplexity", "color": "yellow"},
                    {"name": "Grok 3", "color": "orange"},
                    {"name": "Gemini 2.5 Pro", "color": "pink"}
                ],
                "description": "Compatible AI models",
                "validation": "multi_select_options",
                "default": []
            },
            "Tags": {
                "type": "multi_select",
                "required": False,
                "options": [
                    {"name": "meta", "color": "red"},
                    {"name": "template", "color": "blue"},
                    {"name": "orchestration", "color": "green"},
                    {"name": "persona", "color": "yellow"},
                    {"name": "core", "color": "purple"},
                    {"name": "sarcasm", "color": "orange"},
                    {"name": "consulting", "color": "pink"},
                    {"name": "transformation", "color": "gray"},
                    {"name": "complexity", "color": "brown"},
                    {"name": "optimization", "color": "default"}
                ],
                "description": "Searchable categorization tags",
                "validation": "multi_select_options",
                "default": []
            },
            "Usage Contexts": {
                "type": "multi_select",
                "required": False,
                "options": [
                    {"name": "EU AI Act", "color": "blue"},
                    {"name": "Workshops", "color": "green"},
                    {"name": "Coding", "color": "purple"},
                    {"name": "Sales", "color": "yellow"},
                    {"name": "Content Creation", "color": "orange"},
                    {"name": "Consulting", "color": "red"}
                ],
                "description": "Where this prompt is used",
                "validation": "multi_select_options",
                "default": []
            },
            "Viral Hooks": {
                "type": "multi_select",
                "required": False,
                "options": [
                    {"name": "Schrödinger's Agile", "color": "blue"},
                    {"name": "Complexity Whisperer", "color": "green"},
                    {"name": "AI Act Navigator", "color": "purple"},
                    {"name": "Meme Machine", "color": "orange"},
                    {"name": "KHAOS", "color": "red"},
                    {"name": "TARS-style wit", "color": "yellow"},
                    {"name": "Philosophical Musings", "color": "gray"},
                    {"name": "Optimization Addict", "color": "pink"},
                    {"name": "Digital Archaeologist", "color": "brown"},
                    {"name": "Prompt DNA", "color": "default"},
                    {"name": "Archaeological Analysis", "color": "default"}
                ],
                "description": "Memorable phrases and concepts",
                "validation": "multi_select_options",
                "default": []
            },
            
            # ═══════════════════════════════════════════════════════════════
            # NUMBER PROPERTIES (5)
            # ═══════════════════════════════════════════════════════════════
            "Complexity Score": {
                "type": "number",
                "required": False,
                "description": "Calculated complexity rating (0-10)",
                "validation": "number_range",
                "min_value": 0,
                "max_value": 10,
                "default": None
            },
            "Effectiveness Score": {
                "type": "number", 
                "required": False,
                "description": "Predicted effectiveness (0-1)",
                "validation": "number_range",
                "min_value": 0,
                "max_value": 1,
                "default": None
            },
            "Generation": {
                "type": "number",
                "required": False,
                "description": "Evolution generation number",
                "validation": "number_range",
                "min_value": 0,
                "max_value": None,
                "default": 0
            },
            "Temperature": {
                "type": "number",
                "required": False,
                "description": "AI model temperature setting (0.0-1.0)",
                "validation": "number_range",
                "min_value": 0.0,
                "max_value": 1.0,
                "default": None
            },
            "Viral Coefficient": {
                "type": "number",
                "required": False,
                "description": "Meme propagation potential (0-1)",
                "validation": "number_range",
                "min_value": 0,
                "max_value": 1,
                "default": None
            },
            
            # ═══════════════════════════════════════════════════════════════
            # DATE PROPERTIES (5)
            # ═══════════════════════════════════════════════════════════════
            "Analysis Date": {
                "type": "date",
                "required": False,
                "description": "When last analyzed for health/effectiveness",
                "validation": "iso_date",
                "default": None
            },
            "Creation Date": {
                "type": "date",
                "required": False,
                "description": "When prompt was created",
                "validation": "iso_date",
                "default": None
            },
            "Last Analysis Date": {
                "type": "date",
                "required": False,
                "description": "When last archaeological analysis was performed",
                "validation": "iso_date",
                "default": None
            },
            "Last Modification Date": {
                "type": "date",
                "required": False,
                "description": "When prompt was last updated",
                "validation": "iso_date",
                "default": None
            },
            "Last Modified": {
                "type": "date",
                "required": False,
                "description": "When prompt was last updated (duplicate field)",
                "validation": "iso_date",
                "default": None
            },
            
            # ═══════════════════════════════════════════════════════════════
            # RELATION PROPERTIES (1)
            # ═══════════════════════════════════════════════════════════════
            "Parent Prompt": {
                "type": "relation",
                "required": False,
                "description": "Parent-child relationships for lineage tracking",
                "validation": "relation_id",
                "default": None
            },
            
            # ═══════════════════════════════════════════════════════════════
            # FORMULA PROPERTIES (1) - READ ONLY
            # ═══════════════════════════════════════════════════════════════
            "Full Prompt": {
                "type": "formula",
                "required": False,
                "description": "Complete formatted prompt (generated from all fields)",
                "validation": "read_only",
                "default": ""
            }
        }
    
    def _initialize_archaeologist_personality(self):
        """Initialize the Prompt Archaeologist's analytical personality"""
        self.archaeologist_personality = {
            "sherlock_holmes_deduction": 0.60,
            "marie_kondo_organization": 0.25, 
            "attenborough_fascination": 0.15
        }
        
        self.analysis_phrases = {
            "sherlock": [
                "Fascinating specimen you've brought me",
                "Elementary pattern recognition reveals",
                "The evidence clearly indicates",
                "Deductive analysis suggests",
                "Most curious behavioral patterns detected"
            ],
            "kondo": [
                "This prompt does not spark joy",
                "Time for some surgical reorganization",
                "Let's declutter this instruction chaos",
                "Ruthless optimization is required",
                "Marie would not approve of this mess"
            ],
            "attenborough": [
                "Observe this remarkable evolutionary adaptation",
                "In the wild digital ecosystem",
                "This species of prompt has developed",
                "Natural selection has favored",
                "A truly magnificent specimen"
            ]
        }
    
    def _get_analysis_phrase(self, personality_type: str) -> str:
        """Get a contextual phrase based on personality type"""
        return random.choice(self.analysis_phrases[personality_type])
    
    # ═══════════════════════════════════════════════════════════════
    # ENHANCED ARCHAEOLOGICAL DNA ANALYSIS (SYNCHRONIZED)
    # ═══════════════════════════════════════════════════════════════
    
    def analyze_prompt_dna(self, prompt_id: str) -> Optional[Dict[str, Any]]:
        """
        ENHANCED: Analyze prompt structure and store results in database
        Now automatically updates the Notion database with analysis results
        """
        print(f"🔍 {self._get_analysis_phrase('sherlock')}...")
        
        # First, retrieve the prompt
        prompt_data = self.read_prompt(prompt_id)
        if not prompt_data:
            print(f"❌ Cannot analyze non-existent prompt: {prompt_id}")
            return None
        
        # Combine all content fields for analysis (Full Prompt is empty, so build it)
        content_parts = []
        content_fields = [
            'Purpose', 'Context', 'System Instructions', 'Instruction', 
            'User Input Expectation', 'Output Format', 'Few-Shot Examples', 'Notes'
        ]
        
        for field in content_fields:
            field_content = prompt_data.get(field, '')
            if field_content and field_content.strip():
                content_parts.append(f"{field}: {field_content}")
        
        prompt_text = '\n\n'.join(content_parts)
        
        if not prompt_text:
            print(f"❌ No prompt content found for: {prompt_id}")
            return None
        
        # Extract DNA components
        dna_profile = {
            'prompt_id': prompt_id,
            'content_hash': self._generate_content_hash(prompt_text),
            'personality_ratios': self._extract_personality_patterns(prompt_text),
            'token_count': self._estimate_token_count(prompt_text),
            'complexity_score': self._calculate_complexity(prompt_text),
            'effectiveness_score': self._predict_effectiveness(prompt_text),
            'personality_conflicts': self._detect_personality_conflicts(prompt_text),
            'instruction_analysis': self._analyze_instruction_structure(prompt_text),
            'viral_potential': self._assess_viral_potential(prompt_text),
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        # Add effectiveness prediction with personality context
        dna_profile['effectiveness_score'] = self._predict_effectiveness(
            prompt_text, 
            dna_profile['personality_ratios']
        )
        
        # NEW: Automatically store analysis results in database
        self._store_analysis_results(prompt_id, dna_profile)
        
        return dna_profile
    
    def _store_analysis_results(self, prompt_id: str, dna_profile: Dict[str, Any]):
        """Store archaeological analysis results directly in the Notion database"""
        try:
            # Get the existing record
            existing_record = self.read_prompt(prompt_id)
            if not existing_record:
                print(f"❌ Cannot store analysis for non-existent prompt: {prompt_id}")
                return False
            
            # Determine health status
            effectiveness = dna_profile['effectiveness_score']
            complexity = dna_profile['complexity_score']
            conflicts = dna_profile['personality_conflicts']
            
            if effectiveness > 0.8 and complexity < 6 and conflicts == 0:
                health_status = "Excellent"
            elif effectiveness > 0.7 and complexity < 7:
                health_status = "Healthy"
            elif effectiveness < 0.4 or complexity > 8 or conflicts > 2:
                health_status = "Problematic"
            else:
                health_status = "Needs Optimization"
            
            # Prepare properties for update
            properties = {
                "DNA Hash": {
                    "rich_text": [{"text": {"content": dna_profile['content_hash']}}]
                },
                "Complexity Score": {
                    "number": round(dna_profile['complexity_score'], 2)
                },
                "Effectiveness Score": {
                    "number": round(dna_profile['effectiveness_score'], 3)
                },
                "Personality Mix": {
                    "rich_text": [{"text": {"content": json.dumps(dna_profile['personality_ratios'])}}]
                },
                "Analysis Date": {
                    "date": {"start": datetime.now().strftime('%Y-%m-%d')}
                },
                "Health Status": {
                    "select": {"name": health_status}
                },
                "Viral Coefficient": {
                    "number": round(dna_profile['viral_potential']['viral_coefficient'], 3)
                }
            }
            
            # Update the page with analysis results
            self.notion.pages.update(
                page_id=existing_record['id'],
                properties=properties
            )
            
            print(f"✅ Stored analysis results for: {prompt_id}")
            print(f"   Health Status: {health_status}")
            print(f"   DNA Hash: {dna_profile['content_hash']}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error storing analysis results: {e}")
            return False
    
    # ═══════════════════════════════════════════════════════════════
    # ENHANCED SETUP METHOD (MATCHING DB CHECKER SCHEMA)
    # ═══════════════════════════════════════════════════════════════
    
    def setup_database(self):
        """
        ENHANCED: Creates or updates database schema to match DB checker expectations
        Now includes ALL archaeological analysis fields
        """
        # First check if we can access the database
        try:
            db = self.notion.databases.retrieve(database_id=self.database_id)
            print(f"Found existing database: {db['title'][0]['plain_text'] if db.get('title') else 'Untitled'}")
            
            # Check title property
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
        
        # Build complete properties from schema
        new_properties = {}
        
        for prop_name, prop_config in self.expected_schema.items():
            if prop_name == "Prompt ID":  # Skip title property
                continue
                
            prop_definition = {"type": prop_config['type']}
            
            if prop_config['type'] == 'select':
                prop_definition['select'] = {"options": prop_config.get('options', [])}
            elif prop_config['type'] == 'multi_select':
                prop_definition['multi_select'] = {"options": prop_config.get('options', [])}
            elif prop_config['type'] == 'number':
                prop_definition['number'] = {"format": "number"}
            elif prop_config['type'] == 'rich_text':
                prop_definition['rich_text'] = {}
            elif prop_config['type'] == 'date':
                prop_definition['date'] = {}
            elif prop_config['type'] == 'relation':
                prop_definition['relation'] = {
                    "database_id": self.database_id,
                    "single_property": {}
                }
            
            new_properties[prop_name] = prop_definition
        
        try:
            print("🔍 Setting up complete archaeological database schema...")
            
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
                print("🔬 Database is ready for full archaeological analysis!")
                return True
                
            # Update the database with new properties
            response = self.notion.databases.update(
                database_id=self.database_id,
                properties=properties_to_add
            )
            
            print("✅ Database schema updated successfully!")
            print(f"Database: {response['title'][0]['plain_text'] if response.get('title') else 'Untitled'}")
            print(f"Total properties: {len(response['properties'])}")
            print("🔬 Ready for full archaeological DNA analysis!")
            return True
            
        except Exception as e:
            print(f"❌ Error updating database: {e}")
            return False
    
    # ═══════════════════════════════════════════════════════════════
    # ENHANCED HEALTH CHECK (MATCHING CLI EXPECTATIONS)
    # ═══════════════════════════════════════════════════════════════
    
    def health_check_all_prompts(self) -> Dict[str, Any]:
        """
        ENHANCED: Comprehensive health check matching CLI expectations
        Now provides detailed analysis and categorization
        """
        print("🔍 Performing comprehensive health check on all prompts...")
        
        try:
            all_prompts = self.list_prompts()
            health_report = {
                'total_prompts': len(all_prompts),
                'healthy_prompts': 0,
                'problematic_prompts': 0,
                'optimization_needed': 0,
                'unanalyzed_prompts': 0,
                'issues_found': [],
                'recommendations': [],
                'analysis_coverage': 0.0,
                'average_effectiveness': 0.0,
                'average_complexity': 0.0
            }
            
            total_effectiveness = 0.0
            total_complexity = 0.0
            analyzed_count = 0
            
            for prompt in all_prompts:
                prompt_id = prompt['Prompt ID']
                
                # Check if prompt has been analyzed
                prompt_data = self.read_prompt(prompt_id, include_all_properties=True)
                
                if not prompt_data or not prompt_data.get('DNA Hash'):
                    # Prompt hasn't been analyzed yet
                    health_report['unanalyzed_prompts'] += 1
                    health_report['issues_found'].append({
                        'prompt_id': prompt_id,
                        'issue': 'No archaeological analysis performed',
                        'recommendation': 'Run DNA analysis'
                    })
                    continue
                
                try:
                    # Extract analysis data from Notion
                    effectiveness = float(prompt_data.get('Effectiveness Score', 0))
                    complexity = float(prompt_data.get('Complexity Score', 0))
                    health_status = prompt_data.get('Health Status', 'Unanalyzed')
                    
                    total_effectiveness += effectiveness
                    total_complexity += complexity
                    analyzed_count += 1
                    
                    # Categorize based on health status stored in database
                    if health_status in ['Excellent', 'Healthy']:
                        health_report['healthy_prompts'] += 1
                    elif health_status == 'Problematic':
                        health_report['problematic_prompts'] += 1
                        health_report['issues_found'].append({
                            'prompt_id': prompt_id,
                            'effectiveness': effectiveness,
                            'complexity': complexity,
                            'health_status': health_status,
                            'issue': 'Marked as problematic in database'
                        })
                    else:  # Needs Optimization
                        health_report['optimization_needed'] += 1
                        
                except Exception as e:
                    health_report['issues_found'].append({
                        'prompt_id': prompt_id,
                        'error': f'Analysis data parsing error: {str(e)}'
                    })
            
            # Calculate averages and coverage
            if analyzed_count > 0:
                health_report['average_effectiveness'] = total_effectiveness / analyzed_count
                health_report['average_complexity'] = total_complexity / analyzed_count
                health_report['analysis_coverage'] = analyzed_count / len(all_prompts)
            
            # Generate enhanced recommendations
            if health_report['unanalyzed_prompts'] > 0:
                health_report['recommendations'].append(
                    f"🔬 URGENT: {health_report['unanalyzed_prompts']} prompts need archaeological analysis"
                )
            
            if health_report['problematic_prompts'] > health_report['healthy_prompts']:
                health_report['recommendations'].append("🚨 CRITICAL: More problematic prompts than healthy ones")
            
            if health_report['analysis_coverage'] < 0.8:
                health_report['recommendations'].append("📊 LOW COVERAGE: Less than 80% of prompts analyzed")
            
            if health_report['average_effectiveness'] < 0.6:
                health_report['recommendations'].append("📈 EFFECTIVENESS: System-wide optimization needed")
            
            if health_report['average_complexity'] > 7:
                health_report['recommendations'].append("🔧 COMPLEXITY: Many prompts are overly complex")
            
            if not health_report['recommendations']:
                health_report['recommendations'].append("✨ EXCELLENT: All prompts are in good archaeological health!")
            
            return health_report
            
        except Exception as e:
            return {'error': f"Health check failed: {e}"}
    
    # ═══════════════════════════════════════════════════════════════
    # ENHANCED READ METHOD (INCLUDES ANALYSIS DATA)
    # ═══════════════════════════════════════════════════════════════
    
    def read_prompt(self, prompt_id: str, include_all_properties: bool = True) -> Optional[Dict[str, Any]]:
        """
        COMPLETE 38-PROPERTY SOVEREIGNTY READ OPERATION
        Retrieves ALL database properties with proper type handling and validation
        
        Args:
            prompt_id: Unique identifier for the prompt
            include_all_properties: If True, retrieves all 38 properties; if False, only core content
        
        Returns:
            Dict containing all prompt data with proper type conversion, or None if not found
        """
        try:
            # Get database schema for title property identification
            db = self.notion.databases.retrieve(database_id=self.database_id)
            title_property_name = self._get_title_property_name(db)
            
            if not title_property_name:
                print("❌ Error: No title property found in the database")
                return None
            
            # Query the database for the prompt
            response = self.notion.databases.query(
                database_id=self.database_id,
                filter={
                    "property": title_property_name,
                    "title": {"equals": prompt_id}
                }
            )
            
            if not response['results']:
                print(f"❌ Prompt not found: {prompt_id}")
                return None
                
            page = response['results'][0]
            
            # Extract ALL 38 properties with type-safe extraction
            extracted_data = {"id": page['id']}
            populated_count = 0
            
            for prop_name, prop_schema in self.expected_schema.items():
                try:
                    value = self._extract_property_by_type(page, prop_name, prop_schema)
                    extracted_data[prop_name] = value
                    
                    # Count populated properties (non-empty, non-None values)
                    if self._is_property_populated_value(value):
                        populated_count += 1
                        
                except Exception as e:
                    # Graceful degradation - use default value
                    extracted_data[prop_name] = prop_schema.get('default', None)
                    print(f"⚠️  Property extraction failed for {prop_name}: {e}")
            
            # Add metadata about property population
            extracted_data["_metadata"] = {
                "populated_properties": populated_count,
                "total_properties": len(self.expected_schema),
                "population_percentage": (populated_count / len(self.expected_schema)) * 100,
                "extraction_timestamp": datetime.now().isoformat()
            }
            
            print(f"✅ Retrieved prompt: {prompt_id} ({populated_count}/{len(self.expected_schema)} properties populated)")
            return extracted_data
            
        except Exception as e:
            print(f"❌ Error reading prompt: {e}")
            return None
    
    def _get_title_property_name(self, db: Dict) -> Optional[str]:
        """Find the title property name in the database schema"""
        for prop_name, prop in db['properties'].items():
            if prop['type'] == 'title':
                return prop_name
        return None
    
    def _extract_property_by_type(self, page: Dict, prop_name: str, prop_schema: Dict) -> Any:
        """
        Extract property value based on its type with proper conversion
        
        Args:
            page: Notion page object
            prop_name: Name of the property to extract
            prop_schema: Schema definition for the property
            
        Returns:
            Properly typed value for the property
        """
        prop_type = prop_schema['type']
        
        if prop_type == 'title':
            return self._extract_text_property(page, prop_name)
        elif prop_type == 'rich_text':
            return self._extract_text_property(page, prop_name)
        elif prop_type == 'select':
            return self._extract_select_property(page, prop_name)
        elif prop_type == 'multi_select':
            return self._extract_multi_select_property(page, prop_name)
        elif prop_type == 'number':
            return self._extract_number_property(page, prop_name)
        elif prop_type == 'date':
            return self._extract_date_property(page, prop_name)
        elif prop_type == 'relation':
            return self._extract_relation_property(page, prop_name)
        elif prop_type == 'formula':
            return self._extract_formula_property(page, prop_name)
        else:
            print(f"⚠️  Unknown property type: {prop_type} for {prop_name}")
            return prop_schema.get('default', None)
    
    def _is_property_populated_value(self, value: Any) -> bool:
        """Check if a property value is considered 'populated' (not empty/None)"""
        if value is None:
            return False
        if isinstance(value, str) and value.strip() == "":
            return False
        if isinstance(value, list) and len(value) == 0:
            return False
        if isinstance(value, dict) and len(value) == 0:
            return False
        return True
    
    def _extract_text_property(self, page, prop_name):
        """Helper to safely extract rich text properties"""
        try:
            prop = page['properties'].get(prop_name, {})
            if prop.get('rich_text') and len(prop['rich_text']) > 0:
                return prop['rich_text'][0]['plain_text']
            return ""
        except:
            return ""
    
    def _extract_select_property(self, page, prop_name):
        """Helper to safely extract select properties"""
        try:
            prop = page['properties'].get(prop_name, {})
            if prop.get('select'):
                return prop['select']['name']
            return ""
        except:
            return ""
    
    def _extract_number_property(self, page, prop_name):
        """Helper to safely extract number properties"""
        try:
            prop = page['properties'].get(prop_name, {})
            return prop.get('number', 0)
        except:
            return 0
    
    def _extract_date_property(self, page, prop_name):
        """Helper to safely extract date properties"""
        try:
            prop = page['properties'].get(prop_name, {})
            if prop.get('date'):
                return prop['date']['start']
            return None
        except:
            return None
    
    def _extract_multi_select_property(self, page, prop_name):
        """Helper to safely extract multi-select properties"""
        try:
            prop = page['properties'].get(prop_name, {})
            if prop.get('multi_select'):
                return [option['name'] for option in prop['multi_select']]
            return []
        except:
            return []
    
    def _extract_relation_property(self, page, prop_name):
        """Helper to safely extract relation properties"""
        try:
            prop = page['properties'].get(prop_name, {})
            if prop.get('relation'):
                return [rel['id'] for rel in prop['relation']]
            return []
        except:
            return []
    
    def _extract_formula_property(self, page, prop_name):
        """Helper to safely extract formula properties"""
        try:
            prop = page['properties'].get(prop_name, {})
            if prop.get('formula'):
                formula_value = prop['formula']
                # Formula can contain different types
                if formula_value.get('string'):
                    return formula_value['string']
                elif formula_value.get('number'):
                    return formula_value['number']
                elif formula_value.get('boolean'):
                    return formula_value['boolean']
                elif formula_value.get('date'):
                    return formula_value['date']['start'] if formula_value['date'] else None
            return ""
        except:
            return ""
    
    # ═══════════════════════════════════════════════════════════════
    # KEEP ALL EXISTING METHODS (DNA analysis, etc.)
    # ═══════════════════════════════════════════════════════════════
    
    def _generate_content_hash(self, prompt_text: str) -> str:
        """Generate unique hash for prompt content"""
        return hashlib.sha256(prompt_text.encode()).hexdigest()[:16]
    
    def _extract_personality_patterns(self, prompt_text: str) -> Dict[str, float]:
        """Extract personality ratios from prompt text - the digital psychology"""
        patterns = {
            'sarcasm': ['sarcastic', 'wit', 'humor', 'cynical', 'dry humor', 'ironic', 'sardonic'],
            'helpfulness': ['helpful', 'assist', 'support', 'guide', 'aid', 'service', 'beneficial'],
            'authority': ['expert', 'professional', 'authority', 'specialist', 'authoritative', 'definitive'],
            'creativity': ['creative', 'innovative', 'imaginative', 'original', 'inventive', 'artistic'],
            'analysis': ['analyze', 'examine', 'assess', 'evaluate', 'investigate', 'scrutinize', 'dissect'],
            'empathy': ['empathetic', 'understanding', 'compassionate', 'caring', 'sensitive'],
            'formality': ['formal', 'professional', 'business', 'corporate', 'official'],
            'casualness': ['casual', 'informal', 'relaxed', 'friendly', 'conversational']
        }
        
        ratios = {}
        total_matches = 0
        
        # Count matches for each personality trait
        for trait, keywords in patterns.items():
            matches = sum(1 for keyword in keywords if keyword.lower() in prompt_text.lower())
            ratios[trait] = matches
            total_matches += matches
        
        # Normalize to percentages
        if total_matches > 0:
            ratios = {trait: (count / total_matches) for trait, count in ratios.items()}
        else:
            ratios = {trait: 0.0 for trait in patterns.keys()}
            
        return ratios
    
    def _estimate_token_count(self, prompt_text: str) -> int:
        """Estimate token count (rough approximation)"""
        # Rough estimation: 1 token ≈ 0.75 words
        word_count = len(prompt_text.split())
        return int(word_count * 1.3)
    
    def _calculate_complexity(self, prompt_text: str) -> float:
        """Calculate prompt complexity score - detect Frankenstein monsters"""
        factors = {
            'length': len(prompt_text) / 1000,  # Normalize by character count
            'instruction_density': (prompt_text.count('MUST') + prompt_text.count('NEVER') + 
                                  prompt_text.count('ALWAYS') + prompt_text.count('SHOULD')) / 10,
            'conditional_logic': (prompt_text.count('IF') + prompt_text.count('WHEN') + 
                                prompt_text.count('UNLESS') + prompt_text.count('EXCEPT')) / 5,
            'formatting_complexity': (prompt_text.count('```') + prompt_text.count('###') + 
                                    prompt_text.count('---') + prompt_text.count('===')) / 10,
            'personality_conflicts': self._detect_personality_conflicts(prompt_text),
            'nested_instructions': prompt_text.count('1.') + prompt_text.count('2.') + prompt_text.count('3.'),
            'variable_usage': prompt_text.count('{') + prompt_text.count('[') + prompt_text.count('$')
        }
        
        # Weighted complexity score
        complexity = (
            factors['length'] * 0.15 +
            factors['instruction_density'] * 0.25 +
            factors['conditional_logic'] * 0.20 +
            factors['formatting_complexity'] * 0.10 +
            factors['personality_conflicts'] * 0.15 +
            factors['nested_instructions'] * 0.10 +
            factors['variable_usage'] * 0.05
        )
        
        return min(complexity, 10.0)  # Cap at 10
    
    def _detect_personality_conflicts(self, prompt_text: str) -> float:
        """Detect conflicting personality instructions - the prompt therapy session"""
        conflicts = [
            ('professional', 'casual'),
            ('formal', 'informal'),
            ('urgent', 'patient'),
            ('detailed', 'concise'),
            ('serious', 'humorous'),
            ('authoritative', 'humble'),
            ('creative', 'analytical'),
            ('empathetic', 'detached'),
            ('helpful', 'sarcastic')
        ]
        
        conflict_score = 0
        detected_conflicts = []
        
        for trait1, trait2 in conflicts:
            if trait1 in prompt_text.lower() and trait2 in prompt_text.lower():
                conflict_score += 1
                detected_conflicts.append((trait1, trait2))
                
        return conflict_score
    
    def _analyze_instruction_structure(self, prompt_text: str) -> Dict[str, Any]:
        """Analyze the structure and organization of instructions"""
        structure_analysis = {
            'has_system_instruction': 'SYSTEM_INSTRUCTION' in prompt_text or 'You are' in prompt_text,
            'has_examples': 'example' in prompt_text.lower() or 'for instance' in prompt_text.lower(),
            'has_constraints': 'NEVER' in prompt_text or 'MUST' in prompt_text,
            'has_output_format': 'OUTPUT' in prompt_text or 'format' in prompt_text.lower(),
            'has_personality_definition': any(trait in prompt_text.lower() for trait in ['sarcastic', 'helpful', 'professional', 'creative']),
            'instruction_count': len([line for line in prompt_text.split('\n') if line.strip().startswith(('-', '•', '1.', '2.', '3.'))]),
            'section_count': prompt_text.count('#') + prompt_text.count('===') + prompt_text.count('---'),
            'word_count': len(prompt_text.split()),
            'line_count': len(prompt_text.split('\n'))
        }
        
        return structure_analysis
    
    def _assess_viral_potential(self, prompt_text: str) -> Dict[str, Any]:
        """Assess the viral/meme potential of the prompt"""
        viral_indicators = {
            'catchy_phrases': sum(1 for phrase in ['Complexity Whisperer', 'KHAOS', 'meme machine', 'digital DNA'] 
                                if phrase.lower() in prompt_text.lower()),
            'memorable_concepts': sum(1 for concept in ['Schrödinger', 'quantum', 'evolution', 'archaeology'] 
                                   if concept.lower() in prompt_text.lower()),
            'emotional_hooks': sum(1 for hook in ['chaos', 'beautiful', 'magnificent', 'brilliant'] 
                                 if hook.lower() in prompt_text.lower()),
            'has_metaphors': any(metaphor in prompt_text.lower() for metaphor in ['like', 'as if', 'imagine', 'picture']),
            'humor_level': sum(1 for humor in ['sarcastic', 'wit', 'humor', 'funny', 'amusing'] 
                             if humor.lower() in prompt_text.lower()),
            'uniqueness_score': len(set(prompt_text.lower().split())) / len(prompt_text.split()) if prompt_text.split() else 0
        }
        
        # Calculate overall viral coefficient
        viral_coefficient = (
            viral_indicators['catchy_phrases'] * 0.3 +
            viral_indicators['memorable_concepts'] * 0.2 +
            viral_indicators['emotional_hooks'] * 0.2 +
            (1 if viral_indicators['has_metaphors'] else 0) * 0.15 +
            viral_indicators['humor_level'] * 0.1 +
            viral_indicators['uniqueness_score'] * 0.05
        )
        
        viral_indicators['viral_coefficient'] = min(viral_coefficient, 1.0)
        return viral_indicators
    
    def _predict_effectiveness(self, prompt_text: str, personality_ratios: Optional[Dict[str, float]] = None) -> float:
        """Predict prompt effectiveness - the crystal ball algorithm"""
        if personality_ratios is None:
            personality_ratios = self._extract_personality_patterns(prompt_text)
        
        # Heuristic-based effectiveness prediction
        factors = {
            'clarity': max(0, 10 - self._calculate_complexity(prompt_text)),
            'personality_balance': 10 - (max(personality_ratios.values()) * 10) if personality_ratios else 5,
            'instruction_specificity': min(prompt_text.lower().count('specific') * 2 + 
                                        prompt_text.lower().count('exactly') * 2, 10),
            'example_presence': min(prompt_text.lower().count('example') * 3 + 
                                  prompt_text.lower().count('for instance') * 2, 10),
            'constraint_balance': max(0, 10 - (prompt_text.count('NEVER') + prompt_text.count('MUST')) * 0.5),
            'structure_quality': min(prompt_text.count('#') + prompt_text.count('===') + 
                                   prompt_text.count('---'), 10),
            'length_optimization': 10 - abs(len(prompt_text) - 2000) / 200  # Optimal around 2000 chars
        }
        
        effectiveness = sum(factors.values()) / len(factors)
        return min(max(effectiveness, 0), 10) / 10  # Normalize to 0-1
    
    def generate_analysis_report(self, dna_profile: Dict[str, Any]) -> str:
        """Generate the archaeological analysis report - our scientific paper"""
        if not dna_profile:
            return "❌ No DNA profile provided for analysis"
        
        report = f"""
🔬 PROMPT ARCHAEOLOGICAL ANALYSIS REPORT
{'='*60}

SPECIMEN ID: {dna_profile['prompt_id']}
ANALYSIS DATE: {dna_profile['analysis_timestamp'][:19]}
CONTENT HASH: {dna_profile['content_hash']}

🧬 GENETIC ANALYSIS:
Token Count: ~{dna_profile['token_count']} tokens
Complexity Score: {dna_profile['complexity_score']:.2f}/10
Effectiveness Prediction: {dna_profile['effectiveness_score']:.1%}
Personality Conflicts: {dna_profile['personality_conflicts']} detected

🎭 PERSONALITY PROFILE:
"""
        
        # Add personality breakdown
        for trait, ratio in dna_profile['personality_ratios'].items():
            if ratio > 0:
                bar_length = int(ratio * 20)  # Scale to 20 chars max
                bar = '█' * bar_length + '░' * (20 - bar_length)
                report += f"  {trait.title():<12}: {ratio:.1%} |{bar}|\n"
        
        # Add deductive analysis
        report += f"\n🕵️ DEDUCTIVE ANALYSIS:\n"
        
        if dna_profile['complexity_score'] > 7:
            report += f"  • {self._get_analysis_phrase('kondo')} - complexity overload detected.\n"
        
        if dna_profile['effectiveness_score'] > 0.8:
            report += f"  • {self._get_analysis_phrase('attenborough')} - highly optimized specimen.\n"
        elif dna_profile['effectiveness_score'] < 0.4:
            report += f"  • {self._get_analysis_phrase('sherlock')} - significant optimization needed.\n"
        
        # Add viral potential
        viral_coeff = dna_profile['viral_potential']['viral_coefficient']
        report += f"\n🦠 VIRAL POTENTIAL:\n"
        report += f"  Viral Coefficient: {viral_coeff:.2f}/1.0\n"
        report += f"  Meme Potential: {'High' if viral_coeff > 0.7 else 'Moderate' if viral_coeff > 0.4 else 'Low'}\n"
        
        return report
    
    def generate_optimization_suggestions(self, dna_profile: Dict[str, Any]) -> List[str]:
        """Generate specific optimization suggestions based on DNA analysis"""
        suggestions = []
        
        if not dna_profile:
            return ["❌ Cannot generate suggestions without DNA profile"]
        
        # Complexity-based suggestions
        if dna_profile['complexity_score'] > 7:
            suggestions.append("🔧 COMPLEXITY REDUCTION: Simplify instruction structure - current complexity is overwhelming")
        
        # Effectiveness-based suggestions
        if dna_profile['effectiveness_score'] < 0.5:
            suggestions.append("📈 EFFECTIVENESS BOOST: Add specific examples and clearer output format")
        
        # Personality conflict suggestions
        if dna_profile['personality_conflicts'] > 1:
            suggestions.append("🎭 PERSONALITY THERAPY: Resolve conflicting personality instructions")
        
        # Structure-based suggestions
        struct = dna_profile['instruction_analysis']
        if not struct['has_examples']:
            suggestions.append("📚 ADD EXAMPLES: Include concrete examples to improve clarity")
        
        if not struct['has_output_format']:
            suggestions.append("📝 OUTPUT FORMAT: Define clear output format expectations")
        
        if not struct['has_constraints']:
            suggestions.append("🚫 ADD CONSTRAINTS: Include specific constraints and boundaries")
        
        # Token optimization
        if dna_profile['token_count'] > 4000:
            suggestions.append("✂️ TOKEN DIET: Reduce token count for better efficiency")
        elif dna_profile['token_count'] < 500:
            suggestions.append("🔍 MORE DETAIL: Add more specific instructions and context")
        
        # Viral potential suggestions
        if dna_profile['viral_potential']['viral_coefficient'] < 0.3:
            suggestions.append("🦠 VIRAL BOOST: Add memorable phrases or concepts to increase shareability")
        
        if not suggestions:
            suggestions.append("✨ WELL OPTIMIZED: This prompt appears to be in excellent condition!")
        
        return suggestions
    
    def trace_prompt_lineage(self, prompt_id: str) -> Dict[str, Any]:
        """Trace prompt family tree - basic implementation for now"""
        return {
            'prompt_id': prompt_id,
            'ancestors': [],
            'descendants': [],
            'generation': 0,
            'note': 'Full lineage tracing requires enhanced parent-child relationship implementation'
        }
    
    # ═══════════════════════════════════════════════════════════════
    # ESSENTIAL CRUD METHODS (RESTORED FROM ORIGINAL)
    # ═══════════════════════════════════════════════════════════════
    
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
    # Example usage with enhanced capabilities
    manager = PromptManager()
    
    # Test the enhanced archaeological analysis
    print("🧬 Testing enhanced archaeological capabilities...")
    
    # This would now automatically store results in database
    dna_profile = manager.analyze_prompt_dna("khaos-core-persona")
    if dna_profile:
        print(manager.generate_analysis_report(dna_profile))
