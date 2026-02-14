import React from 'react';
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Separator } from "@/components/ui/separator";
import EvidenceAttachLink from '../EvidenceAttachLink';

const SectionB2 = ({ form, update, toggleInArray, assessmentId, currentUser }) => {
  return (
    <div className="space-y-6 pt-6 border-t" id="B2_1">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-1">B2. Human-Centered Values</h3>
      </div>
      <Separator />
      
      {/* B2.1 */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <Label>B2.1 Has a Human Rights Impact Assessment been completed?</Label>
          {assessmentId && (
            <EvidenceAttachLink 
              questionCode="B2-1" 
              assessmentId={assessmentId} 
              currentUser={currentUser} 
            />
          )}
        </div>
        <div className="flex space-x-4">
          {["Yes", "No"].map((opt) => (
            <label key={opt} className="flex items-center space-x-2">
              <input type="radio" checked={form.B2_1 === opt} onChange={() => update("B2_1", opt)} className="h-4 w-4 text-orange-600" />
              <span className="text-sm">{opt}</span>
            </label>
          ))}
        </div>
      </div>

      {/* B2.2 */}
      <div className="space-y-4">
        <Label>B2.2 Rate the potential impact on:</Label>
        <div className="space-y-3 ml-4">
          {[
            { label: "Human rights:", field: "B2_2_rights" },
            { label: "Diversity:", field: "B2_2_diversity" },
            { label: "Individual autonomy:", field: "B2_2_autonomy" }
          ].map(({ label, field }) => (
            <div key={field}>
              <span className="text-sm font-medium block mb-2">{label}</span>
              <div className="flex space-x-4">
                {["Positive", "Neutral", "Negative", "Unknown"].map((opt) => (
                  <label key={opt} className="flex items-center space-x-2">
                    <input type="radio" checked={form[field] === opt} onChange={() => update(field, opt)} className="h-4 w-4 text-orange-600" />
                    <span className="text-sm">{opt}</span>
                  </label>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* B2.3 */}
      <div className="space-y-3">
        <Label>B2.3 Have diverse perspectives been incorporated in the design?</Label>
        <div className="flex space-x-4">
          {["Yes", "No"].map((opt) => (
            <label key={opt} className="flex items-center space-x-2">
              <input type="radio" checked={form.B2_3 === opt} onChange={() => update("B2_3", opt)} className="h-4 w-4 text-orange-600" />
              <span className="text-sm">{opt}</span>
            </label>
          ))}
        </div>
        
        {form.B2_3 === "Yes" && (
          <div className="ml-4 p-4 bg-gray-50 rounded-lg space-y-2">
            <Label>Which perspectives? (Select all that apply):</Label>
            <div className="grid gap-2 md:grid-cols-2">
              {["people with disabilities", "cultural diversity", "gender diversity", "age diversity", "Indigenous perspectives", "socioeconomic diversity"].map((option) => (
                <label key={option} className="flex items-center space-x-2">
                  <Checkbox checked={(form.B2_3_perspectives || []).includes(option)} onCheckedChange={() => toggleInArray("B2_3_perspectives", option)} />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
              <label className="flex items-center space-x-2">
                <Checkbox checked={(form.B2_3_perspectives || []).includes("Other")} onCheckedChange={() => toggleInArray("B2_3_perspectives", "Other")} />
                <span className="text-sm">Other (specify)</span>
              </label>
            </div>
            {(form.B2_3_perspectives || []).includes("Other") && (
              <Input value={form.B2_3_perspectives_other} onChange={(e) => update("B2_3_perspectives_other", e.target.value)} placeholder="Please specify other perspectives" className="mt-2" />
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default SectionB2;
