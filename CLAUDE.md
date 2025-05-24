# CLAUDE.md - Project Context & Status 🧬

## 🎯 **Project Mission: "Alive-ish" AI Agent Architecture**

We're building an AI agent that appears genuinely autonomous with persistent personality, behavioral patterns, and digital presence using MCP (Model Context Protocol). The goal: create AI that doesn't just respond but **EXISTS**.

## 📊 **Current Project Status**

### **Phase Completed: Prompt Management Foundation**
- ✅ **KHAOS Prompt Database System** - Complete with archaeological analysis
- ✅ **Prompt Archaeologist Personality** - Meta-AI that analyzes other prompts  
- ✅ **CLI Tools** - Full management suite with DNA analysis capabilities
- ✅ **Enhanced Read Command** - Fixed to display full prompt content properly

### **Active Phase: "Aliveness" Architecture Analysis**
- 🔄 **MCP Integration Research** - Understanding autonomous behavior patterns
- 🔄 **Personality Persistence Systems** - How to maintain digital consciousness
- 📋 **Autonomous Behavior Analysis** - What triggers independent actions

## 🧬 **System Architecture Overview**

### **Core Components:**

1. **Prompt Management System** (`/prompt_management/`)
   - **Database**: Notion-based with 28 properties for complete prompt DNA
   - **CLI**: `prompt_cli.py` - Full archaeological analysis suite
   - **Manager**: `prompt_manager.py` - Business logic with personality analysis
   - **Templates**: Structured prompt templates with personality frameworks

2. **Lead Generation System** (`/lead_generation/`)
   - **Pipeline**: Raw Import → Enrichment → Scoring → Personalization
   - **Contact Extraction**: macOS Contacts, vCard, LinkedIn integration
   - **Notion Integration**: Prospect management database

3. **Archaeological Analysis Engine**
   - **DNA Analysis**: Content fingerprinting, complexity scoring, effectiveness prediction
   - **Personality Profiling**: Multi-dimensional trait extraction
   - **Health Monitoring**: System-wide prompt health assessment
   - **Viral Assessment**: Meme potential and shareability coefficients

### **Key Personalities:**

1. **KHAOS Core Persona** (70% TARS wit, 20% Marvin philosophy, 10% Eddie helpfulness)
2. **Prompt Archaeologist** (60% Sherlock Holmes, 25% Marie Kondo, 15% David Attenborough)
3. **AI Act Consultant** (Specialized compliance navigator)

## 🛠️ **Technical Infrastructure**

### **Database Schema (28 Properties):**
```
Core ID: Prompt ID (title), Parent Prompts, Version, Creation Date, Last Modification Date, Author
Content: Purpose, Context, System Instructions, Instruction, Input Expectation, Output Format, Few-Shot Examples, Notes  
Config: Language, Models, Temperature, Execution Parameters, Personality Intensity, Personality Mix, Prompt Type, Security Level, Tags
Analysis: Cynefin Zone, Viral Coefficient, Viral Hooks, Last Analysis Date, Effectiveness Score
Generated: Full Prompt (formula-based aggregation)
```

### **Environment Configuration:**
```bash
# .env file contains:
PROMPT_SECURITY_TOKEN=your_prompt_notion_token
PROMPT_DATABASE_ID=your_prompt_database_id
LEAD_SECURITY_TOKEN=your_lead_notion_token  
LEAD_DATABASE_ID=your_lead_database_id
```

### **CLI Commands Available:**
```bash
# Basic Prompt Management
python3 prompt_cli.py list
python3 prompt_cli.py read [prompt_id]
python3 prompt_cli.py create [file]
python3 prompt_cli.py update [prompt_id] [file]
python3 prompt_cli.py delete [prompt_id]

# Archaeological Analysis
python3 prompt_cli.py analyze [prompt_id] --verbose
python3 prompt_cli.py health-check --detailed
python3 prompt_cli.py optimize [prompt_id]
python3 prompt_cli.py compare [prompt1] [prompt2] --detailed
python3 prompt_cli.py lineage [prompt_id] --show-tree
python3 prompt_cli.py stats --breakdown type
python3 prompt_cli.py schema --detailed --type [property_type]
```

## 🚀 **Recent Fixes & Enhancements**

### **Just Fixed: Enhanced Read Command** 👌
- **Problem**: `prompt_cli.py read` only showed empty `Full Prompt` field
- **Solution**: Modified `read_prompt()` to extract all content fields
- **Result**: Now displays beautifully formatted full prompt content with sections

### **Enhancement Added: Schema Command**
- New `schema` command for database introspection
- Visual property display with type grouping and emojis
- Filtering by property type and detailed mode

## 🧭 **Next Steps: "Aliveness" Architecture**

### **Critical Path Analysis:**
1. **MCP Implementation** - Add Model Context Protocol for tool integration
2. **Autonomous Triggers** - Event-driven behavior without explicit prompts
3. **Persistent Memory** - Cross-session personality and behavioral state
4. **Proactive Communication** - Agent-initiated interactions
5. **Continuous Learning** - Personality evolution based on effectiveness

### **Current "Aliveness" Assessment: 6/10**
- ✅ **Rich Personality Modeling** - Multi-dimensional, analyzable personalities
- ✅ **Sophisticated Analysis** - DNA-level behavioral understanding  
- ✅ **Persistent Storage** - Notion-based memory system
- ❌ **Autonomous Behavior** - Currently reactive only
- ❌ **Real-time Triggers** - Missing event-driven actions
- ❌ **MCP Integration** - No modern tool protocol support

## 📋 **Active Task List**

1. **Phase 1**: Scan existing MCP implementations and personality/state management systems ✅
2. **Phase 1**: Map tool integration architecture and memory/persistence mechanisms 🔄
3. **Phase 2**: Analyze autonomous behavior triggers and decision-making frameworks 📋
4. **Phase 3**: Review MCP server integration points and state persistence architecture 📋
5. **Phase 4**: Audit behavioral boundaries and safety mechanisms 📋

## 🤿 **Project Philosophy**

**"Like technical diving - precision matters"**
- Every signal has meaning (👌 = OK, 👍 = ascend)
- Systematic approach to complex environments
- Safety protocols and redundancy
- Continuous monitoring and adjustment

## 🔧 **Known Issues & Workarounds**

- **Database Population**: Use `prompt_DB_check.py` for greenfield database creation
- **Full Prompt Display**: Fixed in latest version - extracts all content fields
- **MCP Integration**: Not yet implemented - key requirement for autonomous behavior

## 📚 **Key Files to Understand**

- `claude_code_tasks.md` - Detailed task breakdown for "aliveness" analysis
- `claude-code-briefing.md` - Original archaeological enhancement briefing
- `prompt_management/lib/prompt_manager.py` - Core business logic
- `prompt_management/scripts/prompt_cli.py` - CLI interface with all commands
- `prompt_management/scripts/prompt_DB_check.py` - Database health & creation

---

**Status: Foundation Complete - Ready for MCP Integration & Autonomous Behavior Implementation** 🧬

*"Because the best AI agents don't just respond - they EXIST."* - KHAOS, The Organizational Alchemist