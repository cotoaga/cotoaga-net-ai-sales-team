# KHAOS Prompt Management System

A system for creating, storing, and evolving structured AI prompts based on a meta-template architecture.

## Directory Structure

```
prompt_management/
├── scripts/             # Command-line tools
│   ├── prompt_cli.py    # CLI for prompt management
│   ├── create_database.py # Create Notion database
│   └── check_and_seed.py # Check schema and add samples
│
├── lib/                 # Core libraries
│   └── prompt_manager.py # Prompt manager class
│
├── templates/           # Sample prompt templates
│   ├── khaos-meta-template.txt
│   ├── khaos-core-persona.txt
│   └── khaos-ai-act-consultant.txt
│
└── README.md            # This file
```

## The KHAOS Meta-Template

The KHAOS system is built around a sophisticated meta-template architecture that includes:

### Core Identification
- Prompt ID, Version, Creation Date, Author
- Parent-child inheritance relationships

### Functional Architecture
- Purpose and Context
- System Instructions and Behavior Guidelines

### Orchestration Layer
- Dependencies and Required Prompts
- Triggers and Activation Conditions
- Integration with other prompts/systems

### Execution Specifications
- Input and Output Format
- Temperature, Token Limits
- Personality Intensity Settings
- Cynefin Complexity Domain

### Viral Propagation
- Core Message and Viral Hooks
- Transmission Vectors
- Replication Strategy

### Compliance & Governance
- Security Level
- AI Act Risk Category
- Ethics and Oversight Requirements

## Usage

### Creating the Database

```bash
cd scripts
python create_database.py
```

This will:
1. Create a new database in your Notion workspace
2. Set up the complete schema based on the meta-template
3. Add the database ID to your `.env` file

### Setting Up Sample Prompts

```bash
python check_and_seed.py
```

This will:
1. Verify your database has the correct schema
2. Offer to set up the complete meta-template schema
3. Add sample prompts if the database is empty

### Using the CLI

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

## Creating a New Prompt

1. Copy one of the templates in the `templates/` directory
2. Modify it according to your needs
3. Save it with a new filename
4. Add it to the database:
   ```bash
   python prompt_cli.py create path/to/your-prompt.txt
   ```

## Environment Configuration

This system requires these environment variables:

```
PROMPT_SECURITY_TOKEN=your_notion_integration_token
PROMPT_DATABASE_ID=your_notion_database_id
```

## Best Practices

1. **Inheritance**: Use the Parent Prompt field to create inheritance chains
2. **Versioning**: Follow semantic versioning (MAJOR.MINOR.PATCH)
3. **Viral Hooks**: Focus on memorable phrases that trigger recognition
4. **Cynefin Domains**: Match your prompt's complexity level to its purpose
