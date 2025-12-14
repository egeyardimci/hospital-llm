import { useDispatch } from 'react-redux';
import { openDocumentModal } from '../../../store/slices/documentSlice';

function ChatMessage({ message }) {
  const dispatch = useDispatch();
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

  // Parse content and make bracketed references clickable
  const renderContentWithLinks = (text) => {
    if (!text) return null;

    // Match patterns like [1.8 > 1.8.5 - Title] or [1.8.5 - Title]
    const bracketRegex = /\[([^\]]+)\]/g;
    const parts = [];
    let lastIndex = 0;
    let match;

    while ((match = bracketRegex.exec(text)) !== null) {
      // Add text before the match
      if (match.index > lastIndex) {
        parts.push(
          <span
            key={`text-${lastIndex}`}
            dangerouslySetInnerHTML={{ __html: text.slice(lastIndex, match.index) }}
          />
        );
      }

      const bracketContent = match[1];
      // Extract section ID - look for patterns like "1.8.5" (the most specific/last one)
      const sectionIdMatch = bracketContent.match(/(\d+(?:\.\d+)+(?:\.[A-Z])?)/g);
      const sectionId = sectionIdMatch ? sectionIdMatch[sectionIdMatch.length - 1] : null;

      if (sectionId) {
        parts.push(
          <span
            key={`link-${match.index}`}
            onClick={() => dispatch(openDocumentModal(sectionId))}
            style={{
              color: '#002776',
              backgroundColor: '#e3f2fd',
              padding: '2px 6px',
              borderRadius: '4px',
              cursor: 'pointer',
              fontWeight: '500',
              transition: 'all 0.2s ease',
            }}
            onMouseEnter={(e) => {
              e.target.style.backgroundColor = '#bbdefb';
              e.target.style.textDecoration = 'underline';
            }}
            onMouseLeave={(e) => {
              e.target.style.backgroundColor = '#e3f2fd';
              e.target.style.textDecoration = 'none';
            }}
            title={`Click to view section ${sectionId}`}
          >
            [{bracketContent}]
          </span>
        );
      } else {
        parts.push(`[${bracketContent}]`);
      }

      lastIndex = match.index + match[0].length;
    }

    // Add remaining text
    if (lastIndex < text.length) {
      parts.push(
        <span
          key={`text-${lastIndex}`}
          dangerouslySetInnerHTML={{ __html: text.slice(lastIndex) }}
        />
      );
    }

    return parts.length > 0 ? parts : <span dangerouslySetInnerHTML={{ __html: text }} />;
  };

  return (
    <div className={`chat-message ${messageClass}`}>
      <div className="message-avatar">{avatarLabel}</div>
      <div className="message-content">
        {renderContentWithLinks(content)}
      </div>
    </div>
  );
}

export default ChatMessage;
