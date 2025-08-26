import { useState, useEffect } from 'react';
import { useAppDispatch } from '../../../hooks/useAppDispatch';
import { useAppSelector } from '../../../hooks/useAppSelector';
import Select from 'react-select';
import {
  sendMessage,
  setSelectedModel,
  setSelectedEmbedding,
  addUserMessage,
  clearConversation
} from '../../../store/slices/chatSlice';
import { DEFAULT_MODELS, DEFAULT_EMBEDDINGS, customSelectTheme } from '../../../constants';
import ChatMessage from '../../../components/ui/ChatMessage';
import { Dot } from 'lucide-react';

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
      <div className="card-header rounded-t-[8px] h-[60px]">
        <span>SGK Agent</span>
        <span className="model-badge flex align-middle justify-center items-center">
          <Dot color='#10b981' strokeWidth={3}></Dot>
          Online
        </span>
      </div>
      <div className="chatbot-settings">
        <div className="settings-row">
          <div className="settings-group">
            <label className="block text-sm font-medium text-gray-700 mb-2">LLM Model</label>
            <Select theme={customSelectTheme} value={{ value: selectedModel, label: selectedModel }} onChange={option => dispatch(setSelectedModel(option.value))} options={models.map(model => ({ value: model, label: model }))} />
          </div>

          <div className="settings-group">
            <label className="block text-sm font-medium text-gray-700 mb-2">Embedding Model</label>
            <Select theme={customSelectTheme} value={{ value: selectedEmbedding, label: selectedEmbedding }} onChange={option => dispatch(setSelectedEmbedding(option.value))} options={embeddings.map(model => ({ value: model, label: model }))} />
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
    </div >
  );
}

export default ChatbotTab;
