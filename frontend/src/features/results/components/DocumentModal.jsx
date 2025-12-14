import { useEffect, useRef } from 'react';
import { useAppSelector } from '../../../hooks/useAppSelector';
import { useDispatch } from 'react-redux';
import { closeDocumentModal, fetchDocument } from '../../../store/slices/documentSlice';

function DocumentModal() {
  const dispatch = useDispatch();
  const { document, isLoading, error, modalOpen, focusSectionId } = useAppSelector(
    (state) => state.document
  );
  const focusRef = useRef(null);
  const modalRef = useRef(null);

  useEffect(() => {
    if (modalOpen && !document && !isLoading) {
      dispatch(fetchDocument());
    }
  }, [modalOpen, document, isLoading, dispatch]);

  useEffect(() => {
    if (modalOpen && focusRef.current) {
      setTimeout(() => {
        focusRef.current?.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }, 100);
    }
  }, [modalOpen, focusSectionId, document]);

  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') {
        dispatch(closeDocumentModal());
      }
    };
    if (modalOpen) {
      window.addEventListener('keydown', handleEscape);
    }
    return () => window.removeEventListener('keydown', handleEscape);
  }, [modalOpen, dispatch]);

  if (!modalOpen) return null;

  const handleOverlayClick = (e) => {
    if (e.target === modalRef.current) {
      dispatch(closeDocumentModal());
    }
  };

  // Render sub-items within an item
  const renderSubItems = (subItems) => {
    if (!subItems || subItems.length === 0) return null;
    return (
      <div
        style={{
          marginTop: '8px',
          paddingLeft: '16px',
          borderLeft: '2px solid #ffc107',
        }}
      >
        {subItems.map((subItem, idx) => (
          <div
            key={idx}
            style={{
              backgroundColor: 'rgba(255, 193, 7, 0.1)',
              padding: '8px 10px',
              borderRadius: '4px',
              marginBottom: '4px',
            }}
          >
            {subItem.id && (
              <span
                style={{
                  backgroundColor: 'rgba(255, 193, 7, 0.3)',
                  padding: '2px 6px',
                  borderRadius: '3px',
                  fontSize: '0.75em',
                  fontWeight: '600',
                  color: '#e65100',
                  marginRight: '8px',
                }}
              >
                {subItem.id}
              </span>
            )}
            <span style={{ fontSize: '0.85em', color: '#555', lineHeight: '1.5' }}>
              {subItem.content}
            </span>
          </div>
        ))}
      </div>
    );
  };

  // Render items within a paragraph
  const renderParagraphItems = (items) => {
    if (!items || items.length === 0) return null;
    return (
      <div
        style={{
          marginTop: '10px',
          paddingLeft: '14px',
          borderLeft: '2px solid #8bc34a',
        }}
      >
        {items.map((item, idx) => (
          <div
            key={idx}
            style={{
              backgroundColor: 'rgba(139, 195, 74, 0.1)',
              padding: '10px 12px',
              borderRadius: '6px',
              marginBottom: '6px',
            }}
          >
            {item.id && (
              <div style={{ marginBottom: '6px' }}>
                <span
                  style={{
                    backgroundColor: 'rgba(139, 195, 74, 0.3)',
                    padding: '2px 8px',
                    borderRadius: '4px',
                    fontSize: '0.8em',
                    fontWeight: '600',
                    color: '#558b2f',
                  }}
                >
                  {item.id}
                </span>
              </div>
            )}
            {item.content && (
              <div style={{ fontSize: '0.9em', color: '#444', lineHeight: '1.6' }}>
                {item.content}
              </div>
            )}
            {renderSubItems(item.sub_items)}
          </div>
        ))}
      </div>
    );
  };

  // Render paragraphs within a section
  const renderParagraphs = (paragraphs) => {
    if (!paragraphs || paragraphs.length === 0) return null;
    return (
      <div style={{ marginTop: '10px' }}>
        {paragraphs.map((para, idx) => (
          <div
            key={idx}
            style={{
              backgroundColor: '#fff',
              padding: '12px 14px',
              borderRadius: '6px',
              marginBottom: '10px',
              border: '1px solid #e0e0e0',
              borderLeft: '3px solid #00bcd4',
            }}
          >
            {para.id && (
              <div style={{ marginBottom: '8px' }}>
                <span
                  style={{
                    backgroundColor: 'rgba(0, 188, 212, 0.2)',
                    padding: '2px 8px',
                    borderRadius: '4px',
                    fontSize: '0.75em',
                    color: '#00838f',
                  }}
                >
                  Paragraph {para.id}
                </span>
              </div>
            )}
            {para.content && (
              <div style={{ lineHeight: '1.7', color: '#333' }}>{para.content}</div>
            )}
            {renderParagraphItems(para.items)}
          </div>
        ))}
      </div>
    );
  };

  // Render section-level items (simple string array)
  const renderSectionItems = (items) => {
    if (!items || items.length === 0) return null;
    return (
      <div
        style={{
          marginTop: '10px',
          padding: '12px',
          backgroundColor: 'rgba(76, 175, 80, 0.08)',
          borderRadius: '6px',
          borderLeft: '3px solid #4caf50',
        }}
      >
        {items.map((item, idx) => (
          <div
            key={idx}
            style={{
              display: 'flex',
              gap: '8px',
              padding: '6px 0',
              fontSize: '0.9em',
              lineHeight: '1.6',
            }}
          >
            <span style={{ color: '#4caf50', fontWeight: '600', flexShrink: 0 }}>
              {idx + 1})
            </span>
            <span style={{ color: '#444' }}>{item}</span>
          </div>
        ))}
      </div>
    );
  };

  // Render section content (direct content field)
  const renderSectionContent = (content) => {
    if (!content) return null;
    return (
      <div
        style={{
          marginTop: '10px',
          padding: '12px',
          backgroundColor: 'rgba(156, 39, 176, 0.08)',
          borderRadius: '6px',
          borderLeft: '3px solid #9c27b0',
          fontSize: '0.95em',
          color: '#333',
          lineHeight: '1.7',
        }}
      >
        {content}
      </div>
    );
  };

  const renderSection = (section, depth = 0) => {
    const isFocused = section.id === focusSectionId;
    const paddingLeft = depth * 20;

    const hasContent = section.content && section.content.trim();
    const hasParagraphs = section.paragraphs && section.paragraphs.length > 0;
    const hasItems = section.items && section.items.length > 0;
    const hasAmendments = section.amendments && section.amendments.length > 0;
    const hasSubsections = section.subsections && section.subsections.length > 0;

    return (
      <div
        key={section.id}
        ref={isFocused ? focusRef : null}
        style={{
          marginBottom: '16px',
          paddingLeft: `${paddingLeft}px`,
          borderLeft: depth > 0 ? '2px solid #e0e0e0' : 'none',
        }}
      >
        <div
          style={{
            backgroundColor: isFocused ? '#fff3cd' : depth === 0 ? '#f8f9fa' : 'transparent',
            border: isFocused ? '2px solid #ffc107' : 'none',
            borderRadius: '8px',
            padding: '12px',
            transition: 'all 0.3s ease',
          }}
        >
          {/* Section Header */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '10px',
              marginBottom: hasContent || hasParagraphs || hasItems || hasAmendments ? '10px' : '0',
              flexWrap: 'wrap',
            }}
          >
            <span
              style={{
                backgroundColor: '#002776',
                color: 'white',
                padding: '4px 10px',
                borderRadius: '4px',
                fontSize: '0.85em',
                fontWeight: 'bold',
              }}
            >
              {section.id}
            </span>
            <span style={{ fontWeight: 'bold', color: '#333' }}>{section.title}</span>

            {/* Meta badges */}
            <div style={{ display: 'flex', gap: '6px', marginLeft: 'auto', flexWrap: 'wrap' }}>
              {hasParagraphs && (
                <span
                  style={{
                    backgroundColor: 'rgba(0, 188, 212, 0.2)',
                    color: '#00838f',
                    padding: '2px 8px',
                    borderRadius: '10px',
                    fontSize: '0.7em',
                    fontWeight: '500',
                  }}
                >
                  {section.paragraphs.length} paragraphs
                </span>
              )}
              {hasItems && (
                <span
                  style={{
                    backgroundColor: 'rgba(76, 175, 80, 0.2)',
                    color: '#388e3c',
                    padding: '2px 8px',
                    borderRadius: '10px',
                    fontSize: '0.7em',
                    fontWeight: '500',
                  }}
                >
                  {section.items.length} items
                </span>
              )}
              {hasSubsections && (
                <span
                  style={{
                    backgroundColor: 'rgba(233, 30, 99, 0.2)',
                    color: '#c2185b',
                    padding: '2px 8px',
                    borderRadius: '10px',
                    fontSize: '0.7em',
                    fontWeight: '500',
                  }}
                >
                  {section.subsections.length} subsections
                </span>
              )}
            </div>
          </div>

          {/* Amendments */}
          {hasAmendments && (
            <div style={{ marginBottom: '10px' }}>
              {section.amendments.map((amendment, idx) => (
                <div
                  key={idx}
                  style={{
                    backgroundColor: 'rgba(255, 152, 0, 0.1)',
                    padding: '6px 10px',
                    borderRadius: '4px',
                    fontSize: '0.8em',
                    color: '#e65100',
                    marginBottom: '4px',
                    borderLeft: '3px solid #ff9800',
                    fontStyle: 'italic',
                  }}
                >
                  {amendment}
                </div>
              ))}
            </div>
          )}

          {/* Section Content (direct) */}
          {renderSectionContent(section.content)}

          {/* Section-level Items (string array) */}
          {renderSectionItems(section.items)}

          {/* Paragraphs with nested items and sub-items */}
          {renderParagraphs(section.paragraphs)}
        </div>

        {/* Subsections */}
        {hasSubsections &&
          section.subsections.map((sub) => renderSection(sub, depth + 1))}
      </div>
    );
  };

  return (
    <div
      ref={modalRef}
      onClick={handleOverlayClick}
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.6)',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        zIndex: 1000,
        padding: '20px',
      }}
    >
      <div
        style={{
          backgroundColor: 'white',
          borderRadius: '12px',
          width: '90%',
          maxWidth: '900px',
          maxHeight: '85vh',
          display: 'flex',
          flexDirection: 'column',
          boxShadow: '0 10px 40px rgba(0, 0, 0, 0.3)',
        }}
      >
        {/* Modal Header */}
        <div
          style={{
            backgroundColor: '#002776',
            color: 'white',
            padding: '16px 20px',
            borderRadius: '12px 12px 0 0',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}
        >
          <div>
            <h2 style={{ margin: 0, fontSize: '1.2em' }}>
              {document?.title || 'Document'}
            </h2>
            {focusSectionId && (
              <span
                style={{
                  backgroundColor: 'rgba(255, 255, 255, 0.2)',
                  padding: '2px 8px',
                  borderRadius: '4px',
                  fontSize: '0.8em',
                  marginTop: '4px',
                  display: 'inline-block',
                }}
              >
                Focused: {focusSectionId}
              </span>
            )}
          </div>
          <button
            onClick={() => dispatch(closeDocumentModal())}
            style={{
              background: 'rgba(255, 255, 255, 0.2)',
              border: 'none',
              color: 'white',
              width: '32px',
              height: '32px',
              borderRadius: '50%',
              cursor: 'pointer',
              fontSize: '1.2em',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            &times;
          </button>
        </div>

        {/* Modal Body */}
        <div
          style={{
            flex: 1,
            overflowY: 'auto',
            padding: '20px',
          }}
        >
          {isLoading && (
            <div style={{ textAlign: 'center', padding: '40px', color: '#7f8c8d' }}>
              Loading document...
            </div>
          )}

          {error && (
            <div
              style={{
                textAlign: 'center',
                padding: '40px',
                color: '#c62828',
                backgroundColor: '#ffebee',
                borderRadius: '8px',
              }}
            >
              Error: {error}
            </div>
          )}

          {document && document.sections && (
            <div>{document.sections.map((section) => renderSection(section))}</div>
          )}
        </div>
      </div>
    </div>
  );
}

export default DocumentModal;
