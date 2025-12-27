import React from 'react';
import { X } from 'lucide-react';

export default function FrameworkCoverageInfoModal({ isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div 
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div className="bg-white rounded-lg shadow-xl w-full max-h-[90vh] flex flex-col" style={{ maxWidth: '1100px' }}>
        {/* Header */}
        <div className="bg-blue-600 text-white px-6 py-4 rounded-t-lg flex items-start justify-between">
          <div className="flex-1 pr-4">
            <h2 className="text-lg font-semibold leading-tight">
              Framework Coverage Overview — How to Interpret This View
            </h2>
          </div>
          <button 
            onClick={onClose}
            className="text-blue-200 hover:text-white transition-colors flex-shrink-0"
          >
            <X className="h-6 w-6" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto flex-1">
          {/* What this shows */}
          <div className="mb-6">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">What this shows</h3>
            <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
              <p className="text-sm text-gray-700 leading-relaxed mb-3">
                This view summarises how comprehensively selected AI governance frameworks are addressed by the AM AI SAFE assessment for this system. It compares:
              </p>
              <ul className="text-sm text-gray-700 space-y-2 ml-4">
                <li className="flex items-start">
                  <span className="mr-2">•</span>
                  <span><strong>Inherent Coverage</strong> — what AM AI SAFE is designed to cover by default, and</span>
                </li>
                <li className="flex items-start">
                  <span className="mr-2">•</span>
                  <span><strong>Achieved Coverage</strong> — what is supported by the organisation&apos;s assessment responses.</span>
                </li>
              </ul>
            </div>
          </div>

          {/* Confidence-Weighted Coverage */}
          <div className="mb-6">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">Confidence-Weighted Coverage</h3>
            <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
              <p className="text-sm text-gray-700 leading-relaxed mb-3">
                Achieved coverage is adjusted to reflect the strength and completeness of implementation, not just whether a control is addressed.
              </p>
              <ul className="text-sm text-gray-700 space-y-1 ml-4">
                <li className="flex items-start">
                  <span className="mr-2">•</span>
                  <span>Strong coverage contributes fully</span>
                </li>
                <li className="flex items-start">
                  <span className="mr-2">•</span>
                  <span>Moderate and weak coverage contribute partially</span>
                </li>
                <li className="flex items-start">
                  <span className="mr-2">•</span>
                  <span>No coverage reduces overall confidence</span>
                </li>
              </ul>
              <p className="text-sm text-gray-700 leading-relaxed mt-3">
                This helps prevent early or partial implementations from overstating coverage.
              </p>
            </div>
          </div>

          {/* Coverage Gap */}
          <div className="mb-6">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">Coverage Gap</h3>
            <div className="bg-amber-50 p-4 rounded-lg border border-amber-200">
              <p className="text-sm text-gray-700 leading-relaxed">
                The coverage gap represents residual governance risk between intended framework coverage and confidence-weighted implementation. Gap severity labels (<span className="text-green-600 font-medium">LOW</span> / <span className="text-yellow-600 font-medium">MODERATE</span> / <span className="text-red-600 font-medium">HIGH</span>) provide a qualitative indication of where further attention may be required.
              </p>
            </div>
          </div>

          {/* Important note */}
          <div className="mb-6">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">Important note</h3>
            <div className="bg-red-50 p-4 rounded-lg border-l-4 border-red-400">
              <p className="text-sm text-gray-700 leading-relaxed">
                Results are indicative and risk-based. They do not constitute legal, regulatory, or certification advice, and do not replace formal audits or independent assurance.
              </p>
            </div>
          </div>

          {/* How to use this view */}
          <div>
            <h3 className="text-sm font-semibold text-gray-700 mb-3">How to use this view</h3>
            <div className="bg-green-50 p-4 rounded-lg border border-green-200">
              <p className="text-sm text-gray-700 leading-relaxed">
                Use this information to support prioritisation, improvement planning, and informed discussions with governance, risk, and assurance stakeholders.
              </p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="bg-gray-50 px-6 py-4 border-t border-gray-200 flex justify-end rounded-b-lg">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors font-medium"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
