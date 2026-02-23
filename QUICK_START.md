# Quick Start - Voice Assistant React UI

## 🚀 Get Started in 5 Minutes

### Windows Users

```batch
# 1. Double-click setup.bat to install everything
setup.bat

# 2. After setup completes, run:
python app.py

# 3. Open browser
http://localhost:5000
```

### Mac/Linux Users

```bash
# 1. Run setup
bash setup.sh

# 2. After setup, run:
python app.py

# 3. Open browser
http://localhost:5000
```

## 📋 What Gets Installed

- ✅ Python dependencies (Flask, speech recognition, AI engine)
- ✅ Node.js dependencies (React, socket.io client)
- ✅ React production build
- ✅ All required libraries

## 🎤 How to Use

### Voice Commands
1. Click **"Start Listening"** button
2. Speak clearly into your microphone
3. Wait for response (you'll hear the assistant speak)

### Text Commands
1. Type in the text box at the bottom
2. Press Enter or click send button
3. Get instant response

### Supported Commands
- "Open chrome" → Opens Chrome browser
- "Play [song name]" → Plays music on YouTube
- "What time is it?" → Tells you the current time
- "What is [question]?" → Answers any question using AI
- "Goodbye" / "Exit" → Closes the app

## 🎨 UI Features

- 💫 **Animated HUD Background** - Cyan glowing animation
- 💬 **Chat History** - See all conversations with timestamps
- 🟢 **Status Indicator** - Shows connection status
- 📳 **Real-time Updates** - Instant responses via WebSocket
- 📱 **Responsive Design** - Works on desktop, tablet, phone

## ⚙️ Troubleshooting

### Issue: "Connection refused"
```bash
# Make sure Flask is running
python app.py
```

### Issue: Microphone not working
- ✅ Check Windows/Mac/Linux audio settings
- ✅ Test microphone in System Settings
- ✅ Grant microphone permissions if prompted
- ✅ Make sure no other app is using the mic

### Issue: React build failed
```bash
cd react-app
npm cache clean --force
rm -rf node_modules
npm install
npm run build
cd ..
```

### Issue: Port 5000 already in use
```bash
# Change port in app.py
# Search for: socketio.run(app, host='0.0.0.0', port=5000)
# Change 5000 to 5001 or another number
```

## 📦 For Production/Cloud Deployment

### Docker (Easiest)
```bash
docker build -t voice-assistant .
docker run -p 5000:5000 voice-assistant
```

### Cloud Platforms (Railway, Render, AWS, etc.)
1. Upload files to cloud platform
2. Set build command: `pip install -r requirements-deploy.txt && cd react-app && npm install && npm run build && cd ..`
3. Set start command: `gunicorn --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 -b 0.0.0.0:$PORT --timeout 120 wsgi:app`
4. Expose port 5000
5. Enable persistent logging

See `DEPLOYMENT_GUIDE.md` for detailed cloud deployment instructions.

## 📚 Full Documentation

- **REACT_README.md** - Comprehensive guide with all features
- **DEPLOYMENT_GUIDE.md** - Detailed deployment instructions
- **ARCHITECTURE.md** - System architecture overview

## 🔑 Key Files Modified/Created

### New Files (React UI)
- `app.py` - Flask backend replacing Tkinter
- `wsgi.py` - Production WSGI entry
- `react-app/` - Complete React application
- `Dockerfile` - Container configuration
- `docker-compose.yml` - Multi-container setup
- `requirements-deploy.txt` - Web dependencies

### Original Files (Still Used)
- `speech_engine.py` - Unchanged
- `action_executors.py` - Unchanged
- `models.py` - Unchanged
- `command_processor.py` - Unchanged

### Deprecated (Tkinter - No Longer Used)
- `main.py` - Replaced by Flask app
- `ui_manager.py` - Replaced by React UI

## 💡 Pro Tips

1. **Microphone Quality** - Better mic = better recognition
2. **Internet Speed** - Fast internet helps with API calls
3. **Multiple Users** - App supports multiple browser tabs/users simultaneously
4. **Mobile Access** - Access from phone on same network: `http://[your-computer-ip]:5000`
5. **Custom Commands** - Edit `action_executors.py` to add new capabilities

## ❓ Common Questions

**Q: Can I use this without internet?**
A: Speech recognition requires internet. Local recognition can be added.

**Q: Can I modify the AI responses?**
A: Yes! Edit the system prompt in `action_executors.py` in the `QuestionAnswerer` class.

**Q: How do I run this 24/7?**
A: Use `nohup python app.py &` (Linux/Mac) or Windows Task Scheduler, or deploy to cloud.

**Q: Can I add more commands?**
A: Yes! The system uses Strands Agents LLM. Add new tools in `action_executors.py`.

**Q: Why React instead of Tkinter?**
A: React offers: better UI, easy deployment, mobile-friendly, cloud-ready, and a modern dev experience.

---

**Need help?** Check the logs:
```bash
tail -f voice_assistant.log  # Linux/Mac
type voice_assistant.log     # Windows (or open in editor)
```
