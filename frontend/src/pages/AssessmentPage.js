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

  useEffect(() => {
    fetchAssessment();
  }, [id]);

  const fetchAssessment = async () => {
    try {
      const response = await axios.get(`${API}/assessments/${id}`);
      const data = response.data;
      
      setAssessment(data.assessment);
      setQuestions(data.questions);
      setDomains(data.domains);
      
      // Build answers map
      const answersMap = {};
      data.questions.forEach(q => {
        if (q.answer) {
          answersMap[q.id] = {
            option: q.answer.option,
            note: q.answer.note || ''
          };
        }
      });
      setAnswers(answersMap);
      
      // Set current question (first unanswered or first question)
      const firstUnanswered = data.questions.findIndex(q => !q.answer);
      setCurrentQuestionIndex(firstUnanswered >= 0 ? firstUnanswered : 0);
      
    } catch (error) {
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
      
      const response = await axios.patch(`${API}/assessments/${id}/answer`, payload);
      
      // Update local state
      setAnswers(prev => ({
        ...prev,
        [currentQuestion.id]: {
          option: option,
          note: noteText || '',
          other_text: otherTextValue || '',
          needs_review: response.data.needs_review || false
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

  const handleNoteSave = async () => {
    if (currentAnswer) {
      await saveAnswer(currentAnswer.option, note);
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
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo & Title */}
            <div className="flex items-center space-x-4">
              <div className="bg-teal-600 p-2 rounded-lg">
                <Shield className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-lg font-bold text-gray-900">AM AI SAFE</h1>
                <p className="text-xs text-teal-600">Assessment in Progress</p>
              </div>
            </div>

            {/* Progress */}
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <p className="text-sm font-medium text-gray-900">
                  {answeredCount} of {questions.length} answered
                </p>
                <p className="text-xs text-gray-500">
                  {Math.round(progressPercentage)}% complete
                </p>
              </div>
              <div className="w-32 bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-teal-600 h-2 rounded-full progress-bar"
                  style={{ width: `${progressPercentage}%` }}
                ></div>
              </div>
            </div>

            {/* Actions */}
            <div className="flex items-center space-x-2">
              <Button 
                variant="outline" 
                size="sm"
                onClick={() => setShowStatusView(true)}
                data-testid="view-all-questions-btn"
              >
                <BarChart3 className="h-4 w-4 mr-2" />
                View All
              </Button>
              <Button 
                variant="ghost" 
                size="sm"
                onClick={() => navigate('/dashboard')}
                data-testid="return-dashboard-btn"
              >
                <Home className="h-4 w-4" />
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
        />
      )}

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid lg:grid-cols-4 gap-8">
          {/* Sidebar - Question Navigation */}
          <div className="lg:col-span-1">
            <Card className="sticky top-8">
              <CardHeader>
                <CardTitle className="text-lg flex items-center space-x-2">
                  <Shield className="h-5 w-5 text-teal-600" />
                  <span>Progress</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Current Question Info */}
                <div className="p-3 bg-teal-50 rounded-lg border border-teal-200">
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
                <div className="space-y-3">
                  <h4 className="font-medium text-gray-900">Domain Progress</h4>
                  {domains.map(domain => {
                    const domainQuestions = questions.filter(q => q.domain_id === domain.id);
                    const domainAnswered = domainQuestions.filter(q => answers[q.id]).length;
                    const domainProgress = (domainAnswered / domainQuestions.length) * 100;
                    const isCurrentDomain = currentQuestion && currentQuestion.domain_id === domain.id;
                    
                    return (
                      <div key={domain.id} className={`space-y-1 p-2 rounded-lg ${
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
          <div className="lg:col-span-3">
            <Card className="mb-6">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <Badge variant="outline" className="text-teal-600 border-teal-300">
                        {currentQuestion.code}
                      </Badge>
                      <Badge variant="secondary">
                        {currentQuestion.domain_name}
                      </Badge>
                    </div>
                    <CardTitle className="text-xl text-gray-900 leading-relaxed">
                      {currentQuestion.text}
                    </CardTitle>
                  </div>
                  {/* Help button removed - no help_text available */}
                </div>
                
                {/* Context section removed - no help_text available */}
              </CardHeader>
              
              <CardContent className="space-y-6">
                {/* Answer Options */}
                <div className="space-y-3">
                  <Label className="text-base font-medium text-gray-900">
                    Select your response:
                  </Label>
                  
                  {/* Ideal Option */}
                  <div
                    className={`custom-radio ${currentAnswer?.option === 'IDEAL' ? 'selected' : ''}`}
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
                    <div className="flex items-start space-x-3">
                      <div className={`w-4 h-4 rounded-full border-2 flex items-center justify-center mt-0.5 ${
                        currentAnswer?.option === 'IDEAL' 
                          ? 'border-teal-600 bg-teal-600' 
                          : 'border-gray-300'
                      }`}>
                        {currentAnswer?.option === 'IDEAL' && (
                          <div className="w-2 h-2 rounded-full bg-white"></div>
                        )}
                      </div>
                      <div className="flex-1">
                        <div className="font-medium text-gray-900 mb-1">Ideal (3 points)</div>
                        <div className="text-sm text-gray-600 leading-relaxed">
                          Comprehensive implementation with best practices and full compliance
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  {/* Good Option */}
                  <div
                    className={`custom-radio ${currentAnswer?.option === 'GOOD' ? 'selected' : ''}`}
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
                    <div className="flex items-start space-x-3">
                      <div className={`w-4 h-4 rounded-full border-2 flex items-center justify-center mt-0.5 ${
                        currentAnswer?.option === 'GOOD' 
                          ? 'border-teal-600 bg-teal-600' 
                          : 'border-gray-300'
                      }`}>
                        {currentAnswer?.option === 'GOOD' && (
                          <div className="w-2 h-2 rounded-full bg-white"></div>
                        )}
                      </div>
                      <div className="flex-1">
                        <div className="font-medium text-gray-900 mb-1">Good (2 points)</div>
                        <div className="text-sm text-gray-600 leading-relaxed">
                          Solid implementation with room for improvement
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  {/* Basic Option */}
                  <div
                    className={`custom-radio ${currentAnswer?.option === 'BASIC' ? 'selected' : ''}`}
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
                    <div className="flex items-start space-x-3">
                      <div className={`w-4 h-4 rounded-full border-2 flex items-center justify-center mt-0.5 ${
                        currentAnswer?.option === 'BASIC' 
                          ? 'border-teal-600 bg-teal-600' 
                          : 'border-gray-300'
                      }`}>
                        {currentAnswer?.option === 'BASIC' && (
                          <div className="w-2 h-2 rounded-full bg-white"></div>
                        )}
                      </div>
                      <div className="flex-1">
                        <div className="font-medium text-gray-900 mb-1">Basic (1 point)</div>
                        <div className="text-sm text-gray-600 leading-relaxed">
                          Minimal implementation, significant gaps exist
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  {/* Non-Ideal Option */}
                  <div
                    className={`custom-radio ${currentAnswer?.option === 'NON_IDEAL' ? 'selected' : ''}`}
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
                    <div className="flex items-start space-x-3">
                      <div className={`w-4 h-4 rounded-full border-2 flex items-center justify-center mt-0.5 ${
                        currentAnswer?.option === 'NON_IDEAL' 
                          ? 'border-teal-600 bg-teal-600' 
                          : 'border-gray-300'
                      }`}>
                        {currentAnswer?.option === 'NON_IDEAL' && (
                          <div className="w-2 h-2 rounded-full bg-white"></div>
                        )}
                      </div>
                      <div className="flex-1">
                        <div className="font-medium text-gray-900 mb-1">Non-Ideal (0 points)</div>
                        <div className="text-sm text-gray-600 leading-relaxed">
                          Little to no implementation or consideration
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  {/* Other Option */}
                  <div
                    className={`custom-radio ${currentAnswer?.option === 'OTHER' ? 'selected' : ''}`}
                    data-testid="answer-option-other"
                  >
                    <div 
                      onClick={() => {
                        // Focus on text input instead of selecting immediately
                        document.getElementById('other-text-input')?.focus();
                      }}
                      className="flex items-start space-x-3"
                    >
                      <div className={`w-4 h-4 rounded-full border-2 flex items-center justify-center mt-0.5 ${
                        currentAnswer?.option === 'OTHER' 
                          ? 'border-teal-600 bg-teal-600' 
                          : 'border-gray-300'
                      }`}>
                        {currentAnswer?.option === 'OTHER' && (
                          <div className="w-2 h-2 rounded-full bg-white"></div>
                        )}
                      </div>
                      <div className="flex-1">
                        <div className="font-medium text-gray-900 mb-2">Other (Requires Review)</div>
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
                          className="min-h-[80px] focus:ring-teal focus:border-teal-500"
                          data-testid="other-text-input"
                        />
                        {otherText.trim() && (
                          <Button
                            onClick={() => handleOptionSelect('OTHER')}
                            className="mt-2 bg-teal-600 hover:bg-teal-700"
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

                {/* Notes Section */}
                <div className="space-y-3">
                  <Label htmlFor="note" className="text-base font-medium text-gray-900">
                    Additional Notes (Optional)
                  </Label>
                  <Textarea
                    id="note"
                    placeholder="Add any relevant details, context, or explanations..."
                    value={note}
                    onChange={(e) => handleNoteChange(e.target.value)}
                    className="min-h-[100px] focus:ring-teal focus:border-teal-500"
                    data-testid="question-note-textarea"
                  />
                  {note !== (currentAnswer?.note || '') && (
                    <Button 
                      onClick={handleNoteSave}
                      disabled={saving}
                      size="sm"
                      className="bg-teal-600 hover:bg-teal-700"
                      data-testid="save-note-btn"
                    >
                      <Save className="h-4 w-4 mr-2" />
                      {saving ? 'Saving...' : 'Save Note'}
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Navigation */}
            <div className="flex justify-between items-center">
              <Button 
                variant="outline"
                onClick={prevQuestion}
                disabled={currentQuestionIndex === 0}
                data-testid="prev-question-btn"
              >
                <ArrowLeft className="h-4 w-4 mr-2" />
                Previous
              </Button>

              <div className="flex space-x-4">
                {currentQuestionIndex === questions.length - 1 ? (
                  <Button 
                    onClick={submitAssessment}
                    disabled={submitting || answeredCount < questions.length}
                    className="bg-green-600 hover:bg-green-700"
                    data-testid="submit-assessment-btn"
                  >
                    {submitting ? (
                      <div className="flex items-center space-x-2">
                        <div className="loading-spinner w-4 h-4"></div>
                        <span>Submitting...</span>
                      </div>
                    ) : (
                      <div className="flex items-center space-x-2">
                        <CheckCircle2 className="h-4 w-4" />
                        <span>Submit Assessment</span>
                      </div>
                    )}
                  </Button>
                ) : (
                  <Button 
                    onClick={nextQuestion}
                    disabled={currentQuestionIndex === questions.length - 1}
                    className="bg-teal-600 hover:bg-teal-700"
                    data-testid="next-question-btn"
                  >
                    Next
                    <ArrowRight className="h-4 w-4 ml-2" />
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
