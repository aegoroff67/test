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
    case 'Excellent':
      return { color: 'bg-green-100 text-green-800', icon: CheckCircle2 };
    case 'Good':
      return { color: 'bg-blue-100 text-blue-800', icon: TrendingUp };
    case 'Moderate':
      return { color: 'bg-yellow-100 text-yellow-800', icon: TrendingUp };
    case 'Low':
      return { color: 'bg-orange-100 text-orange-800', icon: AlertTriangle };
    case 'Basic':
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
      // TESTING: Use mock data for layout testing
      if (id === 'test-assessment-id') {
        // Mock assessment data
        setAssessment({
          id: 'test-assessment-id',
          user_id: 'test-user-id',
          status: 'COMPLETED',
          created_at: new Date().toISOString()
        });
        
        // Mock questions data
        const mockQuestions = [];
        const mockAnswers = [];
        
        // Create mock questions for 11 domains with 8 questions each
        const domains = [
          { id: 1, name: 'Fairness & Bias' },
          { id: 2, name: 'Transparency' },
          { id: 3, name: 'Reliability' },
          { id: 4, name: 'Security' },
          { id: 5, name: 'Privacy' },
          { id: 6, name: 'Safety' },
          { id: 7, name: 'Inclusivity' },
          { id: 8, name: 'Sustainability' },
          { id: 9, name: 'Accountability' },
          { id: 10, name: 'Human Oversight' },
          { id: 11, name: 'Robustness' }
        ];
        
        domains.forEach(domain => {
          for (let i = 1; i <= 8; i++) {
            const questionId = `${domain.id}-${i}`;
            const question = {
              id: questionId,
              domain_id: domain.id,
              code: `${domain.name.substring(0, 2).toUpperCase()}-${i}`,
              text: `Sample question ${i} for ${domain.name} domain`,
              order: i
            };
            mockQuestions.push(question);
            
            // Mock answer with random score
            const score = Math.floor(Math.random() * 4); // 0-3
            mockAnswers.push({
              question_id: questionId,
              numeric_score: score,
              question: question
            });
          }
        });
        
        setQuestions(mockQuestions);
        setAnswers(mockAnswers);
        
        // Mock summary data
        const mockSummary = {
          overall_percentage: 67.5,
          overall_maturity: 'Good',
          domain_scores: domains.map(domain => ({
            domain_id: domain.id,
            domain_name: domain.name,
            score: Math.floor(Math.random() * 20) + 5, // 5-24
            max_score: 24,
            percentage: Math.floor(Math.random() * 60) + 20 // 20-80%
          }))
        };
        
        setSummary(mockSummary);
        setLoading(false);
        return;
      }
      
      // Original API calls for real data
      const assessmentResponse = await axios.get(`${API}/assessments/${id}`);
      setAssessment(assessmentResponse.data);
      
      const questionsResponse = await axios.get(`${API}/assessments/${id}/questions`);
      const questionData = questionsResponse.data;
      
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
    <div className="h-screen bg-gray-50 flex flex-col">
      {/* Compact Header */}
      <header className="bg-white shadow-sm border-b flex-shrink-0">
        <div className="max-w-full px-6">
          <div className="flex justify-between items-center h-14">
            {/* Logo & Title */}
            <div className="flex items-center space-x-3">
              <div className="bg-teal-600 p-1.5 rounded-lg">
                <Shield className="h-5 w-5 text-white" />
              </div>
              <div>
                <h1 className="text-base font-bold text-gray-900">AM AI SAFE</h1>
                <p className="text-xs text-teal-600">Assessment Results</p>
              </div>
            </div>

            {/* Back Button */}
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
      </header>

      {/* Summary Section */}
      <div className="bg-white border-b flex-shrink-0">
        <div className="max-w-full px-6 py-4">
          <div className="flex items-center">
            {/* First 12.5% - Overall Maturity Score */}
            <div className="flex flex-col items-center" style={{ width: '12.5%' }}>
              <div className={`w-20 h-20 rounded-full border-4 flex items-center justify-center mb-2 ${getScoreColor(summary.overall_percentage).bg.replace('bg-', 'border-')} ${getScoreColor(summary.overall_percentage).bg}`}>
                <div className="text-center">
                  <div className="text-lg font-bold text-white" data-testid="overall-score">
                    {summary.overall_percentage.toFixed(1)}%
                  </div>
                </div>
              </div>
              <Badge className={`text-xs px-2 py-1 ${maturityInfo.color}`} data-testid="maturity-level">
                {summary.overall_maturity} AI MATURITY
              </Badge>
            </div>

            {/* Second 12.5% - Organization Info */}
            <div className="px-4" style={{ width: '12.5%' }}>
              <p className="text-sm font-bold text-gray-900">Organisation: {user?.organization_name}</p>
              <p className="text-sm font-bold text-gray-900">Report Date: {new Date().toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' })}</p>
            </div>

            {/* Third 62.5% - Results Summary Text */}
            <div className="px-6" style={{ width: '62.5%' }}>
              <p className="text-sm font-bold text-gray-900 mb-1">Results Summary:</p>
              <p className="text-sm text-gray-700 leading-relaxed">
                The results indicate that <strong>{user?.organization_name}</strong> has achieved an overall AI maturity score of <strong>{summary.overall_percentage.toFixed(1)}%</strong>, placing the organization within the <strong>{summary.overall_maturity}</strong> AI Maturity category. This rating reflects {
                  summary.overall_maturity === 'Excellent' 
                    ? 'outstanding alignment with AI governance best practices across all domains, with well-developed systems, processes, and policies that are consistently implemented and frequently reviewed for continuous improvement.'
                    : summary.overall_maturity === 'Good'
                    ? 'strong performance in AI governance with many best practices implemented across most areas. While there are minor gaps, they are not critical and can be addressed with targeted improvements.'
                    : summary.overall_maturity === 'Moderate'
                    ? 'a foundation of AI governance practices with some critical areas requiring enhancement to meet industry best practices and mitigate emerging risks. Structured improvement efforts are needed for consistency.'
                    : summary.overall_maturity === 'Low'
                    ? 'limited alignment with AI governance best practices and significant deficiencies across multiple domains. The organization requires immediate attention to address gaps and implement comprehensive governance measures.'
                    : 'minimal or no AI governance processes in place, indicating critical improvement needs. Fundamental governance frameworks must be established to mitigate potential failures and ensure responsible AI deployment.'
                }
              </p>
              <p className="text-sm text-gray-700 mt-2">
                The heatmap below shows domains and questions sorted by lowest score to help prioritize improvement areas.
              </p>
            </div>
            
            {/* Last 12.5% - Action Buttons */}
            <div className="flex flex-col space-y-3" style={{ width: '12.5%' }}>
              <Button 
                onClick={generateReport}
                disabled={generatingReport}
                className="bg-teal-600 hover:bg-teal-700 text-xs px-3 py-2"
                data-testid="generate-report-btn"
              >
                {generatingReport ? (
                  <div className="flex flex-col items-center">
                    <div className="loading-spinner w-3 h-3 mb-1"></div>
                    <span>Generating...</span>
                  </div>
                ) : (
                  <div className="flex flex-col items-center">
                    <Download className="h-3 w-3 mb-1" />
                    <span>Generate PDF Report</span>
                  </div>
                )}
              </Button>
              
              <Button 
                variant="outline"
                className="text-xs px-3 py-2"
                data-testid="request-consultation-btn"
                onClick={() => window.open('https://vciso.one/contact', '_blank')}
              >
                <div className="flex flex-col items-center">
                  <MessageSquare className="h-3 w-3 mb-1" />
                  <span>Request Consultation</span>
                </div>
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content - Two Column Layout */}
      <div className="flex-1 flex overflow-hidden">
        {/* Domain Scores Column - Half the previous width */}
        <div className="w-1/6 bg-white border-r overflow-y-auto">
          <div className="p-4">
            <h2 className="text-base font-bold text-gray-900 mb-3 flex items-center space-x-2">
              <BarChart3 className="h-4 w-4 text-teal-600" />
              <span>Domain Scores</span>
            </h2>
            
            <div className="space-y-3" data-testid="domain-scores-list">
              {[...summary.domain_scores]
                .sort((a, b) => a.percentage - b.percentage) // Sort by percentage, lowest first
                .map((domain, index) => {
                const colors = getScoreColor(domain.percentage);
                return (
                  <div key={domain.domain_id} className="space-y-1">
                    <div className="flex flex-col">
                      <span className="font-medium text-gray-900 text-xs">{domain.domain_name}</span>
                      <div className={`px-1 py-0.5 rounded text-xs font-bold ${colors.bg} ${colors.text} self-start mt-1`}>
                        {domain.percentage.toFixed(1)}%
                      </div>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-1.5">
                      <div 
                        className={`${colors.bg} h-1.5 rounded-full transition-all duration-300`}
                        style={{ width: `${domain.percentage}%` }}
                      ></div>
                    </div>
                    <p className="text-xs text-gray-600">
                      {domain.score} / {domain.max_score}
                    </p>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Assessment Heatmap Column - Takes up remaining space */}
        <div className="flex-1 bg-white overflow-y-auto">
          <div className="p-4">
            <h2 className="text-lg font-bold text-gray-900 mb-4 flex items-center space-x-2">
              <Shield className="h-5 w-5 text-teal-600" />
              <span>Assessment Heatmap</span>
            </h2>
            
            <div className="space-y-2" data-testid="assessment-heatmap">
              {[...summary.domain_scores]
                .sort((a, b) => a.percentage - b.percentage) // Sort by percentage, lowest first
                .map((domain) => {
                const domainQuestions = questions.filter(q => q.domain_id === domain.domain_id);
                const domainAnswers = answers.filter(a => 
                  domainQuestions.some(q => q.id === a.question_id)
                );
                
                return (
                  <div key={domain.domain_id} className="flex items-center py-1">
                    {/* Domain name on the left */}
                    <div className="w-32 flex-shrink-0 pr-4">
                      <div className="text-sm font-medium text-gray-900">{domain.domain_name}</div>
                      <div className="text-xs text-gray-600">({domain.percentage.toFixed(1)}%)</div>
                    </div>
                    
                    {/* Question buttons on the same row */}
                    <div className="flex-1 grid grid-cols-8 gap-1">
                      {domainQuestions
                        .map((question) => {
                          const answer = domainAnswers.find(a => a.question_id === question.id);
                          const score = answer ? answer.numeric_score : 0;
                          return { ...question, score };
                        })
                        .sort((a, b) => a.score - b.score) // Sort by score, lowest first
                        .map((question) => {
                        const score = question.score;
                        const percentage = (score / 3) * 100; // Max score is 3
                        const colors = getScoreColor(percentage);
                        
                        return (
                          <div
                            key={question.id}
                            className={`p-2 rounded text-center ${colors.bg} ${colors.text} border border-gray-300`}
                            title={`${question.code}: ${question.text} (Score: ${score}/3)`}
                            data-testid={`heatmap-cell-${question.code}`}
                          >
                            <div className="font-bold text-xs">{question.code}</div>
                            <div className="text-xs opacity-90">{score}/3</div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ResultsPage;
