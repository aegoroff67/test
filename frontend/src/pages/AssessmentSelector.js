import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from '../context/AuthContext';
import Logo from '../components/Logo';
import { Lightbulb, Building2, Bot, ArrowLeft, Sprout, Rocket, ShieldCheck } from "lucide-react";
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
 * Shows four assessment option cards.
 * Adapted from Next.js to React Router with Tailwind + shadcn/ui + lucide-react.
 */
export default function AssessmentSelector() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [creating, setCreating] = useState(false);
  
  // Get user's assessment access permissions (default to awareness only)
  const assessmentAccess = user?.assessment_access || ['awareness'];
  
  // Check if user has access to a specific assessment type
  const hasAccess = (assessmentType) => assessmentAccess.includes(assessmentType);

  const handleSystemAssessment = async () => {
    setCreating(true);
    try {
      const response = await axios.post(`${API}/assessments`, { assessment_type: "System" });
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

  const handleOrgAssessment = async () => {
    setCreating(true);
    try {
      const response = await axios.post(`${API}/assessments`, { assessment_type: "Orgwide" });
      if (response.data && response.data.id) {
        toast.success('New organisation assessment created!');
        // Redirect to org onboarding page
        navigate(`/assessment/${response.data.id}/org-onboarding`);
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

  const handleReadinessAssessment = async () => {
    setCreating(true);
    try {
      const response = await axios.post(`${API}/assessments`, { assessment_type: "Readiness" });
      if (response.data && response.data.id) {
        toast.success('New readiness assessment created!');
        // Redirect to readiness onboarding page
        navigate(`/assessment/${response.data.id}/readiness-onboarding`);
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

  const handleAwarenessAssessment = async () => {
    setCreating(true);
    try {
      const response = await axios.post(`${API}/assessments`, { assessment_type: "Awareness" });
      if (response.data && response.data.id) {
        toast.success('New awareness assessment created!');
        // Redirect to awareness onboarding page
        navigate(`/assessment/${response.data.id}/awareness-onboarding`);
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

  const handleFairaAssessment = async () => {
    setCreating(true);
    try {
      const response = await axios.post(`${API}/assessments`, { assessment_type: "FAIRA" });
      if (response.data && response.data.id) {
        toast.success('New FAIRA assessment created!');
        // Redirect to FAIRA onboarding page
        navigate(`/assessment/${response.data.id}/faira-onboarding`);
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
              <Logo className="h-10 w-10" />
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
      <main className="mx-auto max-w-7xl px-4 py-12">
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
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">
          {/* 1. AI Awareness & Foundations Assessment */}
          <Card className="relative overflow-hidden transition-all duration-200 hover:shadow-lg border-2 border-green-500 flex flex-col h-full">
            <Badge className="absolute top-4 right-4 text-xs bg-green-100 text-green-700 border-green-300">
              Available Now
            </Badge>
            <CardHeader className="pb-[10px]">
              <div className="mb-3 inline-flex h-12 w-12 items-center justify-center rounded-2xl bg-green-100">
                <Sprout className="h-6 w-6 text-green-600" aria-hidden />
              </div>
              <CardTitle className="text-lg text-gray-900">AI Awareness & Foundations Assessment</CardTitle>
            </CardHeader>
            <CardContent className="px-6 pb-6 pt-[10px] flex-1 flex flex-col">
              <div className="space-y-3 mb-6 flex-1">
                <p className="text-sm text-gray-600 font-semibold">Purpose:</p>
                <p className="text-sm text-gray-600">
                  Discover your organisation's starting point on its AI journey. Learn what AI means for you and identify first steps to build confidence and capability.
                </p>
                <p className="text-xs text-gray-500">
                  <span className="font-semibold">Best for:</span> Organisations new to AI or automation, wanting to raise awareness and begin safely.
                </p>
                <p className="text-xs text-gray-500">
                  <span className="font-semibold">Outcome:</span> A simple "Starting Point Map" showing where to focus next — policy, data, training, or pilot exploration.
                </p>
              </div>
              <div className="mt-auto">
                <Button 
                  className="w-full bg-green-600 hover:bg-green-700"
                  onClick={handleAwarenessAssessment}
                  disabled={creating}
                  data-testid="awareness-assessment-btn"
                >
                  Start Assessment
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* 2. AI Readiness Assessment */}
          <Card className={`relative overflow-hidden transition-all duration-200 hover:shadow-lg border-2 border-blue-500 flex flex-col h-full ${!hasAccess('readiness') ? 'opacity-60' : ''}`}>
            <Badge className={`absolute top-4 right-4 text-xs ${hasAccess('readiness') ? 'bg-blue-100 text-blue-700 border-blue-300' : 'bg-gray-100 text-gray-700 border-gray-300'}`}>
              {hasAccess('readiness') ? 'Available Now' : 'Requires Permission'}
            </Badge>
            <CardHeader className="pb-[10px]">
              <div className="mb-3 inline-flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-100">
                <Rocket className="h-6 w-6 text-blue-600" aria-hidden />
              </div>
              <CardTitle className="text-lg text-gray-900">AI Readiness Assessment</CardTitle>
            </CardHeader>
            <CardContent className="p-6 flex-1 flex flex-col">
              <div className="space-y-3 mb-6 flex-1">
                <p className="text-sm text-gray-600 font-semibold">Purpose:</p>
                <p className="text-sm text-gray-600">
                  Understand your organisation's preparedness for AI adoption. Identify governance gaps, risks, and capabilities before beginning implementation.
                </p>
                <p className="text-xs text-gray-500">
                  <span className="font-semibold">Best for:</span> Organisations planning or piloting AI initiatives for the first time.
                </p>
                <p className="text-xs text-gray-500">
                  <span className="font-semibold">Outcome:</span> A readiness map highlighting foundational improvements across leadership, policy, and data.
                </p>
              </div>
              <div className="mt-auto">
                <Button 
                  className={`w-full ${hasAccess('readiness') ? 'bg-blue-600 hover:bg-blue-700' : 'bg-gray-400 cursor-not-allowed'}`}
                  onClick={hasAccess('readiness') ? handleReadinessAssessment : () => toast.error('You do not have permission to access this assessment. Please contact your administrator.')}
                  disabled={!hasAccess('readiness') || creating}
                  data-testid="readiness-assessment-btn"
                >
                  Start Assessment
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* 3. Organisation-wide AI Maturity Assessment */}
          <Card className={`relative overflow-hidden transition-all duration-200 hover:shadow-lg border-2 border-purple-500 flex flex-col h-full ${!hasAccess('orgwide') ? 'opacity-60' : ''}`}>
            <Badge className={`absolute top-4 right-4 text-xs ${hasAccess('orgwide') ? 'bg-purple-100 text-purple-700 border-purple-300' : 'bg-gray-100 text-gray-700 border-gray-300'}`}>
              {hasAccess('orgwide') ? 'Available Now' : 'Requires Permission'}
            </Badge>
            <CardHeader className="pb-[10px]">
              <div className="mb-3 inline-flex h-12 w-12 items-center justify-center rounded-2xl bg-purple-100">
                <Building2 className="h-6 w-6 text-purple-600" aria-hidden />
              </div>
              <CardTitle className="text-lg text-gray-900">Organisation-wide AI Maturity Assessment</CardTitle>
            </CardHeader>
            <CardContent className="p-6 flex-1 flex flex-col">
              <div className="space-y-3 mb-6 flex-1">
                <p className="text-sm text-gray-600 font-semibold">Purpose:</p>
                <p className="text-sm text-gray-600">
                  Evaluate your organisation's overall AI governance maturity across teams and projects. Benchmark policies, processes, and culture against global standards.
                </p>
                <p className="text-xs text-gray-500">
                  <span className="font-semibold">Best for:</span> Organisations scaling AI initiatives or formalising governance across multiple departments.
                </p>
                <p className="text-xs text-gray-500">
                  <span className="font-semibold">Outcome:</span> An organisation-wide maturity heatmap highlighting systemic strengths and gaps.
                </p>
              </div>
              <div className="mt-auto">
                <Button 
                  className={`w-full ${hasAccess('orgwide') ? 'bg-purple-600 hover:bg-purple-700' : 'bg-gray-400 cursor-not-allowed'}`}
                  onClick={hasAccess('orgwide') ? handleOrgAssessment : () => toast.error('You do not have permission to access this assessment. Please contact your administrator.')}
                  disabled={!hasAccess('orgwide') || creating}
                  data-testid="orgwide-assessment-btn"
                >
                  {creating ? (
                    <div className="flex items-center space-x-2">
                      <div className="loading-spinner w-4 h-4"></div>
                      <span>Creating...</span>
                    </div>
                  ) : (
                    'Start Assessment'
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* 4. AI System Maturity Assessment */}
          <Card className={`relative overflow-hidden transition-all duration-200 hover:shadow-lg border-2 border-teal-500 flex flex-col h-full ${!hasAccess('system') ? 'opacity-60' : ''}`}>
            <Badge className={`absolute top-4 right-4 text-xs ${hasAccess('system') ? 'bg-teal-100 text-teal-700 border-teal-300' : 'bg-gray-100 text-gray-700 border-gray-300'}`}>
              {hasAccess('system') ? 'Available Now' : 'Requires Permission'}
            </Badge>
            <CardHeader className="pb-[10px]">
              <div className="mb-3 inline-flex h-12 w-12 items-center justify-center rounded-2xl bg-teal-100">
                <Bot className="h-6 w-6 text-teal-600" aria-hidden />
              </div>
              <CardTitle className="text-lg text-gray-900">AI System Maturity Assessment</CardTitle>
            </CardHeader>
            <CardContent className="p-6 flex-1 flex flex-col">
              <div className="space-y-3 mb-6 flex-1">
                <p className="text-sm text-gray-600 font-semibold">Purpose:</p>
                <p className="text-sm text-gray-600">
                  Assess a specific AI system for governance, ethics, and compliance. Review bias, explainability, and lifecycle controls.
                </p>
                <p className="text-xs text-gray-500">
                  <span className="font-semibold">Best for:</span> Teams managing an active AI model, automation, or data-driven application.
                </p>
                <p className="text-xs text-gray-500">
                  <span className="font-semibold">Outcome:</span> A detailed assurance report ready for inclusion in risk and compliance reviews.
                </p>
              </div>
              <div className="mt-auto">
                <Button 
                  className={`w-full ${hasAccess('system') ? 'bg-teal-600 hover:bg-teal-700' : 'bg-gray-400 cursor-not-allowed'}`}
                  onClick={hasAccess('system') ? handleSystemAssessment : () => toast.error('You do not have permission to access this assessment. Please contact your administrator.')}
                  disabled={!hasAccess('system') || creating}
                  data-testid="system-assessment-btn"
                >
                  {creating ? (
                    <div className="flex items-center space-x-2">
                      <div className="loading-spinner w-4 h-4"></div>
                      <span>Creating...</span>
                    </div>
                  ) : (
                    'Start Assessment'
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* 5. FAIRA Risk Assessment */}
          <Card className={`relative overflow-hidden transition-all duration-200 hover:shadow-lg border-2 border-orange-500 flex flex-col h-full ${!hasAccess('faira') ? 'opacity-60' : ''}`}>
            <Badge className={`absolute top-4 right-4 text-xs ${hasAccess('faira') ? 'bg-orange-100 text-orange-700 border-orange-300' : 'bg-gray-100 text-gray-700 border-gray-300'}`}>
              {hasAccess('faira') ? 'Available Now' : 'Requires Permission'}
            </Badge>
            <CardHeader className="pb-[10px]">
              <div className="mb-3 inline-flex h-12 w-12 items-center justify-center rounded-2xl bg-orange-100">
                <ShieldCheck className="h-6 w-6 text-orange-600" aria-hidden />
              </div>
              <CardTitle className="text-lg text-gray-900">FAIRA Risk Assessment</CardTitle>
            </CardHeader>
            <CardContent className="p-6 flex-1 flex flex-col">
              <div className="space-y-3 mb-6 flex-1">
                <p className="text-sm text-gray-600 font-semibold">Purpose:</p>
                <p className="text-sm text-gray-600">
                  Evaluate AI solutions using Queensland's FAIRA framework to identify risks, assess impacts, meet governance obligations, and generate assurance-ready compliance documentation.
                </p>
                <p className="text-xs text-gray-500">
                  <span className="font-semibold">Best For:</span> Government agencies, councils, universities, and vendors needing structured, defensible AI risk assessment.
                </p>
                <p className="text-xs text-gray-500">
                  <span className="font-semibold">Outcome:</span> Provides a full FAIRA report with risk ratings, scoring, mitigation controls, and audit-ready documentation for assurance and compliance.
                </p>
              </div>
              <div className="mt-auto">
                <Button 
                  className={`w-full ${hasAccess('faira') ? 'bg-orange-600 hover:bg-orange-700' : 'bg-gray-400 cursor-not-allowed'}`}
                  onClick={hasAccess('faira') ? handleFairaAssessment : () => toast.error('You do not have permission to access this assessment. Please contact your administrator.')}
                  disabled={!hasAccess('faira') || creating}
                  data-testid="faira-assessment-btn"
                >
                  {creating ? (
                    <div className="flex items-center space-x-2">
                      <div className="loading-spinner w-4 h-4"></div>
                      <span>Creating...</span>
                    </div>
                  ) : (
                    'Start Assessment'
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
