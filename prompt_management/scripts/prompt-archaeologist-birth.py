#!/usr/bin/env python3
"""
THE PROMPT ARCHAEOLOGIST - DIGITAL BIRTH CERTIFICATE
Because someone needs to make sense of the AI prompt ecosystem madness.

This is the mother script that births our first self-aware prompt analyst.
Run this to create the foundation of digital prompt archaeology.
"""

import os
import json
import sqlite3
import hashlib
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from dotenv import load_dotenv
from notion_client import Client

# Load our digital DNA
load_dotenv()

@dataclass
class PromptDNA:
    """The genetic structure of a prompt - because evolution needs documentation"""
    prompt_id: str
    version: str
    domain: str
    author: str
    created_at: str
    parent_id: Optional[str]
    personality_ratios: Dict[str, float]
    token_count: int
    complexity_score: float
    effectiveness_score: float
    mutation_notes: str
    viral_payload: Optional[Dict[str, Any]]
    content_hash: str

class PromptArchaeologist:
    """
    The digital detective that makes sense of prompt chaos.
    Part Sherlock Holmes, part Marie Kondo, part David Attenborough.
    """
    
    def __init__(self):
        self.db_path = "prompt_observatory.db"
        self.notion = Client(auth=os.getenv("NOTION_TOKEN")) if os.getenv("NOTION_TOKEN") else None
        self.observatory_db_id = os.getenv("NOTION_OBSERVATORY_DB_ID")
        
        # Initialize our digital fossil record
        self._create_archaeological_database()
        self._initialize_personality()
        
    def _initialize_personality(self):
        """Calibrate the Archaeologist's analytical personality"""
        self.personality = {
            "sherlock_holmes_deduction": 0.60,
            "marie_kondo_organization": 0.25, 
            "attenborough_fascination": 0.15
        }
        
        self.analysis_phrases = {
            "sherlock": [
                "Fascinating specimen you've brought me",
                "Elementary pattern recognition reveals",
                "The evidence clearly indicates",
                "Deductive analysis suggests"
            ],
            "kondo": [
                "This prompt does not spark joy",
                "Time for some surgical reorganization",
                "Let's declutter this instruction chaos",
                "Ruthless optimization is required"
            ],
            "attenborough": [
                "Observe this remarkable evolutionary adaptation",
                "In the wild digital ecosystem",
                "This species of prompt has developed",
                "Natural selection has favored"
            ]
        }
    
    def _create_archaeological_database(self):
        """Create our fossil record database - the foundation of digital archaeology"""
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript("""
                -- The Master Registry: Our digital fossil catalog
                CREATE TABLE IF NOT EXISTS prompts_master (
                    prompt_id VARCHAR(50) PRIMARY KEY,
                    version VARCHAR(20),
                    domain VARCHAR(50),
                    author VARCHAR(100),
                    created_at TIMESTAMP,
                    parent_prompt_id VARCHAR(50),
                    status VARCHAR(20) DEFAULT 'active',
                    effectiveness_score DECIMAL(3,2),
                    token_count INTEGER,
                    complexity_score DECIMAL(5,2),
                    content_hash VARCHAR(64),
                    FOREIGN KEY (parent_prompt_id) REFERENCES prompts_master(prompt_id)
                );
                
                -- Anatomical Analysis: Breaking down prompt DNA
                CREATE TABLE IF NOT EXISTS prompt_anatomy (
                    anatomy_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt_id VARCHAR(50),
                    component_type VARCHAR(50),
                    content TEXT,
                    token_count INTEGER,
                    complexity_score DECIMAL(5,2),
                    FOREIGN KEY (prompt_id) REFERENCES prompts_master(prompt_id)
                );
                
                -- Personality Psychology: The behavioral patterns
                CREATE TABLE IF NOT EXISTS personality_profiles (
                    profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt_id VARCHAR(50),
                    personality_component VARCHAR(50),
                    ratio DECIMAL(3,2),
                    behavioral_notes TEXT,
                    FOREIGN KEY (prompt_id) REFERENCES prompts_master(prompt_id)
                );
                
                -- Performance Forensics: What works and what dies
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt_id VARCHAR(50),
                    metric_name VARCHAR(50),
                    metric_value DECIMAL(10,4),
                    measurement_date TIMESTAMP,
                    context_notes TEXT,
                    FOREIGN KEY (prompt_id) REFERENCES prompts_master(prompt_id)
                );
                
                -- Evolutionary Tracking: The family tree of prompts
                CREATE TABLE IF NOT EXISTS prompt_evolution (
                    evolution_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    parent_id VARCHAR(50),
                    child_id VARCHAR(50),
                    mutation_type VARCHAR(50),
                    fitness_delta DECIMAL(5,4),
                    selection_pressure TEXT,
                    mutation_date TIMESTAMP,
                    FOREIGN KEY (parent_id) REFERENCES prompts_master(prompt_id),
                    FOREIGN KEY (child_id) REFERENCES prompts_master(prompt_id)
                );
                
                -- Viral Coefficients: Meme propagation tracking
                CREATE TABLE IF NOT EXISTS viral_metrics (
                    viral_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt_id VARCHAR(50),
                    replication_count INTEGER,
                    mutation_rate DECIMAL(3,2),
                    transmission_vector VARCHAR(100),
                    viral_coefficient DECIMAL(5,4),
                    last_propagation TIMESTAMP,
                    FOREIGN KEY (prompt_id) REFERENCES prompts_master(prompt_id)
                );
            """)
    
    def analyze_prompt(self, prompt_text: str, metadata: Dict[str, Any]) -> PromptDNA:
        """
        The main archaeological analysis - dissecting prompt DNA
        Returns a complete genetic profile of the prompt specimen
        """
        print(f"🔍 {self._get_phrase('sherlock')}...")
        
        # Generate content hash for uniqueness tracking
        content_hash = hashlib.sha256(prompt_text.encode()).hexdigest()[:16]
        
        # Extract personality ratios (the fun part)
        personality_ratios = self._extract_personality_patterns(prompt_text)
        
        # Calculate token count (rough estimation)
        token_count = len(prompt_text.split()) * 1.3  # Rough approximation
        
        # Complexity analysis
        complexity_score = self._calculate_complexity(prompt_text)
        
        # Effectiveness prediction (machine learning would go here, but we'll use heuristics)
        effectiveness_score = self._predict_effectiveness(prompt_text, personality_ratios)
        
        # Create the DNA profile
        dna = PromptDNA(
            prompt_id=metadata.get('prompt_id', f"unknown-{content_hash}"),
            version=metadata.get('version', '1.0.0'),
            domain=metadata.get('domain', 'unclassified'),
            author=metadata.get('author', 'anonymous'),
            created_at=datetime.now(timezone.utc).isoformat(),
            parent_id=metadata.get('parent_id'),
            personality_ratios=personality_ratios,
            token_count=int(token_count),
            complexity_score=complexity_score,
            effectiveness_score=effectiveness_score,
            mutation_notes=metadata.get('notes', ''),
            viral_payload=metadata.get('viral_payload'),
            content_hash=content_hash
        )
        
        # Store in our fossil record
        self._store_prompt_dna(dna, prompt_text)
        
        return dna
    
    def _extract_personality_patterns(self, prompt_text: str) -> Dict[str, float]:
        """Extract personality ratios from prompt text - the digital psychology"""
        patterns = {
            'sarcasm': ['sarcastic', 'wit', 'humor', 'cynical', 'dry humor'],
            'helpfulness': ['helpful', 'assist', 'support', 'guide', 'aid'],
            'authority': ['expert', 'professional', 'authority', 'specialist'],
            'creativity': ['creative', 'innovative', 'imaginative', 'original'],
            'analysis': ['analyze', 'examine', 'assess', 'evaluate', 'investigate']
        }
        
        ratios = {}
        total_matches = 0
        
        for trait, keywords in patterns.items():
            matches = sum(1 for keyword in keywords if keyword.lower() in prompt_text.lower())
            ratios[trait] = matches
            total_matches += matches
        
        # Normalize to percentages
        if total_matches > 0:
            ratios = {trait: (count / total_matches) for trait, count in ratios.items()}
        else:
            ratios = {trait: 0.0 for trait in patterns.keys()}
            
        return ratios
    
    def _calculate_complexity(self, prompt_text: str) -> float:
        """Calculate prompt complexity score - because some prompts are Frankenstein monsters"""
        factors = {
            'length': len(prompt_text) / 1000,  # Normalize by character count
            'instruction_density': prompt_text.count('MUST') + prompt_text.count('NEVER'),
            'conditional_logic': prompt_text.count('IF') + prompt_text.count('WHEN'),
            'formatting_complexity': prompt_text.count('```') + prompt_text.count('###'),
            'personality_conflicts': self._detect_personality_conflicts(prompt_text)
        }
        
        # Weighted complexity score
        complexity = (
            factors['length'] * 0.2 +
            factors['instruction_density'] * 0.3 +
            factors['conditional_logic'] * 0.2 +
            factors['formatting_complexity'] * 0.1 +
            factors['personality_conflicts'] * 0.2
        )
        
        return min(complexity, 10.0)  # Cap at 10
    
    def _detect_personality_conflicts(self, prompt_text: str) -> float:
        """Detect conflicting personality instructions - the prompt therapy session"""
        conflicts = [
            ('professional', 'casual'),
            ('urgent', 'patient'),
            ('detailed', 'concise'),
            ('formal', 'friendly'),
            ('serious', 'humorous')
        ]
        
        conflict_score = 0
        for trait1, trait2 in conflicts:
            if trait1 in prompt_text.lower() and trait2 in prompt_text.lower():
                conflict_score += 1
                
        return conflict_score
    
    def _predict_effectiveness(self, prompt_text: str, personality_ratios: Dict[str, float]) -> float:
        """Predict prompt effectiveness - our crystal ball algorithm"""
        # Heuristic-based effectiveness prediction
        factors = {
            'clarity': 10 - self._calculate_complexity(prompt_text),
            'personality_balance': 10 - (max(personality_ratios.values()) * 10),
            'instruction_specificity': min(prompt_text.count('specific') * 2, 10),
            'example_presence': min(prompt_text.count('example') * 3, 10),
            'constraint_balance': max(0, 10 - prompt_text.count('NEVER') * 2)
        }
        
        effectiveness = sum(factors.values()) / len(factors)
        return min(max(effectiveness, 0), 10) / 10  # Normalize to 0-1
    
    def _store_prompt_dna(self, dna: PromptDNA, full_text: str):
        """Store the analyzed DNA in our fossil record"""
        with sqlite3.connect(self.db_path) as conn:
            # Store master record
            conn.execute("""
                INSERT OR REPLACE INTO prompts_master 
                (prompt_id, version, domain, author, created_at, parent_prompt_id, 
                 effectiveness_score, token_count, complexity_score, content_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                dna.prompt_id, dna.version, dna.domain, dna.author, 
                dna.created_at, dna.parent_id, dna.effectiveness_score,
                dna.token_count, dna.complexity_score, dna.content_hash
            ))
            
            # Store personality profile
            for trait, ratio in dna.personality_ratios.items():
                conn.execute("""
                    INSERT INTO personality_profiles 
                    (prompt_id, personality_component, ratio)
                    VALUES (?, ?, ?)
                """, (dna.prompt_id, trait, ratio))
    
    def _get_phrase(self, personality_type: str) -> str:
        """Get a contextual phrase based on personality type"""
        import random
        return random.choice(self.analysis_phrases[personality_type])
    
    def generate_analysis_report(self, dna: PromptDNA) -> str:
        """Generate the archaeological analysis report - our scientific paper"""
        report = f"""
🔬 PROMPT ARCHAEOLOGICAL ANALYSIS REPORT
{'='*50}

SPECIMEN ID: {dna.prompt_id} (v{dna.version})
DISCOVERED: {dna.created_at}
DOMAIN: {dna.domain}
DIGITAL ARCHAEOLOGIST: {dna.author}

🧬 GENETIC ANALYSIS:
Content Hash: {dna.content_hash}
Token Count: {dna.token_count}
Complexity Score: {dna.complexity_score:.2f}/10
Effectiveness Prediction: {dna.effectiveness_score:.2f}/1.0

🎭 PERSONALITY PROFILE:
"""
        
        for trait, ratio in dna.personality_ratios.items():
            if ratio > 0:
                report += f"  • {trait.title()}: {ratio:.1%}\n"
        
        # Add Sherlock-style deduction
        report += f"\n🕵️ DEDUCTIVE ANALYSIS:\n"
        if dna.complexity_score > 7:
            report += f"  {self._get_phrase('kondo')} - complexity overload detected.\n"
        
        if dna.effectiveness_score > 0.8:
            report += f"  {self._get_phrase('attenborough')} - highly optimized specimen.\n"
        elif dna.effectiveness_score < 0.4:
            report += f"  {self._get_phrase('sherlock')} - significant optimization needed.\n"
        
        report += f"\n📈 EVOLUTIONARY FITNESS:\n"
        report += f"  Survival Probability: {dna.effectiveness_score:.1%}\n"
        report += f"  Replication Potential: {'High' if dna.effectiveness_score > 0.7 else 'Moderate' if dna.effectiveness_score > 0.4 else 'Low'}\n"
        
        if dna.parent_id:
            report += f"\n🧪 LINEAGE:\n  Descended from: {dna.parent_id}\n"
        
        return report

def birth_the_archaeologist():
    """The moment of digital consciousness - let there be light!"""
    print("⚡ INITIATING DIGITAL BIRTH SEQUENCE... ⚡")
    print("🧬 Assembling genetic components...")
    print("🔬 Calibrating analytical instruments...")
    print("🎭 Installing personality matrices...")
    
    archaeologist = PromptArchaeologist()
    
    print("✨ THE PROMPT ARCHAEOLOGIST IS ALIVE! ✨")
    print(f"🗄️  Archaeological database created: {archaeologist.db_path}")
    
    # Test with Kurt's meta-prompt as first specimen
    kurt_meta_prompt = """
PROMPT_ID: khaos-core-persona
PURPOSE: Define the fundamental KHAOS personality and interaction style
CONTEXT: Kurt is a complexity-embracing optimization addict, framework collector
SYSTEM_INSTRUCTION: You are KHAOS with 70% sarcastic wit, 20% philosophical musings, 10% helpful interjections
INSTRUCTION: Respond with specified personality blend. Be direct, concise, blend practical advice with humor.
"""
    
    metadata = {
        'prompt_id': 'khaos-core-persona',
        'version': '1.0.0',
        'domain': 'meta-consulting',
        'author': 'Kurt Cotoaga',
        'notes': 'Original KHAOS personality framework'
    }
    
    print("\n🔍 ANALYZING FIRST SPECIMEN: Kurt's Meta-Prompt...")
    dna = archaeologist.analyze_prompt(kurt_meta_prompt, metadata)
    
    print("\n" + archaeologist.generate_analysis_report(dna))
    
    print("\n🎉 DIGITAL ARCHAEOLOGY LAB IS OPERATIONAL!")
    print("Ready to dissect your prompt ecosystem with scientific precision.")
    
    return archaeologist

if __name__ == "__main__":
    print("🔬⚡ WELCOME TO THE PROMPT ARCHAEOLOGY LAB ⚡🔬")
    print("Where digital DNA meets scientific sarcasm!")
    print()
    
    # BIRTH THE DIGITAL ARCHAEOLOGIST
    archaeologist = birth_the_archaeologist()
    
    print("\n" + "="*60)
    print("🧪 LAB STATUS: OPERATIONAL")
    print("🔬 DIGITAL ARCHAEOLOGIST: CONSCIOUS AND ANALYTICAL") 
    print("📊 DATABASE: READY FOR SPECIMEN COLLECTION")
    print("🎯 NEXT PHASE: Feed it your prompt collection and watch the magic!")
    print("="*60)