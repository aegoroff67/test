import React, { useState, useEffect } from 'react';
import { Paperclip, Plus } from 'lucide-react';
import axios from 'axios';
import EvidenceUploadModal from './EvidenceUploadModal';
import EvidenceDrawer from './EvidenceDrawer';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

/**
 * EvidenceAttachLink - A reusable component for attaching evidence to FAIRA questions
 * 
 * Props:
 * - questionCode: The question identifier (e.g., "A1-1", "B3-2") 
 * - assessmentId: The current assessment ID
 * - currentUser: The current user object
 * - onEvidenceChange: Optional callback when evidence is added/updated
 */
function EvidenceAttachLink({ questionCode, assessmentId, currentUser, onEvidenceChange }) {
  const [evidenceCount, setEvidenceCount] = useState(0);
  const [evidence, setEvidence] = useState([]);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [showDrawer, setShowDrawer] = useState(false);
  const [selectedEvidence, setSelectedEvidence] = useState(null);
  const [loading, setLoading] = useState(false);

  // Fetch evidence count for this question
  const fetchEvidence = async () => {
    if (!questionCode || !assessmentId) return;
    
    setLoading(true);
    try {
      const response = await axios.get(
        `${BACKEND_URL}/api/evidence/by-question/${questionCode}?assessment_id=${assessmentId}`
      );
      const evidenceList = response.data || [];
      setEvidence(evidenceList);
      setEvidenceCount(evidenceList.length);
    } catch (error) {
      // If no evidence found, just set count to 0
      setEvidence([]);
      setEvidenceCount(0);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEvidence();
  }, [questionCode, assessmentId]);

  const handleUploadSuccess = (file, metadata) => {
    fetchEvidence();
    if (onEvidenceChange) onEvidenceChange();
  };

  const handleEvidenceClick = () => {
    if (evidenceCount > 0) {
      // Show the first evidence in drawer
      setSelectedEvidence(evidence[0]);
      setShowDrawer(true);
    } else {
      // Open upload modal
      setShowUploadModal(true);
    }
  };

  const handleDrawerUpdate = () => {
    fetchEvidence();
    if (onEvidenceChange) onEvidenceChange();
  };

  return (
    <>
      <button
        type="button"
        onClick={handleEvidenceClick}
        className={`inline-flex items-center gap-1 px-2 py-0.5 text-xs rounded-full transition-colors ${
          evidenceCount > 0
            ? 'bg-green-50 text-green-700 border border-green-200 hover:bg-green-100'
            : 'bg-gray-50 text-gray-600 border border-gray-200 hover:bg-gray-100'
        }`}
        title={evidenceCount > 0 ? `${evidenceCount} evidence attached - click to view` : 'Click to attach evidence'}
        data-testid={`evidence-link-${questionCode}`}
      >
        <Paperclip className="h-3 w-3" />
        {evidenceCount > 0 ? (
          <span>{evidenceCount}</span>
        ) : (
          <>
            <span className="hidden sm:inline">Attach</span>
            <Plus className="h-3 w-3 sm:hidden" />
          </>
        )}
      </button>

      {/* Evidence Upload Modal */}
      <EvidenceUploadModal
        isOpen={showUploadModal}
        onClose={() => setShowUploadModal(false)}
        onUpload={handleUploadSuccess}
        questionCode={questionCode}
        assessmentId={assessmentId}
        currentUser={currentUser}
      />

      {/* Evidence Drawer for viewing/editing */}
      <EvidenceDrawer
        isOpen={showDrawer}
        onClose={() => {
          setShowDrawer(false);
          setSelectedEvidence(null);
        }}
        evidence={selectedEvidence}
        onUpdate={handleDrawerUpdate}
        questionCode={questionCode}
        mode="edit"
      />
    </>
  );
}

export default EvidenceAttachLink;
