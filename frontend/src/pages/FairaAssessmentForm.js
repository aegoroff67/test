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

// Import refactored section components
import {
  RadioScale,
  AssessmentOverview,
  SectionA1,
  SectionA2,
  SectionA3,
  SectionA4,
  SectionA5
} from '../components/faira-sections';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Default state with flat structure
const defaultState = {
  // Assessment Overview - A. Assessment Information
  ai_system_name: "",
  ai_system_version: "",
  business_unit: "",
  system_owner_name: "",
  system_owner_role: "",
  
  // Assessment Overview - B. Assessor Information
  assessor_name: "",
  assessor_role: "",
  assessor_branch: "",
  assessor_email: "",
  
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
  A2_2: "", // gate question: Does AI require environmental data? (Yes/No)
  A2_2_sources: [], // A2.2a data sources (multiselect)
  A2_2_sources_other: "", // A2.2a other data sources
  A2_2_data_types: [], // A2.2b data types ingested (multiselect)
  A2_2_data_types_other: "", // A2.2b other data types
  A2_2_user_limits: "", // A2.2c can users limit data (single select)
  A2_2_traceability: "", // A2.2d traceability to source (single select)
  A2_2_trace_mechanisms: [], // A2.2e traceability mechanisms (multiselect)
  A2_2_notes: "", // A2.2f optional notes
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
  A2_7_data_types: [], // types of regulated/sensitive data
  A2_7_data_types_other: "", // other regulated/sensitive data
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
  A4_6: "", // regulated data (Yes/No)
  A4_6_data_types: [], // regulated data types (multiselect)
  A4_7: "", // PII in outputs gate question (Yes/No)
  A4_7_pii_types: [], // A4.7a PII categories (multiselect)
  A4_7_pii_types_other: "", // A4.7a other PII types
  A4_7_access_scope: "", // A4.7b access scope (single select)
  A4_7_access_controls: [], // A4.7c access controls (multiselect)
  A4_7_notes: "", // A4.7d optional notes
  A4_8: "", // legal/regulatory actions gate question (Yes/No)
  A4_8_action_types: [], // A4.8a action types (multiselect)
  A4_8_action_types_other: "", // A4.8a other action types
  A4_8_trigger_pathway: "", // A4.8b trigger pathway (single select)
  A4_8_affected_parties: [], // A4.8c affected parties (multiselect)
  A4_8_decision_records: [], // A4.8d decision records (multiselect)
  A4_8_review_appeal: "", // A4.8e review/appeal pathway (single select)
  A4_8_legal_basis: [], // A4.8f legal basis (multiselect)
  A4_8_legal_basis_other: "", // A4.8f other legal basis
  A4_8_notes: "", // A4.8g optional notes
  
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
  A5_10: "", // sector frameworks (Yes/No)
  A5_10_commonwealth: [], // Commonwealth legislation
  A5_10_qld: [], // Queensland legislation
  A5_10_sector: [], // Sector-specific obligations
  A5_10_frameworks: [], // Frameworks and standards
  A5_10_frameworks_other: "", // Other frameworks specify
  A5_10_other: "", // Other regulations text
  A5_10_impact: "", // Impact description
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
  declaration_name: "",
  declaration_date: new Date().toISOString().split('T')[0],
  declaration_role: ""
};

export default function FairaAssessmentForm() {
  const navigate = useNavigate();
  const { id } = useParams();
  const [form, setForm] = useState(defaultState);
  const [submitting, setSubmitting] = useState(false);
  const [autoSaving, setAutoSaving] = useState(false);
  const [lastSaved, setLastSaved] = useState(null);
  const [showTooltip, setShowTooltip] = useState(false);
  const [loading, setLoading] = useState(true);

  // Fetch existing form data on mount
  useEffect(() => {
    const fetchFormData = async () => {
      if (!id) return;
      
      try {
        console.log('Fetching assessment data for ID:', id);
        const response = await axios.get(`${API}/assessments/${id}`);
        console.log('Fetched assessment:', response.data);
        console.log('FAIRA form data:', response.data?.faira_form);
        
        // Check for local backup (from session expiry)
        const backupKey = `faira_backup_${id}`;
        const backupData = localStorage.getItem(backupKey);
        
        if (response.data && response.data.faira_form) {
          console.log('Loading saved form data');
          
          // If there's backup data, ask user if they want to restore it
          if (backupData) {
            try {
              const parsedBackup = JSON.parse(backupData);
              const backupFields = Object.keys(parsedBackup).filter(k => parsedBackup[k]).length;
              const serverFields = Object.keys(response.data.faira_form).filter(k => response.data.faira_form[k]).length;
              
              // If backup has more data, offer to restore
              if (backupFields > serverFields) {
                toast.info(
                  `Found ${backupFields - serverFields} unsaved changes from your previous session. Click "Restore Backup" to recover them.`,
                  {
                    duration: 10000,
                    action: {
                      label: 'Restore Backup',
                      onClick: () => {
                        setForm(prevForm => ({
                          ...defaultState,
                          ...parsedBackup
                        }));
                        localStorage.removeItem(backupKey);
                        toast.success('Backup restored! Please save your draft.');
                      }
                    }
                  }
                );
              } else {
                // Backup is older, remove it
                localStorage.removeItem(backupKey);
              }
            } catch (e) {
              console.error('Error parsing backup:', e);
              localStorage.removeItem(backupKey);
            }
          }
          
          // Merge saved data with default state to handle any new fields
          setForm(prevForm => ({
            ...defaultState,
            ...response.data.faira_form
          }));
        } else {
          console.log('No saved form data found, using default state');
          
          // If no server data but we have backup, restore it
          if (backupData) {
            try {
              const parsedBackup = JSON.parse(backupData);
              setForm(prevForm => ({
                ...defaultState,
                ...parsedBackup
              }));
              toast.info('Restored your previous unsaved work. Please save your draft.');
              localStorage.removeItem(backupKey);
            } catch (e) {
              console.error('Error restoring backup:', e);
            }
          }
        }
      } catch (error) {
        console.error('Error fetching form data:', error);
        console.error('Error response:', error.response?.data);
      } finally {
        setLoading(false);
      }
    };

    fetchFormData();
  }, [id]);

  // Helper function to check if a field is properly filled (including "Other" validation)
  const isFieldProperlyFilled = (key, value) => {
    if (value === null || value === undefined) return false;
    
    // Special handling for Yes/No questions with conditional selections
    const conditionalYesNoQuestions = {
      'A1_6': 'A1_6_actions',
      'A2_7': 'A2_7_data_types',
      'A2_8': 'A2_8_types',
      'A4_5': 'A4_5_scenarios',
      'A4_6': 'A4_6_data_types',
      'A5_10': ['A5_10_commonwealth', 'A5_10_qld', 'A5_10_sector', 'A5_10_frameworks'],
      'B2_3': 'B2_3_perspectives',
      'B3_1': 'B3_1_methods',
      'B3_2': 'B3_2_groups',
      'B4_2': 'B4_2_types',
      'B5_1': 'B5_1_rating',
      'B5_3': 'B5_3_environments',
      'B6_4': 'B6_4_describe',
      'B7_1': 'B7_1_describe',
      'B8_4': 'B8_4_safeguards'
    };
    
    // If this is a Yes/No question with conditionals, check the conditional fields
    if (conditionalYesNoQuestions[key] && value === 'Yes') {
      const conditionalFields = Array.isArray(conditionalYesNoQuestions[key]) 
        ? conditionalYesNoQuestions[key] 
        : [conditionalYesNoQuestions[key]];
      
      // At least one conditional field must be filled
      const hasFilledConditional = conditionalFields.some(condKey => {
        const condValue = form[condKey];
        if (Array.isArray(condValue) && condValue.length > 0) {
          // Check if "Other" is selected and requires text
          if (condValue.some(v => v && (v.includes('Other') || v.includes('specify')))) {
            const otherFieldKey = `${condKey}_other`;
            const otherValue = form[otherFieldKey];
            return otherValue && otherValue.toString().trim() !== '';
          }
          return true;
        }
        return condValue && condValue.toString().trim() !== '';
      });
      
      if (!hasFilledConditional) return false;
    }
    
    if (Array.isArray(value)) {
      if (value.length === 0) return false;
      // Special check: if array contains "Other", verify the _other field is filled
      if (value.some(v => v && (v.includes('Other') || v === 'Other (specify)'))) {
        const otherFieldKey = `${key}_other`;
        const otherValue = form[otherFieldKey];
        // The _other field must be filled
        if (!otherValue || otherValue.toString().trim() === '') {
          return false;
        }
      }
      return true;
    }
    
    if (typeof value === 'number') return true;
    if (typeof value === 'boolean') return value;
    return value && value.toString().trim() !== '';
  };

  // Calculate progress percentage - only count applicable fields
  const calculateProgress = () => {
    // Fields to exclude from progress calculation (auto-filled or optional fields)
    const excludedFields = ['declaration_date', 'assessor_email', 'declaration_role'];
    
    // List of conditional fields that should only count if their parent condition is met
    const conditionalFields = {
      'A1_3_other': () => form.A1_3.includes('Other'),
      'A1_6_actions': () => form.A1_6 === 'Yes',
      'A1_6_actions_other': () => form.A1_6 === 'Yes' && form.A1_6_actions.includes('Other'),
      'A1_7_other': () => form.A1_7.includes('Other'),
      // A2.2 conditional fields
      'A2_2_sources': () => form.A2_2 === 'Yes',
      'A2_2_sources_other': () => form.A2_2 === 'Yes' && form.A2_2_sources.includes('Other'),
      'A2_2_data_types': () => form.A2_2 === 'Yes',
      'A2_2_data_types_other': () => form.A2_2 === 'Yes' && form.A2_2_data_types.includes('Other'),
      'A2_2_user_limits': () => form.A2_2 === 'Yes',
      'A2_2_traceability': () => form.A2_2 === 'Yes',
      'A2_2_trace_mechanisms': () => form.A2_2 === 'Yes',
      'A2_2_notes': () => form.A2_2 === 'Yes', // Optional, always shown when gate is Yes
      'A2_4_other': () => form.A2_4.includes('Other'),
      'A2_7_data_types': () => form.A2_7 === 'Yes',
      'A2_7_data_types_other': () => form.A2_7 === 'Yes' && form.A2_7_data_types.includes('Other regulated/sensitive data (specify)'),
      'A2_8_types': () => form.A2_8 === 'Yes',
      'A3_3_other': () => form.A3_3.includes('Other'),
      'A4_5_scenarios': () => form.A4_5 === 'Yes',
      'A4_6_data_types': () => form.A4_6 === 'Yes',
      // A4.7 conditional fields
      'A4_7_pii_types': () => form.A4_7 === 'Yes',
      'A4_7_pii_types_other': () => form.A4_7 === 'Yes' && form.A4_7_pii_types.includes('Other'),
      'A4_7_access_scope': () => form.A4_7 === 'Yes',
      'A4_7_access_controls': () => form.A4_7 === 'Yes',
      'A4_7_notes': () => form.A4_7 === 'Yes',
      // A4.8 conditional fields
      'A4_8_action_types': () => form.A4_8 === 'Yes',
      'A4_8_action_types_other': () => form.A4_8 === 'Yes' && form.A4_8_action_types.includes('Other'),
      'A4_8_trigger_pathway': () => form.A4_8 === 'Yes',
      'A4_8_affected_parties': () => form.A4_8 === 'Yes',
      'A4_8_decision_records': () => form.A4_8 === 'Yes',
      'A4_8_review_appeal': () => form.A4_8 === 'Yes',
      'A4_8_legal_basis': () => form.A4_8 === 'Yes',
      'A4_8_legal_basis_other': () => form.A4_8 === 'Yes' && form.A4_8_legal_basis.includes('Other'),
      'A4_8_notes': () => form.A4_8 === 'Yes',
      // A5_10 multiselect sections - at least one selection from any section completes the question
      // Each section is only "required" if no other sections have selections yet
      'A5_10_commonwealth': () => form.A5_10 === 'Yes' && 
        !(form.A5_10_qld?.length > 0 || form.A5_10_sector?.length > 0 || form.A5_10_frameworks?.length > 0),
      'A5_10_qld': () => form.A5_10 === 'Yes' && 
        !(form.A5_10_commonwealth?.length > 0 || form.A5_10_sector?.length > 0 || form.A5_10_frameworks?.length > 0),
      'A5_10_sector': () => form.A5_10 === 'Yes' && 
        !(form.A5_10_commonwealth?.length > 0 || form.A5_10_qld?.length > 0 || form.A5_10_frameworks?.length > 0),
      'A5_10_frameworks': () => form.A5_10 === 'Yes' && 
        !(form.A5_10_commonwealth?.length > 0 || form.A5_10_qld?.length > 0 || form.A5_10_sector?.length > 0),
      'A5_10_frameworks_other': () => form.A5_10 === 'Yes' && form.A5_10_frameworks?.includes('Other standards or frameworks (specify below)'),
      // A5_10_other and A5_10_impact are optional - removed from conditional requirements
      'A5_12_other': () => form.A5_12.includes('Other'),
      'B2_3_perspectives': () => form.B2_3 === 'Yes',
      'B2_3_perspectives_other': () => form.B2_3 === 'Yes' && form.B2_3_perspectives.includes('Other'),
      'B3_1_methods': () => form.B3_1 === 'Yes',
      'B3_2_groups': () => form.B3_2 === 'Yes',
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
    const unfilledFields = [];

    Object.keys(defaultState).forEach(key => {
      // Skip excluded fields
      if (excludedFields.includes(key)) {
        return;
      }
      
      // Check if this is a conditional field
      if (conditionalFields[key]) {
        // Only count if condition is met
        if (conditionalFields[key]()) {
          totalFields++;
          const value = form[key];
          const isFilled = isFieldProperlyFilled(key, value);
          if (isFilled) {
            filledFields++;
          } else {
            unfilledFields.push(key);
          }
        }
      } else {
        // Always count non-conditional fields
        totalFields++;
        const value = form[key];
        const isFilled = isFieldProperlyFilled(key, value);
        if (isFilled) {
          filledFields++;
        } else {
          unfilledFields.push(key);
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
      // A2.2 conditional fields
      'A2_2_sources': () => form.A2_2 === 'Yes',
      'A2_2_sources_other': () => form.A2_2 === 'Yes' && form.A2_2_sources.includes('Other'),
      'A2_2_data_types': () => form.A2_2 === 'Yes',
      'A2_2_data_types_other': () => form.A2_2 === 'Yes' && form.A2_2_data_types.includes('Other'),
      'A2_2_user_limits': () => form.A2_2 === 'Yes',
      'A2_2_traceability': () => form.A2_2 === 'Yes',
      'A2_2_trace_mechanisms': () => form.A2_2 === 'Yes',
      'A2_2_notes': () => form.A2_2 === 'Yes', // Optional, always shown when gate is Yes
      'A2_4_other': () => form.A2_4.includes('Other'),
      'A2_7_data_types': () => form.A2_7 === 'Yes',
      'A2_7_data_types_other': () => form.A2_7 === 'Yes' && form.A2_7_data_types.includes('Other regulated/sensitive data (specify)'),
      'A2_8_types': () => form.A2_8 === 'Yes',
      'A3_3_other': () => form.A3_3.includes('Other'),
      'A4_5_scenarios': () => form.A4_5 === 'Yes',
      'A4_6_data_types': () => form.A4_6 === 'Yes',
      // A4.7 conditional fields
      'A4_7_pii_types': () => form.A4_7 === 'Yes',
      'A4_7_pii_types_other': () => form.A4_7 === 'Yes' && form.A4_7_pii_types.includes('Other'),
      'A4_7_access_scope': () => form.A4_7 === 'Yes',
      'A4_7_access_controls': () => form.A4_7 === 'Yes',
      'A4_7_notes': () => form.A4_7 === 'Yes',
      // A4.8 conditional fields
      'A4_8_action_types': () => form.A4_8 === 'Yes',
      'A4_8_action_types_other': () => form.A4_8 === 'Yes' && form.A4_8_action_types.includes('Other'),
      'A4_8_trigger_pathway': () => form.A4_8 === 'Yes',
      'A4_8_affected_parties': () => form.A4_8 === 'Yes',
      'A4_8_decision_records': () => form.A4_8 === 'Yes',
      'A4_8_review_appeal': () => form.A4_8 === 'Yes',
      'A4_8_legal_basis': () => form.A4_8 === 'Yes',
      'A4_8_legal_basis_other': () => form.A4_8 === 'Yes' && form.A4_8_legal_basis.includes('Other'),
      'A4_8_notes': () => form.A4_8 === 'Yes',
      // A5_10 multiselect sections - at least one selection from any section completes the question
      // Each section is only "required" if no other sections have selections yet
      'A5_10_commonwealth': () => form.A5_10 === 'Yes' && 
        !(form.A5_10_qld?.length > 0 || form.A5_10_sector?.length > 0 || form.A5_10_frameworks?.length > 0),
      'A5_10_qld': () => form.A5_10 === 'Yes' && 
        !(form.A5_10_commonwealth?.length > 0 || form.A5_10_sector?.length > 0 || form.A5_10_frameworks?.length > 0),
      'A5_10_sector': () => form.A5_10 === 'Yes' && 
        !(form.A5_10_commonwealth?.length > 0 || form.A5_10_qld?.length > 0 || form.A5_10_frameworks?.length > 0),
      'A5_10_frameworks': () => form.A5_10 === 'Yes' && 
        !(form.A5_10_commonwealth?.length > 0 || form.A5_10_qld?.length > 0 || form.A5_10_sector?.length > 0),
      'A5_10_frameworks_other': () => form.A5_10 === 'Yes' && form.A5_10_frameworks?.includes('Other standards or frameworks (specify below)'),
      // A5_10_other and A5_10_impact are optional - removed from conditional requirements
      'A5_12_other': () => form.A5_12.includes('Other'),
      'B2_3_perspectives': () => form.B2_3 === 'Yes',
      'B2_3_perspectives_other': () => form.B2_3 === 'Yes' && form.B2_3_perspectives.includes('Other'),
      'B3_1_methods': () => form.B3_1 === 'Yes',
      'B3_2_groups': () => form.B3_2 === 'Yes',
      'B4_2_types': () => form.B4_2 === 'Yes',
      'B4_2_types_other': () => form.B4_2 === 'Yes' && form.B4_2_types.includes('Other'),
      'B5_1_rating': () => form.B5_1 === 'Yes',
      'B5_3_environments': () => form.B5_3 === 'Yes',
      'B6_4_describe': () => form.B6_4 === 'Yes',
      'B7_1_describe': () => form.B7_1 === 'Yes',
      'B8_4_safeguards': () => form.B8_4 === 'Yes'
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
            const value = form[fieldId];
            if (isFieldProperlyFilled(fieldId, value)) {
              completed++;
            } else if (!firstUnanswered) {
              firstUnanswered = fieldId;
            }
          }
        } else {
          totalApplicable++;
          const value = form[fieldId];
          if (isFieldProperlyFilled(fieldId, value)) {
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
    // Try to find the specific field element first
    let element = document.getElementById(fieldId);
    
    // If not found, try to find the section container
    if (!element) {
      // Extract section prefix (e.g., "A3" from "A3_2_technical")
      const sectionMatch = fieldId.match(/^([AB]\d+)/);
      if (sectionMatch) {
        const sectionId = sectionMatch[1];
        // Try common first field patterns for each section
        const firstFieldPatterns = [
          `${sectionId}_1`,
          `${fieldId}` // Try the exact field ID again
        ];
        
        for (const pattern of firstFieldPatterns) {
          element = document.getElementById(pattern);
          if (element) break;
        }
      }
    }
    
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

  // Handle 401 errors (session expired)
  const handleSessionExpired = () => {
    toast.error('Your session has expired. Please log in again to continue.', {
      duration: 5000
    });
    // Store current form data in localStorage before redirecting
    try {
      localStorage.setItem(`faira_backup_${id}`, JSON.stringify(form));
      toast.info('Your unsaved changes have been backed up locally.');
    } catch (e) {
      console.error('Could not backup form data:', e);
    }
    setTimeout(() => {
      window.location.href = '/auth';
    }, 2000);
  };

  const handleAutoSave = async () => {
    if (!id) return;
    setAutoSaving(true);
    try {
      console.log('Auto-saving form data:', form);
      const response = await axios.put(`${API}/assessments/${id}/faira-form`, form);
      console.log('Auto-save response:', response.data);
      setLastSaved(new Date());
    } catch (error) {
      console.error('Auto-save error:', error);
      console.error('Error details:', error.response?.data);
      if (error.response?.status === 401) {
        handleSessionExpired();
      }
    } finally {
      setAutoSaving(false);
    }
  };

  const handleSaveDraft = async () => {
    setSubmitting(true);
    try {
      console.log('Saving draft with data:', form);
      const response = await axios.put(`${API}/assessments/${id}/faira-form`, form);
      console.log('Save draft response:', response.data);
      toast.success('Draft saved successfully!');
      setLastSaved(new Date());
    } catch (error) {
      console.error('Save draft error:', error);
      console.error('Error response:', error.response?.data);
      if (error.response?.status === 401) {
        handleSessionExpired();
      } else {
        toast.error('Failed to save draft');
      }
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
      // Clear any backup data on successful submit
      localStorage.removeItem(`faira_backup_${id}`);
      navigate(`/faira-results/${id}`);
    } catch (error) {
      console.error('Submit error:', error);
      if (error.response?.status === 401) {
        handleSessionExpired();
      } else {
        toast.error(error.response?.data?.detail || 'Failed to submit assessment');
      }
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

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-bg flex items-center justify-center">
        <div className="text-center">
          <div className="loading-spinner w-8 h-8 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading assessment...</p>
        </div>
      </div>
    );
  }

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
                const progress = status?.progress || 0;
                
                // Determine color scheme based on progress
                let bgColor, borderColor, hoverBg, iconColor, textColor, progressTextColor;
                
                if (isCompleted) {
                  // 100% complete - Green
                  bgColor = 'bg-green-50';
                  borderColor = 'border-l-4 border-green-500';
                  hoverBg = 'hover:bg-green-100';
                  iconColor = 'bg-green-500';
                  textColor = 'text-green-700';
                } else if (progress === 0) {
                  // 0% complete - Red/Orange
                  bgColor = 'bg-red-50';
                  borderColor = 'border-l-4 border-red-400';
                  hoverBg = 'hover:bg-red-100';
                  iconColor = 'text-red-400';
                  textColor = 'text-gray-700';
                  progressTextColor = 'text-red-600';
                } else {
                  // Partial completion - Amber/Yellow
                  bgColor = 'bg-amber-50';
                  borderColor = 'border-l-4 border-amber-400';
                  hoverBg = 'hover:bg-amber-100';
                  iconColor = 'text-amber-500';
                  textColor = 'text-gray-700';
                  progressTextColor = 'text-amber-600';
                }
                
                return (
                  <button
                    key={section.id}
                    type="button"
                    onClick={() => {
                      if (!isCompleted && status?.firstUnanswered) {
                        scrollToField(status.firstUnanswered);
                      }
                    }}
                    className={`w-full text-left px-3 py-2 rounded-lg transition-all flex items-start gap-2 ${bgColor} ${borderColor} ${hoverBg} cursor-pointer`}
                  >
                    <div className="flex-shrink-0 mt-0.5">
                      {isCompleted ? (
                        <div className={`h-5 w-5 rounded-full ${iconColor} flex items-center justify-center`}>
                          <Check className="h-3 w-3 text-white" />
                        </div>
                      ) : (
                        <Circle className={`h-5 w-5 ${iconColor}`} />
                      )}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className={`text-sm font-medium ${textColor}`}>
                        {section.name}
                      </p>
                      {!isCompleted && (
                        <p className={`text-xs ${progressTextColor || 'text-gray-500'} font-semibold mt-0.5`}>
                          {progress}% complete
                        </p>
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
        
        {/* BLOCK 1: Assessment Overview */}
        <Card>
          <CardHeader className="bg-orange-50 border-b border-orange-100">
            <div className="flex items-center space-x-2">
              <ShieldCheck className="h-5 w-5 text-orange-600" />
              <CardTitle className="text-xl">Assessment Overview</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="p-6 space-y-8">
            {/* Section A: Assessment Information */}
            <div className="space-y-4">
              <h3 className="text-base font-semibold text-gray-900 border-b border-gray-200 pb-2">A. Assessment Information</h3>
              <div className="grid gap-4 md:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="ai_system_name">AI System Name *</Label>
                  <Input
                    id="ai_system_name"
                    value={form.ai_system_name}
                    onChange={(e) => update("ai_system_name", e.target.value)}
                    required
                    placeholder="Enter AI system name"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="ai_system_version">AI System Version *</Label>
                  <Input
                    id="ai_system_version"
                    value={form.ai_system_version}
                    onChange={(e) => update("ai_system_version", e.target.value)}
                    required
                    placeholder="Enter version"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="business_unit">Business Unit / Branch *</Label>
                  <Input
                    id="business_unit"
                    value={form.business_unit}
                    onChange={(e) => update("business_unit", e.target.value)}
                    required
                    placeholder="Enter business unit or branch"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="system_owner_name">System Owner Name *</Label>
                  <Input
                    id="system_owner_name"
                    value={form.system_owner_name}
                    onChange={(e) => update("system_owner_name", e.target.value)}
                    required
                    placeholder="Enter system owner name"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="system_owner_role">System Owner Role/Title *</Label>
                  <Input
                    id="system_owner_role"
                    value={form.system_owner_role}
                    onChange={(e) => update("system_owner_role", e.target.value)}
                    required
                    placeholder="Enter system owner role"
                  />
                </div>
              </div>
            </div>

            {/* Section B: Assessor Information */}
            <div className="space-y-4">
              <h3 className="text-base font-semibold text-gray-900 border-b border-gray-200 pb-2">B. Assessor Information</h3>
              <div className="grid gap-4 md:grid-cols-2">
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
                  <Label htmlFor="assessor_role">Assessor Role/Title *</Label>
                  <Input
                    id="assessor_role"
                    value={form.assessor_role}
                    onChange={(e) => update("assessor_role", e.target.value)}
                    required
                    placeholder="Enter your role"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="assessor_branch">Assessor Branch / Division *</Label>
                  <Input
                    id="assessor_branch"
                    value={form.assessor_branch}
                    onChange={(e) => update("assessor_branch", e.target.value)}
                    required
                    placeholder="Enter your branch or division"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="assessor_email">Assessor Email (optional)</Label>
                  <Input
                    id="assessor_email"
                    type="email"
                    value={form.assessor_email}
                    onChange={(e) => update("assessor_email", e.target.value)}
                    placeholder="Enter your email"
                  />
                </div>
              </div>
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
            <SectionA1 form={form} update={update} toggleInArray={toggleInArray} />
            <SectionA2 form={form} update={update} toggleInArray={toggleInArray} />
            <SectionA3 form={form} update={update} toggleInArray={toggleInArray} />
            <SectionA4 form={form} update={update} toggleInArray={toggleInArray} />
            <SectionA5 form={form} update={update} toggleInArray={toggleInArray} />
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
                    "privacy risks",
                    "bias/discrimination",
                    "transparency issues",
                    "safety risks",
                    "employment impacts",
                    "social harm",
                    "environmental impact",
                    "accessibility issues",
                    "legal/regulatory risks",
                    "loss of trust"
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
                        "people with disabilities",
                        "cultural diversity",
                        "gender diversity",
                        "age diversity",
                        "Indigenous perspectives",
                        "socioeconomic diversity"
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
                        "statistical parity analysis",
                        "disparate impact analysis",
                        "dataset bias review",
                        "model interpretability testing",
                        "human review panels",
                        "synthetic scenario testing",
                        "accessibility testing",
                        "penetration/security testing",
                        "vendor-provided tests",
                        "informal or ad-hoc checks only (no formal testing) (flag as risk)"
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
                
                {form.B3_2 === "Yes" && (
                  <div className="ml-4 p-4 bg-gray-50 rounded-lg space-y-2">
                    <Label>Against which groups? (Select all that apply):</Label>
                    <div className="grid gap-2 md:grid-cols-2">
                      {[
                        "age groups",
                        "people with disabilities",
                        "racial or ethnic groups",
                        "religious groups",
                        "gender",
                        "sexual orientation",
                        "socioeconomic status"
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
                        "identifiable",
                        "sensitive",
                        "health-related",
                        "financial",
                        "biometric"
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
                    "access controls",
                    "encryption",
                    "security testing",
                    "data anonymization",
                    "privacy-enhancing technologies"
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
                        "essential services",
                        "critical infrastructure",
                        "health services",
                        "education",
                        "law enforcement",
                        "administration of justice",
                        "democratic processes"
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
                  <option value="immediately">immediately</option>
                  <option value="within hours">within hours</option>
                  <option value="within days">within days</option>
                  <option value="within weeks">within weeks</option>
                  <option value="longer than weeks">longer than weeks</option>
                  <option value="unknown">unknown</option>
                </select>
              </div>
            </div>

            {/* B8: Accountability */}
            <div className="space-y-6 pt-6 border-t" id="B8_1">
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
                        "mandatory human review",
                        "confidence thresholds",
                        "explainability requirements",
                        "training for staff",
                        "decision override controls",
                        "system warnings",
                        "monitoring of decision quality"
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
          <CardContent className="p-6 space-y-6">
            <div className="flex items-start space-x-3 p-4 bg-amber-50 border border-amber-200 rounded-lg">
              <Checkbox
                id="declaration_confirmed"
                checked={form.declaration_confirmed}
                onCheckedChange={(checked) => update("declaration_confirmed", checked)}
                required
                className="mt-0.5"
              />
              <Label htmlFor="declaration_confirmed" className="text-sm font-medium cursor-pointer leading-relaxed">
                I certify that all information provided in this FAIRA assessment is accurate and complete to the best of my knowledge.
              </Label>
            </div>
            
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="declaration_name">Name of person making this declaration: *</Label>
                <Input
                  id="declaration_name"
                  value={form.declaration_name || form.assessor_name}
                  onChange={(e) => update("declaration_name", e.target.value)}
                  required
                  placeholder="Enter your name"
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="declaration_date">Date: *</Label>
                <Input
                  id="declaration_date"
                  type="date"
                  value={form.declaration_date}
                  onChange={(e) => update("declaration_date", e.target.value)}
                  required
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="declaration_role">(Optional) Role/Title:</Label>
                <Input
                  id="declaration_role"
                  value={form.declaration_role || form.assessor_role}
                  onChange={(e) => update("declaration_role", e.target.value)}
                  placeholder="Enter your role or title"
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
