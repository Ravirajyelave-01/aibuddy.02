import React, { useState, useEffect, useRef } from 'react';
import io from 'socket.io-client';
import axios from 'axios';
import './App.css';
import VoiceButton from './components/VoiceButton';
import ConversationHistory from './components/ConversationHistory';
import HUDAnimation from './components/HUDAnimation';
import TextInput from './components/TextInput';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function App() {
  const [listening, setListening] = useState(false);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [connected, setConnected] = useState(false);
  const socketRef = useRef(null);

  useEffect(() => {
    // Connect to WebSocket
    socketRef.current = io(API_URL, {
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: 5
    });

    socketRef.current.on('connect', () => {
      console.log('Connected to server');
      setConnected(true);
      // Add welcome message
      setMessages([{
        type: 'assistant',
        text: "Hello! I'm your voice assistant. How can I help you?",
        timestamp: new Date()
      }]);
    });

    socketRef.current.on('disconnect', () => {
      console.log('Disconnected from server');
      setConnected(false);
      setListening(false);
    });

    socketRef.current.on('status', (data) => {
      setListening(data.listening);
    });

    socketRef.current.on('user_message', (data) => {
      setMessages(prev => [...prev, {
        type: 'user',
        text: data.text,
        timestamp: new Date()
      }]);
    });

    socketRef.current.on('assistant_message', (data) => {
      setMessages(prev => [...prev, {
        type: 'assistant',
        text: data.text,
        timestamp: new Date()
      }]);
      setLoading(false);
    });

    socketRef.current.on('error', (data) => {
      setMessages(prev => [...prev, {
        type: 'error',
        text: `Error: ${data.message}`,
        timestamp: new Date()
      }]);
      setLoading(false);
    });

    return () => {
      if (socketRef.current) {
        socketRef.current.disconnect();
      }
    };
  }, []);

  const handleStartListening = async () => {
    if (!connected) {
      alert('Not connected to server. Please refresh the page.');
      return;
    }
    try {
      socketRef.current.emit('start_listening');
      setLoading(true);
    } catch (error) {
      console.error('Error starting listening:', error);
      alert('Failed to start listening');
    }
  };

  const handleStopListening = async () => {
    try {
      socketRef.current.emit('stop_listening');
      setLoading(false);
    } catch (error) {
      console.error('Error stopping listening:', error);
    }
  };

  const handleTextCommand = async (text) => {
    if (!text.trim() || !connected) return;

    try {
      setLoading(true);
      socketRef.current.emit('text_command', { text });
    } catch (error) {
      console.error('Error sending text command:', error);
      alert('Failed to send command');
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <HUDAnimation listening={listening} />
      
      <div className="app-container">
        <div className="header">
          <h1>🎤 Voice Assistant</h1>
          <div className={`status-indicator ${connected ? 'connected' : 'disconnected'}`}>
            {connected ? '✓ Connected' : '✗ Disconnected'}
          </div>
        </div>

        <ConversationHistory messages={messages} />

        <div className="controls">
          <VoiceButton
            listening={listening}
            loading={loading}
            onStart={handleStartListening}
            onStop={handleStopListening}
            disabled={!connected}
          />
          <TextInput onSubmit={handleTextCommand} disabled={!connected || loading} />
        </div>
      </div>
    </div>
  );
}

export default App;
