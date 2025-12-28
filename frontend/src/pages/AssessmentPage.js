import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { toast } from 'sonner';
import Logo from '../components/Logo';
import { 
  ArrowLeft, 
  ArrowRight, 
  Home, 
  CheckCircle2, 
  Circle,
  Grid3X3,
  HelpCircle,
  Save,
  BarChart3,
  Paperclip,
  Upload,
  X
} from 'lucide-react';
import AssessmentStatusView from '../components/AssessmentStatusView';
import AssessmentFrameworkView from '../components/AssessmentFrameworkView';
import InfoBadge from '../components/InfoBadge';
import NistAlignmentModal from '../components/NistAlignmentModal';
import AuEthicsAlignmentModal from '../components/AuEthicsAlignmentModal';
import AuGuidanceAlignmentModal from '../components/AuGuidanceAlignmentModal';
import EuAiActAlignmentModal from '../components/EuAiActAlignmentModal';
import Iso42001AlignmentModal from '../components/Iso42001AlignmentModal';
import AuAssuranceAlignmentModal from '../components/AuAssuranceAlignmentModal';
import SingaporeMafAlignmentModal from '../components/SingaporeMafAlignmentModal';
import OecdPrinciplesAlignmentModal from '../components/OecdPrinciplesAlignmentModal';
import nistAlignmentData from '../data/nistAlignmentData.json';
import iso42001AlignmentData from '../data/iso42001AlignmentData.json';
import auEthicsAlignmentData from '../data/auEthicsAlignmentData.json';
import auGuidanceAlignmentData from '../data/auGuidanceAlignmentData.json';
import auAssuranceAlignmentData from '../data/auAssuranceAlignmentData.json';
import singaporeMafAlignmentData from '../data/singaporeMafAlignmentData.json';
import oecdPrinciplesAlignmentData from '../data/oecdPrinciplesAlignmentData.json';
import euAiActAlignmentData from '../data/euAiActAlignmentData.json';

// Framework configuration - centralizes all framework modal setup
const FRAMEWORK_CONFIG = {
  nist: {
    id: 'nist',
    name: 'NIST AI RMF',
    component: NistAlignmentModal,
    data: nistAlignmentData,
    color: 'indigo'
  },
  iso42001: {
    id: 'iso42001',
    name: 'ISO/IEC 42001',
    component: Iso42001AlignmentModal,
    data: iso42001AlignmentData,
    color: 'teal'
  },
  auEthics: {
    id: 'auEthics',
    name: 'Australian AI Ethics',
    component: AuEthicsAlignmentModal,
    data: auEthicsAlignmentData,
    color: 'green'
  },
  auGuidance: {
    id: 'auGuidance',
    name: 'Australian Guidance',
    component: AuGuidanceAlignmentModal,
    data: auGuidanceAlignmentData,
    color: 'blue'
  },
  euAiAct: {
    id: 'euAiAct',
    name: 'EU AI Act',
    component: EuAiActAlignmentModal,
    data: euAiActAlignmentData,
    color: 'purple'
  },
  auAssurance: {
    id: 'auAssurance',
    name: 'AU Assurance',
    component: AuAssuranceAlignmentModal,
    data: auAssuranceAlignmentData,
    color: 'orange'
  },
  singaporeMaf: {
    id: 'singaporeMaf',
    name: 'Singapore MAF',
    component: SingaporeMafAlignmentModal,
    data: singaporeMafAlignmentData,
    color: 'rose'
  },
  oecdPrinciples: {
    id: 'oecdPrinciples',
    name: 'OECD Principles',
    component: OecdPrinciplesAlignmentModal,
    data: oecdPrinciplesAlignmentData,
    color: 'slate'
  }
};
import HelpModal from '../components/HelpModal';
import EvidenceUploadModal from '../components/EvidenceUploadModal';
import { helpContent } from '../data/helpContent';
import questionGuidanceData from '../data/questionGuidance.json';
import { getResponseOptions, getColorScheme } from './AssessmentPage_awareness_support';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Answer options will be dynamically loaded from question data

function AssessmentPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [assessment, setAssessment] = useState(null);
  const [assessmentType, setAssessmentType] = useState('System');
  const [questions, setQuestions] = useState([]);
  const [domains, setDomains] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [note, setNote] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [showStatusView, setShowStatusView] = useState(false);
  const [otherText, setOtherText] = useState('');
  const [adminScore, setAdminScore] = useState(null);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [showHelpModal, setShowHelpModal] = useState(false);
  const [currentHelpContent, setCurrentHelpContent] = useState(null);
  const [skipAutoNavigation, setSkipAutoNavigation] = useState(false);
  const [showEvidenceModal, setShowEvidenceModal] = useState(false);
  
  // Unified framework modal state - replaces 18 individual state variables
  const [activeFrameworkModal, setActiveFrameworkModal] = useState(null);
  
  // Track which frameworks are selected for this assessment
  const [selectedFrameworks, setSelectedFrameworks] = useState({
    nist: false,
    iso42001: false,
    auEthics: false,
    auGuidance: false,
    euAiAct: false,
    auAssurance: false,
    singaporeMaf: false,
    oecdPrinciples: false
  });
  
  // State for framework alignment view
  const [showFrameworkView, setShowFrameworkView] = useState(false);

  useEffect(() => {
    fetchAssessment();
  }, [id]);

  const fetchAssessment = async (skipNav = false) => {
    try {
      // Fetch assessment metadata
      const assessmentResponse = await axios.get(`${API}/assessments/${id}`);
      setAssessment(assessmentResponse.data);
      setAssessmentType(assessmentResponse.data.assessment_type || 'System');
      
      // Check which frameworks are selected in system_info
      const systemInfo = assessmentResponse.data.system_info || {};
      const frameworks = systemInfo.frameworks || [];
      
      // Update selected frameworks using unified state
      setSelectedFrameworks({
        nist: frameworks.includes("NIST AI RMF (2023)"),
        iso42001: frameworks.includes("AS ISO/IEC 42001:2023"),
        auEthics: frameworks.includes("Australian AI Ethics Principles (2024)"),
        auGuidance: frameworks.includes("Australian Guidance for AI Adoption (2025)"),
        auAssurance: frameworks.includes("Australian National Framework for the Assurance of AI in Government (2024)"),
        singaporeMaf: frameworks.includes("Singapore MAF (2024)"),
        oecdPrinciples: frameworks.includes("OECD Principles (2019)"),
        euAiAct: frameworks.includes("EU AI Act (2024 final)")
      });
      
      // Fetch questions with domains and answers
      const questionsResponse = await axios.get(`${API}/assessments/${id}/questions`);
      const domainQuestionData = questionsResponse.data;
      
      // Extract domains and flatten questions
      const domainsData = [];
      const questionsData = [];
      
      domainQuestionData.forEach(dq => {
        domainsData.push(dq.domain);
        questionsData.push(...dq.questions);
      });
      
      setDomains(domainsData);
      setQuestions(questionsData);
      
      // Build answers map
      const answersMap = {};
      questionsData.forEach(q => {
        if (q.answer) {
          answersMap[q.id] = {
            option: q.answer.option,
            note: q.answer.note || '',
            other_text: q.answer.other_text || '',
            review_status: q.answer.review_status || 'APPROVED'
          };
        }
      });
      setAnswers(answersMap);
      
      // Check if this is a pending review assessment (only if not skipping auto-navigation)
      if (!skipNav && assessmentResponse.data.pending_review_count > 0 && user?.role === 'SUPER_ADMIN') {
        // Get first pending review question
        try {
          const pendingResponse = await axios.get(`${API}/assessments/${id}/first-pending-question`);
          if (pendingResponse.data.question_id) {
            const pendingIndex = questionsData.findIndex(q => q.id === pendingResponse.data.question_id);
            if (pendingIndex >= 0) {
              setCurrentQuestionIndex(pendingIndex);
              setLoading(false);
              return; // Exit early, we found the pending question
            }
          }
        } catch (err) {
          console.error('Error fetching first pending question:', err);
        }
      }
      
      // Set current question (first unanswered or first question) - only if not skipping
      if (!skipNav) {
        const firstUnanswered = questionsData.findIndex(q => !q.answer);
        setCurrentQuestionIndex(firstUnanswered >= 0 ? firstUnanswered : 0);
      }
      
    } catch (error) {
      console.error('Error loading assessment:', error);
      toast.error('Failed to load assessment');
      navigate('/dashboard');
    } finally {
      setLoading(false);
    }
  };

  const currentQuestion = questions[currentQuestionIndex];
  const currentAnswer = currentQuestion ? answers[currentQuestion.id] : null;
  
  // Get dynamic response options and color scheme based on assessment type
  const responseOptions = currentQuestion ? getResponseOptions(assessmentType, currentQuestion.predefined_answers) : [];
  const colors = getColorScheme(assessmentType);

  useEffect(() => {
    if (currentAnswer) {
      setNote(currentAnswer.note || '');
      setOtherText(currentAnswer.other_text || '');
      // Reset uploaded files for new question (files are per-question)
      setUploadedFiles([]);
    } else {
      setNote('');
      setOtherText('');
      setUploadedFiles([]);
    }
  }, [currentQuestionIndex, currentAnswer]);

  const saveAnswer = async (option, noteText = note, otherTextValue = '') => {
    if (!currentQuestion) return;
    
    setSaving(true);
    try {
      const payload = {
        question_id: currentQuestion.id,
        option: option,
        note: noteText || null
      };
      
      if (option === 'OTHER') {
        payload.other_text = otherTextValue;
      }
      
      const response = await axios.post(`${API}/assessments/${id}/answer`, payload);
      
      // Upload files if any are selected
      if (uploadedFiles.length > 0) {
        await saveFilesWithAnswer(option, uploadedFiles);
      }
      
      // Update local state
      setAnswers(prev => ({
        ...prev,
        [currentQuestion.id]: {
          option: option,
          note: noteText || '',
          other_text: otherTextValue || '',
          needs_review: response.data.needs_review || false,
          evidence_files: uploadedFiles.length
        }
      }));
      
      if (response.data.needs_review) {
        toast.success('Answer saved and flagged for review!');
      } else {
        toast.success('Answer saved!');
      }
    } catch (error) {
      // Handle validation errors from backend
      let errorMessage = 'Failed to save answer';
      if (error.response?.data?.detail) {
        if (Array.isArray(error.response.data.detail)) {
          // Pydantic validation error
          errorMessage = error.response.data.detail.map(err => err.msg).join(', ');
        } else if (typeof error.response.data.detail === 'string') {
          errorMessage = error.response.data.detail;
        }
      }
      toast.error(errorMessage);
    } finally {
      setSaving(false);
    }
  };

  const handleOptionSelect = async (option) => {
    if (option === 'OTHER' && (!otherText || !otherText.trim())) {
      toast.error('Please provide text for the "Other" option');
      return;
    }
    await saveAnswer(option, note, otherText);
  };

  const handleSaveAdminScore = async () => {
    if (adminScore === null || adminScore === undefined) {
      toast.error('Please select a score');
      return;
    }

    try {
      const answerId = currentQuestion?.answer?.id;
      if (!answerId) {
        toast.error('No answer found to score');
        return;
      }

      await axios.put(
        `${API}/admin/assessments/${id}/answers/${answerId}/score`,
        null,
        { params: { score: adminScore } }
      );

      toast.success('Score saved successfully!');
      
      // Reset admin score
      setAdminScore(null);
      
      // Refresh assessment data to update pending count (skip auto-navigation)
      await fetchAssessment(true);
      
      // Now manually navigate to next pending question
      try {
        const pendingResponse = await axios.get(`${API}/assessments/${id}/first-pending-question`);
        if (pendingResponse.data.question_id) {
          // Find the index of this question
          const pendingIndex = questions.findIndex(q => q.id === pendingResponse.data.question_id);
          if (pendingIndex >= 0) {
            setCurrentQuestionIndex(pendingIndex);
            return;
          }
        }
        // If no more pending questions, we're done - submit button will show
        toast.success('All pending reviews have been scored!');
      } catch (err) {
        console.error('Error finding next pending question:', err);
      }
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to save score');
    }
  };

  // Check if current domain is complete
  const isCurrentDomainComplete = () => {
    if (!currentQuestion || !questions.length) return false;
    
    const currentDomainId = currentQuestion.domain_id;
    const domainQuestions = questions.filter(q => q.domain_id === currentDomainId);
    const domainAnswers = domainQuestions.filter(q => answers[q.id]);
    
    return domainAnswers.length === domainQuestions.length;
  };

  // Get next question (domain-aware)
  const getNextQuestion = () => {
    if (currentQuestionIndex >= questions.length - 1) return null;
    
    const currentDomainId = currentQuestion.domain_id;
    const nextQuestion = questions[currentQuestionIndex + 1];
    
    // If still in same domain or domain is complete, move to next question
    if (nextQuestion.domain_id === currentDomainId || isCurrentDomainComplete()) {
      return currentQuestionIndex + 1;
    }
    
    // If domain not complete, find next unanswered question in current domain
    const currentDomainQuestions = questions.filter(q => q.domain_id === currentDomainId);
    const nextUnansweredInDomain = currentDomainQuestions.find(q => !answers[q.id]);
    
    if (nextUnansweredInDomain) {
      return questions.findIndex(q => q.id === nextUnansweredInDomain.id);
    }
    
    return currentQuestionIndex + 1;
  };

  const handleNoteChange = (value) => {
    setNote(value);
  };

  const handleOpenHelp = () => {
    if (currentQuestion && currentQuestion.code) {
      // For all assessment types, use evidence_types from the API response
      // Fallback to helpContent (static JSON) for backwards compatibility
      let content = null;
      
      if (currentQuestion.evidence_types) {
        content = currentQuestion.evidence_types;
      } else {
        content = helpContent[currentQuestion.code];
      }
      
      setCurrentHelpContent({
        title: `Help: ${currentQuestion.code} - Evidence Types`,
        content: content || null
      });
      setShowHelpModal(true);
    }
  };

  // Generic framework modal handlers - replaces 18 individual functions
  const handleOpenFrameworkModal = (frameworkId) => {
    setActiveFrameworkModal(frameworkId);
  };

  const handleCloseFrameworkModal = () => {
    setActiveFrameworkModal(null);
  };

  const handleOpenQuestionHelp = () => {
    // Show additional guidance for the current question
    if (currentQuestion && currentQuestion.code) {
      // Try to get additional guidance from the API response first
      // This works for all assessment types (System, Readiness, Organisation)
      let guidance = currentQuestion.additional_guidance || currentQuestion.additional_guide;
      
      // Fallback to static JSON for backwards compatibility
      if (!guidance) {
        guidance = questionGuidanceData[currentQuestion.code];
      }
      
      if (guidance) {
        setCurrentHelpContent({
          title: `${currentQuestion.code} - Additional Guidance`,
          content: guidance
        });
        setShowHelpModal(true);
      } else {
        toast.info('No additional guidance available for this question.');
      }
    }
  };

  const handleFileUpload = async (files, metadata = null) => {
    // Handle both direct file input and modal upload
    const fileList = files instanceof File ? [files] : (files ? Array.from(files) : []);
    if (!fileList || fileList.length === 0) return;
    
    // Validate file sizes (max 10MB per file)
    const maxSize = 10 * 1024 * 1024; // 10MB
    const oversizedFiles = fileList.filter(file => file.size > maxSize);
    
    if (oversizedFiles.length > 0) {
      toast.error(`Some files are too large. Maximum size is 10MB per file.`);
      return;
    }
    
    // Store metadata with the file if provided
    const filesWithMetadata = fileList.map(file => {
      if (metadata) {
        file.metadata = metadata;
      }
      return file;
    });
    
    // Add to uploaded files state
    setUploadedFiles(prev => [...prev, ...filesWithMetadata]);
    
    // If there's already an answer, save the files with it
    if (currentAnswer) {
      await saveFilesWithAnswer(currentAnswer.option, filesWithMetadata);
    }
    
    toast.success(`${fileList.length} file${fileList.length > 1 ? 's' : ''} uploaded successfully`);
  };

  const removeFile = (indexToRemove) => {
    setUploadedFiles(prev => prev.filter((_, index) => index !== indexToRemove));
  };

  const saveFilesWithAnswer = async (option, files = uploadedFiles) => {
    if (!currentQuestion || files.length === 0) return;
    
    try {
      const formData = new FormData();
      formData.append('question_id', currentQuestion.id);
      formData.append('option', option);
      
      files.forEach((file, index) => {
        formData.append(`evidence_${index}`, file);
      });
      
      await axios.post(`${API}/assessments/${id}/answer/evidence`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
    } catch (error) {
      console.error('Error uploading evidence files:', error);
      toast.error('Failed to upload evidence files');
    }
  };

  const goToQuestion = (index) => {
    setCurrentQuestionIndex(index);
  };

  const nextQuestion = () => {
    const nextIndex = getNextQuestion();
    if (nextIndex !== null && nextIndex < questions.length) {
      setCurrentQuestionIndex(nextIndex);
    }
  };

  const prevQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  const submitAssessment = async () => {
    const unansweredCount = questions.filter(q => !answers[q.id]).length;
    
    if (unansweredCount > 0) {
      toast.error(`Please answer all questions (${unansweredCount} remaining)`);
      return;
    }
    
    setSubmitting(true);
    try {
      await axios.post(`${API}/assessments/${id}/submit`);
      toast.success('Assessment submitted successfully!');
      navigate(`/results/${id}`);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to submit assessment');
      setSubmitting(false);
    }
  };

  const answeredCount = Object.keys(answers).length;
  const progressPercentage = (answeredCount / questions.length) * 100;

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="loading-spinner w-12 h-12 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading assessment...</p>
        </div>
      </div>
    );
  }

  if (!currentQuestion) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <Card className="w-full max-w-md">
          <CardContent className="p-8 text-center">
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              No questions found
            </h3>
            <p className="text-gray-600 mb-4">
              This assessment doesn&apos;t have any questions.
            </p>
            <Button onClick={() => navigate('/dashboard')}>
              Return to Dashboard
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-bg">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="w-full px-4 sm:px-6 lg:px-8 xl:px-12 2xl:px-16">
          <div className="flex items-center h-12 sm:h-14 compact-header gap-4">
            {/* Logo & Title */}
            <div className="flex items-center space-x-2 sm:space-x-4">
              <Logo className="h-8 w-8 sm:h-10 sm:w-10" />
              <div className="min-w-0">
                <h1 className="text-sm sm:text-lg font-bold text-gray-900 truncate">AM AI SAFE</h1>
                <p className="text-xs text-teal-600 hidden sm:block">EMPOWERING TRUST IN AI</p>
              </div>
            </div>

            {/* Assessment Name - Center */}
            <div className="hidden lg:flex flex-1 justify-center">
              <div className="text-center max-w-md">
                <p className="text-sm font-semibold text-gray-900 truncate">
                  {assessment?.name || 'Loading...'}
                </p>
              </div>
            </div>

            {/* Progress - Between assessment name and buttons */}
            <div className="hidden md:flex items-center space-x-2 lg:space-x-4">
              <div className="text-right">
                <p className="text-xs lg:text-sm font-medium text-gray-900">
                  {answeredCount} of {questions.length} answered
                </p>
                <p className="text-xs text-gray-500">
                  {Math.round(progressPercentage)}% complete
                </p>
              </div>
              <div className="w-20 lg:w-32 bg-gray-200 rounded-full h-2">
                <div 
                  className={`bg-${colors.primary} h-2 rounded-full progress-bar`}
                  style={{ width: `${progressPercentage}%` }}
                ></div>
              </div>
            </div>

            {/* Actions */}
            <div className="flex items-center space-x-1 sm:space-x-2">
              <Button 
                variant="outline" 
                size="sm"
                onClick={() => setShowStatusView(true)}
                data-testid="view-all-questions-btn"
                className="text-xs sm:text-sm px-2 sm:px-3"
              >
                <BarChart3 className="h-3 w-3 sm:h-4 sm:w-4 mr-1 sm:mr-2" />
                <span className="hidden sm:inline">Progress Status</span>
                <span className="sm:hidden">Status</span>
              </Button>
              <Button 
                variant="outline" 
                size="sm"
                onClick={() => setShowFrameworkView(true)}
                data-testid="view-framework-alignment-btn"
                className="text-xs sm:text-sm px-2 sm:px-3"
              >
                <Grid3X3 className="h-3 w-3 sm:h-4 sm:w-4 mr-1 sm:mr-2" />
                <span className="hidden sm:inline">Framework Alignment</span>
                <span className="sm:hidden">Frameworks</span>
              </Button>
              <Button 
                variant="ghost" 
                size="sm"
                onClick={() => navigate('/dashboard')}
                data-testid="return-dashboard-btn"
                className="px-2 sm:px-3"
              >
                <Home className="h-3 w-3 sm:h-4 sm:w-4" />
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Status Overview - Single screen without scrolling */}
      {showStatusView && (
        <AssessmentStatusView 
          assessmentId={id}
          assessmentType={assessmentType}
          assessmentName={assessment?.name}
          onClose={() => setShowStatusView(false)}
          onQuestionClick={(questionId) => {
            const questionIndex = questions.findIndex(q => q.id === questionId);
            if (questionIndex >= 0) {
              setCurrentQuestionIndex(questionIndex);
              setShowStatusView(false);
            }
          }}
        />
      )}

      {showFrameworkView && (
        <AssessmentFrameworkView 
          assessmentId={id}
          assessmentType={assessment?.assessment_type}
          onClose={() => setShowFrameworkView(false)}
          onQuestionClick={(questionId) => {
            const index = questions.findIndex(q => q.id === questionId);
            if (index !== -1) {
              setCurrentQuestionIndex(index);
              setShowFrameworkView(false);
            }
          }}
        />
      )}

      {/* Main Content */}
      <main className="w-full px-4 sm:px-6 lg:px-8 xl:px-12 2xl:px-16 py-2 sm:py-3 lg:py-4 compact-main">
        <div className="grid grid-cols-1 lg:grid-cols-12 xl:grid-cols-12 gap-3 sm:gap-4 lg:gap-6 xl:gap-8 assessment-spacing">
          {/* Sidebar - Question Navigation */}
          <div className="lg:col-span-3 xl:col-span-2">
            <Card className="sticky top-2 lg:top-4 progress-sidebar">
              <CardHeader>
                <CardTitle className="text-lg flex items-center space-x-2">
                  <CheckCircle2 className={`h-5 w-5 text-${colors.primary}`} />
                  <span>Progress</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3 sm:space-y-4 p-3 sm:p-4 pb-4 sm:pb-5 progress-content">
                {/* Current Question Info */}
                <div className="p-2 sm:p-3 bg-teal-50 rounded-lg border border-teal-200">
                  <div className="flex items-center justify-between mb-2">
                    <Badge className={`bg-${colors.primary}`}>{currentQuestion.code}</Badge>
                    <span className="text-sm text-teal-700">
                      {currentQuestionIndex + 1} of {questions.length}
                    </span>
                  </div>
                  <p className="text-sm font-medium text-teal-900">
                    {currentQuestion.domain_name}
                  </p>
                </div>

                {/* Domain Progress */}
                <div className="space-y-2 sm:space-y-3 domain-progress-expanded">
                  <h4 className="font-medium text-gray-900 text-sm sm:text-base mb-1">Domain Progress</h4>
                  <div className="space-y-1.5">
                  {domains.map(domain => {
                    const domainQuestions = questions.filter(q => q.domain_id === domain.id);
                    const domainAnswered = domainQuestions.filter(q => answers[q.id]).length;
                    const domainProgress = (domainAnswered / domainQuestions.length) * 100;
                    const isCurrentDomain = currentQuestion && currentQuestion.domain_id === domain.id;
                    
                    return (
                      <div key={domain.id} className={`space-y-1 p-1.5 sm:p-2 rounded-lg mb-1.5 ${
                        isCurrentDomain ? 'bg-teal-50 border border-teal-200' : ''
                      }`}>
                        <div className="flex justify-between text-sm">
                          <span className={`${
                            isCurrentDomain ? 'text-teal-900 font-medium' : 'text-gray-600'
                          }`}>
                            {domain.name}
                            {isCurrentDomain && <span className="ml-1 text-xs">(Current)</span>}
                          </span>
                          <span className={`font-medium ${
                            isCurrentDomain ? 'text-teal-700' : 'text-gray-700'
                          }`}>
                            {domainAnswered}/{domainQuestions.length}
                          </span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div 
                            className={`h-2 rounded-full progress-bar ${
                              domainAnswered === domainQuestions.length 
                                ? 'bg-green-600' 
                                : isCurrentDomain ? `bg-${colors.primary}` : 'bg-gray-400'
                            }`}
                            style={{ width: `${domainProgress}%` }}
                          ></div>
                        </div>
                      </div>
                    );
                  })}
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Main Question Area */}
          <div className="lg:col-span-9 xl:col-span-10">
            <Card className="mb-3 sm:mb-4">
              <CardHeader className="p-3 sm:p-4 lg:p-5 assessment-card">
                <div className="flex flex-col sm:flex-row items-start justify-between gap-2 sm:gap-0">
                  <div className="flex-1">
                    <div className="flex flex-wrap items-center gap-2 sm:gap-3 mb-2">
                      <Badge variant="outline" className={`text-${colors.primary} border-${colors.border} text-xs sm:text-sm`}>
                        {currentQuestion.code}
                      </Badge>
                      {/* Top InfoBadge for additional question guidance */}
                      <InfoBadge 
                        title="Click for additional guidance and best practices"
                        onClick={handleOpenQuestionHelp}
                      />
                      {/* Framework Alignment Badges - Display in order: FAIRA, NIST, ISO, AU Ethics, AU AI Adoption, EU AI Act */}
                      {/* ISO/IEC 42001 Alignment Badge */}
                      {selectedFrameworks.iso42001 && iso42001AlignmentData[currentQuestion.code] && (
                        <button
                          onClick={() => handleOpenFrameworkModal('iso42001')}
                          className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium transition-colors ${
                            iso42001AlignmentData[currentQuestion.code].alignmentType === 'Fully Aligns'
                              ? 'bg-teal-100 text-teal-800 border border-teal-300 hover:bg-teal-200'
                              : 'bg-teal-50 text-teal-700 border border-teal-200 hover:bg-teal-100'
                          }`}
                          title="Click to view ISO/IEC 42001 alignment details"
                        >
                          ISO 42001 - {iso42001AlignmentData[currentQuestion.code].alignmentType === 'Fully Aligns' ? 'Full' : 'Partial'}
                        </button>
                      )}
                      {/* Australian AI Ethics Principles Alignment Badge */}
                      {selectedFrameworks.auEthics && auEthicsAlignmentData[currentQuestion.code] && (
                        <button
                          onClick={() => handleOpenFrameworkModal('auEthics')}
                          className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium transition-colors ${
                            auEthicsAlignmentData[currentQuestion.code].alignmentType === 'Fully Aligns'
                              ? 'bg-green-100 text-green-800 border border-green-300 hover:bg-green-200'
                              : 'bg-blue-100 text-blue-800 border border-blue-300 hover:bg-blue-200'
                          }`}
                          title="Click to view Australian AI Ethics Principles alignment details"
                        >
                          AU Ethics - {auEthicsAlignmentData[currentQuestion.code].alignmentType === 'Fully Aligns' ? 'Full' : 'Partial'}
                        </button>
                      )}
                      {/* Australian Guidance for AI Adoption Alignment Badge */}
                      {selectedFrameworks.auGuidance && auGuidanceAlignmentData[currentQuestion.code] && (
                        <button
                          onClick={() => handleOpenFrameworkModal('auGuidance')}
                          className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium transition-colors ${
                            auGuidanceAlignmentData[currentQuestion.code].alignmentType === 'Fully Aligns'
                              ? 'bg-blue-100 text-blue-800 border border-blue-300 hover:bg-blue-200'
                              : 'bg-sky-100 text-sky-800 border border-sky-300 hover:bg-sky-200'
                          }`}
                          title="Click to view Australian Guidance for AI Adoption alignment details"
                        >
                          AU Guidance - {auGuidanceAlignmentData[currentQuestion.code].alignmentType === 'Fully Aligns' ? 'Full' : 'Partial'}
                        </button>
                      )}
                      {/* Australian National Framework for the Assurance of AI in Government Alignment Badge */}
                      {selectedFrameworks.auAssurance && auAssuranceAlignmentData[currentQuestion.code] && (
                        <button
                          onClick={() => handleOpenFrameworkModal('auAssurance')}
                          className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium transition-colors ${
                            auAssuranceAlignmentData[currentQuestion.code].alignmentType === 'Fully Aligns'
                              ? 'bg-orange-100 text-orange-800 border border-orange-300 hover:bg-orange-200'
                              : 'bg-orange-50 text-orange-700 border border-orange-200 hover:bg-orange-100'
                          }`}
                          title="Click to view Australian National Framework for the Assurance of AI in Government alignment details"
                        >
                          AU Assurance - {auAssuranceAlignmentData[currentQuestion.code].alignmentType === 'Fully Aligns' ? 'Full' : 'Partial'}
                        </button>
                      )}
                      {/* EU AI Act Alignment Badge */}
                      {selectedFrameworks.euAiAct && euAiActAlignmentData[currentQuestion.code] && (
                        <button
                          onClick={() => handleOpenFrameworkModal('euAiAct')}
                          className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium transition-colors ${
                            euAiActAlignmentData[currentQuestion.code].alignmentType === 'Fully Aligns'
                              ? 'bg-purple-100 text-purple-800 border border-purple-300 hover:bg-purple-200'
                              : 'bg-purple-50 text-purple-700 border border-purple-200 hover:bg-purple-100'
                          }`}
                          title="Click to view EU AI Act alignment details"
                        >
                          EU AI Act - {euAiActAlignmentData[currentQuestion.code].alignmentType === 'Fully Aligns' ? 'Full' : 'Partial'}
                        </button>
                      )}
                      {/* NIST AI RMF Alignment Badge - Only show if NIST selected and question has alignment */}
                      {selectedFrameworks.nist && nistAlignmentData[currentQuestion.code] && (
                        <button
                          onClick={() => handleOpenFrameworkModal('nist')}
                          className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium transition-colors ${
                            nistAlignmentData[currentQuestion.code].alignmentType === 'Fully Aligns'
                              ? 'bg-indigo-100 text-indigo-800 border border-indigo-300 hover:bg-indigo-200'
                              : 'bg-purple-100 text-purple-800 border border-purple-300 hover:bg-purple-200'
                          }`}
                          title="Click to view NIST AI RMF alignment details"
                        >
                          NIST - {nistAlignmentData[currentQuestion.code].alignmentType === 'Fully Aligns' ? 'Full' : 'Partial'}
                        </button>
                      )}
                      {/* OECD Principles Alignment Badge */}
                      {selectedFrameworks.oecdPrinciples && oecdPrinciplesAlignmentData[currentQuestion.code] && (
                        <button
                          onClick={() => handleOpenFrameworkModal('oecdPrinciples')}
                          className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium transition-colors ${
                            oecdPrinciplesAlignmentData[currentQuestion.code].alignmentType === 'Fully Aligns'
                              ? 'bg-slate-100 text-slate-800 border border-slate-300 hover:bg-slate-200'
                              : 'bg-slate-50 text-slate-700 border border-slate-200 hover:bg-slate-100'
                          }`}
                          title="Click to view OECD Principles alignment details"
                        >
                          OECD Principles - {oecdPrinciplesAlignmentData[currentQuestion.code].alignmentType === 'Fully Aligns' ? 'Full' : 'Partial'}
                        </button>
                      )}
                      {/* Singapore MAF Alignment Badge */}
                      {selectedFrameworks.singaporeMaf && singaporeMafAlignmentData[currentQuestion.code] && (
                        <button
                          onClick={() => handleOpenFrameworkModal('singaporeMaf')}
                          className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium transition-colors ${
                            singaporeMafAlignmentData[currentQuestion.code].alignmentType === 'Fully Aligns'
                              ? 'bg-rose-100 text-rose-800 border border-rose-300 hover:bg-rose-200'
                              : 'bg-rose-50 text-rose-700 border border-rose-200 hover:bg-rose-100'
                          }`}
                          title="Click to view Singapore MAF alignment details"
                        >
                          Singapore MAF - {singaporeMafAlignmentData[currentQuestion.code].alignmentType === 'Fully Aligns' ? 'Full' : 'Partial'}
                        </button>
                      )}
                    </div>
                    <CardTitle className="text-lg sm:text-xl lg:text-2xl text-gray-900 leading-relaxed compact-title">
                      {currentQuestion.text}
                    </CardTitle>
                  </div>
                </div>
                
                {currentQuestion.explanation && (
                  <div className="mt-2 sm:mt-3 p-2 sm:p-3 bg-blue-50 rounded-lg border-l-4 border-blue-400 compact-explanation">
                    <p className="text-sm sm:text-base text-blue-800">
                      {currentQuestion.explanation.startsWith('Context:') 
                        ? <><strong>Context:</strong> {currentQuestion.explanation.replace(/^Context:\s*/, '')}</>
                        : <><strong>Context:</strong> {currentQuestion.explanation}</>
                      }
                    </p>
                  </div>
                )}
              </CardHeader>
              
              <CardContent className="space-y-3 sm:space-y-4 p-3 sm:p-4 lg:p-5 assessment-card assessment-spacing">
                {/* Answer Options */}
                <div className="space-y-1.5 sm:space-y-2 compact-answers">
                  <Label className="text-sm sm:text-base font-medium text-gray-900">
                    Select your response:
                  </Label>
                  
                  {/* Dynamic Response Options */}
                  {responseOptions.slice(0, assessmentType === 'Awareness' ? 4 : 4).map((option) => (
                    <div
                      key={option.value}
                      className={`custom-radio ${currentAnswer?.option === option.value ? 'selected' : ''} p-2 sm:p-3`}
                      onClick={() => handleOptionSelect(option.value)}
                      data-testid={`answer-option-${option.value.toLowerCase()}`}
                    >
                      <input
                        type="radio"
                        name="answer"
                        value={option.value}
                        checked={currentAnswer?.option === option.value}
                        onChange={() => {}}
                      />
                      <div className="flex items-start space-x-2 sm:space-x-3">
                        <div className={`w-4 h-4 sm:w-5 sm:h-5 rounded-full border-2 flex items-center justify-center mt-0.5 flex-shrink-0 ${
                          currentAnswer?.option === option.value 
                            ? `border-${colors.primary} bg-${colors.primary}` 
                            : 'border-gray-300'
                        }`}>
                          {currentAnswer?.option === option.value && (
                            <div className="w-2 h-2 sm:w-2.5 sm:h-2.5 rounded-full bg-white"></div>
                          )}
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="font-medium text-gray-900 mb-0.5 text-sm sm:text-base">
                            {option.label} ({option.score} point{option.score !== 1 ? 's' : ''})
                          </div>
                          <div className="text-xs sm:text-sm text-gray-600 leading-relaxed break-words">
                            {option.text}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                  
                  {/* Other Option - only for System assessments */}
                  {assessmentType !== 'Awareness' && responseOptions[4] && (
                    <div
                      className={`custom-radio ${currentAnswer?.option === 'OTHER' ? 'selected' : ''} p-2 sm:p-3`}
                      onClick={() => {
                        // For OTHER, we only select when user actually submits
                      }}
                      data-testid="answer-option-other"
                    >
                      <input
                        type="radio"
                        name="answer"
                        value="OTHER"
                        checked={currentAnswer?.option === 'OTHER'}
                        onChange={() => {}}
                      />
                      <div className="flex items-start space-x-2 sm:space-x-3">
                        <div className={`w-4 h-4 sm:w-5 sm:h-5 rounded-full border-2 flex items-center justify-center mt-0.5 flex-shrink-0 ${
                          currentAnswer?.option === 'OTHER' 
                            ? `border-${colors.primary} bg-${colors.primary}` 
                            : 'border-gray-300'
                        }`}>
                          {currentAnswer?.option === 'OTHER' && (
                            <div className="w-2 h-2 sm:w-2.5 sm:h-2.5 rounded-full bg-white"></div>
                          )}
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="font-medium text-gray-900 mb-1 text-sm sm:text-base">Other (Requires Review)</div>
                          <Textarea
                            id="other-text-input"
                            placeholder="Please describe your specific situation or approach..."
                            value={otherText}
                            onChange={(e) => {
                              setOtherText(e.target.value);
                              // Auto-select OTHER when user starts typing
                              if (e.target.value.trim() && currentAnswer?.option !== 'OTHER') {
                                // This will trigger the selection without calling the API yet
                              }
                            }}
                            className={`min-h-[50px] sm:min-h-[60px] focus:ring-${colors.primary} focus:border-${colors.primary} text-sm sm:text-base compact-textarea`}
                            data-testid="other-text-input"
                          />
                          {otherText.trim() && (
                            <Button
                              onClick={() => handleOptionSelect('OTHER')}
                              className={`mt-2 bg-${colors.primary} hover:bg-${colors.primaryHover} text-sm sm:text-base`}
                              size="sm"
                              data-testid="save-other-btn"
                            >
                              Save Other Response
                            </Button>
                          )}
                        </div>
                      </div>
                      
                      {/* Super Admin Score Input - only show when reviewing OTHER responses */}
                      {user?.role === 'SUPER_ADMIN' && currentAnswer?.option === 'OTHER' && currentAnswer?.review_status === 'PENDING_REVIEW' && (
                        <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                          <Label className="text-sm font-semibold text-gray-900 mb-3 block">
                            🔒 Super Admin: Score this response
                          </Label>
                          <div className="grid grid-cols-4 gap-2 mb-3">
                            {[0, 1, 2, 3].map((score) => (
                              <button
                                key={score}
                                onClick={() => setAdminScore(score)}
                                className={`py-2 px-3 text-center rounded-md font-medium transition-all ${
                                  adminScore === score
                                    ? `bg-${colors.primary} text-white shadow-md`
                                    : `bg-white text-gray-700 border border-gray-300 hover:border-${colors.primary}`
                                }`}
                              >
                                <div className="text-lg">{score}</div>
                                <div className="text-xs">
                                  {score === 0 && 'Non-Ideal'}
                                  {score === 1 && 'Basic'}
                                  {score === 2 && 'Good'}
                                  {score === 3 && 'Ideal'}
                                </div>
                              </button>
                            ))}
                          </div>
                          <Button
                            onClick={handleSaveAdminScore}
                            className={`w-full bg-${colors.primary} hover:bg-${colors.primaryHover}`}
                            disabled={adminScore === null}
                          >
                            Save Score & Continue
                          </Button>
                        </div>
                      )}
                    </div>
                  )}
                </div>

                {/* Evidence Upload Section */}
                <div className="space-y-1">
                  <Label className="text-sm font-medium text-gray-900 flex items-center gap-2">
                    <svg className={`h-3 w-3 text-${colors.primary}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                    </svg>
                    Upload Evidence (Optional)
                    {(currentQuestion.evidence_types || helpContent[currentQuestion.code]) && (
                      <InfoBadge 
                        title="Click for evidence requirements and compliance guidance"
                        onClick={handleOpenHelp}
                      />
                    )}
                  </Label>
                  <div className="flex items-center space-x-2">
                    <Button
                      type="button"
                      variant="outline"
                      size="sm"
                      onClick={() => setShowEvidenceModal(true)}
                      className="text-xs px-2 py-1 h-7"
                      data-testid="evidence-upload-btn"
                    >
                      <svg className="h-3 w-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                      </svg>
                      Choose Files
                    </Button>
                    {uploadedFiles?.length > 0 && (
                      <span className="text-xs text-green-600 font-medium">
                        {uploadedFiles.length} file{uploadedFiles.length > 1 ? 's' : ''} uploaded
                      </span>
                    )}
                  </div>
                  {uploadedFiles?.length > 0 && (
                    <div className="mt-1">
                      <div className="flex flex-wrap gap-1">
                        {uploadedFiles.map((file, index) => (
                          <span key={index} className="inline-flex items-center px-2 py-0.5 rounded text-xs bg-teal-50 text-teal-700 border border-teal-200">
                            {file.name}
                            {file.metadata?.evidenceType && (
                              <span className="ml-1 text-teal-500">({file.metadata.evidenceType})</span>
                            )}
                            <button
                              onClick={() => removeFile(index)}
                              className="ml-1 text-teal-500 hover:text-teal-700"
                            >
                              <svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                              </svg>
                            </button>
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Navigation */}
            <div className="flex flex-col sm:flex-row justify-between items-stretch sm:items-center gap-2 sm:gap-0 mt-2 compact-nav">
              <Button 
                variant="outline"
                onClick={prevQuestion}
                disabled={currentQuestionIndex === 0}
                data-testid="prev-question-btn"
                className="order-2 sm:order-1 text-sm sm:text-base"
              >
                <ArrowLeft className="h-3 w-3 sm:h-4 sm:w-4 mr-2" />
                Previous
              </Button>

              <div className="flex space-x-2 sm:space-x-4 order-1 sm:order-2">
                {answeredCount >= questions.length && assessment?.pending_review_count === 0 ? (
                  <Button 
                    onClick={submitAssessment}
                    disabled={submitting}
                    className="bg-green-600 hover:bg-green-700 flex-1 sm:flex-initial text-sm sm:text-base"
                    data-testid="submit-assessment-btn"
                  >
                    {submitting ? (
                      <div className="flex items-center space-x-2">
                        <div className="loading-spinner w-3 h-3 sm:w-4 sm:h-4"></div>
                        <span>Submitting...</span>
                      </div>
                    ) : (
                      <div className="flex items-center space-x-2">
                        <CheckCircle2 className="h-3 w-3 sm:h-4 sm:w-4" />
                        <span>Submit Assessment</span>
                      </div>
                    )}
                  </Button>
                ) : answeredCount >= questions.length && assessment?.pending_review_count > 0 ? (
                  <div className="flex-1 sm:flex-initial p-3 bg-yellow-50 border border-yellow-300 rounded-md text-center">
                    <p className="text-sm text-yellow-800 font-medium">
                      {assessment.pending_review_count} response(s) need scoring
                    </p>
                  </div>
                ) : (
                  <Button 
                    onClick={nextQuestion}
                    disabled={currentQuestionIndex === questions.length - 1}
                    className={`bg-${colors.primary} hover:bg-${colors.primaryHover} flex-1 sm:flex-initial text-sm sm:text-base`}
                    data-testid="next-question-btn"
                  >
                    Next
                    <ArrowRight className="h-3 w-3 sm:h-4 sm:w-4 ml-2" />
                  </Button>
                )}
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Help Modal */}
      <HelpModal 
        isOpen={showHelpModal}
        onClose={() => setShowHelpModal(false)}
        title={currentHelpContent?.title || ''}
        content={currentHelpContent?.content || null}
      />

      {/* Evidence Upload Modal */}
      <EvidenceUploadModal
        isOpen={showEvidenceModal}
        onClose={() => setShowEvidenceModal(false)}
        onUpload={handleFileUpload}
        questionCode={currentQuestion?.code}
        questionId={currentQuestion?.id}
        currentUser={user}
      />

      {/* Dynamic Framework Alignment Modals - Replaces 9 separate modal blocks */}
      {currentQuestion && Object.entries(FRAMEWORK_CONFIG).map(([key, config]) => {
        const ModalComponent = config.component;
        const alignmentData = config.data[currentQuestion.code];
        
        if (!alignmentData) return null;
        
        return (
          <ModalComponent
            key={key}
            isOpen={activeFrameworkModal === key}
            onClose={handleCloseFrameworkModal}
            questionCode={currentQuestion.code}
            questionText={currentQuestion.text}
            alignmentData={alignmentData}
          />
        );
      })}
    </div>
  );
}

export default AssessmentPage;
