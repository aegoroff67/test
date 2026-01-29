import React from 'react';
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Separator } from "@/components/ui/separator";

const SectionB6 = ({ form, update, toggleInArray }) => {
  return (
    <div className="space-y-6 pt-6 border-t" id="B6_1">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-1">B6. Transparency and Explainability</h3>
      </div>
      <Separator />
      
      {/* B6.1 */}
      <div className="space-y-2">
        <Label>B6.1 Can the AI system's decisions be explained? (Select all that apply)</Label>
        <div className="grid gap-2 md:grid-cols-2">
          {["model outputs interpretable", "feature importance available", "decision rationale logged", "explanation provided to users", "technical documentation available", "non-technical explanations available", "explanations not currently available (flag as risk)"].map((option) => (
            <label key={option} className="flex items-center space-x-2">
              <Checkbox checked={(form.B6_1 || []).includes(option)} onCheckedChange={() => toggleInArray("B6_1", option)} />
              <span className="text-sm">{option}</span>
            </label>
          ))}
        </div>
      </div>

      {/* B6.2 */}
      <div className="space-y-2">
        <Label>B6.2 How are users informed about AI involvement? (Select all that apply)</Label>
        <div className="grid gap-2 md:grid-cols-2">
          {["in-app disclosure", "terms of service", "public AI statement", "direct notification", "staff training materials", "help documentation", "users not informed (flag as risk)"].map((option) => (
            <label key={option} className="flex items-center space-x-2">
              <Checkbox checked={(form.B6_2 || []).includes(option)} onCheckedChange={() => toggleInArray("B6_2", option)} />
              <span className="text-sm">{option}</span>
            </label>
          ))}
        </div>
      </div>

      {/* B6.3 */}
      <div className="space-y-2">
        <Label htmlFor="B6_3">B6.3 What documentation exists for the AI system?</Label>
        <Textarea id="B6_3" value={form.B6_3} onChange={(e) => update("B6_3", e.target.value)} placeholder="Describe available documentation (technical specs, user guides, data sheets, etc.)" rows={3} />
      </div>
    </div>
  );
};

export default SectionB6;
