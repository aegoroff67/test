import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { toast } from 'sonner';
import { 
  Shield, 
  Plus, 
  Play, 
  CheckCircle2, 
  Clock, 
  BarChart3, 
  FileText, 
  LogOut,
  Settings,
  Building2,
  Trash2,
  Lightbulb,
  Bot
} from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function Dashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [assessments, setAssessments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAssessments();
  }, []);

  const fetchAssessments = async () => {
    try {
      const response = await axios.get(`${API}/assessments`);
      setAssessments(response.data);
    } catch (error) {
      toast.error('Failed to load assessments');
    } finally {
      setLoading(false);
    }
  };

  const createNewAssessment = async () => {
    // Navigate to assessment selector page
    navigate('/assessment-selector');
  };

  const deleteAssessment = async (assessmentId, assessmentName) => {
    // Confirm deletion
    if (!window.confirm(`Are you sure you want to delete "${assessmentName}"? This action cannot be undone.`)) {
      return;
    }

    try {
      await axios.delete(`${API}/assessments/${assessmentId}`);
      toast.success('Assessment deleted successfully');
      // Refresh the assessments list
      fetchAssessments();
    } catch (error) {
      console.error('Error deleting assessment:', error);
      toast.error('Failed to delete assessment');
    }
  };

  const handleLogout = () => {
    logout();
    toast.success('Logged out successfully');
    navigate('/auth');
  };

  const incompleteAssessments = assessments.filter(a => a.status === 'INCOMPLETE');
  const completedAssessments = assessments.filter(a => a.status === 'COMPLETED');

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="loading-spinner w-12 h-12 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-bg">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <div className="flex items-center space-x-3">
              <div className="bg-teal-600 p-2 rounded-lg">
                <Shield className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">AM AI SAFE</h1>
                <p className="text-xs text-teal-600 font-medium">EMPOWERING TRUST IN AI</p>
              </div>
            </div>

            {/* User Menu */}
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <p className="text-sm font-medium text-gray-900">{user?.name}</p>
                <p className="text-xs text-gray-500">{user?.organization_name}</p>
              </div>
              <div className="flex items-center space-x-2">
                <Button 
                  variant="ghost" 
                  size="sm" 
                  className="p-2"
                  data-testid="settings-btn"
                >
                  <Settings className="h-4 w-4" />
                </Button>
                <Button 
                  variant="ghost" 
                  size="sm" 
                  onClick={handleLogout}
                  className="p-2 text-red-600 hover:text-red-700 hover:bg-red-50"
                  data-testid="logout-btn"
                >
                  <LogOut className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Welcome back, {user?.name?.split(' ')[0]}!
              </h1>
              <p className="text-lg text-gray-600 flex items-center space-x-2">
                <Building2 className="h-5 w-5" />
                <span>{user?.organization_name} • {user?.industry}</span>
              </p>
            </div>
            <Button 
              onClick={createNewAssessment}
              className="bg-teal-600 hover:bg-teal-700 btn-hover"
              data-testid="start-new-assessment-btn"
            >
              <div className="flex items-center space-x-2">
                <Plus className="h-4 w-4" />
                <span>Start New Assessment</span>
              </div>
            </Button>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card className="card-hover">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Total Assessments</p>
                  <p className="text-3xl font-bold text-gray-900" data-testid="total-assessments-count">
                    {assessments.length}
                  </p>
                </div>
                <div className="bg-blue-100 p-3 rounded-full">
                  <BarChart3 className="h-6 w-6 text-blue-600" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="card-hover">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">In Progress</p>
                  <p className="text-3xl font-bold text-orange-600" data-testid="incomplete-assessments-count">
                    {incompleteAssessments.length}
                  </p>
                </div>
                <div className="bg-orange-100 p-3 rounded-full">
                  <Clock className="h-6 w-6 text-orange-600" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="card-hover">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Completed</p>
                  <p className="text-3xl font-bold text-green-600" data-testid="completed-assessments-count">
                    {completedAssessments.length}
                  </p>
                </div>
                <div className="bg-green-100 p-3 rounded-full">
                  <CheckCircle2 className="h-6 w-6 text-green-600" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Assessments Sections */}
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Incomplete Assessments */}
          <div>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900 flex items-center space-x-2">
                <Clock className="h-5 w-5 text-orange-500" />
                <span>In Progress</span>
              </h2>
              {incompleteAssessments.length > 0 && (
                <Badge variant="outline" className="text-orange-600 border-orange-200">
                  {incompleteAssessments.length} active
                </Badge>
              )}
            </div>

            <div className="space-y-4" data-testid="incomplete-assessments-list">
              {incompleteAssessments.length === 0 ? (
                <Card className="card-hover">
                  <CardContent className="p-8 text-center">
                    <div className="bg-gray-100 p-4 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                      <Play className="h-8 w-8 text-gray-400" />
                    </div>
                    <h3 className="text-lg font-medium text-gray-900 mb-2">
                      No assessments in progress
                    </h3>
                    <p className="text-gray-600 mb-4">
                      Start your first AI governance assessment to evaluate your organization's AI maturity.
                    </p>
                    <Button 
                      onClick={createNewAssessment}
                      className="bg-teal-600 hover:bg-teal-700"
                      data-testid="start-first-assessment-btn"
                    >
                      <Plus className="h-4 w-4 mr-2" />
                      Start Assessment
                    </Button>
                  </CardContent>
                </Card>
              ) : (
                incompleteAssessments.map((assessment) => (
                  <Card key={assessment.id} className="card-hover">
                    <CardContent className="p-6">
                      <div className="flex items-center justify-between mb-4">
                        <div>
                          <h3 className="font-medium text-gray-900">{assessment.name}</h3>
                          <p className="text-sm text-gray-500">
                            Started {new Date(assessment.started_at).toLocaleDateString()}
                          </p>
                        </div>
                        <Badge className="bg-orange-100 text-orange-800">
                          In Progress
                        </Badge>
                      </div>
                      
                      <div className="mb-4">
                        <div className="flex justify-between text-sm mb-2">
                          <span className="text-gray-600">Progress</span>
                          <span className="font-medium">
                            {assessment.progress}/{assessment.total_questions}
                          </span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-teal-600 h-2 rounded-full progress-bar"
                            style={{
                              width: `${(assessment.progress / assessment.total_questions) * 100}%`
                            }}
                          ></div>
                        </div>
                      </div>
                      
                      <div className="flex gap-2">
                        <Button 
                          onClick={() => navigate(`/assessment/${assessment.id}`)}
                          className="flex-1 bg-teal-600 hover:bg-teal-700"
                          data-testid={`resume-assessment-${assessment.id}`}
                        >
                          <Play className="h-4 w-4 mr-2" />
                          Resume Assessment
                        </Button>
                        <Button 
                          onClick={(e) => {
                            e.stopPropagation();
                            deleteAssessment(assessment.id, assessment.name);
                          }}
                          variant="outline"
                          className="text-red-600 hover:text-red-700 hover:bg-red-50 border-red-200"
                          data-testid={`delete-assessment-${assessment.id}`}
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))
              )}
            </div>
          </div>

          {/* Completed Assessments */}
          <div>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900 flex items-center space-x-2">
                <CheckCircle2 className="h-5 w-5 text-green-500" />
                <span>Completed</span>
              </h2>
              {completedAssessments.length > 0 && (
                <Badge variant="outline" className="text-green-600 border-green-200">
                  {completedAssessments.length} reports
                </Badge>
              )}
            </div>

            <div className="space-y-4" data-testid="completed-assessments-list">
              {completedAssessments.length === 0 ? (
                <Card className="card-hover">
                  <CardContent className="p-8 text-center">
                    <div className="bg-gray-100 p-4 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                      <FileText className="h-8 w-8 text-gray-400" />
                    </div>
                    <h3 className="text-lg font-medium text-gray-900 mb-2">
                      No completed assessments
                    </h3>
                    <p className="text-gray-600">
                      Complete an assessment to view results and generate reports.
                    </p>
                  </CardContent>
                </Card>
              ) : (
                completedAssessments.map((assessment) => (
                  <Card key={assessment.id} className="card-hover">
                    <CardContent className="p-6">
                      <div className="flex items-center justify-between mb-4">
                        <div>
                          <h3 className="font-medium text-gray-900">{assessment.name}</h3>
                          <p className="text-sm text-gray-500">
                            Completed {new Date(assessment.completed_at).toLocaleDateString()}
                          </p>
                        </div>
                        <Badge className="bg-green-100 text-green-800">
                          Complete
                        </Badge>
                      </div>
                      
                      <div className="flex gap-2">
                        <Button 
                          onClick={() => navigate(`/results/${assessment.id}`)}
                          className="flex-1 bg-blue-600 hover:bg-blue-700"
                          data-testid={`view-results-${assessment.id}`}
                        >
                          <BarChart3 className="h-4 w-4 mr-2" />
                          View Results
                        </Button>
                        <Button 
                          onClick={(e) => {
                            e.stopPropagation();
                            deleteAssessment(assessment.id, assessment.name);
                          }}
                          variant="outline"
                          className="text-red-600 hover:text-red-700 hover:bg-red-50 border-red-200"
                          data-testid={`delete-assessment-${assessment.id}`}
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default Dashboard;
