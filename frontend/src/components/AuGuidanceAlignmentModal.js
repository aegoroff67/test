import React from 'react';
import { X } from 'lucide-react';

/**
 * Modal component to display Australian Guidance for AI Adoption alignment information
 */
export default function AuGuidanceAlignmentModal({ isOpen, onClose, questionCode, alignmentData }) {
  if (!isOpen || !alignmentData) return null;

  const { alignmentType, relevantGuidance, alignmentRationale, confidenceLevel } = alignmentData;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="bg-gradient-to-r from-orange-500 to-teal-500 text-white px-6 py-4 flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold">
              Australian Government – Guidance for AI Adoption
            </h2>
            <p className="text-sm text-orange-100 mt-1">
              Question {questionCode}
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-white hover:bg-orange-600 hover:bg-opacity-30 rounded-full p-2 transition-colors"
            aria-label="Close modal"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto flex-1">
          {/* Alignment Type and Confidence Level */}
          <div className="mb-6 flex items-center justify-between flex-wrap gap-4">
            <div>
              <h3 className="text-sm font-semibold text-gray-700 mb-2">Alignment Type</h3>
              <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border ${
                alignmentType === 'Fully Aligns' 
                  ? 'bg-orange-100 text-orange-800 border-orange-300' 
                  : 'bg-teal-100 text-teal-800 border-teal-300'
              }`}>
                {alignmentType}
              </div>
            </div>
            {confidenceLevel && (
              <div>
                <h3 className="text-sm font-semibold text-gray-700 mb-2">Confidence Level</h3>
                <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border ${
                  confidenceLevel === 'High' 
                    ? 'bg-emerald-100 text-emerald-800 border-emerald-300' 
                    : 'bg-yellow-100 text-yellow-800 border-yellow-300'
                }`}>
                  {confidenceLevel}
                </div>
              </div>
            )}
          </div>

          {/* Relevant Guidance Reference */}
          <div className="mb-6">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">Relevant Guidance</h3>
            <div className="bg-orange-50 p-4 rounded-lg border border-orange-200">
              <p className="text-sm text-gray-800 font-medium leading-relaxed">
                {relevantGuidance}
              </p>
            </div>
          </div>

          {/* Alignment Rationale */}
          <div className="mb-6">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">
              Alignment Rationale
            </h3>
            <div className="bg-teal-50 p-4 rounded-lg border border-teal-200">
              <p className="text-sm text-gray-800 leading-relaxed">
                {alignmentRationale}
              </p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="bg-gray-50 px-6 py-4 border-t border-gray-200 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gradient-to-r from-orange-500 to-teal-500 text-white rounded-md hover:from-orange-600 hover:to-teal-600 transition-colors font-medium"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
