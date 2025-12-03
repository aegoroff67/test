import React from 'react';
import { X } from 'lucide-react';

export default function FairaAlignmentModal({ isOpen, onClose, questionCode, alignmentData }) {
  if (!isOpen || !alignmentData) return null;

  const { alignmentType, details } = alignmentData;

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
        {/* Header - Amber theme for FAIRA */}
        <div className="bg-amber-600 text-white p-6">
          <div className="flex justify-between items-start">
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
              className="text-white hover:bg-amber-700 rounded-lg p-2 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto flex-1">
          {/* Alignment Type */}
          <div className="mb-6">
            <h3 className="text-sm font-semibold text-gray-700 mb-2">Alignment Type</h3>
            <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border ${
              alignmentType === 'Direct alignment'
                ? 'bg-amber-100 text-amber-800 border-amber-300'
                : 'bg-amber-50 text-amber-700 border-amber-200'
            }`}>
              {alignmentType}
            </div>
          </div>

          {/* Alignment Details */}
          <div>
            <h3 className="text-sm font-semibold text-gray-700 mb-3">
              Alignment Details
            </h3>
            <div className="bg-amber-50 p-4 rounded-lg border border-amber-200">
              <p className="text-sm text-gray-800 leading-relaxed">
                {details}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
