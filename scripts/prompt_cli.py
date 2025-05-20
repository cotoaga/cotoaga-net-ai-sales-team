#!/usr/bin/env python3
"""
KHAOS Prompt Library CLI
A command-line interface for managing your prompt library
"""

import os
import sys

# Add the parent directory to the sys.path to find modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import argparse
from prompt_manager import PromptManager

def main():
    parser = argparse.ArgumentParser(description="KHAOS Prompt Library Manager")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
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
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize the prompt manager
    manager = PromptManager()
    
    # Check if we're properly configured
    if not os.getenv("NOTION_PROMPTS_DB_ID"):
        print("❌ Error: NOTION_PROMPTS_DB_ID not set in .env file")
        print("Please add the following to your .env file:")
        print("NOTION_PROMPTS_DB_ID=your_prompts_database_id")
        print("\nYou can also run:")
        print("1. python create_database.py (to create a new database)")
        print("2. python env_manager.py (to update your configuration)")
        sys.exit(1)
    
    # Execute the appropriate command
    if args.command == "setup":
        manager.setup_database()
        
    elif args.command == "create":
        manager.create_prompt(args.file)
        
    elif args.command == "read":
        prompt = manager.read_prompt(args.prompt_id)
        if prompt:
            if args.save:
                with open(args.save, "w") as f:
                    f.write(prompt["Full Prompt"])
                print(f"Prompt saved to {args.save}")
            else:
                print(prompt["Full Prompt"])
        
    elif args.command == "update":
        manager.update_prompt(args.prompt_id, args.file)
        
    elif args.command == "delete":
        confirmation = input(f"Are you sure you want to delete prompt '{args.prompt_id}'? (y/n): ")
        if confirmation.lower() == "y":
            manager.delete_prompt(args.prompt_id)
        else:
            print("Delete operation cancelled")
        
    elif args.command == "list":
        prompts = manager.list_prompts(args.type)
        print("\n=== KHAOS PROMPT LIBRARY ===")
        print(f"Found {len(prompts)} prompts")
        print("-----------------------------")
        for p in prompts:
            print(f"{p['Prompt ID']} (v{p['Version']}) - {p['Type']} - Last modified: {p['Last Modified']}")
        print("=============================")
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
