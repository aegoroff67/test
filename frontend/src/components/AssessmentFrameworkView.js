import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { X, Info } from 'lucide-react';

// Import all framework alignment data
import nistAlignmentData from '../data/nistAlignmentData.json';
import iso42001AlignmentData from '../data/iso42001AlignmentData.json';
import auEthicsAlignmentData from '../data/auEthicsAlignmentData.json';
import auGuidanceAlignmentData from '../data/auGuidanceAlignmentData.json';
import auAssuranceAlignmentData from '../data/auAssuranceAlignmentData.json';
import singaporeMafAlignmentData from '../data/singaporeMafAlignmentData.json';
import oecdPrinciplesAlignmentData from '../data/oecdPrinciplesAlignmentData.json';
import euAiActAlignmentData from '../data/euAiActAlignmentData.json';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Framework configuration
const FRAMEWORKS = [
  {
    id: 'iso42001',
    name: 'ISO/IEC 42001 (2023)',
    systemName: 'AS ISO/IEC 42001:2023',
    data: iso42001AlignmentData,
    color: 'teal'
  },
  {
    id: 'auEthics',
    name: 'Australian AI Ethics Principles (2024)',
    systemName: 'Australian AI Ethics Principles (2024)',
    data: auEthicsAlignmentData,
    color: 'green'
  },
  {
    id: 'auGuidance',
    name: 'Australian Guidance for AI Adoption (2025)',
    systemName: 'Australian Guidance for AI Adoption (2025)',
    data: auGuidanceAlignmentData,
    color: 'blue'
  },
  {
    id: 'auAssurance',
    name: 'AU National Framework for the Assurance of AI in Gov (2024)',
    systemName: 'Australian National Framework for the Assurance of AI in Government (2024)',
    data: auAssuranceAlignmentData,
    color: 'orange'
  },
  {
    id: 'euAiAct',
    name: 'EU AI Act (2024)',
    systemName: 'EU AI Act (2024 final)',
    data: euAiActAlignmentData,
    color: 'purple'
  },
  {
    id: 'nist',
    name: 'NIST AI RMF (2023)',
    systemName: 'NIST AI RMF (2023)',
    data: nistAlignmentData,
    color: 'indigo'
  },
  {
    id: 'oecdPrinciples',
    name: 'OECD Principles (2019)',
    systemName: 'OECD Principles (2019)',
    data: oecdPrinciplesAlignmentData,
    color: 'slate'
  },
  {
    id: 'singaporeMaf',
    name: 'Singapore MAF (2024)',
    systemName: 'Singapore MAF (2024)',
    data: singaporeMafAlignmentData,
    color: 'rose'
  }
];

function AssessmentFrameworkView({ assessmentId, assessmentType, onClose, onQuestionClick }) {
  const [statusData, setStatusData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedFramework, setSelectedFramework] = useState(null);
  const [availableFrameworks, setAvailableFrameworks] = useState([]);
  const [showStatsTooltip, setShowStatsTooltip] = useState(false);

  // Get assessment type display name
  const getAssessmentTypeTitle = () => {
    switch(assessmentType) {
      case 'Awareness':
        return 'AI Awareness & Foundations Assessment';
      case 'Readiness':
        return 'AI Readiness Assessment';
      case 'Orgwide':
        return 'Organisation-wide AI Maturity Assessment';
      case 'System':
      default:
        return 'AI System Maturity Assessment';
    }
  };

  useEffect(() => {
    fetchData();
  }, [assessmentId]);

  const fetchData = async () => {
    try {
      // Fetch status data for questions
      const statusResponse = await axios.get(`${API}/assessments/${assessmentId}/status`);
      setStatusData(statusResponse.data);

      // Fetch assessment to get selected frameworks
      const assessmentResponse = await axios.get(`${API}/assessments/${assessmentId}`);
      const systemInfo = assessmentResponse.data.system_info || {};
      const selectedFrameworkNames = systemInfo.frameworks || [];

      // Filter available frameworks based on what's selected in the assessment
      const available = FRAMEWORKS.filter(fw => 
        selectedFrameworkNames.includes(fw.systemName)
      );
      setAvailableFrameworks(available);

      // Auto-select first available framework
      if (available.length > 0) {
        setSelectedFramework(available[0].id);
      }
    } catch (error) {
      console.error('Failed to fetch data:', error);
    } finally {
      setLoading(false);
    }
  };

  // Get alignment color for a question
  const getAlignmentColor = (questionCode) => {
    if (!selectedFramework) return 'bg-gray-100 border-gray-200 text-gray-500';

    const framework = FRAMEWORKS.find(fw => fw.id === selectedFramework);
    if (!framework) return 'bg-gray-100 border-gray-200 text-gray-500';

    const alignmentData = framework.data[questionCode];
    if (!alignmentData) {
      return 'bg-gray-100 border-gray-200 text-gray-500 hover:bg-gray-150';
    }

    const alignmentType = alignmentData.alignmentType;
    
    // Full alignment
    if (alignmentType === 'Fully Aligns' || alignmentType === 'Direct alignment') {
      return 'bg-green-100 border-green-300 text-green-800 hover:bg-green-200';
    }
    
    // Partial alignment
    if (alignmentType === 'Partially Aligns' || alignmentType === 'Related alignment') {
      return 'bg-yellow-100 border-yellow-300 text-yellow-800 hover:bg-yellow-200';
    }

    // No alignment
    return 'bg-gray-100 border-gray-200 text-gray-500 hover:bg-gray-150';
  };

  // Get alignment icon for a question
  const getAlignmentIcon = (questionCode) => {
    if (!selectedFramework) return '○';

    const framework = FRAMEWORKS.find(fw => fw.id === selectedFramework);
    if (!framework) return '○';

    const alignmentData = framework.data[questionCode];
    if (!alignmentData) return '○';

    const alignmentType = alignmentData.alignmentType;
    
    if (alignmentType === 'Fully Aligns' || alignmentType === 'Direct alignment') {
      return '●';
    }
    
    if (alignmentType === 'Partially Aligns' || alignmentType === 'Related alignment') {
      return '◐';
    }

    return '○';
  };

  // Calculate alignment statistics for selected framework
  const getAlignmentStats = () => {
    if (!selectedFramework || !statusData) return null;

    const framework = FRAMEWORKS.find(fw => fw.id === selectedFramework);
    if (!framework) return null;

    let fullyAligned = 0;
    let partiallyAligned = 0;
    let noAlignment = 0;
    let total = 0;

    // Count alignments across all questions
    statusData.status_overview.forEach(domain => {
      domain.questions.forEach(question => {
        total++;
        const alignmentData = framework.data[question.question_code];
        
        if (!alignmentData) {
          noAlignment++;
        } else {
          const alignmentType = alignmentData.alignmentType;
          
          if (alignmentType === 'Fully Aligns' || alignmentType === 'Direct alignment') {
            fullyAligned++;
          } else if (alignmentType === 'Partially Aligns' || alignmentType === 'Related alignment') {
            partiallyAligned++;
          } else {
            noAlignment++;
          }
        }
      });
    });

    return {
      fullyAligned: total > 0 ? Math.round((fullyAligned / total) * 100) : 0,
      partiallyAligned: total > 0 ? Math.round((partiallyAligned / total) * 100) : 0,
      noAlignment: total > 0 ? Math.round((noAlignment / total) * 100) : 0,
      total
    };
  };

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
        <Card className="w-full max-w-4xl max-h-[80vh] overflow-auto">
          <CardContent className="p-8 text-center">
            <div className="loading-spinner w-8 h-8 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading framework alignment...</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!statusData) {
    return null;
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-7xl h-[95vh] flex flex-col">
        <CardHeader>
          <div className="flex justify-between items-start gap-4">
            <div className="flex-1">
              <CardTitle className="text-xl">{getAssessmentTypeTitle()} - Framework Alignment</CardTitle>
              <p className="text-sm text-gray-600 mt-1">
                View how questions align with selected frameworks
              </p>
            </div>
            
            {/* Legend - Moved to header */}
            <div className="flex items-center gap-4 text-xs bg-gray-50 px-4 py-2 rounded-lg border border-gray-200">
              <div className="flex items-center gap-2">
                <span className="text-lg text-green-600 leading-none flex items-center">●</span>
                <span className="text-gray-700 font-medium">Fully Aligns</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-lg text-yellow-600 leading-none flex items-center">◐</span>
                <span className="text-gray-700 font-medium">Partially Aligns</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-lg text-gray-400 leading-none flex items-center">○</span>
                <span className="text-gray-700 font-medium">No Alignment</span>
              </div>
            </div>

            <Button 
              variant="ghost" 
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 flex-shrink-0"
            >
              <X className="h-5 w-5" />
            </Button>
          </div>
        </CardHeader>
        
        <CardContent className="flex-1 overflow-auto">
          {/* Questions Grid */}
          <div className={`grid gap-2 mb-6 ${
            statusData.status_overview.length === 10 ? 'grid-cols-10' : 
            statusData.status_overview.length === 8 ? 'grid-cols-8' : 
            'grid-cols-11'
          }`}>
            {statusData.status_overview.map((domain) => (
              <div key={domain.domain_name} className="flex flex-col">
                {/* Domain Header */}
                <div className="mb-2 text-center h-20 flex flex-col justify-start items-center">
                  <div className="text-sm font-semibold text-gray-900 mb-1 break-words" title={domain.domain_name}>
                    {domain.domain_name}
                  </div>
                  <Badge variant="secondary" className="text-xs">
                    {domain.questions.length} Questions
                  </Badge>
                </div>
                
                {/* Questions */}
                <div className="flex-1 space-y-1">
                  {domain.questions.map((question) => {
                    const colorClass = getAlignmentColor(question.question_code);
                    const icon = getAlignmentIcon(question.question_code);
                    // Use larger size for filled circle to match visual size of hollow circles
                    const iconSizeClass = icon === '●' ? 'text-lg' : 'text-base';
                    
                    return (
                      <div
                        key={question.question_id}
                        className={`p-2 rounded text-center text-xs font-medium border transition-all cursor-pointer hover:shadow-md ${colorClass}`}
                        style={{ maxHeight: '50px' }}
                        title={`${question.question_code} - Click to navigate`}
                        onClick={() => onQuestionClick && onQuestionClick(question.question_id)}
                      >
                        <div className="flex items-center justify-center space-x-1">
                          <span className={`${iconSizeClass} leading-none`}>{icon}</span>
                        </div>
                        <div className="mt-1 text-xs font-semibold">
                          {question.question_code}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>

          {/* Framework Selection - Radio buttons underneath the matrix */}
          <div className="mt-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-semibold text-gray-900">
                Select Framework to View Alignment:
              </h3>
              
              {/* Statistics Tooltip */}
              {selectedFramework && (
                <div className="relative">
                  <button
                    className="flex items-center gap-2 text-xs text-blue-600 hover:text-blue-800 font-medium transition-colors"
                    onMouseEnter={() => setShowStatsTooltip(true)}
                    onMouseLeave={() => setShowStatsTooltip(false)}
                  >
                    <Info className="h-4 w-4" />
                    <span>Alignment Statistics</span>
                  </button>
                  
                  {showStatsTooltip && (() => {
                    const stats = getAlignmentStats();
                    return stats ? (
                      <div className="absolute right-0 top-full mt-2 z-50 w-64 bg-white border-2 border-blue-500 rounded-lg shadow-xl p-4">
                        <div className="space-y-2">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                              <span className="text-lg text-green-600 leading-none flex items-center">●</span>
                              <span className="text-sm font-medium text-gray-700">Fully Aligns</span>
                            </div>
                            <span className="text-lg font-bold text-green-600">{stats.fullyAligned}%</span>
                          </div>
                          
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                              <span className="text-lg text-yellow-600 leading-none flex items-center">◐</span>
                              <span className="text-sm font-medium text-gray-700">Partially Aligns</span>
                            </div>
                            <span className="text-lg font-bold text-yellow-600">{stats.partiallyAligned}%</span>
                          </div>
                          
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                              <span className="text-lg text-gray-400 leading-none flex items-center">○</span>
                              <span className="text-sm font-medium text-gray-700">No Alignment</span>
                            </div>
                            <span className="text-lg font-bold text-gray-500">{stats.noAlignment}%</span>
                          </div>
                          
                          <div className="mt-3 pt-3 border-t border-gray-200">
                            <div className="text-xs text-gray-600 text-center">
                              Total Questions: {stats.total}
                            </div>
                          </div>
                        </div>
                      </div>
                    ) : null;
                  })()}
                </div>
              )}
            </div>
            
            {availableFrameworks.length === 0 ? (
              <p className="text-sm text-gray-600 italic">
                No frameworks selected for this assessment. Please select frameworks in the pre-assessment form.
              </p>
            ) : (
              <div className="grid grid-cols-4 gap-3">
                {availableFrameworks.map((framework) => (
                  <label
                    key={framework.id}
                    className="flex items-center space-x-3 p-3 rounded-lg border-2 cursor-pointer transition-all hover:bg-white hover:shadow-sm"
                    style={{
                      borderColor: selectedFramework === framework.id ? '#3b82f6' : '#e5e7eb',
                      backgroundColor: selectedFramework === framework.id ? '#eff6ff' : 'transparent'
                    }}
                  >
                    <input
                      type="radio"
                      name="framework"
                      value={framework.id}
                      checked={selectedFramework === framework.id}
                      onChange={() => setSelectedFramework(framework.id)}
                      className="h-4 w-4 text-blue-600 focus:ring-blue-500 flex-shrink-0"
                    />
                    <span className="text-sm font-medium text-gray-900">
                      {framework.name}
                    </span>
                  </label>
                ))}
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default AssessmentFrameworkView;
