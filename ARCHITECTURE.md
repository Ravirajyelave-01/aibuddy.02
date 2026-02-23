# Voice Assistant Architecture

## Overview

This voice assistant uses **Strands Agents** with custom tools to provide an intelligent, natural language interface for controlling your computer.

## Key Design Decision

Instead of using traditional command parsing (regex, keyword matching), we leverage **Strands Agents LLM** with custom tools. This allows users to speak naturally, and the AI decides which tool to use.

## Architecture Flow

```
User speaks → Speech Recognition → Strands Agent (with tools) → Tool Execution → Response
                                          ↓
                                    Decides which tool:
                                    - current_time
                                    - open_application  
                                    - play_music_on_youtube
```

## Custom Tools

### 1. `open_application(app_name: str)`
- Opens applications on Windows/macOS/Linux
- Supports common apps: Chrome, Firefox, VS Code, Spotify, Office apps, etc.
- Uses `subprocess` and `shell=True` for Windows compatibility

### 2. `play_music_on_youtube(song_name: str)`
- Opens YouTube search in default browser
- Uses `webbrowser` module for cross-platform compatibility
- Searches for the song/artist name

### 3. `current_time()` (from strands-tools)
- Provides current date and time
- Built-in tool from the strands-tools package

## Components

### 1. Speech Engine (`speech_engine.py`)
- **Input**: Google Speech Recognition API (free)
- **Output**: pyttsx3 (offline TTS)
- Handles microphone access and audio processing
- Includes retry logic for network errors

### 2. Action Executors (`action_executors.py`)
- Defines custom Strands tools using `@tool` decorator
- QuestionAnswerer class initializes Agent with all tools
- Agent intelligently routes requests to appropriate tools

### 3. UI Manager (`ui_manager.py`)
- Tkinter-based interface
- Spinning ball animation (60 FPS)
- Scrollable conversation history
- Status indicator (listening/ready)

### 4. Main Controller (`main.py`)
- Manages threading (UI on main thread, voice on background thread)
- Queue-based communication for thread safety
- Simple flow: listen → send to agent → display response

## Threading Model

```
Main Thread (Tkinter UI)
    ↓
    process_ui_queue() - checks queue every 100ms
    ↑
    Queue (thread-safe)
    ↑
Background Thread (Voice Processing)
    ↓
    listen() → agent() → put results in queue
```

## Why This Approach?

**Traditional Approach (what we moved away from):**
- Regex patterns for each command type
- Brittle - "open chrome" works, "can you open chrome?" doesn't
- Requires exact phrasing
- Hard to extend

**Strands Agent Approach (current):**
- Natural language understanding
- "open chrome", "launch chrome", "can you open chrome?" all work
- Easy to add new tools
- LLM decides which tool to use based on context

## Adding New Tools

To add a new capability:

1. Define a tool function with `@tool` decorator:
```python
@tool
def my_new_tool(param: str) -> str:
    """
    Description of what this tool does.
    
    Args:
        param (str): Description of parameter
    
    Returns:
        str: Description of return value
    """
    # Implementation
    return "result"
```

2. Add it to the Agent initialization:
```python
self.agent = Agent(tools=[current_time, open_application, play_music_on_youtube, my_new_tool])
```

That's it! The LLM will automatically understand when to use your new tool based on the docstring.

## Dependencies

- **strands-agents**: LLM agent framework
- **strands-tools**: Community tools (current_time, etc.)
- **SpeechRecognition**: Voice input
- **pyttsx3**: Text-to-speech
- **tkinter**: GUI (included with Python)

## Future Enhancements

- Add more tools (file operations, system info, web search)
- Wake word detection
- Multi-language support
- Conversation memory/context
- Custom voice profiles
