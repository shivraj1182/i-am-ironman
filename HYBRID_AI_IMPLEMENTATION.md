# I Am Ironman - Hybrid Online/Offline AI Implementation

## Overview

This document provides the complete implementation guide for adding hybrid online/offline AI capabilities with machine learning to the I Am Ironman voice assistant. The system intelligently switches between local processing and cloud-based AI based on network availability and context.

## Architecture

```
Network Manager (network.py) - Detects connectivity
        |
        v
Online/Offline Status Check
        |
    /---+---\
    |       |
    v       v
ONLINE   OFFLINE
MODE     MODE
    |       |
    v       v
  Google   spaCy + ML
  Gemini   Classifier
  API      (offline)
    |       |
    +---+---+
        v
Response Synthesis
```

## Features

### Online Mode (With API Key)

- Google Gemini AI for advanced NLP
- Real-time contextual understanding
- Complex command processing
- Requires secure API key management

### Offline Mode (No Internet Required)

- spaCy for Named Entity Recognition
- scikit-learn for intent classification
- Local ML models for command processing
- Zero cloud dependency
- Full privacy preservation

### Network Awareness

- Automatic online/offline detection
- Seamless fallback mechanisms
- Connection state monitoring
- Graceful degradation

## Implementation Components

### 1. Network Manager (network.py)

```python
from network_connectivity import check_internet

def is_online():
    return check_internet()
```

Detects network connectivity and manages online/offline transitions.

### 2. API Key Management (secure_api_manager.py)

- Fernet symmetric encryption for API keys
- First-run setup wizard
- Encrypted local storage
- Secure credential handling
- File permission restrictions (0o600)

```python
from secure_api_manager import SecureAPIManager

manager = SecureAPIManager()
api_key = manager.get_api_key()
```

### 3. Online AI Handler (gemini_handler.py)

Processes commands using Google Gemini API when online:

```python
import google.generativeai as genai

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content(command)
```

### 4. Offline AI Handler (offline_processor.py)

Processes commands using local ML models when offline:

```python
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

# Load pre-trained offline model
offline_model = load_model('data/offline_model.pkl')
intent = offline_model.predict([command])
```

### 5. Hybrid Orchestrator (hybrid_manager.py)

Manages switching between online and offline modes:

```python
if is_online():
    response = process_with_gemini(command, api_key)
else:
    response = process_offline(command)
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- Internet connection (for initial setup)
- spaCy language model
- scikit-learn trained models
- Google Gemini API key (optional but recommended)

### Installation

1. Install NLP dependencies:

```bash
pip install spacy scikit-learn google-generativeai
python -m spacy download en_core_web_sm
```

2. Download offline ML models:

```bash
python scripts/download_models.py
```

3. Set up API key securely:

```python
from secure_api_manager import setup_api_key
manager = setup_api_key()  # Interactive setup
```

## API Key Security

### Encryption Method

Fernet symmetric encryption (industry standard):
- 256-bit AES encryption
- HMAC for authentication
- Automatic master key generation
- File permissions: 0o600 (owner read/write only)

### Storage Locations

- Master key: `data/.master_key` (git-ignored)
- Encrypted API key: `data/api_key.encrypted` (git-ignored)
- Metadata: `data/google_meta.json` (git-ignored)

### First-Run Setup

User is prompted during startup:

```
"Would you like to add an API key now? (y/n):"
```

If yes:
- Prompts for Google API key (input hidden with getpass)
- Encrypts and stores locally
- Saves metadata (creation date, key length)
- Confirms successful storage

## Usage Examples

### Online Command (with internet)

```
User: "What's the weather in London?"
System: Detects online mode, sends to Gemini API
Response: "The weather in London is..."
```

### Offline Command (no internet)

```
User: "Open Chrome"
System: Detects offline mode, uses local classifier
Response: "Opening Chrome"
```

### Hybrid Fallback

```
User: "Tell me about quantum computing"
System: Tries Gemini API
Result: Network timeout
Fallback: Uses offline processor
Response: "Based on local knowledge..."
```

## Performance Metrics

### Online Processing

- Average latency: 1-3 seconds
- Accuracy: 95%+ with Gemini
- Requires internet: Yes
- Cost: Google API pricing

### Offline Processing

- Average latency: <1 second
- Accuracy: 85-90% with ML models
- Requires internet: No
- Cost: Zero

## Training Custom Models

### Data Format

```csv
command,intent,action
"open chrome",app_launch,launch_app
"increase volume",volume_control,increase_volume
"lock screen",system_control,lock
```

### Training Pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('classifier', MultinomialNB())
])

pipeline.fit(X_train, y_train)
accuracy = pipeline.score(X_test, y_test)
```

## Fallback Strategy

1. Primary: Online mode with Gemini API
2. Secondary: Offline local ML models
3. Tertiary: Basic keyword matching
4. Final: User confirmation prompt

## Troubleshooting

### API Key Issues

- Key not found: Run setup_api_key() again
- Decryption failed: Check master key file permissions
- API errors: Verify key validity in Google AI Studio

### Network Detection Issues

- Always shows offline: Check network connectivity
- Doesn't switch: Verify network_connectivity import
- Timeout errors: Increase timeout values

### ML Model Issues

- Low accuracy: Retrain with more data
- Missing models: Run download_models.py
- Import errors: Install scikit-learn and spaCy

## Future Enhancements

- [ ] Custom neural networks for wake word detection
- [ ] Fine-tuned models for domain-specific tasks
- [ ] Multi-language support
- [ ] Caching for frequent queries
- [ ] Sentiment analysis integration
- [ ] Context persistence across sessions
- [ ] Advanced NER (Named Entity Recognition)
- [ ] Dialogue management system

## Security Considerations

- Never commit API keys to version control
- Use .gitignore for sensitive files
- Rotate API keys periodically
- Use environment variables in production
- Keep encryption dependencies updated
- Monitor API usage for unauthorized access

## Testing

### Unit Tests

```bash
python -m pytest tests/test_api_manager.py
python -m pytest tests/test_network.py
python -m pytest tests/test_offline_processor.py
```

### Integration Tests

```bash
python -m pytest tests/test_hybrid_integration.py
```

## References

- Google Generative AI: https://ai.google.dev/
- spaCy NLP: https://spacy.io/
- scikit-learn: https://scikit-learn.org/
- Fernet Encryption: https://cryptography.io/

## License

MIT License - Free to use and modify

## Support

For issues or questions:
- Open an issue on GitHub
- Check the main README
- Review code comments and documentation
