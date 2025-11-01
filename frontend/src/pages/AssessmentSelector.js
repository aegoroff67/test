import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Logo from '../components/Logo';
import { Lightbulb, Building2, Bot, ArrowLeft } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { toast } from 'sonner';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

/**
 * AssessmentSelector
 *
 * Shows three assessment option cards side-by-side.
 * Only the "AI System Assessment" is currently active.
 * Adapted from Next.js to React Router with Tailwind + shadcn/ui + lucide-react.
 */
export default function AssessmentSelector() {
  const navigate = useNavigate();
  const [creating, setCreating] = useState(false);

  const handleSystemAssessment = async () => {
    setCreating(true);
    try {
      const response = await axios.post(`${API}/assessments`, {});
      if (response.data && response.data.id) {
        toast.success('New assessment created!');
        // Redirect to onboarding page instead of directly to assessment
        navigate(`/assessment/${response.data.id}/onboarding`);
      } else {
        throw new Error('Invalid response from server');
      }
    } catch (error) {
      console.error('Assessment creation error:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to create assessment';
      toast.error(errorMessage);
      setCreating(false);
    }
  };

  const handleComingSoon = (assessmentType) => {
    toast.info(`${assessmentType} coming soon!`);
  };

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

            {/* Back Button */}
            <Button 
              variant="outline" 
              onClick={() => navigate('/dashboard')}
              data-testid="back-to-dashboard-btn"
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Dashboard
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="mx-auto max-w-6xl px-4 py-12">
        {/* Header */}
        <div className="mb-12 text-center">
          <h1 className="text-4xl font-bold tracking-tight text-gray-900 mb-3">
            Choose Your Assessment Type
          </h1>
          <p className="text-lg text-gray-600">
            Select the assessment that best fits your organization's AI journey.
          </p>
        </div>

        {/* Cards */}
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {/* Readiness / Discovery */}
          <Card className="relative overflow-hidden transition-all duration-200 hover:shadow-lg opacity-60">
            <CardHeader>
              <div className="mb-3 inline-flex h-12 w-12 items-center justify-center rounded-2xl bg-gray-200">
                <Lightbulb className="h-6 w-6 text-gray-500" aria-hidden />
              </div>
              <div className="flex items-center justify-between">
                <CardTitle className="text-xl text-gray-700">AI Readiness Assessment</CardTitle>
                <Badge variant="outline" className="text-xs bg-yellow-50 text-yellow-700 border-yellow-300">
                  Coming Soon
                </Badge>
              </div>
            </CardHeader>
            <CardContent className="p-6">
              <div className="space-y-2 mb-6">
                <p className="text-sm text-gray-600">
                  Understand your organisation's preparedness for AI adoption. Identify governance gaps, risks, and
                  capabilities before you begin implementing AI.
                </p>
                <p className="text-xs text-gray-500 italic">
                  Ideal for organisations not yet using AI or just starting out.
                </p>
              </div>
              <div>
                <Button 
                  className="w-full bg-gray-300 hover:bg-gray-400 text-gray-700 cursor-not-allowed"
                  disabled
                  onClick={() => handleComingSoon('AI Readiness Assessment')}
                  data-testid="readiness-assessment-btn"
                >
                  Coming Soon
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Organisation-wide Maturity */}
          <Card className="relative overflow-hidden transition-all duration-200 hover:shadow-lg opacity-60">
            <CardHeader>
              <div className="mb-3 inline-flex h-12 w-12 items-center justify-center rounded-2xl bg-gray-200">
                <Building2 className="h-6 w-6 text-gray-500" aria-hidden />
              </div>
              <div className="flex items-center justify-between">
                <CardTitle className="text-xl text-gray-700">Organisation-wide AI Maturity Assessment</CardTitle>
                <Badge variant="outline" className="text-xs bg-yellow-50 text-yellow-700 border-yellow-300">
                  Coming Soon
                </Badge>
              </div>
            </CardHeader>
            <CardContent className="p-6">
              <div className="space-y-2 mb-6">
                <p className="text-sm text-gray-600">
                  Evaluate your organisation's overall AI governance and maturity. Benchmark policies, processes, and
                  culture against global standards.
                </p>
                <p className="text-xs text-gray-500 italic">
                  Best for organisations with multiple AI projects or growing AI teams.
                </p>
              </div>
              <div>
                <Button 
                  className="w-full bg-gray-300 hover:bg-gray-400 text-gray-700 cursor-not-allowed"
                  disabled
                  onClick={() => handleComingSoon('Organisation-wide AI Maturity Assessment')}
                  data-testid="org-assessment-btn"
                >
                  Coming Soon
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* System-specific Maturity - ACTIVE */}
          <Card className="relative overflow-hidden transition-all duration-200 hover:shadow-xl border-2 border-teal-500 shadow-md">
            <CardHeader>
              <div className="mb-3 inline-flex h-12 w-12 items-center justify-center rounded-2xl bg-teal-100">
                <Bot className="h-6 w-6 text-teal-600" aria-hidden />
              </div>
              <CardTitle className="text-xl text-gray-900">AI System Maturity Assessment</CardTitle>
            </CardHeader>
            <CardContent className="p-6">
              <div className="space-y-2 mb-6">
                <p className="text-sm text-gray-700">
                  Assess a specific AI system for governance, ethics, and compliance. Review bias, explainability, and
                  lifecycle controls for your chosen system.
                </p>
                <p className="text-xs text-gray-600 italic">
                  Recommended if you already have an active AI model or application.
                </p>
              </div>
              <div>
                <Button 
                  className="w-full bg-teal-600 hover:bg-teal-700 btn-hover"
                  onClick={handleSystemAssessment}
                  disabled={creating}
                  data-testid="system-assessment-btn"
                  type="button"
                >
                  {creating ? (
                    <div className="flex items-center justify-center space-x-2">
                      <div className="loading-spinner w-4 h-4"></div>
                      <span>Starting...</span>
                    </div>
                  ) : (
                    'Start System Assessment'
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}
