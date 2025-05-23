#!/usr/bin/env python3
"""
KHAOS Prompt Database Diagnostic & Repair Tool
Comprehensive health check and schema validation for the archaeological database.
Because sometimes you need to know EXACTLY what's broken before you can fix it.
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

class PromptDatabaseDiagnostic:
    """
    The database doctor - diagnoses and repairs schema issues
    """
    
    def __init__(self):
        self.notion = Client(auth=os.getenv("PROMPT_SECURITY_TOKEN"))
        self.database_id = os.getenv("PROMPT_DATABASE_ID")
        self.expected_schema = self._define_expected_schema()
        self.diagnosis_report = {
            'timestamp': datetime.now().isoformat(),
            'connection_status': 'unknown',
            'database_exists': False,
            'database_title': '',
            'entry_count': 0,
            'schema_issues': [],
            'missing_properties': [],
            'incorrect_types': [],
            'schema_complete': False,
            'recommendations': []
        }
    
    def _define_expected_schema(self) -> Dict[str, Dict]:
        """Define the complete expected schema for archaeological analysis"""
        return {
            # Core identification fields
            "Prompt ID": {
                "type": "title",
                "required": True,
                "description": "Primary identifier - auto-title field"
            },
            "Version": {
                "type": "rich_text",
                "required": True,
                "description": "Version number (semantic versioning)"
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
                "description": "Prompt category classification"
            },
            "Purpose": {
                "type": "rich_text",
                "required": True,
                "description": "What this prompt achieves"
            },
            
            # Content and structure
            "Full Prompt": {
                "type": "rich_text",
                "required": True,
                "description": "Complete prompt content"
            },
            "Core Message": {
                "type": "rich_text",
                "required": False,
                "description": "Central theme or message"
            },
            
            # Archaeological analysis fields
            "DNA Hash": {
                "type": "rich_text",
                "required": False,
                "description": "Content fingerprint for uniqueness tracking"
            },
            "Complexity Score": {
                "type": "number",
                "required": False,
                "description": "Calculated complexity rating (0-10)"
            },
            "Effectiveness Score": {
                "type": "number",
                "required": False,
                "description": "Predicted effectiveness (0-1)"
            },
            "Personality Mix": {
                "type": "rich_text",
                "required": False,
                "description": "JSON of personality trait ratios"
            },
            "Analysis Date": {
                "type": "date",
                "required": False,
                "description": "When last analyzed"
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
                "description": "Current health assessment"
            },
            "Viral Coefficient": {
                "type": "number",
                "required": False,
                "description": "Meme propagation potential (0-1)"
            },
            
            # Multi-select categorization
            "Viral Hooks": {
                "type": "multi_select",
                "required": False,
                "options": [
                    {"name": "Complexity Whisperer", "color": "green"},
                    {"name": "KHAOS", "color": "red"},
                    {"name": "Meme Machine", "color": "orange"},
                    {"name": "Schrödinger's Agile", "color": "blue"},
                    {"name": "AI Act Navigator", "color": "purple"}
                ],
                "description": "Memorable phrases and concepts"
            },
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
                "description": "Compatible AI models"
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
                "description": "Where this prompt is used"
            },
            "Tags": {
                "type": "multi_select",
                "required": False,
                "options": [
                    {"name": "persona", "color": "red"},
                    {"name": "core", "color": "blue"},
                    {"name": "sarcasm", "color": "orange"},
                    {"name": "consulting", "color": "green"},
                    {"name": "transformation", "color": "purple"},
                    {"name": "complexity", "color": "yellow"},
                    {"name": "optimization", "color": "pink"}
                ],
                "description": "Searchable tags"
            },
            
            # Metadata and tracking
            "Creation Date": {
                "type": "date",
                "required": False,
                "description": "When prompt was created"
            },
            "Last Modified": {
                "type": "date",
                "required": False,
                "description": "When prompt was last updated"
            },
            "Parent Prompt": {
                "type": "relation",
                "required": False,
                "description": "Parent-child relationships for lineage"
            },
            "Generation": {
                "type": "number",
                "required": False,
                "description": "Evolution generation number"
            },
            
            # Configuration fields
            "Temperature": {
                "type": "number",
                "required": False,
                "description": "AI model temperature setting"
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
                "description": "Personality strength setting"
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
                "description": "Access control level"
            }
        }
    
    def run_comprehensive_diagnostic(self):
        """Run complete database diagnostic and repair sequence"""
        print("🔬" + "=" * 70)
        print("🔬 KHAOS PROMPT DATABASE DIAGNOSTIC & REPAIR TOOL")
        print("🔬" + "=" * 70)
        print(f"🕐 Diagnostic started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Step 1: Basic connectivity
        print("🔌 STEP 1: Testing database connectivity...")
        self._test_connection()
        
        # Step 2: Database existence and basic info
        print("\n📊 STEP 2: Checking database existence and basic info...")
        self._check_database_existence()
        
        # Step 3: Schema validation
        print("\n🧬 STEP 3: Validating schema against expected structure...")
        self._validate_schema()
        
        # Step 4: Content analysis
        print("\n📝 STEP 4: Analyzing database content...")
        self._analyze_content()
        
        # Step 5: Generate recommendations
        print("\n🎯 STEP 5: Generating repair recommendations...")
        self._generate_recommendations()
        
        # Step 6: Optional schema repair
        print("\n🔧 STEP 6: Schema repair options...")
        self._offer_schema_repair()
        
        # Step 7: Final diagnostic report
        print("\n📋 STEP 7: Final diagnostic report...")
        self._generate_final_report()
    
    def _test_connection(self):
        """Test basic Notion API connectivity"""
        try:
            print("   🔍 Testing Notion API connection...")
            
            if not os.getenv("PROMPT_SECURITY_TOKEN"):
                print("   ❌ PROMPT_SECURITY_TOKEN not found in environment")
                self.diagnosis_report['connection_status'] = 'missing_token'
                return False
            
            if not self.database_id:
                print("   ❌ PROMPT_DATABASE_ID not found in environment")
                self.diagnosis_report['connection_status'] = 'missing_database_id'
                return False
            
            # Test API connection with a simple call
            print("   🔍 Attempting to connect to Notion API...")
            test_response = self.notion.users.me()
            print(f"   ✅ Connected to Notion API successfully")
            print(f"   👤 Authenticated as: {test_response.get('name', 'Unknown User')}")
            
            self.diagnosis_report['connection_status'] = 'connected'
            return True
            
        except Exception as e:
            print(f"   ❌ Connection failed: {str(e)}")
            self.diagnosis_report['connection_status'] = f'failed: {str(e)}'
            return False
    
    def _check_database_existence(self):
        """Check if the specified database exists and get basic info"""
        try:
            print(f"   🔍 Checking database: {self.database_id}")
            
            database = self.notion.databases.retrieve(database_id=self.database_id)
            
            # Extract database info
            title = "Untitled Database"
            if database.get('title') and len(database['title']) > 0:
                title = database['title'][0].get('plain_text', 'Untitled Database')
            
            self.diagnosis_report['database_exists'] = True
            self.diagnosis_report['database_title'] = title
            
            print(f"   ✅ Database found: '{title}'")
            print(f"   📅 Created: {database.get('created_time', 'Unknown')}")
            print(f"   🔄 Last edited: {database.get('last_edited_time', 'Unknown')}")
            
            # Count entries
            print("   🔢 Counting database entries...")
            entries_response = self.notion.databases.query(
                database_id=self.database_id,
                page_size=100
            )
            
            entry_count = len(entries_response['results'])
            # Note: This is a simplified count - for large databases, we'd need pagination
            
            self.diagnosis_report['entry_count'] = entry_count
            print(f"   📊 Total entries: {entry_count}")
            
            return database
            
        except Exception as e:
            print(f"   ❌ Database check failed: {str(e)}")
            self.diagnosis_report['database_exists'] = False
            return None
    
    def _validate_schema(self):
        """Validate current schema against expected schema"""
        try:
            print("   🔍 Retrieving current database schema...")
            
            database = self.notion.databases.retrieve(database_id=self.database_id)
            current_properties = database.get('properties', {})
            
            print(f"   📊 Current schema has {len(current_properties)} properties")
            print(f"   📊 Expected schema has {len(self.expected_schema)} properties")
            
            # Check each expected property
            missing_properties = []
            incorrect_types = []
            
            for prop_name, expected_config in self.expected_schema.items():
                if prop_name not in current_properties:
                    missing_properties.append({
                        'name': prop_name,
                        'expected_type': expected_config['type'],
                        'required': expected_config.get('required', False),
                        'description': expected_config.get('description', '')
                    })
                    print(f"   ❌ Missing property: {prop_name} ({expected_config['type']})")
                else:
                    current_prop = current_properties[prop_name]
                    current_type = current_prop.get('type')
                    expected_type = expected_config['type']
                    
                    if current_type != expected_type:
                        incorrect_types.append({
                            'name': prop_name,
                            'current_type': current_type,
                            'expected_type': expected_type,
                            'description': expected_config.get('description', '')
                        })
                        print(f"   ⚠️  Type mismatch: {prop_name} (is {current_type}, should be {expected_type})")
                    else:
                        print(f"   ✅ Property OK: {prop_name} ({current_type})")
            
            # Check for unexpected properties
            unexpected_properties = []
            for prop_name in current_properties:
                if prop_name not in self.expected_schema:
                    unexpected_properties.append({
                        'name': prop_name,
                        'type': current_properties[prop_name].get('type'),
                        'description': 'Not in expected schema'
                    })
                    print(f"   🔍 Unexpected property: {prop_name} ({current_properties[prop_name].get('type')})")
            
            # Update diagnosis
            self.diagnosis_report['missing_properties'] = missing_properties
            self.diagnosis_report['incorrect_types'] = incorrect_types
            self.diagnosis_report['schema_complete'] = len(missing_properties) == 0 and len(incorrect_types) == 0
            
            print(f"\n   📊 SCHEMA VALIDATION SUMMARY:")
            print(f"   ✅ Correct properties: {len(current_properties) - len(missing_properties) - len(incorrect_types)}")
            print(f"   ❌ Missing properties: {len(missing_properties)}")
            print(f"   ⚠️  Type mismatches: {len(incorrect_types)}")
            print(f"   🔍 Unexpected properties: {len(unexpected_properties)}")
            
        except Exception as e:
            print(f"   ❌ Schema validation failed: {str(e)}")
            self.diagnosis_report['schema_issues'].append(f"Validation failed: {str(e)}")
    
    def _analyze_content(self):
        """Analyze existing content in the database"""
        try:
            print("   🔍 Analyzing database content...")
            
            # Get all entries
            response = self.notion.databases.query(
                database_id=self.database_id,
                page_size=100
            )
            
            entries = response['results']
            
            if not entries:
                print("   📭 Database is empty - no content to analyze")
                return
            
            print(f"   📊 Analyzing {len(entries)} entries...")
            
            # Analyze content patterns
            analysis = {
                'total_entries': len(entries),
                'entries_with_full_prompt': 0,
                'entries_with_dna_hash': 0,
                'entries_with_analysis_date': 0,
                'entries_with_health_status': 0,
                'prompt_types': {},
                'health_statuses': {},
                'average_content_length': 0
            }
            
            total_content_length = 0
            
            for entry in entries:
                props = entry.get('properties', {})
                
                # Check for Full Prompt content
                if 'Full Prompt' in props and props['Full Prompt'].get('rich_text'):
                    analysis['entries_with_full_prompt'] += 1
                    content_length = len(props['Full Prompt']['rich_text'][0].get('plain_text', ''))
                    total_content_length += content_length
                
                # Check for archaeological fields
                if 'DNA Hash' in props and props['DNA Hash'].get('rich_text'):
                    analysis['entries_with_dna_hash'] += 1
                
                if 'Analysis Date' in props and props['Analysis Date'].get('date'):
                    analysis['entries_with_analysis_date'] += 1
                
                if 'Health Status' in props and props['Health Status'].get('select'):
                    analysis['entries_with_health_status'] += 1
                    status = props['Health Status']['select']['name']
                    analysis['health_statuses'][status] = analysis['health_statuses'].get(status, 0) + 1
                
                # Track prompt types
                if 'Type' in props and props['Type'].get('select'):
                    ptype = props['Type']['select']['name']
                    analysis['prompt_types'][ptype] = analysis['prompt_types'].get(ptype, 0) + 1
            
            if analysis['entries_with_full_prompt'] > 0:
                analysis['average_content_length'] = total_content_length // analysis['entries_with_full_prompt']
            
            # Display analysis
            print(f"   📊 CONTENT ANALYSIS:")
            print(f"   📝 Entries with content: {analysis['entries_with_full_prompt']}/{analysis['total_entries']}")
            print(f"   🧬 Entries with DNA hash: {analysis['entries_with_dna_hash']}/{analysis['total_entries']}")
            print(f"   📅 Entries analyzed: {analysis['entries_with_analysis_date']}/{analysis['total_entries']}")
            print(f"   🏥 Entries with health status: {analysis['entries_with_health_status']}/{analysis['total_entries']}")
            print(f"   📏 Average content length: {analysis['average_content_length']} characters")
            
            if analysis['prompt_types']:
                print(f"   📊 Prompt types distribution:")
                for ptype, count in analysis['prompt_types'].items():
                    print(f"      {ptype}: {count}")
            
            if analysis['health_statuses']:
                print(f"   🏥 Health status distribution:")
                for status, count in analysis['health_statuses'].items():
                    print(f"      {status}: {count}")
            
            self.diagnosis_report['content_analysis'] = analysis
            
        except Exception as e:
            print(f"   ❌ Content analysis failed: {str(e)}")
    
    def _generate_recommendations(self):
        """Generate repair and optimization recommendations"""
        recommendations = []
        
        if not self.diagnosis_report['database_exists']:
            recommendations.append("🚨 CRITICAL: Database does not exist - create database first")
        
        if self.diagnosis_report['connection_status'] != 'connected':
            recommendations.append("🚨 CRITICAL: Cannot connect to database - check credentials")
        
        if self.diagnosis_report['missing_properties']:
            recommendations.append(f"🔧 SCHEMA: Add {len(self.diagnosis_report['missing_properties'])} missing properties")
        
        if self.diagnosis_report['incorrect_types']:
            recommendations.append(f"⚠️  SCHEMA: Fix {len(self.diagnosis_report['incorrect_types'])} type mismatches")
        
        content_analysis = self.diagnosis_report.get('content_analysis', {})
        if content_analysis:
            total = content_analysis['total_entries']
            if total > 0:
                analyzed_ratio = content_analysis['entries_with_analysis_date'] / total
                if analyzed_ratio < 0.5:
                    recommendations.append(f"🔬 ANALYSIS: Run archaeological analysis on {total - content_analysis['entries_with_analysis_date']} entries")
                
                if content_analysis['entries_with_dna_hash'] == 0:
                    recommendations.append("🧬 DNA: No entries have DNA hashes - run analysis to generate")
        
        if self.diagnosis_report['entry_count'] == 0:
            recommendations.append("📝 CONTENT: Database is empty - add some prompts first")
        
        self.diagnosis_report['recommendations'] = recommendations
        
        print("   🎯 RECOMMENDATIONS:")
        if recommendations:
            for rec in recommendations:
                print(f"   {rec}")
        else:
            print("   ✅ No major issues found - database appears healthy!")
    
    def _offer_schema_repair(self):
        """Offer to automatically repair schema issues"""
        if not self.diagnosis_report['missing_properties'] and not self.diagnosis_report['incorrect_types']:
            print("   ✅ Schema is complete - no repairs needed")
            return
        
        print(f"   🔧 SCHEMA REPAIR OPTIONS:")
        print(f"   Missing properties: {len(self.diagnosis_report['missing_properties'])}")
        print(f"   Type mismatches: {len(self.diagnosis_report['incorrect_types'])}")
        print()
        
        try:
            response = input("   Would you like to automatically repair the schema? (y/n): ")
            if response.lower() == 'y':
                self._repair_schema()
            else:
                print("   ⏭️  Schema repair skipped")
        except (EOFError, KeyboardInterrupt):
            print("   ⏭️  Schema repair skipped (non-interactive mode)")
    
    def _repair_schema(self):
        """Actually repair the schema by adding missing properties"""
        print("   🔧 Starting schema repair...")
        
        try:
            properties_to_add = {}
            
            for missing_prop in self.diagnosis_report['missing_properties']:
                prop_name = missing_prop['name']
                expected_config = self.expected_schema[prop_name]
                
                print(f"   ➕ Adding property: {prop_name} ({expected_config['type']})")
                
                # Build property configuration
                prop_config = {"type": expected_config['type']}
                
                if expected_config['type'] == 'select':
                    prop_config['select'] = {"options": expected_config.get('options', [])}
                elif expected_config['type'] == 'multi_select':
                    prop_config['multi_select'] = {"options": expected_config.get('options', [])}
                elif expected_config['type'] == 'number':
                    prop_config['number'] = {"format": "number"}
                elif expected_config['type'] == 'rich_text':
                    prop_config['rich_text'] = {}
                elif expected_config['type'] == 'date':
                    prop_config['date'] = {}
                elif expected_config['type'] == 'relation':
                    prop_config['relation'] = {
                        "database_id": self.database_id,
                        "single_property": {}
                    }
                
                properties_to_add[prop_name] = prop_config
            
            if properties_to_add:
                print(f"   🔄 Updating database with {len(properties_to_add)} new properties...")
                
                self.notion.databases.update(
                    database_id=self.database_id,
                    properties=properties_to_add
                )
                
                print("   ✅ Schema repair completed successfully!")
                
                # Re-validate schema
                print("   🔍 Re-validating schema...")
                self._validate_schema()
            else:
                print("   ⚠️  No properties to add")
                
        except Exception as e:
            print(f"   ❌ Schema repair failed: {str(e)}")
    
    def _generate_final_report(self):
        """Generate comprehensive final diagnostic report"""
        print("📋" + "=" * 70)
        print("📋 FINAL DIAGNOSTIC REPORT")
        print("📋" + "=" * 70)
        
        # Connection status
        print(f"🔌 Connection Status: {self.diagnosis_report['connection_status']}")
        print(f"🏛️  Database Exists: {self.diagnosis_report['database_exists']}")
        
        if self.diagnosis_report['database_exists']:
            print(f"📋 Database Title: {self.diagnosis_report['database_title']}")
            print(f"📊 Entry Count: {self.diagnosis_report['entry_count']}")
        
        # Schema status
        print(f"🧬 Schema Complete: {self.diagnosis_report['schema_complete']}")
        print(f"❌ Missing Properties: {len(self.diagnosis_report['missing_properties'])}")
        print(f"⚠️  Type Mismatches: {len(self.diagnosis_report['incorrect_types'])}")
        
        # Content analysis
        content_analysis = self.diagnosis_report.get('content_analysis')
        if content_analysis:
            print(f"📝 Content Analysis:")
            print(f"   Entries with content: {content_analysis['entries_with_full_prompt']}/{content_analysis['total_entries']}")
            print(f"   Archaeological analysis: {content_analysis['entries_with_analysis_date']}/{content_analysis['total_entries']}")
        
        # Recommendations
        print(f"\n🎯 ACTION ITEMS ({len(self.diagnosis_report['recommendations'])}):")
        for rec in self.diagnosis_report['recommendations']:
            print(f"   {rec}")
        
        # Overall health
        if self.diagnosis_report['schema_complete'] and self.diagnosis_report['database_exists']:
            print(f"\n🎉 OVERALL STATUS: HEALTHY - Ready for archaeological operations!")
        else:
            print(f"\n⚠️  OVERALL STATUS: NEEDS ATTENTION - Schema repair required")
        
        print("📋" + "=" * 70)
    
    def save_diagnostic_report(self, filename: str = None):
        """Save detailed diagnostic report to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"prompt_db_diagnostic_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.diagnosis_report, f, indent=2)
            print(f"💾 Diagnostic report saved to: {filename}")
        except Exception as e:
            print(f"❌ Failed to save report: {str(e)}")

def main():
    """Main diagnostic execution"""
    print("🚀 Starting KHAOS Prompt Database Diagnostic...")
    
    # Check environment
    if not os.path.exists('.env'):
        print("❌ .env file not found - please create one with required tokens")
        return
    
    # Run diagnostic
    diagnostic = PromptDatabaseDiagnostic()
    diagnostic.run_comprehensive_diagnostic()
    
    # Offer to save report
    try:
        save_report = input("\nWould you like to save the diagnostic report? (y/n): ")
        if save_report.lower() == 'y':
            diagnostic.save_diagnostic_report()
    except (EOFError, KeyboardInterrupt):
        print("\nDiagnostic completed.")

if __name__ == "__main__":
    main()
