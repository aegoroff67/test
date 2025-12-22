import React from 'react';
import { X } from 'lucide-react';

/**
 * Modal component to display Australian AI Ethics Principles alignment information
 */
export default function AuEthicsAlignmentModal({ isOpen, onClose, questionCode, questionText, alignmentData }) {
  if (!isOpen || !alignmentData) return null;

  const { alignmentType, overview, relevantPrinciples, alignmentDetails, confidenceLevel, citation } = alignmentData;

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
        <div className="bg-green-600 text-white px-6 py-4 flex items-center justify-between">
          <div className="flex-1 pr-4">
            <h2 className="text-xl font-semibold">
              Australian AI Ethics Principles Alignment Information
            </h2>
            <p className="text-sm text-green-100 mt-1">
              {questionCode}: {questionText}
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-white hover:bg-green-700 rounded-full p-2 transition-colors flex-shrink-0"
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
                  ? 'bg-green-100 text-green-800 border-green-300' 
                  : 'bg-blue-100 text-blue-800 border-blue-300'
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

          {/* Alignment Details/Rationale - Moved up after Confidence Level */}
          <div className="mb-6">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">
              Alignment Details / Rationale
            </h3>
            <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
              <p className="text-sm text-gray-800 leading-relaxed">
                {alignmentDetails}
              </p>
            </div>
          </div>

          {/* Citation - Moved up after Alignment Details */}
          {citation && (
            <div className="mb-6">
              <h3 className="text-sm font-semibold text-gray-700 mb-3">
                Australian AI Ethics Principles Citation(s)
              </h3>
              <div className="bg-gray-50 p-4 rounded-lg border-l-4 border-green-500">
                <p className="text-sm text-gray-700 italic leading-relaxed">
                  {citation}
                </p>
              </div>
            </div>
          )}

          {/* Overview */}
          {overview && (
            <div className="mb-6">
              <h3 className="text-sm font-semibold text-gray-700 mb-3">
                Alignment Overview
              </h3>
              <div className="bg-green-50 p-4 rounded-lg border border-green-200">
                <p className="text-sm text-gray-800 leading-relaxed">
                  {overview}
                </p>
              </div>
            </div>
          )}

          {/* Relevant Principles */}
          <div>
            <h3 className="text-sm font-semibold text-gray-700 mb-3">Relevant Australian AI Ethics Principles</h3>
            <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
              <p className="text-sm text-gray-700 font-medium">
                {relevantPrinciples}
              </p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="bg-gray-50 px-6 py-4 border-t border-gray-200 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors font-medium"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
