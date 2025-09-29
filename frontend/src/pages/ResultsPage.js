import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { toast } from 'sonner';
import { 
  ArrowLeft, 
  Shield, 
  Download, 
  MessageSquare,
  BarChart3,
  TrendingUp,
  AlertTriangle,
  CheckCircle2,
  FileText,
  Building2
} from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Color mapping for heatmap
const getScoreColor = (percentage) => {
  if (percentage >= 75) return { bg: 'bg-green-500', text: 'text-white' };
  if (percentage >= 50) return { bg: 'bg-yellow-500', text: 'text-white' };
  if (percentage >= 25) return { bg: 'bg-orange-500', text: 'text-white' };
  return { bg: 'bg-red-500', text: 'text-white' };
};

const getMaturityBadge = (maturity) => {
  switch (maturity) {
    case 'HIGH':
      return { color: 'bg-green-100 text-green-800', icon: CheckCircle2 };
    case 'MODERATE':
      return { color: 'bg-yellow-100 text-yellow-800', icon: TrendingUp };
    case 'LOW':
      return { color: 'bg-red-100 text-red-800', icon: AlertTriangle };
    default:
      return { color: 'bg-gray-100 text-gray-800', icon: BarChart3 };
  }
};

function ResultsPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [assessment, setAssessment] = useState(null);
  const [summary, setSummary] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [generatingReport, setGeneratingReport] = useState(false);

  useEffect(() => {
    fetchResults();
  }, [id]);

  const fetchResults = async () => {
    try {
      // Fetch assessment details
      const assessmentResponse = await axios.get(`${API}/assessments/${id}`);
      setAssessment(assessmentResponse.data);
      
      // Fetch questions with answers
      const questionsResponse = await axios.get(`${API}/assessments/${id}/questions`);
      const questionData = questionsResponse.data;
      
      // Extract questions and build answers array
      const allQuestions = [];
      const answersData = [];
      
      questionData.forEach(domainData => {
        domainData.questions.forEach(question => {
          allQuestions.push(question);
          if (question.answer) {
            answersData.push({ ...question.answer, question });
          }
        });
      });
      
      setQuestions(allQuestions);
      setAnswers(answersData);
      
      // Fetch summary
      const summaryResponse = await axios.get(`${API}/assessments/${id}/summary`);
      setSummary(summaryResponse.data);
      
    } catch (error) {
      console.error('Error loading results:', error);
      toast.error('Failed to load results');
      navigate('/dashboard');
    } finally {
      setLoading(false);
    }
  };

  const generateReport = async () => {
    setGeneratingReport(true);
    try {
      const response = await axios.get(`${API}/assessments/${id}/report`);
      window.open(response.data.url, '_blank');
      toast.success('Report generated successfully!');
    } catch (error) {
      toast.error('Failed to generate report');
    } finally {
      setGeneratingReport(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="loading-spinner w-12 h-12 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading results...</p>
        </div>
      </div>
    );
  }

  if (!summary) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <Card className="w-full max-w-md">
          <CardContent className="p-8 text-center">
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Results not available
            </h3>
            <p className="text-gray-600 mb-4">
              This assessment may not be completed yet.
            </p>
            <Button onClick={() => navigate('/dashboard')}>
              Return to Dashboard
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  const maturityInfo = getMaturityBadge(summary.overall_maturity);
  const MaturityIcon = maturityInfo.icon;

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
                <p className="text-xs text-teal-600">Assessment Results</p>
              </div>
            </div>

            {/* Assessment Info */}
            <div className="text-center">
              <p className="text-sm font-medium text-gray-900">{assessment?.name}</p>
              <p className="text-xs text-gray-500 flex items-center justify-center space-x-1">
                <Building2 className="h-3 w-3" />
                <span>{user?.organization_name}</span>
              </p>
            </div>

            {/* Actions */}
            <div className="flex items-center space-x-2">
              <Button 
                variant="outline" 
                size="sm"
                onClick={() => navigate('/dashboard')}
                data-testid="back-dashboard-btn"
              >
                <ArrowLeft className="h-4 w-4 mr-2" />
                Dashboard
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Overall Score Card */}
        <Card className="mb-8 border-0 shadow-lg">
          <CardContent className="p-8">
            <div className="text-center">
              <div className="mb-6">
                <div className="inline-flex items-center justify-center p-4 bg-teal-100 rounded-full mb-4">
                  <MaturityIcon className="h-12 w-12 text-teal-600" />
                </div>
                <h1 className="text-4xl font-bold text-gray-900 mb-2" data-testid="overall-score">
                  {summary.overall_percentage.toFixed(1)}%
                </h1>
                <Badge className={`text-lg px-4 py-2 ${maturityInfo.color}`} data-testid="maturity-level">
                  {summary.overall_maturity} AI MATURITY
                </Badge>
              </div>
              
              <div className="max-w-2xl mx-auto">
                <p className="text-lg text-gray-600 mb-6">
                  {summary.overall_maturity === 'HIGH' && 
                    'Excellent! Your organization demonstrates strong AI governance practices across most domains. Continue to maintain and refine your current approaches.'}
                  {summary.overall_maturity === 'MODERATE' && 
                    'Good foundation! Your organization has implemented basic AI governance measures. Focus on strengthening practices in lower-scoring domains.'}
                  {summary.overall_maturity === 'LOW' && 
                    'Opportunity for improvement. Your organization is in the early stages of AI governance. Prioritize implementing fundamental safeguards and controls.'}
                </p>
                
                <div className="flex justify-center space-x-4">
                  <Button 
                    onClick={generateReport}
                    disabled={generatingReport}
                    className="bg-teal-600 hover:bg-teal-700 btn-hover"
                    data-testid="generate-report-btn"
                  >
                    {generatingReport ? (
                      <div className="flex items-center space-x-2">
                        <div className="loading-spinner w-4 h-4"></div>
                        <span>Generating...</span>
                      </div>
                    ) : (
                      <div className="flex items-center space-x-2">
                        <Download className="h-4 w-4" />
                        <span>Generate PDF Report</span>
                      </div>
                    )}
                  </Button>
                  
                  <Button 
                    variant="outline"
                    className="btn-hover"
                    data-testid="request-consultation-btn"
                  >
                    <MessageSquare className="h-4 w-4 mr-2" />
                    Request Consultation
                  </Button>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Domain Scores */}
          <div className="lg:col-span-1">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <BarChart3 className="h-5 w-5 text-teal-600" />
                  <span>Domain Scores</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4" data-testid="domain-scores-list">
                {[...summary.domain_scores]
                  .sort((a, b) => a.percentage - b.percentage) // Sort by percentage, lowest first
                  .map((domain, index) => {
                  const colors = getScoreColor(domain.percentage);
                  return (
                    <div key={domain.domain_id} className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="font-medium text-gray-900">{domain.domain_name}</span>
                        <Badge 
                          className={`${colors.bg} ${colors.text}`}
                          data-testid={`domain-score-${domain.domain_name.toLowerCase()}`}
                        >
                          {domain.percentage.toFixed(1)}%
                        </Badge>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className={`${colors.bg} h-2 rounded-full progress-bar`}
                          style={{ width: `${domain.percentage}%` }}
                        ></div>
                      </div>
                      <p className="text-xs text-gray-600">
                        {domain.score} out of {domain.max_score} points
                      </p>
                    </div>
                  );
                })}
              </CardContent>
            </Card>
          </div>

          {/* Heatmap */}
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Shield className="h-5 w-5 text-teal-600" />
                  <span>Assessment Heatmap</span>
                </CardTitle>
                <p className="text-sm text-gray-600">
                  Visual representation of your responses across all domains and questions
                </p>
              </CardHeader>
              <CardContent>
                <div className="space-y-6" data-testid="assessment-heatmap">
                  {summary.domain_scores.map((domain) => {
                    const domainQuestions = questions.filter(q => q.domain_id === domain.domain_id);
                    const domainAnswers = answers.filter(a => 
                      domainQuestions.some(q => q.id === a.question_id)
                    );
                    
                    return (
                      <div key={domain.domain_id}>
                        <div className="flex items-center justify-between mb-3">
                          <h4 className="font-medium text-gray-900">{domain.domain_name}</h4>
                          <Badge variant="outline" className="text-xs">
                            {domain.percentage}%
                          </Badge>
                        </div>
                        
                        <div className="grid grid-cols-4 gap-2">
                          {domainQuestions.map((question) => {
                            const answer = domainAnswers.find(a => a.question_id === question.id);
                            const score = answer ? answer.numeric_score : 0;
                            const percentage = (score / 3) * 100; // Max score is 3
                            const colors = getScoreColor(percentage);
                            
                            return (
                              <div
                                key={question.id}
                                className={`heatmap-cell p-3 rounded-lg border-2 text-center ${colors.bg} ${colors.text} border-transparent`}
                                title={`${question.code}: ${question.text} (Score: ${score}/3)`}
                                data-testid={`heatmap-cell-${question.code}`}
                              >
                                <div className="font-bold text-sm">{question.code}</div>
                                <div className="text-xs opacity-90">{score}/3</div>
                              </div>
                            );
                          })}
                        </div>
                      </div>
                    );
                  })}
                </div>
                
                {/* Legend */}
                <div className="mt-6 pt-4 border-t">
                  <h5 className="font-medium text-gray-900 mb-3">Score Legend</h5>
                  <div className="flex items-center space-x-6">
                    <div className="flex items-center space-x-2">
                      <div className="w-4 h-4 bg-red-500 rounded"></div>
                      <span className="text-sm text-gray-600">0-24% (Non-Ideal)</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-4 h-4 bg-orange-500 rounded"></div>
                      <span className="text-sm text-gray-600">25-49% (Basic)</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-4 h-4 bg-yellow-500 rounded"></div>
                      <span className="text-sm text-gray-600">50-74% (Good)</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-4 h-4 bg-green-500 rounded"></div>
                      <span className="text-sm text-gray-600">75-100% (Ideal)</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Next Steps */}
        <Card className="mt-8">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <TrendingUp className="h-5 w-5 text-teal-600" />
              <span>Next Steps</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="bg-teal-100 p-4 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                  <FileText className="h-8 w-8 text-teal-600" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Download Report</h3>
                <p className="text-sm text-gray-600 mb-4">
                  Get a comprehensive PDF report with detailed recommendations and action items.
                </p>
                <Button 
                  onClick={generateReport}
                  disabled={generatingReport}
                  size="sm"
                  className="bg-teal-600 hover:bg-teal-700"
                >
                  Generate PDF
                </Button>
              </div>
              
              <div className="text-center">
                <div className="bg-blue-100 p-4 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                  <MessageSquare className="h-8 w-8 text-blue-600" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Expert Consultation</h3>
                <p className="text-sm text-gray-600 mb-4">
                  Discuss your results with our AI governance experts to develop an action plan.
                </p>
                <Button variant="outline" size="sm">
                  Request Consultation
                </Button>
              </div>
              
              <div className="text-center">
                <div className="bg-green-100 p-4 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                  <BarChart3 className="h-8 w-8 text-green-600" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Track Progress</h3>
                <p className="text-sm text-gray-600 mb-4">
                  Conduct regular assessments to monitor improvements in your AI governance.
                </p>
                <Button 
                  variant="outline" 
                  size="sm"
                  onClick={() => navigate('/dashboard')}
                >
                  View All Assessments
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  );
}

export default ResultsPage;
