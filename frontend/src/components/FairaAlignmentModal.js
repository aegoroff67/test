import React from 'react';
import { X } from 'lucide-react';

/**
 * Modal component to display FAIRA alignment information for a specific question
 */
export default function FairaAlignmentModal({ isOpen, onClose, questionCode, alignmentData }) {
  if (!isOpen || !alignmentData) return null;

  const { alignmentType, overview, fairaComponent, alignmentDetails, confidenceLevel } = alignmentData;

  return (
    <div 
      className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4"
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div 
        className="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-hidden flex flex-col"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="bg-amber-600 text-white px-6 py-4 flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold">
              FAIRA Alignment Information
            </h2>
            <p className="text-sm text-amber-100 mt-1">
              Question {questionCode}
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-white hover:bg-amber-700 rounded-full p-2 transition-colors"
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
              <div className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-amber-100 text-amber-800 border border-amber-300">
                {alignmentType}
              </div>
            </div>
            {confidenceLevel && (
              <div>
                <h3 className="text-sm font-semibold text-gray-700 mb-2">Confidence Level</h3>
                <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border ${
                  confidenceLevel === 'High' 
                    ? 'bg-green-100 text-green-800 border-green-300' 
                    : 'bg-yellow-100 text-yellow-800 border-yellow-300'
                }`}>
                  {confidenceLevel}
                </div>
              </div>
            )}
          </div>

          {/* FAIRA Alignment Overview */}
          {overview && (
            <div className="mb-6">
              <h3 className="text-sm font-semibold text-gray-700 mb-3">
                FAIRA Alignment Overview
              </h3>
              <div className="bg-amber-50 p-4 rounded-lg border border-amber-200">
                <p className="text-sm text-gray-800 leading-relaxed">
                  {overview}
                </p>
              </div>
            </div>
          )}

          {/* FAIRA Components */}
          <div className="mb-6">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">FAIRA Components</h3>
            
            {/* Part B */}
            <div className="mb-4 bg-gray-50 p-4 rounded-lg border border-gray-200">
              <h4 className="text-sm font-semibold text-amber-700 mb-2">
                Part B — Relevant Values
              </h4>
              <p className="text-sm text-gray-700">
                {fairaComponent.partB}
              </p>
            </div>

            {/* Part C */}
            <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
              <h4 className="text-sm font-semibold text-amber-700 mb-2">
                Part C — Relevant Controls
              </h4>
              <p className="text-sm text-gray-700">
                {fairaComponent.partC}
              </p>
            </div>
          </div>

          {/* Alignment Details/Rationale */}
          <div>
            <h3 className="text-sm font-semibold text-gray-700 mb-3">
              Alignment Details / Rationale
            </h3>
            <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
              <p className="text-sm text-gray-800 leading-relaxed">
                {alignmentDetails}
              </p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="bg-gray-50 px-6 py-4 border-t border-gray-200 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-amber-600 text-white rounded-md hover:bg-amber-700 transition-colors font-medium"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
