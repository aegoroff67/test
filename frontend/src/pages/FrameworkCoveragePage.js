import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { toast } from 'sonner';
import Logo from '../components/Logo';
import { 
  ArrowLeft, 
  BarChart3,
  ExternalLink,
  Shield,
  Globe,
  Building2,
  Scale,
  FileCheck,
  Layers,
  BookOpen,
  Award
} from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

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

// Placeholder data for charts
const generatePlaceholderData = () => [
  { name: 'Inherent', value: 75, fill: '#3B82F6' },
  { name: 'Achieved', value: 45, fill: '#10B981' }
];

function FrameworkCoveragePage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [assessment, setAssessment] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAssessment = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`${API}/assessments/${id}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        setAssessment(response.data);
      } catch (error) {
        console.error('Error fetching assessment:', error);
        toast.error('Failed to load assessment data');
      } finally {
        setLoading(false);
      }
    };

    fetchAssessment();
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
        <div className="px-6 py-4">
          {/* Header Row */}
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-4">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => navigate(`/results/${id}`)}
                className="flex items-center space-x-2"
              >
                <ArrowLeft className="h-4 w-4" />
                <span>Back to Results</span>
              </Button>
              <div className="h-6 w-px bg-gray-300" />
              <Logo size="sm" />
            </div>
            
            <div className="flex items-center space-x-3">
              <span className="text-sm text-gray-500">
                {assessment?.name || 'Assessment'}
              </span>
            </div>
          </div>

          {/* Title and Subtitle Section */}
          <div className="max-w-4xl">
            <h1 className="text-2xl font-bold text-gray-900 mb-2">
              Framework Coverage Overview
            </h1>
            <p className="text-sm text-gray-600 leading-relaxed">
              This view shows the extent to which AM AI SAFE covers the controls within selected AI governance frameworks, 
              based on how frequently each framework control is addressed by one or more AM AI SAFE questions. It compares 
              the coverage provided by design (<span className="font-semibold text-blue-600">Inherent Coverage</span>) with 
              the coverage actually achieved based on assessment results (<span className="font-semibold text-green-600">Achieved Coverage</span>).
            </p>
          </div>
        </div>
      </div>

      {/* Main Content - Framework Cards Grid */}
      <div className="flex-1 p-6">
        <div className="grid grid-cols-4 gap-6">
          {FRAMEWORKS.map((framework) => {
            const IconComponent = framework.icon;
            const chartData = generatePlaceholderData();
            
            return (
              <Card key={framework.id} className="flex flex-col">
                <CardHeader className="pb-2">
                  <div className="flex items-start space-x-3">
                    <div 
                      className="p-2 rounded-lg"
                      style={{ backgroundColor: `${framework.color}15` }}
                    >
                      <IconComponent 
                        className="h-5 w-5" 
                        style={{ color: framework.color }}
                      />
                    </div>
                    <div className="flex-1 min-w-0">
                      <CardTitle className="text-sm font-semibold text-gray-900 leading-tight">
                        {framework.title}
                      </CardTitle>
                    </div>
                  </div>
                </CardHeader>
                
                <CardContent className="flex-1 flex flex-col">
                  {/* Placeholder Bar Chart */}
                  <div className="flex-1 min-h-[180px]">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart
                        data={chartData}
                        layout="vertical"
                        margin={{ top: 10, right: 30, left: 10, bottom: 10 }}
                      >
                        <CartesianGrid strokeDasharray="3 3" horizontal={true} vertical={false} />
                        <XAxis 
                          type="number" 
                          domain={[0, 100]} 
                          tickFormatter={(value) => `${value}%`}
                          tick={{ fontSize: 10 }}
                        />
                        <YAxis 
                          type="category" 
                          dataKey="name" 
                          tick={{ fontSize: 11 }}
                          width={60}
                        />
                        <Tooltip 
                          formatter={(value) => [`${value}%`, 'Coverage']}
                          contentStyle={{ fontSize: 12 }}
                        />
                        <Bar 
                          dataKey="value" 
                          radius={[0, 4, 4, 0]}
                          barSize={24}
                        >
                          {chartData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.fill} />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>

                  {/* Legend */}
                  <div className="flex justify-center space-x-4 text-xs text-gray-600 mt-2 mb-3">
                    <div className="flex items-center space-x-1">
                      <div className="w-3 h-3 rounded bg-blue-500"></div>
                      <span>Inherent</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <div className="w-3 h-3 rounded bg-green-500"></div>
                      <span>Achieved</span>
                    </div>
                  </div>

                  {/* View Details Link */}
                  <div className="pt-2 border-t">
                    <button 
                      className="w-full text-sm text-blue-600 hover:text-blue-800 font-medium flex items-center justify-center space-x-1 py-1 transition-colors"
                      onClick={() => {
                        // Placeholder for future navigation
                        toast.info(`${framework.title} details coming soon`);
                      }}
                    >
                      <span>View details</span>
                      <ExternalLink className="h-3 w-3" />
                    </button>
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
