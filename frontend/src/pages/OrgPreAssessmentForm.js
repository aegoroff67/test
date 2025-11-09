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
  Users, 
  ShieldCheck, 
  Workflow,
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
  "1,000–4,999",
  "5,000+"
];

// AI project count options
const AI_PROJECT_COUNTS = [
  "None",
  "1–2",
  "3–5",
  "6–10",
  "10+"
];

// AI usage areas options
const AI_USAGE_AREAS = [
  "Customer service / contact centre",
  "Finance / billing / revenue",
  "HR / recruitment",
  "Operations / asset management",
  "Public service delivery",
  "Fraud / risk / compliance",
  "Data analytics / insights",
  "Other"
];

// Primary purpose options
const PRIMARY_PURPOSES = [
  "Efficiency / cost reduction",
  "Improved decision-making",
  "Enhanced service / customer experience",
  "Innovation / new services",
  "Regulatory / compliance obligations",
  "Mixed / other"
];

// Sourcing model options
const SOURCING_MODELS = [
  "Primarily internal development",
  "Primarily third-party / vendor solutions",
  "Mix of internal and third-party",
  "Not clearly defined"
];

// Governance committee status
const GOVERNANCE_STATUSES = [
  "Yes",
  "In development",
  "No"
];

// Frameworks options
const FRAMEWORKS = [
  "ISO/IEC 42001",
  "NIST AI RMF",
  "FAIRA (QLD)",
  "OECD AI Principles",
  "Australian AI Ethics Principles",
  "Internal enterprise risk framework only",
  "None",
  "Other"
];

// Risk assessment usage
const RISK_ASSESSMENT_OPTIONS = [
  "Not used",
  "Used for some projects",
  "Mandatory for all significant AI initiatives"
];

// Policy review frequency
const POLICY_REVIEW_FREQUENCIES = [
  "No defined review cycle",
  "Every 2+ years",
  "Every 12–24 months",
  "At least annually"
];

// AI register status
const AI_REGISTER_STATUSES = [
  "Yes",
  "Planned",
  "No"
];

// Executive engagement levels
const EXEC_ENGAGEMENT_LEVELS = [
  "Minimal / ad hoc",
  "Periodically informed",
  "Regular reporting to executives",
  "Formally overseen by board / committee"
];

// Training maturity
const TRAINING_MATURITY_LEVELS = [
  "No formal training",
  "One-off / ad hoc sessions",
  "Role-specific training for some staff",
  "Structured, recurring training for all relevant staff"
];

// Maturity self-rating
const MATURITY_RATINGS = [
  "Foundational",
  "Developing",
  "Established",
  "Leading"
];

const defaultState = {
  // Organisation Overview
  org_name: '',
  contact_name: '',
  contact_email: '',
  industry: '',
  org_size: '',
  business_units_scope: '',
  
  // AI Landscape & Scope
  ai_project_count: '',
  ai_usage_areas: [],
  ai_primary_purpose: '',
  ai_sourcing_model: '',
  ai_governance_committee_status: '',
  
  // Governance & Risk
  ai_frameworks: [],
  ai_risk_assessment_usage: '',
  policy_review_frequency: '',
  ai_register_status: '',
  
  // Culture & Capability
  exec_engagement_level: '',
  ai_training_maturity: '',
  ai_maturity_self_rating: '',
  
  // Assessment Details
  assessor_name: '',
  assessment_date: '',
  framework_version: 'v2025.11'
};

export default function OrgPreAssessmentForm() {
  const { assessmentId } = useParams();
  const navigate = useNavigate();
  const [form, setForm] = useState(defaultState);
  const [submitting, setSubmitting] = useState(false);

  const update = (field, value) => {
    setForm(prev => ({ ...prev, [field]: value }));
  };

  const toggleArrayItem = (field, item) => {
    setForm(prev => ({
      ...prev,
      [field]: prev[field].includes(item)
        ? prev[field].filter(i => i !== item)
        : [...prev[field], item]
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);

    // Validate required fields
    const requiredFields = [
      'org_name', 'contact_name', 'contact_email', 'industry', 'org_size',
      'ai_project_count', 'ai_primary_purpose', 'ai_sourcing_model', 
      'ai_governance_committee_status', 'ai_risk_assessment_usage',
      'policy_review_frequency', 'ai_register_status', 'exec_engagement_level',
      'ai_training_maturity', 'ai_maturity_self_rating', 'assessor_name',
      'assessment_date', 'framework_version'
    ];

    for (const field of requiredFields) {
      if (!form[field] || (Array.isArray(form[field]) && form[field].length === 0)) {
        toast.error(`Please fill in all required fields`);
        setSubmitting(false);
        return;
      }
    }

    // Validate email format
    const emailRegex = /.+@.+\..+/;
    if (!emailRegex.test(form.contact_email)) {
      toast.error('Please enter a valid email address');
      setSubmitting(false);
      return;
    }

    try {
      await axios.put(`${API}/assessments/${assessmentId}/org-info`, form);
      toast.success('Organisation information saved!');
      navigate(`/assessment/${assessmentId}`);
    } catch (error) {
      console.error('Error saving org info:', error);
      toast.error(error.response?.data?.detail || 'Failed to save organisation information');
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-bg">
      {/* Header */}
      <header className="bg-white shadow-sm border-b sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 py-4">
          <div className="flex items-center justify-between">
            <Button
              variant="ghost"
              onClick={() => navigate('/dashboard')}
              className="flex items-center gap-2"
            >
              <ArrowLeft className="h-4 w-4" />
              Back
            </Button>
          </div>
        </div>
      </header>

      {/* Main Form */}
      <main className="max-w-6xl mx-auto px-4 sm:px-6 py-8">
        {/* Page Title */}
        <div className="text-center space-y-2">
          <h2 className="text-3xl font-bold text-gray-900">Pre-Assessment Onboarding</h2>
          <p className="text-gray-600">
            Organisation-wide AI Maturity Assessment - Please provide the following information so we can tailor the assessment and reporting.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-8">
          {/* Organisation Overview */}
          <Card>
            <CardHeader className="bg-purple-50 border-b border-purple-100">
              <div className="flex items-center space-x-2">
                <Building2 className="h-5 w-5 text-purple-600" />
                <CardTitle className="text-xl">Organisation Overview</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid gap-4 md:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="org_name">Organisation name *</Label>
                  <Input
                    id="org_name"
                    value={form.org_name}
                    onChange={(e) => update('org_name', e.target.value)}
                    placeholder="Your organisation"
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="contact_name">Primary contact name *</Label>
                  <Input
                    id="contact_name"
                    value={form.contact_name}
                    onChange={(e) => update('contact_name', e.target.value)}
                    placeholder="Contact person"
                    required
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="contact_email">Primary contact email *</Label>
                <Input
                  id="contact_email"
                  type="email"
                  value={form.contact_email}
                  onChange={(e) => update('contact_email', e.target.value)}
                  placeholder="email@example.com"
                  required
                />
              </div>

              <div className="grid gap-4 md:grid-cols-2">
                <div className="space-y-2">
                  <Label>Industry sector *</Label>
                  <Select value={form.industry} onValueChange={(v) => update('industry', v)}>
                    <SelectTrigger><SelectValue placeholder="Select industry" /></SelectTrigger>
                    <SelectContent>
                      {INDUSTRIES.map(ind => (
                        <SelectItem key={ind} value={ind}>{ind}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label>Organisation size (headcount) *</Label>
                  <Select value={form.org_size} onValueChange={(v) => update('org_size', v)}>
                    <SelectTrigger><SelectValue placeholder="Select size" /></SelectTrigger>
                    <SelectContent>
                      {ORG_SIZES.map(size => (
                        <SelectItem key={size} value={size}>{size}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="business_units_scope">Primary business unit(s) in scope (optional)</Label>
                <Input
                  id="business_units_scope"
                  value={form.business_units_scope}
                  onChange={(e) => update('business_units_scope', e.target.value)}
                  placeholder="e.g., IT, Customer Service, Operations"
                />
              </div>
            </CardContent>
          </Card>

          {/* AI Landscape & Scope */}
          <Card>
            <CardHeader className="bg-purple-50 border-b border-purple-100">
              <div className="flex items-center space-x-2">
                <Workflow className="h-5 w-5 text-purple-600" />
                <CardTitle className="text-xl">AI Landscape & Scope</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label>Approximate number of AI / advanced analytics initiatives *</Label>
                <Select value={form.ai_project_count} onValueChange={(v) => update('ai_project_count', v)}>
                  <SelectTrigger><SelectValue placeholder="Select count" /></SelectTrigger>
                  <SelectContent>
                    {AI_PROJECT_COUNTS.map(count => (
                      <SelectItem key={count} value={count}>{count}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Where AI is currently used (select all that apply)</Label>
                <div className="grid gap-2 md:grid-cols-2">
                  {AI_USAGE_AREAS.map(area => (
                    <div key={area} className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        id={`usage_${area}`}
                        checked={form.ai_usage_areas.includes(area)}
                        onChange={() => toggleArrayItem('ai_usage_areas', area)}
                        className="h-4 w-4 rounded border-gray-300"
                      />
                      <label htmlFor={`usage_${area}`} className="text-sm">{area}</label>
                    </div>
                  ))}
                </div>
              </div>

              <div className="space-y-2">
                <Label>Primary organisational purpose for AI adoption *</Label>
                <Select value={form.ai_primary_purpose} onValueChange={(v) => update('ai_primary_purpose', v)}>
                  <SelectTrigger><SelectValue placeholder="Select purpose" /></SelectTrigger>
                  <SelectContent>
                    {PRIMARY_PURPOSES.map(purpose => (
                      <SelectItem key={purpose} value={purpose}>{purpose}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>How are AI solutions typically sourced? *</Label>
                <Select value={form.ai_sourcing_model} onValueChange={(v) => update('ai_sourcing_model', v)}>
                  <SelectTrigger><SelectValue placeholder="Select model" /></SelectTrigger>
                  <SelectContent>
                    {SOURCING_MODELS.map(model => (
                      <SelectItem key={model} value={model}>{model}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Central AI governance / ethics / risk committee in place? *</Label>
                <Select value={form.ai_governance_committee_status} onValueChange={(v) => update('ai_governance_committee_status', v)}>
                  <SelectTrigger><SelectValue placeholder="Select status" /></SelectTrigger>
                  <SelectContent>
                    {GOVERNANCE_STATUSES.map(status => (
                      <SelectItem key={status} value={status}>{status}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>

          {/* Governance & Risk */}
          <Card>
            <CardHeader className="bg-purple-50 border-b border-purple-100">
              <div className="flex items-center space-x-2">
                <ShieldCheck className="h-5 w-5 text-purple-600" />
                <CardTitle className="text-xl">Governance & Risk</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label>Frameworks / standards used to guide AI (select all that apply)</Label>
                <div className="grid gap-2 md:grid-cols-2">
                  {FRAMEWORKS.map(framework => (
                    <div key={framework} className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        id={`framework_${framework}`}
                        checked={form.ai_frameworks.includes(framework)}
                        onChange={() => toggleArrayItem('ai_frameworks', framework)}
                        className="h-4 w-4 rounded border-gray-300"
                      />
                      <label htmlFor={`framework_${framework}`} className="text-sm">{framework}</label>
                    </div>
                  ))}
                </div>
              </div>

              <div className="space-y-2">
                <Label>Use of AI risk / impact assessments *</Label>
                <Select value={form.ai_risk_assessment_usage} onValueChange={(v) => update('ai_risk_assessment_usage', v)}>
                  <SelectTrigger><SelectValue placeholder="Select usage" /></SelectTrigger>
                  <SelectContent>
                    {RISK_ASSESSMENT_OPTIONS.map(option => (
                      <SelectItem key={option} value={option}>{option}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Frequency of AI-related policy / guideline review *</Label>
                <Select value={form.policy_review_frequency} onValueChange={(v) => update('policy_review_frequency', v)}>
                  <SelectTrigger><SelectValue placeholder="Select frequency" /></SelectTrigger>
                  <SelectContent>
                    {POLICY_REVIEW_FREQUENCIES.map(freq => (
                      <SelectItem key={freq} value={freq}>{freq}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Central register of AI systems maintained? *</Label>
                <Select value={form.ai_register_status} onValueChange={(v) => update('ai_register_status', v)}>
                  <SelectTrigger><SelectValue placeholder="Select status" /></SelectTrigger>
                  <SelectContent>
                    {AI_REGISTER_STATUSES.map(status => (
                      <SelectItem key={status} value={status}>{status}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>

          {/* Culture & Capability */}
          <Card>
            <CardHeader className="bg-purple-50 border-b border-purple-100">
              <div className="flex items-center space-x-2">
                <Users className="h-5 w-5 text-purple-600" />
                <CardTitle className="text-xl">Culture & Capability</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label>Executive / board engagement in AI governance *</Label>
                <Select value={form.exec_engagement_level} onValueChange={(v) => update('exec_engagement_level', v)}>
                  <SelectTrigger><SelectValue placeholder="Select level" /></SelectTrigger>
                  <SelectContent>
                    {EXEC_ENGAGEMENT_LEVELS.map(level => (
                      <SelectItem key={level} value={level}>{level}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Staff training on AI, ethics & responsible use *</Label>
                <Select value={form.ai_training_maturity} onValueChange={(v) => update('ai_training_maturity', v)}>
                  <SelectTrigger><SelectValue placeholder="Select maturity" /></SelectTrigger>
                  <SelectContent>
                    {TRAINING_MATURITY_LEVELS.map(level => (
                      <SelectItem key={level} value={level}>{level}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Organisation-wide AI maturity (self-assessed) *</Label>
                <Select value={form.ai_maturity_self_rating} onValueChange={(v) => update('ai_maturity_self_rating', v)}>
                  <SelectTrigger><SelectValue placeholder="Select rating" /></SelectTrigger>
                  <SelectContent>
                    {MATURITY_RATINGS.map(rating => (
                      <SelectItem key={rating} value={rating}>{rating}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>

          {/* Assessment Details */}
          <Card>
            <CardHeader className="bg-purple-50 border-b border-purple-100">
              <div className="flex items-center space-x-2">
                <Calendar className="h-5 w-5 text-purple-600" />
                <CardTitle className="text-xl">Assessment Details</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="assessor_name">Assessment conducted by *</Label>
                <Input
                  id="assessor_name"
                  value={form.assessor_name}
                  onChange={(e) => update('assessor_name', e.target.value)}
                  placeholder="Assessor name"
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="assessment_date">Assessment date *</Label>
                <Input
                  id="assessment_date"
                  type="date"
                  value={form.assessment_date}
                  onChange={(e) => update('assessment_date', e.target.value)}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="framework_version">AM AI SAFE framework version *</Label>
                <Input
                  id="framework_version"
                  value={form.framework_version}
                  onChange={(e) => update('framework_version', e.target.value)}
                  placeholder="e.g., v2025.11"
                  required
                />
              </div>
            </CardContent>
          </Card>

          {/* Submit Button */}
          <div className="flex justify-end gap-4">
            <Button
              type="button"
              variant="outline"
              onClick={() => navigate('/dashboard')}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              disabled={submitting}
              className="bg-purple-600 hover:bg-purple-700"
            >
              {submitting ? (
                <div className="flex items-center space-x-2">
                  <div className="loading-spinner w-4 h-4"></div>
                  <span>Saving...</span>
                </div>
              ) : (
                'Continue to Assessment'
              )}
            </Button>
          </div>
        </form>
      </main>
    </div>
  );
}
