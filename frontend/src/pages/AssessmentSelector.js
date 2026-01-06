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

// Assessment Card Component with hover animations
const AssessmentCard = ({ 
  title, 
  purpose, 
  bestFor, 
  outcome, 
  icon: Icon, 
  color, 
  tagline,
  hasAccess, 
  onClick, 
  creating,
  testId 
}) => {
  const [isHovered, setIsHovered] = useState(false);
  
  // Color configurations
  const colorConfig = {
    green: {
      border: 'border-green-500',
      bg: 'bg-green-100',
      iconColor: 'text-green-600',
      buttonBg: 'bg-green-600 hover:bg-green-700',
      badgeBg: 'bg-green-100 text-green-700 border-green-300',
      glowColor: 'rgba(34, 197, 94, 0.4)',
      taglineBg: 'bg-green-600/75',
    },
    blue: {
      border: 'border-blue-500',
      bg: 'bg-blue-100',
      iconColor: 'text-blue-600',
      buttonBg: 'bg-blue-600 hover:bg-blue-700',
      badgeBg: 'bg-blue-100 text-blue-700 border-blue-300',
      glowColor: 'rgba(59, 130, 246, 0.4)',
      taglineBg: 'bg-blue-600/75',
    },
    purple: {
      border: 'border-purple-500',
      bg: 'bg-purple-100',
      iconColor: 'text-purple-600',
      buttonBg: 'bg-purple-600 hover:bg-purple-700',
      badgeBg: 'bg-purple-100 text-purple-700 border-purple-300',
      glowColor: 'rgba(147, 51, 234, 0.4)',
      taglineBg: 'bg-purple-600/75',
    },
    teal: {
      border: 'border-teal-500',
      bg: 'bg-teal-100',
      iconColor: 'text-teal-600',
      buttonBg: 'bg-teal-600 hover:bg-teal-700',
      badgeBg: 'bg-teal-100 text-teal-700 border-teal-300',
      glowColor: 'rgba(20, 184, 166, 0.4)',
      taglineBg: 'bg-teal-600/75',
    },
    orange: {
      border: 'border-orange-500',
      bg: 'bg-orange-100',
      iconColor: 'text-orange-600',
      buttonBg: 'bg-orange-600 hover:bg-orange-700',
      badgeBg: 'bg-orange-100 text-orange-700 border-orange-300',
      glowColor: 'rgba(249, 115, 22, 0.4)',
      taglineBg: 'bg-orange-600/75',
    },
  };

  const config = colorConfig[color];

  return (
    <Card 
      className={`relative overflow-hidden transition-all duration-300 border-2 ${config.border} flex flex-col h-full ${!hasAccess ? 'opacity-60' : ''}`}
      style={{
        boxShadow: isHovered && hasAccess
          ? `0 0 20px ${config.glowColor}, 0 0 40px ${config.glowColor}, 0 4px 20px rgba(0,0,0,0.1)`
          : '0 1px 3px rgba(0,0,0,0.1)',
        transform: isHovered && hasAccess ? 'translateY(-2px)' : 'translateY(0)',
      }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Animated glow border effect - removed */}

      <Badge className={`absolute top-4 right-4 text-xs ${hasAccess ? config.badgeBg : 'bg-gray-100 text-gray-700 border-gray-300'}`}>
        {hasAccess ? 'Available Now' : 'Requires Permission'}
      </Badge>
      
      <CardHeader className="pb-[10px]">
        <div className={`mb-3 inline-flex h-12 w-12 items-center justify-center rounded-2xl ${config.bg}`}>
          <Icon className={`h-6 w-6 ${config.iconColor}`} aria-hidden />
        </div>
        <CardTitle className="text-lg text-gray-900">{title}</CardTitle>
      </CardHeader>
      
      <CardContent className="px-6 pb-6 pt-[10px] flex-1 flex flex-col">
        <div className="space-y-3 mb-6 flex-1">
          <p className="text-sm text-gray-600 font-semibold">Purpose:</p>
          <p className="text-sm text-gray-600">{purpose}</p>
          <p className="text-xs text-gray-500">
            <span className="font-semibold">Best for:</span> {bestFor}
          </p>
          <p className="text-xs text-gray-500">
            <span className="font-semibold">Outcome:</span> {outcome}
          </p>
        </div>
        
        <div className="mt-auto">
          <Button 
            className={`w-full ${hasAccess ? config.buttonBg : 'bg-gray-400 cursor-not-allowed'}`}
            onClick={onClick}
            disabled={!hasAccess || creating}
            data-testid={testId}
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

      {/* Sliding tagline from top */}
      <div 
        className={`absolute top-0 left-0 right-0 ${config.taglineBg} transition-all duration-300 ease-out overflow-hidden`}
        style={{
          height: isHovered && hasAccess ? '36px' : '0px',
          opacity: isHovered && hasAccess ? 1 : 0,
          backdropFilter: 'blur(12px)',
          WebkitBackdropFilter: 'blur(12px)',
        }}
      >
        <div className="flex items-center justify-center h-full px-4">
          <p className="text-white text-sm font-medium tracking-wide whitespace-nowrap">
            {tagline}
          </p>
        </div>
      </div>

      {/* CSS for glow animation */}
      <style jsx="true">{`
        @keyframes glowPulse {
          0%, 100% { opacity: 0.2; }
          50% { opacity: 0.4; }
        }
      `}</style>
    </Card>
  );
};

/**
 * AssessmentSelector
 *
 * Shows five assessment option cards with animated hover effects.
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

  const assessments = [
    {
      title: "AI Awareness & Foundations Assessment",
      purpose: "Establish your organisation's baseline understanding of AI and identify initial focus areas to build confidence and capability.",
      bestFor: "Organisations new to AI, seeking to raise awareness and take informed first steps safely.",
      outcome: "A clear starting-point map highlighting priority areas for action — including policy, data, training, and pilot exploration.",
      icon: Sprout,
      color: "green",
      tagline: "Start smart with AI.",
      accessKey: "awareness",
      onClick: handleAwarenessAssessment,
      testId: "awareness-assessment-btn",
    },
    {
      title: "AI Readiness Assessment",
      purpose: "Assess your organisation's readiness to adopt AI by identifying governance gaps, risks, and capability constraints prior to implementation.",
      bestFor: "Organisations planning or piloting AI initiatives and seeking confidence before scaling.",
      outcome: "A readiness map highlighting priority improvements across leadership, policy, and data foundations.",
      icon: Rocket,
      color: "blue",
      tagline: "Ready to scale — or not?",
      accessKey: "readiness",
      onClick: handleReadinessAssessment,
      testId: "readiness-assessment-btn",
    },
    {
      title: "Organisation-wide AI Maturity Assessment",
      purpose: "Evaluate AI governance maturity across the organisation and benchmark policies, processes, and culture against recognised global standards.",
      bestFor: "Organisations scaling AI initiatives or formalising governance across multiple teams or departments.",
      outcome: "An organisation-wide maturity heatmap highlighting systemic strengths, gaps, and priority improvement areas.",
      icon: Building2,
      color: "purple",
      tagline: "How mature is AI here?",
      accessKey: "orgwide",
      onClick: handleOrgAssessment,
      testId: "orgwide-assessment-btn",
    },
    {
      title: "AI System Maturity Assessment",
      purpose: "Assess a specific AI system against governance, ethical, and compliance requirements, including bias management, explainability, and lifecycle controls.",
      bestFor: "Teams responsible for an active AI model or AI-enabled system in production or pilot use.",
      outcome: "A detailed system-level assurance report suitable for inclusion in risk, audit, and compliance reviews.",
      icon: Bot,
      color: "teal",
      tagline: "Is this AI trustworthy?",
      accessKey: "system",
      onClick: handleSystemAssessment,
      testId: "system-assessment-btn",
    },
    {
      title: "FAIRA Risk Assessment",
      purpose: "Evaluate algorithmic and AI systems using Queensland's FAIRA framework to identify risks, assess impacts, meet governance obligations, and generate assurance-ready compliance documentation.",
      bestFor: "Government agencies, councils, universities, and vendors requiring structured, defensible AI risk assessments.",
      outcome: "A complete FAIRA assessment report, including risk ratings, scoring, mitigation controls, and audit-ready documentation.",
      icon: ShieldCheck,
      color: "orange",
      tagline: "FAIRA-aligned. Audit-ready.",
      accessKey: "faira",
      onClick: handleFairaAssessment,
      testId: "faira-assessment-btn",
    },
  ];

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
          {assessments.map((assessment) => (
            <AssessmentCard
              key={assessment.accessKey}
              title={assessment.title}
              purpose={assessment.purpose}
              bestFor={assessment.bestFor}
              outcome={assessment.outcome}
              icon={assessment.icon}
              color={assessment.color}
              tagline={assessment.tagline}
              hasAccess={hasAccess(assessment.accessKey)}
              onClick={hasAccess(assessment.accessKey) 
                ? assessment.onClick 
                : () => toast.error('You do not have permission to access this assessment. Please contact your administrator.')}
              creating={creating}
              testId={assessment.testId}
            />
          ))}
        </div>
      </main>
    </div>
  );
}
