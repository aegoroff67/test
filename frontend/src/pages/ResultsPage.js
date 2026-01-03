import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useSearchParams } from 'react-router-dom';
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
  Award,
  Grid3X3,
  Info
} from 'lucide-react';
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer, Tooltip, PieChart, Pie, Cell, Legend } from 'recharts';
import MaturityStackedColumn from '../components/MaturityDonutChart';
import DomainBenchmarkRadar from '../components/DomainBenchmarkRadar';
import { INDUSTRIES, getBenchmarkSector } from '../constants/industries';

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
  const [searchParams] = useSearchParams();
  
  const [assessment, setAssessment] = useState(null);
  const [assessmentType, setAssessmentType] = useState('System');
  const [summary, setSummary] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [generatingReport, setGeneratingReport] = useState(false);
  const [generatingPDF, setGeneratingPDF] = useState(false);
  
  // Check URL parameter for initial view mode (for PDF generation)
  const urlViewParam = searchParams.get('view');
  const initialViewMode = (urlViewParam === 'radar' || urlViewParam === 'heatmap') ? urlViewParam : 'heatmap';
  const [viewMode, setViewMode] = useState(initialViewMode); // 'heatmap' or 'radar'
  const [benchmarks, setBenchmarks] = useState(null);
  const [benchmarkSector, setBenchmarkSector] = useState(null);
  const [showIndustrySelector, setShowIndustrySelector] = useState(false);
  const [selectedIndustry, setSelectedIndustry] = useState('');
  const [actionSteps, setActionSteps] = useState(null);
  const [sectorAverage, setSectorAverage] = useState(null);
  const [showFrameworkCoverage, setShowFrameworkCoverage] = useState(false);
  const [commentaryExpanded, setCommentaryExpanded] = useState(false);

  useEffect(() => {
    fetchResults();
  }, [id]);

  useEffect(() => {
    // Fetch benchmarks when switching to radar view for System, Awareness, Readiness, or Orgwide assessments
    // Try to get industry from: 1) assessment.system_info/awareness_info/readiness_info/orgwide_info, 2) user.industry, 3) selected industry
    if (viewMode === 'radar' && (assessmentType === 'System' || assessmentType === 'Awareness' || assessmentType === 'Readiness' || assessmentType === 'Orgwide') && !benchmarks) {
      let industry;
      
      // Get industry based on assessment type
      if (assessmentType === 'System') {
        industry = assessment?.system_info?.industry || user?.industry || selectedIndustry;
      } else if (assessmentType === 'Awareness') {
        industry = assessment?.awareness_info?.industry || user?.industry || selectedIndustry;
      } else if (assessmentType === 'Readiness') {
        industry = assessment?.readiness_info?.industry || user?.industry || selectedIndustry;
      } else if (assessmentType === 'Orgwide') {
        industry = assessment?.orgwide_info?.industry || user?.industry || selectedIndustry;
      }
      
      console.log('Attempting to fetch benchmarks with industry:', industry);
      console.log('Assessment type:', assessmentType);
      console.log('Assessment info:', assessment?.system_info || assessment?.awareness_info || assessment?.readiness_info || assessment?.orgwide_info);
      console.log('User industry:', user?.industry);
      
      if (industry) {
        fetchBenchmarks(industry, assessmentType);
        setShowIndustrySelector(false);
      } else {
        console.error('No industry found - showing industry selector');
        setShowIndustrySelector(true);
      }
    }
  }, [viewMode, assessmentType, user, assessment, selectedIndustry]);

  useEffect(() => {
    // Fetch sector average for Awareness, System, Readiness, and Orgwide assessments (needed for results summary)
    if ((assessmentType === 'Awareness' || assessmentType === 'System' || assessmentType === 'Readiness' || assessmentType === 'Orgwide') && assessment && sectorAverage === null) {
      let industry;
      if (assessmentType === 'Awareness') {
        industry = assessment?.awareness_info?.industry || user?.industry;
      } else if (assessmentType === 'System') {
        industry = assessment?.system_info?.industry || user?.industry;
      } else if (assessmentType === 'Readiness') {
        industry = assessment?.readiness_info?.industry || user?.industry;
      } else if (assessmentType === 'Orgwide') {
        industry = assessment?.orgwide_info?.industry || user?.industry;
      }
      
      if (industry) {
        fetchBenchmarks(industry, assessmentType);
      }
    }
  }, [assessmentType, assessment, user, sectorAverage]);

  useEffect(() => {
    // Fetch action steps for Awareness assessments
    if (assessmentType === 'Awareness' && assessment && !actionSteps) {
      const industry = assessment?.awareness_info?.industry || user?.industry;
      if (industry) {
        fetchActionSteps(industry);
      }
    }
  }, [assessmentType, assessment, user, actionSteps]);

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
      console.log('Summary response:', summaryResponse.data);
      console.log('Has recommendation_summary?', !!summaryResponse.data.recommendation_summary);
      setSummary(summaryResponse.data);
      
    } catch (error) {
      console.error('Error loading results:', error);
      toast.error('Failed to load results');
      navigate('/dashboard');
    } finally {
      setLoading(false);
    }
  };

  const fetchBenchmarks = async (industry, type = 'System') => {
    try {
      // Get the benchmark sector (now all industries have direct benchmark data in v2)
      const benchmarkSector = getBenchmarkSector(industry);
      
      console.log('=== BENCHMARK FETCH DEBUG ===');
      console.log('Industry:', industry);
      console.log('Assessment Type:', type);
      console.log('Benchmark sector:', benchmarkSector);
      console.log('Full URL:', `${API}/sectors/${encodeURIComponent(benchmarkSector)}/benchmarks?assessment_type=${type}`);
      
      const response = await axios.get(`${API}/sectors/${encodeURIComponent(benchmarkSector)}/benchmarks`, {
        params: { assessment_type: type }
      });
      console.log('Benchmarks response:', response.data);
      console.log('=== FETCH SUCCESS ===');
      
      setBenchmarks(response.data.benchmarks);
      setBenchmarkSector(benchmarkSector);
      
      // Store sector average if available (for Awareness assessments)
      if (response.data.sector_average !== undefined) {
        setSectorAverage(response.data.sector_average);
      }
    } catch (error) {
      console.error('=== BENCHMARK FETCH ERROR ===');
      console.error('Error:', error);
      console.error('Error response:', error.response);
      console.error('Error details:', error.response?.data);
      console.error('Status code:', error.response?.status);
      toast.error(`Failed to load sector benchmarks${error.response?.data?.detail ? ': ' + error.response.data.detail : ''}`);
    }
  };

  const fetchActionSteps = async (industry) => {
    try {
      const benchmarkSector = getBenchmarkSector(industry);
      console.log('Fetching action steps for sector:', benchmarkSector);
      
      const response = await axios.get(`${API}/awareness/action-steps/${encodeURIComponent(benchmarkSector)}`);
      console.log('Action steps response:', response.data);
      
      setActionSteps(response.data.action_steps);
    } catch (error) {
      console.error('Error fetching action steps:', error);
      toast.error('Failed to load action steps');
    }
  };

  const generateReport = async () => {
    setGeneratingReport(true);
    try {
      // Pass the current view mode to backend
      console.log('=== GENERATING REPORT ===');
      console.log('Current viewMode:', viewMode);
      console.log('Sending view_type:', viewMode);
      
      const response = await axios.get(`${API}/assessments/${id}/report`, {
        params: {
          view_type: viewMode  // 'heatmap' or 'radar'
        },
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
      console.log('=== GENERATING PDF ===');
      console.log('Current viewMode:', viewMode);
      console.log('Sending view_type:', viewMode);
      
      const response = await axios.get(`${API}/assessments/${id}/executive-summary-pdf`, {
        params: {
          view_type: viewMode  // 'heatmap' or 'radar'
        },
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
                  : assessmentType === 'Orgwide' ? 'text-purple-600'
                  : 'text-teal-600'
                }`}>
                  {assessmentType === 'Awareness' ? 'AI Awareness & Foundations' 
                   : assessmentType === 'Readiness' ? 'AI Readiness'
                   : assessmentType === 'Orgwide' ? 'Organisation-wide AI Maturity'
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
      <div className={`results-summary-content border-b flex-shrink-0 ${
        assessmentType === 'System' ? 'bg-gradient-to-r from-teal-50 to-teal-100/50'
        : assessmentType === 'Awareness' ? 'bg-gradient-to-r from-green-50 to-green-100/50'
        : assessmentType === 'Readiness' ? 'bg-gradient-to-r from-blue-50 to-blue-100/50'
        : assessmentType === 'Orgwide' ? 'bg-gradient-to-r from-purple-50 to-purple-100/50'
        : 'bg-white'
      }`}>
        <div className="max-w-full px-6 py-4">
          <div className="flex items-start">
            {/* First 15% - Maturity Stacked Column */}
            <div className="flex flex-col items-center justify-center" style={{ width: '15%' }}>
              <MaturityStackedColumn 
                score={summary.overall_percentage} 
                assessmentType={assessmentType}
                sectorAverage={(assessmentType === 'Awareness' || assessmentType === 'System' || assessmentType === 'Readiness') ? sectorAverage : null}
                sectorName={
                  assessmentType === 'System' ? (benchmarkSector || assessment?.system_info?.industry || user?.industry) 
                  : assessmentType === 'Readiness' ? (benchmarkSector || assessment?.readiness_info?.industry || user?.industry)
                  : null
                }
              />
            </div>

            {/* Second 15% - Maturity Tier Descriptions */}
            <div className="px-4" style={{ width: '15%' }}>
              <p className="text-sm font-bold text-gray-900 mb-2 mt-0">
                {assessmentType === 'Awareness' ? 'Awareness Tier Description' 
                 : assessmentType === 'Readiness' ? 'Readiness Tier Description'
                 : 'Maturity Tier Description'}
              </p>
              <div className="text-gray-700 space-y-1" style={{ fontSize: '11px' }}>
                {assessmentType === 'Awareness' ? (
                  <>
                    <p><span className="font-bold">Established (86-100%):</span> Ready to Progress</p>
                    <p><span className="font-bold">Developing (66-85%):</span> Building Readiness</p>
                    <p><span className="font-bold">Emerging (41-65%):</span> Exploring Opportunities</p>
                    <p><span className="font-bold">Introductory (0-40%):</span> Early Awareness</p>
                  </>
                ) : assessmentType === 'Readiness' ? (
                  <>
                    <p><span className="font-bold">Leading (86-100%):</span> AI-Ready</p>
                    <p><span className="font-bold">Established (66-85%):</span> Operational Readiness</p>
                    <p><span className="font-bold">Developing (41-65%):</span> Emerging Capability</p>
                    <p><span className="font-bold">Foundational (0-40%):</span> Limited Foundations</p>
                  </>
                ) : (
                  <>
                    <p><span className="font-bold">Leading (86-100%):</span> Optimised Excellence</p>
                    <p><span className="font-bold">Established (66-85%):</span> Integrated Governance</p>
                    <p><span className="font-bold">Developing (41-65%):</span> Emerging Structure</p>
                    <p><span className="font-bold">Foundational (0-40%):</span> Ad-hoc Beginnings</p>
                  </>
                )}
              </div>
            </div>

            {/* Third 50% - Results Summary Text */}
            <div className="px-6" style={{ width: '50%' }}>
              <p className="text-sm font-bold text-gray-900 mb-2 mt-0">Results Summary</p>
              <p className="text-xs text-gray-700 leading-relaxed">
                {assessmentType === 'Awareness' ? (
                  <>
                    Your organisation demonstrates <strong>{summary.overall_maturity}</strong> AI awareness with an overall score of <strong>{summary.overall_percentage.toFixed(1)}%</strong>{
                      sectorAverage !== null && benchmarkSector ? (
                        (() => {
                          const userScore = summary.overall_percentage;
                          const avgScore = sectorAverage;
                          const comparison = userScore > avgScore ? 'above' : userScore < avgScore ? 'below' : 'equal to';
                          return (
                            <>, which is <strong>{comparison}</strong> the <strong>{benchmarkSector}</strong> sector AI awareness average of <strong>{avgScore}%</strong>.</>
                          );
                        })()
                      ) : '.'
                    } {
                      summary.overall_maturity === 'Established'
                        ? 'Your organisation demonstrates strong and well-distributed AI awareness. Leaders and staff show clear understanding of AI concepts, realistic capabilities, and potential benefits and risks. This puts you in an excellent position to progress into formal readiness assessment and begin exploring structured AI initiatives or early pilots.'
                        : summary.overall_maturity === 'Developing'
                        ? 'AI awareness is growing consistently across the organisation. Many individuals understand core concepts and can identify relevant opportunities, though some knowledge gaps remain. Strengthening leadership engagement, deepening practical understanding, and establishing light governance foundations will support your transition into readiness assessment.'
                        : summary.overall_maturity === 'Emerging'
                        ? 'Your organisation is showing early signs of AI awareness, with isolated pockets of understanding and increasing curiosity. While some staff recognise potential use cases, overall knowledge remains inconsistent. Focus on foundational education, awareness sessions, and building shared language around AI to prepare for the next stage of capability development.'
                        : 'Your organisation is at the beginning of its AI awareness journey. Most staff and leaders are unfamiliar with AI fundamentals, potential applications, or key risks. Priority should be placed on introductory education, building basic literacy, and fostering leadership interest before moving into deeper assessments or planning activities.'
                    }
                  </>
                ) : assessmentType === 'Readiness' ? (
                  <>
                    The results indicate that <strong>{assessment?.readiness_info?.org_name || user?.organization_name}</strong> has achieved an overall AI readiness score of <strong>{summary.overall_percentage.toFixed(1)}%</strong>, placing the organization within the <strong>{summary.overall_maturity}</strong> readiness category{
                      sectorAverage !== null && benchmarkSector ? (
                        (() => {
                          const userScore = summary.overall_percentage;
                          const avgScore = sectorAverage;
                          const comparison = userScore > avgScore ? 'above' : userScore < avgScore ? 'below' : 'equal to';
                          return (
                            <>, which is <strong>{comparison}</strong> the <strong>{benchmarkSector}</strong> sector AI readiness average of <strong>{avgScore}%</strong>.</>
                          );
                        })()
                      ) : '.'
                    } This rating reflects {
                      summary.overall_maturity === 'Leading'
                        ? 'comprehensive AI readiness across all foundational domains. The organization demonstrates strong governance, robust data practices, mature technology infrastructure, capable workforce, and embedded ethical frameworks. Leadership actively champions responsible AI, and the organization is well-prepared to deploy AI systems confidently and safely.'
                        : summary.overall_maturity === 'Established'
                        ? 'strong AI readiness foundations with governance structures, data management practices, and technology capabilities in place. The organization has clear policies, engaged leadership, and growing staff capability. Further strengthening of continuous improvement processes, stakeholder engagement, and advanced risk management will position the organization for leading-edge AI adoption.'
                        : summary.overall_maturity === 'Developing'
                        ? 'emerging AI readiness with foundational elements beginning to take shape. Some governance, data, and technology practices exist, but consistency and maturity vary. Priority should be on formalizing AI governance frameworks, strengthening data quality and security, building staff capability, and establishing clear ethical guidelines before advancing to AI implementation.'
                        : 'limited AI readiness with significant capability gaps across governance, data, technology, and workforce domains. Most foundational elements are informal or absent. Immediate focus should be on building basic governance structures, improving data management practices, securing technology infrastructure, and developing staff awareness before considering AI adoption.'
                    }
                  </>
                ) : assessmentType === 'Orgwide' ? (
                  <>
                    The results indicate that <strong>{assessment?.orgwide_info?.org_name || user?.organization_name}</strong> has achieved an overall Organisation-wide AI Maturity score of <strong>{summary.overall_percentage.toFixed(1)}%</strong>, placing the organisation within the <strong>{summary.overall_maturity}</strong> maturity category. This rating reflects {
                      summary.overall_maturity === 'Leading'
                        ? 'a highly mature and well-embedded AI governance capability. Oversight, ethics, risk management, transparency, and lifecycle assurance are consistently applied across the organisation. AI decisions are well-controlled, monitored, and aligned to recognised standards. This level reflects strong leadership commitment and positions the organisation as a benchmark for responsible AI practice.'
                        : summary.overall_maturity === 'Established'
                        ? 'a well-developed and consistently applied AI governance framework. Most domains show strong performance, with clear roles, oversight, and documented processes. Some variability or manual effort remains, but overall governance is stable and repeatable. Strengthening lifecycle assurance, fairness safeguards, and organisation-wide alignment will support progress toward leading maturity.'
                        : summary.overall_maturity === 'Developing'
                        ? 'emerging and partially consistent AI governance across the organisation. Foundational structures exist but are not yet fully integrated or uniformly adopted. Oversight, transparency, fairness, and continuous monitoring vary across teams. Priorities include formalising governance, strengthening coordination, improving risk and ethical oversight, and embedding systematic lifecycle processes to advance maturity.'
                        : 'early-stage or inconsistent AI governance practices. Key policies, roles, risk controls, and oversight mechanisms are limited or undeveloped. AI maturity varies significantly across teams, and core safeguards are often missing. Establishing baseline governance structures, defining responsibilities, and building organisational awareness are essential next steps for improving responsible AI maturity.'
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
            
            {/* Last 20% - Action Buttons */}
            <div className="flex flex-col" style={{ width: '20%', gap: '3px' }}>
              {/* Button 1 - Detailed Report with Reports label */}
              <div className="flex items-center gap-2">
                <div className="text-[10px] font-semibold text-gray-500 uppercase tracking-wider whitespace-nowrap" style={{ width: '55px' }}>
                  Reports:
                </div>
                <Button 
                  onClick={generateReport}
                  disabled={generatingReport}
                  className="flex-1 bg-blue-600 hover:bg-blue-700 text-[10px] px-1.5 py-1.5 h-auto"
                  data-testid="generate-report-btn"
                >
                  {generatingReport ? (
                    <div className="flex items-center justify-center space-x-1">
                      <div className="loading-spinner w-2 h-2"></div>
                    </div>
                  ) : (
                    <div className="flex items-center justify-center space-x-1">
                      <Download className="h-3 w-3" />
                      <span>Detailed Report (DOCX)</span>
                    </div>
                  )}
                </Button>
              </div>

              {/* Button 2 - Executive Summary */}
              <div className="flex items-center gap-2">
                <div className="text-[10px] font-semibold text-gray-500 uppercase tracking-wider whitespace-nowrap invisible" style={{ width: '55px' }}>
                  Spacer:
                </div>
                <Button 
                  onClick={generateExecutiveSummaryPDF}
                  disabled={generatingPDF}
                  className="flex-1 bg-blue-600 hover:bg-blue-700 text-[10px] px-1.5 py-1.5 h-auto"
                  data-testid="generate-pdf-btn"
                >
                  {generatingPDF ? (
                    <div className="flex items-center justify-center space-x-1">
                      <div className="loading-spinner w-2 h-2"></div>
                    </div>
                  ) : (
                    <div className="flex items-center justify-center space-x-1">
                      <FileText className="h-3 w-3" />
                      <span>Results Summary Report (PDF)</span>
                    </div>
                  )}
                </Button>
              </div>

              {/* Button 3 - Framework Coverage & Evidence Register with Insights label */}
              <div className="flex items-center gap-2">
                <div className="text-[10px] font-semibold text-gray-500 uppercase tracking-wider whitespace-nowrap" style={{ width: '55px' }}>
                  Insights:
                </div>
                <div className="flex-1 flex gap-1">
                  <div 
                    className="flex-1"
                    title={assessmentType !== 'System' ? 'Available for AI System Maturity Assessments only.' : ''}
                  >
                    <Button 
                      onClick={() => assessmentType === 'System' && navigate(`/framework-coverage/${id}`)}
                      className={`w-full text-[10px] px-1 py-1.5 h-auto ${
                        assessmentType === 'System' 
                          ? 'bg-green-600 hover:bg-green-700' 
                          : 'bg-gray-400 cursor-not-allowed opacity-60'
                      }`}
                      disabled={assessmentType !== 'System'}
                      data-testid="framework-coverage-btn"
                    >
                      <div className="flex items-center justify-center space-x-0.5">
                        <Grid3X3 className="h-3 w-3" />
                        <span>Framework Coverage</span>
                      </div>
                    </Button>
                  </div>
                  <div 
                    className="flex-1"
                    title={assessmentType !== 'System' ? 'Available for AI System Maturity Assessments only.' : ''}
                  >
                    <Button 
                      onClick={() => assessmentType === 'System' && navigate(`/evidence-register/${id}`)}
                      className={`w-full text-[10px] px-1 py-1.5 h-auto ${
                        assessmentType === 'System' 
                          ? 'bg-green-600 hover:bg-green-700' 
                          : 'bg-gray-400 cursor-not-allowed opacity-60'
                      }`}
                      disabled={assessmentType !== 'System'}
                      data-testid="evidence-register-btn"
                    >
                      <div className="flex items-center justify-center space-x-0.5">
                        <FileText className="h-3 w-3" />
                        <span>Evidence Register</span>
                      </div>
                    </Button>
                  </div>
                </div>
              </div>

              {/* Button 4 - Request Consultation with Actions label */}
              <div className="flex items-center gap-2">
                <div className="text-[10px] font-semibold text-gray-500 uppercase tracking-wider whitespace-nowrap" style={{ width: '55px' }}>
                  Actions:
                </div>
                <Button 
                  variant="outline"
                  className="flex-1 text-[10px] px-1.5 py-1.5 h-auto bg-white"
                  data-testid="request-consultation-btn"
                  onClick={() => window.open('https://vciso.one/contact', '_blank')}
                >
                  <div className="flex items-center justify-center space-x-1">
                    <MessageSquare className="h-3 w-3" />
                    <span>Request Consultation</span>
                  </div>
                </Button>
              </div>
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
                : assessmentType === 'Orgwide' ? 'text-purple-600'
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
                    <div className="flex items-center">
                      <div 
                        className="px-1 py-0.5 rounded text-xs font-bold"
                        style={{ backgroundColor: colors.bg, color: colors.text }}
                      >
                        {domain.percentage.toFixed(1)}%
                      </div>
                      <span className="font-medium text-gray-900 text-xs ml-[15px]">{domain.domain_name}</span>
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

            {/* How To Read These Results - For Awareness assessments */}
            {assessmentType === 'Awareness' && (
              <div className="mt-6">
                <h2 className="text-base font-bold text-gray-900 mb-3 flex items-center space-x-2">
                  <svg className="h-4 w-4 text-green-600" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
                    <path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <span>How To Read These Results</span>
                </h2>
                <ul className="space-y-2 text-xs text-gray-700">
                  <li className="flex items-start space-x-2">
                    <span className="text-green-600 mt-0.5">•</span>
                    <span>Scores reflect your organisation's <strong>current level of AI awareness</strong>, not readiness to deploy AI or compliance with standards.</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-green-600 mt-0.5">•</span>
                    <span>Differences in maturity across domains are <strong>normal at this stage</strong> and do not indicate risk or failure.</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-green-600 mt-0.5">•</span>
                    <span>Focus first on the <strong>Priority Improvement Areas</strong> and <strong>Top Action Steps</strong>, rather than the overall score.</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-green-600 mt-0.5">•</span>
                    <span>Recommended next steps are intended to <strong>build understanding and confidence</strong> before progressing to more detailed assessments or activities.</span>
                  </li>
                </ul>
              </div>
            )}

            {/* How To Read These Results - For Readiness assessments */}
            {assessmentType === 'Readiness' && (
              <div className="mt-6">
                <h2 className="text-base font-bold text-gray-900 mb-3 flex items-center space-x-2">
                  <svg className="h-4 w-4 text-blue-600" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
                    <path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <span>How To Read These Results</span>
                </h2>
                <ul className="space-y-2 text-xs text-gray-700">
                  <li className="flex items-start space-x-2">
                    <span className="text-blue-600 mt-0.5">•</span>
                    <span>Scores reflect your organisation's <strong>readiness to support and govern AI initiatives</strong>, not formal compliance or system-level assurance.</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-blue-600 mt-0.5">•</span>
                    <span>Gaps identified at this stage may <strong>delay implementation or increase risk</strong> if AI initiatives proceed without remediation.</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-blue-600 mt-0.5">•</span>
                    <span>Priority Improvement Areas highlight <strong>foundational governance, data, and capability issues</strong> that should be addressed before scaling AI use cases.</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-blue-600 mt-0.5">•</span>
                    <span>Progression to system-level assessments is recommended <strong>only once readiness foundations are consistently in place</strong>.</span>
                  </li>
                </ul>
              </div>
            )}

            {/* How To Read These Results - For Orgwide assessments */}
            {assessmentType === 'Orgwide' && (
              <div className="mt-6">
                <h2 className="text-base font-bold text-gray-900 mb-3 flex items-center space-x-2">
                  <svg className="h-4 w-4 text-purple-600" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
                    <path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <span>How To Read These Results</span>
                </h2>
                <ul className="space-y-2 text-xs text-gray-700">
                  <li className="flex items-start space-x-2">
                    <span className="text-purple-600 mt-0.5">•</span>
                    <span>Scores reflect the <strong>consistency</strong> and <strong>maturity</strong> of AI governance practices across the organisation, not certification, regulatory compliance, or system-level assurance.</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-purple-600 mt-0.5">•</span>
                    <span>Variation across domains indicates <strong>uneven adoption, integration, or enforcement of governance controls</strong>, which may introduce organisational risk if not addressed.</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-purple-600 mt-0.5">•</span>
                    <span>Priority Improvement Areas highlight governance domains that require <strong>formalisation, coordination, executive oversight, or clearer accountability</strong>.</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-purple-600 mt-0.5">•</span>
                    <span>Progression to system-level assurance or regulatory alignment should occur only where organisational governance foundations are demonstrably mature and consistently applied.</span>
                  </li>
                </ul>
              </div>
            )}

            {/* How To Read These Results - For System assessments */}
            {assessmentType === 'System' && (
              <div className="mt-6">
                <h2 className="text-base font-bold text-gray-900 mb-3 flex items-center space-x-2">
                  <svg className="h-4 w-4 text-teal-600" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
                    <path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <span>How To Read These Results</span>
                </h2>
                <ul className="space-y-2 text-xs text-gray-700">
                  <li className="flex items-start space-x-2">
                    <span className="text-teal-600 mt-0.5">•</span>
                    <span>Scores reflect the governance, control maturity, and operational assurance of this specific AI system, based on documented practices and supporting evidence.</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-teal-600 mt-0.5">•</span>
                    <span>Results do <strong>not</strong> constitute <strong>certification, regulatory approval, or a guarantee of compliance</strong>, and should be interpreted in the context of applicable laws, regulations, and organisational obligations.</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-teal-600 mt-0.5">•</span>
                    <span>Priority Improvement Areas identify <strong>system-level controls that require strengthening, automation, or closer oversight</strong> to reduce operational, ethical, or regulatory risk.</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-teal-600 mt-0.5">•</span>
                    <span>Framework coverage and linked evidence are provided to <strong>support assurance activities, internal review, and regulatory alignment</strong>, where appropriate, but final accountability remains with the organisation.</span>
                  </li>
                </ul>
              </div>
            )}
          </div>
        </div>

        {/* Center Panel - Assessment Heatmap / Domain Benchmarks - 50% width */}
        <div className="w-1/2 bg-white border-r overflow-y-auto">
          <div className="p-4">
            <div className={viewMode === 'radar' ? '-mb-6' : 'mb-4'}>
              <div className="flex items-start justify-between">
                <div>
                  <h2 className="text-lg font-bold text-gray-900 flex items-center space-x-2">
                    <BarChart3 className={`h-5 w-5 ${
                      assessmentType === 'Awareness' ? 'text-green-600'
                      : assessmentType === 'Readiness' ? 'text-blue-600'
                      : assessmentType === 'Orgwide' ? 'text-purple-600'
                      : 'text-teal-600'
                    }`} />
                    <span>
                      {viewMode === 'heatmap' 
                        ? 'Assessment Response Heatmap' 
                        : assessmentType === 'Awareness'
                        ? 'AI Awareness vs Sector Benchmark'
                        : assessmentType === 'Readiness'
                        ? 'AI Readiness vs Sector Benchmark'
                        : 'AI System Domain Maturity vs Sector Benchmark'}
                    </span>
                    {/* Info tooltip for Awareness heatmap legend */}
                    {viewMode === 'heatmap' && assessmentType === 'Awareness' && (
                      <div className="relative inline-block ml-2 group">
                        <button
                          type="button"
                          aria-label="Heatmap legend"
                          className="inline-flex items-center justify-center h-5 w-5 rounded-full bg-blue-600 text-white opacity-80 hover:opacity-100 transition-opacity focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2"
                        >
                          <svg viewBox="0 0 24 24" aria-hidden="true" className="h-3.5 w-3.5">
                            <path fill="currentColor" d="M11 10h2v8h-2v-8zm0-4h2v2h-2V6z" />
                          </svg>
                        </button>
                        <div className="absolute left-0 top-6 z-50 hidden group-hover:block w-64 bg-white border border-gray-200 rounded-lg shadow-lg p-3">
                          <p className="text-xs font-semibold text-gray-700 mb-2">Heatmap Legend:</p>
                          <div className="space-y-1.5">
                            <div className="flex items-center space-x-2">
                              <div className="w-4 h-4 rounded" style={{ backgroundColor: '#00B050' }}></div>
                              <span className="text-xs font-normal text-gray-600">Ready to Progress (4/4)</span>
                            </div>
                            <div className="flex items-center space-x-2">
                              <div className="w-4 h-4 rounded" style={{ backgroundColor: '#FFFF00' }}></div>
                              <span className="text-xs font-normal text-gray-600">Building Readiness (3/4)</span>
                            </div>
                            <div className="flex items-center space-x-2">
                              <div className="w-4 h-4 rounded" style={{ backgroundColor: '#FFC000' }}></div>
                              <span className="text-xs font-normal text-gray-600">Exploring Opportunities (2/4)</span>
                            </div>
                            <div className="flex items-center space-x-2">
                              <div className="w-4 h-4 rounded" style={{ backgroundColor: '#FF0000' }}></div>
                              <span className="text-xs font-normal text-gray-600">Early Awareness (1/4)</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}
                    {/* Info tooltip for Readiness heatmap legend */}
                    {viewMode === 'heatmap' && assessmentType === 'Readiness' && (
                      <div className="relative inline-block ml-2 group">
                        <button
                          type="button"
                          aria-label="Heatmap legend"
                          className="inline-flex items-center justify-center h-5 w-5 rounded-full bg-blue-600 text-white opacity-80 hover:opacity-100 transition-opacity focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2"
                        >
                          <svg viewBox="0 0 24 24" aria-hidden="true" className="h-3.5 w-3.5">
                            <path fill="currentColor" d="M11 10h2v8h-2v-8zm0-4h2v2h-2V6z" />
                          </svg>
                        </button>
                        <div className="absolute left-0 top-6 z-50 hidden group-hover:block w-64 bg-white border border-gray-200 rounded-lg shadow-lg p-3">
                          <p className="text-xs font-semibold text-gray-700 mb-2">Heatmap Legend:</p>
                          <div className="space-y-1.5">
                            <div className="flex items-center space-x-2">
                              <div className="w-4 h-4 rounded" style={{ backgroundColor: '#00B050' }}></div>
                              <span className="text-xs font-normal text-gray-600">AI-Ready (4/4)</span>
                            </div>
                            <div className="flex items-center space-x-2">
                              <div className="w-4 h-4 rounded" style={{ backgroundColor: '#FFFF00' }}></div>
                              <span className="text-xs font-normal text-gray-600">Operational Readiness (3/4)</span>
                            </div>
                            <div className="flex items-center space-x-2">
                              <div className="w-4 h-4 rounded" style={{ backgroundColor: '#FFC000' }}></div>
                              <span className="text-xs font-normal text-gray-600">Emerging Capability (2/4)</span>
                            </div>
                            <div className="flex items-center space-x-2">
                              <div className="w-4 h-4 rounded" style={{ backgroundColor: '#FF0000' }}></div>
                              <span className="text-xs font-normal text-gray-600">Limited Foundations (1/4)</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}
                    {/* Info tooltip for Orgwide heatmap legend */}
                    {viewMode === 'heatmap' && assessmentType === 'Orgwide' && (
                      <div className="relative inline-block ml-2 group">
                        <button
                          type="button"
                          aria-label="Heatmap legend"
                          className="inline-flex items-center justify-center h-5 w-5 rounded-full bg-blue-600 text-white opacity-80 hover:opacity-100 transition-opacity focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2"
                        >
                          <svg viewBox="0 0 24 24" aria-hidden="true" className="h-3.5 w-3.5">
                            <path fill="currentColor" d="M11 10h2v8h-2v-8zm0-4h2v2h-2V6z" />
                          </svg>
                        </button>
                        <div className="absolute left-0 top-6 z-50 hidden group-hover:block w-64 bg-white border border-gray-200 rounded-lg shadow-lg p-3">
                          <p className="text-xs font-semibold text-gray-700 mb-2">Heatmap Legend:</p>
                          <div className="space-y-1.5">
                            <div className="flex items-center space-x-2">
                              <div className="w-4 h-4 rounded" style={{ backgroundColor: '#00B050' }}></div>
                              <span className="text-xs font-normal text-gray-600">Optimised Excellence (4/4)</span>
                            </div>
                            <div className="flex items-center space-x-2">
                              <div className="w-4 h-4 rounded" style={{ backgroundColor: '#FFFF00' }}></div>
                              <span className="text-xs font-normal text-gray-600">Integrated Governance (3/4)</span>
                            </div>
                            <div className="flex items-center space-x-2">
                              <div className="w-4 h-4 rounded" style={{ backgroundColor: '#FFC000' }}></div>
                              <span className="text-xs font-normal text-gray-600">Emerging Structure (2/4)</span>
                            </div>
                            <div className="flex items-center space-x-2">
                              <div className="w-4 h-4 rounded" style={{ backgroundColor: '#FF0000' }}></div>
                              <span className="text-xs font-normal text-gray-600">Ad-hoc Beginnings (1/4)</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}
                    {/* Info tooltip for System heatmap legend */}
                    {viewMode === 'heatmap' && assessmentType === 'System' && (
                      <div className="relative inline-block ml-2 group">
                        <button
                          type="button"
                          aria-label="Heatmap legend"
                          className="inline-flex items-center justify-center h-5 w-5 rounded-full bg-blue-600 text-white opacity-80 hover:opacity-100 transition-opacity focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2"
                        >
                          <svg viewBox="0 0 24 24" aria-hidden="true" className="h-3.5 w-3.5">
                            <path fill="currentColor" d="M11 10h2v8h-2v-8zm0-4h2v2h-2V6z" />
                          </svg>
                        </button>
                        <div className="absolute left-0 top-6 z-50 hidden group-hover:block w-64 bg-white border border-gray-200 rounded-lg shadow-lg p-3">
                          <p className="text-xs font-semibold text-gray-700 mb-2">Heatmap Legend:</p>
                          <div className="space-y-1.5">
                            <div className="flex items-center space-x-2">
                              <div className="w-4 h-4 rounded" style={{ backgroundColor: '#00B050' }}></div>
                              <span className="text-xs font-normal text-gray-600">Optimised Excellence (4/4)</span>
                            </div>
                            <div className="flex items-center space-x-2">
                              <div className="w-4 h-4 rounded" style={{ backgroundColor: '#FFFF00' }}></div>
                              <span className="text-xs font-normal text-gray-600">Integrated Governance (3/4)</span>
                            </div>
                            <div className="flex items-center space-x-2">
                              <div className="w-4 h-4 rounded" style={{ backgroundColor: '#FFC000' }}></div>
                              <span className="text-xs font-normal text-gray-600">Emerging Structure (2/4)</span>
                            </div>
                            <div className="flex items-center space-x-2">
                              <div className="w-4 h-4 rounded" style={{ backgroundColor: '#FF0000' }}></div>
                              <span className="text-xs font-normal text-gray-600">Ad-hoc Beginnings (1/4)</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}
                    {/* Info tooltip for Sector Benchmark */}
                    {viewMode === 'radar' && (
                      <div className="relative inline-block ml-2 group">
                        <button
                          type="button"
                          aria-label="Benchmark information"
                          className="inline-flex items-center justify-center h-5 w-5 rounded-full bg-blue-600 text-white opacity-80 hover:opacity-100 transition-opacity focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2"
                        >
                          <svg viewBox="0 0 24 24" aria-hidden="true" className="h-3.5 w-3.5">
                            <path fill="currentColor" d="M11 10h2v8h-2v-8zm0-4h2v2h-2V6z" />
                          </svg>
                        </button>
                        <div className="absolute left-0 top-6 z-50 hidden group-hover:block w-72 bg-white border border-gray-200 rounded-lg shadow-lg p-3">
                          <p className="text-xs font-normal text-gray-600">Benchmarks are indicative only and based on aggregated, anonymised assessment data.</p>
                        </div>
                      </div>
                    )}
                  </h2>
                  {/* Subtitle for Assessment Heatmap view */}
                  {viewMode === 'heatmap' && (
                    <p className="text-[12px] text-gray-600 mt-1 ml-7">
                      Visualisation of responses across all domains and questions, highlighting strengths and improvement opportunities.
                    </p>
                  )}
                  {/* Subtitle for Domain Benchmarks view */}
                  {viewMode === 'radar' && (
                    <div className="text-[12px] text-gray-600 mt-1 ml-7">
                      <p>Comparing your AI domain {assessmentType === 'Awareness' ? 'awareness' : assessmentType === 'Readiness' ? 'readiness' : 'maturity'} against the <span className="font-bold">{benchmarkSector || assessment?.system_info?.industry || assessment?.awareness_info?.industry || assessment?.readiness_info?.industry || user?.industry || 'sector'}</span> sector average.</p>
                      <p className="mt-0.5">This comparison highlights relative strengths and gaps — <span className="font-bold">not</span> a target score.</p>
                    </div>
                  )}
                </div>
                
                {/* Radio buttons - show for System, Awareness, and Readiness assessments */}
                {(assessmentType === 'System' || assessmentType === 'Awareness' || assessmentType === 'Readiness') && (
                  <div className="flex items-center space-x-4 mt-0.5">
                    <label className="flex items-center cursor-pointer">
                      <input
                        type="radio"
                        name="viewMode"
                        value="heatmap"
                        checked={viewMode === 'heatmap'}
                        onChange={(e) => setViewMode(e.target.value)}
                        className="mr-2 h-4 w-4 text-teal-600 focus:ring-teal-500"
                      />
                      <span className="text-[12px] font-medium text-gray-700">Assessment Heatmap</span>
                    </label>
                    <label className="flex items-center cursor-pointer">
                      <input
                        type="radio"
                        name="viewMode"
                        value="radar"
                        checked={viewMode === 'radar'}
                        onChange={(e) => setViewMode(e.target.value)}
                        className="mr-2 h-4 w-4 text-teal-600 focus:ring-teal-500"
                      />
                      <span className="text-[12px] font-medium text-gray-700">Sector Benchmarks</span>
                    </label>
                  </div>
                )}
              </div>
            </div>
            
            {/* Conditional rendering based on viewMode */}
            {viewMode === 'heatmap' ? (
              <div className="space-y-1 mt-4" data-testid="assessment-heatmap">
                {[...summary.domain_scores]
                .sort((a, b) => a.percentage - b.percentage) // Sort by percentage, lowest first
                .map((domain) => {
                const domainQuestions = questions.filter(q => q.domain_id === domain.domain_id);
                const domainAnswers = answers.filter(a => 
                  domainQuestions.some(q => q.id === a.question_id)
                );
                
                return (
                  <div key={domain.domain_id} className="flex items-center">
                    {/* Domain name on the left */}
                    <div 
                      className="flex-shrink-0 pr-4" 
                      style={{ 
                        width: assessmentType === 'Awareness' ? '16rem' 
                             : assessmentType === 'Readiness' ? '18rem'
                             : assessmentType === 'Orgwide' ? '14rem' 
                             : '8rem' 
                      }}
                    >
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
            ) : (
              /* Radar Chart - Domain Benchmarks */
              <div className="h-[750px] flex items-center justify-center" style={{ width: '100%', marginTop: '-120px', paddingTop: '140px' }} data-testid="domain-benchmarks">
                {showIndustrySelector ? (
                  <div className="flex items-center justify-center h-full">
                    <div className="text-center max-w-md">
                      <h3 className="text-lg font-semibold text-gray-900 mb-4">Select Your Industry</h3>
                      <p className="text-sm text-gray-600 mb-4">
                        To view sector benchmark comparisons, please select your organization's industry.
                      </p>
                      <select
                        className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                        value={selectedIndustry}
                        onChange={(e) => setSelectedIndustry(e.target.value)}
                      >
                        <option value="">-- Select Industry --</option>
                        {INDUSTRIES.map((industry) => (
                          <option key={industry} value={industry}>
                            {industry}
                          </option>
                        ))}
                      </select>
                    </div>
                  </div>
                ) : benchmarks ? (
                  <DomainBenchmarkRadar
                    domainScores={summary.domain_scores}
                    benchmarks={benchmarks}
                    sector={benchmarkSector || selectedIndustry || user?.industry || 'Unknown'}
                    assessmentType={assessmentType}
                  />
                ) : (
                  <div className="flex items-center justify-center h-full">
                    <div className="text-center">
                      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-teal-600 mx-auto mb-4"></div>
                      <p className="text-gray-600">Loading sector benchmarks...</p>
                    </div>
                  </div>
                )}
              </div>
            )}
            
            {/* Assessment Results Commentary - Only for Awareness assessments */}
            {console.log('Assessment Type:', assessmentType, 'Has recommendation?', summary?.recommendation_summary)}
            {assessmentType === 'Awareness' && summary?.recommendation_summary && (
              <>
                {/* Parse the recommendation_summary to separate commentary from next recommended assessment */}
                {(() => {
                  const fullText = summary.recommendation_summary;
                  // Match both old format "Recommended Next Step" and new format "Next Recommended Assessment"
                  const splitRegex = /\*\*(Recommended Next Step|Next Recommended Assessment):\*\*/i;
                  const parts = fullText.split(splitRegex);
                  const commentary = parts[0]?.trim() || '';
                  const nextAssessment = parts[2]?.trim() || '';
                  
                  return (
                    <>
                      {/* Commentary Card */}
                      {commentary && (
                        <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                          <h3 className="text-base font-bold text-gray-900 mb-3 flex items-center space-x-2">
                            <svg className="h-5 w-5 text-blue-600" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
                              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                            <span>Assessment Results Commentary</span>
                          </h3>
                          <div 
                            className={`text-sm text-gray-700 whitespace-pre-line overflow-hidden transition-all duration-300 ${
                              commentaryExpanded ? '' : 'line-clamp-3'
                            }`}
                            style={!commentaryExpanded ? { display: '-webkit-box', WebkitLineClamp: 3, WebkitBoxOrient: 'vertical' } : {}}
                            dangerouslySetInnerHTML={{
                              __html: commentary
                                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                                .replace(/\n/g, '<br />')
                            }}
                          />
                          <button
                            onClick={() => setCommentaryExpanded(!commentaryExpanded)}
                            className="mt-2 text-sm font-medium text-blue-600 hover:text-blue-800 flex items-center space-x-1 transition-colors"
                          >
                            <span>{commentaryExpanded ? 'Collapse commentary' : 'Expand commentary'}</span>
                            <svg 
                              className={`h-4 w-4 transition-transform duration-200 ${commentaryExpanded ? 'rotate-180' : ''}`} 
                              fill="none" 
                              strokeLinecap="round" 
                              strokeLinejoin="round" 
                              strokeWidth="2" 
                              viewBox="0 0 24 24" 
                              stroke="currentColor"
                            >
                              <path d="M19 9l-7 7-7-7"></path>
                            </svg>
                          </button>
                        </div>
                      )}
                      
                      {/* Next Recommended Assessment Card */}
                      {nextAssessment && (
                        <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
                          <h3 className="text-base font-bold text-gray-900 mb-3 flex items-center space-x-2">
                            <svg className="h-5 w-5 text-green-600" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
                              <path d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
                            </svg>
                            <span>Next Recommended Steps</span>
                          </h3>
                          <div 
                            className="text-sm text-gray-700"
                            dangerouslySetInnerHTML={{
                              __html: nextAssessment
                                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                                .replace(/\n/g, '<br />')
                            }}
                          />
                        </div>
                      )}
                    </>
                  );
                })()}
              </>
            )}
          </div>
        </div>

        {/* Right Panel - 25% width */}
        <div className="w-1/4 bg-white overflow-y-auto">
          <div className="p-4">
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

            {/* Top 3 Action Steps - Only for Awareness assessments */}
            {assessmentType === 'Awareness' && actionSteps && (
              <div className="mt-4">
                <div className="mb-2">
                  <h2 className="text-base font-bold text-gray-900 flex items-center space-x-2 mb-1">
                    <CheckCircle2 className="h-4 w-4 text-blue-600" />
                    <span>Top 3 Action Steps</span>
                  </h2>
                  <p className="text-xs text-gray-600 ml-6">
                    Practical actions to strengthen AI awareness before progressing further.
                  </p>
                </div>
                <div className="space-y-2">
                  {(() => {
                    // Get the 3 lowest scoring questions
                    const lowestScoringQuestions = [...answers]
                      .sort((a, b) => a.numeric_score - b.numeric_score)
                      .slice(0, 3);
                    
                    return lowestScoringQuestions.map((answer, index) => {
                      const question = questions.find(q => q.id === answer.question_id);
                      const questionCode = question?.code;
                      const actionStep = actionSteps[questionCode];
                      
                      if (!actionStep) return null;
                      
                      return (
                        <div key={answer.question_id} className="p-3 bg-blue-50 rounded border border-blue-200">
                          <div className="flex items-start space-x-2">
                            <div className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-600 text-white flex items-center justify-center text-xs font-bold mt-0.5">
                              {index + 1}
                            </div>
                            <div className="flex-1">
                              <div className="text-xs font-semibold text-gray-900 mb-1">
                                {questionCode}: Score {answer.numeric_score}/4
                              </div>
                              <div className="text-xs text-gray-700 leading-relaxed">
                                {actionStep}
                              </div>
                            </div>
                          </div>
                        </div>
                      );
                    });
                  })()}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ResultsPage;
