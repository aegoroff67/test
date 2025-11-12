import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { 
  Building2, 
  Target, 
  ShieldCheck, 
  Users,
  Calendar,
  ArrowLeft
} from 'lucide-react';
import { toast } from 'sonner';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Industry options
const INDUSTRIES = [
  "Local government / Public sector",
  "Education",
  "Healthcare",
  "Finance / Insurance",
  "Utilities / Critical infrastructure",
  "Retail / Hospitality",
  "Technology / Software",
  "Not-for-profit / Charity",
  "Other"
];

// Organization size options
const ORG_SIZES = [
  "1–49",
  "50–249",
  "250–999",
  "1,000+"
];

// AI Maturity stage
const AI_MATURITY_STAGES = [
  "Exploring / No AI use yet",
  "Early pilots / experimentation",
  "Scaling AI across some departments",
  "Enterprise-wide AI deployment"
];

// Primary AI Focus
const AI_FOCUS_AREAS = [
  "Governance & ethics frameworks",
  "Data quality & infrastructure",
  "Risk management & compliance",
  "Talent & capability building",
  "Innovation & transformation",
  "All of the above"
];

// Regulatory compliance priority
const COMPLIANCE_PRIORITIES = [
  "Low priority",
  "Moderate priority",
  "High priority",
  "Critical priority"
];

// Stakeholder engagement level
const ENGAGEMENT_LEVELS = [
  "Minimal / none",
  "Occasional consultation",
  "Regular structured engagement",
  "Embedded in decision-making"
];

export default function OrganisationPreAssessmentForm() {
  const { assessmentId } = useParams();
  const navigate = useNavigate();
  const [saving, setSaving] = useState(false);

  // Form state
  const [formData, setFormData] = useState({
    organizationName: '',
    industry: '',
    size: '',
    aiMaturityStage: '',
    aiFocusArea: '',
    compliancePriority: '',
    engagementLevel: '',
    additionalContext: ''
  });

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async () => {
    // Validate required fields
    if (!formData.organizationName || !formData.industry || !formData.size || 
        !formData.aiMaturityStage || !formData.aiFocusArea) {
      toast.error('Please fill in all required fields');
      return;
    }

    setSaving(true);
    try {
      // Save organisation information
      await axios.post(`${API}/assessments/${assessmentId}/organisation-info`, formData);
      toast.success('Organisation information saved!');
      
      // Navigate to assessment page
      navigate(`/assessment/${assessmentId}`);
    } catch (error) {
      console.error('Error saving organisation information:', error);
      const errorMessage = error.response?.data?.detail || 'Failed to save organisation information';
      toast.error(errorMessage);
      setSaving(false);
    }
  };

  const handleSkip = () => {
    navigate(`/assessment/${assessmentId}`);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-pink-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <Building2 className="h-8 w-8 text-purple-600" />
              <div>
                <h1 className="text-lg font-bold text-gray-900">Organisation-wide AI Maturity Assessment</h1>
                <p className="text-xs text-purple-600 font-medium">PRE-ASSESSMENT INFORMATION</p>
              </div>
            </div>
            <Button 
              variant="ghost" 
              onClick={() => navigate('/dashboard')}
              data-testid="back-btn"
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <Card className="border-2 border-purple-200">
          <CardHeader className="bg-gradient-to-r from-purple-50 to-pink-50">
            <div className="flex items-start justify-between">
              <div>
                <CardTitle className="text-2xl text-purple-900 mb-2">
                  Welcome to Your Organisation-wide Assessment
                </CardTitle>
                <p className="text-sm text-gray-600">
                  Help us understand your organisation's AI journey. This information will help contextualize your assessment results.
                </p>
              </div>
              <Badge className="bg-purple-100 text-purple-700 border-purple-300">
                Optional
              </Badge>
            </div>
          </CardHeader>

          <CardContent className="space-y-6 p-6">
            {/* Organization Name */}
            <div className="space-y-2">
              <Label htmlFor="organizationName" className="flex items-center gap-2 text-gray-700">
                <Building2 className="h-4 w-4 text-purple-600" />
                Organisation Name *
              </Label>
              <Input
                id="organizationName"
                value={formData.organizationName}
                onChange={(e) => handleInputChange('organizationName', e.target.value)}
                placeholder="Enter your organisation name"
                className="border-purple-200 focus:border-purple-400"
              />
            </div>

            {/* Industry */}
            <div className="space-y-2">
              <Label htmlFor="industry" className="flex items-center gap-2 text-gray-700">
                <Target className="h-4 w-4 text-purple-600" />
                Industry / Sector *
              </Label>
              <Select value={formData.industry} onValueChange={(value) => handleInputChange('industry', value)}>
                <SelectTrigger className="border-purple-200 focus:border-purple-400">
                  <SelectValue placeholder="Select industry" />
                </SelectTrigger>
                <SelectContent>
                  {INDUSTRIES.map((industry) => (
                    <SelectItem key={industry} value={industry}>
                      {industry}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Organization Size */}
            <div className="space-y-2">
              <Label htmlFor="size" className="flex items-center gap-2 text-gray-700">
                <Users className="h-4 w-4 text-purple-600" />
                Organisation Size (Number of Employees) *
              </Label>
              <Select value={formData.size} onValueChange={(value) => handleInputChange('size', value)}>
                <SelectTrigger className="border-purple-200 focus:border-purple-400">
                  <SelectValue placeholder="Select size" />
                </SelectTrigger>
                <SelectContent>
                  {ORG_SIZES.map((size) => (
                    <SelectItem key={size} value={size}>
                      {size}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* AI Maturity Stage */}
            <div className="space-y-2">
              <Label htmlFor="aiMaturityStage" className="flex items-center gap-2 text-gray-700">
                <Calendar className="h-4 w-4 text-purple-600" />
                Current AI Maturity Stage *
              </Label>
              <Select value={formData.aiMaturityStage} onValueChange={(value) => handleInputChange('aiMaturityStage', value)}>
                <SelectTrigger className="border-purple-200 focus:border-purple-400">
                  <SelectValue placeholder="Select maturity stage" />
                </SelectTrigger>
                <SelectContent>
                  {AI_MATURITY_STAGES.map((stage) => (
                    <SelectItem key={stage} value={stage}>
                      {stage}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Primary AI Focus */}
            <div className="space-y-2">
              <Label htmlFor="aiFocusArea" className="flex items-center gap-2 text-gray-700">
                <Target className="h-4 w-4 text-purple-600" />
                Primary AI Focus Area *
              </Label>
              <Select value={formData.aiFocusArea} onValueChange={(value) => handleInputChange('aiFocusArea', value)}>
                <SelectTrigger className="border-purple-200 focus:border-purple-400">
                  <SelectValue placeholder="Select focus area" />
                </SelectTrigger>
                <SelectContent>
                  {AI_FOCUS_AREAS.map((area) => (
                    <SelectItem key={area} value={area}>
                      {area}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Compliance Priority */}
            <div className="space-y-2">
              <Label htmlFor="compliancePriority" className="flex items-center gap-2 text-gray-700">
                <ShieldCheck className="h-4 w-4 text-purple-600" />
                Regulatory Compliance Priority (Optional)
              </Label>
              <Select value={formData.compliancePriority} onValueChange={(value) => handleInputChange('compliancePriority', value)}>
                <SelectTrigger className="border-purple-200 focus:border-purple-400">
                  <SelectValue placeholder="Select priority level" />
                </SelectTrigger>
                <SelectContent>
                  {COMPLIANCE_PRIORITIES.map((priority) => (
                    <SelectItem key={priority} value={priority}>
                      {priority}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Stakeholder Engagement */}
            <div className="space-y-2">
              <Label htmlFor="engagementLevel" className="flex items-center gap-2 text-gray-700">
                <Users className="h-4 w-4 text-purple-600" />
                Stakeholder Engagement Level (Optional)
              </Label>
              <Select value={formData.engagementLevel} onValueChange={(value) => handleInputChange('engagementLevel', value)}>
                <SelectTrigger className="border-purple-200 focus:border-purple-400">
                  <SelectValue placeholder="Select engagement level" />
                </SelectTrigger>
                <SelectContent>
                  {ENGAGEMENT_LEVELS.map((level) => (
                    <SelectItem key={level} value={level}>
                      {level}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Additional Context */}
            <div className="space-y-2">
              <Label htmlFor="additionalContext" className="text-gray-700">
                Additional Context (Optional)
              </Label>
              <textarea
                id="additionalContext"
                value={formData.additionalContext}
                onChange={(e) => handleInputChange('additionalContext', e.target.value)}
                placeholder="Share any additional context about your organisation's AI journey..."
                className="w-full min-h-[100px] px-3 py-2 border border-purple-200 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-400"
              />
            </div>

            {/* Action Buttons */}
            <div className="flex gap-3 pt-4">
              <Button
                onClick={handleSubmit}
                disabled={saving}
                className="flex-1 bg-purple-600 hover:bg-purple-700"
              >
                {saving ? 'Saving...' : 'Save & Continue'}
              </Button>
              <Button
                variant="outline"
                onClick={handleSkip}
                disabled={saving}
                className="border-purple-200 text-purple-600 hover:bg-purple-50"
              >
                Skip for Now
              </Button>
            </div>

            <p className="text-xs text-center text-gray-500 mt-4">
              * Required fields. You can update this information later from your assessment dashboard.
            </p>
          </CardContent>
        </Card>
      </main>
    </div>
  );
}
