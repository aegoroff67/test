import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import { toast } from 'sonner';
import { ArrowLeft, Save } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';

const API = process.env.REACT_APP_BACKEND_URL || '';

function ReviewAssessmentPage() {
  const { assessmentId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [pendingAnswers, setPendingAnswers] = useState([]);
  const [scores, setScores] = useState({});

  useEffect(() => {
    fetchPendingAnswers();
  }, [assessmentId]);

  const fetchPendingAnswers = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/admin/assessments/${assessmentId}/pending-answers`);
      setPendingAnswers(response.data);
      
      // Initialize scores with current values
      const initialScores = {};
      response.data.forEach(answer => {
        initialScores[answer.answer_id] = answer.current_score;
      });
      setScores(initialScores);
    } catch (error) {
      toast.error('Failed to fetch pending answers');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleScoreChange = (answerId, score) => {
    setScores(prev => ({
      ...prev,
      [answerId]: parseInt(score)
    }));
  };

  const handleSubmitScore = async (answerId) => {
    try {
      const score = scores[answerId];
      if (score < 0 || score > 3) {
        toast.error('Score must be between 0 and 3');
        return;
      }

      await axios.put(`${API}/admin/assessments/${assessmentId}/answers/${answerId}/score`, null, {
        params: { score }
      });
      
      toast.success('Score saved successfully');
      
      // Refresh the list
      fetchPendingAnswers();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to save score');
      console.error(error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-bg flex items-center justify-center">
        <div className="loading-spinner w-12 h-12"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-bg">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <h1 className="text-xl font-bold text-gray-900">Review Assessment Responses</h1>
            <Button 
              variant="outline" 
              onClick={() => navigate('/settings?tab=reviews')}
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Reviews
            </Button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {pendingAnswers.length === 0 ? (
          <Card>
            <CardContent className="text-center py-12">
              <p className="text-gray-500 text-lg">No pending answers for this assessment</p>
              <p className="text-gray-400 text-sm mt-2">All responses have been scored</p>
              <Button 
                className="mt-4"
                onClick={() => navigate('/settings?tab=reviews')}
              >
                Back to Reviews
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-6">
            {pendingAnswers.map((answer, index) => (
              <Card key={answer.answer_id}>
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <div>
                      <CardTitle className="text-lg">
                        Question {index + 1} of {pendingAnswers.length}
                      </CardTitle>
                      <div className="flex items-center gap-2 mt-2">
                        <Badge className="bg-blue-100 text-blue-800">
                          {answer.domain_name}
                        </Badge>
                        <Badge className="bg-gray-100 text-gray-800">
                          {answer.question_code}
                        </Badge>
                      </div>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Question Text */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Question:
                    </label>
                    <p className="text-gray-900 bg-gray-50 p-3 rounded border">
                      {answer.question_text}
                    </p>
                  </div>

                  {/* Custom Response */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      User's Custom Response:
                    </label>
                    <p className="text-gray-900 bg-yellow-50 p-3 rounded border border-yellow-200">
                      {answer.other_text || 'No text provided'}
                    </p>
                  </div>

                  {/* Score Input */}
                  <div className="flex items-center gap-4">
                    <div className="flex-1">
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Assign Score (0-3):
                      </label>
                      <div className="flex gap-2">
                        {[0, 1, 2, 3].map(scoreValue => (
                          <button
                            key={scoreValue}
                            onClick={() => handleScoreChange(answer.answer_id, scoreValue)}
                            className={`px-6 py-3 rounded-lg border-2 font-semibold transition-all ${
                              scores[answer.answer_id] === scoreValue
                                ? 'border-teal-600 bg-teal-600 text-white'
                                : 'border-gray-300 bg-white text-gray-700 hover:border-teal-400'
                            }`}
                          >
                            {scoreValue}
                          </button>
                        ))}
                      </div>
                      <p className="text-xs text-gray-500 mt-2">
                        0 = Non-ideal, 1 = Basic, 2 = Good, 3 = Ideal
                      </p>
                    </div>

                    <Button
                      onClick={() => handleSubmitScore(answer.answer_id)}
                      className="bg-teal-600 hover:bg-teal-700 mt-6"
                    >
                      <Save className="h-4 w-4 mr-2" />
                      Save Score
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default ReviewAssessmentPage;
