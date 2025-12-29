import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { File, Check, X, Archive, Plus, Trash2 } from 'lucide-react';
import { toast } from 'sonner';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

function EvidenceDrawer({ 
  isOpen, 
  onClose, 
  evidence, 
  onUpdate, 
  questionIdToCode,
  mode = 'view' // 'view' for Evidence Register (read-only except linked questions), 'edit' for Assessment page
}) {
  const [linkedQuestions, setLinkedQuestions] = useState([]);
  const [newQuestionId, setNewQuestionId] = useState('');
  const [saving, setSaving] = useState(false);
  const [archiving, setArchiving] = useState(false);
  const [hasChanges, setHasChanges] = useState(false);

  // Load evidence data when drawer opens or evidence changes
  useEffect(() => {
    if (isOpen && evidence) {
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
    }
  }, [isOpen]);

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

    setSaving(true);
    try {
      const updateData = {
        linked_question_ids: linkedQuestions
      };

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

  if (!isOpen) return null;

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
              {/* Read-only Classification Fields */}
              <Card>
                <CardHeader className="py-3 px-4">
                  <CardTitle className="text-sm font-semibold text-gray-900">Classification</CardTitle>
                </CardHeader>
                <CardContent className="py-3 px-4 space-y-3">
                  {renderReadOnlyField('Evidence Type', evidence.evidence_type)}
                  {renderReadOnlyField('Lifecycle Phase', evidence.lifecycle_phase)}
                  {renderReadOnlyField('Trust Level', evidence.trust_level)}
                  {renderReadOnlyField('Applies To Scope', evidence.applies_to_scope)}
                  
                  {/* Reuse Status - Read only */}
                  <div className="space-y-1">
                    <Label className="text-xs font-medium text-gray-500">Reuse Status</Label>
                    <div className="flex items-center space-x-2 px-3 py-2 bg-gray-50 border border-gray-200 rounded-md">
                      <div className={`w-4 h-4 rounded border-2 flex items-center justify-center ${
                        evidence.is_reusable 
                          ? 'bg-teal-600 border-teal-600' 
                          : 'border-gray-400 bg-white'
                      }`}>
                        {evidence.is_reusable && (
                          <Check className="w-3 h-3 text-white" />
                        )}
                      </div>
                      <span className="text-sm text-gray-900">
                        {evidence.is_reusable ? 'Yes - Can be reused across questions' : 'No'}
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Editable Linked Questions */}
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
                          <button
                            onClick={() => handleRemoveQuestion(question)}
                            className="ml-1.5 p-0.5 hover:bg-teal-200 rounded-full transition-colors"
                          >
                            <X className="w-3 h-3 text-teal-600" />
                          </button>
                        </div>
                      ))
                    )}
                  </div>
                  
                  {/* Add new question */}
                  <div className="flex items-center space-x-2">
                    <Input
                      type="text"
                      placeholder="Enter question ID (e.g., FA-5)"
                      value={newQuestionId}
                      onChange={(e) => setNewQuestionId(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && handleAddQuestion()}
                      className="flex-1 text-sm"
                    />
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={handleAddQuestion}
                      disabled={!newQuestionId.trim()}
                    >
                      <Plus className="w-4 h-4" />
                    </Button>
                  </div>
                  <p className="text-xs text-gray-500">
                    Add or remove question IDs to update which questions this evidence supports.
                  </p>
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
