import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { CheckCircle2, Circle, X } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function AssessmentStatusView({ assessmentId, assessmentType, assessmentName, onClose, onQuestionClick }) {
  const [statusData, setStatusData] = useState(null);
  const [loading, setLoading] = useState(true);
  
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
    fetchStatusData();
  }, [assessmentId]);

  const fetchStatusData = async () => {
    try {
      const response = await axios.get(`${API}/assessments/${assessmentId}/status`);
      setStatusData(response.data);
    } catch (error) {
      console.error('Failed to fetch status data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
        <Card className="w-full max-w-4xl max-h-[80vh] overflow-auto">
          <CardContent className="p-8 text-center">
            <div className="loading-spinner w-8 h-8 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading assessment status...</p>
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
          <div className="flex justify-between items-center">
            <div>
              <CardTitle className="text-xl">{getAssessmentTypeTitle()}</CardTitle>
              <p className="text-sm text-gray-600 mt-1">
                {statusData.answered_questions} of {statusData.total_questions} questions completed 
                ({statusData.completion_percentage}%)
              </p>
            </div>
            <Button 
              variant="ghost" 
              onClick={onClose}
              data-testid="close-status-view-btn"
              className="text-gray-400 hover:text-gray-600"
            >
              <X className="h-5 w-5" />
            </Button>
          </div>
          
          {/* Progress Bar */}
          <div className="w-full bg-gray-200 rounded-full h-3 mt-4">
            <div 
              className="bg-teal-600 h-3 rounded-full progress-bar"
              style={{ width: `${statusData.completion_percentage}%` }}
            ></div>
          </div>
        </CardHeader>
        
        <CardContent className="flex-1 overflow-hidden">
          {/* Compact grid layout - all domains in one view without scrolling */}
          <div className={`grid gap-2 h-full ${
            statusData.status_overview.length === 10 ? 'grid-cols-10' : 
            statusData.status_overview.length === 8 ? 'grid-cols-8' : 
            'grid-cols-11'
          }`}>
            {statusData.status_overview.map((domain) => {
              const domainAnswered = domain.questions.filter(q => q.answered).length;
              const domainTotal = domain.questions.length;
              
              return (
                <div key={domain.domain_name} className="flex flex-col">
                  {/* Domain Header - Fixed height to ensure alignment */}
                  <div className="mb-2 text-center h-20 flex flex-col justify-start items-center">
                    <div className="text-xs font-semibold text-gray-900 mb-1 break-words" title={domain.domain_name}>
                      {domain.domain_name}
                    </div>
                    <Badge 
                      variant={domainAnswered === domainTotal ? "default" : "secondary"}
                      className={`text-xs ${domainAnswered === domainTotal ? "bg-green-100 text-green-800" : ""}`}
                    >
                      {domainAnswered}/{domainTotal}
                    </Badge>
                  </div>
                  
                  {/* Questions Grid */}
                  <div className="flex-1 space-y-1">
                    {domain.questions.map((question) => {
                      const isPendingReview = question.review_status === 'PENDING_REVIEW';
                      const bgColor = isPendingReview 
                        ? 'bg-blue-100 border-blue-300 text-blue-800 hover:bg-blue-200'
                        : question.answered
                          ? 'bg-green-100 border-green-300 text-green-800 hover:bg-green-200'
                          : 'bg-gray-50 border-gray-200 text-gray-500 hover:bg-gray-100';
                      
                      return (
                      <div
                        key={question.question_id}
                        className={`p-2 rounded text-center text-xs font-medium border transition-all cursor-pointer hover:shadow-md ${bgColor}`}
                        title={`${question.question_code} - ${isPendingReview ? 'Pending Review 📝' : question.answered ? 'Answered ✓' : 'Not answered'} - Click to navigate`}
                        data-testid={`status-${question.question_code}`}
                        onClick={() => onQuestionClick && onQuestionClick(question.question_id)}
                      >
                        <div className="flex items-center justify-center space-x-1">
                          {question.answered ? (
                            <CheckCircle2 className={`h-3 w-3 ${isPendingReview ? 'text-blue-600' : 'text-green-600'}`} />
                          ) : (
                            <Circle className="h-3 w-3 text-gray-400" />
                          )}
                        </div>
                        <div className="mt-1 text-xs font-semibold">
                          {question.question_code}
                        </div>
                      </div>
                      );
                    })}
                  </div>
                </div>
              );
            })}
          </div>
          
          {/* Summary at bottom */}
          <div className="mt-4 p-3 bg-teal-50 rounded-lg border border-teal-200">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-medium text-teal-900">Overall Progress</h3>
                <p className="text-sm text-teal-700">
                  {statusData.answered_questions} of {statusData.total_questions} questions completed
                </p>
              </div>
              <div className="text-right">
                <div className="text-xl font-bold text-teal-900">
                  {statusData.completion_percentage}%
                </div>
                <div className="text-xs text-teal-700">Complete</div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default AssessmentStatusView;