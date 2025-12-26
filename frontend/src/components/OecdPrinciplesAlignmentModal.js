import React, { useState } from 'react';
import { X, ChevronRight, ChevronDown } from 'lucide-react';

export default function OecdPrinciplesAlignmentModal({ isOpen, onClose, questionCode, questionText, alignmentData }) {
  const [isExpanded, setIsExpanded] = useState(false);
  
  if (!isOpen || !alignmentData) return null;

  const { alignmentType, confidenceLevel, alignmentRationale, framework_citations, alignedControls } = alignmentData;

  // Function to get confidence level color based on level
  const getConfidenceLevelColor = (level) => {
    if (!level) return 'bg-gray-100 text-gray-800 border-gray-300';
    
    const levelStr = level.toLowerCase();
    if (levelStr.includes('very high') || levelStr.includes('95') || levelStr.includes('98')) {
      return 'bg-emerald-100 text-emerald-800 border-emerald-300';
    } else if (levelStr.includes('high') || levelStr.includes('90')) {
      return 'bg-green-100 text-green-800 border-green-300';
    } else if (levelStr.includes('medium') || (levelStr.includes('80') || levelStr.includes('85') || levelStr.includes('75'))) {
      return 'bg-yellow-100 text-yellow-800 border-yellow-300';
    } else if (levelStr.includes('low') || (levelStr.includes('60') || levelStr.includes('65') || levelStr.includes('70'))) {
      return 'bg-orange-100 text-orange-800 border-orange-300';
    }
    return 'bg-gray-100 text-gray-800 border-gray-300';
  };

  const controlCount = alignedControls?.length || 0;

  return (
    <div 
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div 
        className="bg-white rounded-lg w-full max-w-3xl max-h-[90vh] overflow-hidden flex flex-col"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header - Slate/gray-blue theme for OECD */}
        <div className="bg-slate-600 text-white p-6">
          <div className="flex justify-between items-start">
            <div className="flex-1 pr-4">
              <div className="flex items-center space-x-2 mb-1">
                <span className="text-slate-200 text-sm font-medium">{questionCode}</span>
                <span className="text-slate-300">•</span>
                <span className="text-slate-200 text-sm">OECD Principles on AI (2019)</span>
              </div>
              <h2 className="text-lg font-semibold leading-tight">
                {questionText}
              </h2>
            </div>
            <button
              onClick={onClose}
              className="text-slate-200 hover:text-white transition-colors flex-shrink-0"
            >
              <X className="w-6 h-6" />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto flex-1">
          {/* Alignment Type & Confidence Level - Side by side */}
          <div className="mb-6 flex items-center justify-between flex-wrap gap-4">
            <div>
              <h3 className="text-sm font-semibold text-gray-700 mb-2">Alignment Type</h3>
              <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border ${
                alignmentType === 'Fully Aligns'
                  ? 'bg-slate-100 text-slate-800 border-slate-300'
                  : 'bg-slate-50 text-slate-700 border-slate-200'
              }`}>
                {alignmentType}
              </div>
            </div>

            {confidenceLevel && (
              <div>
                <h3 className="text-sm font-semibold text-gray-700 mb-2">Confidence Level</h3>
                <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border ${getConfidenceLevelColor(confidenceLevel)}`}>
                  {confidenceLevel}
                </div>
              </div>
            )}
          </div>

          {/* Alignment Details / Rationale */}
          <div className="mb-6">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">
              Alignment Details / Rationale
            </h3>
            <div className="bg-slate-50 p-4 rounded-lg border border-slate-200">
              <p className="text-sm text-gray-800 leading-relaxed">
                {alignmentRationale}
              </p>
            </div>
          </div>

          {/* Citation */}
          {framework_citations && (
            <div className="mb-6">
              <h3 className="text-sm font-semibold text-gray-700 mb-3">OECD AI Principles Citation(s)</h3>
              <div className="bg-gray-50 p-4 rounded-lg border-l-4 border-slate-500">
                <p className="text-sm text-gray-700 italic leading-relaxed">
                  {framework_citations}
                </p>
              </div>
            </div>
          )}

          {/* Framework Control Mapping - Expandable */}
          {(alignedControls && alignedControls.length > 0) && (
            <div>
              <h3 className="text-sm font-semibold text-gray-700 mb-3">Framework Control Mapping</h3>
              <div className="border border-gray-200 rounded-lg overflow-hidden">
                {/* Expandable Header */}
                <button
                  onClick={() => setIsExpanded(!isExpanded)}
                  className="w-full flex items-center gap-2 px-4 py-3 bg-gray-50 hover:bg-gray-100 transition-colors text-left"
                >
                  {isExpanded ? (
                    <ChevronDown className="h-4 w-4 text-gray-600" />
                  ) : (
                    <ChevronRight className="h-4 w-4 text-gray-600" />
                  )}
                  <span className="text-sm text-slate-700 font-medium">View mapped controls</span>
                  <span className="text-sm text-gray-500">({controlCount})</span>
                </button>

                {/* Expandable Table */}
                {isExpanded && (
                  <div className="border-t border-gray-200">
                    <table className="w-full text-sm">
                      <thead className="bg-gray-100">
                        <tr>
                          <th className="px-4 py-2 text-left font-semibold text-gray-700 border-b">Framework Control</th>
                          <th className="px-4 py-2 text-left font-semibold text-gray-700 border-b">Alignment</th>
                          <th className="px-4 py-2 text-left font-semibold text-gray-700 border-b">AM AI SAFE Control</th>
                        </tr>
                      </thead>
                      <tbody>
                        {alignedControls.map((control, index) => (
                          <tr key={index} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                            <td className="px-4 py-2 border-b border-gray-100 font-medium text-gray-800">
                              {control.nativeId}
                            </td>
                            <td className="px-4 py-2 border-b border-gray-100">
                              <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                                control.alignmentType === 'full' 
                                  ? 'bg-green-100 text-green-800' 
                                  : 'bg-yellow-100 text-yellow-800'
                              }`}>
                                {control.alignmentType === 'full' ? 'Full' : 'Partial'}
                              </span>
                            </td>
                            <td className="px-4 py-2 border-b border-gray-100 text-gray-700">
                              <span className="font-medium text-slate-700">{control.controlId}</span>
                              {control.description && (
                                <span className="text-gray-500"> - {control.description}</span>
                              )}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Disclaimer */}
          <div className="mt-6 pt-4 border-t border-gray-200">
            <p className="text-xs text-gray-500 leading-relaxed">
              <span className="font-semibold">Disclaimer:</span> Framework alignments are indicative, derived mappings based on AM AI SAFE&apos;s independent interpretation of publicly available guidance. They do not constitute legal advice, regulatory approval, or official framework endorsement.
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="bg-gray-50 px-6 py-4 border-t border-gray-200 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-600 text-white rounded-md hover:bg-slate-700 transition-colors font-medium"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
