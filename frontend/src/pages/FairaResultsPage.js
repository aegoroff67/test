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
  X,
  Target,
  Clock,
  Zap,
  ChevronDown,
  ChevronUp
} from 'lucide-react';
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer, PieChart, Pie, Cell, Legend, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts';

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

// Risk Stacked Column Component for FAIRA
const RiskStackedColumn = ({ score }) => {
  // Define the 5 risk tiers based on the specified bands
  const tiers = [
    { name: 'Very High', min: 81, max: 100, color: '#7B0000', percentage: 20 },  // Dark red
    { name: 'High', min: 61, max: 80, color: '#FF0000', percentage: 20 },        // Red
    { name: 'Medium', min: 41, max: 60, color: '#FFC000', percentage: 20 },      // Orange
    { name: 'Low', min: 21, max: 40, color: '#FFFF00', percentage: 20 },         // Yellow
    { name: 'Very Low', min: 0, max: 20, color: '#00B050', percentage: 20 }      // Green
  ];

  // Determine which tier the score falls into
  const getCurrentTier = (scoreValue) => {
    const numScore = Math.round(Number(scoreValue) || 0);
    if (numScore >= 81) return 'Very High';
    if (numScore >= 61) return 'High';
    if (numScore >= 41) return 'Medium';
    if (numScore >= 21) return 'Low';
    return 'Very Low';
  };

  const currentTier = getCurrentTier(score);

  // Calculate arrow position (percentage from bottom)
  const arrowPosition = Math.round(Number(score) || 0);

  return (
    <div className="flex flex-col items-center w-full">
      <div className="flex items-center justify-center w-full" style={{ height: '120px', gap: '30px' }}>
        {/* Stacked Column */}
        <div className="relative flex flex-col" style={{ width: '75px', height: '100px' }}>
          {tiers.map((tier, index) => (
            <div
              key={index}
              className="relative border border-gray-800"
              style={{
                height: `${tier.percentage}%`,
              backgroundColor: tier.color,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
          >
            <div className="text-center px-1">
              <div className={`text-[9px] font-semibold leading-tight ${tier.name === 'Very High' ? 'text-white' : 'text-gray-900'}`}>
                {tier.name}
              </div>
            </div>
          </div>
        ))}
        
        {/* Score arrow indicator */}
        <div
          className="absolute right-0 flex items-center"
          style={{
            bottom: `${arrowPosition}%`,
            transform: 'translateY(50%)',
            right: '-8px'
          }}
        >
          <div
            style={{
              width: 0,
              height: 0,
              borderTop: '6px solid transparent',
              borderBottom: '6px solid transparent',
              borderRight: '8px solid #000000'
            }}
          />
        </div>
      </div>

      {/* Score Display */}
      <div className="flex flex-col items-center">
        <div className="text-2xl font-bold text-gray-900">
          {Math.round(score)}
        </div>
        <div className="text-[15px] font-semibold text-gray-700 leading-tight text-center">
          {currentTier} Risk
        </div>
        <div className="text-[10px] italic text-gray-500 mt-1 text-center">
          Risk score shown as a normalised index (0–100).
        </div>
      </div>
      </div>
    </div>
  );
};

// Control Card Component for Top 3 Controls
const ControlCard = ({ control, index, isExpanded, onToggle }) => {
  // Priority badge colors
  const getPriorityColor = (priority) => {
    switch(priority) {
      case 'High':
        return 'bg-red-100 text-red-700 border-red-200';
      case 'Medium':
        return 'bg-yellow-100 text-yellow-700 border-yellow-200';
      case 'Low':
        return 'bg-green-100 text-green-700 border-green-200';
      default:
        return 'bg-gray-100 text-gray-700 border-gray-200';
    }
  };

  // Effort badge colors
  const getEffortColor = (effort) => {
    switch(effort) {
      case 'Low':
        return 'bg-green-50 text-green-600';
      case 'Medium':
        return 'bg-yellow-50 text-yellow-600';
      case 'High':
        return 'bg-red-50 text-red-600';
      default:
        return 'bg-gray-50 text-gray-600';
    }
  };

  // Horizon badge colors
  const getHorizonColor = (horizon) => {
    switch(horizon) {
      case 'Immediate':
        return 'bg-teal-50 text-teal-600';
      case 'Short-term':
        return 'bg-blue-50 text-blue-600';
      case 'Medium-term':
        return 'bg-purple-50 text-purple-600';
      case 'Ongoing':
        return 'bg-orange-50 text-orange-600';
      default:
        return 'bg-gray-50 text-gray-600';
    }
  };

  return (
    <div className="border border-teal-200 rounded-lg bg-teal-50/50 overflow-hidden">
      {/* Header - always visible */}
      <div 
        className="p-2 cursor-pointer hover:bg-teal-50 transition-colors"
        onClick={() => onToggle(index)}
      >
        <div className="flex items-start gap-2">
          {/* Rank badge */}
          <div className="flex-shrink-0 w-5 h-5 rounded-full bg-teal-600 text-white flex items-center justify-center text-[10px] font-bold">
            {index + 1}
          </div>
          
          {/* Control title and priority */}
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-1.5 mb-0.5">
              <span className="text-xs font-semibold text-gray-900 leading-tight">{control.title}</span>
              <span className={`px-1 py-0.5 rounded text-[9px] font-medium border ${getPriorityColor(control.priority)}`}>
                {control.priority}
              </span>
            </div>
            <p className="text-[10px] text-gray-600 line-clamp-2">{control.description}</p>
          </div>
          
          {/* Expand/collapse icon */}
          <div className="flex-shrink-0 text-gray-400">
            {isExpanded ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
          </div>
        </div>
      </div>
      
      {/* Expanded content */}
      {isExpanded && (
        <div className="px-2 pb-2 pt-1 border-t border-teal-100 bg-white/50">
          {/* Effort & Horizon badges */}
          <div className="flex flex-wrap gap-1 mb-2">
            <span className={`px-1.5 py-0.5 rounded text-[9px] font-medium flex items-center gap-0.5 ${getEffortColor(control.implementation_effort)}`}>
              <Zap className="h-2.5 w-2.5" />
              {control.implementation_effort} Effort
            </span>
            <span className={`px-1.5 py-0.5 rounded text-[9px] font-medium flex items-center gap-0.5 ${getHorizonColor(control.implementation_horizon)}`}>
              <Clock className="h-2.5 w-2.5" />
              {control.implementation_horizon}
            </span>
          </div>
          
          {/* Domains */}
          <div className="mb-2">
            <div className="text-[9px] font-semibold text-gray-500 uppercase mb-0.5">Domains</div>
            <div className="flex flex-wrap gap-1">
              {control.domains.map((domain, i) => (
                <span key={i} className="px-1 py-0.5 bg-gray-100 text-gray-600 rounded text-[9px]">
                  {domain}
                </span>
              ))}
            </div>
          </div>
          
          {/* Detailed description */}
          <div className="mb-2">
            <div className="text-[9px] font-semibold text-gray-500 uppercase mb-0.5">Details</div>
            <p className="text-[10px] text-gray-700 leading-relaxed">{control.detailed_description}</p>
          </div>
          
          {/* Rationale */}
          {control.rationale && (
            <div className="mb-2">
              <div className="text-[9px] font-semibold text-gray-500 uppercase mb-0.5">Why This Control?</div>
              <p className="text-[10px] text-teal-700 italic">{control.rationale}</p>
            </div>
          )}
          
          {/* Evidence examples */}
          {control.evidence_examples && control.evidence_examples.length > 0 && (
            <div>
              <div className="text-[9px] font-semibold text-gray-500 uppercase mb-0.5">Evidence Examples</div>
              <div className="flex flex-wrap gap-1">
                {control.evidence_examples.slice(0, 4).map((example, i) => (
                  <span key={i} className="px-1 py-0.5 bg-blue-50 text-blue-600 rounded text-[9px]">
                    {example}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
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
  
  // Top 3 Controls from API
  const [topControls, setTopControls] = useState([]);
  const [controlsLoading, setControlsLoading] = useState(false);
  const [expandedControls, setExpandedControls] = useState({}); // Track expanded state by index
  
  // Toggle control expansion
  const toggleControlExpanded = (index) => {
    setExpandedControls(prev => ({
      ...prev,
      [index]: !prev[index]
    }));
  };
  
  // Radar chart data from API
  const [radarChartData, setRadarChartData] = useState(null);

  // Risk summary data from API  
  const [riskSummary, setRiskSummary] = useState({
    overall_risk_level: 'Medium',
    overall_risk_score: 0,
    risk_category: 'Calculating...',
    domain_scores: {},
    section_scores: [],
    top_risk_areas: []
  });

  // Warning Light System - determines indicator colour, tier, and tooltip based on score and chart type
  const getWarningLight = (chartId, score, riskViewType = 'residual') => {
    const numScore = Number(score) || 0;
    
    switch (chartId) {
      case 'impact':
        // Domain Impact: Red ≥70, Amber 40-69, Green <40
        if (numScore >= 70) {
          return {
            colour: 'red',
            tier: 'High Impact',
            microLabel: 'Impact Signal',
            tooltipTitle: 'High Impact Potential',
            tooltipText: "This system exhibits a high potential for significant consequences if risks materialise. Impacts may be substantial in scale, severity, or scope, even if likelihood is currently limited."
          };
        } else if (numScore >= 40) {
          return {
            colour: 'amber',
            tier: 'Moderate Impact',
            microLabel: 'Impact Signal',
            tooltipTitle: 'Moderate Impact Potential',
            tooltipText: "Potential impacts within this system are assessed as moderate. Consequences may be material but are generally more limited in scale or severity."
          };
        } else {
          return {
            colour: 'green',
            tier: 'Low Impact',
            microLabel: 'Impact Signal',
            tooltipTitle: 'Low Impact Potential',
            tooltipText: "Potential impacts associated with this system are assessed as limited, indicating lower consequence severity if risks were to occur within the assessed context."
          };
        }
      
      case 'likelihood':
        // Domain Likelihood: Red ≥60, Amber 30-59, Green <30
        if (numScore >= 60) {
          return {
            colour: 'red',
            tier: 'High Likelihood',
            microLabel: 'Likelihood Signal',
            tooltipTitle: 'Elevated Likelihood',
            tooltipText: "Risk events within this system are assessed as likely to occur under current conditions, indicating ongoing exposure."
          };
        } else if (numScore >= 30) {
          return {
            colour: 'amber',
            tier: 'Moderate Likelihood',
            microLabel: 'Likelihood Signal',
            tooltipTitle: 'Moderate Likelihood',
            tooltipText: "The likelihood of risk events occurring within this system is assessed as moderate, suggesting some exposure depending on context and conditions."
          };
        } else {
          return {
            colour: 'green',
            tier: 'Low Likelihood',
            microLabel: 'Likelihood Signal',
            tooltipTitle: 'Low Likelihood',
            tooltipText: "Risk events within this system are considered unlikely to occur based on current information and conditions."
          };
        }
      
      case 'control':
        // Domain Control Effectiveness: Inverted - Red <30, Amber 30-59, Green ≥60
        if (numScore < 30) {
          return {
            colour: 'red',
            tier: 'Low Effectiveness',
            microLabel: 'Control Signal',
            tooltipTitle: 'Low Control Effectiveness',
            tooltipText: "Existing controls may not sufficiently mitigate identified risks within this system, increasing reliance on monitoring or future control strengthening."
          };
        } else if (numScore < 60) {
          return {
            colour: 'amber',
            tier: 'Partial Effectiveness',
            microLabel: 'Control Signal',
            tooltipTitle: 'Partially Effective Controls',
            tooltipText: "Controls provide some mitigation of risk but may not fully address all relevant risk drivers within this system."
          };
        } else {
          return {
            colour: 'green',
            tier: 'Effective Controls',
            microLabel: 'Control Signal',
            tooltipTitle: 'Effective Controls',
            tooltipText: "Controls within this system contribute to mitigating identified risks. Their presence reduces exposure but does not eliminate risk, particularly where potential impacts are high."
          };
        }
      
      case 'risk':
        // Risk chart - depends on whether viewing inherent or residual
        if (riskViewType === 'inherent') {
          // Inherent Domain Risk: Red ≥60, Amber 20-59, Green <20
          if (numScore >= 60) {
            return {
              colour: 'red',
              tier: 'High Inherent Exposure',
              microLabel: 'Inherent Exposure Signal',
              tooltipTitle: 'High Baseline Exposure (Contextual)',
              tooltipText: "This system exhibits a high level of baseline risk in the absence of controls. This reflects the nature, scale, or context of the system rather than any control deficiencies."
            };
          } else if (numScore >= 20) {
            return {
              colour: 'amber',
              tier: 'Moderate Inherent Exposure',
              microLabel: 'Inherent Exposure Signal',
              tooltipTitle: 'Moderate Baseline Exposure',
              tooltipText: "Baseline risk within this system is assessed as moderate, indicating some inherent exposure prior to the application of controls."
            };
          } else {
            return {
              colour: 'green',
              tier: 'Low Inherent Exposure',
              microLabel: 'Inherent Exposure Signal',
              tooltipTitle: 'Low Baseline Exposure',
              tooltipText: "Baseline risk within this system is assessed as low, reflecting limited inherent exposure based on system context."
            };
          }
        } else {
          // Residual Domain Risk: Red ≥60, Amber 20-59, Green <20
          if (numScore >= 60) {
            return {
              colour: 'red',
              tier: 'High Residual Risk',
              microLabel: 'Residual Risk Signal',
              tooltipTitle: 'Elevated Residual Risk',
              tooltipText: "After considering impact, likelihood, and control effectiveness, this system retains a high level of residual risk, indicating areas requiring prioritised attention."
            };
          } else if (numScore >= 20) {
            return {
              colour: 'amber',
              tier: 'Moderate Residual Risk',
              microLabel: 'Residual Risk Signal',
              tooltipTitle: 'Moderate Residual Risk',
              tooltipText: "Residual risk within this system is assessed as moderate, suggesting some ongoing exposure that may warrant monitoring or further consideration."
            };
          } else {
            return {
              colour: 'green',
              tier: 'Low Residual Risk',
              microLabel: 'Residual Risk Signal',
              tooltipTitle: 'Low Residual Risk',
              tooltipText: "Residual risk within this system is currently assessed as limited, reflecting the combined effect of impact, likelihood, and existing controls under current conditions. This does not imply the absence of risk or the need for ongoing governance."
            };
          }
        }
      
      default:
        return {
          colour: 'green',
          tier: 'Normal',
          microLabel: 'Signal',
          tooltipTitle: 'Status',
          tooltipText: 'No specific signal is highlighted for this indicator based on available assessment inputs.'
        };
    }
  };

  // Warning Light Component
  const WarningLight = ({ chartId, score, riskViewType }) => {
    const [showTooltip, setShowTooltip] = useState(false);
    const warning = getWarningLight(chartId, score, riskViewType);
    
    const colourClasses = {
      red: 'bg-red-500',
      amber: 'bg-amber-400',
      green: 'bg-green-500'
    };
    
    const glowClasses = {
      red: 'shadow-[0_0_8px_2px_rgba(239,68,68,0.6)]',
      amber: 'shadow-[0_0_8px_2px_rgba(251,191,36,0.6)]',
      green: 'shadow-[0_0_8px_2px_rgba(34,197,94,0.6)]'
    };
    
    return (
      <div className="relative flex flex-col items-center">
        <span className="text-[8px] text-gray-500 mb-0.5 whitespace-nowrap">{warning.microLabel}</span>
        <button
          onMouseEnter={() => setShowTooltip(true)}
          onMouseLeave={() => setShowTooltip(false)}
          onClick={() => setShowTooltip(!showTooltip)}
          className={`w-4 h-4 rounded-full ${colourClasses[warning.colour]} ${glowClasses[warning.colour]} border border-white/50 cursor-pointer transition-all hover:scale-110`}
          aria-label={warning.tier}
        />
        <span className="text-[8px] text-gray-600 mt-0.5 font-medium whitespace-nowrap">{warning.tier}</span>
        
        {/* Tooltip */}
        {showTooltip && (
          <div className="absolute top-full mt-2 right-0 z-50 w-56 bg-white border border-gray-200 rounded-lg shadow-xl p-3">
            <div className="flex items-center gap-2 mb-2">
              <div className={`w-3 h-3 rounded-full ${colourClasses[warning.colour]}`} />
              <h4 className="text-xs font-semibold text-gray-900">{warning.tooltipTitle}</h4>
            </div>
            <p className="text-[10px] text-gray-600 leading-relaxed">{warning.tooltipText}</p>
          </div>
        )}
      </div>
    );
  };

  // The 8 FAIRA Part B domains with short labels for radar chart display
  const fairadomains = [
    { id: 'B1', shortLabel: 'Wellbeing', fullName: 'Human, Societal and Environmental Wellbeing' },
    { id: 'B2', shortLabel: 'Values', fullName: 'Human-Centred Values' },
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
  
  // State for Domain Risk view toggle (Inherent vs Residual)
  const [riskViewType, setRiskViewType] = useState('residual');
  
  // Calculate Inherent Risk data (Impact × Likelihood, without CE division)
  const domainInherentRiskData = React.useMemo(() => {
    return fairadomains.map(domain => {
      const impactData = domainImpactData.find(d => d.domain === domain.shortLabel);
      const likelihoodData = domainLikelihoodData.find(d => d.domain === domain.shortLabel);
      const impact = impactData?.score || 0;
      const likelihood = likelihoodData?.score || 0;
      // Inherent Risk = (Impact × Likelihood) / 100 to normalize to 0-100
      const inherentRisk = Math.min(100, (impact * likelihood) / 100);
      return {
        domain: domain.shortLabel,
        fullName: domain.fullName,
        score: Math.round(inherentRisk * 10) / 10,
        fullMark: 100
      };
    });
  }, [domainImpactData, domainLikelihoodData, fairadomains]);

  // Chart configurations for the 4 radar charts
  const radarCharts = [
    {
      id: 'impact',
      title: 'Domain Impact',
      overallLabel: 'Overall Impact',
      overallValue: riskSummary.total_impact || 0,
      data: domainImpactData,
      color: '#ef4444', // Red
      formula: 'Domain_Impact = Σ(Domain Impact modifiers)',
      tooltipContent: {
        whatItShows: 'How serious the consequences would be in this area if the AI system caused harm.',
        whyItChanges: 'Higher where decisions affect people\'s rights, safety, or access to services.',
        example: 'An AI used in healthcare or law enforcement would have higher impact than one used for internal reporting.'
      }
    },
    {
      id: 'likelihood',
      title: 'Domain Likelihood',
      overallLabel: 'Overall Likelihood',
      overallValue: riskSummary.total_likelihood || 0,
      data: domainLikelihoodData,
      color: '#f97316', // Orange
      formula: 'Domain_Likelihood = Σ(Domain Likelihood modifiers)',
      tooltipContent: {
        whatItShows: 'How likely risks in this area are to occur based on how the AI is designed and used.',
        whyItChanges: 'Increases with higher automation, poorer data quality, or limited human oversight.',
        example: 'An AI that acts autonomously on live data is more likely to cause issues than one used only for decision support.'
      }
    },
    {
      id: 'control',
      title: 'Domain Control Effectiveness',
      overallLabel: 'Overall Control Effectiveness',
      overallValue: riskSummary.total_control_effectiveness || 0,
      data: domainControlEffectivenessData,
      color: '#22c55e', // Green
      formula: 'Domain_CE = Σ(Domain CE modifiers)',
      tooltipContent: {
        whatItShows: 'How strong the safeguards and governance are for managing risks in this area.',
        whyItChanges: 'Improves when testing, oversight, training, and clear processes are in place.',
        example: 'Regular audits, documented accountability, and clear escalation paths increase control effectiveness.'
      }
    },
    {
      id: 'risk',
      title: riskViewType === 'inherent' ? 'Inherent Domain Risk' : 'Residual Domain Risk',
      overallLabel: riskViewType === 'inherent' ? 'Overall Inherent Risk' : 'Overall Residual Risk',
      overallValue: riskViewType === 'inherent' ? (riskSummary.overall_inherent_risk || 0) : (riskSummary.overall_risk_score || 0),
      data: riskViewType === 'inherent' ? domainInherentRiskData : domainRiskData,
      color: '#8b5cf6', // Purple
      formula: riskViewType === 'inherent' 
        ? 'Domain_Risk = Domain_Impact × Domain_Likelihood'
        : 'Domain_Risk = (Domain_Impact × Domain_Likelihood) ÷ Domain_CE',
      isRiskChart: true,
      hasToggle: true
    }
  ];

  // State for info modal
  const [activeInfoModal, setActiveInfoModal] = useState(null);

  // Calculate response distribution from risk summary
  const responseDistribution = React.useMemo(() => {
    // Define risk tier colors matching the stacked bar
    const tierColors = {
      'Very Low': '#00B050',
      'Low': '#FFFF00', 
      'Medium': '#FFC000',
      'High': '#FF0000',
      'Very High': '#7B0000'
    };
    
    if (!riskSummary?.domain_scores) {
      return [
        { name: 'Very Low', count: 0, color: tierColors['Very Low'], domains: [] },
        { name: 'Low', count: 0, color: tierColors['Low'], domains: [] },
        { name: 'Medium', count: 0, color: tierColors['Medium'], domains: [] },
        { name: 'High', count: 0, color: tierColors['High'], domains: [] },
        { name: 'Very High', count: 0, color: tierColors['Very High'], domains: [] }
      ];
    }
    
    const tierData = {
      'Very Low': { count: 0, domains: [] },
      'Low': { count: 0, domains: [] },
      'Medium': { count: 0, domains: [] },
      'High': { count: 0, domains: [] },
      'Very High': { count: 0, domains: [] }
    };
    
    // Domain name mapping for display
    const domainDisplayNames = {
      'Wellbeing': 'Human, Societal and Environmental Wellbeing',
      'Values': 'Human-Centred Values',
      'Fairness': 'Fairness',
      'Privacy': 'Privacy Protection and Security',
      'Reliability': 'Reliability and Safety',
      'Transparency': 'Transparency and Explainability',
      'Contestability': 'Contestability',
      'Accountability': 'Accountability'
    };
    
    Object.entries(riskSummary.domain_scores).forEach(([domainKey, scores]) => {
      const risk = scores.Risk || 0;
      const displayName = domainDisplayNames[domainKey] || domainKey;
      
      if (risk >= 81) {
        tierData['Very High'].count++;
        tierData['Very High'].domains.push(displayName);
      } else if (risk >= 61) {
        tierData['High'].count++;
        tierData['High'].domains.push(displayName);
      } else if (risk >= 41) {
        tierData['Medium'].count++;
        tierData['Medium'].domains.push(displayName);
      } else if (risk >= 21) {
        tierData['Low'].count++;
        tierData['Low'].domains.push(displayName);
      } else {
        tierData['Very Low'].count++;
        tierData['Very Low'].domains.push(displayName);
      }
    });
    
    return [
      { name: 'Very Low', count: tierData['Very Low'].count, color: tierColors['Very Low'], domains: tierData['Very Low'].domains },
      { name: 'Low', count: tierData['Low'].count, color: tierColors['Low'], domains: tierData['Low'].domains },
      { name: 'Medium', count: tierData['Medium'].count, color: tierColors['Medium'], domains: tierData['Medium'].domains },
      { name: 'High', count: tierData['High'].count, color: tierColors['High'], domains: tierData['High'].domains },
      { name: 'Very High', count: tierData['Very High'].count, color: tierColors['Very High'], domains: tierData['Very High'].domains }
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
            // Calculate overall inherent risk from total_impact and total_likelihood
            const totalImpact = summary.total_impact || 0;
            const totalLikelihood = summary.total_likelihood || 0;
            const overallInherentRisk = Math.round((totalImpact * totalLikelihood) / 100);
            
            setRiskSummary({
              overall_risk_level: summary.overall_risk_level || 'Medium',
              overall_risk_score: summary.overall_risk_score || 0,
              risk_category: getRiskCategory(summary.overall_risk_level),
              domain_scores: summary.domain_scores || {},
              section_scores: Object.entries(summary.domain_scores || {}).map(([name, scores]) => ({
                section_id: name,
                section_name: fairadomains.find(d => d.shortLabel === name)?.fullName || name,
                risk_score: scores.Risk || 0,
                risk_level: getRiskLevelFromScore(scores.Risk || 0)
              })),
              top_risk_areas: summary.top_risk_areas || [],
              // Store overall totals for radar chart subtitles
              total_impact: totalImpact,
              total_likelihood: totalLikelihood,
              total_control_effectiveness: summary.total_control_effectiveness || 0,
              overall_inherent_risk: overallInherentRisk
            });
          }
        }
      } catch (scoreError) {
        console.warn('Could not fetch FAIRA scores:', scoreError);
        // Continue with assessment display even if scores fail
      }
      
      // Fetch recommended controls
      setControlsLoading(true);
      try {
        const controlsResponse = await axios.get(`${API}/assessments/${id}/faira-controls?top_n=3`);
        if (controlsResponse.data?.controls?.top_controls) {
          setTopControls(controlsResponse.data.controls.top_controls);
        }
      } catch (controlsError) {
        console.warn('Could not fetch FAIRA controls:', controlsError);
        // Continue with results display even if controls fail
      } finally {
        setControlsLoading(false);
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
      const token = localStorage.getItem('token');
      
      // Get indices of expanded controls
      const expandedIndices = Object.entries(expandedControls)
        .filter(([_, isExpanded]) => isExpanded)
        .map(([index]) => index)
        .join(',');
      
      const response = await axios.get(
        `${API}/assessments/${id}/faira-results-pdf${expandedIndices ? `?expanded=${expandedIndices}` : ''}`,
        {
          headers: { Authorization: `Bearer ${token}` },
          responseType: 'blob'
        }
      );
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `FAIRA_Results_Summary_${assessment?.name || 'Assessment'}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      toast.success('PDF report generated successfully');
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
      const response = await axios.get(`${API}/assessments/${id}/report`, {
        params: {
          view_type: 'detailed',
          use_ai: true
        },
        responseType: 'blob',
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
      let filename = `FAIRA_Risk_Assessment_Report_${assessment?.name || id}.docx`;
      
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
      
      toast.success('FAIRA report downloaded successfully');
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
      <header className="bg-white shadow-sm border-b flex-shrink-0">
        <div className="max-w-full px-6">
          <div className="flex justify-between items-center h-14">
            {/* Logo & Title */}
            <div className="flex items-center space-x-3">
              <Logo className="h-10 w-10" />
              <div>
                <h1 className="text-base font-bold text-gray-900">AM AI SAFE</h1>
                <p className="text-xs text-orange-600">FAIRA Risk Assessment Results</p>
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
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              Dashboard
            </Button>
          </div>
        </div>
      </header>

      {/* Results Summary Bar */}
      <div className="bg-gradient-to-r from-orange-50 to-orange-100 border-b border-orange-200">
        <div className="px-6 py-4">
          <div className="flex items-stretch gap-6">
            {/* First 15% - Risk Stacked Column */}
            <div className="flex flex-col items-center justify-center" style={{ width: '15%' }}>
              <RiskStackedColumn score={riskSummary.overall_risk_score} />
            </div>

            {/* Second 15% - Risk Level Descriptions */}
            <div className="px-4" style={{ width: '15%' }}>
              <p className="text-sm font-bold text-gray-900 mb-2 mt-0">Risk Level Description</p>
              <div className="text-gray-700 space-y-1" style={{ fontSize: '11px' }}>
                <p><span className="font-bold">Very High (81-100):</span> Critical Risk</p>
                <p><span className="font-bold">High (61-80):</span> Significant Risk</p>
                <p><span className="font-bold">Medium (41-60):</span> Moderate Risk</p>
                <p><span className="font-bold">Low (21-40):</span> Minor Risk</p>
                <p><span className="font-bold">Very Low (0-20):</span> Minimal Risk</p>
              </div>
            </div>

            {/* Middle 50% - Summary Text */}
            <div className="px-6" style={{ width: '50%' }}>
              <p className="text-sm font-bold text-gray-900 mb-2 mt-0">Risk Assessment Summary</p>
              <p className="text-xs text-gray-700 leading-relaxed">
                The FAIRA assessment indicates that <strong>{fairaData.ai_system_name || 'this AI system'}</strong> presents an overall risk level of <strong>{riskSummary.overall_risk_level}</strong> with a risk score of <strong>{riskSummary.overall_risk_score}</strong>. This classification reflects a <strong>{
                  riskSummary.overall_risk_level === 'Very High' ? 'Critical Risk profile' :
                  riskSummary.overall_risk_level === 'High' ? 'Significant Risk profile' :
                  riskSummary.overall_risk_level === 'Medium' ? 'Moderate Risk profile' :
                  riskSummary.overall_risk_level === 'Low' ? 'Minor Risk profile' :
                  riskSummary.overall_risk_level === 'Very Low' ? 'Minimal Risk profile' :
                  'risk profile'
                }</strong> across regulatory compliance, data governance, fairness considerations, and accountability measures. Key areas requiring attention include <strong>{riskSummary.top_risk_areas[0]?.fullName}</strong>, <strong>{riskSummary.top_risk_areas[1]?.fullName}</strong>, and <strong>{riskSummary.top_risk_areas[2]?.fullName}</strong>. Targeted risk mitigation strategies should focus on strengthening controls in high-risk sections while maintaining established safeguards in lower-risk areas.
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
                      <span>Detailed Report (DOCX)</span>
                    </div>
                  )}
                </Button>
              </div>

              {/* Button 2 - Results Summary Report */}
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
                    title="Available for AI System Maturity Assessments only."
                  >
                    <Button 
                      className="w-full text-[10px] px-1 py-1.5 h-auto bg-gray-400 cursor-not-allowed opacity-60"
                      disabled={true}
                    >
                      <div className="flex items-center justify-center space-x-0.5">
                        <Grid3X3 className="h-3 w-3" />
                        <span>Framework Coverage</span>
                      </div>
                    </Button>
                  </div>
                  <div 
                    className="flex-1"
                    title="Not available in this assessment."
                  >
                    <Button 
                      className="w-full text-[10px] px-1 py-1.5 h-auto bg-gray-400 cursor-not-allowed opacity-60"
                      disabled={true}
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
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-base font-bold text-gray-900 flex items-center space-x-2">
                <Shield className="h-4 w-4 text-orange-600" />
                <span>{riskViewType === 'inherent' ? 'Inherent Domain Risk' : 'Residual Domain Risk'}</span>
              </h2>
              <div className="bg-gray-100 rounded-md p-1.5 border border-gray-200">
                <div className="flex flex-col gap-1">
                  <label className="flex items-center gap-1.5 cursor-pointer">
                    <input
                      type="radio"
                      name="leftPanelRiskViewType"
                      value="inherent"
                      checked={riskViewType === 'inherent'}
                      onChange={(e) => setRiskViewType(e.target.value)}
                      className="w-3 h-3 text-purple-600"
                    />
                    <span className="text-[10px] text-gray-700">Inherent Risk</span>
                  </label>
                  <label className="flex items-center gap-1.5 cursor-pointer">
                    <input
                      type="radio"
                      name="leftPanelRiskViewType"
                      value="residual"
                      checked={riskViewType === 'residual'}
                      onChange={(e) => setRiskViewType(e.target.value)}
                      className="w-3 h-3 text-purple-600"
                    />
                    <span className="text-[10px] text-gray-700">Residual Risk</span>
                  </label>
                </div>
              </div>
            </div>
            
            <div className="space-y-2">
              {[...(riskViewType === 'inherent' ? domainInherentRiskData : domainRiskData)]
                .sort((a, b) => b.score - a.score) // Sort by score, highest first
                .map((domain) => {
                const riskLevel = getRiskLevelFromScore(domain.score);
                const colors = getRiskColor(riskLevel);
                return (
                  <div key={domain.domain} className="space-y-0.5">
                    <div className="flex items-center">
                      <div 
                        className="px-1 py-0.5 rounded text-xs font-bold min-w-[32px] text-center"
                        style={{ backgroundColor: colors.bg, color: colors.text }}
                      >
                        {Math.round(domain.score)}
                      </div>
                      <span className="font-medium text-gray-900 text-xs ml-[15px]">{domain.fullName}</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-1.5">
                      <div 
                        className="h-1.5 rounded-full transition-all duration-300"
                        style={{ width: `${domain.score}%`, backgroundColor: colors.bg }}
                      ></div>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Residual Risk Distribution */}
            <div className="mt-6">
              <h2 className="text-base font-bold text-gray-900 mb-1 flex items-center space-x-2">
                <BarChart3 className="h-4 w-4 text-orange-600" />
                <span>Residual Risk Distribution</span>
              </h2>
              <p className="text-xs text-gray-600 mb-3">Number of assessed domains aligned to each residual risk tier (8 total).</p>
              
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={responseDistribution} margin={{ top: 10, right: 10, left: -10, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <XAxis 
                    dataKey="name" 
                    tick={{ fontSize: 10 }}
                    interval={0}
                  />
                  <YAxis 
                    domain={[0, 8]}
                    ticks={[1, 2, 3, 4, 5, 6, 7, 8]}
                    tick={{ fontSize: 10 }}
                    allowDecimals={false}
                  />
                  <Tooltip 
                    content={({ active, payload }) => {
                      if (active && payload && payload.length) {
                        const data = payload[0].payload;
                        // Map risk level to description
                        const riskDescriptions = {
                          'Very High': 'Critical Risk',
                          'High': 'Significant Risk',
                          'Medium': 'Moderate Risk',
                          'Low': 'Minor Risk',
                          'Very Low': 'Minimal Risk'
                        };
                        const description = riskDescriptions[data.name] || '';
                        return (
                          <div className="bg-white p-3 border border-gray-200 rounded shadow-lg max-w-xs">
                            <p className="font-bold text-gray-900 mb-1">{data.name} ({description})</p>
                            <p className="text-sm text-gray-700 mb-2">{data.count} domain{data.count !== 1 ? 's' : ''}</p>
                            {data.domains && data.domains.length > 0 && (
                              <ul className="text-xs text-gray-600 list-disc list-inside space-y-0.5">
                                {data.domains.map((domain, idx) => (
                                  <li key={idx}>{domain}</li>
                                ))}
                              </ul>
                            )}
                          </div>
                        );
                      }
                      return null;
                    }}
                  />
                  <Bar 
                    dataKey="count" 
                    radius={[4, 4, 0, 0]}
                  >
                    {responseDistribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Bar>
                </BarChart>
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
                <span>FAIRA Domain Profiles</span>
              </h2>
              
              {/* 2x2 Grid of Radar Charts */}
              <div className="grid grid-cols-2 gap-4">
                {radarCharts.map((chart) => (
                  <Card key={chart.id} className="relative">
                    {/* Info Icon - Top Left */}
                    <button
                      onClick={() => setActiveInfoModal(chart.id)}
                      className="absolute top-2 left-2 z-10 p-1 rounded-full bg-blue-500 hover:bg-blue-600 transition-colors"
                      title={`${chart.title} Information`}
                    >
                      <Info className="h-3 w-3 text-white" />
                    </button>

                    {/* Warning Light & Risk Toggle - Top Right */}
                    <div className="absolute top-2 right-2 z-10 flex flex-col items-center">
                      <WarningLight 
                        chartId={chart.id} 
                        score={chart.overallValue} 
                        riskViewType={chart.hasToggle ? riskViewType : undefined}
                      />
                      
                      {/* Risk Type Toggle - below warning light, only for Domain Risk chart */}
                      {chart.hasToggle && (
                        <div className="mt-2 bg-gray-100 rounded-md p-1.5 border border-gray-200">
                          <span className="text-[8px] text-gray-500 block text-center mb-1">Risk View</span>
                          <div className="flex flex-col gap-1">
                            <label className="flex items-center gap-1.5 cursor-pointer">
                              <input
                                type="radio"
                                name="riskViewType"
                                value="inherent"
                                checked={riskViewType === 'inherent'}
                                onChange={(e) => setRiskViewType(e.target.value)}
                                className="w-3 h-3 text-purple-600"
                              />
                              <span className="text-[10px] text-gray-700">Inherent</span>
                            </label>
                            <label className="flex items-center gap-1.5 cursor-pointer">
                              <input
                                type="radio"
                                name="riskViewType"
                                value="residual"
                                checked={riskViewType === 'residual'}
                                onChange={(e) => setRiskViewType(e.target.value)}
                                className="w-3 h-3 text-purple-600"
                              />
                              <span className="text-[10px] text-gray-700">Residual</span>
                            </label>
                          </div>
                        </div>
                      )}
                    </div>

                    <CardContent className="pt-4 pb-2">
                      <h3 className="text-sm font-semibold text-gray-900 text-center mb-1">{chart.title}</h3>
                      <p className="text-xs text-gray-600 text-center mb-2">
                        {chart.overallLabel}: <span className="font-bold text-gray-900">{chart.overallValue}</span>
                      </p>
                      
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
                          <Tooltip 
                            content={({ active, payload }) => {
                              if (active && payload && payload.length) {
                                const data = payload[0].payload;
                                return (
                                  <div className="bg-white border border-gray-200 rounded-lg shadow-lg p-2">
                                    <p className="text-xs font-semibold text-gray-900">{data.fullName}</p>
                                    <p className="text-xs text-gray-600">Score: <span className="font-bold" style={{ color: chart.color }}>{data.score}</span></p>
                                  </div>
                                );
                              }
                              return null;
                            }}
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
                  <div className="bg-white rounded-lg shadow-xl w-full mx-4" style={{ maxWidth: '650px' }}>
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
                    {radarCharts.find(c => c.id === activeInfoModal)?.isRiskChart ? (
                      <div className="p-4 space-y-4 max-h-[60vh] overflow-y-auto">
                        <div>
                          <p className="text-sm font-semibold text-gray-900 mb-1">What this chart shows</p>
                          <p className="text-sm text-gray-600">
                            This chart shows the level of risk across each AI ethics domain.
                          </p>
                        </div>
                        <div>
                          <p className="text-sm font-semibold text-gray-900 mb-1">Inherent Risk</p>
                          <p className="text-sm text-gray-600">
                            <strong>Inherent risk</strong> shows the level of risk <strong>before any controls or safeguards are applied.</strong> It reflects the system's underlying exposure based on impact and likelihood alone.
                          </p>
                          <p className="text-sm text-gray-600 italic mt-2">
                            <strong>For example…</strong> An AI used in healthcare or law enforcement may show high inherent risk due to the potential severity of harm, even before considering controls.
                          </p>
                        </div>
                        <div>
                          <p className="text-sm font-semibold text-gray-900 mb-1">Residual Risk</p>
                          <p className="text-sm text-gray-600">
                            <strong>Residual risk</strong> shows the level of risk <strong>remaining after controls and governance measures are applied.</strong> It reflects how effectively existing safeguards reduce risk.
                          </p>
                          <p className="text-sm text-gray-600 italic mt-2">
                            <strong>For example…</strong> Strong oversight, testing, and accountability can significantly reduce residual risk, even where inherent risk is high.
                          </p>
                        </div>
                        <div>
                          <p className="text-sm font-semibold text-gray-900 mb-1">Why both views matter</p>
                          <p className="text-sm text-gray-600">
                            Comparing inherent and residual risk helps explain <strong>where controls are effective</strong> and <strong>where additional safeguards may be required.</strong>
                          </p>
                        </div>
                        <div>
                          <p className="text-sm font-semibold text-gray-900 mb-1">How to use this chart</p>
                          <p className="text-sm text-gray-600">
                            Use <strong>Residual Risk</strong> to understand current risk exposure.<br />
                            Use <strong>Inherent Risk</strong> to understand why controls are needed and what they are mitigating.
                          </p>
                        </div>
                      </div>
                    ) : (
                      <div className="p-4 space-y-4">
                        <div>
                          <p className="text-sm font-semibold text-gray-900 mb-1">What it shows</p>
                          <p className="text-sm text-gray-600">
                            {radarCharts.find(c => c.id === activeInfoModal)?.tooltipContent?.whatItShows}
                          </p>
                        </div>
                        <div>
                          <p className="text-sm font-semibold text-gray-900 mb-1">Why it changes</p>
                          <p className="text-sm text-gray-600">
                            {radarCharts.find(c => c.id === activeInfoModal)?.tooltipContent?.whyItChanges}
                          </p>
                        </div>
                        <div>
                          <p className="text-sm font-semibold text-gray-900 mb-1">For example…</p>
                          <p className="text-sm text-gray-600 italic">
                            {radarCharts.find(c => c.id === activeInfoModal)?.tooltipContent?.example}
                          </p>
                        </div>
                      </div>
                    )}
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
            
            {/* 3-column grid for assessment info */}
            <div className="grid grid-cols-3 gap-x-3 gap-y-2 text-xs">
              <div>
                <p className="text-gray-600 mb-0.5">AI System</p>
                <p className="font-medium text-gray-900 truncate" title={fairaData.ai_system_name || 'Not specified'}>{fairaData.ai_system_name || 'Not specified'}</p>
              </div>
              
              <div>
                <p className="text-gray-600 mb-0.5">Version</p>
                <p className="font-medium text-gray-900">{fairaData.ai_system_version || 'Not specified'}</p>
              </div>
              
              <div>
                <p className="text-gray-600 mb-0.5">Business Unit</p>
                <p className="font-medium text-gray-900 truncate" title={fairaData.business_unit || 'Not specified'}>{fairaData.business_unit || 'Not specified'}</p>
              </div>
              
              <div>
                <p className="text-gray-600 mb-0.5">Assessor</p>
                <p className="font-medium text-gray-900 truncate" title={fairaData.assessor_name || 'Not specified'}>{fairaData.assessor_name || 'Not specified'}</p>
              </div>
              
              <div className="col-span-2">
                <p className="text-gray-600 mb-0.5">Completed Date</p>
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

            {/* How to read these results */}
            <div className="mt-4 pt-4 border-t">
              <h3 className="text-sm font-bold text-gray-900 mb-2 flex items-center space-x-2">
                <svg className="h-4 w-4 text-orange-600" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
                  <path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <span>How To Read These Results</span>
              </h3>
              <div className="space-y-2 text-gray-700" style={{ fontSize: '11px' }}>
                <p>
                  Individual domain scores reflect <strong>localised residual risk within each risk area</strong>, while the overall risk score reflects the <strong>combined, system-level residual risk</strong> after considering cumulative impact, likelihood, and control effectiveness across all domains.
                </p>
                <p>
                  As a result, multiple low or moderate domain risks can <strong>aggregate into a higher overall system risk</strong> where controls are insufficient to offset combined impact and likelihood. This approach ensures that <strong>systemic risk is not understated</strong> when assessing AI systems.
                </p>
              </div>
            </div>

            {/* Top 3 Domain Risks */}
            <div className="mt-4 pt-4 border-t">
              <h3 className="text-sm font-bold text-gray-900 mb-2 flex items-center space-x-2">
                <AlertTriangle className="h-4 w-4 text-red-600" />
                <span>Top 3 Domain Risks</span>
              </h3>
              <div className="space-y-1.5">
                {riskSummary.top_risk_areas.slice(0, 3).map((area, index) => {
                  const colors = getRiskColor(area.concern_level);
                  return (
                    <div key={index} className="flex items-center space-x-2 p-2 bg-red-50 rounded border border-red-200">
                      <div className="flex-shrink-0 w-5 h-5 rounded-full bg-red-600 text-white flex items-center justify-center text-[10px] font-bold">
                        {index + 1}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="text-xs font-medium text-gray-900 truncate">{area.fullName}</div>
                      </div>
                      <div 
                        className="px-1.5 py-0.5 rounded text-[10px] font-bold"
                        style={{ backgroundColor: colors.bg, color: colors.text }}
                      >
                        {area.concern_level}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Top 3 Controls */}
            <div className="mt-4 pt-4 border-t">
              <h3 className="text-sm font-bold text-gray-900 mb-2 flex items-center space-x-2">
                <Target className="h-4 w-4 text-teal-600" />
                <span>Top 3 Controls</span>
              </h3>
              {controlsLoading ? (
                <div className="flex items-center justify-center py-4">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-teal-600"></div>
                  <span className="ml-2 text-xs text-gray-500">Loading controls...</span>
                </div>
              ) : topControls.length > 0 ? (
                <div className="space-y-2">
                  {topControls.map((control, index) => (
                    <ControlCard 
                      key={control.control_id} 
                      control={control} 
                      index={index}
                      isExpanded={!!expandedControls[index]}
                      onToggle={toggleControlExpanded}
                    />
                  ))}
                </div>
              ) : (
                <div className="text-xs text-gray-500 py-2">
                  No controls recommended based on current risk profile.
                </div>
              )}
            </div>

            <div className="mt-4 pt-4 border-t">
              <h3 className="text-sm font-bold text-gray-900 mb-2">Next Steps</h3>
              <div className="space-y-1.5 text-xs">
                <div className="flex items-start space-x-2">
                  <CheckCircle2 className="h-3.5 w-3.5 text-green-600 flex-shrink-0 mt-0.5" />
                  <p className="text-gray-700">Review high-risk areas and develop mitigation plans</p>
                </div>
                <div className="flex items-start space-x-2">
                  <CheckCircle2 className="h-3.5 w-3.5 text-green-600 flex-shrink-0 mt-0.5" />
                  <p className="text-gray-700">Consult with stakeholders on priority risk controls</p>
                </div>
                <div className="flex items-start space-x-2">
                  <CheckCircle2 className="h-3.5 w-3.5 text-green-600 flex-shrink-0 mt-0.5" />
                  <p className="text-gray-700">Schedule follow-up assessment after implementing controls</p>
                </div>
              </div>
            </div>

            {/* Declaration Info */}
            {fairaData.declaration_confirmed && (
              <div className="mt-4 pt-4 border-t">
                <h3 className="text-sm font-bold text-gray-900 mb-2">Declaration</h3>
                <div className="space-y-1.5 text-xs">
                  <div className="flex items-start space-x-2">
                    <CheckCircle2 className="h-3.5 w-3.5 text-green-600 flex-shrink-0 mt-0.5" />
                    <p className="text-gray-700">
                      I confirm that the information provided in this FAIRA assessment is accurate to the best of my knowledge at the time of completion.
                    </p>
                  </div>
                  <div className="pl-5 space-y-0.5 text-gray-600">
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
