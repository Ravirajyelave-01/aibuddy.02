# Voice Assistant - React UI Setup

## Quick Start Guide

### Prerequisites
- Node.js 16+ 
- Python 3.9+
- pip

### Step 1: Install Backend Dependencies
```bash
pip install -r requirements-deploy.txt
```

### Step 2: Build React App
```bash
cd react-app
npm install
npm run build
cd ..
```

### Step 3: Move React Build to Flask Templates
```bash
# Copy built React app to Flask template folder
# The Flask app will serve the built React app
```

### Step 4: Run Development Server

#### Option A: Run Locally (Development)
```bash
# Terminal 1: Start Flask server
python app.py

# Terminal 2: Start React development server (optional, for hot reload)
cd react-app
npm start
```

Visit `http://localhost:3000` (React dev) or `http://localhost:5000` (Flask)

#### Option B: Run Production
```bash
gunicorn --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 -b 0.0.0.0:5000 --timeout 120 wsgi:app
```

Visit `http://localhost:5000`

### Step 5: Docker Deployment

```bash
# Build Docker image
docker build -t voice-assistant .

# Run container
docker run -p 5000:5000 --device /dev/snd:/dev/snd voice-assistant
```

Or use docker-compose:
```bash
docker-compose up -d
```

## Architecture

### Backend (Python/Flask)
- **app.py**: Flask server with WebSocket support
- **speech_engine.py**: Handles voice recognition and TTS
- **action_executors.py**: Processes commands and uses Strands Agents LLM
- **wsgi.py**: WSGI entry point for production

### Frontend (React)
- **App.js**: Main React component
- **VoiceButton**: Voice control button with listening state
- **ConversationHistory**: Chat history display
- **TextInput**: Text command input
- **HUDAnimation**: Animated background (like original Tkinter)

## API Endpoints

### REST API
- `GET /`: Serve React app
- `GET /api/health`: Health check
- `POST /api/start-listening`: Start voice listening
- `POST /api/stop-listening`: Stop voice listening
- `POST /api/text-command`: Send text command
- `POST /api/speak`: Text to speech

### WebSocket Events
- `connect`: Client connects
- `disconnect`: Client disconnects
- `start_listening`: Start listening
- `stop_listening`: Stop listening
- `text_command`: Send text command
- `user_message`: User message (broadcast)
- `assistant_message`: Assistant response (broadcast)
- `status`: Listening status update (broadcast)
- `error`: Error message (broadcast)

## Deployment Options

### 1. **Local Machine**
- Run `python app.py`
- Access at `http://localhost:5000`

### 2. **Docker**
```bash
docker-compose up -d
```

### 3. **Heroku** (Free tier deprecated, but can use alternatives)

**Requirements.txt updated** with all necessary dependencies.

### 4. **AWS/DigitalOcean/Azure**
- Use provided Dockerfile
- Scale with multiple workers if needed

### 5. **Replit/Railway/Render**
- Upload files
- Set startup command: `gunicorn --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 -b 0.0.0.0:5000 wsgi:app`
- Configure environment variables

## Environment Variables
- `FLASK_ENV`: Set to `production` for production
- `API_URL`: Backend API URL (for React to connect)

## Troubleshooting

### React Build Issues
```bash
cd react-app
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
npm run build
```

### WebSocket Connection Issues
- Ensure both frontend and backend are on same origin or CORS is enabled
- Check firewall rules for port 5000
- For production, use reverse proxy (nginx/Apache) to handle WebSocket upgrades

### Audio Issues
- On Linux: Install `alsa-utils` and `portaudio19-dev`
- On Mac: Install `portaudio` via brew
- On Windows: Ensure audio drivers are updated

### GPU/Memory Issues
- Reduce gunicorn workers: `-w 1`
- Increase timeout: `--timeout 120`

## Performance Tips

1. **Production Build**
   - Always use `npm run build` before deployment
   - Disable React dev tools

2. **Server**
   - Use gunicorn with multiple workers (2-4)
   - Use nginx as reverse proxy
   - Enable gzip compression

3. **Caching**
   - Browser caches static files
   - WebSocket for real-time updates

## Security Considerations

1. Enable HTTPS in production
2. Set CORS properly for your domain
3. Use environment variables for sensitive data
4. Implement rate limiting
5. Add authentication if needed

## Support

For issues, check:
- Backend logs: `voice_assistant.log`
- Browser console (F12)
- Network tab in DevTools
