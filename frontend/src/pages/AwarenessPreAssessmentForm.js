import React, { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";
import { Badge } from "@/components/ui/badge";
import { Building2, Lightbulb, Target, Shield, ClipboardCheck, ArrowLeft } from "lucide-react";
import { toast } from 'sonner';
import axios from 'axios';
import Logo from '../components/Logo';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

/**
 * AwarenessPreAssessmentForm
 *
 * Pre-assessment form for the AI Awareness & Foundations Assessment.
 * Follows the same styling principles as SystemPreAssessmentForm.
 */

// Option helpers based on the JSON schema
const INDUSTRY_OPTIONS = [
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

const ORG_SIZE_OPTIONS = [
  "1–49",
  "50–249",
  "250–999",
  "1,000+"
];

const AI_FAMILIARITY_OPTIONS = [
  "None",
  "Basic awareness",
  "Moderate",
  "Good understanding"
];

const DIGITAL_STAGE_OPTIONS = [
  "Early / starting out",
  "Developing",
  "Established",
  "Advanced / data-driven"
];

const LEADERSHIP_INTEREST_OPTIONS = [
  "Not yet",
  "Occasionally",
  "Regularly",
  "Embedded in planning"
];

const COMFORT_LEVEL_OPTIONS = [
  "Low",
  "Moderate",
  "High"
];

const AWARENESS_REASON_OPTIONS = [
  "Learn AI fundamentals",
  "Gauge current awareness",
  "Educate staff / leadership",
  "Prepare for future AI assessments",
  "Support an upcoming AI initiative",
  "Other / not sure"
];

const AWARENESS_OUTCOMES = [
  "Understand AI basics and terminology",
  "Identify safe first steps",
  "Benchmark current awareness level",
  "Identify gaps before deeper assessments",
  "Get tailored learning recommendations",
  "Other"
];

const LEARNING_PREFERENCES = [
  "Short online explainers",
  "Live or virtual workshops",
  "Use-case examples and case studies",
  "Self-directed reading materials"
];

const GOVERNANCE_FOUNDATIONS = [
  "ICT / Cybersecurity policies",
  "Data governance practices",
  "Privacy policy / processes",
  "Values or ethics charter",
  "None of the above"
];

const DIGITAL_INITIATIVES_OPTIONS = [
  "None",
  "Basic upgrades (e.g., cloud, CRM)",
  "Some automation or analytics pilots",
  "Multiple ongoing digital initiatives"
];

const defaultState = {
  org_name: "",
  contact_name: "",
  contact_email: "",
  industry: "",
  org_size: "",
  business_unit: "",
  ai_familiarity: "",
  digital_maturity: "",
  leadership_ai_interest: "",
  tech_change_comfort: "",
  awareness_reason: "",
  awareness_outcomes: [],
  learning_preferences: [],
  governance_foundations: [],
  digital_initiatives_level: "",
  data_skill_confidence: "",
  openness_to_learning: "",
  assessor_name: "",
  assessment_date: "",
  framework_version: "v2025.11",
};

export default function AwarenessPreAssessmentForm() {
  const navigate = useNavigate();
  const { id } = useParams();
  const [form, setForm] = useState(defaultState);
  const [submitting, setSubmitting] = useState(false);

  function update(key, value) {
    setForm((f) => ({ ...f, [key]: value }));
  }

  function toggleInArray(key, value) {
    setForm((f) => {
      const arr = f[key] || [];
      const newArr = arr.includes(value)
        ? arr.filter((v) => v !== value)
        : [...arr, value];
      return { ...f, [key]: newArr };
    });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setSubmitting(true);
    try {
      // Save the awareness information to the assessment
      await axios.put(`${API}/assessments/${id}/awareness-info`, form);
      toast.success('Awareness information saved!');
      // Navigate to the assessment page
      navigate(`/assessment/${id}`);
    } catch (error) {
      console.error('Error saving awareness information:', error);
      toast.error('Failed to save awareness information');
    } finally {
      setSubmitting(false);
    }
  }

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
              type="button"
              variant="outline"
              onClick={() => navigate('/dashboard')}
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Dashboard
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <form onSubmit={handleSubmit} className="mx-auto max-w-6xl space-y-8 px-4 py-8">
        {/* Page Title */}
        <div className="text-center space-y-2">
          <h2 className="text-3xl font-bold text-gray-900">Pre-Assessment Onboarding</h2>
          <p className="text-gray-600">
            AI Awareness & Foundations Assessment - Please provide the following information
          </p>
        </div>

        {/* 1. Organisation Snapshot */}
        <Card>
          <CardHeader className="bg-green-50 border-b border-green-100">
            <div className="flex items-center space-x-2">
              <Building2 className="h-5 w-5 text-green-600" />
              <CardTitle className="text-xl">Organisation Snapshot</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="grid gap-6 p-6 md:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="org_name">Organisation name *</Label>
              <Input
                id="org_name"
                value={form.org_name}
                onChange={(e) => update("org_name", e.target.value)}
                required
                placeholder="Enter organisation name"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="contact_name">Primary contact name *</Label>
              <Input
                id="contact_name"
                value={form.contact_name}
                onChange={(e) => update("contact_name", e.target.value)}
                required
                placeholder="Enter contact name"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="contact_email">Primary contact email *</Label>
              <Input
                id="contact_email"
                type="email"
                value={form.contact_email}
                onChange={(e) => update("contact_email", e.target.value)}
                required
                placeholder="email@example.com"
              />
            </div>

            <div className="space-y-2">
              <Label>Industry / sector *</Label>
              <Select value={form.industry} onValueChange={(v) => update("industry", v)}>
                <SelectTrigger><SelectValue placeholder="Select industry" /></SelectTrigger>
                <SelectContent>
                  {INDUSTRY_OPTIONS.map((opt) => (
                    <SelectItem key={opt} value={opt}>{opt}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label>Organisation size (headcount) *</Label>
              <Select value={form.org_size} onValueChange={(v) => update("org_size", v)}>
                <SelectTrigger><SelectValue placeholder="Select size" /></SelectTrigger>
                <SelectContent>
                  {ORG_SIZE_OPTIONS.map((opt) => (
                    <SelectItem key={opt} value={opt}>{opt}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="business_unit">Business unit / department (optional)</Label>
              <Input
                id="business_unit"
                value={form.business_unit}
                onChange={(e) => update("business_unit", e.target.value)}
                placeholder="e.g., IT, Operations"
              />
            </div>
          </CardContent>
        </Card>

        {/* 2. Starting Point & Familiarity */}
        <Card>
          <CardHeader className="bg-green-50 border-b border-green-100">
            <div className="flex items-center space-x-2">
              <Lightbulb className="h-5 w-5 text-green-600" />
              <CardTitle className="text-xl">Starting Point & Familiarity</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="grid gap-6 p-6 md:grid-cols-2">
            <div className="space-y-2">
              <Label>How familiar is your organisation with AI? *</Label>
              <Select value={form.ai_familiarity} onValueChange={(v) => update("ai_familiarity", v)}>
                <SelectTrigger><SelectValue placeholder="Select familiarity level" /></SelectTrigger>
                <SelectContent>
                  {AI_FAMILIARITY_OPTIONS.map((opt) => (
                    <SelectItem key={opt} value={opt}>{opt}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label>Current stage of digital transformation *</Label>
              <Select value={form.digital_maturity} onValueChange={(v) => update("digital_maturity", v)}>
                <SelectTrigger><SelectValue placeholder="Select stage" /></SelectTrigger>
                <SelectContent>
                  {DIGITAL_STAGE_OPTIONS.map((opt) => (
                    <SelectItem key={opt} value={opt}>{opt}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label>Has leadership discussed or shown interest in AI? *</Label>
              <Select value={form.leadership_ai_interest} onValueChange={(v) => update("leadership_ai_interest", v)}>
                <SelectTrigger><SelectValue placeholder="Select level" /></SelectTrigger>
                <SelectContent>
                  {LEADERSHIP_INTEREST_OPTIONS.map((opt) => (
                    <SelectItem key={opt} value={opt}>{opt}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label>Current comfort level with technology change *</Label>
              <Select value={form.tech_change_comfort} onValueChange={(v) => update("tech_change_comfort", v)}>
                <SelectTrigger><SelectValue placeholder="Select comfort level" /></SelectTrigger>
                <SelectContent>
                  {COMFORT_LEVEL_OPTIONS.map((opt) => (
                    <SelectItem key={opt} value={opt}>{opt}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* 3. Motivation & Goals */}
        <Card>
          <CardHeader className="bg-green-50 border-b border-green-100">
            <div className="flex items-center space-x-2">
              <Target className="h-5 w-5 text-green-600" />
              <CardTitle className="text-xl">Motivation & Goals</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-6 p-6">
            <div className="space-y-2">
              <Label>Main reason for taking this assessment *</Label>
              <Select value={form.awareness_reason} onValueChange={(v) => update("awareness_reason", v)}>
                <SelectTrigger><SelectValue placeholder="Select reason" /></SelectTrigger>
                <SelectContent>
                  {AWARENESS_REASON_OPTIONS.map((opt) => (
                    <SelectItem key={opt} value={opt}>{opt}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-3">
              <Label>What outcomes are you hoping for? (select all that apply)</Label>
              <div className="grid gap-3 md:grid-cols-2">
                {AWARENESS_OUTCOMES.map((outcome) => (
                  <div key={outcome} className="flex items-start space-x-2">
                    <Checkbox
                      id={`outcome-${outcome}`}
                      checked={form.awareness_outcomes.includes(outcome)}
                      onCheckedChange={() => toggleInArray("awareness_outcomes", outcome)}
                    />
                    <Label
                      htmlFor={`outcome-${outcome}`}
                      className="text-sm font-normal leading-tight cursor-pointer"
                    >
                      {outcome}
                    </Label>
                  </div>
                ))}
              </div>
            </div>

            <div className="space-y-3">
              <Label>Preferred learning formats (select all that apply)</Label>
              <div className="grid gap-3 md:grid-cols-2">
                {LEARNING_PREFERENCES.map((pref) => (
                  <div key={pref} className="flex items-start space-x-2">
                    <Checkbox
                      id={`pref-${pref}`}
                      checked={form.learning_preferences.includes(pref)}
                      onCheckedChange={() => toggleInArray("learning_preferences", pref)}
                    />
                    <Label
                      htmlFor={`pref-${pref}`}
                      className="text-sm font-normal leading-tight cursor-pointer"
                    >
                      {pref}
                    </Label>
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* 4. Foundational Context */}
        <Card>
          <CardHeader className="bg-green-50 border-b border-green-100">
            <div className="flex items-center space-x-2">
              <Shield className="h-5 w-5 text-green-600" />
              <CardTitle className="text-xl">Foundational Context</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="grid gap-6 p-6 md:grid-cols-2">
            <div className="space-y-3 md:col-span-2">
              <Label>Existing governance / policy foundations * (select all that apply)</Label>
              <div className="grid gap-3 md:grid-cols-2">
                {GOVERNANCE_FOUNDATIONS.map((gov) => (
                  <div key={gov} className="flex items-start space-x-2">
                    <Checkbox
                      id={`gov-${gov}`}
                      checked={form.governance_foundations.includes(gov)}
                      onCheckedChange={() => toggleInArray("governance_foundations", gov)}
                    />
                    <Label
                      htmlFor={`gov-${gov}`}
                      className="text-sm font-normal leading-tight cursor-pointer"
                    >
                      {gov}
                    </Label>
                  </div>
                ))}
              </div>
            </div>

            <div className="space-y-2">
              <Label>Current level of digital / automation initiatives *</Label>
              <Select value={form.digital_initiatives_level} onValueChange={(v) => update("digital_initiatives_level", v)}>
                <SelectTrigger><SelectValue placeholder="Select level" /></SelectTrigger>
                <SelectContent>
                  {DIGITAL_INITIATIVES_OPTIONS.map((opt) => (
                    <SelectItem key={opt} value={opt}>{opt}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label>Confidence in staff data and digital skills *</Label>
              <Select value={form.data_skill_confidence} onValueChange={(v) => update("data_skill_confidence", v)}>
                <SelectTrigger><SelectValue placeholder="Select confidence level" /></SelectTrigger>
                <SelectContent>
                  {COMFORT_LEVEL_OPTIONS.map((opt) => (
                    <SelectItem key={opt} value={opt}>{opt}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2 md:col-span-2">
              <Label>Openness to future AI learning or pilot projects *</Label>
              <Select value={form.openness_to_learning} onValueChange={(v) => update("openness_to_learning", v)}>
                <SelectTrigger><SelectValue placeholder="Select openness level" /></SelectTrigger>
                <SelectContent>
                  {COMFORT_LEVEL_OPTIONS.map((opt) => (
                    <SelectItem key={opt} value={opt}>{opt}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* 5. Assessment Details */}
        <Card>
          <CardHeader className="bg-teal-50 border-b border-teal-100">
            <div className="flex items-center space-x-2">
              <ClipboardCheck className="h-5 w-5 text-teal-600" />
              <CardTitle className="text-xl">Assessment Details</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="grid gap-6 p-6 md:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="assessor_name">Assessment conducted by *</Label>
              <Input
                id="assessor_name"
                value={form.assessor_name}
                onChange={(e) => update("assessor_name", e.target.value)}
                required
                placeholder="Enter assessor name"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="assessment_date">Assessment date *</Label>
              <Input
                id="assessment_date"
                type="date"
                value={form.assessment_date}
                onChange={(e) => update("assessment_date", e.target.value)}
                required
              />
            </div>

            <div className="space-y-2 md:col-span-2">
              <Label htmlFor="framework_version">AM AI SAFE framework version *</Label>
              <Input
                id="framework_version"
                value={form.framework_version}
                onChange={(e) => update("framework_version", e.target.value)}
                required
                placeholder="e.g., v2025.11"
              />
            </div>
          </CardContent>
        </Card>

        {/* Submit Button */}
        <div className="flex justify-end space-x-4">
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
            className="bg-green-600 hover:bg-green-700"
          >
            {submitting ? (
              <div className="flex items-center space-x-2">
                <div className="loading-spinner w-4 h-4"></div>
                <span>Saving...</span>
              </div>
            ) : (
              'Next: Begin Assessment'
            )}
          </Button>
        </div>
      </form>
    </div>
  );
}
