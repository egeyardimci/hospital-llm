import React, { useState, useEffect } from 'react';
import { useAppDispatch } from '../../../hooks/useAppDispatch';
import { useAppSelector } from '../../../hooks/useAppSelector';
import { 
  sendMessage, 
  setSelectedModel, 
  setSelectedEmbedding, 
  addUserMessage, 
  clearConversation 
} from '../../../store/slices/chatSlice';
import { DEFAULT_MODELS, DEFAULT_EMBEDDINGS } from '../../../constants';
import ChatMessage from '../../../components/ui/ChatMessage';

function ChatbotTab({ availableModels = [], embeddingModels = [] }) {
  const dispatch = useAppDispatch();
  const { 
    conversation, 
    selectedModel, 
    selectedEmbedding, 
    systemPrompt, 
    isLoading 
  } = useAppSelector(state => state.chat);
  
  const models = availableModels.length ? availableModels : DEFAULT_MODELS;
  const embeddings = embeddingModels.length ? embeddingModels : DEFAULT_EMBEDDINGS;
  
  const [userQuery, setUserQuery] = useState('');

  useEffect(() => {
    if (!selectedModel && models.length > 0) {
      dispatch(setSelectedModel(models[0]));
    }
    if (!selectedEmbedding && embeddings.length > 0) {
      dispatch(setSelectedEmbedding(embeddings[0]));
    }
  }, [selectedModel, selectedEmbedding, models, embeddings, dispatch]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!userQuery.trim()) return;
    
    dispatch(addUserMessage(userQuery));
    
    await dispatch(sendMessage({
      selectedModel,
      selectedEmbedding,
      systemPrompt,
      query: userQuery
    }));
    
    setUserQuery('');
  };

  const handleClearConversation = () => {
    dispatch(clearConversation());
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-settings">
        <div className="settings-row">
          <div className="settings-group">
            <label>LLM Model</label>
            <select 
              className="input-field"
              value={selectedModel} 
              onChange={(e) => dispatch(setSelectedModel(e.target.value))}
            >
              {models.map(model => (
                <option key={model} value={model}>{model}</option>
              ))}
            </select>
          </div>
          
          <div className="settings-group">
            <label>Embedding Model</label>
            <select 
              className="input-field"
              value={selectedEmbedding} 
              onChange={(e) => dispatch(setSelectedEmbedding(e.target.value))}
            >
              {embeddings.map(model => (
                <option key={model} value={model}>{model}</option>
              ))}
            </select>
          </div>
          
          <div className="settings-group settings-actions">
            <button onClick={handleClearConversation} className="button">
              Clear Chat
            </button>
          </div>
        </div>
        
{/*         <div className="system-prompt-container">
          <div className="system-prompt-header">
            <h3>System Prompt</h3>
            <button 
              onClick={() => setIsEditingPrompt(!isEditingPrompt)}
              className="edit-button"
            >
              {isEditingPrompt ? 'Cancel' : 'Edit'}
            </button>
          </div>
          
          {isEditingPrompt ? (
            <div className="system-prompt-editor">
              <textarea
                value={systemPrompt}
                onChange={(e) => setSystemPrompt(e.target.value)}
                rows={5}
                placeholder="Enter system prompt here..."
              />
              <button onClick={handleSystemPromptSave} className="save-button">
                Save
              </button>
            </div>
          ) : (
            <div className="system-prompt-display">
              {systemPrompt}
            </div>
          )}
        </div> */}
      </div>
      
      <div className="chat-messages">
        {conversation.length === 0 ? (
          <div className="empty-chat">
            <p>No messages yet. Start a conversation by typing a query below.</p>
          </div>
        ) : (
          conversation.map((message, index) => (
            <ChatMessage key={index} message={message} />
          ))
        )}
        
        {isLoading && (
          <div className="loading-message">
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
      </div>
      
      <form className="chat-input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={userQuery}
          onChange={(e) => setUserQuery(e.target.value)}
          placeholder="Type your query here..."
          disabled={isLoading}
        />
        <button className='button' type="submit" disabled={!userQuery.trim() || isLoading}>
          Send
        </button>
      </form>
    </div>
  );
}

export default ChatbotTab;
