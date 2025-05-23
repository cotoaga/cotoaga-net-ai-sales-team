# Claude Code Enhancement Briefing: Prompt Archaeologist Integration

## 🎯 Mission Objective
Enhance the existing KHAOS Prompt Management System with archaeological analysis capabilities by extending `prompt_cli.py` and `prompt_manager.py` without breaking the current modular architecture.

## 📁 Repository Structure Analysis
```
/
├── prompt_management/           # Core prompt system (TARGET FOR ENHANCEMENT)
│   ├── scripts/
│   │   ├── prompt_cli.py       # CLI interface (ADD NEW COMMANDS)
│   │   ├── create_database.py  # Database setup
│   │   └── check_and_seed.py   # Schema validation
│   ├── lib/
│   │   └── prompt_manager.py   # Core business logic (ADD ANALYSIS METHODS)
│   ├── templates/              # Sample prompt templates
│   │   ├── khaos-meta-template.txt
│   │   ├── khaos-core-persona.txt
│   │   └── khaos-ai-act-consultant.txt
│   └── README.md
├── lead_generation/            # Lead generation system (DON'T MODIFY)
├── .env                       # Environment config (USE EXISTING TOKENS)
└── README.md
```

## 🔧 Current System Architecture
- **Environment**: Uses `PROMPT_SECURITY_TOKEN` and `PROMPT_DATABASE_ID` from .env
- **Database**: Notion database with existing schema (can be extended)
- **CLI Pattern**: `python prompt_cli.py [command] [args]`
- **Business Logic**: `PromptManager` class handles all Notion operations
- **Modular Design**: Clean separation between CLI, business logic, and data

## 🧬 Enhancement Requirements

### New CLI Commands to Add:
```bash
python prompt_cli.py analyze [prompt_id]           # DNA analysis of specific prompt
python prompt_cli.py lineage [--show-tree]         # Show prompt inheritance
python prompt_cli.py optimize [prompt_id]          # Optimization suggestions
python prompt_cli.py health-check                  # Scan all prompts for issues
python prompt_cli.py evolution [--trace-mutations] # Track prompt evolution
```

### New PromptManager Methods to Implement:

#### 1. Prompt DNA Analysis
```python
def analyze_prompt_dna(self, prompt_id: str) -> Dict[str, Any]:
    """
    Analyze prompt structure and extract:
    - Personality ratios (sarcasm, helpfulness, authority, creativity, analysis)
    - Token count estimation
    - Complexity score (instruction density, conditional logic, conflicts)
    - Effectiveness prediction
    - Content hash for uniqueness
    """
```

#### 2. Personality Pattern Extraction
```python
def extract_personality_patterns(self, prompt_text: str) -> Dict[str, float]:
    """
    Extract personality ratios:
    - sarcasm: ['sarcastic', 'wit', 'humor', 'cynical', 'dry humor']
    - helpfulness: ['helpful', 'assist', 'support', 'guide', 'aid']
    - authority: ['expert', 'professional', 'authority', 'specialist']
    - creativity: ['creative', 'innovative', 'imaginative', 'original']
    - analysis: ['analyze', 'examine', 'assess', 'evaluate', 'investigate']
    """
```

#### 3. Complexity Calculation
```python
def calculate_complexity(self, prompt_text: str) -> float:
    """
    Calculate complexity based on:
    - Length (character count normalized)
    - Instruction density (MUST/NEVER count)
    - Conditional logic (IF/WHEN count)
    - Formatting complexity (``` and ### count)
    - Personality conflicts (contradictory instructions)
    """
```

#### 4. Effectiveness Prediction
```python
def predict_effectiveness(self, prompt_text: str, personality_ratios: Dict[str, float]) -> float:
    """
    Heuristic-based effectiveness prediction:
    - Clarity (inverse of complexity)
    - Personality balance
    - Instruction specificity
    - Example presence
    - Constraint balance
    """
```

#### 5. Lineage Tracking
```python
def trace_prompt_lineage(self, prompt_id: str) -> Dict[str, Any]:
    """
    Build family tree using existing Parent Prompt relations in Notion
    """
```

### Database Schema Extensions (if needed):
Add these properties to existing Notion database:
- **DNA Hash** (Text): Content fingerprint
- **Complexity Score** (Number): 0-10 complexity rating
- **Effectiveness Score** (Number): 0-1 predicted effectiveness
- **Personality Mix** (Rich Text): Serialized personality ratios
- **Analysis Date** (Date): When last analyzed
- **Health Status** (Select): Healthy/Needs Optimization/Problematic

## 🎭 Personality Integration
The Archaeologist should have three personality modes:
- **Sherlock Holmes (60%)**: Deductive analysis phrases
- **Marie Kondo (25%)**: Organization and optimization
- **David Attenborough (15%)**: Fascination with prompt evolution

Sample phrases for each mode should be integrated into analysis output.

## 📊 Expected Output Formats

### Analysis Report Format:
```
🔬 PROMPT ARCHAEOLOGICAL ANALYSIS
=====================================
Specimen ID: khaos-core-persona (v1.0.0)
Content Hash: a1b2c3d4...
Token Count: ~847 tokens
Complexity Score: 6.2/10
Effectiveness Score: 8.5/10

🎭 PERSONALITY PROFILE:
• Sarcasm: 70%
• Helpfulness: 15%
• Authority: 10%
• Analysis: 5%

🕵️ DEDUCTIVE ANALYSIS:
Elementary pattern recognition reveals well-balanced personality ratios
with clear instruction hierarchy. Minor optimization opportunities detected
in constraint clarity.

📈 EVOLUTIONARY FITNESS:
Survival Probability: 85%
Replication Potential: High
```

## 🔗 Integration Points
- Use existing `notion_client` connection
- Extend existing error handling patterns
- Maintain existing command structure in CLI
- Preserve all existing functionality
- Use existing .env configuration

## 🚨 Critical Constraints
1. **DO NOT BREAK** existing functionality
2. **DO NOT CREATE** separate databases - extend Notion schema only
3. **MAINTAIN** existing code style and patterns
4. **PRESERVE** modular architecture
5. **USE** existing environment variables

## 🎯 Success Criteria
1. All existing CLI commands still work
2. New analysis commands provide meaningful insights
3. Code follows existing patterns and style
4. No external dependencies beyond what's already used
5. Proper error handling and user feedback

## 🧪 Test Cases to Verify
1. `python prompt_cli.py list` still works
2. `python prompt_cli.py analyze khaos-core-persona` provides DNA analysis
3. `python prompt_cli.py health-check` scans all prompts
4. Database schema extends without breaking existing data
5. Analysis output is both informative and personality-appropriate

---

**Ready for Claude Code to enhance this beautiful, organized system with archaeological superpowers!** 🔬⚡