import React from 'react';
import './VoiceButton.css';
import { Mic, Square } from 'lucide-react';

function VoiceButton({ listening, loading, onStart, onStop, disabled }) {
  return (
    <div className="voice-button-container">
      {!listening ? (
        <button
          className={`voice-button start ${disabled ? 'disabled' : ''}`}
          onClick={onStart}
          disabled={disabled || loading}
          title="Click to start listening"
        >
          <Mic size={24} />
          <span>{loading ? 'Initializing...' : 'Start Listening'}</span>
        </button>
      ) : (
        <button
          className="voice-button stop listening"
          onClick={onStop}
          disabled={disabled}
          title="Click to stop listening"
        >
          <Square size={24} fill="currentColor" />
          <span>Stop</span>
          <div className="pulse-ring"></div>
        </button>
      )}
    </div>
  );
}

export default VoiceButton;
