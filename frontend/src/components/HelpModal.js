import React from 'react';
import { X } from 'lucide-react';

export default function HelpModal({ isOpen, onClose, title, content }) {
  if (!isOpen) return null;

  return (
    <>
      {/* Backdrop */}
      <div 
        className="fixed inset-0 bg-black bg-opacity-50 z-50 transition-opacity"
        onClick={onClose}
      />
      
      {/* Modal */}
      <div className="fixed inset-0 z-50 overflow-y-auto">
        <div className="flex min-h-full items-center justify-center p-4">
          <div 
            className="relative bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[80vh] overflow-hidden"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Header */}
            <div className="flex items-center justify-between p-4 border-b border-gray-200 bg-blue-50">
              <h3 className="text-lg font-semibold text-gray-900">
                {title}
              </h3>
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-gray-600 transition-colors"
                aria-label="Close"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
            
            {/* Content */}
            <div className="p-6 overflow-y-auto max-h-[calc(80vh-80px)]">
              <div className="prose prose-sm max-w-none">
                {content ? (
                  <div className="text-gray-700 leading-relaxed space-y-4">
                    {/* Remove trailing --- separator before processing */}
                    {content.replace(/\n---$/, '').split('\n\n').map((paragraph, index) => {
                      // Skip separator lines
                      if (paragraph.trim() === '---' || paragraph.trim() === '**---**') {
                        return null;
                      }
                      
                      // Handle bold headings (starts and ends with **)
                      // But NOT if it contains a colon (like "Key evidence types:")
                      if (paragraph.startsWith('**') && paragraph.endsWith('**') && !paragraph.includes(':')) {
                        return (
                          <h4 key={index} className="font-semibold text-gray-900 text-base mt-4 mb-2">
                            {paragraph.replace(/\*\*/g, '')}
                          </h4>
                        );
                      }
                      
                      // Check if paragraph contains bullet points
                      const hasBullets = paragraph.includes('•') || paragraph.includes('- **') || paragraph.match(/^\s*- /m);
                      
                      if (hasBullets) {
                        const lines = paragraph.split('\n');
                        const processedItems = [];
                        let textBeforeBullets = [];
                        let textAfterBullets = [];
                        let i = 0;
                        
                        // First, find where bullets start and end
                        let firstBulletIndex = -1;
                        let lastBulletIndex = -1;
                        
                        for (let j = 0; j < lines.length; j++) {
                          const line = lines[j];
                          const trimmed = line.trim();
                          const isSubBullet = line.match(/^  - /);
                          const isRootBullet = !isSubBullet && (trimmed.startsWith('•') || trimmed.startsWith('- '));
                          
                          if (isRootBullet || isSubBullet) {
                            if (firstBulletIndex === -1) firstBulletIndex = j;
                            lastBulletIndex = j;
                          } else if (line.match(/^    /) && lastBulletIndex > -1) {
                            // Continuation line of a sub-bullet
                            lastBulletIndex = j;
                          } else if (line.match(/^  /) && !isSubBullet && lastBulletIndex > -1 && j === lastBulletIndex + 1) {
                            // Continuation line of a root bullet
                            lastBulletIndex = j;
                          }
                        }
                        
                        // Now process with proper section detection
                        i = 0;
                        while (i < lines.length) {
                          const line = lines[i];
                          const trimmed = line.trim();
                          
                          if (!trimmed) {
                            i++;
                            continue;
                          }
                          
                          // Determine which section this line belongs to
                          if (firstBulletIndex === -1 || i < firstBulletIndex) {
                            // Before bullets
                            textBeforeBullets.push(trimmed);
                            i++;
                          } else if (i > lastBulletIndex) {
                            // After bullets
                            textAfterBullets.push(trimmed);
                            i++;
                          } else {
                            // Within bullet section - process bullets
                            const isSubBullet = line.match(/^  - /);
                            const isRootBullet = !isSubBullet && (trimmed.startsWith('•') || trimmed.startsWith('- '));
                            
                            if (isSubBullet) {
                              const cleanItem = line.substring(4);
                              let fullText = cleanItem;
                              
                              let j = i + 1;
                              while (j < lines.length && lines[j].match(/^    /)) {
                                fullText += ' ' + lines[j].trim();
                                j++;
                              }
                              
                              processedItems.push({ type: 'sub', text: fullText });
                              i = j;
                            }
                            else if (isRootBullet) {
                              const cleanItem = trimmed.startsWith('•') 
                                ? trimmed.substring(1).trim() 
                                : trimmed.substring(2).trim();
                              let fullText = cleanItem;
                              
                              let j = i + 1;
                              while (j < lines.length) {
                                const nextLine = lines[j];
                                const nextTrimmed = nextLine.trim();
                                
                                // Continuation: starts with 2 spaces but not a sub-bullet
                                if (nextLine.match(/^  /) && !nextLine.match(/^  - /) && nextTrimmed) {
                                  fullText += ' ' + nextTrimmed;
                                  j++;
                                } else {
                                  break;
                                }
                              }
                              
                              processedItems.push({ type: 'root', text: fullText });
                              i = j;
                            }
                            else {
                              i++;
                            }
                          }
                        }
                        
                        // Render text with bold/italic support
                        const renderText = (text) => {
                          const parts = text.split(/(\*\*.*?\*\*|\*.*?\*)/g);
                          return parts.map((part, partIndex) => {
                            if (part.startsWith('**') && part.endsWith('**')) {
                              return (
                                <strong key={partIndex} className="font-semibold text-gray-900">
                                  {part.replace(/\*\*/g, '')}
                                </strong>
                              );
                            } else if (part.startsWith('*') && part.endsWith('*') && !part.startsWith('**')) {
                              return (
                                <em key={partIndex} className="italic">
                                  {part.replace(/\*/g, '')}
                                </em>
                              );
                            }
                            return <span key={partIndex}>{part}</span>;
                          });
                        };
                        
                        return (
                          <div key={index}>
                            {/* Text before bullets */}
                            {textBeforeBullets.length > 0 && (
                              (() => {
                                // Check if the last line is a label (ends with colon)
                                const lastLine = textBeforeBullets[textBeforeBullets.length - 1];
                                const isLastLineLabel = lastLine.trim().endsWith(':');
                                
                                if (isLastLineLabel && textBeforeBullets.length > 1) {
                                  // We have both intro text AND a label
                                  const introText = textBeforeBullets.slice(0, -1).join(' ');
                                  const labelText = lastLine;
                                  
                                  return (
                                    <>
                                      <p className="text-sm leading-relaxed mb-3">
                                        {renderText(introText)}
                                      </p>
                                      <p className="text-sm font-semibold leading-relaxed mb-2">
                                        {renderText(labelText)}
                                      </p>
                                    </>
                                  );
                                } else if (isLastLineLabel) {
                                  // Only a label, no intro text
                                  return (
                                    <p className="text-sm font-semibold leading-relaxed mb-2">
                                      {renderText(lastLine)}
                                    </p>
                                  );
                                } else {
                                  // No label, just regular text
                                  return (
                                    <p className="text-sm leading-relaxed mb-3">
                                      {renderText(textBeforeBullets.join(' '))}
                                    </p>
                                  );
                                }
                              })()
                            )}
                            
                            {/* Bullet list */}
                            {processedItems.length > 0 && (
                              <ul className="list-none pl-0 space-y-2 mb-3">
                                {processedItems.map((item, itemIndex) => (
                                  <li 
                                    key={itemIndex} 
                                    className={`text-sm flex ${item.type === 'sub' ? 'ml-6' : 'ml-0'}`}
                                  >
                                    <span className="mr-2 flex-shrink-0">{item.type === 'sub' ? '◦' : '•'}</span>
                                    <span className="flex-1">{renderText(item.text)}</span>
                                  </li>
                                ))}
                              </ul>
                            )}
                            
                            {/* Text after bullets */}
                            {textAfterBullets.length > 0 && (
                              <p className="text-sm leading-relaxed">
                                {renderText(textAfterBullets.join(' '))}
                              </p>
                            )}
                          </div>
                        );
                      }
                      
                      // Handle regular paragraphs with inline bold and italic
                      const renderText = (text) => {
                        const parts = text.split(/(\*\*.*?\*\*|\*.*?\*)/g);
                        return parts.map((part, partIndex) => {
                          if (part.startsWith('**') && part.endsWith('**')) {
                            return (
                              <strong key={partIndex} className="font-semibold text-gray-900">
                                {part.replace(/\*\*/g, '')}
                              </strong>
                            );
                          } else if (part.startsWith('*') && part.endsWith('*') && !part.startsWith('**')) {
                            return (
                              <em key={partIndex} className="italic">
                                {part.replace(/\*/g, '')}
                              </em>
                            );
                          }
                          return <span key={partIndex}>{part}</span>;
                        });
                      };
                      
                      return (
                        <p key={index} className="text-sm leading-relaxed">
                          {renderText(paragraph)}
                        </p>
                      );
                    })}
                  </div>
                ) : (
                  <p className="text-gray-500 text-sm">No help content available for this question.</p>
                )}
              </div>
            </div>
            
            {/* Footer */}
            <div className="flex justify-end p-4 border-t border-gray-200 bg-gray-50">
              <button
                onClick={onClose}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
