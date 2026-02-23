"""
Data models for the Voice Assistant
"""
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class CommandIntent(Enum):
    """Enumeration of possible command intents"""
    OPEN_APP = "open_app"
    PLAY_MUSIC = "play_music"
    ANSWER_QUESTION = "answer_question"
    EXIT = "exit"
    UNKNOWN = "unknown"


@dataclass
class Command:
    """Represents a parsed voice command"""
    intent: CommandIntent
    parameters: dict
    raw_text: str


class MessageType(Enum):
    """Enumeration of message types in conversation history"""
    USER = "user"
    ASSISTANT = "assistant"


@dataclass
class Message:
    """Represents a message in the conversation history"""
    type: MessageType
    content: str
    timestamp: datetime
