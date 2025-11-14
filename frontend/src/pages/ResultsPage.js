import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { toast } from 'sonner';
import Logo from '../components/Logo';
import { 
  ArrowLeft, 
  Download, 
  MessageSquare,
  BarChart3,
  TrendingUp,
  AlertTriangle,
  CheckCircle2,
  FileText,
  Building2,
  Award
} from 'lucide-react';
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer, Tooltip, PieChart, Pie, Cell, Legend } from 'recharts';
import MaturityStackedColumn from '../components/MaturityDonutChart';
import DomainBenchmarkRadar from '../components/DomainBenchmarkRadar';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Color mapping for heatmap (1-4 scale)
const getScoreColor = (percentage, reviewStatus = 'APPROVED') => {
  // Blue for pending review
  if (reviewStatus === 'PENDING_REVIEW') {
    return { bg: '#3B82F6', text: '#FFFFFF' }; // Blue
  }
  
  // Colors for 1-4 scale: 1=Red(25%), 2=Orange(50%), 3=Yellow(75%), 4=Green(100%)
  if (percentage > 87.5) return { bg: '#00B050', text: '#FFFFFF' }; // Green (score 4)
  if (percentage > 62.5) return { bg: '#FFFF00', text: '#000000' }; // Yellow (score 3)
  if (percentage > 37.5) return { bg: '#FFC000', text: '#000000' }; // Orange (score 2)
  return { bg: '#FF0000', text: '#FFFFFF' }; // Red (score 1)
};

const getMaturityBadge = (maturity) => {
  switch (maturity) {
    case 'Leading':
      return { color: 'bg-green-100 text-green-800', icon: CheckCircle2 };
    case 'Established':
      return { color: 'bg-blue-100 text-blue-800', icon: TrendingUp };
    case 'Developing':
      return { color: 'bg-yellow-100 text-yellow-800', icon: TrendingUp };
    case 'Foundational':
      return { color: 'bg-red-100 text-red-800', icon: AlertTriangle };
    // Legacy support for old tier names
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
  const [assessmentType, setAssessmentType] = useState('System');
  const [summary, setSummary] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [generatingReport, setGeneratingReport] = useState(false);
  const [generatingPDF, setGeneratingPDF] = useState(false);
  const [viewMode, setViewMode] = useState('heatmap'); // 'heatmap' or 'benchmark'
  const [benchmarks, setBenchmarks] = useState(null);
  const [benchmarkSector, setBenchmarkSector] = useState(null);

  useEffect(() => {
    fetchResults();
  }, [id]);

  useEffect(() => {
    // Fetch benchmarks when switching to benchmark view for System assessments
    if (viewMode === 'benchmark' && assessmentType === 'System' && user?.industry && !benchmarks) {
      fetchBenchmarks(user.industry);
    }
  }, [viewMode, assessmentType, user]);

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
      setAssessmentType(assessmentResponse.data.assessment_type || 'System');
      
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

  const fetchBenchmarks = async (sector) => {
    try {
      const response = await axios.get(`${API}/sectors/${encodeURIComponent(sector)}/benchmarks`);
      setBenchmarks(response.data.benchmarks);
      setBenchmarkSector(sector);
    } catch (error) {
      console.error('Error fetching benchmarks:', error);
      toast.error('Failed to load sector benchmarks');
    }
  };

  const generateReport = async () => {
    setGeneratingReport(true);
    try {
      const response = await axios.get(`${API}/assessments/${id}/report`, {
        responseType: 'blob', // Important for handling binary DOCX data
        headers: {
          'Accept': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        }
      });
      
      // Create blob URL and trigger download
      const blob = new Blob([response.data], { 
        type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' 
      });
      const url = window.URL.createObjectURL(blob);
      
      // Extract filename from response headers or create default
      const contentDisposition = response.headers['content-disposition'];
      let filename = 'AM_AI_SAFE_Assessment_Report.docx';
      
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?([^"]+)"?/);
        if (filenameMatch) {
          filename = filenameMatch[1];
        }
      }
      
      // Create temporary link element to trigger download
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      
      // Cleanup
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      toast.success('DOCX Report downloaded successfully!');
    } catch (error) {
      console.error('Error generating DOCX report:', error);
      toast.error('Failed to generate DOCX report');
    } finally {
      setGeneratingReport(false);
    }
  };

  const generateExecutiveSummaryPDF = async () => {
    setGeneratingPDF(true);
    try {
      const response = await axios.get(`${API}/assessments/${id}/executive-summary-pdf`, {
        responseType: 'blob',
        headers: {
          'Accept': 'application/pdf'
        }
      });
      
      // Create blob URL and trigger download
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      
      // Extract filename from response headers or create default
      const contentDisposition = response.headers['content-disposition'];
      let filename = 'Executive_Summary.pdf';
      
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?([^"]+)"?/);
        if (filenameMatch) {
          filename = filenameMatch[1];
        }
      }
      
      // Create temporary link element to trigger download
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      
      // Cleanup
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      toast.success('Executive Summary PDF downloaded successfully!');
    } catch (error) {
      console.error('Error generating PDF:', error);
      toast.error('Failed to generate PDF');
    } finally {
      setGeneratingPDF(false);
    }
  };

  // generatePDFReport function removed

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
              <Logo className="h-10 w-10" />
              <div>
                <h1 className="text-base font-bold text-gray-900">AM AI SAFE</h1>
                <p className={`text-xs ${
                  assessmentType === 'Awareness' ? 'text-green-600' 
                  : assessmentType === 'Readiness' ? 'text-blue-600'
                  : 'text-teal-600'
                }`}>
                  {assessmentType === 'Awareness' ? 'AI Awareness & Foundations' 
                   : assessmentType === 'Readiness' ? 'AI Readiness'
                   : 'AI System Maturity'} Assessment Results
                </p>
              </div>
            </div>

            {/* Center - Assessment Name */}
            <div className="flex flex-col items-center">
              <p className="text-sm font-bold text-gray-900">{assessment?.name || 'Loading...'}</p>
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

      {/* Summary Section - Wrapper for PDF generation */}
      <div className="results-summary-content bg-white border-b flex-shrink-0">
        <div className="max-w-full px-6 py-4">
          <div className="flex items-start">
            {/* First 12.5% - Maturity Stacked Column */}
            <div className="flex flex-col items-center justify-center" style={{ width: '12.5%' }}>
              <MaturityStackedColumn score={summary.overall_percentage} />
            </div>

            {/* Second 20% - Maturity Tier Descriptions */}
            <div className="px-4" style={{ width: '20%' }}>
              <p className="text-sm font-bold text-gray-900 mb-2 mt-0">Maturity Tier Description</p>
              <div className="text-xs text-gray-700 space-y-1">
                {assessmentType === 'Awareness' ? (
                  <>
                    <p><span className="font-bold">Foundational (0-40%):</span> Early Awareness</p>
                    <p><span className="font-bold">Developing (41-70%):</span> Building Understanding</p>
                    <p><span className="font-bold">Established (71-100%):</span> Ready for Action</p>
                  </>
                ) : assessmentType === 'Readiness' ? (
                  <>
                    <p><span className="font-bold">Foundational (0-20%):</span> Minimal Foundations</p>
                    <p><span className="font-bold">Developing (21-40%):</span> Building Capability</p>
                    <p><span className="font-bold">Established (41-70%):</span> Strong Readiness</p>
                    <p><span className="font-bold">Leading (71-100%):</span> AI-Ready Organisation</p>
                  </>
                ) : (
                  <>
                    <p><span className="font-bold">Foundational (0-40%):</span> Ad-hoc Beginnings</p>
                    <p><span className="font-bold">Developing (41-65%):</span> Emerging Structure</p>
                    <p><span className="font-bold">Established (66-85%):</span> Integrated Governance</p>
                    <p><span className="font-bold">Leading (86-100%):</span> Optimised Excellence</p>
                  </>
                )}
              </div>
            </div>

            {/* Third 55% - Results Summary Text */}
            <div className="px-6" style={{ width: '55%' }}>
              <p className="text-sm font-bold text-gray-900 mb-2 mt-0">Results Summary</p>
              <p className="text-xs text-gray-700 leading-relaxed">
                {assessmentType === 'Awareness' ? (
                  <>
                    The results indicate that <strong>{assessment?.awareness_info?.org_name || user?.organization_name}</strong> has achieved an overall AI awareness score of <strong>{summary.overall_percentage.toFixed(1)}%</strong>, placing the organization within the <strong>{summary.overall_maturity}</strong> awareness category. This rating reflects {
                      summary.overall_maturity === 'Established'
                        ? 'strong foundational AI awareness across the organization. Leaders and staff demonstrate good understanding of AI concepts, potential applications, and associated risks. The organization is well-positioned to progress to readiness assessment and begin exploring AI implementation opportunities.'
                        : summary.overall_maturity === 'Developing'
                        ? 'growing AI awareness and emerging understanding across the organization. Some individuals are familiar with AI concepts, but knowledge gaps exist. Focus on foundational education, building leadership support, and creating shared understanding of AI opportunities and challenges will strengthen readiness for AI adoption.'
                        : 'early-stage AI awareness with limited understanding across the organization. Most staff and leaders are unfamiliar with AI fundamentals, potential applications, or key considerations. Priority should be on foundational education, building basic AI literacy, and establishing leadership interest before progressing to more advanced assessments.'
                    }
                  </>
                ) : assessmentType === 'Readiness' ? (
                  <>
                    The results indicate that <strong>{assessment?.readiness_info?.org_name || user?.organization_name}</strong> has achieved an overall AI readiness score of <strong>{summary.overall_percentage.toFixed(1)}%</strong>, placing the organization within the <strong>{summary.overall_maturity}</strong> readiness category. This rating reflects {
                      summary.overall_maturity === 'Leading'
                        ? 'comprehensive AI readiness across all foundational domains. The organization demonstrates strong governance, robust data practices, mature technology infrastructure, capable workforce, and embedded ethical frameworks. Leadership actively champions responsible AI, and the organization is well-prepared to deploy AI systems confidently and safely.'
                        : summary.overall_maturity === 'Established'
                        ? 'strong AI readiness foundations with governance structures, data management practices, and technology capabilities in place. The organization has clear policies, engaged leadership, and growing staff capability. Further strengthening of continuous improvement processes, stakeholder engagement, and advanced risk management will position the organization for leading-edge AI adoption.'
                        : summary.overall_maturity === 'Developing'
                        ? 'emerging AI readiness with foundational elements beginning to take shape. Some governance, data, and technology practices exist, but consistency and maturity vary. Priority should be on formalizing AI governance frameworks, strengthening data quality and security, building staff capability, and establishing clear ethical guidelines before advancing to AI implementation.'
                        : 'limited AI readiness with significant capability gaps across governance, data, technology, and workforce domains. Most foundational elements are informal or absent. Immediate focus should be on building basic governance structures, improving data management practices, securing technology infrastructure, and developing staff awareness before considering AI adoption.'
                    }
                  </>
                ) : (
                  <>
                    The results indicate that <strong>{assessment?.system_info?.systemName || assessment?.system_info?.organizationName || user?.organization_name}</strong> has achieved an overall AI maturity score of <strong>{summary.overall_percentage.toFixed(1)}%</strong>, placing this system within the <strong>{summary.overall_maturity}</strong> AI Maturity category. This rating reflects {
                      summary.overall_maturity === 'Leading'
                        ? 'exemplary AI governance and ethical assurance, setting a benchmark for responsible AI leadership. Governance systems are fully embedded, adaptive, and continuously refined through data-driven insights, external validation, and innovation. The focus is on optimisation, transparency, and sustained improvement across all AI operations.'
                        : summary.overall_maturity === 'Established'
                        ? 'well-defined and consistently applied AI governance frameworks across most domains. Risk management, transparency, and ethical oversight are integrated into day-to-day operations. Continuous monitoring and regular review cycles are evident, though further optimisation and automation would strengthen maturity and resilience against evolving AI risks.'
                        : summary.overall_maturity === 'Developing'
                        ? 'growing awareness and emerging structure in its AI governance practices. Some policies and controls are in place, but they are applied inconsistently. Progress has been made in recognising key governance needs; however, targeted improvements are needed to achieve full integration and accountability across the AI lifecycle.'
                        : 'minimal or inconsistent AI governance, with most practices being reactive or informal. Policies, processes, and accountability structures are largely undeveloped, resulting in fragmented oversight and heightened risk exposure. Immediate action is required to establish a foundational governance framework, define roles and responsibilities, and embed basic ethical and risk management principles.'
                    }
                  </>
                )}
              </p>
            </div>
            
            {/* Last 12.5% - Action Buttons */}
            <div className="flex flex-col space-y-2" style={{ width: '12.5%' }}>
              {/* DOCX Report Button */}
              <Button 
                onClick={generateReport}
                disabled={generatingReport}
                className={`${
                  assessmentType === 'Awareness' ? 'bg-green-600 hover:bg-green-700'
                  : assessmentType === 'Readiness' ? 'bg-blue-600 hover:bg-blue-700'
                  : 'bg-teal-600 hover:bg-teal-700'
                } text-xs px-3 py-2`}
                data-testid="generate-report-btn"
              >
                {generatingReport ? (
                  <div className="flex items-center justify-center space-x-2">
                    <div className="loading-spinner w-3 h-3"></div>
                    <span>Generating...</span>
                  </div>
                ) : (
                  <div className="flex items-center justify-center space-x-2">
                    <Download className="h-3 w-3" />
                    <span>Detailed Report (DOCX)</span>
                  </div>
                )}
              </Button>
              
              {/* Executive Summary PDF Button */}
              <Button 
                onClick={generateExecutiveSummaryPDF}
                disabled={generatingPDF}
                className="bg-blue-600 hover:bg-blue-700 text-xs px-3 py-2"
                data-testid="generate-pdf-btn"
              >
                {generatingPDF ? (
                  <div className="flex items-center justify-center space-x-2">
                    <div className="loading-spinner w-3 h-3"></div>
                    <span>Preparing...</span>
                  </div>
                ) : (
                  <div className="flex items-center justify-center space-x-2">
                    <FileText className="h-3 w-3" />
                    <span>Executive Summary (PDF)</span>
                  </div>
                )}
              </Button>
              
              {/* Request Consultation Button */}
              <Button 
                variant="outline"
                className="text-xs px-3 py-2"
                data-testid="request-consultation-btn"
                onClick={() => window.open('https://vciso.one/contact', '_blank')}
              >
                <div className="flex items-center justify-center space-x-2">
                  <MessageSquare className="h-3 w-3" />
                  <span>Request Consultation</span>
                </div>
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content - Three Column Layout */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Panel - 25% width */}
        <div className="w-1/4 bg-white border-r overflow-y-auto">
          <div className="p-4">
            <h2 className="text-base font-bold text-gray-900 mb-3 flex items-center space-x-2">
              <BarChart3 className={`h-4 w-4 ${
                assessmentType === 'Awareness' ? 'text-green-600'
                : assessmentType === 'Readiness' ? 'text-blue-600'
                : 'text-teal-600'
              }`} />
              <span>Domain Scores</span>
            </h2>
            
            <div className="space-y-2" data-testid="domain-scores-list">
              {[...summary.domain_scores]
                .sort((a, b) => a.percentage - b.percentage) // Sort by percentage, lowest first
                .map((domain, index) => {
                const colors = getScoreColor(domain.percentage);
                return (
                  <div key={domain.domain_id} className="space-y-0.5">
                    <div className="flex flex-col">
                      <span className="font-medium text-gray-900 text-xs">{domain.domain_name}</span>
                      <div 
                        className="px-1 py-0.5 rounded text-xs font-bold self-start mt-1"
                        style={{ backgroundColor: colors.bg, color: colors.text }}
                      >
                        {domain.percentage.toFixed(1)}%
                      </div>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-1.5">
                      <div 
                        className="h-1.5 rounded-full transition-all duration-300"
                        style={{ width: `${domain.percentage}%`, backgroundColor: colors.bg }}
                      ></div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Center Panel - Assessment Heatmap / Domain Benchmarks - 50% width */}
        <div className="w-1/2 bg-white border-r overflow-y-auto">
          <div className="p-4">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-bold text-gray-900 flex items-center space-x-2">
                <BarChart3 className={`h-5 w-5 ${
                  assessmentType === 'Awareness' ? 'text-green-600'
                  : assessmentType === 'Readiness' ? 'text-blue-600'
                  : 'text-teal-600'
                }`} />
                <span>{viewMode === 'heatmap' ? 'Assessment Heatmap' : 'Domain Benchmarks'}</span>
              </h2>
              
              {/* Radio buttons - only show for System assessments */}
              {assessmentType === 'System' && (
                <div className="flex items-center space-x-4">
                  <label className="flex items-center cursor-pointer">
                    <input
                      type="radio"
                      name="viewMode"
                      value="heatmap"
                      checked={viewMode === 'heatmap'}
                      onChange={(e) => setViewMode(e.target.value)}
                      className="mr-2 h-4 w-4 text-teal-600 focus:ring-teal-500"
                    />
                    <span className="text-sm font-medium text-gray-700">Assessment Heatmap</span>
                  </label>
                  <label className="flex items-center cursor-pointer">
                    <input
                      type="radio"
                      name="viewMode"
                      value="benchmark"
                      checked={viewMode === 'benchmark'}
                      onChange={(e) => setViewMode(e.target.value)}
                      className="mr-2 h-4 w-4 text-teal-600 focus:ring-teal-500"
                    />
                    <span className="text-sm font-medium text-gray-700">Domain Benchmarks</span>
                  </label>
                </div>
              )}
            </div>
            
            <div className="space-y-1" data-testid="assessment-heatmap">
              {[...summary.domain_scores]
                .sort((a, b) => a.percentage - b.percentage) // Sort by percentage, lowest first
                .map((domain) => {
                const domainQuestions = questions.filter(q => q.domain_id === domain.domain_id);
                const domainAnswers = answers.filter(a => 
                  domainQuestions.some(q => q.id === a.question_id)
                );
                
                return (
                  <div key={domain.domain_id} className="flex items-center py-0.5">
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
                          const reviewStatus = answer ? answer.review_status : 'APPROVED';
                          return { ...question, score, reviewStatus };
                        })
                        .sort((a, b) => a.score - b.score) // Sort by score, lowest first
                        .map((question) => {
                        const score = question.score;
                        const percentage = (score / 4) * 100; // Max score is 4 (1-4 scale)
                        const colors = getScoreColor(percentage, question.reviewStatus);
                        
                        return (
                          <div
                            key={question.id}
                            className="p-2 rounded text-center border border-gray-300"
                            style={{ backgroundColor: colors.bg, color: colors.text }}
                            title={`${question.code}: ${question.text} (Score: ${score}/4)${question.reviewStatus === 'PENDING_REVIEW' ? ' - Pending Review' : ''}`}
                            data-testid={`heatmap-cell-${question.code}`}
                          >
                            <div className="font-bold text-xs">{question.code}</div>
                            <div className="text-xs opacity-90">{question.reviewStatus === 'PENDING_REVIEW' ? 'Review' : `${score}/4`}</div>
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

        {/* Right Panel - 25% width */}
        <div className="w-1/4 bg-white overflow-y-auto">
          <div className="p-4">
            {/* Pie Chart - Response Distribution */}
            <div className="mb-3">
              <h2 className="text-base font-bold text-gray-900 mb-1 flex items-center space-x-2">
                <BarChart3 className="h-4 w-4 text-teal-600" />
                <span>Response Distribution</span>
              </h2>
              <div className="h-48">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={(() => {
                        // Calculate distribution of answers by score category (1-4 scale)
                        const distribution = {
                          'Foundational': 0,
                          'Developing': 0,
                          'Established': 0,
                          'Leading': 0
                        };
                        
                        // Count all answered questions based on numeric score
                        answers.forEach(answer => {
                          if (answer.numeric_score === 1) {
                            distribution['Foundational']++;
                          } else if (answer.numeric_score === 2) {
                            distribution['Developing']++;
                          } else if (answer.numeric_score === 3) {
                            distribution['Established']++;
                          } else if (answer.numeric_score === 4) {
                            distribution['Leading']++;
                          }
                        });
                        
                        // Convert to array format for pie chart
                        return Object.entries(distribution)
                          .filter(([_, value]) => value > 0) // Only show categories with data
                          .map(([name, value]) => ({ name, value }));
                      })()}
                      cx="50%"
                      cy="50%"
                      innerRadius={0}
                      outerRadius={55}
                      paddingAngle={2}
                      dataKey="value"
                      label={(props) => {
                        const { cx, cy, midAngle, outerRadius, name, value } = props;
                        const RADIAN = Math.PI / 180;
                        const radius = outerRadius + 20;
                        const x = cx + radius * Math.cos(-midAngle * RADIAN);
                        const y = cy + radius * Math.sin(-midAngle * RADIAN);
                        
                        const total = answers.length;
                        const percent = ((value / total) * 100).toFixed(1);
                        
                        return (
                          <text
                            x={x}
                            y={y}
                            fill="#333"
                            textAnchor={x > cx ? 'start' : 'end'}
                            dominantBaseline="central"
                          >
                            <tspan x={x} dy="0" fontSize="12" fontWeight="500">
                              {name}: {value}
                            </tspan>
                            <tspan x={x} dy="14" fontSize="10" fill="#666">
                              ({percent}%)
                            </tspan>
                          </text>
                        );
                      }}
                      labelLine={{ stroke: '#666', strokeWidth: 1 }}
                    >
                      {(() => {
                        // Define colors matching heatmap (updated for new categories)
                        const colorMap = {
                          'Foundational': '#FF0000',  // red
                          'Developing': '#FFC000',    // orange
                          'Established': '#FFFF00',   // yellow
                          'Leading': '#00B050'        // green
                        };
                        
                        const distribution = {
                          'Foundational': 0,
                          'Developing': 0,
                          'Established': 0,
                          'Leading': 0
                        };
                        
                        answers.forEach(answer => {
                          if (answer.numeric_score === 1) {
                            distribution['Foundational']++;
                          } else if (answer.numeric_score === 2) {
                            distribution['Developing']++;
                          } else if (answer.numeric_score === 3) {
                            distribution['Established']++;
                          } else if (answer.numeric_score === 4) {
                            distribution['Leading']++;
                          }
                        });
                        
                        return Object.entries(distribution)
                          .filter(([_, value]) => value > 0)
                          .map(([name, _], index) => (
                            <Cell key={`cell-${index}`} fill={colorMap[name]} />
                          ));
                      })()}
                    </Pie>
                    <Tooltip 
                      formatter={(value) => `${value} questions`}
                      contentStyle={{ 
                        backgroundColor: 'white', 
                        border: '1px solid #e5e7eb',
                        borderRadius: '0.375rem',
                        fontSize: '12px'
                      }}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Key Strengths */}
            <div className="mb-3">
              <div className="mb-2">
                <h2 className="text-base font-bold text-gray-900 flex items-center space-x-2 mb-1">
                  <CheckCircle2 className="h-4 w-4 text-green-600" />
                  <span>Key Strengths</span>
                </h2>
                <p className="text-xs text-gray-600 ml-6">
                  Domains demonstrating the strongest maturity, effective governance, and well-embedded responsible AI practices.
                </p>
              </div>
              <div className="space-y-1.5">
                {[...summary.domain_scores]
                  .sort((a, b) => b.percentage - a.percentage) // Sort highest first
                  .slice(0, 3)
                  .map((domain, index) => {
                    const colors = getScoreColor(domain.percentage);
                    return (
                      <div key={domain.domain_id} className="flex items-center space-x-2 p-2 bg-green-50 rounded border border-green-200">
                        <div className="flex-shrink-0 w-6 h-6 rounded-full bg-green-600 text-white flex items-center justify-center text-xs font-bold">
                          {index + 1}
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="text-xs font-medium text-gray-900 truncate">{domain.domain_name}</div>
                        </div>
                        <div 
                          className="px-2 py-0.5 rounded text-xs font-bold"
                          style={{ backgroundColor: colors.bg, color: colors.text }}
                        >
                          {domain.percentage.toFixed(1)}%
                        </div>
                      </div>
                    );
                  })}
              </div>
            </div>

            {/* Priority Improvement Areas */}
            <div>
              <div className="mb-2">
                <h2 className="text-base font-bold text-gray-900 flex items-center space-x-2 mb-1">
                  <AlertTriangle className="h-4 w-4 text-red-600" />
                  <span>Priority Improvement Areas</span>
                </h2>
                <p className="text-xs text-gray-600 ml-6">
                  Domains requiring focused uplift to strengthen oversight, consistency, and alignment with leading AI governance standards.
                </p>
              </div>
              <div className="space-y-1.5">
                {[...summary.domain_scores]
                  .sort((a, b) => a.percentage - b.percentage) // Sort lowest first
                  .slice(0, 3)
                  .map((domain, index) => {
                    const colors = getScoreColor(domain.percentage);
                    return (
                      <div key={domain.domain_id} className="flex items-center space-x-2 p-2 bg-red-50 rounded border border-red-200">
                        <div className="flex-shrink-0 w-6 h-6 rounded-full bg-red-600 text-white flex items-center justify-center text-xs font-bold">
                          {index + 1}
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="text-xs font-medium text-gray-900 truncate">{domain.domain_name}</div>
                        </div>
                        <div 
                          className="px-2 py-0.5 rounded text-xs font-bold"
                          style={{ backgroundColor: colors.bg, color: colors.text }}
                        >
                          {domain.percentage.toFixed(1)}%
                        </div>
                      </div>
                    );
                  })}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ResultsPage;
