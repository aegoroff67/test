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
  Database,
  ClipboardList,
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

// AI Motivation options
const AI_MOTIVATIONS = [
  "Improve efficiency / reduce costs",
  "Enhance decision-making / insights",
  "Improve customer / community experience",
  "Innovate services / offerings",
  "Meet regulatory / policy expectations",
  "Other / not sure"
];

// Leadership commitment options
const LEADERSHIP_COMMITMENTS = [
  "Exploring ideas only",
  "Discussed at leadership level",
  "Budget or resources allocated",
  "Approved AI / digital roadmap"
];

// AI Strategy status
const AI_STRATEGY_STATUSES = [
  "None",
  "In development",
  "Informal / draft only",
  "Formally approved"
];

// Risk awareness levels
const RISK_AWARENESS_LEVELS = [
  "None",
  "Emerging",
  "Moderate",
  "Strong"
];

// Governance foundations
const GOVERNANCE_FOUNDATIONS = [
  "Cybersecurity / ICT policies",
  "Data governance framework",
  "Privacy management program",
  "Risk management framework",
  "Ethics or responsible innovation policy",
  "None of the above"
];

// Decision ownership
const DECISION_OWNERSHIP = [
  "Board",
  "Executive leadership",
  "CIO / IT / Digital team",
  "Individual departments",
  "Ad hoc / unclear"
];

// Ethical principles
const ETHICAL_PRINCIPLES = [
  "Fairness / non-discrimination",
  "Accountability",
  "Transparency",
  "Privacy & security",
  "Human oversight",
  "Do not currently reference specific principles"
];

// Data maturity levels
const DATA_MATURITY_LEVELS = [
  "Poor / fragmented",
  "Inconsistent but improving",
  "Managed with some standards",
  "Well-governed and reliable"
];

// AI capability levels
const AI_CAPABILITY_LEVELS = [
  "None",
  "Limited (rely on external partners)",
  "Some analytics / data skills",
  "Dedicated data / AI team"
];

// Current tools
const CURRENT_TOOLS = [
  "Business intelligence / reporting tools",
  "Workflow / process automation",
  "Chatbots or virtual assistants",
  "Predictive analytics",
  "None currently in use"
];

// POC status
const POC_STATUSES = [
  "No",
  "Yes, early ideas only",
  "Yes, defined use cases",
  "Unsure"
];

const defaultState = {
  // Organisation Details
  org_name: '',
  contact_name: '',
  contact_email: '',
  industry: '',
  org_size: '',
  business_unit: '',
  
  // Strategic Intent
  ai_motivation: '',
  leadership_commitment: '',
  ai_strategy_status: '',
  ai_risk_awareness: '',
  
  // Governance & Ethics
  governance_foundations: [],
  decision_ownership: '',
  ethical_principles: [],
  
  // Data & Capability
  data_maturity: '',
  ai_capability: '',
  current_tools: [],
  poc_status: '',
  
  // Assessment Details
  assessor_name: '',
  assessment_date: '',
  framework_version: 'v2025.11'
};

export default function ReadinessPreAssessmentForm() {
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
      'ai_motivation', 'leadership_commitment', 'ai_strategy_status', 'ai_risk_awareness',
      'decision_ownership', 'data_maturity', 'ai_capability', 'poc_status',
      'assessor_name', 'assessment_date', 'framework_version'
    ];

    for (const field of requiredFields) {
      if (!form[field]) {
        toast.error(`Please fill in all required fields`);
        setSubmitting(false);
        return;
      }
    }

    // Validate governance_foundations
    if (form.governance_foundations.length === 0) {
      toast.error('Please select at least one governance foundation');
      setSubmitting(false);
      return;
    }

    // Validate email format
    const emailRegex = /.+@.+\..+/;
    if (!emailRegex.test(form.contact_email)) {
      toast.error('Please enter a valid email address');
      setSubmitting(false);
      return;
    }

    try {
      await axios.put(`${API}/assessments/${assessmentId}/readiness-info`, form);
      toast.success('Readiness information saved!');
      navigate(`/assessment/${assessmentId}`);
    } catch (error) {
      console.error('Error saving readiness info:', error);
      toast.error(error.response?.data?.detail || 'Failed to save readiness information');
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
      <main className="max-w-4xl mx-auto px-4 sm:px-6 py-8">
        {/* Header */}
        <div className="flex items-center gap-3">
          <ClipboardList className="h-6 w-6" />
          <div>
            <h1 className="text-2xl font-semibold leading-tight">Pre-Assessment Onboarding</h1>
            <p className="text-sm text-muted-foreground">
              Provide a few details about your organisation so we can tailor the assessment and reporting.
            </p>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="mt-8 space-y-6">
          {/* Organisation Details */}
          <Card>
            <CardHeader className="bg-blue-50 border-b border-blue-100">
              <div className="flex items-center space-x-2">
                <Building2 className="h-5 w-5 text-blue-600" />
                <CardTitle className="text-xl">Organisation Details</CardTitle>
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
                <Label htmlFor="business_unit">Business unit / Department (optional)</Label>
                <Input
                  id="business_unit"
                  value={form.business_unit}
                  onChange={(e) => update('business_unit', e.target.value)}
                  placeholder="e.g., IT, Customer Service"
                />
              </div>
            </CardContent>
          </Card>

          {/* Strategic Intent */}
          <Card>
            <CardHeader className="bg-blue-50 border-b border-blue-100">
              <div className="flex items-center space-x-2">
                <Target className="h-5 w-5 text-blue-600" />
                <CardTitle className="text-xl">Strategic Intent</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label>Primary motivation to explore AI *</Label>
                <Select value={form.ai_motivation} onValueChange={(v) => update('ai_motivation', v)}>
                  <SelectTrigger><SelectValue placeholder="Select motivation" /></SelectTrigger>
                  <SelectContent>
                    {AI_MOTIVATIONS.map(motivation => (
                      <SelectItem key={motivation} value={motivation}>{motivation}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Leadership commitment to AI adoption *</Label>
                <Select value={form.leadership_commitment} onValueChange={(v) => update('leadership_commitment', v)}>
                  <SelectTrigger><SelectValue placeholder="Select commitment level" /></SelectTrigger>
                  <SelectContent>
                    {LEADERSHIP_COMMITMENTS.map(commitment => (
                      <SelectItem key={commitment} value={commitment}>{commitment}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>AI strategy or digital transformation roadmap *</Label>
                <Select value={form.ai_strategy_status} onValueChange={(v) => update('ai_strategy_status', v)}>
                  <SelectTrigger><SelectValue placeholder="Select status" /></SelectTrigger>
                  <SelectContent>
                    {AI_STRATEGY_STATUSES.map(status => (
                      <SelectItem key={status} value={status}>{status}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Current understanding of AI risks & ethics *</Label>
                <Select value={form.ai_risk_awareness} onValueChange={(v) => update('ai_risk_awareness', v)}>
                  <SelectTrigger><SelectValue placeholder="Select level" /></SelectTrigger>
                  <SelectContent>
                    {RISK_AWARENESS_LEVELS.map(level => (
                      <SelectItem key={level} value={level}>{level}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>

          {/* Governance & Ethics */}
          <Card>
            <CardHeader className="bg-blue-50 border-b border-blue-100">
              <div className="flex items-center space-x-2">
                <ShieldCheck className="h-5 w-5 text-blue-600" />
                <CardTitle className="text-xl">Governance & Ethics</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label>Existing governance foundations (select all that apply) *</Label>
                <div className="grid gap-2 md:grid-cols-2">
                  {GOVERNANCE_FOUNDATIONS.map(foundation => (
                    <div key={foundation} className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        id={`foundation_${foundation}`}
                        checked={form.governance_foundations.includes(foundation)}
                        onChange={() => toggleArrayItem('governance_foundations', foundation)}
                        className="h-4 w-4 rounded border-gray-300"
                      />
                      <label htmlFor={`foundation_${foundation}`} className="text-sm">{foundation}</label>
                    </div>
                  ))}
                </div>
              </div>

              <div className="space-y-2">
                <Label>Who currently approves new technology / AI initiatives? *</Label>
                <Select value={form.decision_ownership} onValueChange={(v) => update('decision_ownership', v)}>
                  <SelectTrigger><SelectValue placeholder="Select decision maker" /></SelectTrigger>
                  <SelectContent>
                    {DECISION_OWNERSHIP.map(owner => (
                      <SelectItem key={owner} value={owner}>{owner}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Ethical principles already referenced (optional)</Label>
                <div className="grid gap-2 md:grid-cols-2">
                  {ETHICAL_PRINCIPLES.map(principle => (
                    <div key={principle} className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        id={`principle_${principle}`}
                        checked={form.ethical_principles.includes(principle)}
                        onChange={() => toggleArrayItem('ethical_principles', principle)}
                        className="h-4 w-4 rounded border-gray-300"
                      />
                      <label htmlFor={`principle_${principle}`} className="text-sm">{principle}</label>
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Data & Capability */}
          <Card>
            <CardHeader className="flex flex-row items-center gap-3">
              <Database className="h-5 w-5" />
              <CardTitle style={{fontSize: '23px'}}>Data & Capability</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label>Current data quality & management *</Label>
                <Select value={form.data_maturity} onValueChange={(v) => update('data_maturity', v)}>
                  <SelectTrigger><SelectValue placeholder="Select maturity" /></SelectTrigger>
                  <SelectContent>
                    {DATA_MATURITY_LEVELS.map(level => (
                      <SelectItem key={level} value={level}>{level}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>In-house data / AI capability *</Label>
                <Select value={form.ai_capability} onValueChange={(v) => update('ai_capability', v)}>
                  <SelectTrigger><SelectValue placeholder="Select capability" /></SelectTrigger>
                  <SelectContent>
                    {AI_CAPABILITY_LEVELS.map(level => (
                      <SelectItem key={level} value={level}>{level}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Existing analytics / automation tools (optional)</Label>
                <div className="grid gap-2 md:grid-cols-2">
                  {CURRENT_TOOLS.map(tool => (
                    <div key={tool} className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        id={`tool_${tool}`}
                        checked={form.current_tools.includes(tool)}
                        onChange={() => toggleArrayItem('current_tools', tool)}
                        className="h-4 w-4 rounded border-gray-300"
                      />
                      <label htmlFor={`tool_${tool}`} className="text-sm">{tool}</label>
                    </div>
                  ))}
                </div>
              </div>

              <div className="space-y-2">
                <Label>Are AI pilots / proofs-of-concept being considered? *</Label>
                <Select value={form.poc_status} onValueChange={(v) => update('poc_status', v)}>
                  <SelectTrigger><SelectValue placeholder="Select status" /></SelectTrigger>
                  <SelectContent>
                    {POC_STATUSES.map(status => (
                      <SelectItem key={status} value={status}>{status}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>

          {/* Assessment Details */}
          <Card>
            <CardHeader className="flex flex-row items-center gap-3">
              <Calendar className="h-5 w-5" />
              <CardTitle style={{fontSize: '23px'}}>Assessment Details</CardTitle>
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
              className="bg-blue-600 hover:bg-blue-700"
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
