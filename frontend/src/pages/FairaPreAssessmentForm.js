import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, ShieldCheck, Save, CheckCircle } from "lucide-react";
import { toast } from 'sonner';
import axios from 'axios';
import Logo from '../components/Logo';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Default state with flat structure
const defaultState = {
  // Assessment Details
  assessor_name: "",
  assessor_role: "",
  assessor_branch: "",
  
  // A1: AI Solution Fundamentals
  A1_1: [], // primary function (multiselect)
  A1_2: "", // version
  A1_3: [], // AI features (multiselect)
  A1_3_other: "",
  A1_4: [], // decisions addressed (multiselect)
  A1_5: [], // tangible benefits (multiselect)
  A1_6: "", // convert to actions (Yes/No)
  A1_6_actions: [], // if yes - actions (multiselect)
  A1_6_actions_other: "",
  A1_7: [], // AI model type (multiselect)
  A1_7_other: "",
  A1_8: [], // source (multiselect)
  A1_9: [], // integration (multiselect)
  
  // A2: Data and Inputs
  A2_1: [], // tracking (multiselect)
  A2_2: "", // environmental data (text)
  A2_3: [], // safeguards (multiselect)
  A2_4: [], // data types (multiselect)
  A2_4_other: "",
  A2_5_accuracy: 3, // 1-5 scale
  A2_5_completeness: 3,
  A2_5_reliability: 3,
  A2_5_relevance: 3,
  A2_5_timeliness: 3,
  A2_6: "", // BIL (single select)
  A2_7: "", // regulated data (Yes/No)
  A2_7_regulation: "",
  A2_8: "", // user inputs required (Yes/No)
  A2_8_types: [], // if yes - input types (multiselect)
  
  // A3: Human Interface and Impact
  A3_1: [], // interface types (multiselect)
  A3_2_technical: 3, // 1-5 scale
  A3_2_domain: 3,
  A3_2_ai_literacy: 3,
  A3_3: [], // impacted groups (multiselect)
  A3_3_other: "",
  A3_4: [], // notification methods (multiselect)
  A3_5a: [], // staff impacts (multiselect)
  A3_5b: 3, // severity 1-5
  A3_6a: [], // group impacts (multiselect)
  A3_6b: 2, // severity 1-3
  
  // A4: Outputs and Actions
  A4_1: [], // primary outputs (multiselect)
  A4_2: "", // external without review (Yes/No)
  A4_3: "", // BIL outputs (single select)
  A4_4: [], // tracking outputs (multiselect)
  A4_5: "", // unauthorized access (Yes/No)
  A4_5_scenarios: [],
  A4_6: [], // regulated data (multiselect)
  A4_7: "", // PII access (text)
  A4_8: "", // legal/regulatory actions (text)
  
  // A5: Governance and Oversight
  A5_1: "", // accountability (single select)
  A5_2: "", // tracking method (text)
  A5_3: [], // monitoring processes (multiselect)
  A5_4: "", // frequency (single select)
  A5_5: "", // independent review (Yes/No)
  A5_6: "", // responsible role (single select)
  A5_7: [], // stakeholder engagement (multiselect)
  A5_8: [], // detecting harm (multiselect)
  A5_9: [], // values/principles (multiselect)
  A5_10: "", // sector frameworks (text)
  A5_11: "", // deployment location (single select)
  A5_12: [], // frameworks/standards (multiselect)
  A5_12_other: "",
  
  // B1: Human, Societal, and Environmental Wellbeing
  B1_1_individual: 3, // 1-5 scale
  B1_1_organizational: 3,
  B1_1_social: 3,
  B1_1_environmental: 3,
  B1_2: [], // negative impacts (multiselect)
  B1_3: "", // employment impact (Yes/No/Unknown)
  
  // B2: Human-Centered Values
  B2_1: "", // HRIA completed (Yes/No)
  B2_2_rights: "", // Positive/Neutral/Negative/Unknown
  B2_2_diversity: "",
  B2_2_autonomy: "",
  B2_3: "", // diverse perspectives (Yes/No)
  B2_3_perspectives: [],
  B2_3_perspectives_other: "",
  
  // B3: Fairness
  B3_1: "", // tested for fairness (Yes/No)
  B3_1_methods: [],
  B3_2: "", // unfair discrimination (Yes/No/Unknown)
  B3_2_groups: [],
  
  // B4: Privacy Protection and Security
  B4_1: "", // PIA completed (Yes/No)
  B4_2: "", // collects personal info (Yes/No)
  B4_2_types: [],
  B4_2_types_other: "",
  B4_3: [], // security measures (multiselect)
  
  // B5: Reliability and Safety
  B5_1: "", // tested for reliability (Yes/No)
  B5_1_rating: 3,
  B5_2: "", // disengage process (Yes/No)
  B5_3: "", // high-risk environment (Yes/No)
  B5_3_environments: [],
  
  // B6: Transparency and Explainability
  B6_1: 3, // transparency 1-5
  B6_2: 3, // explainability 1-5
  B6_3: "", // how informed (text)
  B6_4: "", // limitations (Yes/No)
  B6_4_describe: "",
  
  // B7: Contestability
  B7_1: "", // challenge process (Yes/No)
  B7_1_describe: "",
  B7_2: "", // response time (select)
  
  // B8: Accountability
  B8_1: "", // oversight (text)
  B8_2: "", // roles established (Yes/No)
  B8_3: "", // staff trained (Yes/No)
  B8_4: "", // safeguards (Yes/No)
  B8_4_safeguards: [],
  
  // Declaration
  declaration_confirmed: false,
  declaration_assessor: "",
  declaration_date: new Date().toISOString().split('T')[0]
};

export default function FairaPreAssessmentForm() {
  const navigate = useNavigate();
  const { id } = useParams();
  const [form, setForm] = useState(defaultState);
  const [submitting, setSubmitting] = useState(false);
  const [autoSaving, setAutoSaving] = useState(false);
  const [lastSaved, setLastSaved] = useState(null);

  // Calculate progress percentage
  const calculateProgress = () => {
    const totalFields = Object.keys(defaultState).length;
    const filledFields = Object.keys(form).filter(key => {
      const value = form[key];
      if (Array.isArray(value)) return value.length > 0;
      if (typeof value === 'number') return true;
      if (typeof value === 'boolean') return value;
      return value && value.toString().trim() !== '';
    }).length;
    return Math.round((filledFields / totalFields) * 100);
  };

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

  // Auto-save functionality
  useEffect(() => {
    const autoSaveTimer = setTimeout(() => {
      if (id && !submitting) {
        handleAutoSave();
      }
    }, 2000); // Auto-save after 2 seconds of inactivity

    return () => clearTimeout(autoSaveTimer);
  }, [form]);

  const handleAutoSave = async () => {
    setAutoSaving(true);
    try {
      await axios.put(`${API}/assessments/${id}/faira-form`, form);
      setLastSaved(new Date());
    } catch (error) {
      console.error('Auto-save error:', error);
    } finally {
      setAutoSaving(false);
    }
  };

  const handleSaveDraft = async () => {
    setSubmitting(true);
    try {
      await axios.put(`${API}/assessments/${id}/faira-form`, form);
      toast.success('Draft saved successfully!');
      setLastSaved(new Date());
    } catch (error) {
      console.error('Save draft error:', error);
      toast.error('Failed to save draft');
    } finally {
      setSubmitting(false);
    }
  };

  async function handleSubmit(e) {
    e.preventDefault();
    setSubmitting(true);
    try {
      await axios.put(`${API}/assessments/${id}/faira-form`, { ...form, status: 'completed' });
      toast.success('FAIRA assessment form completed!');
      navigate(`/assessment/${id}`);
    } catch (error) {
      console.error('Submit error:', error);
      toast.error(error.response?.data?.detail || 'Failed to submit form');
    } finally {
      setSubmitting(false);
    }
  }

  const progress = calculateProgress();

  return (
    <div className="min-h-screen bg-gradient-bg">
      {/* Header */}
      <header className="bg-white shadow-sm border-b sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <Logo className="h-10 w-10" />
              <div>
                <h1 className="text-xl font-bold text-gray-900">FAIRA Risk Assessment</h1>
                <p className="text-xs text-orange-600 font-medium">Foundational AI Risk Assessment Framework</p>
              </div>
            </div>
            
            {/* Progress Indicator */}
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <span className="text-sm text-gray-600">Progress:</span>
                <Badge variant="secondary" className="bg-orange-100 text-orange-700">
                  {progress}%
                </Badge>
              </div>
              {autoSaving && (
                <span className="text-xs text-gray-500 flex items-center">
                  <Save className="h-3 w-3 mr-1 animate-pulse" />
                  Saving...
                </span>
              )}
              {lastSaved && !autoSaving && (
                <span className="text-xs text-green-600 flex items-center">
                  <CheckCircle className="h-3 w-3 mr-1" />
                  Saved {new Date(lastSaved).toLocaleTimeString()}
                </span>
              )}
              <Button 
                variant="outline" 
                size="sm"
                onClick={() => navigate('/dashboard')}
              >
                <ArrowLeft className="h-4 w-4 mr-2" />
                Dashboard
              </Button>
            </div>
          </div>
          
          {/* Progress Bar */}
          <div className="h-1 bg-gray-200">
            <div 
              className="h-full bg-orange-500 transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      </header>

      {/* Form Content */}
      <form onSubmit={handleSubmit} className="max-w-5xl mx-auto p-6 space-y-6">
        
        {/* Assessment Details */}
        <Card>
          <CardHeader className="bg-orange-50 border-b border-orange-100">
            <div className="flex items-center space-x-2">
              <ShieldCheck className="h-5 w-5 text-orange-600" />
              <CardTitle className="text-xl">Assessment Details</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="grid gap-4 p-6 md:grid-cols-3">
            <div className="space-y-2">
              <Label htmlFor="assessor_name">Assessor Name *</Label>
              <Input
                id="assessor_name"
                value={form.assessor_name}
                onChange={(e) => update("assessor_name", e.target.value)}
                required
                placeholder="Enter your name"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="assessor_role">Role *</Label>
              <Input
                id="assessor_role"
                value={form.assessor_role}
                onChange={(e) => update("assessor_role", e.target.value)}
                required
                placeholder="Enter your role"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="assessor_branch">Branch *</Label>
              <Input
                id="assessor_branch"
                value={form.assessor_branch}
                onChange={(e) => update("assessor_branch", e.target.value)}
                required
                placeholder="Enter your branch"
              />
            </div>
          </CardContent>
        </Card>

        {/* Continue with remaining sections... */}
        {/* This is a template - I'll create the full form in the next message */}
        
        {/* Actions */}
        <div className="flex items-center justify-between gap-3 sticky bottom-0 bg-white p-4 border-t shadow-lg rounded-lg">
          <Button 
            type="button" 
            variant="outline" 
            onClick={handleSaveDraft}
            disabled={submitting}
          >
            <Save className="h-4 w-4 mr-2" />
            Save Draft
          </Button>
          <div className="flex gap-3">
            <Button 
              type="button" 
              variant="secondary" 
              onClick={() => setForm(defaultState)}
            >
              Reset
            </Button>
            <Button 
              type="submit" 
              disabled={submitting || !form.declaration_confirmed}
              className="bg-orange-600 hover:bg-orange-700"
            >
              {submitting ? "Submitting..." : "Complete Assessment"}
            </Button>
          </div>
        </div>
      </form>
    </div>
  );
}
