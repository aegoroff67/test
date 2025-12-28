import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { toast } from 'sonner';
import Logo from '../components/Logo';
import InfoBadge from '../components/InfoBadge';
import FrameworkCoverageInfoModal from '../components/FrameworkCoverageInfoModal';
import { 
  ArrowLeft, 
  BarChart3,
  Shield,
  Globe,
  Building2,
  Scale,
  FileCheck,
  Layers,
  BookOpen,
  Award,
  Printer
} from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Framework configuration
const FRAMEWORKS = [
  {
    id: 'iso42001',
    title: 'AS ISO/IEC 42001:2023',
    icon: Shield,
    color: '#0066CC',
    description: 'AI Management System Standard'
  },
  {
    id: 'au_ethics',
    title: 'Australian AI Ethics Principles (2024)',
    icon: Scale,
    color: '#00A86B',
    description: 'National AI Ethics Framework'
  },
  {
    id: 'au_guidance',
    title: 'Australian Guidance for AI Adoption (2025)',
    icon: BookOpen,
    color: '#6B5B95',
    description: 'Government AI Adoption Guide'
  },
  {
    id: 'au_assurance',
    title: 'Australian National Framework for the Assurance of AI in Government (2024)',
    icon: Building2,
    color: '#E94B3C',
    description: 'Government AI Assurance Framework'
  },
  {
    id: 'eu_ai_act',
    title: 'EU AI Act (2024 final)',
    icon: Globe,
    color: '#003399',
    description: 'European AI Regulation'
  },
  {
    id: 'nist_rmf',
    title: 'NIST AI RMF (2023)',
    icon: FileCheck,
    color: '#FF6B35',
    description: 'AI Risk Management Framework'
  },
  {
    id: 'oecd',
    title: 'OECD Principles (2019)',
    icon: Layers,
    color: '#4A90A4',
    description: 'International AI Principles'
  },
  {
    id: 'singapore_maf',
    title: 'Singapore MAF (2024)',
    icon: Award,
    color: '#D4AF37',
    description: 'Model AI Governance Framework'
  }
];

// Placeholder data for charts - grouped bar chart format
const generatePlaceholderData = () => [
  { category: 'Strong Coverage', inherent: 58, achieved: 39 },
  { category: 'Moderate Coverage', inherent: 24, achieved: 32 },
  { category: 'Weak Coverage', inherent: 8, achieved: 13 },
  { category: 'No Coverage', inherent: 10, achieved: 16 }
];

// Chart colors
const CHART_COLORS = {
  inherent: '#1B4F72',  // Dark teal/blue
  achieved: '#E67E22'   // Orange
};

function FrameworkCoveragePage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [assessment, setAssessment] = useState(null);
  const [coverageData, setCoverageData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showInfoModal, setShowInfoModal] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem('token');
        
        // Fetch assessment and coverage data in parallel
        const [assessmentRes, coverageRes] = await Promise.all([
          axios.get(`${API}/assessments/${id}`, {
            headers: { Authorization: `Bearer ${token}` }
          }),
          axios.get(`${API}/assessments/${id}/framework-coverage`, {
            headers: { Authorization: `Bearer ${token}` }
          })
        ]);
        
        setAssessment(assessmentRes.data);
        setCoverageData(coverageRes.data);
      } catch (error) {
        console.error('Error fetching data:', error);
        toast.error('Failed to load framework coverage data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [id]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="loading-spinner w-8 h-8 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading framework coverage...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Top Header Section - Full Width */}
      <div className="bg-white border-b shadow-sm">
        <div className="px-6 py-3">
          {/* Header Row */}
          <div className="flex items-start justify-between">
            {/* Left Section: Logo + AM AI SAFE Title */}
            <div className="flex items-center space-x-3">
              <Logo size="sm" />
              <div>
                <h1 className="text-base font-bold text-gray-900">AM AI SAFE</h1>
                <p className="text-xs text-teal-600">Framework Coverage Overview</p>
              </div>
            </div>

            {/* Center Section: Framework Coverage Overview Content */}
            <div className="flex-1 mx-6">
              <div className="flex items-center">
                <h2 className="text-lg font-bold text-gray-900">
                  Framework Coverage Overview
                </h2>
                <InfoBadge
                  className="ml-2"
                  title="How to interpret this view"
                  onClick={() => setShowInfoModal(true)}
                />
              </div>
              <p className="text-xs text-gray-600 leading-relaxed mt-1" style={{ maxWidth: '1100px' }}>
                This view shows how comprehensively the <span className="font-semibold">controls</span> within selected AI governance frameworks are covered by the 
                AM AI SAFE assessment, based on how many assessment questions fully or partially address each framework control. 
                It compares coverage provided by design (<span className="font-semibold text-blue-600">Inherent Coverage</span>) with 
                coverage achieved based on assessment results (<span className="font-semibold text-green-600">Achieved Coverage</span>).
              </p>
            </div>

            {/* Assessment Name */}
            <div className="flex items-center mr-6">
              <span className="text-sm text-gray-700 font-bold">
                {assessment?.name || 'Assessment'}
              </span>
            </div>

            {/* Right Section: Buttons */}
            <div className="flex flex-col space-y-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => navigate(`/results/${id}`)}
                className="flex items-center space-x-2 border border-gray-300"
              >
                <ArrowLeft className="h-4 w-4" />
                <span>Back to Results</span>
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => window.print()}
                className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white border-blue-600"
              >
                <Printer className="h-4 w-4" />
                <span>Print PDF</span>
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Info Modal */}
      <FrameworkCoverageInfoModal 
        isOpen={showInfoModal} 
        onClose={() => setShowInfoModal(false)} 
      />

      {/* Main Content - Framework Cards Grid */}
      <div className="flex-1 p-6">
        <div className="grid grid-cols-4 gap-6">
          {FRAMEWORKS.map((framework) => {
            const IconComponent = framework.icon;
            
            // Find the coverage data for this framework from the API response
            const frameworkCoverage = coverageData?.frameworks?.find(
              fw => fw.framework_id === framework.id
            );
            
            // Use real data if available, otherwise use placeholder
            const chartData = frameworkCoverage?.chart_data 
              ? frameworkCoverage.chart_data.map(d => ({
                  category: d.category,
                  inherent: d.inherent,
                  achieved: d.achieved
                }))
              : generatePlaceholderData();
            
            // Check if this framework was selected (from API response)
            const isFrameworkSelected = frameworkCoverage?.is_selected ?? false;
            
            return (
              <Card 
                key={framework.id} 
                className={`flex flex-col relative ${!isFrameworkSelected ? 'opacity-50 bg-gray-100' : ''}`}
              >
                {/* Overlay banner for unselected frameworks */}
                {!isFrameworkSelected && (
                  <div className="absolute inset-0 z-10 flex items-center justify-center pointer-events-none">
                    <div className="bg-gray-700 bg-opacity-90 text-white text-xs font-medium px-4 py-2 rounded-md shadow-lg transform -rotate-6">
                      Framework not selected for this assessment
                    </div>
                  </div>
                )}
                
                <CardHeader className="pb-2">
                  <div className="flex items-start space-x-3">
                    <div 
                      className="p-2 rounded-lg"
                      style={{ backgroundColor: isFrameworkSelected ? `${framework.color}15` : '#E5E7EB' }}
                    >
                      <IconComponent 
                        className="h-5 w-5" 
                        style={{ color: isFrameworkSelected ? framework.color : '#9CA3AF' }}
                      />
                    </div>
                    <div className="flex-1 min-w-0">
                      <CardTitle className={`text-sm font-semibold leading-tight ${isFrameworkSelected ? 'text-gray-900' : 'text-gray-500'}`}>
                        {framework.title}
                      </CardTitle>
                    </div>
                  </div>
                </CardHeader>
                
                <CardContent className="flex-1 flex flex-col">
                  {/* Chart Title */}
                  <div className="text-center mb-2">
                    <span className={`text-xs font-medium ${isFrameworkSelected ? 'text-gray-700' : 'text-gray-400'}`}>
                      Inherent vs Achieved Coverage
                    </span>
                    {frameworkCoverage?.total_controls && (
                      <div className={`text-[10px] ${isFrameworkSelected ? 'text-gray-500' : 'text-gray-400'}`}>
                        Based on {frameworkCoverage.total_controls} total controls
                      </div>
                    )}
                  </div>
                  
                  {/* Grouped Bar Chart */}
                  <div className="flex-1 min-h-[200px]">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart
                        data={chartData}
                        margin={{ top: 10, right: 10, left: -10, bottom: 5 }}
                      >
                        <CartesianGrid strokeDasharray="3 3" vertical={false} />
                        <XAxis 
                          dataKey="category" 
                          tick={{ fontSize: 9, fill: isFrameworkSelected ? '#374151' : '#9CA3AF' }}
                          interval={0}
                          tickLine={false}
                          axisLine={{ stroke: '#E5E7EB' }}
                        />
                        <YAxis 
                          domain={[0, 100]} 
                          tickFormatter={(value) => `${value}%`}
                          tick={{ fontSize: 9, fill: isFrameworkSelected ? '#374151' : '#9CA3AF' }}
                          tickLine={false}
                          axisLine={{ stroke: '#E5E7EB' }}
                          label={{ 
                            value: '% of controls', 
                            angle: -90, 
                            position: 'insideLeft',
                            style: { fontSize: 9, fill: isFrameworkSelected ? '#6B7280' : '#9CA3AF' },
                            offset: 15
                          }}
                        />
                        <Tooltip 
                          formatter={(value, name) => [`${value}%`, name === 'inherent' ? 'Inherent' : 'Achieved']}
                          contentStyle={{ fontSize: 11 }}
                        />
                        <Bar 
                          dataKey="inherent" 
                          fill={isFrameworkSelected ? CHART_COLORS.inherent : '#D1D5DB'}
                          radius={[2, 2, 0, 0]}
                          barSize={20}
                        />
                        <Bar 
                          dataKey="achieved" 
                          fill={isFrameworkSelected ? CHART_COLORS.achieved : '#9CA3AF'}
                          radius={[2, 2, 0, 0]}
                          barSize={20}
                        />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>

                  {/* Legend */}
                  <div className="flex justify-center space-x-4 text-xs text-gray-600 mt-1 mb-3">
                    <div className="flex items-center space-x-1">
                      <div className="w-3 h-3 rounded" style={{ backgroundColor: isFrameworkSelected ? CHART_COLORS.inherent : '#D1D5DB' }}></div>
                      <span className={isFrameworkSelected ? '' : 'text-gray-400'}>Inherent</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <div className="w-3 h-3 rounded" style={{ backgroundColor: isFrameworkSelected ? CHART_COLORS.achieved : '#9CA3AF' }}></div>
                      <span className={isFrameworkSelected ? '' : 'text-gray-400'}>Achieved</span>
                    </div>
                  </div>

                  {/* Coverage Summary */}
                  <div className="pt-2 border-t -mb-2.5">
                    {(() => {
                      const inherentCoverage = frameworkCoverage?.inherent_coverage || {};
                      const achievedCoverage = frameworkCoverage?.achieved_coverage || {};
                      
                      const overallInherent = (inherentCoverage.strong || 0) + (inherentCoverage.moderate || 0);
                      const overallAchieved = (achievedCoverage.strong || 0) + (achievedCoverage.moderate || 0);
                      const confidenceWeighted = Math.max(0, ((achievedCoverage.strong || 0) * 1.0) + ((achievedCoverage.moderate || 0) * 0.3) + ((achievedCoverage.weak || 0) * 0.1) - ((achievedCoverage.none || 0) * 0.1));
                      const coverageGap = overallInherent > 0 ? Math.min(100, Math.max(0, (1 - (confidenceWeighted / overallInherent)) * 100)) : 0;
                      
                      return (
                        <div className={`text-xs pt-1 flex ${isFrameworkSelected ? 'text-gray-700' : 'text-gray-400'}`}>
                          {/* Left Panel */}
                          <div className="flex-1 space-y-1 pr-2">
                            <div className="flex items-center">
                              <span className="font-medium">Overall Inherent:</span>
                              <span className="ml-1">{overallInherent.toFixed(1)}%</span>
                            </div>
                            <div className="flex items-center">
                              <span className="font-medium">Overall Achieved:</span>
                              <span className="ml-1">{overallAchieved.toFixed(1)}%</span>
                            </div>
                          </div>
                          
                          {/* Divider */}
                          <div className={`w-px ${isFrameworkSelected ? 'bg-gray-300' : 'bg-gray-200'} mx-2`}></div>
                          
                          {/* Right Panel */}
                          <div className="flex-1 space-y-1 pl-2">
                            <div className="flex items-center">
                              <span className="font-medium">Confidence-Weighted:</span>
                              <span className="ml-1">{confidenceWeighted.toFixed(1)}%</span>
                            </div>
                            <div className="flex items-center">
                              <span className="font-medium">Coverage Gap:</span>
                              <span className={`ml-1 font-bold ${
                                isFrameworkSelected 
                                  ? coverageGap <= 20 
                                    ? 'text-green-600' 
                                    : coverageGap <= 40 
                                      ? 'text-amber-600' 
                                      : 'text-red-600'
                                  : ''
                              }`}>
                                {coverageGap.toFixed(1)}% {isFrameworkSelected && (
                                  coverageGap <= 20 ? '(LOW)' : coverageGap <= 40 ? '(MODERATE)' : '(HIGH)'
                                )}
                              </span>
                            </div>
                          </div>
                        </div>
                      );
                    })()}
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export default FrameworkCoveragePage;
