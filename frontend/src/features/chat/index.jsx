import { useState, useEffect } from 'react';
import { useAppDispatch } from '../../hooks/useAppDispatch';
import { useAppSelector } from '../../hooks/useAppSelector';
import Select from 'react-select';
import {
  sendMessage,
  setSelectedModel,
  addUserMessage,
  clearConversation,
} from '../../store/slices/chatSlice';
import { DEFAULT_MODELS, customSelectTheme } from '../../constants';
import { Dot } from 'lucide-react';
import { fetchCurrentVectorDB } from '../../store/slices/vectordbSlice';
import ChatMessage from './components/ChatMessage';

function ChatbotTab() {
  const dispatch = useAppDispatch();
  const { conversation, selectedModel, systemPrompt, isLoading } =
    useAppSelector((state) => state.chat);

  const availableModels = useAppSelector(
    (state) => state.config.config.LLM_MODELS || []
  );
  const models = availableModels.length ? availableModels : DEFAULT_MODELS;
  const currentVectorDB = useAppSelector(
    (state) => state.vectorDBs.currentVectorDB
  );

  const [userQuery, setUserQuery] = useState('');

  useEffect(() => {
    dispatch(fetchCurrentVectorDB());
  }, [dispatch]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!userQuery.trim()) return;

    dispatch(addUserMessage(userQuery));

    await dispatch(
      sendMessage({
        selectedModel,
        systemPrompt,
        query: userQuery,
      })
    );

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
          <Dot color="#10b981" strokeWidth={3}></Dot>
          {currentVectorDB}
        </span>
      </div>
      <div className="chatbot-settings">
        <div className="settings-row">
          <div className="settings-group">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              LLM Model
            </label>
            <Select
              theme={customSelectTheme}
              value={{ value: selectedModel, label: selectedModel }}
              onChange={(option) => dispatch(setSelectedModel(option.value))}
              options={models.map((model) => ({ value: model, label: model }))}
            />
          </div>

          <div className="settings-group settings-actions">
            <button onClick={handleClearConversation} className="button">
              Clear Chat
            </button>
          </div>
        </div>
      </div>

      <div className="chat-messages">
        {conversation.length === 0 ? (
          <div className="empty-chat">
            <p>
              No messages yet. Start a conversation by typing a query below.
            </p>
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
        <button
          className="button"
          type="submit"
          disabled={!userQuery.trim() || isLoading}
        >
          Send
        </button>
      </form>
    </div>
  );
}

export default ChatbotTab;
