import React, { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";
import { Switch } from "@/components/ui/switch";
import { Badge } from "@/components/ui/badge";
import { ClipboardList, Cpu, ShieldCheck, FileText, Settings2, Workflow, ArrowLeft } from "lucide-react";
import { toast } from 'sonner';
import axios from 'axios';
import Logo from '../components/Logo';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

/**
 * SystemPreAssessmentForm
 *
 * Pre-assessment form for the AI System Maturity Assessment.
 * - Grouped into logical sections
 * - Tailwind + shadcn/ui components
 */

// Option helpers
const LIFECYCLE_OPTIONS = [
  { value: "design", label: "Design" },
  { value: "development", label: "Development" },
  { value: "pilot", label: "Pilot" },
  { value: "production", label: "Production" },
  { value: "retired", label: "Retired" },
];

const MODEL_TYPES = [
  "NLP / Text (e.g., LLM)",
  "Computer Vision",
  "Predictive Analytics / Tabular",
  "Recommendation",
  "Speech / Voice",
  "Reinforcement Learning",
  "Rules-based Hybrid",
];

const OWNERSHIP = [
  "In-house",
  "Vendor / SaaS",
  "Open-source foundation model",
  "Co-developed (hybrid)",
];

const HOSTING = ["On‑prem", "Private Cloud", "Public Cloud", "SaaS"];

const CLOUD_PROVIDERS = [
  "Google Cloud Platform (GCP)",
  "Microsoft Azure",
  "Amazon Web Services (AWS)",
  "Other / Not Applicable",
];

const DATA_FLOW = ["Batch", "Real‑time", "Hybrid"];

const DATA_SENSITIVITY = [
  "Non-personal",
  "Personal",
  "Sensitive (health, biometrics, etc.)",
  "Mixed",
];

const OVERSIGHT = ["Human‑in‑the‑loop", "Human‑on‑the‑loop", "No formal oversight"];

const ARTEFACTS = [
  "Model Card",
  "Risk Register",
  "Privacy Impact Assessment (PIA)",
  "Bias / Fairness Audit",
  "Transparency Report",
  "Logging & Audit Trails",
];

const FRAMEWORKS = [
  "FAIRA (QLD)",
  "ISO/IEC 42001",
  "NIST AI RMF",
  "OECD AI Principles",
  "EU AI Act (applicability)",
  "Australian Privacy Principles (APPs)",
];

const REGULATIONS = [
  "GDPR",
  "Australian Privacy Act / APPs",
  "Sectoral (e.g., Health, Finance)",
  "Other / Not sure",
];

const defaultState = {
  systemName: "",
  description: "",
  owner: "",
  department: "",
  lifecycle: "",
  usersStakeholders: "",
  monthlyVolume: "",
  criticality: "",
  modelType: "",
  ownership: "",
  hosting: "",
  cloudProvider: "",
  cloudRegion: "",
  dataFlow: "",
  dataSensitivity: "",
  dataSources: "",
  representationNotes: "",
  hasRetentionPolicy: false,
  oversight: "",
  artefacts: [],
  frameworks: [],
  regulations: [],
  ethicsCommitments: "",
  sustainabilityGoals: "",
  dependencies: "",
  versionRef: "",
  evidenceRepoUrl: "",
};

export default function SystemPreAssessmentForm() {
  const navigate = useNavigate();
  const { id } = useParams(); // assessment ID from route
  const [form, setForm] = useState(defaultState);
  const [submitting, setSubmitting] = useState(false);

  function update(key, value) {
    setForm((f) => ({ ...f, [key]: value }));
  }

  function toggleInArray(key, value) {
    setForm((f) => {
      const arr = new Set(f[key] ?? []);
      arr.has(value) ? arr.delete(value) : arr.add(value);
      return { ...f, [key]: Array.from(arr) };
    });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setSubmitting(true);
    try {
      // Save the system information to the assessment
      await axios.put(`${API}/assessments/${id}/system-info`, form);
      toast.success('System information saved!');
      // Navigate to the assessment page
      navigate(`/assessment/${id}`);
    } catch (error) {
      console.error('Error saving system information:', error);
      toast.error('Failed to save system information');
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

      <form onSubmit={handleSubmit} className="mx-auto max-w-6xl space-y-8 px-4 py-8">
        {/* Header */}
        <div className="flex items-center gap-3">
          <ClipboardList className="h-6 w-6" />
          <div>
            <h1 className="text-2xl font-semibold leading-tight">Pre-Assessment Onboarding</h1>
            <p className="text-sm text-muted-foreground">
              Provide a few details about the AI system so we can tailor the assessment and reporting.
            </p>
          </div>
        </div>

        {/* System Overview */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <div className="flex items-center gap-3">
              <FileText className="h-5 w-5" />
              <CardTitle style={{fontSize: '23px'}}>System Overview</CardTitle>
            </div>
            <Badge variant="secondary">Required</Badge>
          </CardHeader>
          <CardContent className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="systemName">System name</Label>
              <Input id="systemName" value={form.systemName} onChange={(e) => update("systemName", e.target.value)}
                placeholder="e.g., SmartRecruit Chatbot" required />
            </div>

            <div className="space-y-2">
              <Label htmlFor="owner">System owner</Label>
              <Input id="owner" value={form.owner} onChange={(e) => update("owner", e.target.value)} placeholder="e.g., Jane Smith (Head of HR)" required />
            </div>

            <div className="space-y-2 md:col-span-2">
              <Label htmlFor="description">Purpose / description</Label>
              <Textarea id="description" value={form.description} onChange={(e) => update("description", e.target.value)}
                placeholder="What does this AI system do and why does it exist?" rows={3} />
            </div>

            <div className="space-y-2">
              <Label htmlFor="department">Department / business function</Label>
              <Input id="department" value={form.department} onChange={(e) => update("department", e.target.value)} placeholder="e.g., HR / People & Culture" />
            </div>

            <div className="space-y-2">
              <Label>Lifecycle stage</Label>
              <Select onValueChange={(v) => update("lifecycle", v)} value={form.lifecycle}>
                <SelectTrigger><SelectValue placeholder="Select stage" /></SelectTrigger>
                <SelectContent>
                  {LIFECYCLE_OPTIONS.map((o) => (
                    <SelectItem key={o.value} value={o.value}>{o.label}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* Lifecycle & Usage */}
        <Card>
          <CardHeader className="flex flex-row items-center gap-3">
            <Settings2 className="h-5 w-5" />
            <CardTitle style={{fontSize: '23px'}}>Lifecycle & Usage</CardTitle>
          </CardHeader>
          <CardContent className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="usersStakeholders">Primary users / stakeholders</Label>
              <Input id="usersStakeholders" value={form.usersStakeholders}
                onChange={(e) => update("usersStakeholders", e.target.value)} placeholder="e.g., HR staff, job applicants" />
            </div>

            <div className="space-y-2">
              <Label htmlFor="monthlyVolume">Monthly interactions / transactions</Label>
              <Input id="monthlyVolume" value={form.monthlyVolume}
                onChange={(e) => update("monthlyVolume", e.target.value)} placeholder="e.g., 5,000 / month" />
            </div>

            <div className="space-y-2">
              <Label>Business criticality</Label>
              <Select value={form.criticality} onValueChange={(v) => update("criticality", v)}>
                <SelectTrigger><SelectValue placeholder="Select level" /></SelectTrigger>
                <SelectContent>
                  {["Low","Moderate","High","Critical"].map((l) => (
                    <SelectItem key={l} value={l}>{l}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* Technical Setup */}
        <Card>
          <CardHeader className="flex flex-row items-center gap-3">
            <Cpu className="h-5 w-5" />
            <CardTitle style={{fontSize: '23px'}}>Technical Setup</CardTitle>
          </CardHeader>
          <CardContent className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2">
              <Label>AI type / model category</Label>
              <Select value={form.modelType} onValueChange={(v) => update("modelType", v)}>
                <SelectTrigger><SelectValue placeholder="Select type" /></SelectTrigger>
                <SelectContent>
                  {MODEL_TYPES.map((m) => (<SelectItem key={m} value={m}>{m}</SelectItem>))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label>Model origin / ownership</Label>
              <Select value={form.ownership} onValueChange={(v) => update("ownership", v)}>
                <SelectTrigger><SelectValue placeholder="Select ownership" /></SelectTrigger>
                <SelectContent>
                  {OWNERSHIP.map((o) => (<SelectItem key={o} value={o}>{o}</SelectItem>))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label>Hosting type</Label>
              <Select value={form.hosting} onValueChange={(v) => update("hosting", v)}>
                <SelectTrigger><SelectValue placeholder="Select hosting" /></SelectTrigger>
                <SelectContent>
                  {HOSTING.map((h) => (<SelectItem key={h} value={h}>{h}</SelectItem>))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label>Cloud provider</Label>
              <Select value={form.cloudProvider} onValueChange={(v) => update("cloudProvider", v)}>
                <SelectTrigger><SelectValue placeholder="Select provider" /></SelectTrigger>
                <SelectContent>
                  {CLOUD_PROVIDERS.map((c) => (<SelectItem key={c} value={c}>{c}</SelectItem>))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="cloudRegion">Primary region</Label>
              <Input id="cloudRegion" value={form.cloudRegion} onChange={(e) => update("cloudRegion", e.target.value)} placeholder="e.g., australia-southeast1 (Sydney)" />
            </div>

            <div className="space-y-2">
              <Label>Data flow</Label>
              <Select value={form.dataFlow} onValueChange={(v) => update("dataFlow", v)}>
                <SelectTrigger><SelectValue placeholder="Select data flow" /></SelectTrigger>
                <SelectContent>
                  {DATA_FLOW.map((d) => (<SelectItem key={d} value={d}>{d}</SelectItem>))}
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* Data Characteristics */}
        <Card>
          <CardHeader className="flex flex-row items-center gap-3">
            <ShieldCheck className="h-5 w-5" />
            <CardTitle style={{fontSize: '23px'}}>Data Characteristics</CardTitle>
          </CardHeader>
          <CardContent className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2">
              <Label>Data sensitivity</Label>
              <Select value={form.dataSensitivity} onValueChange={(v) => update("dataSensitivity", v)}>
                <SelectTrigger><SelectValue placeholder="Select sensitivity" /></SelectTrigger>
                <SelectContent>
                  {DATA_SENSITIVITY.map((s) => (<SelectItem key={s} value={s}>{s}</SelectItem>))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="dataSources">Primary data sources</Label>
              <Input id="dataSources" value={form.dataSources} onChange={(e) => update("dataSources", e.target.value)} placeholder="e.g., HRIS, candidate CVs, job boards" />
            </div>

            <div className="space-y-2 md:col-span-2">
              <Label htmlFor="representationNotes">Representation coverage (notes)</Label>
              <Textarea id="representationNotes" value={form.representationNotes}
                onChange={(e) => update("representationNotes", e.target.value)} placeholder="e.g., balanced by gender, geography; identified gaps" rows={3} />
            </div>

            <div className="flex items-center justify-between rounded-md border p-3 md:col-span-2">
              <div className="space-y-1">
                <Label>Data retention policy exists?</Label>
                <p className="text-xs text-muted-foreground">Indicates if formal retention & disposal controls are in place.</p>
              </div>
              <Switch checked={form.hasRetentionPolicy} onCheckedChange={(v) => update("hasRetentionPolicy", v)} />
            </div>
          </CardContent>
        </Card>

        {/* Governance & Oversight */}
        <Card>
          <CardHeader className="flex flex-row items-center gap-3">
            <Workflow className="h-5 w-5" />
            <CardTitle>Governance & Oversight</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <Label>Human oversight model</Label>
                <Select value={form.oversight} onValueChange={(v) => update("oversight", v)}>
                  <SelectTrigger><SelectValue placeholder="Select oversight" /></SelectTrigger>
                  <SelectContent>
                    {OVERSIGHT.map((o) => (<SelectItem key={o} value={o}>{o}</SelectItem>))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Regulatory obligations</Label>
                <div className="grid grid-cols-1 gap-2">
                  {REGULATIONS.map((r) => (
                    <label key={r} className="inline-flex items-center gap-2">
                      <Checkbox checked={form.regulations.includes(r)} onCheckedChange={() => toggleInArray("regulations", r)} />
                      <span className="text-sm">{r}</span>
                    </label>
                  ))}
                </div>
              </div>
            </div>

            <Separator />

            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <Label>Governance artefacts available</Label>
                <div className="grid grid-cols-1 gap-2">
                  {ARTEFACTS.map((a) => (
                    <label key={a} className="inline-flex items-center gap-2">
                      <Checkbox checked={form.artefacts.includes(a)} onCheckedChange={() => toggleInArray("artefacts", a)} />
                      <span className="text-sm">{a}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div className="space-y-2">
                <Label>Applicable frameworks / standards</Label>
                <div className="grid grid-cols-1 gap-2">
                  {FRAMEWORKS.map((f) => (
                    <label key={f} className="inline-flex items-center gap-2">
                      <Checkbox checked={form.frameworks.includes(f)} onCheckedChange={() => toggleInArray("frameworks", f)} />
                      <span className="text-sm">{f}</span>
                    </label>
                  ))}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Ethics & Sustainability */}
        <Card>
          <CardHeader>
            <CardTitle>Ethics & Sustainability</CardTitle>
          </CardHeader>
          <CardContent className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2 md:col-span-2">
              <Label htmlFor="ethicsCommitments">Ethical commitments / principles</Label>
              <Textarea id="ethicsCommitments" value={form.ethicsCommitments}
                onChange={(e) => update("ethicsCommitments", e.target.value)} placeholder="e.g., human-centric design, fairness, non-discrimination" rows={3} />
            </div>
            <div className="space-y-2 md:col-span-2">
              <Label htmlFor="sustainabilityGoals">Sustainability goals</Label>
              <Textarea id="sustainabilityGoals" value={form.sustainabilityGoals}
                onChange={(e) => update("sustainabilityGoals", e.target.value)} placeholder="e.g., track energy usage; reduce carbon by 20% YoY" rows={3} />
            </div>
          </CardContent>
        </Card>

        {/* Optional Advanced */}
        <Card>
          <CardHeader>
            <CardTitle>Optional (Advanced)</CardTitle>
          </CardHeader>
          <CardContent className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="dependencies">Third‑party dependencies / APIs</Label>
              <Textarea id="dependencies" value={form.dependencies}
                onChange={(e) => update("dependencies", e.target.value)} placeholder="e.g., OpenAI API, AWS Rekognition" rows={3} />
            </div>
            <div className="space-y-2">
              <Label htmlFor="versionRef">Version reference</Label>
              <Input id="versionRef" value={form.versionRef} onChange={(e) => update("versionRef", e.target.value)} placeholder="e.g., v1.2 (2025‑05)" />
            </div>
            <div className="space-y-2 md:col-span-2">
              <Label htmlFor="evidenceRepoUrl">Evidence repository URL (optional)</Label>
              <Input id="evidenceRepoUrl" value={form.evidenceRepoUrl} onChange={(e) => update("evidenceRepoUrl", e.target.value)} placeholder="e.g., https://company.sharepoint.com/sites/AI-Assurance" />
            </div>
          </CardContent>
        </Card>

        {/* Actions */}
        <div className="flex items-center justify-end gap-3">
          <Button type="button" variant="secondary" onClick={() => setForm(defaultState)}>Reset</Button>
          <Button type="submit" disabled={submitting} className="bg-teal-600 hover:bg-teal-700">
            {submitting ? "Saving..." : "Save & Start Assessment"}
          </Button>
        </div>
      </form>
    </div>
  );
}
