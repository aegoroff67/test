import React from 'react';
import { X } from 'lucide-react';

/**
 * Modal component to display NIST AI RMF alignment information
 */
export default function NistAlignmentModal({ isOpen, onClose, questionCode, alignmentData }) {
  if (!isOpen || !alignmentData) return null;

  const { alignmentType, function: nistFunction, categorySubcategory, reasoning, citations, confidenceLevel } = alignmentData;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="bg-indigo-600 text-white px-6 py-4 flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold">
              NIST AI RMF Alignment Information
            </h2>
            <p className="text-sm text-indigo-100 mt-1">
              Question {questionCode}
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-white hover:bg-indigo-700 rounded-full p-2 transition-colors"
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
              <h3 className="text-sm font-semibold text-gray-700 mb-2">Alignment Level</h3>
              <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border ${
                alignmentType === 'Fully Aligns' 
                  ? 'bg-indigo-100 text-indigo-800 border-indigo-300' 
                  : 'bg-purple-100 text-purple-800 border-purple-300'
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

          {/* NIST AI RMF Function */}
          <div className="mb-6">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">NIST AI RMF Function</h3>
            <div className="bg-indigo-50 p-4 rounded-lg border border-indigo-200">
              <p className="text-sm text-gray-800 font-medium">
                {nistFunction}
              </p>
            </div>
          </div>

          {/* Category / Subcategory */}
          <div className="mb-6">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">Relevant Category / Subcategory</h3>
            <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
              <p className="text-sm text-gray-700 font-medium">
                {categorySubcategory}
              </p>
            </div>
          </div>

          {/* Alignment Details / Rationale */}
          <div className="mb-6">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">
              Alignment Details / Rationale
            </h3>
            <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
              <p className="text-sm text-gray-800 leading-relaxed whitespace-pre-line">
                {reasoning}
              </p>
            </div>
          </div>

          {/* Citations */}
          {citations && citations.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-gray-700 mb-3">
                NIST AI RMF Citations
              </h3>
              <div className="space-y-3">
                {citations.map((citation, index) => (
                  <div key={index} className="bg-gray-50 p-4 rounded-lg border-l-4 border-indigo-500">
                    <p className="text-sm text-gray-700 leading-relaxed">
                      {citation}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="bg-gray-50 px-6 py-4 border-t border-gray-200 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition-colors font-medium"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
