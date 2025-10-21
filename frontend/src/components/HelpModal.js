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
                    {content.split('\n\n').map((paragraph, index) => {
                      // Handle bold headings
                      if (paragraph.startsWith('**') && paragraph.endsWith('**')) {
                        return (
                          <h4 key={index} className="font-semibold text-gray-900 text-base mt-4 mb-2">
                            {paragraph.replace(/\*\*/g, '')}
                          </h4>
                        );
                      }
                      
                      // Handle bullet points (both root and sub-bullets)
                      if (paragraph.includes('•') || paragraph.includes('- **') || paragraph.match(/^\s+- /m)) {
                        const lines = paragraph.split('\n').filter(line => line.trim());
                        return (
                          <ul key={index} className="list-none pl-0 space-y-2">
                            {lines.map((line, lineIndex) => {
                              const trimmed = line.trim();
                              // Check if it's a sub-bullet (starts with whitespace + dash)
                              const isSubBullet = line.match(/^\s{2,}-\s/);
                              
                              // Remove bullet character or dash from the start
                              // Use negative lookbehind to avoid matching dash in middle of words
                              let cleanItem = trimmed;
                              if (trimmed.startsWith('•')) {
                                cleanItem = trimmed.substring(1).trim();
                              } else if (trimmed.startsWith('-')) {
                                cleanItem = trimmed.substring(1).trim();
                              }
                              
                              // Parse bold sections and italic sections
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
                                <li 
                                  key={lineIndex} 
                                  className={`text-sm flex ${isSubBullet ? 'ml-6' : 'ml-0'}`}
                                >
                                  <span className="mr-2 flex-shrink-0">{isSubBullet ? '◦' : '•'}</span>
                                  <span className="flex-1">{renderText(cleanItem)}</span>
                                </li>
                              );
                            })}
                          </ul>
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
