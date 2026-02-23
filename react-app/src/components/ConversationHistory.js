import React, { useEffect, useRef } from 'react';
import './ConversationHistory.css';
import { User, Bot, AlertCircle } from 'lucide-react';

function ConversationHistory({ messages }) {
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="conversation-history">
      <div className="messages-container">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.type}`}>
            <div className="message-avatar">
              {msg.type === 'user' && <User size={20} />}
              {msg.type === 'assistant' && <Bot size={20} />}
              {msg.type === 'error' && <AlertCircle size={20} />}
            </div>
            <div className="message-content">
              <div className="message-text">{msg.text}</div>
              <div className="message-time">
                {msg.timestamp?.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </div>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
}

export default ConversationHistory;
