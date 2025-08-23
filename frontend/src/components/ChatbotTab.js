import React, { useState } from 'react';
import ChatMessage from './ChatMessage';

function ChatbotTab({ availableModels = [], embeddingModels = [] }) {
  // Default models if none provided
  const defaultModels = ['gpt-4', 'gpt-3.5-turbo', 'claude-2']; 
  const defaultEmbeddings = ['text-embedding-ada-002', 'text-embedding-3-small'];
  
  const models = availableModels.length ? availableModels : defaultModels;
  const embeddings = embeddingModels.length ? embeddingModels : defaultEmbeddings;
  
  const [selectedModel, setSelectedModel] = useState(models[0] || '');
  const [selectedEmbedding, setSelectedEmbedding] = useState(embeddings[0] || '');
  const [systemPrompt, setSystemPrompt] = useState(
"You are a helpful assistant specializing in document analysis. Answer questions strictly based on the provided context and DO NOT use any external knowledge. Do not assume or infer information that is not explicitly stated in the context. If the context does not contain enough information, clearly state that you cannot provide an answer based on the available context. Always cite your sources by referencing the exact page numbers using this format: <a href='yourfile.pdf#page=PAGENUMBER' target='_blank'>Sayfa PAGENUMBER</a>. When multiple references exist across different pages, summarize the collective information before providing your answer. Structure your responses with bullet points, numbered lists, or short paragraphs as appropriate to the question. Communicate exclusively in Turkish, using formal and grammatically correct language unless the user's tone suggests informality is appropriate. Remember that the context is formatted as: Page Number: [page number]: [content of that page]."
  );
  const [isEditingPrompt, setIsEditingPrompt] = useState(false);
  const [userQuery, setUserQuery] = useState('');
  const [conversation, setConversation] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!userQuery.trim()) return;
    
    // Add user message to conversation
    const userMessage = {
      role: 'user',
      content: userQuery
    };
    
    setConversation(prev => [...prev, userMessage]);
    setIsLoading(true);
    
    try {
      // Send POST request to FastAPI endpoint
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          llm: selectedModel,
          embedding_model: selectedEmbedding,
          system_message: systemPrompt,
          query: userQuery
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      // Assuming the FastAPI returns a JSON object with role and content
      const result = await response.json();
      
      setConversation(prev => [...prev, result]);
      setUserQuery('');
    } catch (error) {
      console.error('Error querying LLM:', error);
      // Add error message to conversation
      setConversation(prev => [
        ...prev, 
        { 
          role: 'system', 
          content: 'Error: Failed to get response from the model. Please try again.'
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSystemPromptSave = () => {
    setIsEditingPrompt(false);
  };

  const clearConversation = () => {
    setConversation([]);
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-settings">
        <div className="settings-row">
          <div className="settings-group">
            <label>LLM Model</label>
            <select 
              value={selectedModel} 
              onChange={(e) => setSelectedModel(e.target.value)}
            >
              {models.map(model => (
                <option key={model} value={model}>{model}</option>
              ))}
            </select>
          </div>
          
          <div className="settings-group">
            <label>Embedding Model</label>
            <select 
              value={selectedEmbedding} 
              onChange={(e) => setSelectedEmbedding(e.target.value)}
            >
              {embeddings.map(model => (
                <option key={model} value={model}>{model}</option>
              ))}
            </select>
          </div>
          
          <div className="settings-group settings-actions">
            <button onClick={clearConversation} className="clear-button">
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
        <button type="submit" disabled={!userQuery.trim() || isLoading}>
          Send
        </button>
      </form>
    </div>
  );
}

export default ChatbotTab;
