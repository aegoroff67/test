import React from 'react';
import { X } from 'lucide-react';

export default function AuGuidanceAlignmentModal({ isOpen, onClose, questionCode, alignmentData }) {
  if (!isOpen || !alignmentData) return null;

  const { alignmentType, confidenceLevel, alignmentRationale, citation } = alignmentData;

  // Function to get confidence level color
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
        {/* Header - Blue theme for AU Guidance */}
        <div className="bg-blue-600 text-white p-6">
          <div className="flex justify-between items-start">
            <div>
              <h2 className="text-xl font-semibold">
                Australian Government – Guidance for AI Adoption (2025) Alignment Information
              </h2>
              <p className="text-sm text-blue-100 mt-1">
                Question {questionCode}
              </p>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:bg-blue-700 rounded-lg p-2 transition-colors"
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
                  ? 'bg-blue-100 text-blue-800 border-blue-300'
                  : 'bg-sky-100 text-sky-800 border-sky-300'
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
            <div className="bg-sky-50 p-4 rounded-lg border border-sky-200">
              <p className="text-sm text-gray-800 leading-relaxed">
                {alignmentRationale}
              </p>
            </div>
          </div>

          {/* Citation */}
          {citation && (
            <div>
              <h3 className="text-sm font-semibold text-gray-700 mb-3">Australian Government – Guidance for AI Adoption Citation(s)</h3>
              <div className="bg-gray-50 p-4 rounded-lg border-l-4 border-blue-500">
                <p className="text-sm text-gray-700 italic leading-relaxed">
                  {citation}
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
