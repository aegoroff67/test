import React from 'react';
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Separator } from "@/components/ui/separator";
import { RadioScale } from './RadioScale';
import EvidenceAttachLink from '../EvidenceAttachLink';

const SectionB5 = ({ form, update, toggleInArray, assessmentId, currentUser }) => {
  return (
    <div className="space-y-6 pt-6 border-t" id="B5_1">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-1">B5. Reliability and Safety</h3>
      </div>
      <Separator />
      
      {/* B5.1 */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <Label>B5.1 Has the AI solution been tested for reliability?</Label>
          {assessmentId && form.B5_1 === "Yes" && (
            <EvidenceAttachLink 
              questionCode="B5-1" 
              assessmentId={assessmentId} 
              currentUser={currentUser} 
            />
          )}
        </div>
        <div className="flex space-x-4">
          {["Yes", "No"].map((opt) => (
            <label key={opt} className="flex items-center space-x-2">
              <input type="radio" checked={form.B5_1 === opt} onChange={() => update("B5_1", opt)} className="h-4 w-4 text-orange-600" />
              <span className="text-sm">{opt}</span>
            </label>
          ))}
        </div>
        
        {form.B5_1 === "Yes" && (
          <div className="ml-4 p-4 bg-gray-50 rounded-lg space-y-3">
            <div>
              <Label>Rate the reliability (1 = Very Low, 5 = Very High):</Label>
              <div className="mt-2">
                <RadioScale value={form.B5_1_rating} onChange={(val) => update("B5_1_rating", val)} />
              </div>
            </div>
          </div>
        )}
      </div>

      {/* B5.2 */}
      <div className="space-y-2">
        <Label>B5.2 Is there a process to disengage if AI fails?</Label>
        <div className="flex space-x-4">
          {["Yes", "No"].map((opt) => (
            <label key={opt} className="flex items-center space-x-2">
              <input type="radio" checked={form.B5_2 === opt} onChange={() => update("B5_2", opt)} className="h-4 w-4 text-orange-600" />
              <span className="text-sm">{opt}</span>
            </label>
          ))}
        </div>
      </div>

      {/* B5.3 */}
      <div className="space-y-3">
        <Label>B5.3 Does the AI operate in a high-risk environment?</Label>
        <div className="flex space-x-4">
          {["Yes", "No"].map((opt) => (
            <label key={opt} className="flex items-center space-x-2">
              <input type="radio" checked={form.B5_3 === opt} onChange={() => update("B5_3", opt)} className="h-4 w-4 text-orange-600" />
              <span className="text-sm">{opt}</span>
            </label>
          ))}
        </div>
        
        {form.B5_3 === "Yes" && (
          <div className="ml-4 p-4 bg-gray-50 rounded-lg space-y-2">
            <Label>Which environments? (Select all that apply):</Label>
            <div className="grid gap-2 md:grid-cols-2">
              {["healthcare", "finance", "critical infrastructure", "public safety", "transportation", "legal/judicial", "employment decisions", "education"].map((option) => (
                <label key={option} className="flex items-center space-x-2">
                  <Checkbox checked={(form.B5_3_environments || []).includes(option)} onCheckedChange={() => toggleInArray("B5_3_environments", option)} />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SectionB5;
