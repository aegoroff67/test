import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { File, Check, X, Archive, Plus, ChevronDown } from 'lucide-react';
import { toast } from 'sonner';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

// Dropdown options (matching EvidenceUploadModal)
const EVIDENCE_TYPE_OPTIONS = [
  'Policy',
  'Standard',
  'Procedure',
  'Process Description',
  'Risk Assessment',
  'Impact Assessment',
  'Technical Configuration',
  'System Architecture',
  'Model Documentation',
  'Training Material',
  'Contract / SLA',
  'Audit Report',
  'Log / Monitoring Output',
  'Screenshot / Snapshot',
  'Other'
];

const LIFECYCLE_PHASE_OPTIONS = [
  'Design',
  'Development',
  'Testing',
  'Deployment',
  'Operation',
  'Monitoring',
  'Decommissioning',
  'Cross-Lifecycle'
];

const TRUST_LEVEL_OPTIONS = [
  'Unspecified',
  'Draft',
  'Approved',
  'Operational',
  'Independently Reviewed',
  'Regulator / External Assured'
];

const APPLIES_TO_SCOPE_OPTIONS = [
  'Organisation-wide',
  'Shared Platform / Service',
  'Specific AI System',
  'Specific Model',
  'Specific Use Case',
  'Third Party / Vendor',
  'Unspecified'
];

function EvidenceDrawer({ 
  isOpen, 
  onClose, 
  evidence, 
  onUpdate, 
  questionIdToCode,
  mode = 'view' // 'view' for Evidence Register (read-only), 'edit' for Assessment page (in-progress)
}) {
  // Editable fields state
  const [evidenceType, setEvidenceType] = useState('');
  const [lifecyclePhase, setLifecyclePhase] = useState('');
  const [trustLevel, setTrustLevel] = useState('');
  const [appliesToScope, setAppliesToScope] = useState('');
  const [isReusable, setIsReusable] = useState(false);
  const [linkedQuestions, setLinkedQuestions] = useState([]);
  const [notes, setNotes] = useState('');
  // Phase 1 new fields
  const [evidenceSummary, setEvidenceSummary] = useState('');
  const [limitations, setLimitations] = useState('');
  
  const [newQuestionId, setNewQuestionId] = useState('');
  const [saving, setSaving] = useState(false);
  const [archiving, setArchiving] = useState(false);
  const [hasChanges, setHasChanges] = useState(false);
  
  // Dropdown open states
  const [openDropdown, setOpenDropdown] = useState(null);

  // Load evidence data when drawer opens or evidence changes
  useEffect(() => {
    if (isOpen && evidence) {
      // Set all editable fields from evidence
      setEvidenceType(evidence.evidence_type || 'Unspecified');
      setLifecyclePhase(evidence.lifecycle_phase || 'Unspecified');
      setTrustLevel(evidence.trust_level || 'Unspecified');
      setAppliesToScope(evidence.applies_to_scope || 'Unspecified');
      setIsReusable(evidence.is_reusable || false);
      setNotes(evidence.notes || '');
      // Phase 1 new fields
      setEvidenceSummary(evidence.evidence_summary || '');
      setLimitations(evidence.limitations || '');
      
      // Convert UUIDs to codes if possible
      const codes = (evidence.linked_question_ids || []).map(id => {
        if (questionIdToCode && questionIdToCode[id]) {
          return questionIdToCode[id];
        }
        return id;
      });
      setLinkedQuestions(codes);
      setHasChanges(false);
    }
  }, [isOpen, evidence, questionIdToCode]);

  // Reset when drawer closes
  useEffect(() => {
    if (!isOpen) {
      setLinkedQuestions([]);
      setNewQuestionId('');
      setHasChanges(false);
      setOpenDropdown(null);
    }
  }, [isOpen]);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (openDropdown && !event.target.closest('.dropdown-container')) {
        setOpenDropdown(null);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [openDropdown]);

  const handleFieldChange = (setter) => (value) => {
    setter(value);
    setHasChanges(true);
    setOpenDropdown(null);
  };

  const handleAddQuestion = () => {
    const trimmed = newQuestionId.trim().toUpperCase();
    if (trimmed && !linkedQuestions.includes(trimmed)) {
      setLinkedQuestions([...linkedQuestions, trimmed]);
      setNewQuestionId('');
      setHasChanges(true);
    }
  };

  const handleRemoveQuestion = (questionToRemove) => {
    setLinkedQuestions(linkedQuestions.filter(q => q !== questionToRemove));
    setHasChanges(true);
  };

  const handleSave = async () => {
    if (!evidence?.evidence_id) {
      toast.error('Cannot save: No evidence selected');
      return;
    }

    if (linkedQuestions.length === 0) {
      toast.error('At least one linked question is required');
      return;
    }

    // If not reusable, only one question allowed
    if (!isReusable && linkedQuestions.length > 1) {
      toast.error('Non-reusable evidence can only be linked to one question');
      return;
    }

    setSaving(true);
    try {
      const updateData = {
        linked_question_ids: linkedQuestions,
        notes: notes,
        // Phase 1 new fields
        evidence_summary: evidenceSummary || null,
        limitations: limitations || null
      };

      // In edit mode (assessment in progress), include all classification fields
      if (mode === 'edit') {
        updateData.evidence_type = evidenceType;
        updateData.lifecycle_phase = lifecyclePhase;
        updateData.trust_level = trustLevel;
        updateData.applies_to_scope = appliesToScope;
        updateData.is_reusable = isReusable;
      }

      await axios.put(`${BACKEND_URL}/api/evidence/${evidence.evidence_id}`, updateData);
      
      toast.success('Evidence updated successfully!');
      setHasChanges(false);
      
      if (onUpdate) {
        onUpdate();
      }
    } catch (error) {
      console.error('Error saving evidence:', error);
      toast.error(error.response?.data?.detail || 'Failed to save evidence');
    } finally {
      setSaving(false);
    }
  };

  const handleArchive = async () => {
    if (!evidence?.evidence_id) {
      toast.error('Cannot archive: No evidence selected');
      return;
    }

    if (!window.confirm('Are you sure you want to archive this evidence? It will no longer appear in active reports.')) {
      return;
    }

    setArchiving(true);
    try {
      const updateData = {
        status: 'Archived'
      };

      await axios.put(`${BACKEND_URL}/api/evidence/${evidence.evidence_id}`, updateData);
      
      toast.success('Evidence archived successfully!');
      
      if (onUpdate) {
        onUpdate();
      }
      onClose();
    } catch (error) {
      console.error('Error archiving evidence:', error);
      toast.error(error.response?.data?.detail || 'Failed to archive evidence');
    } finally {
      setArchiving(false);
    }
  };

  const handleClose = () => {
    if (hasChanges) {
      if (!window.confirm('You have unsaved changes. Are you sure you want to close?')) {
        return;
      }
    }
    onClose();
  };

  // Render a read-only field
  const renderReadOnlyField = (label, value) => (
    <div className="space-y-1">
      <Label className="text-xs font-medium text-gray-500">{label}</Label>
      <div className="px-3 py-2 bg-gray-50 border border-gray-200 rounded-md text-sm text-gray-900">
        {value || 'Unspecified'}
      </div>
    </div>
  );

  // Render an editable dropdown field
  const renderEditableDropdown = (label, value, options, dropdownKey, onChange) => (
    <div className="space-y-1 dropdown-container relative">
      <Label className="text-xs font-medium text-gray-500">{label}</Label>
      <button
        type="button"
        onClick={() => setOpenDropdown(openDropdown === dropdownKey ? null : dropdownKey)}
        className="w-full flex items-center justify-between px-3 py-2 bg-white border border-gray-300 rounded-md text-sm text-gray-900 hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-500"
      >
        <span>{value || 'Select...'}</span>
        <ChevronDown className="w-4 h-4 text-gray-500" />
      </button>
      {openDropdown === dropdownKey && (
        <div className="absolute z-50 w-full mt-1 bg-white border border-gray-200 rounded-md shadow-lg max-h-48 overflow-auto">
          {options.map((option) => (
            <button
              key={option}
              type="button"
              onClick={() => onChange(option)}
              className={`w-full text-left px-3 py-2 text-sm hover:bg-gray-50 ${
                value === option ? 'bg-teal-50 text-teal-700 font-medium' : 'text-gray-700'
              }`}
            >
              {option}
            </button>
          ))}
        </div>
      )}
    </div>
  );

  if (!isOpen) return null;

  const isEditMode = mode === 'edit';

  return (
    <>
      {/* Backdrop */}
      <div 
        className="fixed inset-0 bg-black/50 z-40 transition-opacity"
        onClick={handleClose}
      />
      
      {/* Drawer */}
      <div className="fixed right-0 top-0 h-full w-[500px] max-w-[95vw] bg-white shadow-xl z-50 flex flex-col animate-in slide-in-from-right duration-300">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-lg bg-teal-50 flex items-center justify-center">
              <File className="w-5 h-5 text-teal-600" />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-gray-900 truncate max-w-[300px]">
                {evidence?.evidence_title || evidence?.file_name || 'Evidence Details'}
              </h2>
              <p className="text-xs text-gray-500">
                {evidence?.status === 'Archived' ? 'Archived' : 'Active'} • Uploaded {evidence?.uploaded_date ? new Date(evidence.uploaded_date).toLocaleDateString() : 'Unknown'}
              </p>
            </div>
          </div>
          <button
            onClick={handleClose}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <X className="w-5 h-5 text-gray-500" />
          </button>
        </div>

        {/* Main Content */}
        <div className="flex-1 overflow-auto p-4">
          {evidence ? (
            <div className="space-y-4">
              {/* Classification Fields */}
              <Card>
                <CardHeader className="py-3 px-4">
                  <CardTitle className="text-sm font-semibold text-gray-900">
                    Classification
                    {isEditMode && <span className="ml-2 text-xs font-normal text-teal-600">(Editable)</span>}
                  </CardTitle>
                </CardHeader>
                <CardContent className="py-3 px-4 space-y-3">
                  {isEditMode ? (
                    <>
                      {renderEditableDropdown('Evidence Type', evidenceType, EVIDENCE_TYPE_OPTIONS, 'evidenceType', handleFieldChange(setEvidenceType))}
                      {renderEditableDropdown('Lifecycle Phase', lifecyclePhase, LIFECYCLE_PHASE_OPTIONS, 'lifecyclePhase', handleFieldChange(setLifecyclePhase))}
                      {renderEditableDropdown('Trust Level', trustLevel, TRUST_LEVEL_OPTIONS, 'trustLevel', handleFieldChange(setTrustLevel))}
                      {renderEditableDropdown('Applies To Scope', appliesToScope, APPLIES_TO_SCOPE_OPTIONS, 'appliesToScope', handleFieldChange(setAppliesToScope))}
                    </>
                  ) : (
                    <>
                      {renderReadOnlyField('Evidence Type', evidence.evidence_type)}
                      {renderReadOnlyField('Lifecycle Phase', evidence.lifecycle_phase)}
                      {renderReadOnlyField('Trust Level', evidence.trust_level)}
                      {renderReadOnlyField('Applies To Scope', evidence.applies_to_scope)}
                    </>
                  )}
                  
                  {/* Reuse Status */}
                  <div className="space-y-1">
                    <Label className="text-xs font-medium text-gray-500">
                      {isEditMode ? 'Allow this evidence to be reused across other questions?' : 'Reuse Status'}
                    </Label>
                    {isEditMode ? (
                      <div className="flex items-center space-x-4 px-3 py-2 bg-white border border-gray-300 rounded-md">
                        <label className="flex items-center space-x-2 cursor-pointer">
                          <input
                            type="radio"
                            name="reusable"
                            checked={isReusable}
                            onChange={() => handleFieldChange(setIsReusable)(true)}
                            className="w-4 h-4 text-teal-600 border-gray-300 focus:ring-teal-500"
                          />
                          <span className="text-sm text-gray-900">Yes – Reusable</span>
                        </label>
                        <label className="flex items-center space-x-2 cursor-pointer">
                          <input
                            type="radio"
                            name="reusable"
                            checked={!isReusable}
                            onChange={() => handleFieldChange(setIsReusable)(false)}
                            className="w-4 h-4 text-teal-600 border-gray-300 focus:ring-teal-500"
                          />
                          <span className="text-sm text-gray-900">No – Question-specific</span>
                        </label>
                      </div>
                    ) : (
                      <div className="flex items-center space-x-2 px-3 py-2 bg-gray-50 border border-gray-200 rounded-md">
                        {evidence.is_reusable ? (
                          <Check className="w-4 h-4 text-green-600" />
                        ) : (
                          <X className="w-4 h-4 text-red-500" />
                        )}
                        <span className="text-sm text-gray-900">
                          {evidence.is_reusable ? 'Yes – Can be reused across questions' : 'No – Restricted to this question'}
                        </span>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>

              {/* Linked Questions */}
              <Card>
                <CardHeader className="py-3 px-4">
                  <CardTitle className="text-sm font-semibold text-gray-900">Linked Questions</CardTitle>
                </CardHeader>
                <CardContent className="py-3 px-4 space-y-3">
                  {/* Current linked questions */}
                  <div className="flex flex-wrap gap-2">
                    {linkedQuestions.length === 0 ? (
                      <p className="text-sm text-gray-500">No questions linked</p>
                    ) : (
                      linkedQuestions.map((question, index) => (
                        <div 
                          key={index}
                          className="inline-flex items-center px-2.5 py-1 rounded-md bg-teal-50 border border-teal-200"
                        >
                          <span className="text-sm font-medium text-teal-800">{question}</span>
                          {/* Show remove button if: edit mode, OR (view mode AND reusable AND more than 1 question) */}
                          {(isEditMode || (isReusable && linkedQuestions.length > 1)) && (
                            <button
                              onClick={() => handleRemoveQuestion(question)}
                              className="ml-1.5 p-0.5 hover:bg-teal-200 rounded-full transition-colors"
                            >
                              <X className="w-3 h-3 text-teal-600" />
                            </button>
                          )}
                        </div>
                      ))
                    )}
                  </div>
                  
                  {/* Add new question */}
                  {(isEditMode || isReusable) ? (
                    <>
                      <div className="flex items-center space-x-2">
                        <Input
                          type="text"
                          placeholder="Enter question ID (e.g., FA-5)"
                          value={newQuestionId}
                          onChange={(e) => setNewQuestionId(e.target.value)}
                          onKeyPress={(e) => e.key === 'Enter' && handleAddQuestion()}
                          className="flex-1 text-sm"
                          disabled={!isReusable && linkedQuestions.length >= 1 && !isEditMode}
                        />
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={handleAddQuestion}
                          disabled={!newQuestionId.trim() || (!isReusable && linkedQuestions.length >= 1 && !isEditMode)}
                        >
                          <Plus className="w-4 h-4" />
                        </Button>
                      </div>
                      {!isReusable && (
                        <p className="text-xs text-amber-600 bg-amber-50 border border-amber-200 rounded-md px-3 py-2">
                          This evidence is question-specific. {isEditMode ? 'Change Reuse Status to "Yes" to link to multiple questions.' : 'It cannot be linked to additional questions.'}
                        </p>
                      )}
                      {isReusable && (
                        <p className="text-xs text-gray-500">
                          Add or remove question IDs to update which questions this evidence supports.
                        </p>
                      )}
                    </>
                  ) : (
                    <p className="text-xs text-amber-600 bg-amber-50 border border-amber-200 rounded-md px-3 py-2">
                      This evidence was uploaded as question-specific and cannot be reused across other questions.
                    </p>
                  )}
                </CardContent>
              </Card>

              {/* Notes Section */}
              <Card>
                <CardHeader className="py-3 px-4">
                  <CardTitle className="text-sm font-semibold text-gray-900">Notes</CardTitle>
                </CardHeader>
                <CardContent className="py-3 px-4">
                  {isEditMode ? (
                    <Textarea
                      placeholder="Add notes about this evidence..."
                      value={notes}
                      onChange={(e) => {
                        setNotes(e.target.value);
                        setHasChanges(true);
                      }}
                      className="min-h-[100px] text-sm"
                    />
                  ) : (
                    <div className="px-3 py-2 bg-gray-50 border border-gray-200 rounded-md text-sm text-gray-900 min-h-[60px]">
                      {evidence.notes || <span className="text-gray-400 italic">No notes</span>}
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* Archive Section */}
              {evidence.status !== 'Archived' && (
                <Card className="border-red-200">
                  <CardHeader className="py-3 px-4">
                    <CardTitle className="text-sm font-semibold text-red-700">Danger Zone</CardTitle>
                  </CardHeader>
                  <CardContent className="py-3 px-4">
                    <Button
                      variant="outline"
                      onClick={handleArchive}
                      disabled={archiving}
                      className="w-full text-red-600 border-red-300 hover:bg-red-50"
                    >
                      {archiving ? (
                        <>
                          <div className="w-4 h-4 mr-2 border-2 border-red-600 border-t-transparent rounded-full animate-spin" />
                          Archiving...
                        </>
                      ) : (
                        <>
                          <Archive className="w-4 h-4 mr-2" />
                          Archive Evidence
                        </>
                      )}
                    </Button>
                    <p className="text-xs text-gray-500 mt-2">
                      Archived evidence will no longer appear in active reports but can be restored later.
                    </p>
                  </CardContent>
                </Card>
              )}
            </div>
          ) : (
            <div className="flex-1 flex items-center justify-center">
              <p className="text-gray-500">No evidence selected</p>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-gray-200 flex justify-end items-center space-x-3">
          <Button variant="outline" onClick={handleClose} disabled={saving}>
            Cancel
          </Button>
          <Button
            onClick={handleSave}
            disabled={!hasChanges || saving}
            className="bg-teal-600 hover:bg-teal-700 text-white"
          >
            {saving ? (
              <>
                <div className="w-4 h-4 mr-2 border-2 border-white border-t-transparent rounded-full animate-spin" />
                Saving...
              </>
            ) : (
              'Save Changes'
            )}
          </Button>
        </div>
      </div>
    </>
  );
}

export default EvidenceDrawer;
