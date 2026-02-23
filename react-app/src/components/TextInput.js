import React, { useState, useRef, useEffect } from 'react';
import './TextInput.css';
import { Send } from 'lucide-react';

function TextInput({ onSubmit, disabled }) {
  const [text, setText] = useState('');
  const inputRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (text.trim() && !disabled) {
      onSubmit(text);
      setText('');
      inputRef.current?.focus();
    }
  };

  return (
    <form className="text-input-form" onSubmit={handleSubmit}>
      <input
        ref={inputRef}
        type="text"
        placeholder="Type a command or question..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        disabled={disabled}
        className="text-input"
        autoComplete="off"
      />
      <button
        type="submit"
        className="send-button"
        disabled={disabled || !text.trim()}
        title="Send message"
      >
        <Send size={20} />
      </button>
    </form>
  );
}

export default TextInput;
