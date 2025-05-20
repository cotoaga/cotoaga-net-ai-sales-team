# KHAOS AI Systems

This repository contains two interrelated AI-powered systems:

1. **Prompt Management System**: The foundation - a system for creating, storing, and evolving structured AI prompts
2. **Lead Generation System**: Built on top - a system for EU AI Act lead generation and prospect management

## Repository Structure

```
/
├── prompt_management/  # Core prompt system
│   ├── scripts/        # Command-line tools
│   ├── lib/            # Reusable libraries
│   ├── templates/      # Sample prompt templates
│   └── README.md       # Documentation
│
├── lead_generation/    # Lead generation system
│   ├── scripts/        # Command-line tools
│   ├── lib/            # Reusable libraries
│   ├── data/           # Data directory (for exports/imports)
│   └── README.md       # Documentation
│
├── common/             # Shared utilities
│   └── utils/          # Common utilities
│
├── .env                # Environment variables
├── .gitignore          # Git ignore patterns
└── README.md           # This file
```

## Environment Setup

The `.env` file contains configuration for both systems, each with its own Notion integration:

```
# Prompt Management System
PROMPT_SECURITY_TOKEN=your_prompt_notion_token
PROMPT_DATABASE_ID=your_prompt_database_id

# Lead Generation System
LEAD_SECURITY_TOKEN=your_lead_notion_token
LEAD_DATABASE_ID=your_lead_database_id
```

## Prompt Management System

The Prompt Management System is the foundation of KHAOS, managing structured AI prompts based on a meta-template architecture.

### Key Features

- Create, read, update, and delete prompts in a Notion database
- Structured prompt format with comprehensive metadata
- Versioning and inheritance tracking
- Support for viral propagation and meme spreading

### Getting Started

1. Set up your environment:
   ```
   PROMPT_SECURITY_TOKEN=your_notion_integration_token
   PROMPT_DATABASE_ID=your_notion_database_id
   ```

2. Create your prompt database:
   ```bash
   cd prompt_management/scripts
   python create_database.py
   ```

3. Verify and seed your database:
   ```bash
   python check_and_seed.py
   ```

4. Manage your prompts:
   ```bash
   # List all prompts
   python prompt_cli.py list
   
   # Create a new prompt
   python prompt_cli.py create ../templates/khaos-new-prompt.txt
   
   # Read a prompt
   python prompt_cli.py read khaos-meta-template
   
   # Update a prompt
   python prompt_cli.py update khaos-example ../templates/khaos-example-updated.txt
   
   # Delete a prompt
   python prompt_cli.py delete test-prompt
   ```

## Lead Generation System

The Lead Generation System is built on top of the prompt foundation, focused on managing and nurturing leads for EU AI Act compliance consulting.

### Key Features

- Extract contacts from multiple sources (macOS Contacts, vCard exports, LinkedIn)
- Process leads through a structured pipeline: Raw Import → Enrichment → Scoring → Personalization
- Store and manage prospects in a Notion database
- Generate personalized outreach content

### Getting Started

1. Set up your environment:
   ```
   LEAD_SECURITY_TOKEN=your_notion_integration_token
   LEAD_DATABASE_ID=your_notion_database_id
   ```

2. Create your prospects database:
   ```bash
   cd lead_generation/scripts
   python setup_database.py
   ```

3. Import contacts:
   ```bash
   # From macOS contacts
   python macos_contact_extractor.py
   
   # From vCard file
   python vcard_extractor.py data/contacts_export.vcf
   ```

4. Process and enrich:
   ```bash
   # Add processing stages to track progress
   python add_processing_stage.py
   
   # LinkedIn enrichment (requires setup)
   python linkedin_enricher.py
   ```

## Integration Between Systems

The Prompt Management System provides the foundation for how the Lead Generation System interacts with leads:

1. Prompt templates dictate the messaging style and approach
2. Lead-specific data enriches the prompts to create personalized content
3. Specialized prompts for different lead stages and scenarios

## Development

This project follows these principles:

1. **KISS (Keep It Simple, Stupid)**: Favor simplicity over complexity
2. **Separation of Concerns**: Each subsystem has its own directory and configuration
3. **Progressive Enhancement**: Raw data → Basic Cleaning → Enrichment → AI Scoring

## Requirements

- Python 3.8+
- Notion API access
- Required packages: `notion-client`, `python-dotenv`, `pandas`
