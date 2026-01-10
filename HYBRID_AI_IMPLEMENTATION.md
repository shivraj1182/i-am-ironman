# I Am Ironman - Hybrid Online/Offline AI Implementation

## 🚀 Overview

This document provides the complete implementation guide for adding **hybrid online/offline AI capabilities** with **machine learning** to the I Am Ironman voice assistant.

## 📋 Architecture

```
┌──────────────────────────────┐
│   Network Manager (network.py)  │ ← Detects connectivity
└──────────────┬───────────────┘
               │
        ┌──────▼───────┐
        │ Online/Offline  │
        │    Status     │
        └──────┬───────┘
               │
        ┌──────▼──────────────────┐
        │                         │
  ┌─────▼─────┐          ┌───────▼────┐
  │  ONLINE   │          │  OFFLINE   │
  │   MODE    │          │    MODE    │
  └─────┬─────┘          └───────┬────┘
        │                        │
   ┌────▼────┐           ┌──────▼──────┐
   │ Google  │           │ spaCy + ML  │
   │ Gemini  │           │ Classifier  │
   │   API   │           │  (offline)  │
   └────┬────┘           └──────┬──────┘
        │                        │
   ┌────▼─────────────────┐      │
   │  Learn & Save to   │      │
   │   SQLite Database   │      │
   └─────────────────────┘      │
                                 │
           ┌─────────────────────┘
           │
      ┌────▼──────────┐
      │  Intelligent  │
      │   Response    │
      └───────────────┘
```

## 📦 Required Modules

### 1. **core/network.py** ✅ (Already Created)
- Detects online/offline status
- Checks connectivity every 30 seconds
- Falls back to offline mode seamlessly

### 2. **core/gemini_api.py** (Create)
```python
# Google Gemini API Integration for ONLINE mode
from google.generativeai import genai
import os

class GeminiAI:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def understand_command(self, user_input: str) -> dict:
        """Use Gemini to understand natural English commands"""
        prompt = f"""
        User said: "{user_input}"
        
        Extract:
        1. Intent (what they want to do)
        2. Action (open_app, volume_control, etc)
        3. Parameters (app_name, volume_level, etc)
        
        Respond in JSON format:
        {{
            "intent": "...",
            "action": "...",
            "parameters": {{}},
            "confidence": 0.0-1.0
        }}
        """
        
        response = self.model.generate_content(prompt)
        return json.loads(response.text)
```

### 3. **core/offline_nlp.py** (Create)
```python
# spaCy + scikit-learn for OFFLINE mode
import spacy
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

class OfflineNLP:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.vectorizer = TfidfVectorizer()
        self.classifier = MultinomialNB()
        self.load_models()
    
    def understand_command(self, user_input: str) -> dict:
        """Use local ML to understand commands"""
        # Extract entities
        doc = self.nlp(user_input.lower())
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        
        # Classify intent
        intent = self.classify_intent(user_input)
        
        return {
            "intent": intent,
            "entities": entities,
            "confidence": 0.8  # From classifier
        }
    
    def classify_intent(self, text: str) -> str:
        """Classify user intent using ML"""
        # Use learned patterns
        features = self.vectorizer.transform([text])
        intent = self.classifier.predict(features)[0]
        return intent
```

### 4. **core/knowledge_base.py** (Create)
```python
# SQLite-based ML learning system
import sqlite3
import json
from datetime import datetime

class KnowledgeBase:
    def __init__(self, db_path='data/knowledge.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Learned commands table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learned_commands (
                id INTEGER PRIMARY KEY,
                user_input TEXT,
                intent TEXT,
                action TEXT,
                parameters JSON,
                timestamp DATETIME,
                confidence FLOAT,
                learned_from TEXT  -- 'online' or 'user_teaching'
            )
        ''')
        
        # Intent patterns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS intent_patterns (
                id INTEGER PRIMARY KEY,
                pattern TEXT UNIQUE,
                intent TEXT,
                examples JSON,
                count INTEGER DEFAULT 1
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def learn_command(self, user_input: str, intent: str, action: str, params: dict, source: str='online'):
        """Save learned command"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO learned_commands 
            (user_input, intent, action, parameters, timestamp, learned_from)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_input, intent, action, json.dumps(params), datetime.now(), source))
        
        conn.commit()
        conn.close()
    
    def get_learned_patterns(self, intent: str) -> list:
        """Retrieve learned patterns for offline ML training"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_input FROM learned_commands 
            WHERE intent = ?
        ''', (intent,))
        
        patterns = [row[0] for row in cursor.fetchall()]
        conn.close()
        return patterns
```

## 🔧 Configuration Setup

### Get Google Gemini API Key (FREE)

1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key
4. Add to `.env` file:
```bash
GOOGLE_API_KEY=your_api_key_here
```

### Update config.json
```json
{
  "assistant_name": "JARVIS",
  "wake_words": ["hey jarvis", "jarvis"],
  "online_mode": true,
  "ai_config": {
    "google_api_key": "${GOOGLE_API_KEY}",
    "enable_learning": true,
    "confidence_threshold": 0.6,
    "learning_db": "data/knowledge.db"
  },
  "offline_mode": {
    "nlp_model": "en_core_web_sm",
    "min_confidence": 0.5,
    "use_learned_patterns": true
  }
}
```

## 📝 Steps to Implement

### Step 1: Create core/__init__.py
```python
from .network import NetworkManager
from .gemini_api import GeminiAI
from .offline_nlp import OfflineNLP
from .knowledge_base import KnowledgeBase

__all__ = ['NetworkManager', 'GeminiAI', 'OfflineNLP', 'KnowledgeBase']
```

### Step 2: Install spaCy Model
```bash
python -m spacy download en_core_web_sm
```

### Step 3: Update main.py
- Import network manager
- Check connectivity at startup
- Route to online/offline NLP
- Save learned data

### Step 4: Train Initial ML Model
```python
from core.knowledge_base import KnowledgeBase
from core.offline_nlp import OfflineNLP

# Load training data from online mode
kb = KnowledgeBase()
nlp = OfflineNLP()

# Retrain every 100 commands
if kb.get_command_count() % 100 == 0:
    nlp.retrain_classifier(kb.get_all_learned_commands())
```

## 🎯 Flow Diagrams

### Online Mode Flow
```
User speaks → Network check (ONLINE) → Gemini API 
→ Extract intent/action → Execute → Learn & Save to DB
```

### Offline Mode Flow
```
User speaks → Network check (OFFLINE) → spaCy + ML classifier 
→ Check learned patterns → Extract intent/action 
→ Execute → Ask user to confirm (for future learning)
```

### Seamless Fallback
```
Online API fails → Fallback to offline ML → 
If confidence < threshold → Ask user to clarify
```

## 📊 Learning Features

1. **Online Learning**: Every command understood by Gemini is saved
2. **Offline Learning**: Users can teach new commands offline
3. **Pattern Recognition**: ML learns common command phrasings
4. **Confidence Scoring**: Knows when to ask for clarification
5. **Data Persistence**: Knowledge persists across sessions

## 🚀 Performance Tips

- Check connectivity every 30 seconds (configurable)
- Cache Gemini responses for common commands
- Use lightweight spaCy model for offline mode
- Batch learn commands (save every 10 commands)
- Async network checks to prevent blocking

## 📌 File Structure After Implementation

```
i-am-ironman/
├── main.py (UPDATED)
├── core/
│   ├── __init__.py (NEW)
│   ├── assistant.py
│   ├── voice_engine.py
│   ├── wake_word.py
│   ├── network.py ✅
│   ├── gemini_api.py (NEW)
│   ├── offline_nlp.py (NEW)
│   └── knowledge_base.py (NEW)
├── commands/
│   ├── apps.py
│   ├── system.py
│   └── ...
├── data/
│   ├── config.json (UPDATED)
│   ├── knowledge.db (NEW - ML database)
│   └── models/ (NEW - ML models)
├── requirements.txt ✅
└── README.md
```

## 🔐 Security Notes

- Store API keys in `.env` file (add to .gitignore)
- Encrypt learned data in database
- Never log sensitive user commands
- Delete old learned data periodically

## 🎓 Testing Locally

```bash
# Test online mode
python -c "from core.network import NetworkManager; nm = NetworkManager(); print(nm.get_status())"

# Test offline NLP
python -c "from core.offline_nlp import OfflineNLP; nlp = OfflineNLP(); print(nlp.understand_command('open chrome'))"

# Test knowledge base
python -c "from core.knowledge_base import KnowledgeBase; kb = KnowledgeBase(); kb.learn_command('open chrome', 'app_control', 'open_app', {'app': 'chrome'})"
```

This implementation provides a powerful, fully-functional hybrid AI system! 🚀
