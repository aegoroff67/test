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
import { 
  ArrowLeft, 
  ArrowRight, 
  Home, 
  Shield, 
  CheckCircle2, 
  Circle,
  Grid3X3,
  HelpCircle,
  Save,
  BarChart3
} from 'lucide-react';
import AssessmentStatusView from '../components/AssessmentStatusView';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Answer options will be dynamically loaded from question data

function AssessmentPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [assessment, setAssessment] = useState(null);
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
  const [uploadedFiles, setUploadedFiles] = useState([]);

  useEffect(() => {
    fetchAssessment();
  }, [id]);

  const fetchAssessment = async () => {
    try {
      // Fetch assessment metadata
      const assessmentResponse = await axios.get(`${API}/assessments/${id}`);
      setAssessment(assessmentResponse.data);
      
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
            other_text: q.answer.other_text || ''
          };
        }
      });
      setAnswers(answersMap);
      
      // Set current question (first unanswered or first question)
      const firstUnanswered = questionsData.findIndex(q => !q.answer);
      setCurrentQuestionIndex(firstUnanswered >= 0 ? firstUnanswered : 0);
      
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

  useEffect(() => {
    if (currentAnswer) {
      setNote(currentAnswer.note || '');
      setOtherText(currentAnswer.other_text || '');
    } else {
      setNote('');
      setOtherText('');
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
      toast.error(error.response?.data?.detail || 'Failed to save answer');
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

  const handleFileUpload = async (files) => {
    if (!files || files.length === 0) return;
    
    const newFiles = Array.from(files);
    
    // Validate file sizes (max 10MB per file)
    const maxSize = 10 * 1024 * 1024; // 10MB
    const oversizedFiles = newFiles.filter(file => file.size > maxSize);
    
    if (oversizedFiles.length > 0) {
      toast.error(`Some files are too large. Maximum size is 10MB per file.`);
      return;
    }
    
    // Add to uploaded files state
    setUploadedFiles(prev => [...prev, ...newFiles]);
    
    // If there's already an answer, save the files with it
    if (currentAnswer) {
      await saveFilesWithAnswer(currentAnswer.option, newFiles);
    }
    
    toast.success(`${newFiles.length} file${newFiles.length > 1 ? 's' : ''} uploaded successfully`);
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
    setShowQuestionGrid(false);
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
              This assessment doesn't have any questions.
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
          <div className="flex justify-between items-center h-12 sm:h-14 compact-header">
            {/* Logo & Title */}
            <div className="flex items-center space-x-2 sm:space-x-4">
              <div className="bg-teal-600 p-1.5 sm:p-2 rounded-lg">
                <Shield className="h-4 w-4 sm:h-6 sm:w-6 text-white" />
              </div>
              <div className="min-w-0">
                <h1 className="text-sm sm:text-lg font-bold text-gray-900 truncate">AM AI SAFE</h1>
                <p className="text-xs text-teal-600 hidden sm:block">Assessment in Progress</p>
              </div>
            </div>

            {/* Progress - Hidden on small screens, shown in compact form on medium+ */}
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
                  className="bg-teal-600 h-2 rounded-full progress-bar"
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
                <span className="hidden sm:inline">View All</span>
                <span className="sm:hidden">All</span>
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

      {/* Main Content */}
      <main className="w-full px-4 sm:px-6 lg:px-8 xl:px-12 2xl:px-16 py-2 sm:py-3 lg:py-4 compact-main">
        <div className="grid grid-cols-1 lg:grid-cols-12 xl:grid-cols-12 gap-3 sm:gap-4 lg:gap-6 xl:gap-8 assessment-spacing">
          {/* Sidebar - Question Navigation */}
          <div className="lg:col-span-3 xl:col-span-2">
            <Card className="sticky top-2 lg:top-4">
              <CardHeader>
                <CardTitle className="text-lg flex items-center space-x-2">
                  <Shield className="h-5 w-5 text-teal-600" />
                  <span>Progress</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-1.5 sm:space-y-2 p-3 sm:p-4">
                {/* Current Question Info */}
                <div className="p-1.5 sm:p-2 bg-teal-50 rounded-lg border border-teal-200">
                  <div className="flex items-center justify-between mb-2">
                    <Badge className="bg-teal-600">{currentQuestion.code}</Badge>
                    <span className="text-sm text-teal-700">
                      {currentQuestionIndex + 1} of {questions.length}
                    </span>
                  </div>
                  <p className="text-sm font-medium text-teal-900">
                    {currentQuestion.domain_name}
                  </p>
                </div>

                {/* Domain Progress */}
                <div className="space-y-1.5 sm:space-y-2">
                  <h4 className="font-medium text-gray-900 text-sm sm:text-base">Domain Progress</h4>
                  {domains.map(domain => {
                    const domainQuestions = questions.filter(q => q.domain_id === domain.id);
                    const domainAnswered = domainQuestions.filter(q => answers[q.id]).length;
                    const domainProgress = (domainAnswered / domainQuestions.length) * 100;
                    const isCurrentDomain = currentQuestion && currentQuestion.domain_id === domain.id;
                    
                    return (
                      <div key={domain.id} className={`space-y-0.5 p-1 sm:p-1.5 rounded-lg ${
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
                                : isCurrentDomain ? 'bg-teal-600' : 'bg-gray-400'
                            }`}
                            style={{ width: `${domainProgress}%` }}
                          ></div>
                        </div>
                      </div>
                    );
                  })}
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
                      <Badge variant="outline" className="text-teal-600 border-teal-300 text-xs sm:text-sm">
                        {currentQuestion.code}
                      </Badge>
                      <Badge variant="secondary" className="text-xs sm:text-sm">
                        {currentQuestion.domain_name}
                      </Badge>
                    </div>
                    <CardTitle className="text-lg sm:text-xl lg:text-2xl text-gray-900 leading-relaxed compact-title">
                      {currentQuestion.text}
                    </CardTitle>
                  </div>
                  {currentQuestion.explanation && (
                    <Button 
                      variant="ghost" 
                      size="sm" 
                      className="text-gray-400 hover:text-gray-600"
                      title="Help"
                      data-testid="question-help-btn"
                    >
                      <HelpCircle className="h-4 w-4" />
                    </Button>
                  )}
                </div>
                
                {currentQuestion.explanation && (
                  <div className="mt-2 sm:mt-3 p-2 sm:p-3 bg-blue-50 rounded-lg border-l-4 border-blue-400 compact-explanation">
                    <p className="text-sm sm:text-base text-blue-800">
                      <strong>Context:</strong> {currentQuestion.explanation}
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
                  
                  {/* Ideal Option */}
                  <div
                    className={`custom-radio ${currentAnswer?.option === 'IDEAL' ? 'selected' : ''} p-2 sm:p-3`}
                    onClick={() => handleOptionSelect('IDEAL')}
                    data-testid="answer-option-ideal"
                  >
                    <input
                      type="radio"
                      name="answer"
                      value="IDEAL"
                      checked={currentAnswer?.option === 'IDEAL'}
                      onChange={() => {}}
                    />
                    <div className="flex items-start space-x-2 sm:space-x-3">
                      <div className={`w-4 h-4 sm:w-5 sm:h-5 rounded-full border-2 flex items-center justify-center mt-0.5 flex-shrink-0 ${
                        currentAnswer?.option === 'IDEAL' 
                          ? 'border-teal-600 bg-teal-600' 
                          : 'border-gray-300'
                      }`}>
                        {currentAnswer?.option === 'IDEAL' && (
                          <div className="w-2 h-2 sm:w-2.5 sm:h-2.5 rounded-full bg-white"></div>
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="font-medium text-gray-900 mb-0.5 text-sm sm:text-base">Ideal (3 points)</div>
                        <div className="text-xs sm:text-sm text-gray-600 leading-relaxed break-words">
                          {currentQuestion?.predefined_answers?.ideal || 'Comprehensive implementation with best practices and full compliance'}
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  {/* Good Option */}
                  <div
                    className={`custom-radio ${currentAnswer?.option === 'GOOD' ? 'selected' : ''} p-2 sm:p-3`}
                    onClick={() => handleOptionSelect('GOOD')}
                    data-testid="answer-option-good"
                  >
                    <input
                      type="radio"
                      name="answer"
                      value="GOOD"
                      checked={currentAnswer?.option === 'GOOD'}
                      onChange={() => {}}
                    />
                    <div className="flex items-start space-x-2 sm:space-x-3">
                      <div className={`w-4 h-4 sm:w-5 sm:h-5 rounded-full border-2 flex items-center justify-center mt-0.5 flex-shrink-0 ${
                        currentAnswer?.option === 'GOOD' 
                          ? 'border-teal-600 bg-teal-600' 
                          : 'border-gray-300'
                      }`}>
                        {currentAnswer?.option === 'GOOD' && (
                          <div className="w-2 h-2 sm:w-2.5 sm:h-2.5 rounded-full bg-white"></div>
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="font-medium text-gray-900 mb-0.5 text-sm sm:text-base">Good (2 points)</div>
                        <div className="text-xs sm:text-sm text-gray-600 leading-relaxed break-words">
                          {currentQuestion?.predefined_answers?.good || 'Solid implementation with room for improvement'}
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  {/* Basic Option */}
                  <div
                    className={`custom-radio ${currentAnswer?.option === 'BASIC' ? 'selected' : ''} p-2 sm:p-3`}
                    onClick={() => handleOptionSelect('BASIC')}
                    data-testid="answer-option-basic"
                  >
                    <input
                      type="radio"
                      name="answer"
                      value="BASIC"
                      checked={currentAnswer?.option === 'BASIC'}
                      onChange={() => {}}
                    />
                    <div className="flex items-start space-x-2 sm:space-x-3">
                      <div className={`w-4 h-4 sm:w-5 sm:h-5 rounded-full border-2 flex items-center justify-center mt-0.5 flex-shrink-0 ${
                        currentAnswer?.option === 'BASIC' 
                          ? 'border-teal-600 bg-teal-600' 
                          : 'border-gray-300'
                      }`}>
                        {currentAnswer?.option === 'BASIC' && (
                          <div className="w-2 h-2 sm:w-2.5 sm:h-2.5 rounded-full bg-white"></div>
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="font-medium text-gray-900 mb-0.5 text-sm sm:text-base">Basic (1 point)</div>
                        <div className="text-xs sm:text-sm text-gray-600 leading-relaxed break-words">
                          {currentQuestion?.predefined_answers?.basic || 'Minimal implementation, significant gaps exist'}
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  {/* Non-Ideal Option */}
                  <div
                    className={`custom-radio ${currentAnswer?.option === 'NON_IDEAL' ? 'selected' : ''} p-2 sm:p-3`}
                    onClick={() => handleOptionSelect('NON_IDEAL')}
                    data-testid="answer-option-non-ideal"
                  >
                    <input
                      type="radio"
                      name="answer"
                      value="NON_IDEAL"
                      checked={currentAnswer?.option === 'NON_IDEAL'}
                      onChange={() => {}}
                    />
                    <div className="flex items-start space-x-2 sm:space-x-3">
                      <div className={`w-4 h-4 sm:w-5 sm:h-5 rounded-full border-2 flex items-center justify-center mt-0.5 flex-shrink-0 ${
                        currentAnswer?.option === 'NON_IDEAL' 
                          ? 'border-teal-600 bg-teal-600' 
                          : 'border-gray-300'
                      }`}>
                        {currentAnswer?.option === 'NON_IDEAL' && (
                          <div className="w-2 h-2 sm:w-2.5 sm:h-2.5 rounded-full bg-white"></div>
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="font-medium text-gray-900 mb-0.5 text-sm sm:text-base">Non-Ideal (0 points)</div>
                        <div className="text-xs sm:text-sm text-gray-600 leading-relaxed break-words">
                          {currentQuestion?.predefined_answers?.non_ideal || 'Little to no implementation or consideration'}
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  {/* Other Option */}
                  <div
                    className={`custom-radio ${currentAnswer?.option === 'OTHER' ? 'selected' : ''} p-2 sm:p-3`}
                    data-testid="answer-option-other"
                  >
                    <div 
                      onClick={() => {
                        // Focus on text input instead of selecting immediately
                        document.getElementById('other-text-input')?.focus();
                      }}
                      className="flex items-start space-x-2 sm:space-x-3"
                    >
                      <div className={`w-4 h-4 sm:w-5 sm:h-5 rounded-full border-2 flex items-center justify-center mt-0.5 flex-shrink-0 ${
                        currentAnswer?.option === 'OTHER' 
                          ? 'border-teal-600 bg-teal-600' 
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
                          className="min-h-[50px] sm:min-h-[60px] focus:ring-teal focus:border-teal-500 text-sm sm:text-base compact-textarea"
                          data-testid="other-text-input"
                        />
                        {otherText.trim() && (
                          <Button
                            onClick={() => handleOptionSelect('OTHER')}
                            className="mt-2 bg-teal-600 hover:bg-teal-700 text-sm sm:text-base"
                            size="sm"
                            data-testid="save-other-btn"
                          >
                            Save Other Response
                          </Button>
                        )}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Evidence Upload Section */}
                <div className="space-y-1">
                  <Label className="text-sm font-medium text-gray-900 flex items-center">
                    <svg className="h-3 w-3 mr-1 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                    </svg>
                    Upload Evidence (Optional)
                  </Label>
                  <div className="flex items-center space-x-2">
                    <input
                      type="file"
                      id="evidence-upload"
                      multiple
                      accept=".pdf,.doc,.docx,.jpg,.jpeg,.png,.xlsx,.xls"
                      className="hidden"
                      onChange={(e) => handleFileUpload(e.target.files)}
                      data-testid="evidence-upload-input"
                    />
                    <Button
                      type="button"
                      variant="outline"
                      size="sm"
                      onClick={() => document.getElementById('evidence-upload')?.click()}
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
                {answeredCount >= questions.length ? (
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
                ) : (
                  <Button 
                    onClick={nextQuestion}
                    disabled={currentQuestionIndex === questions.length - 1}
                    className="bg-teal-600 hover:bg-teal-700 flex-1 sm:flex-initial text-sm sm:text-base"
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
    </div>
  );
}

export default AssessmentPage;
