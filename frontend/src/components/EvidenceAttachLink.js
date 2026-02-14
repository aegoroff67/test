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
              <div className="whitespace-pre-line">{tooltip}</div>
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
  'A1-1': `Suitable evidence may include:
• System overview or architecture diagrams
• Workflow or process flow charts
• Screenshots of dashboards or user interfaces
• Project initiation or business case summaries

Upload evidence if it helps clarify how the AI system operates in practice.`,

  'A1-9': `Suitable evidence may include:
• System integration diagrams
• Data flow diagrams
• API documentation excerpts
• Infrastructure or hosting architecture diagrams

Upload evidence to illustrate how the AI system connects to other systems.`,

  'A3-1': `Suitable evidence may include:
• Source system screenshots
• Data inventory extracts
• Data schema or data dictionary excerpts
• Vendor documentation describing data inputs

Upload evidence to demonstrate provenance and ownership of data sources.`,

  'A3-3': `Suitable evidence may include:
• Data quality reports
• Validation or reconciliation procedures
• Testing results or audit findings
• Documented data governance processes

Upload evidence if data quality controls are formally documented.`,

  'A4-7': `Suitable evidence may include:
• Privacy Impact Assessment extracts
• Security configuration screenshots
• Access control policies
• Encryption or de-identification documentation

Upload evidence where safeguards are formally defined or implemented.`,

  'A4-8': `Suitable evidence may include:
• Decision pathway or escalation diagrams
• Delegations or approval workflows
• Relevant policy or legislative references
• Records demonstrating human review steps

Upload evidence to support how legal or regulatory effects are managed.`,

  'A5-1': `Suitable evidence may include:
• Governance charters or terms of reference
• Organisational charts
• Role descriptions
• Delegations or accountability statements

Upload evidence to demonstrate clear ownership of AI-related decisions.`,

  'A5-3': `Suitable evidence may include:
• Monitoring plans or review schedules
• Performance dashboards
• Risk registers
• Evaluation reports

Upload evidence where monitoring arrangements are documented.`,

  'A5-5': `Suitable evidence may include:
• Independent review reports
• Audit findings
• External assurance statements
• Peer review documentation

Upload evidence if an independent review has been conducted.`,

  'A5-10': `Suitable evidence may include:
• Legislative mapping tables
• Compliance registers
• Framework alignment documentation
• Legal advice extracts (where appropriate)

Upload evidence if compliance obligations are formally documented.`,

  'B2-1': `Suitable evidence may include:
• Completed HRIA report
• Impact analysis documentation
• Consultation records

Upload evidence if a formal human rights assessment has been undertaken.`,

  'B4-1': `Suitable evidence may include:
• Completed PIA report
• Risk treatment plan
• Privacy mitigation documentation

Upload evidence if a Privacy Impact Assessment has been completed.`,

  'B5-1': `Suitable evidence may include:
• Test plans and test results
• QA documentation
• Model validation reports
• Performance benchmarking outputs

Upload evidence if reliability or safety testing has been performed.`,

  'B7-1': `Suitable evidence may include:
• Complaints or review procedures
• Escalation workflows
• Service standards documentation
• Policy extracts describing appeal rights

Upload evidence to demonstrate how affected parties can challenge outcomes.`
};

export default EvidenceAttachLink;
