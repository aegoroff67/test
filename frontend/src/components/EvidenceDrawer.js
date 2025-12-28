import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { File, Check, X } from 'lucide-react';
import { toast } from 'sonner';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

// Evidence metadata options (same as EvidenceUploadModal)
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
  'Specific AI System',
  'Specific Model',
  'Specific Use Case',
  'Third Party / Vendor',
  'Unspecified'
];

function EvidenceDrawer({ isOpen, onClose, evidenceFiles, onUpdate, questionCode }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [evidenceType, setEvidenceType] = useState('Unspecified');
  const [lifecyclePhase, setLifecyclePhase] = useState('Unspecified');
  const [trustLevel, setTrustLevel] = useState('Unspecified');
  const [appliesToScope, setAppliesToScope] = useState('Unspecified');
  const [isReusable, setIsReusable] = useState(false);
  const [saving, setSaving] = useState(false);
  const [hasChanges, setHasChanges] = useState(false);

  // Select the first file when drawer opens or files change
  useEffect(() => {
    if (isOpen && evidenceFiles?.length > 0 && !selectedFile) {
      selectFile(evidenceFiles[0]);
    }
  }, [isOpen, evidenceFiles]);

  // Reset when drawer closes
  useEffect(() => {
    if (!isOpen) {
      setSelectedFile(null);
      setHasChanges(false);
    }
  }, [isOpen]);

  const selectFile = (file) => {
    setSelectedFile(file);
    // Load the file's current settings
    setEvidenceType(file.evidence_type || 'Unspecified');
    setLifecyclePhase(file.lifecycle_phase || 'Unspecified');
    setTrustLevel(file.trust_level || 'Unspecified');
    setAppliesToScope(file.applies_to_scope || 'Unspecified');
    setIsReusable(file.is_reusable || false);
    setHasChanges(false);
  };

  const handleSettingChange = (setter, value) => {
    setter(value);
    setHasChanges(true);
  };

  const handleSave = async () => {
    if (!selectedFile?.evidence_id) {
      toast.error('Cannot save: No evidence selected');
      return;
    }

    setSaving(true);
    try {
      const updateData = {
        evidence_type: evidenceType,
        lifecycle_phase: lifecyclePhase,
        trust_level: trustLevel,
        applies_to_scope: appliesToScope,
        is_reusable: isReusable
      };

      await axios.put(`${BACKEND_URL}/api/evidence/${selectedFile.evidence_id}`, updateData);
      
      toast.success('Evidence settings saved!');
      setHasChanges(false);
      
      // Notify parent to refresh evidence list
      if (onUpdate) {
        onUpdate();
      }
    } catch (error) {
      console.error('Error saving evidence:', error);
      toast.error(error.response?.data?.detail || 'Failed to save evidence settings');
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    if (hasChanges) {
      // Reset to original values
      if (selectedFile) {
        selectFile(selectedFile);
      }
    }
    onClose();
  };

  const renderOptionCard = (title, options, selectedValue, onSelect) => (
    <Card className="w-full">
      <CardHeader className="py-1.5 px-4">
        <CardTitle className="text-sm font-semibold text-gray-900">{title}</CardTitle>
      </CardHeader>
      <CardContent className="py-1.5 px-4">
        <div className="grid grid-cols-3 gap-x-4 gap-y-1">
          {options.map((option) => (
            <div
              key={option}
              onClick={() => handleSettingChange(onSelect, option)}
              className={`flex items-center space-x-2 py-1 cursor-pointer transition-colors rounded ${
                selectedValue === option
                  ? 'bg-teal-50'
                  : 'hover:bg-gray-50'
              }`}
            >
              <div
                className={`w-3.5 h-3.5 rounded-full border-2 flex items-center justify-center flex-shrink-0 ${
                  selectedValue === option
                    ? 'border-teal-600 bg-teal-600'
                    : 'border-gray-400'
                }`}
              >
                {selectedValue === option && (
                  <div className="w-1.5 h-1.5 rounded-full bg-white" />
                )}
              </div>
              <span className={`text-xs ${selectedValue === option ? 'text-teal-900 font-medium' : 'text-gray-700'}`}>
                {option}
              </span>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );

  if (!isOpen) return null;

  return (
    <>
      {/* Backdrop */}
      <div 
        className="fixed inset-0 bg-black/50 z-40 transition-opacity"
        onClick={handleCancel}
      />
      
      {/* Drawer */}
      <div className="fixed right-0 top-0 h-full w-[1200px] max-w-[95vw] bg-white shadow-xl z-50 flex flex-col animate-in slide-in-from-right duration-300">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200">
          <div>
            <h2 className="text-lg font-semibold text-gray-900">Evidence Details</h2>
            <p className="text-sm text-gray-500">
              View and edit evidence for {questionCode || 'this question'}
            </p>
          </div>
          <button
            onClick={handleCancel}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <X className="w-5 h-5 text-gray-500" />
          </button>
        </div>

        {/* Main Content */}
        <div className="flex flex-1 min-h-0">
          {/* Left Panel - File List */}
          <div className="w-[300px] border-r border-gray-200 flex flex-col">
            <div className="p-4 border-b border-gray-100">
              <h3 className="text-sm font-medium text-gray-700">Uploaded Files</h3>
              <p className="text-xs text-gray-500 mt-1">{evidenceFiles?.length || 0} file(s)</p>
            </div>
            <ScrollArea className="flex-1">
              <div className="p-2 space-y-1">
                {evidenceFiles?.map((file, index) => (
                  <div
                    key={file.evidence_id || index}
                    onClick={() => selectFile(file)}
                    className={`flex items-center p-3 rounded-lg cursor-pointer transition-colors ${
                      selectedFile?.evidence_id === file.evidence_id
                        ? 'bg-teal-50 border border-teal-200'
                        : 'hover:bg-gray-50 border border-transparent'
                    }`}
                  >
                    <div className={`w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0 ${
                      selectedFile?.evidence_id === file.evidence_id
                        ? 'bg-teal-100'
                        : 'bg-gray-100'
                    }`}>
                      <File className={`w-5 h-5 ${
                        selectedFile?.evidence_id === file.evidence_id
                          ? 'text-teal-600'
                          : 'text-gray-500'
                      }`} />
                    </div>
                    <div className="ml-3 flex-1 min-w-0">
                      <p className={`text-sm font-medium truncate ${
                        selectedFile?.evidence_id === file.evidence_id
                          ? 'text-teal-900'
                          : 'text-gray-900'
                      }`}>
                        {file.evidence_title || file.file_name || file.name}
                      </p>
                      <p className="text-xs text-gray-500 truncate">
                        {file.evidence_type || 'Unspecified'}
                      </p>
                    </div>
                    {selectedFile?.evidence_id === file.evidence_id && (
                      <Check className="w-4 h-4 text-teal-600 flex-shrink-0" />
                    )}
                  </div>
                ))}
              </div>
            </ScrollArea>
          </div>

          {/* Right Panel - Classification Settings */}
          <div className="flex-1 flex flex-col">
            {selectedFile ? (
              <>
                <div className="p-4 border-b border-gray-100">
                  <h3 className="text-sm font-medium text-gray-900">
                    {selectedFile.evidence_title || selectedFile.file_name || selectedFile.name}
                  </h3>
                  <p className="text-xs text-gray-500 mt-1">
                    Edit the classification settings for this evidence
                  </p>
                </div>
                <div className="flex-1 p-4 overflow-auto">
                  <div className="flex flex-col gap-3">
                    {renderOptionCard('Evidence Type', EVIDENCE_TYPE_OPTIONS, evidenceType, setEvidenceType)}
                    {renderOptionCard('Lifecycle Phase', LIFECYCLE_PHASE_OPTIONS, lifecyclePhase, setLifecyclePhase)}
                    {renderOptionCard('Trust Level', TRUST_LEVEL_OPTIONS, trustLevel, setTrustLevel)}
                    {renderOptionCard('Applies To Scope', APPLIES_TO_SCOPE_OPTIONS, appliesToScope, setAppliesToScope)}
                  </div>
                  
                  {/* Reusable Toggle */}
                  <div className="mt-4 pt-3 border-t border-gray-100">
                    <label 
                      className="flex items-center space-x-2 cursor-pointer"
                      onClick={() => handleSettingChange(setIsReusable, !isReusable)}
                    >
                      <div className={`w-5 h-5 rounded border-2 flex items-center justify-center transition-colors ${
                        isReusable 
                          ? 'bg-teal-600 border-teal-600' 
                          : 'border-gray-400 bg-white'
                      }`}>
                        {isReusable && (
                          <Check className="w-3 h-3 text-white" />
                        )}
                      </div>
                      <span className="text-sm text-gray-700">
                        Make this evidence reusable across other questions
                      </span>
                    </label>
                  </div>
                </div>
              </>
            ) : (
              <div className="flex-1 flex items-center justify-center">
                <p className="text-gray-500">Select a file to view its settings</p>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-gray-200 flex justify-end items-center space-x-3">
          <Button variant="outline" onClick={handleCancel} disabled={saving}>
            Cancel
          </Button>
          <Button
            onClick={handleSave}
            disabled={!selectedFile || saving || !hasChanges}
            className="bg-teal-600 hover:bg-teal-700 text-white"
          >
            {saving ? (
              <>
                <div className="w-4 h-4 mr-2 border-2 border-white border-t-transparent rounded-full animate-spin" />
                Saving...
              </>
            ) : (
              'Save'
            )}
          </Button>
        </div>
      </div>
    </>
  );
}

export default EvidenceDrawer;
