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
  FileText,
  CheckCircle2,
  Shield,
  Clock
} from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function FairaResultsPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [assessment, setAssessment] = useState(null);
  const [fairaData, setFairaData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [generatingPDF, setGeneratingPDF] = useState(false);

  useEffect(() => {
    fetchResults();
  }, [id]);

  const fetchResults = async () => {
    try {
      const response = await axios.get(`${API}/assessments/${id}`);
      setAssessment(response.data);
      setFairaData(response.data.faira_form || {});
      setLoading(false);
    } catch (error) {
      console.error('Error fetching FAIRA results:', error);
      toast.error('Failed to load assessment results');
      setLoading(false);
    }
  };

  const handleGeneratePDF = async () => {
    setGeneratingPDF(true);
    try {
      const response = await axios.get(`${API}/assessments/${id}/faira-pdf`, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `FAIRA_Assessment_${assessment.name}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      
      toast.success('PDF report generated successfully');
    } catch (error) {
      console.error('Error generating PDF:', error);
      toast.error('Failed to generate PDF report');
    } finally {
      setGeneratingPDF(false);
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Logo />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">FAIRA Risk Assessment</h1>
                <p className="text-sm text-gray-600">Results Summary</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <Button
                variant="outline"
                onClick={() => navigate('/dashboard')}
                className="flex items-center space-x-2"
              >
                <ArrowLeft className="h-4 w-4" />
                <span>Dashboard</span>
              </Button>
              <Button
                onClick={handleGeneratePDF}
                disabled={generatingPDF}
                className="flex items-center space-x-2 bg-teal-600 hover:bg-teal-700"
              >
                <Download className="h-4 w-4" />
                <span>{generatingPDF ? 'Generating...' : 'Download PDF'}</span>
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Assessment Overview */}
        <Card className="mb-6">
          <CardHeader className="bg-orange-50 border-b border-orange-100">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <Shield className="h-6 w-6 text-orange-600" />
                <CardTitle className="text-xl">Assessment Overview</CardTitle>
              </div>
              <Badge className="bg-green-100 text-green-800 flex items-center space-x-1">
                <CheckCircle2 className="h-4 w-4" />
                <span>Completed</span>
              </Badge>
            </div>
          </CardHeader>
          <CardContent className="pt-6">
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <h3 className="font-semibold text-gray-900 mb-3">Assessment Information</h3>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Assessment Name:</span>
                    <span className="font-medium">{assessment.name}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">AI System Name:</span>
                    <span className="font-medium">{fairaData.ai_system_name || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">System Version:</span>
                    <span className="font-medium">{fairaData.ai_system_version || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Business Unit:</span>
                    <span className="font-medium">{fairaData.business_unit || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">System Owner:</span>
                    <span className="font-medium">{fairaData.system_owner_name || 'N/A'}</span>
                  </div>
                </div>
              </div>
              
              <div>
                <h3 className="font-semibold text-gray-900 mb-3">Assessor Information</h3>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Assessor Name:</span>
                    <span className="font-medium">{fairaData.assessor_name || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Role/Title:</span>
                    <span className="font-medium">{fairaData.assessor_role || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Branch/Division:</span>
                    <span className="font-medium">{fairaData.assessor_branch || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Completed Date:</span>
                    <span className="font-medium">
                      {assessment.completed_at 
                        ? new Date(assessment.completed_at).toLocaleDateString() 
                        : 'N/A'
                      }
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Summary Statistics - Placeholder */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <FileText className="h-5 w-5 text-teal-600" />
              <span>Assessment Summary</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-center">
              <Clock className="h-8 w-8 text-blue-600 mx-auto mb-2" />
              <p className="text-gray-700 font-medium">Detailed Analysis Coming Soon</p>
              <p className="text-sm text-gray-600 mt-1">
                This section will display comprehensive risk analysis, recommendations, and visualizations based on your FAIRA assessment responses.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Declaration */}
        {fairaData.declaration_confirmed && (
          <Card>
            <CardHeader>
              <CardTitle>Declaration</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-start space-x-2">
                  <CheckCircle2 className="h-5 w-5 text-green-600 mt-0.5" />
                  <p className="text-sm text-gray-700">
                    I certify that all information provided in this FAIRA assessment is accurate and complete to the best of my knowledge.
                  </p>
                </div>
                <div className="pl-7 space-y-1 text-sm">
                  <div>
                    <span className="text-gray-600">Declared by:</span>{' '}
                    <span className="font-medium">{fairaData.declaration_name || fairaData.assessor_name}</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Date:</span>{' '}
                    <span className="font-medium">{fairaData.declaration_date || 'N/A'}</span>
                  </div>
                  {fairaData.declaration_role && (
                    <div>
                      <span className="text-gray-600">Role:</span>{' '}
                      <span className="font-medium">{fairaData.declaration_role}</span>
                    </div>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        )}
      </main>
    </div>
  );
}

export default FairaResultsPage;
