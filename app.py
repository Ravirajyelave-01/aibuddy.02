"""
Flask Backend Server - Replaces Tkinter UI with REST API + WebSocket
"""
import logging
import threading
import queue
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room
from speech_engine import SpeechEngine
from action_executors import QuestionAnswerer
import json

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

# Initialize Flask app with correct React build paths
import os
react_build_path = os.path.join(os.path.dirname(__file__), 'react-app', 'build')
app = Flask(__name__, 
            template_folder=react_build_path,
            static_folder=os.path.join(react_build_path, 'static'),
            static_url_path='/static')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Global state
class VoiceAssistantServer:
    def __init__(self):
        self.speech_engine = SpeechEngine()
        self.question_answerer = QuestionAnswerer()
        self.running = False
        self.voice_thread = None
        self.listening = False
        self.message_queue = queue.Queue()
        self.tts_queue = queue.Queue()
        self.tts_thread = threading.Thread(target=self._tts_worker, daemon=True)
        self.tts_thread.start()
        logger.info("TTS worker thread started")
        
    def start_listening(self):
        """Start voice input in background thread"""
        if not self.running:
            self.running = True
            self.voice_thread = threading.Thread(target=self._listen_loop, daemon=True)
            self.voice_thread.start()
            logger.info("Started listening thread")
    
    def stop_listening(self):
        """Stop voice input"""
        self.running = False
        if self.voice_thread:
            self.voice_thread.join(timeout=2)
        logger.info("Stopped listening thread")
    
    def speak_async(self, text: str):
        """Queue text for asynchronous speech"""
        self.tts_queue.put(text)
    
    def _tts_worker(self):
        """Background thread that handles all TTS requests"""
        logger.info("TTS worker started and ready")
        while True:
            try:
                text = self.tts_queue.get(timeout=1)
                if text is None:
                    break
                
                try:
                    preview = text[:50] + "..." if len(text) > 50 else text
                    logger.info(f"TTS worker speaking: {preview}")
                    self.speech_engine.speak(text)
                    logger.info("TTS worker: speech completed")
                except Exception as e:
                    logger.error(f"TTS worker error: {e}", exc_info=True)
            except queue.Empty:
                pass
            except Exception as e:
                logger.error(f"TTS worker unexpected error: {e}", exc_info=True)
    
    def _listen_loop(self):
        """Main listening loop"""
        while self.running:
            try:
                self.listening = True
                with app.app_context():
                    socketio.emit('status', {'listening': True}, to=None)
                
                # Listen for voice input
                text = self.speech_engine.listen()
                
                self.listening = False
                with app.app_context():
                    socketio.emit('status', {'listening': False}, to=None)
                
                if not text:
                    continue
                
                # Check for exit command
                if text.lower().strip() in ['bye', 'goodbye', 'exit', 'quit', 'stop']:
                    with app.app_context():
                        socketio.emit('user_message', {'text': text}, to=None)
                        response = "Goodbye! Have a great day!"
                        socketio.emit('assistant_message', {'text': response}, to=None)
                    self.speak_async(response)
                    self.running = False
                    continue
                
                # Add user message
                with app.app_context():
                    socketio.emit('user_message', {'text': text}, to=None)
                
                # Get response from AI
                response = self.question_answerer.answer_question(text)
                response_text = str(response)  # Convert AgentResult to string
                
                # Send response
                with app.app_context():
                    socketio.emit('assistant_message', {'text': response_text}, to=None)
                
                # Queue for async speech
                self.speak_async(response_text)
                
            except Exception as e:
                logger.error(f"Error in listening loop: {e}")
                self.listening = False
                with app.app_context():
                    socketio.emit('status', {'listening': False}, to=None)
                    socketio.emit('error', {'message': str(e)}, to=None)

# Initialize server
assistant_server = VoiceAssistantServer()

# REST API Routes
@app.route('/')
def index():
    """Serve the React app"""
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'Voice Assistant API'})

@app.route('/api/start-listening', methods=['POST'])
def start_listening():
    """Start listening for voice input"""
    try:
        assistant_server.start_listening()
        return jsonify({'success': True, 'message': 'Started listening'})
    except Exception as e:
        logger.error(f"Error starting listening: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stop-listening', methods=['POST'])
def stop_listening():
    """Stop listening for voice input"""
    try:
        assistant_server.stop_listening()
        return jsonify({'success': True, 'message': 'Stopped listening'})
    except Exception as e:
        logger.error(f"Error stopping listening: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/text-command', methods=['POST'])
def text_command():
    """Process text command (for typing instead of voice)"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'success': False, 'error': 'Empty text'}), 400
        
        # Process command
        response = assistant_server.question_answerer.answer_question(text)
        response_text = str(response)  # Convert AgentResult to string
        
        # Emit messages via WebSocket to all clients
        socketio.emit('user_message', {'text': text}, to=None)
        socketio.emit('assistant_message', {'text': response_text}, to=None)
        
        # Queue for async speech
        assistant_server.speak_async(response_text)
        
        return jsonify({
            'success': True,
            'response': response_text,
            'user_message': text
        })
    except Exception as e:
        logger.error(f"Error processing text command: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/speak', methods=['POST'])
def speak():
    """Text to speech only"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'success': False, 'error': 'Empty text'}), 400
        
        assistant_server.speak_async(text)
        return jsonify({'success': True, 'message': 'Speaking'})
    except Exception as e:
        logger.error(f"Error speaking: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# WebSocket Events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info(f"Client connected: {request.sid}")
    emit('connect_response', {'data': 'Connected to Voice Assistant'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info(f"Client disconnected: {request.sid}")

@socketio.on('start_listening')
def handle_start_listening():
    """Start listening via WebSocket"""
    try:
        assistant_server.start_listening()
        emit('status', {'listening': True})
    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('stop_listening')
def handle_stop_listening():
    """Stop listening via WebSocket"""
    try:
        assistant_server.stop_listening()
        emit('status', {'listening': False})
    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('text_command')
def handle_text_command(data):
    """Process text command via WebSocket"""
    try:
        text = data.get('text', '').strip()
        if not text:
            emit('error', {'message': 'Empty text'})
            return
        
        # Process command
        response = assistant_server.question_answerer.answer_question(text)
        response_text = str(response)  # Convert AgentResult to string
        
        # Emit messages to all clients using emit() with broadcast
        emit('user_message', {'text': text}, broadcast=True)
        emit('assistant_message', {'text': response_text}, broadcast=True)
        
        # Queue for async speech
        assistant_server.speak_async(response_text)
    except Exception as e:
        logger.error(f"Error processing text command: {e}")
        emit('error', {'message': str(e)})

if __name__ == '__main__':
    try:
        logger.info("Starting Voice Assistant Server...")
        socketio.run(app, host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
        assistant_server.stop_listening()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise
