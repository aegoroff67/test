import React, { useState, useRef } from 'react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
  DialogDescription,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Upload, File, X, Check } from 'lucide-react';

// Evidence metadata options
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
  'Operational',
  'Approved',
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

function EvidenceUploadModal({ isOpen, onClose, onUpload, questionCode }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [evidenceType, setEvidenceType] = useState('');
  const [lifecyclePhase, setLifecyclePhase] = useState('');
  const [trustLevel, setTrustLevel] = useState('');
  const [appliesToScope, setAppliesToScope] = useState('');
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setSelectedFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleBrowseClick = () => {
    fileInputRef.current?.click();
  };

  const handleRemoveFile = () => {
    setSelectedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleUpload = () => {
    if (selectedFile) {
      const metadata = {
        evidenceType,
        lifecyclePhase,
        trustLevel,
        appliesToScope,
        questionCode
      };
      onUpload(selectedFile, metadata);
      handleClose();
    }
  };

  const handleClose = () => {
    setSelectedFile(null);
    setEvidenceType('');
    setLifecyclePhase('');
    setTrustLevel('');
    setAppliesToScope('');
    onClose();
  };

  const renderOptionCard = (title, options, selectedValue, onSelect) => (
    <Card className="w-full">
      <CardHeader className="py-2 px-4">
        <CardTitle className="text-sm font-semibold text-gray-900">{title}</CardTitle>
      </CardHeader>
      <CardContent className="py-2 px-4">
        <div className="flex flex-wrap gap-2">
          {options.map((option) => (
            <div
              key={option}
              onClick={() => onSelect(option)}
              className={`flex items-center space-x-1.5 px-2.5 py-1.5 rounded-md cursor-pointer transition-colors ${
                selectedValue === option
                  ? 'bg-teal-100 border border-teal-400'
                  : 'bg-gray-50 hover:bg-gray-100 border border-gray-200'
              }`}
            >
              <div
                className={`w-3 h-3 rounded-full border-2 flex items-center justify-center flex-shrink-0 ${
                  selectedValue === option
                    ? 'border-teal-600 bg-teal-600'
                    : 'border-gray-400'
                }`}
              >
                {selectedValue === option && (
                  <div className="w-1 h-1 rounded-full bg-white" />
                )}
              </div>
              <span className={`text-xs whitespace-nowrap ${selectedValue === option ? 'text-teal-900 font-medium' : 'text-gray-700'}`}>
                {option}
              </span>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );

  return (
    <Dialog open={isOpen} onOpenChange={handleClose}>
      <DialogContent className="w-[1500px] max-w-[95vw] h-[750px] max-h-[90vh] overflow-hidden flex flex-col">
        <DialogHeader>
          <DialogTitle className="text-lg font-semibold">Upload Evidence</DialogTitle>
          <DialogDescription className="text-sm text-gray-500">
            Upload supporting evidence and classify it for {questionCode || 'this question'}
          </DialogDescription>
        </DialogHeader>

        <div className="flex gap-6 flex-1 min-h-0 items-stretch">
          {/* Left Panel - File Upload */}
          <div className="flex-1 flex flex-col">
            <Label className="text-sm font-medium text-gray-700 mb-2">Select File</Label>
            <div
              className={`flex-1 border-2 border-dashed rounded-lg flex flex-col items-center justify-center p-6 transition-colors ${
                dragActive
                  ? 'border-teal-500 bg-teal-50'
                  : selectedFile
                  ? 'border-green-400 bg-green-50'
                  : 'border-gray-300 hover:border-gray-400 bg-gray-50'
              }`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              <input
                ref={fileInputRef}
                type="file"
                className="hidden"
                onChange={handleFileChange}
                accept=".pdf,.doc,.docx,.jpg,.jpeg,.png,.xlsx,.xls,.txt,.csv"
              />

              {selectedFile ? (
                <div className="text-center">
                  <div className="w-16 h-16 mx-auto mb-4 bg-green-100 rounded-full flex items-center justify-center">
                    <File className="w-8 h-8 text-green-600" />
                  </div>
                  <p className="text-sm font-medium text-gray-900 mb-1">{selectedFile.name}</p>
                  <p className="text-xs text-gray-500 mb-4">
                    {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleRemoveFile}
                    className="text-red-600 border-red-300 hover:bg-red-50"
                  >
                    <X className="w-4 h-4 mr-1" />
                    Remove File
                  </Button>
                </div>
              ) : (
                <div className="text-center">
                  <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
                    <Upload className="w-8 h-8 text-gray-400" />
                  </div>
                  <p className="text-sm font-medium text-gray-900 mb-1">
                    Drag and drop your file here
                  </p>
                  <p className="text-xs text-gray-500 mb-4">or</p>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleBrowseClick}
                    className="border-teal-300 text-teal-700 hover:bg-teal-50"
                  >
                    Browse Files
                  </Button>
                  <p className="text-xs text-gray-400 mt-4">
                    Supported: PDF, DOC, DOCX, JPG, PNG, XLSX, XLS, TXT, CSV
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Right Panel - Metadata Cards */}
          <div className="flex-1 flex flex-col">
            <Label className="text-sm font-medium text-gray-700 mb-2 h-5">Classify Evidence</Label>
            <div className="flex-1 flex flex-col gap-3">
              {renderOptionCard('Evidence Type', EVIDENCE_TYPE_OPTIONS, evidenceType, setEvidenceType)}
              {renderOptionCard('Lifecycle Phase', LIFECYCLE_PHASE_OPTIONS, lifecyclePhase, setLifecyclePhase)}
              {renderOptionCard('Trust Level', TRUST_LEVEL_OPTIONS, trustLevel, setTrustLevel)}
              {renderOptionCard('Applies To Scope', APPLIES_TO_SCOPE_OPTIONS, appliesToScope, setAppliesToScope)}
            </div>
          </div>
        </div>

        <DialogFooter className="mt-4">
          <Button variant="outline" onClick={handleClose}>
            Cancel
          </Button>
          <Button
            onClick={handleUpload}
            disabled={!selectedFile}
            className="bg-teal-600 hover:bg-teal-700 text-white"
          >
            <Check className="w-4 h-4 mr-2" />
            Upload Evidence
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

export default EvidenceUploadModal;
