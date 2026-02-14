import React from 'react';
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Separator } from "@/components/ui/separator";
import EvidenceAttachLink, { EVIDENCE_TOOLTIPS } from '../EvidenceAttachLink';

const SectionB4 = ({ form, update, toggleInArray, assessmentId, currentUser }) => {
  return (
    <div className="space-y-6 pt-6 border-t" id="B4_1">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-1">B4. Privacy Protection and Security</h3>
      </div>
      <Separator />
      
      {/* B4.1 */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <Label>B4.1 Has a Privacy Impact Assessment been completed?</Label>
          {assessmentId && form.B4_1 === "Yes" && (
            <EvidenceAttachLink 
              questionCode="B4-1" 
              assessmentId={assessmentId} 
              currentUser={currentUser}
              tooltip={EVIDENCE_TOOLTIPS['B4-1']}
            />
          )}
        </div>
        <div className="flex space-x-4">
          {["Yes", "No"].map((opt) => (
            <label key={opt} className="flex items-center space-x-2">
              <input type="radio" checked={form.B4_1 === opt} onChange={() => update("B4_1", opt)} className="h-4 w-4 text-orange-600" />
              <span className="text-sm">{opt}</span>
            </label>
          ))}
        </div>
      </div>

      {/* B4.2 */}
      <div className="space-y-3">
        <Label>B4.2 Does the system collect, use, or disclose personal information?</Label>
        <div className="flex space-x-4">
          {["Yes", "No"].map((opt) => (
            <label key={opt} className="flex items-center space-x-2">
              <input type="radio" checked={form.B4_2 === opt} onChange={() => update("B4_2", opt)} className="h-4 w-4 text-orange-600" />
              <span className="text-sm">{opt}</span>
            </label>
          ))}
        </div>
        
        {form.B4_2 === "Yes" && (
          <div className="ml-4 p-4 bg-gray-50 rounded-lg space-y-2">
            <Label>Is this information (Select all that apply):</Label>
            <div className="grid gap-2 md:grid-cols-2">
              {["identifiable", "sensitive", "health-related", "financial", "biometric"].map((option) => (
                <label key={option} className="flex items-center space-x-2">
                  <Checkbox checked={(form.B4_2_types || []).includes(option)} onCheckedChange={() => toggleInArray("B4_2_types", option)} />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
              <label className="flex items-center space-x-2">
                <Checkbox checked={(form.B4_2_types || []).includes("Other")} onCheckedChange={() => toggleInArray("B4_2_types", "Other")} />
                <span className="text-sm">Other (specify)</span>
              </label>
            </div>
            {(form.B4_2_types || []).includes("Other") && (
              <Input value={form.B4_2_types_other} onChange={(e) => update("B4_2_types_other", e.target.value)} placeholder="Please specify other types" className="mt-2" />
            )}
          </div>
        )}
      </div>

      {/* B4.3 */}
      <div className="space-y-2">
        <Label>B4.3 What security controls are in place? (Select all that apply)</Label>
        <div className="grid gap-2 md:grid-cols-2">
          {["access controls", "encryption", "auditing", "intrusion detection", "secure development practices", "security testing", "regular security assessments", "no formal security measures (flag as risk)"].map((option) => (
            <label key={option} className="flex items-center space-x-2">
              <Checkbox checked={(form.B4_3 || []).includes(option)} onCheckedChange={() => toggleInArray("B4_3", option)} />
              <span className="text-sm">{option}</span>
            </label>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SectionB4;
