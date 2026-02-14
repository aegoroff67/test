import React, { useState, useEffect, useRef } from 'react';
import { Paperclip, HelpCircle, ChevronDown, FileText } from 'lucide-react';
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
  const [showDropdown, setShowDropdown] = useState(false);
  const dropdownRef = useRef(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setShowDropdown(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

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

  const handleAttachClick = () => {
    setShowUploadModal(true);
  };

  const handleViewEvidenceClick = (evidenceItem) => {
    setSelectedEvidence(evidenceItem);
    setShowDrawer(true);
    setShowDropdown(false);
  };

  const handleDrawerUpdate = () => {
    fetchEvidence();
    if (onEvidenceChange) onEvidenceChange();
  };

  return (
    <div className="inline-flex items-center gap-1.5">
      {/* Attach Evidence Button - Always visible */}
      <button
        type="button"
        onClick={handleAttachClick}
        className="inline-flex items-center gap-1 px-2 py-0.5 text-xs rounded-full transition-colors bg-gray-50 text-gray-600 border border-gray-200 hover:bg-gray-100"
        title="Click to attach evidence"
        data-testid={`evidence-attach-${questionCode}`}
      >
        <Paperclip className="h-3 w-3" />
        <span>Attach evidence</span>
      </button>

      {/* View Evidence Dropdown - Only shown when evidence exists */}
      {evidenceCount > 0 && (
        <div className="relative" ref={dropdownRef}>
          <button
            type="button"
            onClick={() => setShowDropdown(!showDropdown)}
            className="inline-flex items-center gap-1 px-2 py-0.5 text-xs rounded-full transition-colors bg-green-50 text-green-700 border border-green-200 hover:bg-green-100"
            title={`${evidenceCount} evidence artefact${evidenceCount === 1 ? '' : 's'} attached - click to view`}
            data-testid={`evidence-view-${questionCode}`}
          >
            <FileText className="h-3 w-3" />
            <span>{evidenceCount}</span>
            <ChevronDown className={`h-3 w-3 transition-transform ${showDropdown ? 'rotate-180' : ''}`} />
          </button>

          {/* Dropdown menu */}
          {showDropdown && (
            <div className="absolute right-0 top-7 z-50 w-64 bg-white border border-gray-200 rounded-lg shadow-lg overflow-hidden">
              <div className="px-3 py-2 bg-gray-50 border-b border-gray-200">
                <span className="text-xs font-medium text-gray-700">
                  {evidenceCount} evidence artefact{evidenceCount === 1 ? '' : 's'}
                </span>
              </div>
              <ul className="max-h-48 overflow-y-auto">
                {evidence.map((item, index) => (
                  <li key={item.id || index}>
                    <button
                      type="button"
                      onClick={() => handleViewEvidenceClick(item)}
                      className="w-full px-3 py-2 text-left text-xs hover:bg-gray-50 flex items-start gap-2 border-b border-gray-100 last:border-b-0"
                    >
                      <FileText className="h-3.5 w-3.5 text-gray-400 mt-0.5 flex-shrink-0" />
                      <div className="min-w-0 flex-1">
                        <div className="font-medium text-gray-900 truncate">
                          {item.evidence_title || item.file_name || `Evidence ${index + 1}`}
                        </div>
                        <div className="text-gray-500 truncate">
                          {item.evidence_type || 'Document'}
                        </div>
                      </div>
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
      
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
              <div>{tooltip}</div>
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
