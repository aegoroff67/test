import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
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
  Shield,
  Grid3X3,
  Info,
  X
} from 'lucide-react';
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer, PieChart, Pie, Cell, Legend } from 'recharts';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Color mapping for risk levels
const getRiskColor = (level) => {
  switch(level) {
    case 'Critical':
      return { bg: '#FF0000', text: '#FFFFFF' };
    case 'High':
      return { bg: '#FFC000', text: '#000000' };
    case 'Medium':
      return { bg: '#FFFF00', text: '#000000' };
    case 'Low':
      return { bg: '#00B050', text: '#FFFFFF' };
    default:
      return { bg: '#808080', text: '#FFFFFF' };
  }
};

const getRiskBadge = (level) => {
  switch (level) {
    case 'Low':
      return { color: 'bg-green-100 text-green-800', icon: CheckCircle2 };
    case 'Medium':
      return { color: 'bg-yellow-100 text-yellow-800', icon: TrendingUp };
    case 'High':
      return { color: 'bg-orange-100 text-orange-800', icon: AlertTriangle };
    case 'Critical':
      return { color: 'bg-red-100 text-red-800', icon: AlertTriangle };
    default:
      return { color: 'bg-gray-100 text-gray-800', icon: BarChart3 };
  }
};

function FairaResultsPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [assessment, setAssessment] = useState(null);
  const [fairaData, setFairaData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [generatingPDF, setGeneratingPDF] = useState(false);
  const [generatingReport, setGeneratingReport] = useState(false);
  
  // Radar chart data from API
  const [radarChartData, setRadarChartData] = useState(null);

  // Risk summary data from API  
  const [riskSummary, setRiskSummary] = useState({
    overall_risk_level: 'Medium',
    overall_risk_score: 0,
    risk_category: 'Calculating...',
    section_scores: [],
    top_risk_areas: []
  });

  // The 8 FAIRA Part B domains with short labels for radar chart display
  const fairadomains = [
    { id: 'B1', shortLabel: 'Wellbeing', fullName: 'Human, Societal and Environmental Wellbeing' },
    { id: 'B2', shortLabel: 'Human', fullName: 'Human-Centred Values' },
    { id: 'B3', shortLabel: 'Fairness', fullName: 'Fairness' },
    { id: 'B4', shortLabel: 'Privacy', fullName: 'Privacy Protection and Security' },
    { id: 'B5', shortLabel: 'Reliability', fullName: 'Reliability and Safety' },
    { id: 'B6', shortLabel: 'Transparency', fullName: 'Transparency and Explainability' },
    { id: 'B7', shortLabel: 'Contestability', fullName: 'Contestability' },
    { id: 'B8', shortLabel: 'Accountability', fullName: 'Accountability' }
  ];

  // Default placeholder data (used while loading or if API fails)
  const getDefaultChartData = () => fairadomains.map(domain => ({
    domain: domain.shortLabel,
    fullName: domain.fullName,
    score: 0,
    fullMark: 100
  }));

  // Get radar chart data from API response or use defaults
  const domainImpactData = radarChartData?.domainImpact || getDefaultChartData();
  const domainLikelihoodData = radarChartData?.domainLikelihood || getDefaultChartData();
  const domainControlEffectivenessData = radarChartData?.domainControlEffectiveness || getDefaultChartData();
  const domainRiskData = radarChartData?.domainRisk || getDefaultChartData();

  // Chart configurations for the 4 radar charts
  const radarCharts = [
    {
      id: 'impact',
      title: 'Domain Impact',
      data: domainImpactData,
      color: '#ef4444', // Red
      formula: 'Domain_Impact = Σ(Domain Impact modifiers)',
      description: 'How serious the consequences would be in each domain if the AI system went wrong.'
    },
    {
      id: 'likelihood',
      title: 'Domain Likelihood',
      data: domainLikelihoodData,
      color: '#f97316', // Orange
      formula: 'Domain_Likelihood = Σ(Domain Likelihood modifiers)',
      description: 'How likely problems are to occur in each domain based on how the AI is built and used.'
    },
    {
      id: 'control',
      title: 'Domain Control Effectiveness',
      data: domainControlEffectivenessData,
      color: '#22c55e', // Green
      formula: 'Domain_CE(D) = Baseline_Domain_CE + Σ(Domain CE modifiers)',
      description: 'How strong the safeguards and oversight are to manage risks in each domain.'
    },
    {
      id: 'risk',
      title: 'Domain Risk',
      data: domainRiskData,
      color: '#8b5cf6', // Purple
      formula: 'Domain_Risk = (Domain_Impact × Domain_Likelihood) ÷ Domain_CE',
      description: 'The overall level of risk remaining in each domain after safeguards are taken into account.'
    }
  ];

  // State for info modal
  const [activeInfoModal, setActiveInfoModal] = useState(null);

  // Calculate response distribution from risk summary
  const responseDistribution = React.useMemo(() => {
    if (!riskSummary?.domain_scores) {
      return [
        { name: 'Low Risk', value: 25, color: '#00B050' },
        { name: 'Medium Risk', value: 25, color: '#FFFF00' },
        { name: 'High Risk', value: 25, color: '#FFC000' },
        { name: 'Critical Risk', value: 25, color: '#FF0000' }
      ];
    }
    
    let low = 0, medium = 0, high = 0, critical = 0;
    const domains = Object.values(riskSummary.domain_scores);
    
    domains.forEach(d => {
      const risk = d.Risk || 0;
      if (risk >= 75) critical++;
      else if (risk >= 50) high++;
      else if (risk >= 25) medium++;
      else low++;
    });
    
    const total = domains.length || 1;
    return [
      { name: 'Low Risk', value: Math.round((low / total) * 100), color: '#00B050' },
      { name: 'Medium Risk', value: Math.round((medium / total) * 100), color: '#FFFF00' },
      { name: 'High Risk', value: Math.round((high / total) * 100), color: '#FFC000' },
      { name: 'Critical Risk', value: Math.round((critical / total) * 100), color: '#FF0000' }
    ];
  }, [riskSummary]);

  useEffect(() => {
    fetchResults();
  }, [id]);

  const fetchResults = async () => {
    try {
      // Fetch assessment data
      const assessmentResponse = await axios.get(`${API}/assessments/${id}`);
      setAssessment(assessmentResponse.data);
      setFairaData(assessmentResponse.data.faira_form || {});
      
      // Fetch calculated scores from the scoring engine
      try {
        const scoresResponse = await axios.get(`${API}/assessments/${id}/faira-scores`);
        if (scoresResponse.data) {
          setRadarChartData(scoresResponse.data.radar_charts);
          if (scoresResponse.data.risk_summary) {
            const summary = scoresResponse.data.risk_summary;
            setRiskSummary({
              overall_risk_level: summary.overall_risk_level || 'Medium',
              overall_risk_score: summary.overall_risk_score || 0,
              risk_category: getRiskCategory(summary.overall_risk_level),
              section_scores: Object.entries(summary.domain_scores || {}).map(([name, scores]) => ({
                section_id: name,
                section_name: fairadomains.find(d => d.shortLabel === name)?.fullName || name,
                risk_score: scores.Risk || 0,
                risk_level: getRiskLevelFromScore(scores.Risk || 0)
              })),
              top_risk_areas: summary.top_risk_areas || []
            });
          }
        }
      } catch (scoreError) {
        console.warn('Could not fetch FAIRA scores:', scoreError);
        // Continue with assessment display even if scores fail
      }
      
      setLoading(false);
    } catch (error) {
      console.error('Error fetching FAIRA results:', error);
      toast.error('Failed to load assessment results');
      setLoading(false);
    }
  };
  
  const getRiskCategory = (level) => {
    switch(level) {
      case 'Critical': return 'Critical Risk Profile';
      case 'High': return 'High Risk Profile';
      case 'Medium': return 'Moderate Risk Profile';
      case 'Low': return 'Low Risk Profile';
      default: return 'Risk Profile';
    }
  };
  
  const getRiskLevelFromScore = (score) => {
    if (score >= 75) return 'Critical';
    if (score >= 50) return 'High';
    if (score >= 25) return 'Medium';
    return 'Low';
  };

  const handleGeneratePDF = async () => {
    setGeneratingPDF(true);
    try {
      // Placeholder - PDF endpoint needs backend implementation
      toast.info('PDF generation feature coming soon');
    } catch (error) {
      console.error('Error generating PDF:', error);
      toast.error('Failed to generate PDF report');
    } finally {
      setGeneratingPDF(false);
    }
  };

  const handleGenerateReport = async () => {
    setGeneratingReport(true);
    try {
      // Placeholder - Report endpoint needs backend implementation
      toast.info('Detailed report generation feature coming soon');
    } catch (error) {
      console.error('Error generating report:', error);
      toast.error('Failed to generate report');
    } finally {
      setGeneratingReport(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-teal-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading FAIRA assessment results...</p>
        </div>
      </div>
    );
  }

  if (!assessment) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center">
        <Card className="max-w-md">
          <CardContent className="pt-6">
            <p className="text-center text-gray-600">Assessment not found</p>
            <Button onClick={() => navigate('/dashboard')} className="w-full mt-4">
              Return to Dashboard
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  const badgeInfo = getRiskBadge(riskSummary.overall_risk_level);
  const BadgeIcon = badgeInfo.icon;

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex flex-col">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 shadow-sm">
        <div className="px-6 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Logo />
              <div>
                <div className="flex items-center space-x-2">
                  <h1 className="text-lg font-bold text-gray-900">FAIRA Risk Assessment Results</h1>
                  <Badge className={`${badgeInfo.color} flex items-center space-x-1`}>
                    <BadgeIcon className="h-3 w-3" />
                    <span>{riskSummary.overall_risk_level} Risk</span>
                  </Badge>
                </div>
                <p className="text-xs text-gray-600">{assessment.name}</p>
              </div>
            </div>
            <Button
              variant="outline"
              onClick={() => navigate('/dashboard')}
              className="flex items-center space-x-2"
            >
              <ArrowLeft className="h-4 w-4" />
              <span>Dashboard</span>
            </Button>
          </div>
        </div>
      </div>

      {/* Results Summary Bar */}
      <div className="bg-gradient-to-r from-orange-50 to-orange-100 border-b border-orange-200">
        <div className="px-6 py-4">
          <div className="flex items-stretch gap-6">
            {/* First 35% - Scores Display */}
            <div className="flex flex-col justify-center" style={{ width: '35%' }}>
              <div className="grid grid-cols-2 gap-4">
                <div className="text-center">
                  <p className="text-3xl font-bold text-gray-900">{riskSummary.overall_risk_score}%</p>
                  <p className="text-xs text-gray-600">Overall Risk Score</p>
                </div>
                <div className="text-center">
                  <p className="text-3xl font-bold text-gray-900">{riskSummary.section_scores.length}</p>
                  <p className="text-xs text-gray-600">Sections Analyzed</p>
                </div>
              </div>
            </div>

            {/* Middle 50% - Summary Text */}
            <div className="px-6" style={{ width: '50%' }}>
              <p className="text-sm font-bold text-gray-900 mb-2 mt-0">Risk Assessment Summary</p>
              <p className="text-xs text-gray-700 leading-relaxed">
                The FAIRA assessment indicates that <strong>{fairaData.ai_system_name || 'this AI system'}</strong> presents an overall risk level of <strong>{riskSummary.overall_risk_level}</strong> with a risk score of <strong>{riskSummary.overall_risk_score}%</strong>. This classification reflects a <strong>{riskSummary.risk_category.toLowerCase()}</strong> across regulatory compliance, data governance, fairness considerations, and accountability measures. Key areas requiring attention include <strong>{riskSummary.top_risk_areas[0].name}</strong>, <strong>{riskSummary.top_risk_areas[1].name}</strong>, and <strong>{riskSummary.top_risk_areas[2].name}</strong>. Targeted risk mitigation strategies should focus on strengthening controls in high-risk sections while maintaining established safeguards in lower-risk areas.
              </p>
            </div>
            
            {/* Last 15% - Action Buttons */}
            <div className="flex flex-col" style={{ width: '15%', gap: '3px' }}>
              {/* Button 1 - Detailed Report */}
              <div className="flex items-center gap-2">
                <div className="text-[10px] font-semibold text-gray-500 uppercase tracking-wider whitespace-nowrap" style={{ width: '55px' }}>
                  Exports:
                </div>
                <Button 
                  onClick={handleGenerateReport}
                  disabled={generatingReport}
                  className="flex-1 bg-blue-600 hover:bg-blue-700 text-[10px] px-1.5 py-1.5 h-auto"
                >
                  {generatingReport ? (
                    <div className="flex items-center justify-center space-x-1">
                      <div className="loading-spinner w-2 h-2"></div>
                    </div>
                  ) : (
                    <div className="flex items-center justify-center space-x-1">
                      <Download className="h-3 w-3" />
                      <span>Detailed Report</span>
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
                  onClick={handleGeneratePDF}
                  disabled={generatingPDF}
                  className="flex-1 bg-blue-600 hover:bg-blue-700 text-[10px] px-1.5 py-1.5 h-auto"
                >
                  {generatingPDF ? (
                    <div className="flex items-center justify-center space-x-1">
                      <div className="loading-spinner w-2 h-2"></div>
                    </div>
                  ) : (
                    <div className="flex items-center justify-center space-x-1">
                      <FileText className="h-3 w-3" />
                      <span>Executive Summary</span>
                    </div>
                  )}
                </Button>
              </div>

              {/* Button 3 - Framework Insights */}
              <div className="flex items-center gap-2">
                <div className="text-[10px] font-semibold text-gray-500 uppercase tracking-wider whitespace-nowrap" style={{ width: '55px' }}>
                  Insights:
                </div>
                <Button 
                  onClick={() => toast.info('Framework insights coming soon')}
                  className="flex-1 bg-green-600 hover:bg-green-700 text-[10px] px-1.5 py-1.5 h-auto"
                >
                  <div className="flex items-center justify-center space-x-1">
                    <Grid3X3 className="h-3 w-3" />
                    <span>Risk Matrix</span>
                  </div>
                </Button>
              </div>

              {/* Button 4 - Request Consultation */}
              <div className="flex items-center gap-2">
                <div className="text-[10px] font-semibold text-gray-500 uppercase tracking-wider whitespace-nowrap" style={{ width: '55px' }}>
                  Actions:
                </div>
                <Button 
                  variant="outline"
                  className="flex-1 text-[10px] px-1.5 py-1.5 h-auto"
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
              <Shield className="h-4 w-4 text-orange-600" />
              <span>Section Risk Scores</span>
            </h2>
            
            <div className="space-y-2">
              {[...riskSummary.section_scores]
                .sort((a, b) => b.risk_score - a.risk_score) // Sort by risk score, highest first
                .map((section) => {
                const colors = getRiskColor(section.risk_level);
                return (
                  <div key={section.section_id} className="space-y-0.5">
                    <div className="flex items-center">
                      <div 
                        className="px-1 py-0.5 rounded text-xs font-bold"
                        style={{ backgroundColor: colors.bg, color: colors.text }}
                      >
                        {section.risk_score}%
                      </div>
                      <span className="font-medium text-gray-900 text-xs ml-[15px]">{section.section_name}</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-1.5">
                      <div 
                        className="h-1.5 rounded-full transition-all duration-300"
                        style={{ width: `${section.risk_score}%`, backgroundColor: colors.bg }}
                      ></div>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Risk Distribution */}
            <div className="mt-6">
              <h2 className="text-base font-bold text-gray-900 mb-1 flex items-center space-x-2">
                <BarChart3 className="h-4 w-4 text-orange-600" />
                <span>Risk Distribution</span>
              </h2>
              <p className="text-xs text-gray-600 mb-3">Based on {riskSummary.section_scores.length} assessed sections</p>
              
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie
                    data={responseDistribution}
                    cx="50%"
                    cy="50%"
                    innerRadius={40}
                    outerRadius={80}
                    paddingAngle={2}
                    dataKey="value"
                  >
                    {responseDistribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Legend 
                    verticalAlign="bottom" 
                    height={36}
                    formatter={(value, entry) => (
                      <span className="text-xs">{value}: {entry.payload.value}%</span>
                    )}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Middle Panel - 50% width */}
        <div className="flex-1 bg-gray-50 overflow-y-auto">
          <div className="px-6 pb-6 pt-4">
            <div className="mb-6">
              <h2 className="text-lg font-bold text-gray-900 mb-4 flex items-center space-x-2">
                <Shield className="h-5 w-5 text-orange-600" />
                <span>FAIRA Risk Profile</span>
              </h2>
              
              {/* 2x2 Grid of Radar Charts */}
              <div className="grid grid-cols-2 gap-4">
                {radarCharts.map((chart) => (
                  <Card key={chart.id} className="relative">
                    {/* Info Icon */}
                    <button
                      onClick={() => setActiveInfoModal(chart.id)}
                      className="absolute top-2 left-2 z-10 p-1 rounded-full bg-blue-500 hover:bg-blue-600 transition-colors"
                      title={`${chart.title} Information`}
                    >
                      <Info className="h-3 w-3 text-white" />
                    </button>

                    <CardContent className="pt-4 pb-2">
                      <h3 className="text-sm font-semibold text-gray-900 text-center mb-2">{chart.title}</h3>
                      <ResponsiveContainer width="100%" height={180}>
                        <RadarChart data={chart.data}>
                          <PolarGrid stroke="#e5e7eb" />
                          <PolarAngleAxis 
                            dataKey="domain" 
                            tick={{ fill: '#6b7280', fontSize: 9 }}
                          />
                          <PolarRadiusAxis 
                            angle={90} 
                            domain={[0, 100]}
                            tick={{ fill: '#6b7280', fontSize: 8 }}
                            tickCount={3}
                          />
                          <Radar 
                            name={chart.title} 
                            dataKey="score" 
                            stroke={chart.color} 
                            fill={chart.color} 
                            fillOpacity={0.5}
                          />
                        </RadarChart>
                      </ResponsiveContainer>
                    </CardContent>
                  </Card>
                ))}
              </div>

              {/* Info Modal */}
              {activeInfoModal && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                  <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
                    <div className="flex items-center justify-between p-4 border-b">
                      <h3 className="text-lg font-semibold text-gray-900">
                        {radarCharts.find(c => c.id === activeInfoModal)?.title}
                      </h3>
                      <button
                        onClick={() => setActiveInfoModal(null)}
                        className="p-1 hover:bg-gray-100 rounded-full transition-colors"
                      >
                        <X className="h-5 w-5 text-gray-500" />
                      </button>
                    </div>
                    <div className="p-4">
                      <div className="mb-4">
                        <p className="text-sm font-medium text-gray-700 mb-2">Formula:</p>
                        <pre className="bg-gray-100 p-3 rounded text-sm font-mono text-gray-800 whitespace-pre-wrap">
                          {radarCharts.find(c => c.id === activeInfoModal)?.formula}
                        </pre>
                      </div>
                      <div>
                        <p className="text-sm font-medium text-gray-700 mb-2">Description:</p>
                        <p className="text-sm text-gray-600">
                          {radarCharts.find(c => c.id === activeInfoModal)?.description}
                        </p>
                      </div>
                    </div>
                    <div className="p-4 border-t bg-gray-50 rounded-b-lg">
                      <Button
                        onClick={() => setActiveInfoModal(null)}
                        className="w-full"
                      >
                        Close
                      </Button>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Top Risk Areas */}
            <div className="mb-6">
              <h2 className="text-lg font-bold text-gray-900 mb-4 flex items-center space-x-2">
                <AlertTriangle className="h-5 w-5 text-red-600" />
                <span>Top Risk Areas</span>
              </h2>
              
              <div className="space-y-3">
                {riskSummary.top_risk_areas.map((area, index) => {
                  const colors = getRiskColor(area.concern_level);
                  return (
                    <Card key={index}>
                      <CardContent className="p-4">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <div className="flex items-center space-x-2 mb-1">
                              <Badge className="text-xs">{area.section}</Badge>
                              <h3 className="font-semibold text-gray-900">{area.name}</h3>
                            </div>
                            <p className="text-sm text-gray-600">
                              Risk Score: <strong>{area.risk_score}%</strong> - This section requires immediate attention and targeted risk mitigation strategies.
                            </p>
                          </div>
                          <div 
                            className="px-3 py-1 rounded font-bold text-sm ml-4"
                            style={{ backgroundColor: colors.bg, color: colors.text }}
                          >
                            {area.concern_level}
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  );
                })}
              </div>
            </div>

            {/* Placeholder for additional sections */}
            <div>
              <h2 className="text-lg font-bold text-gray-900 mb-4 flex items-center space-x-2">
                <FileText className="h-5 w-5 text-blue-600" />
                <span>Detailed Analysis</span>
              </h2>
              
              <Card>
                <CardContent className="p-6">
                  <div className="text-center py-8">
                    <Shield className="h-12 w-12 text-gray-400 mx-auto mb-3" />
                    <p className="text-gray-700 font-medium mb-2">Comprehensive Risk Analysis Coming Soon</p>
                    <p className="text-sm text-gray-600">
                      This section will display detailed breakdowns, recommendations, compliance mappings, and actionable mitigation strategies based on your FAIRA assessment responses.
                    </p>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>

        {/* Right Panel - 25% width */}
        <div className="w-1/4 bg-white border-l overflow-y-auto">
          <div className="p-4">
            <h2 className="text-base font-bold text-gray-900 mb-3 flex items-center space-x-2">
              <FileText className="h-4 w-4 text-orange-600" />
              <span>Assessment Information</span>
            </h2>
            
            <div className="space-y-4 text-xs">
              <div>
                <p className="text-gray-600 mb-1">AI System Name</p>
                <p className="font-medium text-gray-900">{fairaData.ai_system_name || 'Not specified'}</p>
              </div>
              
              <div>
                <p className="text-gray-600 mb-1">System Version</p>
                <p className="font-medium text-gray-900">{fairaData.ai_system_version || 'Not specified'}</p>
              </div>
              
              <div>
                <p className="text-gray-600 mb-1">Business Unit</p>
                <p className="font-medium text-gray-900">{fairaData.business_unit || 'Not specified'}</p>
              </div>
              
              <div>
                <p className="text-gray-600 mb-1">Assessor</p>
                <p className="font-medium text-gray-900">{fairaData.assessor_name || 'Not specified'}</p>
              </div>
              
              <div>
                <p className="text-gray-600 mb-1">Completed Date</p>
                <p className="font-medium text-gray-900">
                  {assessment.completed_at 
                    ? new Date(assessment.completed_at).toLocaleDateString('en-AU', { 
                        year: 'numeric', 
                        month: 'long', 
                        day: 'numeric' 
                      })
                    : 'In Progress'
                  }
                </p>
              </div>
            </div>

            <div className="mt-6 pt-6 border-t">
              <h3 className="text-sm font-bold text-gray-900 mb-3">Next Steps</h3>
              <div className="space-y-2 text-xs">
                <div className="flex items-start space-x-2">
                  <CheckCircle2 className="h-4 w-4 text-green-600 flex-shrink-0 mt-0.5" />
                  <p className="text-gray-700">Review high-risk areas and develop mitigation plans</p>
                </div>
                <div className="flex items-start space-x-2">
                  <CheckCircle2 className="h-4 w-4 text-green-600 flex-shrink-0 mt-0.5" />
                  <p className="text-gray-700">Consult with stakeholders on priority risk controls</p>
                </div>
                <div className="flex items-start space-x-2">
                  <CheckCircle2 className="h-4 w-4 text-green-600 flex-shrink-0 mt-0.5" />
                  <p className="text-gray-700">Schedule follow-up assessment after implementing controls</p>
                </div>
              </div>
            </div>

            {/* Declaration Info */}
            {fairaData.declaration_confirmed && (
              <div className="mt-6 pt-6 border-t">
                <h3 className="text-sm font-bold text-gray-900 mb-3">Declaration</h3>
                <div className="space-y-2 text-xs">
                  <div className="flex items-start space-x-2">
                    <CheckCircle2 className="h-4 w-4 text-green-600 flex-shrink-0 mt-0.5" />
                    <p className="text-gray-700">
                      Assessment certified as accurate and complete
                    </p>
                  </div>
                  <div className="pl-6 space-y-1 text-gray-600">
                    <p>By: {fairaData.declaration_name || fairaData.assessor_name}</p>
                    <p>Date: {fairaData.declaration_date || 'Not specified'}</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default FairaResultsPage;
