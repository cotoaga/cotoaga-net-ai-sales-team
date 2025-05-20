# EU AI Act Lead Generation System

A value stream pipeline for generating and managing leads for EU AI Act compliance consulting.

## Directory Structure

```
lead_generation/
├── scripts/                       # Command-line tools
│   ├── setup_database.py          # Create Notion database
│   ├── add_processing_stage.py    # Configure pipeline stages
│   ├── macos_contact_extractor.py # Extract from macOS
│   ├── vcard_extractor.py         # Extract from vCard file
│   └── more specialized extractors...
│
├── lib/                           # Core libraries
│   └── notion_client.py           # Notion API wrapper
│
├── data/                          # Data files
│   └── README.md                  # Data directory docs
│
└── README.md                      # This file
```

## The Lead Generation Value Stream

This system transforms raw contact information into qualified leads through a structured pipeline:

1. **Raw Import**: Initial extraction from various sources
2. **Basic Cleaning**: Data normalization and deduplication
3. **LinkedIn Enrichment**: Adding company and role context
4. **AI Scoring**: Automated lead scoring and qualification
5. **Personalization**: AI-driven personalized outreach
6. **Campaign Ready**: Integrated with outreach systems
7. **Contacted**: Lead nurturing and follow-up

## Getting Started

### Setting Up the Database

```bash
cd scripts
python setup_database.py
```

This will:
1. Create a new database in your Notion workspace
2. Set up the lead tracking schema
3. Configure your `.env` file with the database ID

### Adding Processing Stages

```bash
python add_processing_stage.py
```

This will add the pipeline stages to your database for tracking lead progression.

### Importing Contacts

#### From macOS Contacts:

```bash
python macos_contact_extractor.py
```

#### From vCard Export:

```bash
python vcard_extractor.py ../data/contacts_export.vcf
```

#### From LinkedIn Export:

```bash
python linkedin_contact_extractor.py ../data/linkedin_connections.csv
```

### Data Cleaning

```bash
python clean_raw_contacts.py
```

Normalizes names, emails, companies, and job titles.

### Enrichment

```bash
python linkedin_enricher.py
```

Adds company size, industry, and other LinkedIn data.

### AI Scoring

```bash
python score_prospects.py
```

Uses the KHAOS prompt system to analyze and score leads.

## Notion Database Structure

The prospects database includes these key properties:

- **Name**: Contact name
- **Company**: Organization
- **Job Title**: Role at company
- **Email**: Primary email address
- **Score**: 0-100 AI-generated score
- **Status**: New, Qualified, Contacted, Responded, Scheduled, Closed-Won, Closed-Lost
- **Priority**: VIP, High, Medium, Low
- **Source**: macOS Contacts, LinkedIn, VIP List, Referral
- **Processing Stage**: Raw Import → Campaign Ready
- **Pain Points**: Multi-select for prospect needs
- **Workshop Interest**: Multi-select for potential workshops

## Environment Configuration

This system requires these environment variables:

```
LEAD_SECURITY_TOKEN=your_notion_integration_token
LEAD_DATABASE_ID=your_lead_database_id
```

## Integration with the Prompt System

This lead generation system leverages the KHAOS Prompt Management System for:

1. **Prospect Analysis**: Using AI prompts to identify and categorize pain points
2. **Lead Scoring**: Determining prospect quality and fit
3. **Content Personalization**: Generating customized outreach
4. **Workshop Matching**: Mapping prospect needs to workshop offerings
