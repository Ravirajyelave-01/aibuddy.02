"""
Speech Engine - Handles voice input and audio output
"""
import speech_recognition as sr
import pyttsx3
import logging

logger = logging.getLogger(__name__)


class SpeechEngine:
    """Handles speech recognition and text-to-speech"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()
        self._is_listening = False
        
        # Configure recognizer for better performance
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        
    def listen(self) -> str:
        """
        Captures voice input and converts to text using Google Speech Recognition
        
        Returns:
            str: Recognized text from voice input, or empty string if recognition fails
        """
        self._is_listening = True
        max_retries = 3
        retry_count = 0
        
        try:
            with sr.Microphone() as source:
                logger.info("Listening...")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                logger.info("Processing speech...")
                
                # Retry logic for network errors
                while retry_count < max_retries:
                    try:
                        # Use Google Speech Recognition (free)
                        text = self.recognizer.recognize_google(audio)
                        logger.info(f"Recognized: {text}")
                        self._is_listening = False
                        return text
                    except sr.RequestError as e:
                        retry_count += 1
                        if retry_count < max_retries:
                            logger.warning(f"Network error (attempt {retry_count}/{max_retries}): {e}")
                            import time
                            time.sleep(2 ** retry_count)  # Exponential backoff
                        else:
                            logger.error(f"Failed after {max_retries} attempts: {e}")
                            self._is_listening = False
                            return ""
                
        except sr.WaitTimeoutError:
            logger.warning("Listening timeout - no speech detected")
            self._is_listening = False
            return ""
            
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            self._is_listening = False
            return ""
            
        except Exception as e:
            logger.error(f"Error in speech recognition: {e}")
            self._is_listening = False
            return ""
        
        self._is_listening = False
        return ""
    
    def speak(self, text: str) -> None:
        """
        Converts text to speech using pyttsx3
        
        Args:
            text: The text to speak
        """
        try:
            logger.info(f"Speaking: {text}")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            logger.error(f"Error in text-to-speech: {e}")
    
    def is_listening(self) -> bool:
        """
        Returns current listening state
        
        Returns:
            bool: True if currently listening, False otherwise
        """
        return self._is_listening
