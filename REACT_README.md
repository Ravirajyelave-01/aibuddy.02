# Voice Assistant - React UI Edition

A modern, web-based voice assistant with a beautiful React UI that replaces the Tkinter interface. Control your computer with voice commands through a professional web interface.

## Features

✨ **Modern Web UI** - Beautiful, responsive React interface with real-time updates
🎤 **Voice Control** - Listen and respond with natural speech
⚡ **Real-time Communication** - WebSocket for instant feedback
🎨 **Futuristic Design** - HUD animation background with cyan theme
📱 **Mobile Responsive** - Works on desktop, tablet, and mobile
🚀 **Easy Deployment** - Docker, production-ready with gunicorn
🔌 **Dual Interface** - Both voice and text command support
💬 **Chat History** - Beautiful conversation display with timestamps

## Project Structure

```
ai-voice-assistance/
├── app.py                          # Flask backend server with WebSocket
├── wsgi.py                         # WSGI entry point for production
├── speech_engine.py                # Speech recognition & TTS (unchanged)
├── action_executors.py             # LLM & command processing (unchanged)
├── ui_manager.py                   # Deprecated (Tkinter UI)
├── main.py                         # Deprecated (Tkinter entry point)
│
├── react-app/                      # React frontend
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js                  # Main React component
│   │   ├── App.css
│   │   ├── index.js
│   │   ├── index.css
│   │   └── components/
│   │       ├── VoiceButton.js      # Voice control button
│   │       ├── ConversationHistory.js  # Chat display
│   │       ├── TextInput.js        # Text command input
│   │       └── HUDAnimation.js     # Background animation
│   ├── package.json
│   └── build/                      # Built files (generated)
│
├── Dockerfile                      # Docker container config
├── docker-compose.yml              # Docker Compose setup
├── requirements-deploy.txt         # Python dependencies
├── setup.bat / setup.sh           # Setup scripts
├── run_production.bat / run_production.sh  # Production run scripts
├── DEPLOYMENT_GUIDE.md            # Detailed deployment guide
└── QUICK_START.md                 # Quick start guide
```

## Quick Start

### For Windows Users

1. **Run Setup Script**
   ```bash
   setup.bat
   ```

2. **Start Server**
   ```bash
   python app.py
   ```

3. **Visit**
   ```
   http://localhost:5000
   ```

### For Linux/Mac Users

1. **Run Setup Script**
   ```bash
   bash setup.sh
   ```

2. **Start Server**
   ```bash
   python app.py
   ```

3. **Visit**
   ```
   http://localhost:5000
   ```

## Installation (Manual)

### Prerequisites
- Python 3.9 or higher
- Node.js 16 or higher
- npm or yarn

### Step-by-Step

```bash
# 1. Install Python dependencies
pip install -r requirements-deploy.txt

# 2. Install Node dependencies and build React
cd react-app
npm install
npm run build
cd ..

# 3. Start the server
python app.py
```

Visit `http://localhost:5000`

## Development Mode

For development with hot reload:

```bash
# Terminal 1: Start Flask backend
python app.py

# Terminal 2: Start React dev server
cd react-app
npm start
```

Frontend will be at `http://localhost:3000` and will proxy requests to Flask at `http://localhost:5000`.

## Production Deployment

### Option 1: Direct Gunicorn (Linux/Mac)

```bash
gunicorn --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 -b 0.0.0.0:5000 --timeout 120 wsgi:app
```

Or use the provided script:
```bash
bash run_production.sh
```

### Option 2: Docker

```bash
docker build -t voice-assistant .
docker run -p 5000:5000 --device /dev/snd:/dev/snd voice-assistant
```

Or use Docker Compose:
```bash
docker-compose up -d
```

### Option 3: Cloud Platforms

**Heroku (deprecated free tier, use alternatives)**

**Railway.app**
```bash
# Add railway.toml or use web interface
# Start command: gunicorn --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 -b 0.0.0.0:$PORT --timeout 120 wsgi:app
```

**Render.com**
- Build command: `pip install -r requirements-deploy.txt && cd react-app && npm install && npm run build && cd ..`
- Start command: `gunicorn --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 -b 0.0.0.0:$PORT --timeout 120 wsgi:app`
- Add port 5000

**AWS/DigitalOcean/Azure**
- Use provided Dockerfile
- Configure auto-scaling if needed

## Architecture

### Backend (Flask + Python)

**Flask Server** (`app.py`)
- REST API for command processing
- WebSocket support for real-time updates
- Integration with existing Python components

**Components Used**
- `SpeechEngine`: Google Speech Recognition + pyttsx3 TTS
- `QuestionAnswerer`: Strands Agents LLM for intelligent responses
- `action_executors.py`: Open apps, play music, answer questions

### Frontend (React)

**Real-time Communication**
- Socket.io for WebSocket connection
- Axios for REST API calls
- State management with React hooks

**UI Components**
- **VoiceButton**: Toggle voice listening with visual feedback
- **ConversationHistory**: Beautiful chat display with timestamps
- **TextInput**: Alternative text command input
- **HUDAnimation**: Animated canvas background (like original Tkinter)

## API Reference

### REST Endpoints

```
GET  /                         # Serve React app
GET  /api/health              # Health check
POST /api/start-listening     # Start voice input
POST /api/stop-listening      # Stop voice input
POST /api/text-command        # Send text command
POST /api/speak               # Text to speech
```

### WebSocket Events

**Client → Server**
- `start_listening`: Begin voice input
- `stop_listening`: End voice input  
- `text_command`: Send text with `{text: string}`

**Server → Client**
- `connect_response`: Connection confirmation
- `status`: Listening state `{listening: bool}`
- `user_message`: User message `{text: string}`
- `assistant_message`: AI response `{text: string}`
- `error`: Error message `{message: string}`

## Configuration

### Environment Variables

```env
FLASK_ENV=production
FLASK_DEBUG=0
API_PORT=5000
REACT_APP_API_URL=http://localhost:5000
WORKERS=1
TIMEOUT=120
```

### Flask Configuration

Edit `app.py`:
```python
socketio.run(app, host='0.0.0.0', port=5000, debug=False)
```

## Troubleshooting

### React Build Fails
```bash
cd react-app
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Port Already in Use
```bash
# Kill process on port 5000
# Windows: netstat -ano | findstr :5000
# Linux/Mac: lsof -i :5000
```

### WebSocket Connection Issues
- Check browser console (F12)
- Verify Flask server is running
- Check firewall settings
- For production: ensure reverse proxy (nginx) supports WebSocket upgrades

### Audio Not Working
- **Windows**: Update audio drivers, ensure microphone permissions
- **Mac**: Grant microphone access: System Preferences → Security & Privacy → Microphone
- **Linux**: 
  ```bash
  sudo apt install alsa-utils portaudio19-dev
  sudo usermod -a -G audio $USER
  # Restart for group changes to take effect
  ```

### Poor Voice Recognition
- Speak clearly and slowly
- Reduce background noise
- Check microphone levels (System Settings)
- May need to retry if network is slow

## Performance Tips

1. **Build Optimization**
   - Always build React before deployment: `npm run build`
   - Disable source maps in production

2. **Server Optimization**
   - Use 2-4 gunicorn workers for small deployments
   - Scale horizontally on cloud platforms
   - Use nginx as reverse proxy

3. **Browser Optimization**
   - Enable browser caching for static files
   - Use CDN for assets
   - Minimize WebSocket message size

## Security

1. **HTTPS Only** - Always use HTTPS in production
2. **CORS** - Properly configured for your domain only
3. **Authentication** - Add if handling sensitive operations
4. **Rate Limiting** - Implement to prevent abuse
5. **Input Validation** - Server-side validation of all inputs
6. **Logging** - Monitor `voice_assistant.log` for issues

## Customization

### Change Theme Colors

Edit `react-app/src/index.css` and `App.css`:
```css
/* Change from cyan to your color */
--primary-color: #00ffff;  /* Edit this */
```

### Modify HUD Animation

Edit `react-app/src/components/HUDAnimation.js`:
```javascript
// Adjust animation speed, colors, shapes, etc.
ctx.strokeStyle = 'rgba(0, 255, 255, 0.6)';  // Color
angleRef.current += 2;  // Speed
```

### Add New Commands

Edit `action_executors.py` to add new tools to the Strands Agent:
```python
@tool
def new_command(param: str) -> str:
    """Description of your command"""
    # Implementation here
    return "Result"

# Add to agent tools list
self.agent = Agent(
    tools=[existing_tools, new_command],
    system_prompt=system_prompt
)
```

## Monitoring & Logging

**Log File**: `voice_assistant.log`

Monitor real-time:
```bash
# Linux/Mac
tail -f voice_assistant.log

# Windows
Get-Content voice_assistant.log -Wait
```

## Support & Issues

1. Check `voice_assistant.log` for errors
2. Open browser DevTools (F12) → Console tab
3. Check Network tab for API/WebSocket issues
4. Ensure all services are running:
   - Flask backend ✓
   - React build ✓
   - Network connectivity ✓

## License

Same as original project

## Changelog

### v2.0.0 - React Web UI
- ✨ Modern React UI replacing Tkinter
- 🚀 REST API + WebSocket backend
- 📱 Responsive design for all devices
- 🐳 Docker & production-ready deployment
- ⚡ Real-time WebSocket communication
- 🎨 Enhanced HUD animation

### v1.0.0 - Original Tkinter UI
- Voice recognition and TTS
- Application launching
- Music playback
- LLM-powered responses
