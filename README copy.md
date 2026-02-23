# Virtual Voice Assistant

A Python-based voice assistant that can open applications, play music on YouTube, answer questions, and provides a beautiful UI with a spinning ball animation and conversation history.

## Features

- 🎤 **Voice Control**: Control your laptop hands-free with natural language
- 🚀 **App Launcher**: Open applications naturally - "open chrome", "launch spotify", "start calculator"
- 🎵 **Music Player**: Play music on YouTube - "play despacito", "play some jazz music"
- 💬 **Intelligent Assistant**: Ask questions and get smart answers powered by Strands Agents with custom tools
- ⏰ **Time & Date**: Ask "what time is it?" or "what's the date today?"
- 🎨 **Futuristic UI**: Tkinter interface with animated HUD (like JARVIS) and scrollable conversation history
- 👋 **Easy Exit**: Say "bye" to close the assistant

## How It Works

The assistant uses **Strands Agents** with custom tools:
- `current_time` - Provides current date and time in IST (Indian Standard Time)
- `open_application` - Opens apps on your computer
- `play_music_on_youtube` - Plays music on YouTube

The LLM intelligently decides which tool to use based on your natural language input!

**Special Features:**
- ⏰ All times are in IST timezone
- 💬 Concise one-line responses (no lengthy explanations)
- 🎨 Futuristic HUD animation that glows red when listening

## Installation

1. Install Python 3.8 or higher

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. For PyAudio on Windows, you may need to install it separately:
```bash
pip install pipwin
pipwin install pyaudio
```

## Usage

Run the voice assistant:
```bash
python main.py
```

### Example Commands

Just speak naturally! The AI agent will understand and use the right tool:

**Opening Applications:**
- "open chrome"
- "launch spotify"
- "start calculator"
- "can you open notepad for me?"

**Playing Music:**
- "play despacito"
- "play some jazz music"
- "I want to listen to shape of you"

**Questions & Information:**
- "what time is it?"
- "what's the date today?"
- "tell me a joke"
- "what is 25 times 37?"

**Exit:**
- "bye"
- "goodbye"
- "exit"

## Requirements

- Python 3.8+
- Microphone access
- Internet connection (for speech recognition and music playback)
- Strands Agents API access

## Troubleshooting

### Microphone not working
- Check system permissions for microphone access
- Ensure your microphone is properly connected
- Try adjusting the `energy_threshold` in `speech_engine.py`

### Speech recognition errors
- Speak clearly and at a moderate pace
- Reduce background noise
- Check your internet connection

### Application launch issues
- Use the exact application name as it appears in your system
- On Windows, try adding ".exe" to the app name

## Project Structure

```
.
├── main.py                 # Main application controller
├── speech_engine.py        # Voice input and text-to-speech
├── command_processor.py    # Command parsing and intent detection
├── action_executors.py     # Action execution (apps, music, Q&A)
├── ui_manager.py          # Tkinter UI management
├── models.py              # Data models
└── requirements.txt       # Python dependencies
```

## License

MIT License
