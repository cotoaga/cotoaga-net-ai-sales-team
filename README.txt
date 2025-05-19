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