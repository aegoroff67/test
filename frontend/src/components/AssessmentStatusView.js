import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { CheckCircle2, Circle, X } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function AssessmentStatusView({ assessmentId, onClose }) {
  const [statusData, setStatusData] = useState(null);
  const [loading, setLoading] = useState(true);

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
      <Card className="w-full max-w-6xl max-h-[80vh] overflow-auto">
        <CardHeader>
          <div className="flex justify-between items-center">
            <div>
              <CardTitle className="text-xl">Assessment Progress Overview</CardTitle>
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
        
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {statusData.status_overview.map((domain) => {
              const domainAnswered = domain.questions.filter(q => q.answered).length;
              const domainTotal = domain.questions.length;
              const domainPercentage = (domainAnswered / domainTotal) * 100;
              
              return (
                <Card key={domain.domain_name} className="border-2">
                  <CardHeader className="pb-3">
                    <div className="flex justify-between items-start">
                      <CardTitle className="text-base font-semibold text-gray-900">
                        {domain.domain_name}
                      </CardTitle>
                      <Badge 
                        variant={domainAnswered === domainTotal ? "default" : "secondary"}
                        className={domainAnswered === domainTotal ? "bg-green-100 text-green-800" : ""}
                      >
                        {domainAnswered}/{domainTotal}
                      </Badge>
                    </div>
                    
                    {/* Domain Progress Bar */}
                    <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                      <div 
                        className={`h-2 rounded-full progress-bar ${
                          domainAnswered === domainTotal ? 'bg-green-600' : 'bg-teal-600'
                        }`}
                        style={{ width: `${domainPercentage}%` }}
                      ></div>
                    </div>
                  </CardHeader>
                  
                  <CardContent className="pt-0">
                    <div className="grid grid-cols-4 gap-2">
                      {domain.questions.map((question) => (
                        <div
                          key={question.question_id}
                          className={`p-2 rounded-lg border text-center text-xs font-medium transition-all ${
                            question.answered
                              ? 'bg-green-50 border-green-200 text-green-700'
                              : 'bg-gray-50 border-gray-200 text-gray-500'
                          }`}
                          title={`${question.question_code} - ${question.answered ? 'Answered' : 'Not answered'}`}
                          data-testid={`status-${question.question_code}`}
                        >
                          <div className="flex items-center justify-center space-x-1">
                            {question.answered ? (
                              <CheckCircle2 className="h-3 w-3" />
                            ) : (
                              <Circle className="h-3 w-3" />
                            )}
                            <span>{question.question_code}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
          
          {/* Summary */}
          <div className="mt-6 p-4 bg-teal-50 rounded-lg border border-teal-200">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-medium text-teal-900">Overall Progress</h3>
                <p className="text-sm text-teal-700">
                  Complete {statusData.total_questions - statusData.answered_questions} more questions to finish your assessment
                </p>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-teal-900">
                  {statusData.completion_percentage}%
                </div>
                <div className="text-sm text-teal-700">Complete</div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default AssessmentStatusView;