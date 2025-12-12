import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { ArrowLeft, ShieldCheck, Save, CheckCircle, AlertCircle, Check, Circle } from "lucide-react";
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
  A2_5_accuracy: null, // 1-5 scale
  A2_5_completeness: null,
  A2_5_reliability: null,
  A2_5_relevance: null,
  A2_5_timeliness: null,
  A2_6: "", // BIL (single select)
  A2_7: "", // regulated data (Yes/No)
  A2_7_regulation: "",
  A2_8: "", // user inputs required (Yes/No)
  A2_8_types: [], // if yes - input types (multiselect)
  
  // A3: Human Interface and Impact
  A3_1: [], // interface types (multiselect)
  A3_2_technical: null, // 1-5 scale
  A3_2_domain: null,
  A3_2_ai_literacy: null,
  A3_3: [], // impacted groups (multiselect)
  A3_3_other: "",
  A3_4: [], // notification methods (multiselect)
  A3_5a: [], // staff impacts (multiselect)
  A3_5b: null, // severity 1-5
  A3_6a: [], // group impacts (multiselect)
  A3_6b: null, // severity 1-3
  
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
  B1_1_individual: null, // 1-5 scale
  B1_1_organizational: null,
  B1_1_social: null,
  B1_1_environmental: null,
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
  B5_1_rating: null,
  B5_2: "", // disengage process (Yes/No)
  B5_3: "", // high-risk environment (Yes/No)
  B5_3_environments: [],
  
  // B6: Transparency and Explainability
  B6_1: null, // transparency 1-5
  B6_2: null, // explainability 1-5
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

export default function FairaAssessmentForm() {
  const navigate = useNavigate();
  const { id } = useParams();
  const [form, setForm] = useState(defaultState);
  const [submitting, setSubmitting] = useState(false);
  const [autoSaving, setAutoSaving] = useState(false);
  const [lastSaved, setLastSaved] = useState(null);
  const [showTooltip, setShowTooltip] = useState(false);

  // Calculate progress percentage - only count applicable fields
  const calculateProgress = () => {
    // List of conditional fields that should only count if their parent condition is met
    const conditionalFields = {
      'A1_3_other': () => form.A1_3.includes('Other'),
      'A1_6_actions': () => form.A1_6 === 'Yes',
      'A1_6_actions_other': () => form.A1_6 === 'Yes' && form.A1_6_actions.includes('Other'),
      'A1_7_other': () => form.A1_7.includes('Other'),
      'A2_4_other': () => form.A2_4.includes('Other'),
      'A2_7_regulation': () => form.A2_7 === 'Yes',
      'A2_8_types': () => form.A2_8 === 'Yes',
      'A3_3_other': () => form.A3_3.includes('Other'),
      'A4_5_scenarios': () => form.A4_5 === 'Yes',
      'A5_12_other': () => form.A5_12.includes('Other'),
      'B2_3_perspectives': () => form.B2_3 === 'Yes',
      'B2_3_perspectives_other': () => form.B2_3 === 'Yes' && form.B2_3_perspectives.includes('Other'),
      'B3_1_methods': () => form.B3_1 === 'Yes',
      'B3_2_groups': () => form.B3_2 === 'Yes' || form.B3_2 === 'Unknown',
      'B4_2_types': () => form.B4_2 === 'Yes',
      'B4_2_types_other': () => form.B4_2 === 'Yes' && form.B4_2_types.includes('Other'),
      'B5_1_rating': () => form.B5_1 === 'Yes',
      'B5_3_environments': () => form.B5_3 === 'Yes',
      'B6_4_describe': () => form.B6_4 === 'Yes',
      'B7_1_describe': () => form.B7_1 === 'Yes',
      'B8_4_safeguards': () => form.B8_4 === 'Yes'
    };

    // Calculate applicable fields
    let totalFields = 0;
    let filledFields = 0;

    Object.keys(defaultState).forEach(key => {
      // Check if this is a conditional field
      if (conditionalFields[key]) {
        // Only count if condition is met
        if (conditionalFields[key]()) {
          totalFields++;
          const value = form[key];
          if (value !== null && value !== undefined) {
            if (Array.isArray(value)) {
              if (value.length > 0) filledFields++;
            } else if (typeof value === 'number') {
              filledFields++;
            } else if (typeof value === 'boolean') {
              if (value) filledFields++;
            } else if (value && value.toString().trim() !== '') {
              filledFields++;
            }
          }
        }
      } else {
        // Always count non-conditional fields
        totalFields++;
        const value = form[key];
        if (value !== null && value !== undefined) {
          if (Array.isArray(value)) {
            if (value.length > 0) filledFields++;
          } else if (typeof value === 'number') {
            filledFields++;
          } else if (typeof value === 'boolean') {
            if (value) filledFields++;
          } else if (value && value.toString().trim() !== '') {
            filledFields++;
          }
        }
      }
    });

    return totalFields > 0 ? Math.round((filledFields / totalFields) * 100) : 0;
  };

  // Calculate section completion status
  const getSectionCompletion = () => {
    const sections = {
      'A1': ['A1_1', 'A1_2', 'A1_3', 'A1_4', 'A1_5', 'A1_6', 'A1_7', 'A1_8', 'A1_9'],
      'A2': ['A2_1', 'A2_2', 'A2_3', 'A2_4', 'A2_5_accuracy', 'A2_5_completeness', 'A2_5_reliability', 'A2_5_relevance', 'A2_5_timeliness', 'A2_6', 'A2_7', 'A2_8'],
      'A3': ['A3_1', 'A3_2_technical', 'A3_2_domain', 'A3_2_ai_literacy', 'A3_3', 'A3_4', 'A3_5a', 'A3_5b', 'A3_6a', 'A3_6b'],
      'A4': ['A4_1', 'A4_2', 'A4_3', 'A4_4', 'A4_5', 'A4_6', 'A4_7', 'A4_8'],
      'A5': ['A5_1', 'A5_2', 'A5_3', 'A5_4', 'A5_5', 'A5_6', 'A5_7', 'A5_8', 'A5_9', 'A5_10', 'A5_11', 'A5_12'],
      'B1': ['B1_1_individual', 'B1_1_organizational', 'B1_1_social', 'B1_1_environmental', 'B1_2', 'B1_3'],
      'B2': ['B2_1', 'B2_2_rights', 'B2_2_diversity', 'B2_2_autonomy', 'B2_3'],
      'B3': ['B3_1', 'B3_2'],
      'B4': ['B4_1', 'B4_2', 'B4_3'],
      'B5': ['B5_1', 'B5_2', 'B5_3'],
      'B6': ['B6_1', 'B6_2', 'B6_3', 'B6_4'],
      'B7': ['B7_1', 'B7_2'],
      'B8': ['B8_1', 'B8_2', 'B8_3', 'B8_4']
    };

    const conditionalFields = {
      'A1_3_other': () => form.A1_3.includes('Other'),
      'A1_6_actions': () => form.A1_6 === 'Yes',
      'A1_6_actions_other': () => form.A1_6 === 'Yes' && form.A1_6_actions.includes('Other'),
      'A1_7_other': () => form.A1_7.includes('Other'),
      'A2_4_other': () => form.A2_4.includes('Other'),
      'A2_7_regulation': () => form.A2_7 === 'Yes',
      'A2_8_types': () => form.A2_8 === 'Yes',
      'A3_3_other': () => form.A3_3.includes('Other'),
      'A4_5_scenarios': () => form.A4_5 === 'Yes',
      'A5_12_other': () => form.A5_12.includes('Other'),
      'B2_3_perspectives': () => form.B2_3 === 'Yes',
      'B2_3_perspectives_other': () => form.B2_3 === 'Yes' && form.B2_3_perspectives.includes('Other'),
      'B3_1_methods': () => form.B3_1 === 'Yes',
      'B3_2_groups': () => form.B3_2 === 'Yes' || form.B3_2 === 'Unknown',
      'B4_2_types': () => form.B4_2 === 'Yes',
      'B4_2_types_other': () => form.B4_2 === 'Yes' && form.B4_2_types.includes('Other'),
      'B5_1_rating': () => form.B5_1 === 'Yes',
      'B5_3_environments': () => form.B5_3 === 'Yes',
      'B6_4_describe': () => form.B6_4 === 'Yes',
      'B7_1_describe': () => form.B7_1 === 'Yes',
      'B8_4_safeguards': () => form.B8_4 === 'Yes'
    };

    const isFieldFilled = (key) => {
      const value = form[key];
      if (value === null || value === undefined) return false;
      if (Array.isArray(value)) return value.length > 0;
      if (typeof value === 'number') return true;
      if (typeof value === 'boolean') return value;
      return value && value.toString().trim() !== '';
    };

    const sectionStatus = {};
    Object.keys(sections).forEach(sectionId => {
      const fields = sections[sectionId];
      let totalApplicable = 0;
      let completed = 0;
      let firstUnanswered = null;

      fields.forEach(fieldId => {
        // Check if field is conditional
        if (conditionalFields[fieldId]) {
          if (conditionalFields[fieldId]()) {
            totalApplicable++;
            if (isFieldFilled(fieldId)) {
              completed++;
            } else if (!firstUnanswered) {
              firstUnanswered = fieldId;
            }
          }
        } else {
          totalApplicable++;
          if (isFieldFilled(fieldId)) {
            completed++;
          } else if (!firstUnanswered) {
            firstUnanswered = fieldId;
          }
        }
      });

      sectionStatus[sectionId] = {
        completed: totalApplicable > 0 && completed === totalApplicable,
        progress: totalApplicable > 0 ? Math.round((completed / totalApplicable) * 100) : 0,
        firstUnanswered
      };
    });

    return sectionStatus;
  };

  const scrollToField = (fieldId) => {
    const element = document.getElementById(fieldId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'center' });
      // Flash the field to draw attention
      element.classList.add('ring-2', 'ring-orange-400', 'rounded');
      setTimeout(() => {
        element.classList.remove('ring-2', 'ring-orange-400', 'rounded');
      }, 2000);
    }
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
    }, 3000); // Auto-save after 3 seconds of inactivity

    return () => clearTimeout(autoSaveTimer);
  }, [form]);

  const handleAutoSave = async () => {
    if (!id) return;
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
    
    if (!form.declaration_confirmed) {
      toast.error('Please confirm the declaration to complete the assessment');
      return;
    }
    
    setSubmitting(true);
    try {
      await axios.put(`${API}/assessments/${id}/faira-form`, { ...form, status: 'completed' });
      toast.success('FAIRA assessment completed successfully!');
      navigate(`/assessment/${id}`);
    } catch (error) {
      console.error('Submit error:', error);
      toast.error(error.response?.data?.detail || 'Failed to submit assessment');
    } finally {
      setSubmitting(false);
    }
  }

  const progress = calculateProgress();
  const sectionStatus = getSectionCompletion();
  const isComplete = progress === 100;

  const sectionsList = [
    { id: 'A1', name: 'A1. AI Solution Fundamentals' },
    { id: 'A2', name: 'A2. Data and Inputs' },
    { id: 'A3', name: 'A3. Human Interface and Impact' },
    { id: 'A4', name: 'A4. Outputs and Actions' },
    { id: 'A5', name: 'A5. Governance and Oversight' },
    { id: 'B1', name: 'B1. Human, Societal and Environmental Wellbeing' },
    { id: 'B2', name: 'B2. Human-Centred Values' },
    { id: 'B3', name: 'B3. Fairness' },
    { id: 'B4', name: 'B4. Privacy Protection and Security' },
    { id: 'B5', name: 'B5. Reliability and Safety' },
    { id: 'B6', name: 'B6. Transparency and Explainability' },
    { id: 'B7', name: 'B7. Contestability' },
    { id: 'B8', name: 'B8. Accountability' }
  ];

  // Helper component for radio scale
  const RadioScale = ({ value, onChange, min = 1, max = 5, labels = {} }) => (
    <div className="flex items-center space-x-4">
      {Array.from({ length: max - min + 1 }, (_, i) => min + i).map((num) => (
        <label key={num} className="flex flex-col items-center cursor-pointer">
          <input
            type="radio"
            checked={value === num}
            onChange={() => onChange(num)}
            className="h-4 w-4 text-orange-600 focus:ring-orange-500"
          />
          <span className="text-xs mt-1">{labels[num] || num}</span>
        </label>
      ))}
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-bg flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-sm border-b sticky top-0 z-20">
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

      {/* Main Content Area with Sidebar */}
      <div className="flex flex-1">
        {/* Sidebar */}
        <aside className="w-80 bg-white border-r shadow-sm sticky top-16 h-[calc(100vh-4rem)] overflow-y-auto hidden lg:block">
          <div className="p-6">
            <h3 className="text-sm font-semibold text-gray-900 mb-4 uppercase tracking-wider">Assessment Progress</h3>
            <div className="space-y-2">
              {sectionsList.map((section) => {
                const status = sectionStatus[section.id];
                const isCompleted = status?.completed;
                
                return (
                  <button
                    key={section.id}
                    type="button"
                    onClick={() => {
                      if (!isCompleted && status?.firstUnanswered) {
                        scrollToField(status.firstUnanswered);
                      }
                    }}
                    className={`w-full text-left px-3 py-2 rounded-lg transition-all flex items-start gap-2 ${
                      isCompleted 
                        ? 'bg-green-50 hover:bg-green-100 cursor-pointer' 
                        : 'bg-gray-50 hover:bg-orange-50 cursor-pointer'
                    }`}
                  >
                    <div className="flex-shrink-0 mt-0.5">
                      {isCompleted ? (
                        <div className="h-5 w-5 rounded-full bg-green-500 flex items-center justify-center">
                          <Check className="h-3 w-3 text-white" />
                        </div>
                      ) : (
                        <Circle className="h-5 w-5 text-gray-400" />
                      )}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className={`text-sm font-medium ${isCompleted ? 'text-green-700' : 'text-gray-700'}`}>
                        {section.name}
                      </p>
                      {!isCompleted && (
                        <p className="text-xs text-gray-500 mt-0.5">{status?.progress}% complete</p>
                      )}
                    </div>
                  </button>
                );
              })}
            </div>
            
            {/* Overall Progress Summary */}
            <div className="mt-6 p-4 bg-orange-50 rounded-lg border border-orange-200">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-semibold text-orange-900">Overall Progress</span>
                <span className="text-lg font-bold text-orange-600">{progress}%</span>
              </div>
              <div className="h-2 bg-orange-200 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-orange-500 transition-all duration-300"
                  style={{ width: `${progress}%` }}
                />
              </div>
            </div>
          </div>
        </aside>

        {/* Form Content */}
        <form onSubmit={handleSubmit} className="flex-1 max-w-5xl mx-auto p-6 space-y-8 pb-32">
        
        {/* BLOCK 1: Assessment Details */}
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

        {/* BLOCK 2: Part A - Components Analysis */}
        <Card>
          <CardHeader className="bg-orange-50 border-b border-orange-100">
            <CardTitle className="text-2xl font-bold">Part A: Components Analysis</CardTitle>
            <p className="text-sm text-gray-600 mt-1">Systematic breakdown of the AI solution components</p>
          </CardHeader>
          <CardContent className="p-6 space-y-8">
            
            {/* A1: AI Solution Fundamentals */}
            <div className="space-y-6" id="A1_1">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-1">A1. AI Solution Fundamentals</h3>
                <p className="text-sm text-gray-600">Maps to FAIRA Table 1: AI solution (Questions 1.1-1.10)</p>
              </div>
              <Separator />
              
              {/* A1.1 */}
              <div className="space-y-2">
                <Label>A1.1 What is the primary function of the AI solution? (Select all that apply)</Label>
                <div className="grid gap-2 md:grid-cols-2">
                  {[
                    "Information retrieval",
                    "Natural language understanding",
                    "Prediction / forecasting",
                    "Classification",
                    "Recommendation",
                    "Summarisation",
                    "Decision support",
                    "Process automation",
                    "Compliance monitoring",
                    "Content generation"
                  ].map((option) => (
                    <label key={option} className="flex items-center space-x-2">
                      <Checkbox
                        checked={form.A1_1.includes(option)}
                        onCheckedChange={() => toggleInArray("A1_1", option)}
                      />
                      <span className="text-sm">{option}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* A1.2 */}
              <div className="space-y-2">
                <Label htmlFor="A1_2">A1.2 What version of the AI solution does this FAIRA assessment apply to?</Label>
                <Input
                  id="A1_2"
                  value={form.A1_2}
                  onChange={(e) => update("A1_2", e.target.value)}
                  placeholder="e.g., v1.2.0"
                />
              </div>

              {/* A1.3 */}
              <div className="space-y-2">
                <Label>A1.3 Select all AI features that apply:</Label>
                <div className="grid gap-2 md:grid-cols-2">
                  {[
                    "Natural language processing",
                    "Data analysis and visualization",
                    "Automated content generation",
                    "Integration with existing systems",
                    "Personalized recommendations",
                    "Collaboration enhancement",
                    "Task automation",
                    "Security and compliance",
                    "Voice recognition"
                  ].map((option) => (
                    <label key={option} className="flex items-center space-x-2">
                      <Checkbox
                        checked={form.A1_3.includes(option)}
                        onCheckedChange={() => toggleInArray("A1_3", option)}
                      />
                      <span className="text-sm">{option}</span>
                    </label>
                  ))}
                  <label className="flex items-center space-x-2">
                    <Checkbox
                      checked={form.A1_3.includes("Other")}
                      onCheckedChange={() => toggleInArray("A1_3", "Other")}
                    />
                    <span className="text-sm">Other (specify)</span>
                  </label>
                </div>
                {form.A1_3.includes("Other") && (
                  <Input
                    value={form.A1_3_other}
                    onChange={(e) => update("A1_3_other", e.target.value)}
                    placeholder="Please specify other AI features"
                    className="mt-2"
                  />
                )}
              </div>

              {/* A1.4 */}
              <div className="space-y-2">
                <Label>A1.4 What decisions will be addressed by the AI functionality? (Select all that apply)</Label>
                <div className="grid gap-2 md:grid-cols-2">
                  {[
                    "Content development and approval",
                    "Data interpretation and business strategy",
                    "Prioritization of communications",
                    "Workflow optimization",
                    "Security and compliance oversight",
                    "Resource allocation",
                    "Crisis management",
                    "Employee training",
                    "Customer relationship management",
                    "Administrative decision-making (regulated by law)"
                  ].map((option) => (
                    <label key={option} className="flex items-center space-x-2">
                      <Checkbox
                        checked={form.A1_4.includes(option)}
                        onCheckedChange={() => toggleInArray("A1_4", option)}
                      />
                      <span className="text-sm">{option}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* A1.5 */}
              <div className="space-y-2">
                <Label>A1.5 What tangible benefits does this AI solution provide? (Select all that apply)</Label>
                <div className="grid gap-2 md:grid-cols-2">
                  {[
                    "Increased efficiency",
                    "Reduced manual effort",
                    "Improved decision-making",
                    "Faster processing time",
                    "Improved accuracy or consistency",
                    "Enhanced user experience",
                    "Cost reduction",
                    "Improved accessibility",
                    "Reduced risk or error",
                    "Better service delivery",
                    "Improved communication",
                    "Increased transparency"
                  ].map((option) => (
                    <label key={option} className="flex items-center space-x-2">
                      <Checkbox
                        checked={form.A1_5.includes(option)}
                        onCheckedChange={() => toggleInArray("A1_5", option)}
                      />
                      <span className="text-sm">{option}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* A1.6 */}
              <div className="space-y-3">
                <Label>A1.6 Can the AI solution convert decisions into actions without human intervention?</Label>
                <div className="flex space-x-4">
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.A1_6 === "Yes"}
                      onChange={() => update("A1_6", "Yes")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">Yes</span>
                  </label>
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.A1_6 === "No"}
                      onChange={() => update("A1_6", "No")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">No</span>
                  </label>
                </div>
                
                {form.A1_6 === "Yes" && (
                  <div className="ml-4 p-4 bg-gray-50 rounded-lg space-y-2">
                    <Label>Describe these actions (Select all that apply):</Label>
                    <div className="grid gap-2 md:grid-cols-2">
                      {[
                        "Sends notifications",
                        "Updates internal records",
                        "Applies rules/decisions automatically",
                        "Initiates workflows",
                        "Generates external communications",
                        "Allocates resources",
                        "Approves/declines items",
                        "Triggers system events"
                      ].map((option) => (
                        <label key={option} className="flex items-center space-x-2">
                          <Checkbox
                            checked={form.A1_6_actions.includes(option)}
                            onCheckedChange={() => toggleInArray("A1_6_actions", option)}
                          />
                          <span className="text-sm">{option}</span>
                        </label>
                      ))}
                      <label className="flex items-center space-x-2">
                        <Checkbox
                          checked={form.A1_6_actions.includes("Other")}
                          onCheckedChange={() => toggleInArray("A1_6_actions", "Other")}
                        />
                        <span className="text-sm">Other (specify)</span>
                      </label>
                    </div>
                    {form.A1_6_actions.includes("Other") && (
                      <Input
                        value={form.A1_6_actions_other}
                        onChange={(e) => update("A1_6_actions_other", e.target.value)}
                        placeholder="Please specify other actions"
                        className="mt-2"
                      />
                    )}
                  </div>
                )}
              </div>

              {/* A1.7 */}
              <div className="space-y-2">
                <Label>A1.7 What type of AI model or technique is used? (Select all that apply)</Label>
                <div className="grid gap-2 md:grid-cols-2">
                  {[
                    "Large Language Model",
                    "Computer Vision",
                    "Supervised learning",
                    "Unsupervised learning",
                    "Reinforcement learning",
                    "Rule-based system",
                    "Neural network"
                  ].map((option) => (
                    <label key={option} className="flex items-center space-x-2">
                      <Checkbox
                        checked={form.A1_7.includes(option)}
                        onCheckedChange={() => toggleInArray("A1_7", option)}
                      />
                      <span className="text-sm">{option}</span>
                    </label>
                  ))}
                  <label className="flex items-center space-x-2">
                    <Checkbox
                      checked={form.A1_7.includes("Other")}
                      onCheckedChange={() => toggleInArray("A1_7", "Other")}
                    />
                    <span className="text-sm">Other (specify)</span>
                  </label>
                </div>
                {form.A1_7.includes("Other") && (
                  <Input
                    value={form.A1_7_other}
                    onChange={(e) => update("A1_7_other", e.target.value)}
                    placeholder="Please specify other AI model types"
                    className="mt-2"
                  />
                )}
              </div>

              {/* A1.8 */}
              <div className="space-y-2">
                <Label>A1.8 What is the source of the AI solution? (Select all that apply)</Label>
                <div className="grid gap-2 md:grid-cols-2">
                  {[
                    "Commercial off-the-shelf",
                    "Bespoke development",
                    "Open-source",
                    "Hybrid approach"
                  ].map((option) => (
                    <label key={option} className="flex items-center space-x-2">
                      <Checkbox
                        checked={form.A1_8.includes(option)}
                        onCheckedChange={() => toggleInArray("A1_8", option)}
                      />
                      <span className="text-sm">{option}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* A1.9 */}
              <div className="space-y-2">
                <Label>A1.9 How does the AI solution integrate with other systems? (Select all that apply)</Label>
                <div className="grid gap-2 md:grid-cols-2">
                  {[
                    "REST API",
                    "Webhooks",
                    "Batch data transfer",
                    "Real-time data stream",
                    "File-based integration",
                    "Embedded widget/iframe",
                    "Database connection",
                    "Message queue (e.g., Kafka)"
                  ].map((option) => (
                    <label key={option} className="flex items-center space-x-2">
                      <Checkbox
                        checked={form.A1_9.includes(option)}
                        onCheckedChange={() => toggleInArray("A1_9", option)}
                      />
                      <span className="text-sm">{option}</span>
                    </label>
                  ))}
                </div>
              </div>
            </div>

            {/* A2: Data and Inputs */}
            <div className="space-y-6 pt-6 border-t" id="A2_1">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-1">A2. Data and Inputs</h3>
                <p className="text-sm text-gray-600">Maps to FAIRA 1.8-1.9 (data used and data quality) and AI use inputs (Table 3)</p>
              </div>
              <Separator />
              
              {/* A2.1 */}
              <div className="space-y-2">
                <Label>A2.1 How are AI use inputs tracked and recorded? (Select all that apply)</Label>
                <div className="grid gap-2 md:grid-cols-2">
                  {[
                    "Audit logs",
                    "Access logs",
                    "CRM/Case management logging",
                    "System-level logging",
                    "Manual records",
                    "No inputs tracked or recorded (flag as risk)"
                  ].map((option) => (
                    <label key={option} className="flex items-center space-x-2">
                      <Checkbox
                        checked={form.A2_1.includes(option)}
                        onCheckedChange={() => toggleInArray("A2_1", option)}
                      />
                      <span className="text-sm">{option}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* A2.2 */}
              <div className="space-y-2">
                <Label htmlFor="A2_2">A2.2 Does the AI require data from the digital or physical environment? If yes, what data and can users limit or trace it?</Label>
                <Textarea
                  id="A2_2"
                  value={form.A2_2}
                  onChange={(e) => update("A2_2", e.target.value)}
                  placeholder="Describe environmental data requirements and user controls"
                  rows={3}
                />
              </div>

              {/* A2.3 */}
              <div className="space-y-2">
                <Label>A2.3 What safeguards exist to detect and handle corrupted, missing, or out-of-range data inputs? (Select all that apply)</Label>
                <div className="grid gap-2 md:grid-cols-2">
                  {[
                    "Input validation",
                    "Range checking",
                    "Schema enforcement",
                    "Fallback defaults",
                    "Human review",
                    "Data quality monitoring",
                    "Error alerts",
                    "No safeguards identified (flag as risk)"
                  ].map((option) => (
                    <label key={option} className="flex items-center space-x-2">
                      <Checkbox
                        checked={form.A2_3.includes(option)}
                        onCheckedChange={() => toggleInArray("A2_3", option)}
                      />
                      <span className="text-sm">{option}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* A2.4 */}
              <div className="space-y-2">
                <Label>A2.4 What data does the AI solution use? (Select all that apply)</Label>
                <div className="grid gap-2 md:grid-cols-2">
                  {[
                    "Government data",
                    "Open data",
                    "Synthetic data",
                    "Personal information",
                    "Sensitive information",
                    "Internet data"
                  ].map((option) => (
                    <label key={option} className="flex items-center space-x-2">
                      <Checkbox
                        checked={form.A2_4.includes(option)}
                        onCheckedChange={() => toggleInArray("A2_4", option)}
                      />
                      <span className="text-sm">{option}</span>
                    </label>
                  ))}
                  <label className="flex items-center space-x-2">
                    <Checkbox
                      checked={form.A2_4.includes("Other")}
                      onCheckedChange={() => toggleInArray("A2_4", "Other")}
                    />
                    <span className="text-sm">Other (specify)</span>
                  </label>
                </div>
                {form.A2_4.includes("Other") && (
                  <Input
                    value={form.A2_4_other}
                    onChange={(e) => update("A2_4_other", e.target.value)}
                    placeholder="Please specify other data types"
                    className="mt-2"
                  />
                )}
              </div>

              {/* A2.5 */}
              <div className="space-y-4">
                <Label>A2.5 Rate the quality of the input data (1 = Very Low, 5 = Very High):</Label>
                <div className="space-y-3 ml-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium w-32">Accuracy:</span>
                    <RadioScale 
                      value={form.A2_5_accuracy} 
                      onChange={(val) => update("A2_5_accuracy", val)} 
                    />
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium w-32">Completeness:</span>
                    <RadioScale 
                      value={form.A2_5_completeness} 
                      onChange={(val) => update("A2_5_completeness", val)} 
                    />
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium w-32">Reliability:</span>
                    <RadioScale 
                      value={form.A2_5_reliability} 
                      onChange={(val) => update("A2_5_reliability", val)} 
                    />
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium w-32">Relevance:</span>
                    <RadioScale 
                      value={form.A2_5_relevance} 
                      onChange={(val) => update("A2_5_relevance", val)} 
                    />
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium w-32">Timeliness:</span>
                    <RadioScale 
                      value={form.A2_5_timeliness} 
                      onChange={(val) => update("A2_5_timeliness", val)} 
                    />
                  </div>
                </div>
              </div>

              {/* A2.6 */}
              <div className="space-y-2">
                <Label>A2.6 What is the Business Impact Level (BIL) of the input data?</Label>
                <select
                  value={form.A2_6}
                  onChange={(e) => update("A2_6", e.target.value)}
                  className="w-full p-2 border rounded-md"
                >
                  <option value="">Select BIL</option>
                  <option value="Official">Official</option>
                  <option value="Official: Sensitive">Official: Sensitive</option>
                  <option value="Protected">Protected</option>
                  <option value="Highly Protected">Highly Protected</option>
                  <option value="Secret">Secret</option>
                  <option value="Top Secret">Top Secret</option>
                </select>
              </div>

              {/* A2.7 */}
              <div className="space-y-3">
                <Label>A2.7 Does the solution use regulated data?</Label>
                <div className="flex space-x-4">
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.A2_7 === "Yes"}
                      onChange={() => update("A2_7", "Yes")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">Yes</span>
                  </label>
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.A2_7 === "No"}
                      onChange={() => update("A2_7", "No")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">No</span>
                  </label>
                </div>
                
                {form.A2_7 === "Yes" && (
                  <div className="ml-4 p-4 bg-gray-50 rounded-lg">
                    <Label htmlFor="A2_7_regulation">Specify the regulation:</Label>
                    <Input
                      id="A2_7_regulation"
                      value={form.A2_7_regulation}
                      onChange={(e) => update("A2_7_regulation", e.target.value)}
                      placeholder="e.g., GDPR, Privacy Act 1988"
                      className="mt-2"
                    />
                  </div>
                )}
              </div>

              {/* A2.8 */}
              <div className="space-y-3">
                <Label>A2.8 Does the solution require user inputs to operate?</Label>
                <div className="flex space-x-4">
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.A2_8 === "Yes"}
                      onChange={() => update("A2_8", "Yes")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">Yes</span>
                  </label>
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.A2_8 === "No"}
                      onChange={() => update("A2_8", "No")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">No</span>
                  </label>
                </div>
                
                {form.A2_8 === "Yes" && (
                  <div className="ml-4 p-4 bg-gray-50 rounded-lg space-y-2">
                    <Label>Select the types of inputs (Select all that apply):</Label>
                    <div className="grid gap-2 md:grid-cols-2">
                      {[
                        "Free-text prompts",
                        "Uploaded files",
                        "Form fields",
                        "API request data",
                        "Structured records",
                        "Voice input",
                        "Sensor data",
                        "User selection/choices",
                        "None"
                      ].map((option) => (
                        <label key={option} className="flex items-center space-x-2">
                          <Checkbox
                            checked={form.A2_8_types.includes(option)}
                            onCheckedChange={() => toggleInArray("A2_8_types", option)}
                          />
                          <span className="text-sm">{option}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* A3: Human Interface and Impact */}
            <div className="space-y-6 pt-6 border-t" id="A3_1">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-1">A3. Human Interface and Impact</h3>
                <p className="text-sm text-gray-600">Maps to FAIRA Table 2 (HMI) and Table 5 (Object of AI action)</p>
              </div>
              <Separator />
              
              {/* A3.1 */}
              <div className="space-y-2">
                <Label>A3.1 How does the system interface with humans? (Select all that apply)</Label>
                <div className="grid gap-2 md:grid-cols-2">
                  {[
                    "Chat interface",
                    "Web application",
                    "Mobile application",
                    "API integration",
                    "Voice interface",
                    "Dashboard"
                  ].map((option) => (
                    <label key={option} className="flex items-center space-x-2">
                      <Checkbox
                        checked={form.A3_1.includes(option)}
                        onCheckedChange={() => toggleInArray("A3_1", option)}
                      />
                      <span className="text-sm">{option}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* A3.2 */}
              <div className="space-y-4">
                <Label>A3.2 What expertise is required to use the AI solution? (1 = Very Low, 5 = Very High):</Label>
                <div className="space-y-3 ml-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium w-48">Technical expertise:</span>
                    <RadioScale 
                      value={form.A3_2_technical} 
                      onChange={(val) => update("A3_2_technical", val)} 
                    />
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium w-48">Domain knowledge:</span>
                    <RadioScale 
                      value={form.A3_2_domain} 
                      onChange={(val) => update("A3_2_domain", val)} 
                    />
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium w-48">AI literacy:</span>
                    <RadioScale 
                      value={form.A3_2_ai_literacy} 
                      onChange={(val) => update("A3_2_ai_literacy", val)} 
                    />
                  </div>
                </div>
              </div>

              {/* A3.3 */}
              <div className="space-y-2">
                <Label>A3.3 Who will be impacted by the AI system? (Select all that apply)</Label>
                <div className="grid gap-2 md:grid-cols-2">
                  {[
                    "Queensland Government employees",
                    "General public",
                    "Vulnerable communities",
                    "Children",
                    "Elderly",
                    "People with disabilities",
                    "Indigenous peoples",
                    "Small businesses"
                  ].map((option) => (
                    <label key={option} className="flex items-center space-x-2">
                      <Checkbox
                        checked={form.A3_3.includes(option)}
                        onCheckedChange={() => toggleInArray("A3_3", option)}
                      />
                      <span className="text-sm">{option}</span>
                    </label>
                  ))}
                  <label className="flex items-center space-x-2">
                    <Checkbox
                      checked={form.A3_3.includes("Other")}
                      onCheckedChange={() => toggleInArray("A3_3", "Other")}
                    />
                    <span className="text-sm">Other (specify)</span>
                  </label>
                </div>
                {form.A3_3.includes("Other") && (
                  <Input
                    value={form.A3_3_other}
                    onChange={(e) => update("A3_3_other", e.target.value)}
                    placeholder="Please specify other impacted groups"
                    className="mt-2"
                  />
                )}
              </div>

              {/* A3.4 */}
              <div className="space-y-2">
                <Label>A3.4 How will impacted parties be informed of AI use? (Select all that apply)</Label>
                <div className="grid gap-2 md:grid-cols-2">
                  {[
                    "Website notice",
                    "In-app notice",
                    "Email communication",
                    "Terms & conditions",
                    "Public-facing AI statement",
                    "Staff training",
                    "Consent/acknowledgement",
                    "No planned notifications (flag as risk)"
                  ].map((option) => (
                    <label key={option} className="flex items-center space-x-2">
                      <Checkbox
                        checked={form.A3_4.includes(option)}
                        onCheckedChange={() => toggleInArray("A3_4", option)}
                      />
                      <span className="text-sm">{option}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* A3.5 */}
              <div className="space-y-3">
                <Label>A3.5(a) What are the expected impacts of this AI solution on staff? (Select all that apply)</Label>
                <div className="grid gap-2 md:grid-cols-2">
                  {[
                    "Increased workload",
                    "Reduced workload",
                    "Reduced autonomy",
                    "Improved autonomy",
                    "De-skilling risk",
                    "Skill enhancement",
                    "Accountability ambiguity",
                    "Increased accountability clarity",
                    "Stress or psychological impact",
                    "Job redesign required",
                    "No significant impact"
                  ].map((option) => (
                    <label key={option} className="flex items-center space-x-2">
                      <Checkbox
                        checked={form.A3_5a.includes(option)}
                        onCheckedChange={() => toggleInArray("A3_5a", option)}
                      />
                      <span className="text-sm">{option}</span>
                    </label>
                  ))}
                </div>
                
                <div className="mt-4">
                  <Label>A3.5(b) Rate the overall severity of these impacts (1 = Very Low, 5 = Very High):</Label>
                  <div className="mt-2">
                    <RadioScale 
                      value={form.A3_5b} 
                      onChange={(val) => update("A3_5b", val)} 
                    />
                  </div>
                </div>
              </div>

              {/* A3.6 */}
              <div className="space-y-3">
                <Label>A3.6(a) How will each impacted group be affected? (Select all that apply)</Label>
                <div className="grid gap-2 md:grid-cols-2">
                  {[
                    "Service quality changes",
                    "Accessibility changes",
                    "Decision-making impacts",
                    "Delay reduction",
                    "Bias or fairness concerns",
                    "Data/privacy concerns",
                    "Security concerns",
                    "Communication changes",
                    "Risk of exclusion",
                    "Increased assistance/support",
                    "None/minimal impact"
                  ].map((option) => (
                    <label key={option} className="flex items-center space-x-2">
                      <Checkbox
                        checked={form.A3_6a.includes(option)}
                        onCheckedChange={() => toggleInArray("A3_6a", option)}
                      />
                      <span className="text-sm">{option}</span>
                    </label>
                  ))}
                </div>
                
                <div className="mt-4">
                  <Label>A3.6(b) Rate the overall severity of these impacts (1 = Minor, 2 = Moderate, 3 = Major):</Label>
                  <div className="mt-2">
                    <RadioScale 
                      value={form.A3_6b} 
                      onChange={(val) => update("A3_6b", val)} 
                      min={1}
                      max={3}
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* A4: Outputs and Actions */}
            <div className="space-y-6 pt-6 border-t" id="A4_1">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-1">A4. Outputs and Actions</h3>
                <p className="text-sm text-gray-600">Maps to FAIRA Table 4: AI use outputs</p>
              </div>
              <Separator />
              
              {/* A4.1 */}
              <div className="space-y-2">
                <Label>A4.1 What are the primary outputs of the AI system? (Select all that apply)</Label>
                <div className="grid gap-2 md:grid-cols-2">
                  {[
                    "Text responses",
                    "Visual outputs",
                    "Recommendations",
                    "Decisions",
                    "Data analysis",
                    "Predictions",
                    "Actions in systems"
                  ].map((option) => (
                    <label key={option} className="flex items-center space-x-2">
                      <Checkbox
                        checked={form.A4_1.includes(option)}
                        onCheckedChange={() => toggleInArray("A4_1", option)}
                      />
                      <span className="text-sm">{option}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* A4.2 */}
              <div className="space-y-2">
                <Label>A4.2 Are outputs sent to external systems without human review?</Label>
                <div className="flex space-x-4">
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.A4_2 === "Yes"}
                      onChange={() => update("A4_2", "Yes")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">Yes</span>
                  </label>
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.A4_2 === "No"}
                      onChange={() => update("A4_2", "No")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">No</span>
                  </label>
                </div>
              </div>

              {/* A4.3 */}
              <div className="space-y-2">
                <Label>A4.3 What is the Business Impact Level (BIL) of the outputs?</Label>
                <select
                  value={form.A4_3}
                  onChange={(e) => update("A4_3", e.target.value)}
                  className="w-full p-2 border rounded-md"
                >
                  <option value="">Select BIL</option>
                  <option value="Official">Official</option>
                  <option value="Official: Sensitive">Official: Sensitive</option>
                  <option value="Protected">Protected</option>
                  <option value="Highly Protected">Highly Protected</option>
                  <option value="Secret">Secret</option>
                  <option value="Top Secret">Top Secret</option>
                </select>
              </div>

              {/* A4.4 */}
              <div className="space-y-2">
                <Label>A4.4 How are AI outputs tracked and recorded? (Select all that apply)</Label>
                <div className="grid gap-2 md:grid-cols-2">
                  {[
                    "Stored in database",
                    "Logged in audit system",
                    "Logged in CRM/case system",
                    "Logged in activity logs",
                    "Not currently tracked (flag as risk)",
                    "Retention based on policy"
                  ].map((option) => (
                    <label key={option} className="flex items-center space-x-2">
                      <Checkbox
                        checked={form.A4_4.includes(option)}
                        onCheckedChange={() => toggleInArray("A4_4", option)}
                      />
                      <span className="text-sm">{option}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* A4.5 */}
              <div className="space-y-3">
                <Label>A4.5 Could any AI outputs allow unauthorised access to information?</Label>
                <div className="flex space-x-4">
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.A4_5 === "Yes"}
                      onChange={() => update("A4_5", "Yes")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">Yes</span>
                  </label>
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.A4_5 === "No"}
                      onChange={() => update("A4_5", "No")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">No</span>
                  </label>
                </div>
                
                {form.A4_5 === "Yes" && (
                  <div className="ml-4 p-4 bg-gray-50 rounded-lg space-y-2">
                    <Label>Select scenarios and mitigations (Select all that apply):</Label>
                    <div className="grid gap-2 md:grid-cols-2">
                      {[
                        "Misrouted outputs",
                        "Excessive data exposure",
                        "Output reveals sensitive attributes",
                        "Outputs sent to incorrect system",
                        "Injection or poisoning risk",
                        "None identified"
                      ].map((option) => (
                        <label key={option} className="flex items-center space-x-2">
                          <Checkbox
                            checked={form.A4_5_scenarios.includes(option)}
                            onCheckedChange={() => toggleInArray("A4_5_scenarios", option)}
                          />
                          <span className="text-sm">{option}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* A4.6 */}
              <div className="space-y-2">
                <Label>A4.6 Do outputs involve data regulated by law? (Select all that apply)</Label>
                <div className="grid gap-2 md:grid-cols-2">
                  {[
                    "Personal",
                    "Sensitive",
                    "Financial",
                    "Health",
                    "Child-related",
                    "Law enforcement",
                    "Indigenous data",
                    "Confidential government data",
                    "Operationally sensitive data"
                  ].map((option) => (
                    <label key={option} className="flex items-center space-x-2">
                      <Checkbox
                        checked={form.A4_6.includes(option)}
                        onCheckedChange={() => toggleInArray("A4_6", option)}
                      />
                      <span className="text-sm">{option}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* A4.7 */}
              <div className="space-y-2">
                <Label htmlFor="A4_7">A4.7 Do outputs contain personally identifiable information? Who can access it (internal / external)?</Label>
                <Textarea
                  id="A4_7"
                  value={form.A4_7}
                  onChange={(e) => update("A4_7", e.target.value)}
                  placeholder="Describe PII in outputs and access controls"
                  rows={3}
                />
              </div>

              {/* A4.8 */}
              <div className="space-y-2">
                <Label htmlFor="A4_8">A4.8 Are any AI outputs directly used to trigger actions with legal or regulatory effect? If yes, describe and justify.</Label>
                <Textarea
                  id="A4_8"
                  value={form.A4_8}
                  onChange={(e) => update("A4_8", e.target.value)}
                  placeholder="Describe legal/regulatory actions and justification"
                  rows={3}
                />
              </div>
            </div>

            {/* A5: Governance and Oversight */}
            <div className="space-y-6 pt-6 border-t" id="A5_1">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-1">A5. Governance and Oversight</h3>
                <p className="text-sm text-gray-600">Maps to FAIRA Table 9 (Monitoring & evaluation) plus accountability references</p>
              </div>
              <Separator />
              
              {/* A5.1 */}
              <div className="space-y-2">
                <Label>A5.1 Who is accountable for decisions made using this system?</Label>
                <select
                  value={form.A5_1}
                  onChange={(e) => update("A5_1", e.target.value)}
                  className="w-full p-2 border rounded-md"
                >
                  <option value="">Select role</option>
                  <option value="Product owner">Product owner</option>
                  <option value="System owner">System owner</option>
                  <option value="Executive sponsor">Executive sponsor</option>
                  <option value="Service manager">Service manager</option>
                  <option value="Data custodian">Data custodian</option>
                  <option value="Governance committee">Governance committee</option>
                  <option value="AI oversight board">AI oversight board</option>
                </select>
              </div>

              {/* A5.2 */}
              <div className="space-y-2">
                <Label htmlFor="A5_2">A5.2 How are AI use inputs and outputs tracked and recorded?</Label>
                <Textarea
                  id="A5_2"
                  value={form.A5_2}
                  onChange={(e) => update("A5_2", e.target.value)}
                  placeholder="Describe tracking mechanisms"
                  rows={3}
                />
              </div>

              {/* A5.3 */}
              <div className="space-y-2">
                <Label>A5.3 What monitoring and evaluation processes are in place? (Select all that apply)</Label>
                <div className="grid gap-2 md:grid-cols-2">
                  {[
                    "Regular system audits",
                    "Continuous performance monitoring",
                    "User feedback collection",
                    "Periodic stakeholder reviews"
                  ].map((option) => (
                    <label key={option} className="flex items-center space-x-2">
                      <Checkbox
                        checked={form.A5_3.includes(option)}
                        onCheckedChange={() => toggleInArray("A5_3", option)}
                      />
                      <span className="text-sm">{option}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* A5.4 */}
              <div className="space-y-2">
                <Label>A5.4 How frequently will monitoring and evaluation occur?</Label>
                <select
                  value={form.A5_4}
                  onChange={(e) => update("A5_4", e.target.value)}
                  className="w-full p-2 border rounded-md"
                >
                  <option value="">Select frequency</option>
                  <option value="weekly">Weekly</option>
                  <option value="monthly">Monthly</option>
                  <option value="quarterly">Quarterly</option>
                  <option value="annually">Annually</option>
                  <option value="event-driven">Event-driven</option>
                </select>
              </div>

              {/* A5.5 */}
              <div className="space-y-2">
                <Label>A5.5 Has the AI solution been subject to independent review?</Label>
                <div className="flex space-x-4">
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.A5_5 === "Yes"}
                      onChange={() => update("A5_5", "Yes")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">Yes</span>
                  </label>
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.A5_5 === "No"}
                      onChange={() => update("A5_5", "No")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">No</span>
                  </label>
                </div>
              </div>

              {/* A5.6 */}
              <div className="space-y-2">
                <Label>A5.6 Who is responsible for monitoring and evaluation?</Label>
                <select
                  value={form.A5_6}
                  onChange={(e) => update("A5_6", e.target.value)}
                  className="w-full p-2 border rounded-md"
                >
                  <option value="">Select role</option>
                  <option value="ICT operations">ICT operations</option>
                  <option value="Data science team">Data science team</option>
                  <option value="Risk/Compliance">Risk/Compliance</option>
                  <option value="Business owner">Business owner</option>
                  <option value="Vendor">Vendor</option>
                  <option value="Customer-facing staff">Customer-facing staff</option>
                  <option value="External auditor">External auditor</option>
                </select>
              </div>

              {/* A5.7 */}
              <div className="space-y-2">
                <Label>A5.7 How are stakeholders engaged in monitoring and evaluation? (Select all that apply)</Label>
                <div className="grid gap-2 md:grid-cols-2">
                  {[
                    "Workshops",
                    "Public consultation",
                    "Union consultation",
                    "Focus groups",
                    "User feedback sessions",
                    "Accessibility reviews",
                    "No engagements planned (flag as risk)"
                  ].map((option) => (
                    <label key={option} className="flex items-center space-x-2">
                      <Checkbox
                        checked={form.A5_7.includes(option)}
                        onCheckedChange={() => toggleInArray("A5_7", option)}
                      />
                      <span className="text-sm">{option}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* A5.8 */}
              <div className="space-y-2">
                <Label>A5.8 How are undesirable or harmful results detected? (Select all that apply)</Label>
                <div className="grid gap-2 md:grid-cols-2">
                  {[
                    "Alerting and monitoring",
                    "User complaints",
                    "Human review triggers",
                    "Automated anomaly detection",
                    "Escalation procedures",
                    "Incident response team",
                    "No defined contingencies (flag as risk)"
                  ].map((option) => (
                    <label key={option} className="flex items-center space-x-2">
                      <Checkbox
                        checked={form.A5_8.includes(option)}
                        onCheckedChange={() => toggleInArray("A5_8", option)}
                      />
                      <span className="text-sm">{option}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* A5.9 */}
              <div className="space-y-2">
                <Label>A5.9 Which values and principles informed the AI solution's design? (Select all that apply)</Label>
                <div className="grid gap-2 md:grid-cols-2">
                  {[
                    "Australia's AI Ethics Principles",
                    "Human Rights Act",
                    "Data governance policies",
                    "WHS",
                    "Accessibility standards",
                    "Agency ethics statements",
                    "Privacy principles",
                    "Risk management framework"
                  ].map((option) => (
                    <label key={option} className="flex items-center space-x-2">
                      <Checkbox
                        checked={form.A5_9.includes(option)}
                        onCheckedChange={() => toggleInArray("A5_9", option)}
                      />
                      <span className="text-sm">{option}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* A5.10 */}
              <div className="space-y-2">
                <Label htmlFor="A5_10">A5.10 Which sector-specific frameworks and obligations apply?</Label>
                <Textarea
                  id="A5_10"
                  value={form.A5_10}
                  onChange={(e) => update("A5_10", e.target.value)}
                  placeholder="e.g., health, policing, education frameworks"
                  rows={3}
                />
              </div>

              {/* A5.11 */}
              <div className="space-y-2">
                <Label>A5.11 Where will this AI solution be deployed?</Label>
                <select
                  value={form.A5_11}
                  onChange={(e) => update("A5_11", e.target.value)}
                  className="w-full p-2 border rounded-md"
                >
                  <option value="">Select deployment location</option>
                  <option value="Internal use only">Internal use only</option>
                  <option value="Internal + selected partners">Internal + selected partners</option>
                  <option value="Public-facing">Public-facing</option>
                  <option value="Citizen-facing high-sensitivity">Citizen-facing high-sensitivity</option>
                  <option value="Embedded in another product">Embedded in another product</option>
                  <option value="Multi-channel deployment">Multi-channel deployment</option>
                </select>
              </div>

              {/* A5.12 */}
              <div className="space-y-2">
                <Label>A5.12 Which national and international AI frameworks and standards apply? (Select all that apply)</Label>
                <div className="grid gap-2 md:grid-cols-2">
                  {[
                    "National Framework for the Assurance of AI in Government",
                    "Queensland Government Enterprise Architecture",
                    "ISO/IEC 42001",
                    "ISO 27001",
                    "ISO 31000",
                    "NIST AI RMF",
                    "OECD AI Principles",
                    "EU AI Act",
                    "Singapore MAF"
                  ].map((option) => (
                    <label key={option} className="flex items-center space-x-2">
                      <Checkbox
                        checked={form.A5_12.includes(option)}
                        onCheckedChange={() => toggleInArray("A5_12", option)}
                      />
                      <span className="text-sm">{option}</span>
                    </label>
                  ))}
                  <label className="flex items-center space-x-2">
                    <Checkbox
                      checked={form.A5_12.includes("Other")}
                      onCheckedChange={() => toggleInArray("A5_12", "Other")}
                    />
                    <span className="text-sm">Other (specify)</span>
                  </label>
                </div>
                {form.A5_12.includes("Other") && (
                  <Input
                    value={form.A5_12_other}
                    onChange={(e) => update("A5_12_other", e.target.value)}
                    placeholder="Please specify other frameworks"
                    className="mt-2"
                  />
                )}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* BLOCK 3: Part B - Values Assessment */}
        <Card>
          <CardHeader className="bg-orange-50 border-b border-orange-100">
            <CardTitle className="text-2xl font-bold">Part B: Values Assessment</CardTitle>
            <p className="text-sm text-gray-600 mt-1">Assessment against core values: ethics, fairness, privacy, reliability, transparency, and accountability</p>
          </CardHeader>
          <CardContent className="p-6 space-y-8">
            
            {/* B1: Human, Societal, and Environmental Wellbeing */}
            <div className="space-y-6" id="B1_1_individual">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-1">B1. Human, Societal, and Environmental Wellbeing</h3>
              </div>
              <Separator />
              
              {/* B1.1 */}
              <div className="space-y-4">
                <Label>B1.1 How will the AI solution benefit (1 = Very Low, 5 = Very High):</Label>
                <div className="space-y-3 ml-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium w-48">Individual wellbeing:</span>
                    <RadioScale 
                      value={form.B1_1_individual} 
                      onChange={(val) => update("B1_1_individual", val)} 
                    />
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium w-48">Organizational efficiency:</span>
                    <RadioScale 
                      value={form.B1_1_organizational} 
                      onChange={(val) => update("B1_1_organizational", val)} 
                    />
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium w-48">Social outcomes:</span>
                    <RadioScale 
                      value={form.B1_1_social} 
                      onChange={(val) => update("B1_1_social", val)} 
                    />
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium w-48">Environmental outcomes:</span>
                    <RadioScale 
                      value={form.B1_1_environmental} 
                      onChange={(val) => update("B1_1_environmental", val)} 
                    />
                  </div>
                </div>
              </div>

              {/* B1.2 */}
              <div className="space-y-2">
                <Label>B1.2 What negative impacts might arise from the AI solution? (Select all that apply)</Label>
                <div className="grid gap-2 md:grid-cols-2">
                  {[
                    "Privacy risks",
                    "Bias/discrimination",
                    "Transparency issues",
                    "Safety risks",
                    "Employment impacts",
                    "Social harm",
                    "Environmental impact",
                    "Accessibility issues",
                    "Legal/regulatory risks",
                    "Loss of trust"
                  ].map((option) => (
                    <label key={option} className="flex items-center space-x-2">
                      <Checkbox
                        checked={form.B1_2.includes(option)}
                        onCheckedChange={() => toggleInArray("B1_2", option)}
                      />
                      <span className="text-sm">{option}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* B1.3 */}
              <div className="space-y-2">
                <Label>B1.3 Will the AI solution affect employee employment?</Label>
                <div className="flex space-x-4">
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.B1_3 === "Yes"}
                      onChange={() => update("B1_3", "Yes")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">Yes</span>
                  </label>
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.B1_3 === "No"}
                      onChange={() => update("B1_3", "No")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">No</span>
                  </label>
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.B1_3 === "Unknown"}
                      onChange={() => update("B1_3", "Unknown")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">Unknown</span>
                  </label>
                </div>
              </div>
            </div>

            {/* B2: Human-Centered Values */}
            <div className="space-y-6 pt-6 border-t" id="B2_1">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-1">B2. Human-Centered Values</h3>
              </div>
              <Separator />
              
              {/* B2.1 */}
              <div className="space-y-2">
                <Label>B2.1 Has a Human Rights Impact Assessment been completed?</Label>
                <div className="flex space-x-4">
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.B2_1 === "Yes"}
                      onChange={() => update("B2_1", "Yes")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">Yes</span>
                  </label>
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.B2_1 === "No"}
                      onChange={() => update("B2_1", "No")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">No</span>
                  </label>
                </div>
              </div>

              {/* B2.2 */}
              <div className="space-y-4">
                <Label>B2.2 Rate the potential impact on:</Label>
                <div className="space-y-3 ml-4">
                  <div>
                    <span className="text-sm font-medium block mb-2">Human rights:</span>
                    <div className="flex space-x-4">
                      {["Positive", "Neutral", "Negative", "Unknown"].map((opt) => (
                        <label key={opt} className="flex items-center space-x-2">
                          <input
                            type="radio"
                            checked={form.B2_2_rights === opt}
                            onChange={() => update("B2_2_rights", opt)}
                            className="h-4 w-4 text-orange-600"
                          />
                          <span className="text-sm">{opt}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                  <div>
                    <span className="text-sm font-medium block mb-2">Diversity:</span>
                    <div className="flex space-x-4">
                      {["Positive", "Neutral", "Negative", "Unknown"].map((opt) => (
                        <label key={opt} className="flex items-center space-x-2">
                          <input
                            type="radio"
                            checked={form.B2_2_diversity === opt}
                            onChange={() => update("B2_2_diversity", opt)}
                            className="h-4 w-4 text-orange-600"
                          />
                          <span className="text-sm">{opt}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                  <div>
                    <span className="text-sm font-medium block mb-2">Individual autonomy:</span>
                    <div className="flex space-x-4">
                      {["Positive", "Neutral", "Negative", "Unknown"].map((opt) => (
                        <label key={opt} className="flex items-center space-x-2">
                          <input
                            type="radio"
                            checked={form.B2_2_autonomy === opt}
                            onChange={() => update("B2_2_autonomy", opt)}
                            className="h-4 w-4 text-orange-600"
                          />
                          <span className="text-sm">{opt}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              {/* B2.3 */}
              <div className="space-y-3">
                <Label>B2.3 Have diverse perspectives been incorporated in the design?</Label>
                <div className="flex space-x-4">
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.B2_3 === "Yes"}
                      onChange={() => update("B2_3", "Yes")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">Yes</span>
                  </label>
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.B2_3 === "No"}
                      onChange={() => update("B2_3", "No")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">No</span>
                  </label>
                </div>
                
                {form.B2_3 === "Yes" && (
                  <div className="ml-4 p-4 bg-gray-50 rounded-lg space-y-2">
                    <Label>Which perspectives? (Select all that apply):</Label>
                    <div className="grid gap-2 md:grid-cols-2">
                      {[
                        "People with disabilities",
                        "Cultural diversity",
                        "Gender diversity",
                        "Age diversity",
                        "Indigenous perspectives",
                        "Socioeconomic diversity"
                      ].map((option) => (
                        <label key={option} className="flex items-center space-x-2">
                          <Checkbox
                            checked={form.B2_3_perspectives.includes(option)}
                            onCheckedChange={() => toggleInArray("B2_3_perspectives", option)}
                          />
                          <span className="text-sm">{option}</span>
                        </label>
                      ))}
                      <label className="flex items-center space-x-2">
                        <Checkbox
                          checked={form.B2_3_perspectives.includes("Other")}
                          onCheckedChange={() => toggleInArray("B2_3_perspectives", "Other")}
                        />
                        <span className="text-sm">Other (specify)</span>
                      </label>
                    </div>
                    {form.B2_3_perspectives.includes("Other") && (
                      <Input
                        value={form.B2_3_perspectives_other}
                        onChange={(e) => update("B2_3_perspectives_other", e.target.value)}
                        placeholder="Please specify other perspectives"
                        className="mt-2"
                      />
                    )}
                  </div>
                )}
              </div>
            </div>

            {/* B3: Fairness */}
            <div className="space-y-6 pt-6 border-t" id="B3_1">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-1">B3. Fairness</h3>
              </div>
              <Separator />
              
              {/* B3.1 */}
              <div className="space-y-3">
                <Label>B3.1 Has the AI solution been tested for fairness and bias?</Label>
                <div className="flex space-x-4">
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.B3_1 === "Yes"}
                      onChange={() => update("B3_1", "Yes")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">Yes</span>
                  </label>
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.B3_1 === "No"}
                      onChange={() => update("B3_1", "No")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">No</span>
                  </label>
                </div>
                
                {form.B3_1 === "Yes" && (
                  <div className="ml-4 p-4 bg-gray-50 rounded-lg space-y-2">
                    <Label>Select testing methods (Select all that apply):</Label>
                    <div className="grid gap-2 md:grid-cols-2">
                      {[
                        "Statistical parity analysis",
                        "Disparate impact analysis",
                        "Dataset bias review",
                        "Model interpretability testing",
                        "Human review panels",
                        "Synthetic scenario testing",
                        "Accessibility testing",
                        "Penetration/security testing",
                        "Vendor-provided tests",
                        "Informal or ad-hoc checks only (no formal testing) (flag as risk)"
                      ].map((option) => (
                        <label key={option} className="flex items-center space-x-2">
                          <Checkbox
                            checked={form.B3_1_methods.includes(option)}
                            onCheckedChange={() => toggleInArray("B3_1_methods", option)}
                          />
                          <span className="text-sm">{option}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* B3.2 */}
              <div className="space-y-3">
                <Label>B3.2 Could the AI solution result in unfair discrimination?</Label>
                <div className="flex space-x-4">
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.B3_2 === "Yes"}
                      onChange={() => update("B3_2", "Yes")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">Yes</span>
                  </label>
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.B3_2 === "No"}
                      onChange={() => update("B3_2", "No")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">No</span>
                  </label>
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.B3_2 === "Unknown"}
                      onChange={() => update("B3_2", "Unknown")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">Unknown</span>
                  </label>
                </div>
                
                {(form.B3_2 === "Yes" || form.B3_2 === "Unknown") && (
                  <div className="ml-4 p-4 bg-gray-50 rounded-lg space-y-2">
                    <Label>Against which groups? (Select all that apply):</Label>
                    <div className="grid gap-2 md:grid-cols-2">
                      {[
                        "Age groups",
                        "People with disabilities",
                        "Racial or ethnic groups",
                        "Religious groups",
                        "Gender",
                        "Sexual orientation",
                        "Socioeconomic status"
                      ].map((option) => (
                        <label key={option} className="flex items-center space-x-2">
                          <Checkbox
                            checked={form.B3_2_groups.includes(option)}
                            onCheckedChange={() => toggleInArray("B3_2_groups", option)}
                          />
                          <span className="text-sm">{option}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* B4: Privacy Protection and Security */}
            <div className="space-y-6 pt-6 border-t" id="B4_1">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-1">B4. Privacy Protection and Security</h3>
              </div>
              <Separator />
              
              {/* B4.1 */}
              <div className="space-y-2">
                <Label>B4.1 Has a Privacy Impact Assessment been completed?</Label>
                <div className="flex space-x-4">
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.B4_1 === "Yes"}
                      onChange={() => update("B4_1", "Yes")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">Yes</span>
                  </label>
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.B4_1 === "No"}
                      onChange={() => update("B4_1", "No")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">No</span>
                  </label>
                </div>
              </div>

              {/* B4.2 */}
              <div className="space-y-3">
                <Label>B4.2 Does the system collect, use, or disclose personal information?</Label>
                <div className="flex space-x-4">
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.B4_2 === "Yes"}
                      onChange={() => update("B4_2", "Yes")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">Yes</span>
                  </label>
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.B4_2 === "No"}
                      onChange={() => update("B4_2", "No")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">No</span>
                  </label>
                </div>
                
                {form.B4_2 === "Yes" && (
                  <div className="ml-4 p-4 bg-gray-50 rounded-lg space-y-2">
                    <Label>Is this information (Select all that apply):</Label>
                    <div className="grid gap-2 md:grid-cols-2">
                      {[
                        "Identifiable",
                        "Sensitive",
                        "Health-related",
                        "Financial",
                        "Biometric"
                      ].map((option) => (
                        <label key={option} className="flex items-center space-x-2">
                          <Checkbox
                            checked={form.B4_2_types.includes(option)}
                            onCheckedChange={() => toggleInArray("B4_2_types", option)}
                          />
                          <span className="text-sm">{option}</span>
                        </label>
                      ))}
                      <label className="flex items-center space-x-2">
                        <Checkbox
                          checked={form.B4_2_types.includes("Other")}
                          onCheckedChange={() => toggleInArray("B4_2_types", "Other")}
                        />
                        <span className="text-sm">Other (specify)</span>
                      </label>
                    </div>
                    {form.B4_2_types.includes("Other") && (
                      <Input
                        value={form.B4_2_types_other}
                        onChange={(e) => update("B4_2_types_other", e.target.value)}
                        placeholder="Please specify other information types"
                        className="mt-2"
                      />
                    )}
                  </div>
                )}
              </div>

              {/* B4.3 */}
              <div className="space-y-2">
                <Label>B4.3 What security measures are in place? (Select all that apply)</Label>
                <div className="grid gap-2 md:grid-cols-2">
                  {[
                    "Access controls",
                    "Encryption",
                    "Security testing",
                    "Data anonymization",
                    "Privacy-enhancing technologies"
                  ].map((option) => (
                    <label key={option} className="flex items-center space-x-2">
                      <Checkbox
                        checked={form.B4_3.includes(option)}
                        onCheckedChange={() => toggleInArray("B4_3", option)}
                      />
                      <span className="text-sm">{option}</span>
                    </label>
                  ))}
                </div>
              </div>
            </div>

            {/* B5: Reliability and Safety */}
            <div className="space-y-6 pt-6 border-t" id="B5_1">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-1">B5. Reliability and Safety</h3>
              </div>
              <Separator />
              
              {/* B5.1 */}
              <div className="space-y-3">
                <Label>B5.1 Has the system been tested for reliability?</Label>
                <div className="flex space-x-4">
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.B5_1 === "Yes"}
                      onChange={() => update("B5_1", "Yes")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">Yes</span>
                  </label>
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.B5_1 === "No"}
                      onChange={() => update("B5_1", "No")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">No</span>
                  </label>
                </div>
                
                {form.B5_1 === "Yes" && (
                  <div className="ml-4 p-4 bg-gray-50 rounded-lg space-y-2">
                    <Label>Rate reliability test results (1 = Very Low, 5 = Very High):</Label>
                    <RadioScale 
                      value={form.B5_1_rating} 
                      onChange={(val) => update("B5_1_rating", val)} 
                    />
                  </div>
                )}
              </div>

              {/* B5.2 */}
              <div className="space-y-2">
                <Label>B5.2 Is there a process to disengage the system if issues arise?</Label>
                <div className="flex space-x-4">
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.B5_2 === "Yes"}
                      onChange={() => update("B5_2", "Yes")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">Yes</span>
                  </label>
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.B5_2 === "No"}
                      onChange={() => update("B5_2", "No")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">No</span>
                  </label>
                </div>
              </div>

              {/* B5.3 */}
              <div className="space-y-3">
                <Label>B5.3 Is this AI solution for use in high-risk environments?</Label>
                <div className="flex space-x-4">
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.B5_3 === "Yes"}
                      onChange={() => update("B5_3", "Yes")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">Yes</span>
                  </label>
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.B5_3 === "No"}
                      onChange={() => update("B5_3", "No")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">No</span>
                  </label>
                </div>
                
                {form.B5_3 === "Yes" && (
                  <div className="ml-4 p-4 bg-gray-50 rounded-lg space-y-2">
                    <Label>Which environments? (Select all that apply):</Label>
                    <div className="grid gap-2 md:grid-cols-2">
                      {[
                        "Essential services",
                        "Critical infrastructure",
                        "Health services",
                        "Education",
                        "Law enforcement",
                        "Administration of justice",
                        "Democratic processes"
                      ].map((option) => (
                        <label key={option} className="flex items-center space-x-2">
                          <Checkbox
                            checked={form.B5_3_environments.includes(option)}
                            onCheckedChange={() => toggleInArray("B5_3_environments", option)}
                          />
                          <span className="text-sm">{option}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* B6: Transparency and Explainability */}
            <div className="space-y-6 pt-6 border-t" id="B6_1">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-1">B6. Transparency and Explainability</h3>
              </div>
              <Separator />
              
              {/* B6.1 */}
              <div className="space-y-2">
                <Label>B6.1 How transparent is the AI solution's operation? (1 = Very Low, 5 = Very High):</Label>
                <RadioScale 
                  value={form.B6_1} 
                  onChange={(val) => update("B6_1", val)} 
                />
              </div>

              {/* B6.2 */}
              <div className="space-y-2">
                <Label>B6.2 Can the system explain its outputs or decisions? (1 = Very Low, 5 = Very High):</Label>
                <RadioScale 
                  value={form.B6_2} 
                  onChange={(val) => update("B6_2", val)} 
                />
              </div>

              {/* B6.3 */}
              <div className="space-y-2">
                <Label htmlFor="B6_3">B6.3 How will people be informed they are interacting with AI?</Label>
                <Textarea
                  id="B6_3"
                  value={form.B6_3}
                  onChange={(e) => update("B6_3", e.target.value)}
                  placeholder="Describe how AI interaction is communicated"
                  rows={3}
                />
              </div>

              {/* B6.4 */}
              <div className="space-y-3">
                <Label>B6.4 Are there limitations to explaining how the system works?</Label>
                <div className="flex space-x-4">
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.B6_4 === "Yes"}
                      onChange={() => update("B6_4", "Yes")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">Yes</span>
                  </label>
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.B6_4 === "No"}
                      onChange={() => update("B6_4", "No")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">No</span>
                  </label>
                </div>
                
                {form.B6_4 === "Yes" && (
                  <div className="ml-4 p-4 bg-gray-50 rounded-lg">
                    <Label htmlFor="B6_4_describe">Describe limitations:</Label>
                    <Textarea
                      id="B6_4_describe"
                      value={form.B6_4_describe}
                      onChange={(e) => update("B6_4_describe", e.target.value)}
                      placeholder="Describe the limitations"
                      rows={3}
                      className="mt-2"
                    />
                  </div>
                )}
              </div>
            </div>

            {/* B7: Contestability */}
            <div className="space-y-6 pt-6 border-t" id="B7_1">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-1">B7. Contestability</h3>
              </div>
              <Separator />
              
              {/* B7.1 */}
              <div className="space-y-3">
                <Label>B7.1 Is there a process for people to challenge AI outcomes?</Label>
                <div className="flex space-x-4">
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.B7_1 === "Yes"}
                      onChange={() => update("B7_1", "Yes")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">Yes</span>
                  </label>
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.B7_1 === "No"}
                      onChange={() => update("B7_1", "No")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">No</span>
                  </label>
                </div>
                
                {form.B7_1 === "Yes" && (
                  <div className="ml-4 p-4 bg-gray-50 rounded-lg">
                    <Label htmlFor="B7_1_describe">Describe the process:</Label>
                    <Textarea
                      id="B7_1_describe"
                      value={form.B7_1_describe}
                      onChange={(e) => update("B7_1_describe", e.target.value)}
                      placeholder="Describe the challenge process"
                      rows={3}
                      className="mt-2"
                    />
                  </div>
                )}
              </div>

              {/* B7.2 */}
              <div className="space-y-2">
                <Label>B7.2 How quickly can challenges be addressed?</Label>
                <select
                  value={form.B7_2}
                  onChange={(e) => update("B7_2", e.target.value)}
                  className="w-full p-2 border rounded-md"
                >
                  <option value="">Select timeframe</option>
                  <option value="Immediately">Immediately</option>
                  <option value="Within hours">Within hours</option>
                  <option value="Within days">Within days</option>
                  <option value="Within weeks">Within weeks</option>
                  <option value="Longer than weeks">Longer than weeks</option>
                  <option value="Unknown">Unknown</option>
                </select>
              </div>
            </div>

            {/* B8: Accountability */}
            <div className="space-y-6 pt-6 border-t">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-1">B8. Accountability</h3>
              </div>
              <Separator />
              
              {/* B8.1 */}
              <div className="space-y-2">
                <Label htmlFor="B8_1">B8.1 Who has oversight of the AI system?</Label>
                <Input
                  id="B8_1"
                  value={form.B8_1}
                  onChange={(e) => update("B8_1", e.target.value)}
                  placeholder="Name role or position"
                />
              </div>

              {/* B8.2 */}
              <div className="space-y-2">
                <Label>B8.2 Are clear roles and responsibilities established?</Label>
                <div className="flex space-x-4">
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.B8_2 === "Yes"}
                      onChange={() => update("B8_2", "Yes")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">Yes</span>
                  </label>
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.B8_2 === "No"}
                      onChange={() => update("B8_2", "No")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">No</span>
                  </label>
                </div>
              </div>

              {/* B8.3 */}
              <div className="space-y-2">
                <Label>B8.3 Have staff been trained on AI risk management?</Label>
                <div className="flex space-x-4">
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.B8_3 === "Yes"}
                      onChange={() => update("B8_3", "Yes")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">Yes</span>
                  </label>
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.B8_3 === "No"}
                      onChange={() => update("B8_3", "No")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">No</span>
                  </label>
                </div>
              </div>

              {/* B8.4 */}
              <div className="space-y-3">
                <Label>B8.4 Are there safeguards against overreliance on AI outputs?</Label>
                <div className="flex space-x-4">
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.B8_4 === "Yes"}
                      onChange={() => update("B8_4", "Yes")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">Yes</span>
                  </label>
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      checked={form.B8_4 === "No"}
                      onChange={() => update("B8_4", "No")}
                      className="h-4 w-4 text-orange-600"
                    />
                    <span className="text-sm">No</span>
                  </label>
                </div>
                
                {form.B8_4 === "Yes" && (
                  <div className="ml-4 p-4 bg-gray-50 rounded-lg space-y-2">
                    <Label>Select safeguards (Select all that apply):</Label>
                    <div className="grid gap-2 md:grid-cols-2">
                      {[
                        "Mandatory human review",
                        "Confidence thresholds",
                        "Explainability requirements",
                        "Training for staff",
                        "Decision override controls",
                        "System warnings",
                        "Monitoring of decision quality"
                      ].map((option) => (
                        <label key={option} className="flex items-center space-x-2">
                          <Checkbox
                            checked={form.B8_4_safeguards.includes(option)}
                            onCheckedChange={() => toggleInArray("B8_4_safeguards", option)}
                          />
                          <span className="text-sm">{option}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* BLOCK 4: Declaration */}
        <Card>
          <CardHeader className="bg-orange-50 border-b border-orange-100">
            <div className="flex items-center space-x-2">
              <AlertCircle className="h-5 w-5 text-orange-600" />
              <CardTitle className="text-xl">Declaration</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="p-6 space-y-4">
            <div className="flex items-start space-x-3 p-4 bg-amber-50 border border-amber-200 rounded-lg">
              <Checkbox
                id="declaration_confirmed"
                checked={form.declaration_confirmed}
                onCheckedChange={(checked) => update("declaration_confirmed", checked)}
                required
              />
              <Label htmlFor="declaration_confirmed" className="text-sm font-medium cursor-pointer">
                I confirm that the information provided in this FAIRA assessment is accurate to the best of my knowledge.
              </Label>
            </div>
            
            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="declaration_assessor">Name of assessor *</Label>
                <Input
                  id="declaration_assessor"
                  value={form.declaration_assessor}
                  onChange={(e) => update("declaration_assessor", e.target.value)}
                  required
                  placeholder="Enter your name"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="declaration_date">Date *</Label>
                <Input
                  id="declaration_date"
                  type="date"
                  value={form.declaration_date}
                  onChange={(e) => update("declaration_date", e.target.value)}
                  required
                />
              </div>
            </div>
          </CardContent>
        </Card>
        
        {/* Actions */}
        <div className="fixed bottom-0 left-0 lg:left-80 right-0 bg-white border-t shadow-lg z-10">
          <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between gap-3">
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
              <div 
                className="relative"
                onMouseEnter={() => !isComplete && setShowTooltip(true)}
                onMouseLeave={() => setShowTooltip(false)}
              >
                <Button 
                  type="submit" 
                  disabled={submitting || !isComplete}
                  className={`${isComplete ? 'bg-orange-600 hover:bg-orange-700' : 'bg-gray-400 cursor-not-allowed'}`}
                >
                  {submitting ? "Submitting..." : "Complete Assessment"}
                </Button>
                {!isComplete && showTooltip && (
                  <div className="absolute bottom-full mb-2 right-0 w-64 px-3 py-2 text-xs text-white bg-gray-900 rounded-lg shadow-lg">
                    Complete all required fields to finish the assessment.
                    <div className="absolute top-full right-4 -mt-1 border-4 border-transparent border-t-gray-900"></div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </form>
      </div>
    </div>
  );
}
