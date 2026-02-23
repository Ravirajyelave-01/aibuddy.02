"""
Virtual Voice Assistant - Main Entry Point
"""
import logging
import tkinter as tk
import threading
import queue
from speech_engine import SpeechEngine
from action_executors import QuestionAnswerer
from ui_manager import UIManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('voice_assistant.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class VoiceAssistant:
    """Main application controller for the Voice Assistant"""
    
    def __init__(self):
        """Initializes all components"""
        logger.info("Initializing Voice Assistant...")
        
        # Initialize components
        self.speech_engine = SpeechEngine()
        self.question_answerer = QuestionAnswerer()  # Now handles everything with tools
        
        # Initialize UI
        self.root = tk.Tk()
        self.ui_manager = UIManager(self.root)
        
        # State
        self.running = False
        self.voice_thread = None
        
        # Queue for thread-safe communication
        self.ui_queue = queue.Queue()
        
        logger.info("Voice Assistant initialized")
    
    def start(self) -> None:
        """Starts the voice assistant"""
        logger.info("Starting Voice Assistant...")
        self.running = True
        
        # Start animation
        self.ui_manager.start_animation()
        
        # Start processing UI queue
        self.process_ui_queue()
        
        # Schedule welcome message after UI is visible (500ms delay)
        self.root.after(500, self._delayed_start)
        
        # Start UI main loop
        self.root.mainloop()
    
    def _delayed_start(self) -> None:
        """Delayed start after UI is visible"""
        # Add welcome message
        self.ui_manager.add_assistant_message("Hello! I'm your voice assistant. How can I help you?")
        
        # Speak welcome message
        threading.Thread(target=lambda: self.speech_engine.speak("Hello! I'm your voice assistant. How can I help you?"), daemon=True).start()
        
        # Start voice processing in separate thread
        self.voice_thread = threading.Thread(target=self.process_voice_input, daemon=True)
        self.voice_thread.start()
    
    def process_voice_input(self) -> None:
        """Main loop for processing voice commands"""
        while self.running:
            try:
                # Update UI to show listening status
                self.ui_queue.put(('status', True))
                
                # Listen for voice input
                text = self.speech_engine.listen()
                
                # Update UI to show ready status
                self.ui_queue.put(('status', False))
                
                # Skip if no text recognized
                if not text:
                    continue
                
                # Check for exit command
                if text.lower().strip() in ['bye', 'goodbye', 'exit', 'quit', 'stop']:
                    self.ui_queue.put(('user_message', text))
                    response = "Goodbye! Have a great day!"
                    self.ui_queue.put(('assistant_message', response))
                    self.speech_engine.speak(response)
                    import time
                    time.sleep(1)
                    self.ui_queue.put(('shutdown', None))
                    continue
                
                # Add user message to UI
                self.ui_queue.put(('user_message', text))
                
                # Send everything to the agent (it has all the tools)
                response = self.question_answerer.answer_question(text)
                
                # Add response to UI and speak it
                self.ui_queue.put(('assistant_message', response))
                self.speech_engine.speak(response)
                
            except Exception as e:
                logger.error(f"Error in voice processing loop: {e}")
                self.ui_queue.put(('status', False))
                error_msg = "I encountered an error. Please try again."
                self.ui_queue.put(('assistant_message', error_msg))
                self.speech_engine.speak(error_msg)
    
    def process_ui_queue(self) -> None:
        """Process UI updates from the queue (runs on main thread)"""
        try:
            while True:
                try:
                    # Get item from queue without blocking
                    item = self.ui_queue.get_nowait()
                    action, data = item
                    
                    if action == 'status':
                        self.ui_manager.set_listening_status(data)
                    elif action == 'user_message':
                        self.ui_manager.add_user_message(data)
                    elif action == 'assistant_message':
                        self.ui_manager.add_assistant_message(data)
                    elif action == 'shutdown':
                        self.shutdown()
                        
                except queue.Empty:
                    break
        except Exception as e:
            logger.error(f"Error processing UI queue: {e}")
        
        # Schedule next check
        if self.running:
            self.root.after(100, self.process_ui_queue)
    

    
    def shutdown(self) -> None:
        """Cleans up resources and exits"""
        logger.info("Shutting down Voice Assistant...")
        self.running = False
        
        # Wait for voice thread to finish
        if self.voice_thread and self.voice_thread.is_alive():
            self.voice_thread.join(timeout=2)
        
        # Close UI
        self.ui_manager.close()
        
        logger.info("Voice Assistant shut down successfully")


if __name__ == "__main__":
    try:
        assistant = VoiceAssistant()
        assistant.start()
    except KeyboardInterrupt:
        logger.info("Voice Assistant interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise
