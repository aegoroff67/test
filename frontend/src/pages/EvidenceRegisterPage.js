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
  ChevronDown
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
  
  // Filter states
  const [evidenceTypeFilter, setEvidenceTypeFilter] = useState('All Types');
  const [lifecycleFilter, setLifecycleFilter] = useState('All Phases');
  const [trustLevelFilter, setTrustLevelFilter] = useState('All Levels');
  const [scopeFilter, setScopeFilter] = useState('All Scopes');
  const [statusFilter, setStatusFilter] = useState('All Statuses');
  const [questionIdToCode, setQuestionIdToCode] = useState({}); // Map UUID -> question code
  
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

  // Filter evidence
  const filteredEvidence = evidence.filter(item => {
    const matchesSearch = searchTerm === '' || 
      (item.evidence_title || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
      (item.file_name || '').toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesType = evidenceTypeFilter === 'All Types' || item.evidence_type === evidenceTypeFilter;
    const matchesLifecycle = lifecycleFilter === 'All Phases' || item.lifecycle_phase === lifecycleFilter;
    const matchesTrust = trustLevelFilter === 'All Levels' || item.trust_level === trustLevelFilter;
    const matchesScope = scopeFilter === 'All Scopes' || item.applies_to_scope === scopeFilter;
    const matchesStatus = statusFilter === 'All Statuses' || item.status === statusFilter;
    
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
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <span className="text-sm font-medium text-gray-700">Filters:</span>
              
              {/* Evidence Type Filter */}
              <div className="relative">
                <select
                  value={evidenceTypeFilter}
                  onChange={(e) => setEvidenceTypeFilter(e.target.value)}
                  className="appearance-none bg-gray-50 border border-gray-200 rounded-md px-3 py-1.5 pr-8 text-xs text-gray-700 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                >
                  {EVIDENCE_TYPE_OPTIONS.map(option => (
                    <option key={option} value={option}>{option}</option>
                  ))}
                </select>
                <ChevronDown className="absolute right-2 top-1/2 transform -translate-y-1/2 h-3 w-3 text-gray-500 pointer-events-none" />
              </div>

              {/* Lifecycle Phase Filter */}
              <div className="relative">
                <select
                  value={lifecycleFilter}
                  onChange={(e) => setLifecycleFilter(e.target.value)}
                  className="appearance-none bg-gray-50 border border-gray-200 rounded-md px-3 py-1.5 pr-8 text-xs text-gray-700 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                >
                  {LIFECYCLE_PHASE_OPTIONS.map(option => (
                    <option key={option} value={option}>{option}</option>
                  ))}
                </select>
                <ChevronDown className="absolute right-2 top-1/2 transform -translate-y-1/2 h-3 w-3 text-gray-500 pointer-events-none" />
              </div>

              {/* Trust Level Filter */}
              <div className="relative">
                <select
                  value={trustLevelFilter}
                  onChange={(e) => setTrustLevelFilter(e.target.value)}
                  className="appearance-none bg-gray-50 border border-gray-200 rounded-md px-3 py-1.5 pr-8 text-xs text-gray-700 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                >
                  {TRUST_LEVEL_OPTIONS.map(option => (
                    <option key={option} value={option}>{option}</option>
                  ))}
                </select>
                <ChevronDown className="absolute right-2 top-1/2 transform -translate-y-1/2 h-3 w-3 text-gray-500 pointer-events-none" />
              </div>

              {/* Scope Filter */}
              <div className="relative">
                <select
                  value={scopeFilter}
                  onChange={(e) => setScopeFilter(e.target.value)}
                  className="appearance-none bg-gray-50 border border-gray-200 rounded-md px-3 py-1.5 pr-8 text-xs text-gray-700 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                >
                  {SCOPE_OPTIONS.map(option => (
                    <option key={option} value={option}>{option}</option>
                  ))}
                </select>
                <ChevronDown className="absolute right-2 top-1/2 transform -translate-y-1/2 h-3 w-3 text-gray-500 pointer-events-none" />
              </div>

              {/* Status Filter */}
              <div className="relative">
                <select
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                  className="appearance-none bg-gray-50 border border-gray-200 rounded-md px-3 py-1.5 pr-8 text-xs text-gray-700 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                >
                  {STATUS_OPTIONS.map(option => (
                    <option key={option} value={option}>{option}</option>
                  ))}
                </select>
                <ChevronDown className="absolute right-2 top-1/2 transform -translate-y-1/2 h-3 w-3 text-gray-500 pointer-events-none" />
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
