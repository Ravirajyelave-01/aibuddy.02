"""
Command Processor - Parses voice input and determines user intent
"""
import re
import logging
from models import Command, CommandIntent

logger = logging.getLogger(__name__)


class CommandProcessor:
    """Processes voice commands and extracts intent and parameters"""
    
    def __init__(self):
        # Keywords for different intents
        self.exit_keywords = ['bye', 'exit', 'quit', 'goodbye', 'stop']
        self.open_keywords = ['open', 'launch', 'start', 'run']
        self.music_keywords = ['play', 'music', 'song']
        
    def process_command(self, text: str) -> Command:
        """
        Analyzes text and returns a Command object with intent and parameters
        
        Args:
            text: The voice input text to process
            
        Returns:
            Command: Parsed command with intent and parameters
        """
        if not text or not text.strip():
            return Command(
                intent=CommandIntent.UNKNOWN,
                parameters={},
                raw_text=text
            )
        
        text_lower = text.lower().strip()
        
        # Check for exit command
        if self._is_exit_command(text_lower):
            logger.info("Exit command detected")
            return Command(
                intent=CommandIntent.EXIT,
                parameters={},
                raw_text=text
            )
        
        # Check for open application command
        app_name = self._extract_app_name(text_lower)
        if app_name:
            logger.info(f"Open app command detected: {app_name}")
            return Command(
                intent=CommandIntent.OPEN_APP,
                parameters={'app_name': app_name},
                raw_text=text
            )
        
        # Check for music playback command
        song_name = self._extract_song_name(text_lower)
        if song_name:
            logger.info(f"Play music command detected: {song_name}")
            return Command(
                intent=CommandIntent.PLAY_MUSIC,
                parameters={'song_name': song_name},
                raw_text=text
            )
        
        # Default to question answering
        logger.info("Question answering command detected")
        return Command(
            intent=CommandIntent.ANSWER_QUESTION,
            parameters={'question': text},
            raw_text=text
        )
    
    def _is_exit_command(self, text: str) -> bool:
        """Check if text contains exit keywords"""
        return any(keyword in text for keyword in self.exit_keywords)
    
    def _extract_app_name(self, text: str) -> str:
        """
        Extract application name from open command
        
        Args:
            text: The voice input text
            
        Returns:
            str: Application name if found, empty string otherwise
        """
        for keyword in self.open_keywords:
            if keyword in text:
                # Find text after the keyword
                pattern = rf'{keyword}\s+(.+)'
                match = re.search(pattern, text)
                if match:
                    app_name = match.group(1).strip()
                    # Remove common trailing words
                    app_name = re.sub(r'\s+(please|now|application|app)$', '', app_name)
                    return app_name
        return ""
    
    def _extract_song_name(self, text: str) -> str:
        """
        Extract song name from music command
        
        Args:
            text: The voice input text
            
        Returns:
            str: Song name if found, empty string otherwise
        """
        for keyword in self.music_keywords:
            if keyword in text:
                # Find text after the keyword
                pattern = rf'{keyword}\s+(.+)'
                match = re.search(pattern, text)
                if match:
                    song_name = match.group(1).strip()
                    # Remove common trailing words
                    song_name = re.sub(r'\s+(please|now|on youtube)$', '', song_name)
                    return song_name
        return ""
