import React, { useState, useEffect } from 'react';
import { Paperclip, HelpCircle } from 'lucide-react';
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
 * - tooltip: Optional tooltip text to display on hover
 */
function EvidenceAttachLink({ questionCode, assessmentId, currentUser, onEvidenceChange, tooltip }) {
  const [evidenceCount, setEvidenceCount] = useState(0);
  const [evidence, setEvidence] = useState([]);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [showDrawer, setShowDrawer] = useState(false);
  const [selectedEvidence, setSelectedEvidence] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showTooltip, setShowTooltip] = useState(false);

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
    <div className="inline-flex items-center gap-1.5">
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
          <span>Attach evidence</span>
        )}
      </button>
      
      {/* Tooltip help icon */}
      {tooltip && (
        <div className="relative">
          <button
            type="button"
            onMouseEnter={() => setShowTooltip(true)}
            onMouseLeave={() => setShowTooltip(false)}
            onClick={(e) => {
              e.preventDefault();
              setShowTooltip(!showTooltip);
            }}
            className="text-gray-400 hover:text-gray-600 transition-colors"
            aria-label="Evidence guidance"
          >
            <HelpCircle className="h-3.5 w-3.5" />
          </button>
          
          {showTooltip && (
            <div className="absolute right-0 top-6 z-50 w-72 p-3 text-xs bg-gray-900 text-white rounded-lg shadow-lg">
              <div className="whitespace-pre-line">{typeof tooltip === 'string' ? tooltip : tooltip}</div>
              <div className="absolute -top-1.5 right-2 w-3 h-3 bg-gray-900 transform rotate-45"></div>
            </div>
          )}
        </div>
      )}

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
    </div>
  );
}

// Tooltip content for each question
export const EVIDENCE_TOOLTIPS = {
  'A1-1': (
    <>
      <strong>Suitable evidence may include:</strong>
      <br /><br />
      • System overview or architecture diagrams
      <br />• Workflow or process flow charts
      <br />• Screenshots of dashboards or user interfaces
      <br />• Project initiation or business case summaries
      <br /><br />
      <strong>Upload evidence if it helps clarify how the AI system operates in practice.</strong>
    </>
  ),

  'A1-9': (
    <>
      <strong>Suitable evidence may include:</strong>
      <br /><br />
      • System integration diagrams
      <br />• Data flow diagrams
      <br />• API documentation excerpts
      <br />• Infrastructure or hosting architecture diagrams
      <br /><br />
      <strong>Upload evidence to illustrate how the AI system connects to other systems.</strong>
    </>
  ),

  'A3-1': (
    <>
      <strong>Suitable evidence may include:</strong>
      <br /><br />
      • Source system screenshots
      <br />• Data inventory extracts
      <br />• Data schema or data dictionary excerpts
      <br />• Vendor documentation describing data inputs
      <br /><br />
      <strong>Upload evidence to demonstrate provenance and ownership of data sources.</strong>
    </>
  ),

  'A3-3': (
    <>
      <strong>Suitable evidence may include:</strong>
      <br /><br />
      • Data quality reports
      <br />• Validation or reconciliation procedures
      <br />• Testing results or audit findings
      <br />• Documented data governance processes
      <br /><br />
      <strong>Upload evidence if data quality controls are formally documented.</strong>
    </>
  ),

  'A4-7': (
    <>
      <strong>Suitable evidence may include:</strong>
      <br /><br />
      • Privacy Impact Assessment extracts
      <br />• Security configuration screenshots
      <br />• Access control policies
      <br />• Encryption or de-identification documentation
      <br /><br />
      <strong>Upload evidence where safeguards are formally defined or implemented.</strong>
    </>
  ),

  'A4-8': (
    <>
      <strong>Suitable evidence may include:</strong>
      <br /><br />
      • Decision pathway or escalation diagrams
      <br />• Delegations or approval workflows
      <br />• Relevant policy or legislative references
      <br />• Records demonstrating human review steps
      <br /><br />
      <strong>Upload evidence to support how legal or regulatory effects are managed.</strong>
    </>
  ),

  'A5-1': (
    <>
      <strong>Suitable evidence may include:</strong>
      <br /><br />
      • Governance charters or terms of reference
      <br />• Organisational charts
      <br />• Role descriptions
      <br />• Delegations or accountability statements
      <br /><br />
      <strong>Upload evidence to demonstrate clear ownership of AI-related decisions.</strong>
    </>
  ),

  'A5-3': (
    <>
      <strong>Suitable evidence may include:</strong>
      <br /><br />
      • Monitoring plans or review schedules
      <br />• Performance dashboards
      <br />• Risk registers
      <br />• Evaluation reports
      <br /><br />
      <strong>Upload evidence where monitoring arrangements are documented.</strong>
    </>
  ),

  'A5-5': (
    <>
      <strong>Suitable evidence may include:</strong>
      <br /><br />
      • Independent review reports
      <br />• Audit findings
      <br />• External assurance statements
      <br />• Peer review documentation
      <br /><br />
      <strong>Upload evidence if an independent review has been conducted.</strong>
    </>
  ),

  'A5-10': (
    <>
      <strong>Suitable evidence may include:</strong>
      <br /><br />
      • Legislative mapping tables
      <br />• Compliance registers
      <br />• Framework alignment documentation
      <br />• Legal advice extracts (where appropriate)
      <br /><br />
      <strong>Upload evidence if compliance obligations are formally documented.</strong>
    </>
  ),

  'B2-1': (
    <>
      <strong>Suitable evidence may include:</strong>
      <br /><br />
      • Completed HRIA report
      <br />• Impact analysis documentation
      <br />• Consultation records
      <br /><br />
      <strong>Upload evidence if a formal human rights assessment has been undertaken.</strong>
    </>
  ),

  'B4-1': (
    <>
      <strong>Suitable evidence may include:</strong>
      <br /><br />
      • Completed PIA report
      <br />• Risk treatment plan
      <br />• Privacy mitigation documentation
      <br /><br />
      <strong>Upload evidence if a Privacy Impact Assessment has been completed.</strong>
    </>
  ),

  'B5-1': (
    <>
      <strong>Suitable evidence may include:</strong>
      <br /><br />
      • Test plans and test results
      <br />• QA documentation
      <br />• Model validation reports
      <br />• Performance benchmarking outputs
      <br /><br />
      <strong>Upload evidence if reliability or safety testing has been performed.</strong>
    </>
  ),

  'B7-1': (
    <>
      <strong>Suitable evidence may include:</strong>
      <br /><br />
      • Complaints or review procedures
      <br />• Escalation workflows
      <br />• Service standards documentation
      <br />• Policy extracts describing appeal rights
      <br /><br />
      <strong>Upload evidence to demonstrate how affected parties can challenge outcomes.</strong>
    </>
  )
};

export default EvidenceAttachLink;
