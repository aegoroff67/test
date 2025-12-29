import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { toast } from 'sonner';
import Logo from '../components/Logo';
import EvidenceDrawer from '../components/EvidenceDrawer';
import { 
  ArrowLeft, 
  FileText,
  Search,
  File,
  CheckCircle,
  Archive,
  Link2,
  ChevronDown,
  X
} from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Filter options (without "All" options - multi-select handles empty state)
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
  'Other',
  'Unspecified'
];

const LIFECYCLE_PHASE_OPTIONS = [
  'Design',
  'Development',
  'Testing',
  'Deployment',
  'Operation',
  'Monitoring',
  'Decommissioning',
  'Cross-Lifecycle',
  'Unspecified'
];

const TRUST_LEVEL_OPTIONS = [
  'Unspecified',
  'Draft',
  'Approved',
  'Operational',
  'Independently Reviewed',
  'Regulator / External Assured'
];

const SCOPE_OPTIONS = [
  'Organisation-wide',
  'Specific AI System',
  'Specific Model',
  'Specific Use Case',
  'Third Party / Vendor',
  'Unspecified'
];

const STATUS_OPTIONS = [
  'Active',
  'Archived'
];

function EvidenceRegisterPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [assessment, setAssessment] = useState(null);
  const [evidence, setEvidence] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  
  // Filter states (arrays for multi-select, empty = show all)
  const [evidenceTypeFilter, setEvidenceTypeFilter] = useState([]);
  const [lifecycleFilter, setLifecycleFilter] = useState([]);
  const [trustLevelFilter, setTrustLevelFilter] = useState([]);
  const [scopeFilter, setScopeFilter] = useState([]);
  const [statusFilter, setStatusFilter] = useState([]);
  const [linkedQuestionFilter, setLinkedQuestionFilter] = useState(''); // Single-select for linked questions
  const [questionIdToCode, setQuestionIdToCode] = useState({}); // Map UUID -> question code
  const [questionSummaries, setQuestionSummaries] = useState([]); // List of {code, summary, domain}
  
  // Dropdown open states
  const [openDropdown, setOpenDropdown] = useState(null);
  
  // Drawer states
  const [showDrawer, setShowDrawer] = useState(false);
  const [selectedEvidence, setSelectedEvidence] = useState(null);

  const fetchData = async () => {
    try {
      const token = localStorage.getItem('token');
      
      // Fetch assessment, questions, and evidence data in parallel
      const [assessmentRes, questionsRes, evidenceRes] = await Promise.all([
        axios.get(`${API}/assessments/${id}`, {
          headers: { Authorization: `Bearer ${token}` }
        }),
        axios.get(`${API}/assessments/${id}/questions`, {
          headers: { Authorization: `Bearer ${token}` }
        }),
        axios.get(`${API}/evidence`, {
          headers: { Authorization: `Bearer ${token}` }
        })
      ]);
      
      setAssessment(assessmentRes.data);
      
      // Build a map from question UUID to question code
      // Questions are nested inside domains: [{domain: {...}, questions: [...]}]
      const domainsWithQuestions = questionsRes.data || [];
      const idToCodeMap = {};
      const assessmentQuestionIds = new Set(); // Track all question IDs/codes for this assessment
      
      domainsWithQuestions.forEach(domainObj => {
        const questions = domainObj.questions || [];
        questions.forEach(q => {
          if (q.id && q.code) {
            idToCodeMap[q.id] = q.code;
            assessmentQuestionIds.add(q.id);
            assessmentQuestionIds.add(q.code);
          }
        });
      });
      setQuestionIdToCode(idToCodeMap);
      
      // Filter evidence to only show items linked to THIS assessment
      // Primary filter: assessment_id matches
      // Fallback filter: linked_question_ids contain questions from this assessment
      const allEvidence = evidenceRes.data || [];
      const filteredEvidence = allEvidence.filter(evidence => {
        // If evidence has assessment_id, use that for filtering (new evidence)
        if (evidence.assessment_id) {
          return evidence.assessment_id === id;
        }
        // Fallback: check linked question IDs (legacy evidence without assessment_id)
        const linkedIds = evidence.linked_question_ids || [];
        return linkedIds.some(linkedId => assessmentQuestionIds.has(linkedId));
      });
      
      setEvidence(filteredEvidence);
    } catch (error) {
      console.error('Error fetching data:', error);
      toast.error('Failed to load evidence data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [id]);

  // Handle row click to open drawer
  const handleRowClick = (evidenceItem) => {
    setSelectedEvidence(evidenceItem);
    setShowDrawer(true);
  };

  // Handle drawer update (refresh data)
  const handleDrawerUpdate = () => {
    fetchData();
  };

  // Calculate stats
  const stats = {
    totalEvidence: evidence.length,
    questionsCovered: new Set(evidence.flatMap(e => e.linked_question_ids || [])).size,
    reusable: evidence.filter(e => e.is_reusable).length,
    archived: evidence.filter(e => e.status === 'Archived').length
  };

  // Filter evidence (empty array = show all)
  const filteredEvidence = evidence.filter(item => {
    const matchesSearch = searchTerm === '' || 
      (item.evidence_title || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
      (item.file_name || '').toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesType = evidenceTypeFilter.length === 0 || evidenceTypeFilter.includes(item.evidence_type);
    const matchesLifecycle = lifecycleFilter.length === 0 || lifecycleFilter.includes(item.lifecycle_phase);
    const matchesTrust = trustLevelFilter.length === 0 || trustLevelFilter.includes(item.trust_level);
    const matchesScope = scopeFilter.length === 0 || scopeFilter.includes(item.applies_to_scope);
    const matchesStatus = statusFilter.length === 0 || statusFilter.includes(item.status);
    
    return matchesSearch && matchesType && matchesLifecycle && matchesTrust && matchesScope && matchesStatus;
  });

  // Truncate text helper
  const truncate = (text, maxLength) => {
    if (!text) return '';
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
  };

  // Convert linked question IDs (UUIDs or codes) to display-friendly question codes
  const getLinkedQuestionCodes = (linkedIds) => {
    if (!linkedIds || linkedIds.length === 0) return 'None';
    
    return linkedIds.map(id => {
      // If it's already a question code format (like FA-1, TR-4), return as-is
      if (id && /^[A-Z]{2,3}-\d+$/.test(id)) {
        return id;
      }
      // Otherwise, try to map UUID to code
      return questionIdToCode[id] || id;
    }).join(', ');
  };

  // Format date helper
  const formatDate = (dateString) => {
    if (!dateString) return '-';
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-GB', {
        day: '2-digit',
        month: 'short',
        year: 'numeric'
      });
    } catch {
      return '-';
    }
  };

  // Get file icon based on extension
  const getFileIcon = (fileName) => {
    const ext = (fileName || '').split('.').pop()?.toLowerCase();
    return <File className="h-4 w-4 text-blue-600" />;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="loading-spinner w-8 h-8 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading evidence register...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Top Header Section */}
      <div className="bg-white border-b shadow-sm">
        <div className="px-6 py-3">
          <div className="flex items-start justify-between">
            {/* Left Section: Logo + Title */}
            <div className="flex items-center space-x-3">
              <Logo size="sm" />
              <div>
                <h1 className="text-base font-bold text-gray-900">AM AI SAFE</h1>
                <p className="text-xs text-teal-600">Evidence Register</p>
              </div>
            </div>

            {/* Center Section: Title and Subtitle */}
            <div className="flex-1 flex flex-col items-center justify-center px-8">
              <h2 className="text-lg font-bold text-gray-900">Evidence Register</h2>
              <p className="text-sm text-gray-600">All evidence artefacts uploaded to support this assessment</p>
              <p className="text-xs text-gray-500 mt-1">{assessment?.name || 'Loading...'}</p>
            </div>

            {/* Right Section: Back Button */}
            <div className="flex items-center space-x-3">
              <Button 
                variant="outline" 
                size="sm"
                onClick={() => navigate(`/results/${id}`)}
              >
                <ArrowLeft className="h-4 w-4 mr-2" />
                Back to Results
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Panel */}
      <div className="bg-white border-b">
        <div className="px-6 py-3">
          <div className="flex items-center justify-center space-x-8">
            <div className="flex items-center space-x-2">
              <FileText className="h-4 w-4 text-teal-600" />
              <span className="text-sm font-semibold text-gray-900">{stats.totalEvidence} Evidence Artefacts</span>
            </div>
            <div className="h-4 w-px bg-gray-300" />
            <div className="flex items-center space-x-2">
              <Link2 className="h-4 w-4 text-blue-600" />
              <span className="text-sm font-semibold text-gray-900">{stats.questionsCovered} Questions Covered</span>
            </div>
            <div className="h-4 w-px bg-gray-300" />
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-4 w-4 text-green-600" />
              <span className="text-sm font-semibold text-gray-900">{stats.reusable} Reusable</span>
            </div>
            <div className="h-4 w-px bg-gray-300" />
            <div className="flex items-center space-x-2">
              <Archive className="h-4 w-4 text-gray-500" />
              <span className="text-sm font-semibold text-gray-900">{stats.archived} Archived</span>
            </div>
          </div>
        </div>
      </div>

      {/* Filters Panel */}
      <div className="bg-white border-b">
        <div className="px-6 py-3">
          <div className="flex flex-col space-y-3">
            {/* Filter dropdowns row */}
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <span className="text-sm font-medium text-gray-700">Filters:</span>
                
                {/* Evidence Type Multi-Select */}
                <div className="relative">
                  <button
                    onClick={() => setOpenDropdown(openDropdown === 'type' ? null : 'type')}
                    className="flex items-center justify-between min-w-[140px] bg-gray-50 border border-gray-200 rounded-md px-3 py-1.5 text-xs text-gray-700 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-teal-500"
                  >
                    <span>{evidenceTypeFilter.length === 0 ? 'Evidence Type' : `${evidenceTypeFilter.length} selected`}</span>
                    <ChevronDown className="ml-2 h-3 w-3 text-gray-500" />
                  </button>
                  {openDropdown === 'type' && (
                    <div className="absolute z-50 mt-1 w-56 bg-white border border-gray-200 rounded-md shadow-lg max-h-60 overflow-auto">
                      {EVIDENCE_TYPE_OPTIONS.map(option => (
                        <label key={option} className="flex items-center px-3 py-2 hover:bg-gray-50 cursor-pointer">
                          <input
                            type="checkbox"
                            checked={evidenceTypeFilter.includes(option)}
                            onChange={(e) => {
                              if (e.target.checked) {
                                setEvidenceTypeFilter([...evidenceTypeFilter, option]);
                              } else {
                                setEvidenceTypeFilter(evidenceTypeFilter.filter(v => v !== option));
                              }
                            }}
                            className="h-3.5 w-3.5 text-teal-600 rounded border-gray-300 focus:ring-teal-500"
                          />
                          <span className="ml-2 text-xs text-gray-700">{option}</span>
                        </label>
                      ))}
                    </div>
                  )}
                </div>

                {/* Lifecycle Phase Multi-Select */}
                <div className="relative">
                  <button
                    onClick={() => setOpenDropdown(openDropdown === 'lifecycle' ? null : 'lifecycle')}
                    className="flex items-center justify-between min-w-[140px] bg-gray-50 border border-gray-200 rounded-md px-3 py-1.5 text-xs text-gray-700 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-teal-500"
                  >
                    <span>{lifecycleFilter.length === 0 ? 'Lifecycle Phase' : `${lifecycleFilter.length} selected`}</span>
                    <ChevronDown className="ml-2 h-3 w-3 text-gray-500" />
                  </button>
                  {openDropdown === 'lifecycle' && (
                    <div className="absolute z-50 mt-1 w-48 bg-white border border-gray-200 rounded-md shadow-lg max-h-60 overflow-auto">
                      {LIFECYCLE_PHASE_OPTIONS.map(option => (
                        <label key={option} className="flex items-center px-3 py-2 hover:bg-gray-50 cursor-pointer">
                          <input
                            type="checkbox"
                            checked={lifecycleFilter.includes(option)}
                            onChange={(e) => {
                              if (e.target.checked) {
                                setLifecycleFilter([...lifecycleFilter, option]);
                              } else {
                                setLifecycleFilter(lifecycleFilter.filter(v => v !== option));
                              }
                            }}
                            className="h-3.5 w-3.5 text-teal-600 rounded border-gray-300 focus:ring-teal-500"
                          />
                          <span className="ml-2 text-xs text-gray-700">{option}</span>
                        </label>
                      ))}
                    </div>
                  )}
                </div>

                {/* Trust Level Multi-Select */}
                <div className="relative">
                  <button
                    onClick={() => setOpenDropdown(openDropdown === 'trust' ? null : 'trust')}
                    className="flex items-center justify-between min-w-[130px] bg-gray-50 border border-gray-200 rounded-md px-3 py-1.5 text-xs text-gray-700 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-teal-500"
                  >
                    <span>{trustLevelFilter.length === 0 ? 'Trust Level' : `${trustLevelFilter.length} selected`}</span>
                    <ChevronDown className="ml-2 h-3 w-3 text-gray-500" />
                  </button>
                  {openDropdown === 'trust' && (
                    <div className="absolute z-50 mt-1 w-56 bg-white border border-gray-200 rounded-md shadow-lg max-h-60 overflow-auto">
                      {TRUST_LEVEL_OPTIONS.map(option => (
                        <label key={option} className="flex items-center px-3 py-2 hover:bg-gray-50 cursor-pointer">
                          <input
                            type="checkbox"
                            checked={trustLevelFilter.includes(option)}
                            onChange={(e) => {
                              if (e.target.checked) {
                                setTrustLevelFilter([...trustLevelFilter, option]);
                              } else {
                                setTrustLevelFilter(trustLevelFilter.filter(v => v !== option));
                              }
                            }}
                            className="h-3.5 w-3.5 text-teal-600 rounded border-gray-300 focus:ring-teal-500"
                          />
                          <span className="ml-2 text-xs text-gray-700">{option}</span>
                        </label>
                      ))}
                    </div>
                  )}
                </div>

                {/* Scope Multi-Select */}
                <div className="relative">
                  <button
                    onClick={() => setOpenDropdown(openDropdown === 'scope' ? null : 'scope')}
                    className="flex items-center justify-between min-w-[130px] bg-gray-50 border border-gray-200 rounded-md px-3 py-1.5 text-xs text-gray-700 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-teal-500"
                  >
                    <span>{scopeFilter.length === 0 ? 'Scope' : `${scopeFilter.length} selected`}</span>
                    <ChevronDown className="ml-2 h-3 w-3 text-gray-500" />
                  </button>
                  {openDropdown === 'scope' && (
                    <div className="absolute z-50 mt-1 w-48 bg-white border border-gray-200 rounded-md shadow-lg max-h-60 overflow-auto">
                      {SCOPE_OPTIONS.map(option => (
                        <label key={option} className="flex items-center px-3 py-2 hover:bg-gray-50 cursor-pointer">
                          <input
                            type="checkbox"
                            checked={scopeFilter.includes(option)}
                            onChange={(e) => {
                              if (e.target.checked) {
                                setScopeFilter([...scopeFilter, option]);
                              } else {
                                setScopeFilter(scopeFilter.filter(v => v !== option));
                              }
                            }}
                            className="h-3.5 w-3.5 text-teal-600 rounded border-gray-300 focus:ring-teal-500"
                          />
                          <span className="ml-2 text-xs text-gray-700">{option}</span>
                        </label>
                      ))}
                    </div>
                  )}
                </div>

                {/* Status Multi-Select */}
                <div className="relative">
                  <button
                    onClick={() => setOpenDropdown(openDropdown === 'status' ? null : 'status')}
                    className="flex items-center justify-between min-w-[110px] bg-gray-50 border border-gray-200 rounded-md px-3 py-1.5 text-xs text-gray-700 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-teal-500"
                  >
                    <span>{statusFilter.length === 0 ? 'Status' : `${statusFilter.length} selected`}</span>
                    <ChevronDown className="ml-2 h-3 w-3 text-gray-500" />
                  </button>
                  {openDropdown === 'status' && (
                    <div className="absolute z-50 mt-1 w-36 bg-white border border-gray-200 rounded-md shadow-lg max-h-60 overflow-auto">
                      {STATUS_OPTIONS.map(option => (
                        <label key={option} className="flex items-center px-3 py-2 hover:bg-gray-50 cursor-pointer">
                          <input
                            type="checkbox"
                            checked={statusFilter.includes(option)}
                            onChange={(e) => {
                              if (e.target.checked) {
                                setStatusFilter([...statusFilter, option]);
                              } else {
                                setStatusFilter(statusFilter.filter(v => v !== option));
                              }
                            }}
                            className="h-3.5 w-3.5 text-teal-600 rounded border-gray-300 focus:ring-teal-500"
                          />
                          <span className="ml-2 text-xs text-gray-700">{option}</span>
                        </label>
                      ))}
                    </div>
                  )}
                </div>
              </div>

              {/* Search */}
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <Input
                  type="text"
                  placeholder="Search evidence..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-9 pr-4 py-1.5 w-64 text-sm border-gray-200 focus:ring-teal-500"
                />
              </div>
            </div>

            {/* Selected filter chips */}
            {(evidenceTypeFilter.length > 0 || lifecycleFilter.length > 0 || trustLevelFilter.length > 0 || scopeFilter.length > 0 || statusFilter.length > 0) && (
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-xs text-gray-500">Active filters:</span>
                
                {/* Evidence Type chips */}
                {evidenceTypeFilter.map(value => (
                  <span key={`type-${value}`} className="inline-flex items-center px-2 py-0.5 rounded-full text-xs bg-teal-50 text-teal-700 border border-teal-200">
                    {value}
                    <button
                      onClick={() => setEvidenceTypeFilter(evidenceTypeFilter.filter(v => v !== value))}
                      className="ml-1 hover:text-teal-900"
                    >
                      <X className="h-3 w-3" />
                    </button>
                  </span>
                ))}
                
                {/* Lifecycle chips */}
                {lifecycleFilter.map(value => (
                  <span key={`lifecycle-${value}`} className="inline-flex items-center px-2 py-0.5 rounded-full text-xs bg-blue-50 text-blue-700 border border-blue-200">
                    {value}
                    <button
                      onClick={() => setLifecycleFilter(lifecycleFilter.filter(v => v !== value))}
                      className="ml-1 hover:text-blue-900"
                    >
                      <X className="h-3 w-3" />
                    </button>
                  </span>
                ))}
                
                {/* Trust Level chips */}
                {trustLevelFilter.map(value => (
                  <span key={`trust-${value}`} className="inline-flex items-center px-2 py-0.5 rounded-full text-xs bg-purple-50 text-purple-700 border border-purple-200">
                    {value}
                    <button
                      onClick={() => setTrustLevelFilter(trustLevelFilter.filter(v => v !== value))}
                      className="ml-1 hover:text-purple-900"
                    >
                      <X className="h-3 w-3" />
                    </button>
                  </span>
                ))}
                
                {/* Scope chips */}
                {scopeFilter.map(value => (
                  <span key={`scope-${value}`} className="inline-flex items-center px-2 py-0.5 rounded-full text-xs bg-amber-50 text-amber-700 border border-amber-200">
                    {value}
                    <button
                      onClick={() => setScopeFilter(scopeFilter.filter(v => v !== value))}
                      className="ml-1 hover:text-amber-900"
                    >
                      <X className="h-3 w-3" />
                    </button>
                  </span>
                ))}
                
                {/* Status chips */}
                {statusFilter.map(value => (
                  <span key={`status-${value}`} className="inline-flex items-center px-2 py-0.5 rounded-full text-xs bg-gray-100 text-gray-700 border border-gray-300">
                    {value}
                    <button
                      onClick={() => setStatusFilter(statusFilter.filter(v => v !== value))}
                      className="ml-1 hover:text-gray-900"
                    >
                      <X className="h-3 w-3" />
                    </button>
                  </span>
                ))}
                
                {/* Clear all button */}
                <button
                  onClick={() => {
                    setEvidenceTypeFilter([]);
                    setLifecycleFilter([]);
                    setTrustLevelFilter([]);
                    setScopeFilter([]);
                    setStatusFilter([]);
                  }}
                  className="text-xs text-gray-500 hover:text-gray-700 underline ml-2"
                >
                  Clear all
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Main Evidence Table */}
      <div className="flex-1 px-6 py-4 overflow-auto">
        <Card>
          <CardContent className="p-0">
            {/* Table Header */}
            <div className="grid grid-cols-24 gap-2 px-4 py-3 bg-gray-50 border-b text-xs font-semibold text-gray-600 uppercase tracking-wider">
              <div className="col-span-5">Evidence</div>
              <div className="col-span-3">Type</div>
              <div className="col-span-3">Lifecycle</div>
              <div className="col-span-2">Trust</div>
              <div className="col-span-3">Scope</div>
              <div className="col-span-3">Linked Questions</div>
              <div className="col-span-2 text-center">Reusable</div>
              <div className="col-span-1">Status</div>
              <div className="col-span-2">Last Updated</div>
            </div>

            {/* Table Body */}
            <div className="divide-y divide-gray-100">
              {filteredEvidence.length === 0 ? (
                <div className="px-4 py-12 text-center">
                  <FileText className="h-12 w-12 text-gray-300 mx-auto mb-3" />
                  <p className="text-gray-500 text-sm">No evidence artefacts found</p>
                  <p className="text-gray-400 text-xs mt-1">Upload evidence during the assessment to see it here</p>
                </div>
              ) : (
                filteredEvidence.map((item, index) => (
                  <div 
                    key={item.evidence_id || index} 
                    onClick={() => handleRowClick(item)}
                    className="grid grid-cols-24 gap-2 px-4 py-3 hover:bg-teal-50 transition-colors items-center cursor-pointer"
                  >
                    {/* Evidence Name */}
                    <div className="col-span-5">
                      <div className="flex items-center space-x-2">
                        {getFileIcon(item.file_name)}
                        <p className="text-xs font-medium text-gray-900 truncate">
                          {item.evidence_title || item.file_name || 'Untitled'}
                        </p>
                      </div>
                    </div>

                    {/* Type */}
                    <div className="col-span-3">
                      <span className="text-xs text-gray-700">
                        {truncate(item.evidence_type || 'Unspecified', 18)}
                      </span>
                    </div>

                    {/* Lifecycle */}
                    <div className="col-span-3">
                      <span className="text-xs text-gray-700">
                        {truncate(item.lifecycle_phase || 'Unspecified', 15)}
                      </span>
                    </div>

                    {/* Trust */}
                    <div className="col-span-2">
                      <span className="text-xs text-gray-700">
                        {truncate(item.trust_level || 'Unspecified', 12)}
                      </span>
                    </div>

                    {/* Scope */}
                    <div className="col-span-3">
                      <span className="text-xs text-gray-700">
                        {truncate(item.applies_to_scope || 'Unspecified', 15)}
                      </span>
                    </div>

                    {/* Linked Questions */}
                    <div className="col-span-3">
                      <span className="text-xs text-teal-600 font-medium">
                        {getLinkedQuestionCodes(item.linked_question_ids)}
                      </span>
                    </div>

                    {/* Reusable */}
                    <div className="col-span-2 flex justify-center">
                      {item.is_reusable && (
                        <CheckCircle className="h-4 w-4 text-green-500" title="Reusable" />
                      )}
                    </div>

                    {/* Status */}
                    <div className="col-span-1">
                      <span className={`text-xs font-medium ${
                        item.status === 'Archived' ? 'text-gray-500' : 'text-green-600'
                      }`}>
                        {item.status || 'Active'}
                      </span>
                    </div>

                    {/* Last Updated */}
                    <div className="col-span-2">
                      <span className="text-xs text-gray-500">
                        {formatDate(item.last_updated_date || item.uploaded_date)}
                      </span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Evidence Drawer */}
      <EvidenceDrawer
        isOpen={showDrawer}
        onClose={() => setShowDrawer(false)}
        evidence={selectedEvidence}
        onUpdate={handleDrawerUpdate}
        questionIdToCode={questionIdToCode}
        mode="view"
      />
    </div>
  );
}

export default EvidenceRegisterPage;
