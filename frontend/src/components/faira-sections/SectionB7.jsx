import React from 'react';
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Separator } from "@/components/ui/separator";

const SectionB7 = ({ form, update, toggleInArray }) => {
  return (
    <div className="space-y-6 pt-6 border-t" id="B7_1">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-1">B7. Contestability</h3>
      </div>
      <Separator />
      
      {/* B7.1 */}
      <div className="space-y-3">
        <Label>B7.1 Can affected parties challenge AI decisions?</Label>
        <div className="flex space-x-4">
          {["Yes", "No"].map((opt) => (
            <label key={opt} className="flex items-center space-x-2">
              <input type="radio" checked={form.B7_1 === opt} onChange={() => update("B7_1", opt)} className="h-4 w-4 text-orange-600" />
              <span className="text-sm">{opt}</span>
            </label>
          ))}
        </div>
        
        {form.B7_1 === "Yes" && (
          <div className="ml-4 p-4 bg-gray-50 rounded-lg space-y-2">
            <Label>How? (Select all that apply):</Label>
            <div className="grid gap-2 md:grid-cols-2">
              {["formal appeal process", "complaint mechanism", "human review request", "ombudsman / external review", "internal escalation", "informal feedback channel"].map((option) => (
                <label key={option} className="flex items-center space-x-2">
                  <Checkbox checked={(form.B7_1_methods || []).includes(option)} onCheckedChange={() => toggleInArray("B7_1_methods", option)} />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* B7.2 */}
      <div className="space-y-2">
        <Label>B7.2 Are affected parties aware of their right to contest?</Label>
        <div className="flex space-x-4">
          {["Yes", "No", "Unknown"].map((opt) => (
            <label key={opt} className="flex items-center space-x-2">
              <input type="radio" checked={form.B7_2 === opt} onChange={() => update("B7_2", opt)} className="h-4 w-4 text-orange-600" />
              <span className="text-sm">{opt}</span>
            </label>
          ))}
        </div>
      </div>

      {/* B7.3 */}
      <div className="space-y-2">
        <Label>B7.3 What redress mechanisms are available? (Select all that apply)</Label>
        <div className="grid gap-2 md:grid-cols-2">
          {["decision reversal", "compensation", "alternative service provision", "explanation of decision", "data correction", "system adjustment", "no redress available (flag as risk)"].map((option) => (
            <label key={option} className="flex items-center space-x-2">
              <Checkbox checked={(form.B7_3 || []).includes(option)} onCheckedChange={() => toggleInArray("B7_3", option)} />
              <span className="text-sm">{option}</span>
            </label>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SectionB7;
