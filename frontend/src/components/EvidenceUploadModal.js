import React, { useState, useRef } from 'react';
import {
  Dialog,
  DialogContent,
  DialogFooter,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Upload, File, X, Check } from 'lucide-react';
import { toast } from 'sonner';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

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

// Reordered as requested
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

function EvidenceUploadModal({ isOpen, onClose, onUpload, questionCode, questionId, assessmentId, currentUser }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [dragActive, setDragActive] = useState(false);
  const [evidenceType, setEvidenceType] = useState('Unspecified');
  const [lifecyclePhase, setLifecyclePhase] = useState('Unspecified');
  const [trustLevel, setTrustLevel] = useState('Unspecified'); // Default selected
  const [appliesToScope, setAppliesToScope] = useState('Unspecified');
  const [isReusable, setIsReusable] = useState(false);
  const [uploading, setUploading] = useState(false);
  // Phase 1 new fields
  const [evidenceSummary, setEvidenceSummary] = useState('');
  const [limitations, setLimitations] = useState('');
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

  const handleUpload = async () => {
    if (!selectedFile) return;
    
    setUploading(true);
    
    try {
      // First, upload the file (you may need to implement file storage)
      // For now, we'll create a placeholder URL - in production this should upload to S3/cloud storage
      const fileUrl = `uploads/${Date.now()}_${selectedFile.name}`;
      
      // Create Evidence record via API
      // Use questionCode (e.g., "FA-1") for linked_question_ids, not the UUID
      // Include assessment_id to link evidence to specific assessment
      const evidenceData = {
        evidence_title: selectedFile.name,
        file_name: selectedFile.name,
        file_type: selectedFile.type || selectedFile.name.split('.').pop(),
        file_url: fileUrl,
        evidence_type: evidenceType || 'Unspecified',
        lifecycle_phase: lifecyclePhase || 'Unspecified',
        trust_level: trustLevel || 'Unspecified',
        applies_to_scope: appliesToScope || 'Unspecified',
        assessment_id: assessmentId,
        linked_question_ids: [questionCode],
        is_reusable: isReusable,
        notes: null,
        // Phase 1 new fields
        evidence_summary: evidenceSummary || null,
        limitations: limitations || null
      };
      
      const response = await axios.post(`${BACKEND_URL}/api/evidence`, evidenceData);
      
      if (response.data) {
        toast.success('Evidence uploaded successfully!');
        
        // Add to uploaded files list
        setUploadedFiles(prev => [...prev, {
          name: selectedFile.name,
          evidence_id: response.data.evidence_id,
          evidenceType: evidenceType
        }]);
        
        // Call the parent's onUpload callback with the file and metadata
        if (onUpload) {
          onUpload(selectedFile, {
            ...evidenceData,
            evidence_id: response.data.evidence_id
          });
        }
        
        // Reset for next upload (but keep modal open and keep uploaded files list)
        setSelectedFile(null);
        setEvidenceType('Unspecified');
        setLifecyclePhase('Unspecified');
        setTrustLevel('Unspecified');
        setAppliesToScope('Unspecified');
        setIsReusable(false);
        setEvidenceSummary('');
        setLimitations('');
        if (fileInputRef.current) {
          fileInputRef.current.value = '';
        }
      }
    } catch (error) {
      console.error('Error uploading evidence:', error);
      // Handle Pydantic validation errors which return as array of objects
      let errorMessage = 'Failed to upload evidence';
      if (error.response?.data?.detail) {
        const detail = error.response.data.detail;
        if (Array.isArray(detail)) {
          // Pydantic validation error - extract message from first error
          errorMessage = detail.map(err => err.msg || String(err)).join(', ');
        } else if (typeof detail === 'object') {
          // Single error object
          errorMessage = detail.msg || JSON.stringify(detail);
        } else {
          // String error message
          errorMessage = String(detail);
        }
      }
      toast.error(errorMessage);
    } finally {
      setUploading(false);
    }
  };

  const handleClose = () => {
    setSelectedFile(null);
    setUploadedFiles([]);
    setEvidenceType('Unspecified');
    setLifecyclePhase('Unspecified');
    setTrustLevel('Unspecified');
    setAppliesToScope('Unspecified');
    setIsReusable(false);
    setEvidenceSummary('');
    setLimitations('');
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
              onClick={() => onSelect(option)}
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

  return (
    <Dialog open={isOpen} onOpenChange={handleClose}>
      <DialogContent className="w-[1500px] max-w-[95vw] h-[750px] max-h-[90vh] overflow-hidden flex flex-col p-0">
        {/* Main content area - split into two halves from the top */}
        <div className="flex flex-1 min-h-0">
          {/* Left Panel - Upload Evidence */}
          <div className="flex-1 flex flex-col p-6 border-r border-gray-200">
            {/* Left Header with uploaded files */}
            <div className="mb-4">
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0">
                  <h2 className="text-lg font-semibold text-gray-900">Upload Evidence</h2>
                  <p className="text-sm text-gray-500">
                    Upload supporting evidence for {questionCode || 'this question'}
                  </p>
                </div>
                {/* Uploaded files list */}
                {uploadedFiles.length > 0 && (
                  <div className="flex-1 flex flex-wrap gap-2 items-start">
                    {uploadedFiles.map((file, index) => (
                      <div
                        key={index}
                        className="inline-flex items-center px-2.5 py-1 rounded-md bg-green-50 border border-green-200 text-xs"
                      >
                        <File className="w-3 h-3 text-green-600 mr-1.5" />
                        <span className="text-green-800 font-medium max-w-[150px] truncate">
                          {file.name}
                        </span>
                        <Check className="w-3 h-3 text-green-600 ml-1.5" />
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
            
            {/* File Upload Area */}
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
            
            {/* Phase 1: New Context Fields */}
            <div className="mt-4 space-y-3">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  What does this evidence demonstrate? <span className="text-gray-400 font-normal">(optional, max 500 chars)</span>
                </label>
                <textarea
                  value={evidenceSummary}
                  onChange={(e) => setEvidenceSummary(e.target.value.slice(0, 500))}
                  placeholder="Briefly describe what this evidence demonstrates about your AI governance..."
                  className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:ring-teal-500 focus:border-teal-500 resize-none"
                  rows={3}
                  maxLength={500}
                  data-testid="evidence-summary-input"
                />
                <div className="text-xs text-gray-400 text-right mt-1">{evidenceSummary.length}/500</div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Known limitations <span className="text-gray-400 font-normal">(optional, max 300 chars)</span>
                </label>
                <textarea
                  value={limitations}
                  onChange={(e) => setLimitations(e.target.value.slice(0, 300))}
                  placeholder="Note any limitations or caveats for this evidence..."
                  className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:ring-teal-500 focus:border-teal-500 resize-none"
                  rows={2}
                  maxLength={300}
                  data-testid="evidence-limitations-input"
                />
                <div className="text-xs text-gray-400 text-right mt-1">{limitations.length}/300</div>
              </div>
            </div>
          </div>

          {/* Right Panel - Classify Evidence */}
          <div className="flex-1 flex flex-col p-6">
            {/* Right Header */}
            <div className="mb-4">
              <h2 className="text-lg font-semibold text-gray-900">Classify Evidence</h2>
              <p className="text-sm text-gray-500">
                These classifications are optional and help improve reporting and traceability. You can skip this step or update it later.
              </p>
            </div>
            
            {/* Classification Cards */}
            <div className="flex flex-col gap-3 flex-1">
              {renderOptionCard('Evidence Type', EVIDENCE_TYPE_OPTIONS, evidenceType, setEvidenceType)}
              {renderOptionCard('Lifecycle Phase', LIFECYCLE_PHASE_OPTIONS, lifecyclePhase, setLifecyclePhase)}
              {renderOptionCard('Trust Level', TRUST_LEVEL_OPTIONS, trustLevel, setTrustLevel)}
              {renderOptionCard('Applies To Scope', APPLIES_TO_SCOPE_OPTIONS, appliesToScope, setAppliesToScope)}
            </div>
          </div>
        </div>

        {/* Footer */}
        <DialogFooter className="p-4 border-t border-gray-200 flex flex-row justify-between items-center sm:justify-between">
          {/* Reusable Toggle - Left side of footer */}
          <label 
            className="flex items-center space-x-2 cursor-pointer"
            onClick={() => setIsReusable(!isReusable)}
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
          
          {/* Buttons - Right side of footer */}
          <div className="flex items-center space-x-2">
            <Button variant="outline" onClick={handleClose} disabled={uploading}>
              Cancel
            </Button>
            <Button
              onClick={handleUpload}
              disabled={!selectedFile || uploading}
              className="bg-teal-600 hover:bg-teal-700 text-white"
            >
              {uploading ? (
                <>
                  <div className="w-4 h-4 mr-2 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Uploading...
                </>
              ) : (
                <>
                  <Check className="w-4 h-4 mr-2" />
                  Upload Evidence
                </>
              )}
            </Button>
          </div>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

export default EvidenceUploadModal;
