import React from 'react';
import { X } from 'lucide-react';

export default function OecdPrinciplesAlignmentModal({ isOpen, onClose, questionCode, questionText, alignmentData }) {
  if (!isOpen || !alignmentData) return null;

  const { alignmentType, confidenceLevel, alignmentRationale, framework_citations } = alignmentData;

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
              <h2 className="text-xl font-semibold">
                OECD Principles (2019) Alignment Information
              </h2>
              <p className="text-sm text-slate-100 mt-1">
                {questionCode}: {questionText}
              </p>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:bg-slate-700 rounded-lg p-2 transition-colors flex-shrink-0"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto flex-1">
          {/* Alignment Type & Confidence Level - Side by side */}
          <div className="grid grid-cols-2 gap-6 mb-6">
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
            <div>
              <h3 className="text-sm font-semibold text-gray-700 mb-3">OECD AI Principles Citation(s)</h3>
              <div className="bg-gray-50 p-4 rounded-lg border-l-4 border-slate-500">
                <p className="text-sm text-gray-700 italic leading-relaxed">
                  {framework_citations}
                </p>
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
