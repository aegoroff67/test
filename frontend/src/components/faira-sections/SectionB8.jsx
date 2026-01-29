import React from 'react';
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Separator } from "@/components/ui/separator";

const SectionB8 = ({ form, update, toggleInArray }) => {
  return (
    <div className="space-y-6 pt-6 border-t" id="B8_1">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-1">B8. Accountability</h3>
      </div>
      <Separator />
      
      {/* B8.1 */}
      <div className="space-y-2">
        <Label>B8.1 Are accountability roles clearly defined? (Select all that apply)</Label>
        <div className="grid gap-2 md:grid-cols-2">
          {["system owner identified", "data custodian identified", "technical lead identified", "business owner identified", "governance body identified", "external oversight identified", "roles not clearly defined (flag as risk)"].map((option) => (
            <label key={option} className="flex items-center space-x-2">
              <Checkbox checked={form.B8_1.includes(option)} onCheckedChange={() => toggleInArray("B8_1", option)} />
              <span className="text-sm">{option}</span>
            </label>
          ))}
        </div>
      </div>

      {/* B8.2 */}
      <div className="space-y-2">
        <Label>B8.2 What audit and compliance mechanisms exist? (Select all that apply)</Label>
        <div className="grid gap-2 md:grid-cols-2">
          {["regular audits scheduled", "compliance monitoring", "incident reporting", "performance metrics tracked", "third-party audits", "regulatory reporting", "no audit mechanisms (flag as risk)"].map((option) => (
            <label key={option} className="flex items-center space-x-2">
              <Checkbox checked={form.B8_2.includes(option)} onCheckedChange={() => toggleInArray("B8_2", option)} />
              <span className="text-sm">{option}</span>
            </label>
          ))}
        </div>
      </div>

      {/* B8.3 */}
      <div className="space-y-2">
        <Label htmlFor="B8_3">B8.3 How are incidents and issues documented?</Label>
        <Textarea id="B8_3" value={form.B8_3} onChange={(e) => update("B8_3", e.target.value)} placeholder="Describe incident documentation processes" rows={3} />
      </div>

      {/* B8.4 */}
      <div className="space-y-3">
        <Label>B8.4 Does the AI system operate in a regulated domain?</Label>
        <div className="flex space-x-4">
          {["Yes", "No", "Unknown"].map((opt) => (
            <label key={opt} className="flex items-center space-x-2">
              <input type="radio" checked={form.B8_4 === opt} onChange={() => update("B8_4", opt)} className="h-4 w-4 text-orange-600" />
              <span className="text-sm">{opt}</span>
            </label>
          ))}
        </div>
        
        {form.B8_4 === "Yes" && (
          <div className="ml-4 p-4 bg-gray-50 rounded-lg space-y-2">
            <Label>What regulatory safeguards exist? (Select all that apply):</Label>
            <div className="grid gap-2 md:grid-cols-2">
              {["compliance certification", "regulatory approval obtained", "ongoing compliance monitoring", "regular regulatory reporting", "external audit requirement", "no specific safeguards (flag as risk)"].map((option) => (
                <label key={option} className="flex items-center space-x-2">
                  <Checkbox checked={form.B8_4_safeguards.includes(option)} onCheckedChange={() => toggleInArray("B8_4_safeguards", option)} />
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

export default SectionB8;
