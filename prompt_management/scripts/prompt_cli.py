#!/usr/bin/env python3
"""
KHAOS Prompt Library CLI
A command-line interface for managing your prompt library
NOW WITH ARCHAEOLOGICAL DNA ANALYSIS SUPERPOWERS!
"""

import os
import sys

# Add the parent directory to the sys.path to find modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import argparse
from lib.prompt_manager import PromptManager

def main():
    parser = argparse.ArgumentParser(description="KHAOS Prompt Library Manager with Archaeological Analysis")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # ═══════════════════════════════════════════════════════════════
    # EXISTING COMMANDS (Keep all your original functionality)
    # ═══════════════════════════════════════════════════════════════
    
    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Setup the Notion database schema")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new prompt")
    create_parser.add_argument("file", help="Path to the prompt file")
    
    # Read command
    read_parser = subparsers.add_parser("read", help="Read a prompt")
    read_parser.add_argument("prompt_id", help="ID of the prompt to read")
    read_parser.add_argument("--save", help="Path to save the prompt to", default=None)
    
    # Update command
    update_parser = subparsers.add_parser("update", help="Update an existing prompt")
    update_parser.add_argument("prompt_id", help="ID of the prompt to update")
    update_parser.add_argument("file", help="Path to the updated prompt file")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a prompt")
    delete_parser.add_argument("prompt_id", help="ID of the prompt to delete")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all prompts")
    list_parser.add_argument("--type", help="Filter by prompt type", default=None)
    
    # ═══════════════════════════════════════════════════════════════
    # NEW ARCHAEOLOGICAL COMMANDS (The Digital DNA Analysis Suite)
    # ═══════════════════════════════════════════════════════════════
    
    # Analyze command - The main DNA analysis
    analyze_parser = subparsers.add_parser("analyze", help="🔬 Analyze prompt DNA and generate archaeological report")
    analyze_parser.add_argument("prompt_id", help="ID of the prompt to analyze")
    analyze_parser.add_argument("--save-report", help="Save analysis report to file", default=None)
    analyze_parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed analysis")
    
    # Health Check command - System-wide diagnosis
    health_parser = subparsers.add_parser("health-check", help="🏥 Perform health check on all prompts")
    health_parser.add_argument("--detailed", "-d", action="store_true", help="Show detailed health report")
    health_parser.add_argument("--save-report", help="Save health report to file", default=None)
    
    # Optimize command - Get improvement suggestions
    optimize_parser = subparsers.add_parser("optimize", help="⚡ Get optimization suggestions for a prompt")
    optimize_parser.add_argument("prompt_id", help="ID of the prompt to optimize")
    optimize_parser.add_argument("--apply", action="store_true", help="Apply automatic optimizations (when available)")
    
    # Lineage command - Trace prompt family tree
    lineage_parser = subparsers.add_parser("lineage", help="🌳 Trace prompt lineage and family relationships")
    lineage_parser.add_argument("prompt_id", nargs="?", help="ID of the prompt to trace (optional)")
    lineage_parser.add_argument("--show-tree", action="store_true", help="Show visual family tree")
    lineage_parser.add_argument("--all", action="store_true", help="Show lineage for all prompts")
    
    # Evolution command - Track prompt mutations over time
    evolution_parser = subparsers.add_parser("evolution", help="🧬 Track prompt evolution and mutations")
    evolution_parser.add_argument("--trace-mutations", action="store_true", help="Show mutation history")
    evolution_parser.add_argument("--fitness-trends", action="store_true", help="Show fitness evolution over time")
    
    # Compare command - Compare two prompts side by side
    compare_parser = subparsers.add_parser("compare", help="⚖️ Compare DNA profiles of two prompts")
    compare_parser.add_argument("prompt_id_1", help="First prompt ID")
    compare_parser.add_argument("prompt_id_2", help="Second prompt ID")
    compare_parser.add_argument("--detailed", "-d", action="store_true", help="Show detailed comparison")
    
    # Stats command - Show database statistics
    stats_parser = subparsers.add_parser("stats", help="📊 Show prompt database statistics")
    stats_parser.add_argument("--breakdown", help="Break down by field (type, effectiveness, complexity)", default=None)
    
    # Schema command - Show database schema/properties
    schema_parser = subparsers.add_parser("schema", help="🏗️ Show database schema and properties")
    schema_parser.add_argument("--detailed", "-d", action="store_true", help="Show detailed property information")
    schema_parser.add_argument("--type", help="Filter by property type (select, rich_text, number, etc.)", default=None)
    
    # Evolve command - Create evolved version of existing prompt
    evolve_parser = subparsers.add_parser("evolve", help="🧬 Create evolved version of existing prompt")
    evolve_parser.add_argument("prompt_id", help="ID of the prompt to evolve")
    evolve_parser.add_argument("--save-template", help="Save evolved template to file", default=None)
    evolve_parser.add_argument("--auto-create", action="store_true", help="Automatically create evolved version in database")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize the prompt manager
    manager = PromptManager()
    
    # Check if we're properly configured
    if not os.getenv("PROMPT_DATABASE_ID"):
        print("❌ Error: PROMPT_DATABASE_ID not set in .env file")
        print("Please add the following to your .env file:")
        print("PROMPT_DATABASE_ID=your_prompts_database_id")
        print("\nYou can also run:")
        print("1. python create_database.py (to create a new database)")
        sys.exit(1)
    
    # Execute the appropriate command
    if args.command == "setup":
        print("🔧 Setting up database schema with archaeological enhancements...")
        success = manager.setup_database()
        if success:
            print("✅ Database setup complete! Ready for prompt archaeology.")
        else:
            print("❌ Database setup failed. Check your configuration.")
        
    elif args.command == "create":
        print(f"📝 Creating new prompt from: {args.file}")
        result = manager.create_prompt(args.file)
        if result:
            print("✅ Prompt created successfully!")
            print("🔬 Tip: Run 'analyze' command to see its DNA profile.")
        else:
            print("❌ Failed to create prompt. Check file format and content.")
        
    elif args.command == "read":
        prompt = manager.read_prompt(args.prompt_id)
        if prompt:
            if args.save:
                # Generate full prompt content for saving
                full_content = _generate_full_prompt_content(prompt)
                with open(args.save, "w") as f:
                    f.write(full_content)
                print(f"💾 Prompt saved to: {args.save}")
            else:
                print("\n" + "="*70)
                print(f"🧬 PROMPT: {args.prompt_id} (v{prompt['Version']})")
                print("="*70)
                
                # Display structured content
                _display_prompt_content(prompt)
                
                print("="*70)
        
    elif args.command == "update":
        print(f"🔄 Updating prompt: {args.prompt_id}")
        success = manager.update_prompt(args.prompt_id, args.file)
        if success:
            print("✅ Prompt updated successfully!")
            print("🔬 Tip: Re-analyze to see how the DNA changed.")
        else:
            print("❌ Failed to update prompt.")
        
    elif args.command == "delete":
        confirmation = input(f"⚠️  Are you sure you want to delete prompt '{args.prompt_id}'? (y/n): ")
        if confirmation.lower() == "y":
            success = manager.delete_prompt(args.prompt_id)
            if success:
                print("🗑️  Prompt deleted (archived) successfully.")
            else:
                print("❌ Failed to delete prompt.")
        else:
            print("❌ Delete operation cancelled")
        
    elif args.command == "list":
        prompts = manager.list_prompts(args.type)
        print("\n" + "="*70)
        print("🧬 KHAOS PROMPT LIBRARY - DIGITAL SPECIMEN CATALOG")
        print("="*70)
        print(f"Found {len(prompts)} prompts" + (f" (filtered by type: {args.type})" if args.type else ""))
        print("-"*70)
        
        if prompts:
            for i, p in enumerate(prompts, 1):
                type_emoji = {
                    'meta': '🎭', 'consultation': '💼', 'workshop': '🎓', 
                    'analysis': '🔬', 'creation': '🎨', 'viral': '🦠',
                    'coding-companion': '💻'
                }.get(p.get('Type', ''), '📄')
                
                print(f"{i:2}. {type_emoji} {p['Prompt ID']} (v{p['Version']})")
                print(f"    📅 Last modified: {p['Last Modified'] or 'Unknown'}")
                if i < len(prompts):
                    print()
        else:
            print("📭 No prompts found. Use 'create' command to add some!")
            
        print("="*70)
        print("🔬 Use 'analyze [prompt_id]' for DNA analysis")
        print("🏥 Use 'health-check' for system-wide diagnosis")
    
    # ═══════════════════════════════════════════════════════════════
    # ARCHAEOLOGICAL COMMAND IMPLEMENTATIONS
    # ═══════════════════════════════════════════════════════════════
    
    elif args.command == "analyze":
        print(f"🔬 ENHANCED ARCHAEOLOGICAL ANALYSIS: {args.prompt_id}")
        print("=" * 70)
        
        # First, get complete property data using our enhanced read method
        print("📊 Phase 1: Complete Property Extraction...")
        prompt_data = manager.read_prompt(args.prompt_id, include_all_properties=True)
        
        if not prompt_data:
            print("❌ Analysis failed - prompt not found or inaccessible")
            return
        
        # Display property population status
        if '_metadata' in prompt_data:
            meta = prompt_data['_metadata']
            print(f"✅ Property Status: {meta['populated_properties']}/{meta['total_properties']} properties ({meta['population_percentage']:.1f}%)")
        
        # Phase 2: Perform DNA analysis
        print("\n🧬 Phase 2: DNA Analysis...")
        dna_profile = manager.analyze_prompt_dna(args.prompt_id)
        
        if dna_profile:
            # Generate and display the analysis report
            report = manager.generate_analysis_report(dna_profile)
            print(report)
            
            if args.verbose:
                print("\n🔍 ENHANCED ARCHAEOLOGICAL DATA:")
                print("-" * 50)
                print(f"Content Hash: {dna_profile['content_hash']}")
                print(f"Token Count: {dna_profile['token_count']}")
                print(f"Complexity Factors: {dna_profile['complexity_score']:.2f}")
                print(f"Personality Conflicts: {dna_profile['personality_conflicts']}")
                print(f"Viral Coefficient: {dna_profile['viral_potential']['viral_coefficient']:.2f}")
                
                # Show property completeness analysis
                print(f"\n📊 PROPERTY COMPLETENESS ANALYSIS:")
                core_properties = ['Purpose', 'System Instructions', 'Instruction', 'Output Format']
                populated_core = sum(1 for prop in core_properties if prompt_data.get(prop) and prompt_data[prop].strip())
                print(f"  Core Content Properties: {populated_core}/{len(core_properties)} populated")
                
                config_properties = ['Type', 'Models', 'Temperature', 'Security Level']
                populated_config = sum(1 for prop in config_properties if prompt_data.get(prop))
                print(f"  Configuration Properties: {populated_config}/{len(config_properties)} populated")
                
                analysis_properties = ['DNA Hash', 'Complexity Score', 'Effectiveness Score', 'Health Status']
                populated_analysis = sum(1 for prop in analysis_properties if prompt_data.get(prop))
                print(f"  Analysis Properties: {populated_analysis}/{len(analysis_properties)} populated")
                
                # Show instruction analysis
                struct = dna_profile['instruction_analysis']
                print(f"\n🏗️ STRUCTURAL ARCHAEOLOGY:")
                print(f"  Word Count: {struct['word_count']}")
                print(f"  Line Count: {struct['line_count']}")
                print(f"  Section Count: {struct['section_count']}")
                print(f"  Instruction Count: {struct['instruction_count']}")
                
                # Show missing critical properties
                missing_critical = []
                critical_props = ['Purpose', 'System Instructions', 'Type', 'Version']
                for prop in critical_props:
                    if not prompt_data.get(prop) or (isinstance(prompt_data[prop], str) and not prompt_data[prop].strip()):
                        missing_critical.append(prop)
                
                if missing_critical:
                    print(f"\n⚠️  MISSING CRITICAL PROPERTIES:")
                    for prop in missing_critical:
                        print(f"  • {prop}")
                else:
                    print(f"\n✅ All critical properties populated!")
            
            # Save enhanced report if requested
            if args.save_report:
                enhanced_report = report + f"\n\n📊 PROPERTY ANALYSIS:\n"
                enhanced_report += f"Population: {meta['populated_properties']}/{meta['total_properties']} ({meta['population_percentage']:.1f}%)\n"
                enhanced_report += f"Extraction Time: {meta['extraction_timestamp']}\n"
                
                with open(args.save_report, "w") as f:
                    f.write(enhanced_report)
                print(f"\n💾 Enhanced analysis report saved to: {args.save_report}")
        else:
            print("❌ DNA analysis failed - unable to process prompt content")
    
    elif args.command == "health-check":
        print("🏥 ENHANCED SYSTEM-WIDE HEALTH CHECK")
        print("=" * 70)
        print("Leveraging complete 38-property database sovereignty...")
        
        # Phase 1: Get all prompts with complete property data
        print("\n📊 Phase 1: Complete Property Assessment...")
        all_prompts = manager.list_prompts()
        
        if not all_prompts:
            print("❌ No prompts found in database")
            return
        
        # Enhanced health analysis with complete property awareness
        total_prompts = len(all_prompts)
        property_health = []
        dna_health = []
        
        print(f"✅ Found {total_prompts} prompts for comprehensive analysis")
        
        # Phase 2: Detailed property and health analysis
        print("\n🔬 Phase 2: Detailed Health Analysis...")
        
        for i, prompt_summary in enumerate(all_prompts, 1):
            prompt_id = prompt_summary['Prompt ID']
            print(f"  Analyzing {i}/{total_prompts}: {prompt_id}")
            
            # Get complete property data
            prompt_data = manager.read_prompt(prompt_id, include_all_properties=True)
            if prompt_data and '_metadata' in prompt_data:
                property_health.append({
                    'prompt_id': prompt_id,
                    'populated_properties': prompt_data['_metadata']['populated_properties'],
                    'population_percentage': prompt_data['_metadata']['population_percentage']
                })
        
        # Phase 3: Traditional DNA health check
        print("\n🧬 Phase 3: DNA Health Assessment...")
        health_report = manager.health_check_all_prompts()
        
        if 'error' in health_report:
            print(f"❌ DNA health check failed: {health_report['error']}")
            return
        
        # Enhanced health summary
        print(f"\n📊 ENHANCED SYSTEM HEALTH SUMMARY:")
        print(f"{'='*50}")
        
        # Property completeness analysis
        if property_health:
            avg_population = sum(p['population_percentage'] for p in property_health) / len(property_health)
            fully_populated = sum(1 for p in property_health if p['population_percentage'] >= 95)
            well_populated = sum(1 for p in property_health if p['population_percentage'] >= 80)
            poorly_populated = sum(1 for p in property_health if p['population_percentage'] < 50)
            
            print(f"🏗️ PROPERTY COMPLETENESS:")
            print(f"  Average Population: {avg_population:.1f}%")
            print(f"  Fully Populated (≥95%): {fully_populated}/{total_prompts} ({fully_populated/total_prompts*100:.1f}%)")
            print(f"  Well Populated (≥80%): {well_populated}/{total_prompts} ({well_populated/total_prompts*100:.1f}%)")
            print(f"  Poorly Populated (<50%): {poorly_populated}/{total_prompts} ({poorly_populated/total_prompts*100:.1f}%)")
        
        # Traditional health metrics
        total = health_report['total_prompts']
        healthy = health_report['healthy_prompts']
        needs_opt = health_report['optimization_needed']
        problematic = health_report['problematic_prompts']
        unanalyzed = health_report['unanalyzed_prompts']
        
        print(f"\n🧬 DNA HEALTH STATUS:")
        print(f"  Total Prompts: {total}")
        print(f"  Healthy: {healthy} ✅ ({healthy/total*100:.1f}%)")
        print(f"  Need Optimization: {needs_opt} ⚠️  ({needs_opt/total*100:.1f}%)")
        print(f"  Problematic: {problematic} ❌ ({problematic/total*100:.1f}%)")
        print(f"  Unanalyzed: {unanalyzed} 🔍 ({unanalyzed/total*100:.1f}%)")
        
        # Enhanced health bar visualization
        healthy_bar = '█' * max(1, int(healthy/total*30)) if total > 0 else ''
        warning_bar = '▓' * max(1, int(needs_opt/total*30)) if total > 0 else ''
        problem_bar = '▒' * max(1, int(problematic/total*30)) if total > 0 else ''
        unanalyzed_bar = '░' * max(1, int(unanalyzed/total*30)) if total > 0 else ''
        
        print(f"\nHealth Visualization:")
        print(f"  |{healthy_bar}{warning_bar}{problem_bar}{unanalyzed_bar}|")
        print(f"  ✅ Healthy  ⚠️ Warning  ❌ Problem  🔍 Unanalyzed")
        
        # Enhanced recommendations
        print(f"\n🎯 ENHANCED RECOMMENDATIONS:")
        
        if property_health:
            if avg_population < 70:
                print(f"  🏗️ PROPERTY COMPLETENESS: Average population is {avg_population:.1f}% - improve data entry")
            if poorly_populated > 0:
                print(f"  📝 DATA QUALITY: {poorly_populated} prompts are poorly populated (<50% properties)")
        
        if unanalyzed > total * 0.3:
            print(f"  🔬 ANALYSIS COVERAGE: {unanalyzed} prompts need DNA analysis (>30% unanalyzed)")
        
        if health_report['recommendations']:
            for rec in health_report['recommendations']:
                print(f"  🧬 {rec}")
        
        # Show detailed issues if requested
        if args.detailed:
            if property_health:
                print(f"\n🔍 DETAILED PROPERTY ANALYSIS:")
                for p in sorted(property_health, key=lambda x: x['population_percentage']):
                    status = "🔴" if p['population_percentage'] < 50 else "🟡" if p['population_percentage'] < 80 else "🟢"
                    print(f"  {status} {p['prompt_id']}: {p['populated_properties']}/38 ({p['population_percentage']:.1f}%)")
            
            if health_report['issues_found']:
                print(f"\n🔍 DETAILED DNA HEALTH ISSUES:")
                for issue in health_report['issues_found']:
                    if 'error' in issue:
                        print(f"  ❌ {issue['prompt_id']}: {issue['error']}")
                    else:
                        print(f"  ⚠️  {issue['prompt_id']}:")
                        print(f"      Effectiveness: {issue.get('effectiveness', 'N/A')}")
                        print(f"      Complexity: {issue.get('complexity', 'N/A')}")
                        print(f"      Health Status: {issue.get('health_status', 'N/A')}")
        
        # Save enhanced report if requested
        if args.save_report:
            import json
            enhanced_report = {
                **health_report,
                'property_completeness': {
                    'average_population': avg_population if property_health else 0,
                    'property_details': property_health
                },
                'analysis_timestamp': datetime.now().isoformat()
            }
            
            with open(args.save_report, "w") as f:
                json.dump(enhanced_report, f, indent=2)
            print(f"\n💾 Enhanced health report saved to: {args.save_report}")
        
        print(f"\n🎉 Enhanced health check complete!")
        print(f"📊 Database sovereignty: ✅ Complete access to all 38 properties")
    
    elif args.command == "optimize":
        print(f"⚡ Generating optimization suggestions for: {args.prompt_id}")
        print("=" * 60)
        
        # First analyze the prompt
        dna_profile = manager.analyze_prompt_dna(args.prompt_id)
        if dna_profile:
            # Generate optimization suggestions
            suggestions = manager.generate_optimization_suggestions(dna_profile)
            
            print("🔧 OPTIMIZATION SUGGESTIONS:")
            print("-" * 40)
            for i, suggestion in enumerate(suggestions, 1):
                print(f"{i}. {suggestion}")
            
            # Show current vs target metrics
            print(f"\n📊 IMPROVEMENT TARGETS:")
            print(f"Current Effectiveness: {dna_profile['effectiveness_score']:.1%}")
            print(f"Current Complexity: {dna_profile['complexity_score']:.1f}/10")
            print(f"Personality Conflicts: {dna_profile['personality_conflicts']}")
            
            if args.apply:
                print("\n🚀 AUTO-OPTIMIZATION:")
                print("(Auto-optimization not yet implemented - requires manual review)")
                print("Consider the suggestions above and manually edit your prompt file.")
                print("Then use 'update' command to apply changes.")
        else:
            print("❌ Cannot optimize - analysis failed")
    
    elif args.command == "lineage":
        if args.all:
            print("🌳 Showing lineage for all prompts...")
            print("(Full lineage tracing not yet implemented)")
            print("This feature will show the complete family tree of all prompts.")
        elif args.prompt_id:
            print(f"🌳 Tracing lineage for: {args.prompt_id}")
            print("=" * 60)
            
            lineage = manager.trace_prompt_lineage(args.prompt_id)
            
            if 'error' in lineage:
                print(f"❌ Lineage tracing failed: {lineage['error']}")
            else:
                print(f"📊 LINEAGE REPORT:")
                print(f"Prompt: {lineage['prompt_id']}")
                print(f"Generation: {lineage['generation']}")
                
                if lineage['ancestors']:
                    print(f"\n🔺 ANCESTORS:")
                    for ancestor in lineage['ancestors']:
                        print(f"  Gen {ancestor['generation']}: {ancestor['prompt_id']}")
                
                if lineage['descendants']:
                    print(f"\n🔻 DESCENDANTS:")
                    for descendant in lineage['descendants']:
                        print(f"  Gen {descendant['generation']}: {descendant['prompt_id']}")
                
                if not lineage['ancestors'] and not lineage['descendants']:
                    print("🌱 This prompt appears to be a standalone specimen")
                    print("   (No parent-child relationships detected)")
        else:
            print("❌ Please specify a prompt ID or use --all flag")
            print("Usage: prompt_cli.py lineage [prompt_id]")
    
    elif args.command == "evolution":
        print("🧬 Tracking prompt evolution...")
        print("=" * 60)
        
        if args.trace_mutations:
            print("📈 MUTATION TRACKING:")
            print("(Mutation tracking not yet fully implemented)")
            print("This would show how prompts have changed over time,")
            print("tracking version changes and effectiveness evolution.")
        
        if args.fitness_trends:
            print("📊 FITNESS TRENDS:")
            print("(Fitness trend analysis not yet fully implemented)")  
            print("This would show effectiveness scores over time,")
            print("highlighting which evolutionary changes improved performance.")
            
        if not args.trace_mutations and not args.fitness_trends:
            print("🧬 EVOLUTION OVERVIEW:")
            print("Use --trace-mutations to see change history")
            print("Use --fitness-trends to see performance evolution")
    
    elif args.command == "compare":
        print(f"⚖️ Comparing prompts: {args.prompt_id_1} vs {args.prompt_id_2}")
        print("=" * 60)
        
        # Analyze both prompts
        print("🔬 Analyzing first prompt...")
        dna1 = manager.analyze_prompt_dna(args.prompt_id_1)
        print("🔬 Analyzing second prompt...")
        dna2 = manager.analyze_prompt_dna(args.prompt_id_2)
        
        if dna1 and dna2:
            print("\n📊 COMPARATIVE ANALYSIS:")
            print("-" * 60)
            print(f"{'Metric':<20} | {'Prompt 1':<15} | {'Prompt 2':<15} | {'Winner'}")
            print("-" * 65)
            
            # Compare key metrics
            metrics = [
                ('Effectiveness', 'effectiveness_score'),
                ('Complexity', 'complexity_score'),
                ('Token Count', 'token_count'),
                ('Conflicts', 'personality_conflicts'),
                ('Viral Potential', ('viral_potential', 'viral_coefficient'))
            ]
            
            for metric_name, metric_key in metrics:
                if isinstance(metric_key, tuple):
                    val1 = dna1[metric_key[0]][metric_key[1]]
                    val2 = dna2[metric_key[0]][metric_key[1]]
                else:
                    val1 = dna1[metric_key]
                    val2 = dna2[metric_key]
                
                # Determine winner (lower is better for complexity and conflicts)
                if metric_name in ['Complexity', 'Conflicts']:
                    winner = args.prompt_id_1 if val1 < val2 else args.prompt_id_2 if val2 < val1 else "Tie"
                else:
                    winner = args.prompt_id_1 if val1 > val2 else args.prompt_id_2 if val2 > val1 else "Tie"
                
                print(f"{metric_name:<20} | {val1:<15.2f} | {val2:<15.2f} | {winner}")
            
            if args.detailed:
                print(f"\n🔍 DETAILED PERSONALITY COMPARISON:")
                print("-" * 40)
                print("Personality trait distributions:")
                all_traits = set(dna1['personality_ratios'].keys()) | set(dna2['personality_ratios'].keys())
                for trait in sorted(all_traits):
                    ratio1 = dna1['personality_ratios'].get(trait, 0)
                    ratio2 = dna2['personality_ratios'].get(trait, 0)
                    print(f"  {trait.title():<12}: {ratio1:.1%} vs {ratio2:.1%}")
        else:
            print("❌ Comparison failed - could not analyze one or both prompts")
            if not dna1:
                print(f"   Failed to analyze: {args.prompt_id_1}")
            if not dna2:
                print(f"   Failed to analyze: {args.prompt_id_2}")
    
    elif args.command == "stats":
        print("📊 Prompt Database Statistics")
        print("=" * 60)
        
        # Get all prompts for analysis
        all_prompts = manager.list_prompts()
        
        if not all_prompts:
            print("❌ No prompts found in database")
            print("Use 'create' command to add some prompts first!")
            return
        
        print(f"📈 BASIC STATISTICS:")
        print(f"Total Prompts: {len(all_prompts)}")
        
        # Type breakdown
        type_counts = {}
        for prompt in all_prompts:
            prompt_type = prompt.get('Type', 'Unknown')
            type_counts[prompt_type] = type_counts.get(prompt_type, 0) + 1
        
        if args.breakdown == "type" or not args.breakdown:
            print(f"\n📊 BREAKDOWN BY TYPE:")
            for ptype, count in sorted(type_counts.items()):
                bar = '█' * min(count, 20)
                percentage = count / len(all_prompts) * 100
                print(f"  {ptype:<15}: {count:>3} ({percentage:4.1f}%) |{bar}")
        
        # Version analysis
        if args.breakdown == "version" or not args.breakdown:
            versions = [p.get('Version', '1.0.0') for p in all_prompts]
            major_versions = {}
            for version in versions:
                major = version.split('.')[0] if version else '1'
                major_versions[f"v{major}.x"] = major_versions.get(f"v{major}.x", 0) + 1
            
            print(f"\n📊 BREAKDOWN BY VERSION:")
            for version, count in sorted(major_versions.items()):
                bar = '█' * min(count, 20)
                percentage = count / len(all_prompts) * 100
                print(f"  {version:<15}: {count:>3} ({percentage:4.1f}%) |{bar}")
        
        # This could be extended with effectiveness and complexity breakdowns
        # when we have that data available in the Notion database
        
        if args.breakdown in ["effectiveness", "complexity"]:
            print(f"\n🔬 ANALYSIS BREAKDOWN:")
            print(f"(Advanced statistics require running analysis on all prompts first)")
            print(f"Try: python prompt_cli.py health-check --detailed")
    
    elif args.command == "schema":
        print("🏗️ Database Schema & Properties")
        print("=" * 60)
        
        try:
            # Get database schema
            db = manager.notion.databases.retrieve(database_id=manager.database_id)
            properties = db.get('properties', {})
            
            if not properties:
                print("❌ No properties found in database")
                return
            
            # Filter by type if specified
            if args.type:
                filtered_properties = {name: prop for name, prop in properties.items() 
                                     if prop['type'] == args.type}
                if not filtered_properties:
                    print(f"❌ No properties found with type: {args.type}")
                    return
                properties = filtered_properties
                print(f"Showing properties of type: {args.type}")
            
            # Group properties by type
            prop_by_type = {}
            for name, prop in properties.items():
                prop_type = prop['type']
                if prop_type not in prop_by_type:
                    prop_by_type[prop_type] = []
                prop_by_type[prop_type].append((name, prop))
            
            print(f"📊 Total Properties: {len(properties)}")
            print(f"📊 Property Types: {len(prop_by_type)}")
            print()
            
            # Display by type
            type_order = ['title', 'rich_text', 'select', 'multi_select', 'number', 'date', 'relation']
            
            for prop_type in type_order + [t for t in prop_by_type.keys() if t not in type_order]:
                if prop_type not in prop_by_type:
                    continue
                    
                type_props = prop_by_type[prop_type]
                type_emoji = {
                    'title': '🏷️',
                    'rich_text': '📝',
                    'select': '🎯',
                    'multi_select': '🏷️',
                    'number': '🔢',
                    'date': '📅',
                    'relation': '🔗',
                    'checkbox': '☑️',
                    'url': '🌐',
                    'email': '📧',
                    'phone_number': '📞'
                }.get(prop_type, '❓')
                
                print(f"{type_emoji} {prop_type.upper()} PROPERTIES ({len(type_props)}):")
                print("-" * 40)
                
                for name, prop in sorted(type_props):
                    if args.detailed:
                        print(f"  📋 {name}")
                        
                        if prop_type == 'select' and 'select' in prop:
                            options = prop['select'].get('options', [])
                            if options:
                                print(f"     Options: {', '.join([opt['name'] for opt in options[:5]])}")
                                if len(options) > 5:
                                    print(f"              ... and {len(options) - 5} more")
                        
                        elif prop_type == 'multi_select' and 'multi_select' in prop:
                            options = prop['multi_select'].get('options', [])
                            if options:
                                print(f"     Options: {', '.join([opt['name'] for opt in options[:5]])}")
                                if len(options) > 5:
                                    print(f"              ... and {len(options) - 5} more")
                        
                        elif prop_type == 'relation' and 'relation' in prop:
                            rel_db = prop['relation'].get('database_id', 'Unknown')
                            print(f"     Related DB: {rel_db[:8]}...")
                        
                        elif prop_type == 'number' and 'number' in prop:
                            format_type = prop['number'].get('format', 'number')
                            print(f"     Format: {format_type}")
                        
                        print()
                    else:
                        # Simple format
                        extra_info = ""
                        if prop_type == 'select' and 'select' in prop:
                            option_count = len(prop['select'].get('options', []))
                            extra_info = f" ({option_count} options)"
                        elif prop_type == 'multi_select' and 'multi_select' in prop:
                            option_count = len(prop['multi_select'].get('options', []))
                            extra_info = f" ({option_count} options)"
                        
                        print(f"  • {name}{extra_info}")
                
                print()
            
            # Quick stats
            print("📊 SCHEMA SUMMARY:")
            print("-" * 20)
            for prop_type, count in sorted([(t, len(props)) for t, props in prop_by_type.items()], 
                                         key=lambda x: x[1], reverse=True):
                bar = '█' * min(count, 15)
                print(f"{prop_type:<12}: {count:>2} |{bar}")
            
        except Exception as e:
            print(f"❌ Error retrieving schema: {e}")
    
    elif args.command == "evolve":
        print(f"🧬 Creating evolved version of: {args.prompt_id}")
        print("=" * 60)
        
        # This would create an evolved version based on archaeological analysis
        print("🚧 EVOLUTION CHAMBER:")
        print("(Prompt evolution not yet fully implemented)")
        print("This feature would:")
        print("1. Analyze current prompt DNA")
        print("2. Apply optimization suggestions") 
        print("3. Generate evolved template")
        print("4. Optionally create new database entry")
        
        if args.save_template:
            print(f"Would save evolved template to: {args.save_template}")
        if args.auto_create:
            print("Would automatically create evolved version in database")
    
    else:
        # Show help with some personality
        print("\n🤖 KHAOS Prompt Archaeological Command Center")
        print("=" * 50)
        print("Available expeditions into the digital fossil record:")
        print()
        parser.print_help()
        print("\n🔬 Pro tip: Start with 'list' to see your specimens,")
        print("   then 'analyze' to examine their DNA!")

def _display_prompt_content(prompt):
    """Display structured prompt content in a readable format"""
    sections = [
        ("📋 METADATA", [
            ("Author", prompt.get('Author')),
            ("Version", prompt.get('Version')),
            ("Type", prompt.get('Type')),
            ("Language", prompt.get('Language')),
            ("Parent Prompts", prompt.get('Parent Prompts'))
        ]),
        ("🎯 PURPOSE", [
            ("Purpose", prompt.get('Purpose'))
        ]),
        ("🌍 CONTEXT", [
            ("Context", prompt.get('Context'))
        ]),
        ("🤖 SYSTEM INSTRUCTIONS", [
            ("System Instructions", prompt.get('System Instructions'))
        ]),
        ("📋 INSTRUCTION", [
            ("Instruction", prompt.get('Instruction'))
        ]),
        ("📥 INPUT EXPECTATION", [
            ("User Input Expectation", prompt.get('User Input Expectation'))
        ]),
        ("📤 OUTPUT FORMAT", [
            ("Output Format", prompt.get('Output Format'))
        ]),
        ("🎯 EXAMPLES", [
            ("Few-Shot Examples", prompt.get('Few-Shot Examples'))
        ]),
        ("⚙️ CONFIGURATION", [
            ("Execution Parameters", prompt.get('Execution Parameters')),
            ("Personality Mix", prompt.get('Personality Mix'))
        ]),
        ("📝 NOTES", [
            ("Notes", prompt.get('Notes'))
        ])
    ]
    
    for section_title, fields in sections:
        # Check if any fields in this section have content
        has_content = any(field_value and field_value.strip() for _, field_value in fields)
        if has_content:
            print(f"\n{section_title}")
            print("-" * 50)
            for field_name, field_value in fields:
                if field_value and field_value.strip():
                    if len(field_value) > 200:
                        # Format long content with proper wrapping
                        print(f"{field_value}")
                        print()
                    else:
                        print(f"{field_value}")
                        print()

def _generate_full_prompt_content(prompt):
    """Generate full prompt content for saving to file"""
    content_parts = []
    
    # Header
    content_parts.append(f"PROMPT ID: {prompt.get('Prompt ID', '')}")
    content_parts.append(f"VERSION: {prompt.get('Version', '')}")
    content_parts.append(f"TYPE: {prompt.get('Type', '')}")
    content_parts.append(f"AUTHOR: {prompt.get('Author', '')}")
    content_parts.append(f"LANGUAGE: {prompt.get('Language', '')}")
    content_parts.append(f"PARENT PROMPTS: {prompt.get('Parent Prompts', '')}")
    content_parts.append("")
    
    # Core content sections
    if prompt.get('Purpose'):
        content_parts.append("PURPOSE:")
        content_parts.append(prompt['Purpose'])
        content_parts.append("")
    
    if prompt.get('Context'):
        content_parts.append("CONTEXT:")
        content_parts.append(prompt['Context'])
        content_parts.append("")
    
    if prompt.get('System Instructions'):
        content_parts.append("SYSTEM INSTRUCTIONS:")
        content_parts.append(prompt['System Instructions'])
        content_parts.append("")
    
    if prompt.get('Instruction'):
        content_parts.append("INSTRUCTION:")
        content_parts.append(prompt['Instruction'])
        content_parts.append("")
    
    if prompt.get('User Input Expectation'):
        content_parts.append("INPUT EXPECTATION:")
        content_parts.append(prompt['User Input Expectation'])
        content_parts.append("")
    
    if prompt.get('Output Format'):
        content_parts.append("OUTPUT FORMAT:")
        content_parts.append(prompt['Output Format'])
        content_parts.append("")
    
    if prompt.get('Few-Shot Examples'):
        content_parts.append("FEW-SHOT EXAMPLES:")
        content_parts.append(prompt['Few-Shot Examples'])
        content_parts.append("")
    
    if prompt.get('Execution Parameters'):
        content_parts.append("EXECUTION PARAMETERS:")
        content_parts.append(prompt['Execution Parameters'])
        content_parts.append("")
    
    if prompt.get('Personality Mix'):
        content_parts.append("PERSONALITY MIX:")
        content_parts.append(prompt['Personality Mix'])
        content_parts.append("")
    
    if prompt.get('Notes'):
        content_parts.append("NOTES:")
        content_parts.append(prompt['Notes'])
        content_parts.append("")
    
    return "\n".join(content_parts)

if __name__ == "__main__":
    main()
