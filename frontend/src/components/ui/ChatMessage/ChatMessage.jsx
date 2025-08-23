import React from 'react';

function ChatMessage({ message }) {
  const { role, content } = message;
  
  let avatarLabel;
  let messageClass;
  
  switch (role) {
    case 'user':
      avatarLabel = 'You';
      messageClass = 'user-message';
      break;
    case 'assistant':
      avatarLabel = 'AI';
      messageClass = 'assistant-message';
      break;
    case 'system':
      avatarLabel = 'SYS';
      messageClass = 'system-message';
      break;
    default:
      avatarLabel = '?';
      messageClass = 'unknown-message';
  }
  
  return (
    <div className={`chat-message ${messageClass}`}>
      <div className="message-avatar">
        {avatarLabel}
      </div>
      <div className="message-content" dangerouslySetInnerHTML={{ __html: content }}>
      </div>
    </div>
  );
}

export default ChatMessage;