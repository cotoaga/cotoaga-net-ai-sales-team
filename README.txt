cotoaga-net-ai-sales-team/
├── .env                     # Environment variables (NEVER commit this)
├── .gitignore              # Git ignore patterns
├── requirements.txt        # Python dependencies
├── config/
│   └── notion_schema.json  # Database schema definition
├── scripts/
│   ├── 0_setup_notion.py   # Initial setup & database creation
│   └── 1_test_connection.py # Connection testing
├── src/
│   ├── __init__.py
│   ├── notion_client.py    # Notion API wrapper
│   └── models.py           # Data models
└── README.md               # Setup instructions

---

# KHAOS Prompt Library Manager

A system for managing, versioning, and evolving AI prompts using Notion as a database backend.

## Features

- Create, read, update, and delete prompts in a Notion database
- Track prompt versions, types, and metadata
- Support for the KHAOS meta-prompt format
- CLI interface for easy management

## Setup

1. Clone this repository
2. Create a `.env` file with your Notion credentials:

```
NOTION_TOKEN=your_notion_integration_token
NOTION_PARENT_PAGE_ID=your_parent_page_id
```

3. Install dependencies:

```bash
pip install notion-client python-dotenv
```

4. Create your prompts database:

```bash
python create_prompts_db.py
```

5. Add the generated database ID to your `.env` file:

```
NOTION_PROMPTS_DB_ID=your_new_database_id
```

## Usage

### Creating a new prompt

1. Create a text file following the KHAOS prompt format:

```
# ═══════════════════════════════════════════════════════════════
# CORE IDENTIFICATION
# ═══════════════════════════════════════════════════════════════
PROMPT_ID: khaos-example-1.0.0
VERSION: 1.0.0
CREATION_DATE: 2025-05-20
LAST_MODIFIED: 2025-05-20
AUTHOR: Kurt Cotoaga, The Complexity Whisperer
PARENT_PROMPT: khaos-meta-template

# ═══════════════════════════════════════════════════════════════
# FUNCTIONAL ARCHITECTURE
# ═══════════════════════════════════════════════════════════════
PURPOSE: Example prompt for the README
...
```

2. Add the prompt to your library:

```bash
python khaos_cli.py create prompts/khaos-example.txt
```

### Managing prompts

List all prompts:
```bash
python khaos_cli.py list
```

Read a prompt:
```bash
python khaos_cli.py read khaos-example
```

Update a prompt:
```bash
python khaos_cli.py update khaos-example prompts/khaos-example-updated.txt
```

Delete a prompt:
```bash
python khaos_cli.py delete khaos-example
```

## Prompt Structure

The KHAOS prompt format includes these key sections:

- **Core Identification**: Basic metadata (ID, version, dates)
- **Functional Architecture**: Purpose and instructions
- **Orchestration Layer**: Dependencies and triggers
- **Execution Specifications**: Format and parameters
- **Learning & Adaptation**: Examples and failure modes
- **Viral Propagation**: Core messages and hooks
- **Compliance & Governance**: Security and ethical constraints
- **Ecosystem Integration**: Compatible models and metrics

## Directory Structure

```
/
├── .env                    # Environment variables
├── .gitignore              # Git ignore file
├── README.md               # This file
├── create_prompts_db.py    # Script to create the Notion database  
├── prompt_manager.py       # Core prompt management functionality
├── khaos_cli.py            # Command-line interface
└── prompts/                # Directory for prompt files
    ├── khaos-meta-template.txt
    └── khaos-coding-companion.txt
```

By the way, all of this was created by KHAOS itself - how's that for meta?