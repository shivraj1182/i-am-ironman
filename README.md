# I Am Ironman 🤖

A fully **local**, offline-first voice assistant for your PC inspired by JARVIS from Iron Man.

## Features

### 🎤 Voice Recognition
- Wake word detection with personalized assistant name
- Offline speech recognition (using Vosk or SpeechRecognition)
- Continuous listening with minimal CPU usage

### 🤖 System Control
- **Launch Applications** - Open Chrome, VS Code, Notepad, Discord, etc.
- **Volume Control** - Increase/decrease/mute volume
- **Brightness Control** - Adjust screen brightness
- **Window Management** - Minimize, maximize, close windows
- **System Fixes** - Clear cache, free up RAM, clean temp files
- **Quick Settings** - Toggle WiFi, Bluetooth, Dark Mode

### 🧠 Smart Features
- Personalization - Remember your assistant's name
- Context awareness - Understand various command phrasings
- Local operation - Everything runs on your machine (no cloud)
- Persistent memory - Store preferences and settings

### 🔊 Voice Feedback
- Offline text-to-speech using pyttsx3
- Natural responses to commands
- Audio confirmation for actions

## Project Structure

```
i-am-ironman/
├── main.py                 # Entry point & main loop
├── config.py              # Configuration & settings
├── requirements.txt        # Python dependencies
├── README.md              # This file
│
├── core/
│   ├── __init__.py
│   ├── assistant.py       # Main assistant logic
│   ├── voice_engine.py    # Speech recognition & TTS
│   └── wake_word.py       # Wake word detection
│
├── commands/
│   ├── __init__.py
│   ├── apps.py           # Application launcher
│   ├── system.py         # System controls (volume, brightness)
│   ├── maintenance.py    # System maintenance
│   └── utils.py          # Utility commands
│
└── data/
    ├── config.json       # Stored configuration
    └── commands.json     # Custom command mappings
```

## Installation

### Prerequisites
- Python 3.8 or higher
- Windows 10/11, macOS, or Linux
- Microphone for voice input
- Speaker for audio output

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/shivraj1182/i-am-ironman.git
   cd i-am-ironman
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the assistant:**
   ```bash
   python main.py
   ```

## First Run

On first launch, the assistant will ask:
```
🤖 "Hey there, give me a name!"
```

Provide a name (e.g., "JARVIS", "Friday", "Cortana") and it will:
- Save your preference
- Calibrate microphone levels
- Test voice output
- Begin listening for wake word

## Usage Examples

### Wake the Assistant
```
"Hey [AssistantName]!"
or
"[AssistantName]!"
```

### Commands

**Application Control:**
```
"Open Chrome"
"Launch VS Code"
"Open Discord"
```

**Volume Control:**
```
"Increase volume"
"Set volume to 50%"
"Mute"
"Unmute"
```

**Brightness Control:**
```
"Increase brightness"
"Set brightness to 75%"
"Decrease brightness"
```

**System Maintenance:**
```
"Clean cache"
"Free up RAM"
"Clear temp files"
"Show system info"
```

**Other Utilities:**
```
"Lock screen"
"Shutdown"
"Sleep"
"Show clipboard"
```

## Configuration

Edit `data/config.json` to customize:

```json
{
  "assistant_name": "JARVIS",
  "wake_words": ["hey jarvis", "jarvis", "wake up"],
  "listening_timeout": 5,
  "voice_speed": 1.0,
  "tts_engine": "pyttsx3",
  "auto_start": true
}
```

## Supported Applications

Default app mappings (easily customizable):
- **Browsers:** Chrome, Firefox, Edge
- **Development:** VS Code, Python, Git Bash
- **Communication:** Discord, Telegram, WhatsApp
- **Productivity:** Notepad, Calc, Paint
- **Media:** VLC, Spotify

## API & Extension

Add custom commands easily:

```python
# In commands/custom.py
from commands.utils import register_command

@register_command(["play music", "start music"])
def play_music():
    # Your code here
    os.startfile("spotify_path")
    return "Playing music now"
```

## System Requirements

| Component | Requirement |
|-----------|-------------|
| RAM       | Minimum 2GB |
| Storage   | ~500MB      |
| CPU       | Any modern processor |
| Network   | None (fully offline) |

## Performance

- **Startup time:** ~3-5 seconds
- **Wake word latency:** <500ms
- **Command recognition:** 1-2 seconds
- **Memory usage:** ~100-150MB
- **CPU usage:** <5% when idle

## Troubleshooting

### Microphone not detected
```bash
python -c "import pyaudio; print(pyaudio.PyAudio().get_device_count())"
```

### No sound output
- Check speaker connection
- Test TTS: `python -c "from pyttsx3 import init; e=init(); e.say('Hello'); e.runAndWait()"`

### Wake word not detected
- Check audio levels in system settings
- Ensure microphone is properly configured
- Try speaking closer to microphone

## Roadmap

- [ ] Machine Learning for intent classification
- [ ] Custom neural net for wake word detection
- [ ] Integration with smart home devices
- [ ] Web dashboard for control
- [ ] Mobile app integration
- [ ] Multi-language support
- [ ] Natural language processing improvements
- [ ] Scheduled tasks and reminders
- [ ] Email integration
- [ ] Calendar sync

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## Privacy & Security

✅ **Fully Local** - No cloud processing
✅ **No Tracking** - No data collection
✅ **Open Source** - Transparent code
✅ **Offline** - Works without internet

## License

MIT License - Free to use and modify

## Author

Created by [Shivraj Suman](https://github.com/shivraj1182)

## Support

Having issues? 
- Check [Troubleshooting](#troubleshooting) section
- Open an [Issue](https://github.com/shivraj1182/i-am-ironman/issues)
- Read the [Documentation](https://github.com/shivraj1182/i-am-ironman/wiki)

## Disclaimer

This project is for educational purposes. Use responsibly and ensure you have proper permissions before automating system actions.

---

**"Sir, would you like to turn up the lights?"** 🤖💡
