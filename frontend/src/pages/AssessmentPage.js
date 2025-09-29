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
  Save
} from 'lucide-react';

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
  const [showQuestionGrid, setShowQuestionGrid] = useState(false);

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
    } else {
      setNote('');
    }
  }, [currentQuestionIndex, currentAnswer]);

  const saveAnswer = async (option, noteText = note) => {
    if (!currentQuestion) return;
    
    setSaving(true);
    try {
      await axios.patch(`${API}/assessments/${id}/answer`, {
        question_id: currentQuestion.id,
        option: option,
        note: noteText || null
      });
      
      // Update local state
      setAnswers(prev => ({
        ...prev,
        [currentQuestion.id]: {
          option: option,
          note: noteText || ''
        }
      }));
      
      toast.success('Answer saved!');
    } catch (error) {
      toast.error('Failed to save answer');
    } finally {
      setSaving(false);
    }
  };

  const handleOptionSelect = async (option) => {
    await saveAnswer(option);
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
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
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
                onClick={() => setShowQuestionGrid(!showQuestionGrid)}
                data-testid="view-all-questions-btn"
              >
                <Grid3X3 className="h-4 w-4 mr-2" />
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

      {/* Question Grid Overlay */}
      {showQuestionGrid && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
          <Card className="w-full max-w-4xl max-h-[80vh] overflow-auto">
            <CardHeader>
              <div className="flex justify-between items-center">
                <CardTitle>Assessment Questions</CardTitle>
                <Button 
                  variant="ghost" 
                  onClick={() => setShowQuestionGrid(false)}
                  data-testid="close-question-grid-btn"
                >
                  ×
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                {domains.map(domain => {
                  const domainQuestions = questions.filter(q => q.domain_id === domain.id);
                  return (
                    <div key={domain.id}>
                      <h3 className="font-semibold text-gray-900 mb-3">{domain.name}</h3>
                      <div className="grid grid-cols-4 gap-2">
                        {domainQuestions.map((question, index) => {
                          const questionIndex = questions.findIndex(q => q.id === question.id);
                          const isAnswered = answers[question.id];
                          const isCurrent = questionIndex === currentQuestionIndex;
                          
                          return (
                            <button
                              key={question.id}
                              onClick={() => goToQuestion(questionIndex)}
                              className={`p-3 rounded-lg border-2 text-sm font-medium transition-all ${
                                isCurrent 
                                  ? 'border-teal-500 bg-teal-50 text-teal-700' 
                                  : isAnswered 
                                    ? 'border-green-200 bg-green-50 text-green-700' 
                                    : 'border-gray-200 bg-white text-gray-600 hover:border-teal-300'
                              }`}
                              data-testid={`question-nav-${question.code}`}
                            >
                              <div className="flex items-center justify-center space-x-1">
                                {isAnswered ? (
                                  <CheckCircle2 className="h-4 w-4" />
                                ) : (
                                  <Circle className="h-4 w-4" />
                                )}
                                <span>{question.code}</span>
                              </div>
                            </button>
                          );
                        })}
                      </div>
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        </div>
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
                    
                    return (
                      <div key={domain.id} className="space-y-1">
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-600">{domain.name}</span>
                          <span className="font-medium">
                            {domainAnswered}/{domainQuestions.length}
                          </span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-teal-600 h-2 rounded-full progress-bar"
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
                  {currentQuestion.help_text && (
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
                
                {currentQuestion.help_text && (
                  <div className="mt-4 p-4 bg-blue-50 rounded-lg border-l-4 border-blue-400">
                    <p className="text-sm text-blue-800">
                      <strong>Context:</strong> {currentQuestion.help_text}
                    </p>
                  </div>
                )}
              </CardHeader>
              
              <CardContent className="space-y-6">
                {/* Answer Options */}
                <div className="space-y-3">
                  <Label className="text-base font-medium text-gray-900">
                    Select your response:
                  </Label>
                  {answerOptions.map((option) => {
                    const isSelected = currentAnswer?.option === option.value;
                    return (
                      <div
                        key={option.value}
                        className={`custom-radio ${isSelected ? 'selected' : ''}`}
                        onClick={() => handleOptionSelect(option.value)}
                        data-testid={`answer-option-${option.value.toLowerCase()}`}
                      >
                        <input
                          type="radio"
                          name="answer"
                          value={option.value}
                          checked={isSelected}
                          onChange={() => {}} // Handled by onClick
                        />
                        <div className="flex items-start space-x-3">
                          <div className={`w-4 h-4 rounded-full border-2 flex items-center justify-center mt-0.5 ${
                            isSelected 
                              ? 'border-teal-600 bg-teal-600' 
                              : 'border-gray-300'
                          }`}>
                            {isSelected && (
                              <div className="w-2 h-2 rounded-full bg-white"></div>
                            )}
                          </div>
                          <div className="flex-1">
                            <div className="font-medium text-gray-900">{option.label}</div>
                            <div className="text-sm text-gray-600">{option.description}</div>
                          </div>
                        </div>
                      </div>
                    );
                  })}
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
