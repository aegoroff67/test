import React from 'react';
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Separator } from "@/components/ui/separator";
import { RadioScale } from './RadioScale';

const SectionB1 = ({ form, update, toggleInArray, assessmentId, currentUser }) => {
  return (
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
            <RadioScale value={form.B1_1_individual} onChange={(val) => update("B1_1_individual", val)} />
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium w-48">Organizational efficiency:</span>
            <RadioScale value={form.B1_1_organizational} onChange={(val) => update("B1_1_organizational", val)} />
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium w-48">Social outcomes:</span>
            <RadioScale value={form.B1_1_social} onChange={(val) => update("B1_1_social", val)} />
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium w-48">Environmental outcomes:</span>
            <RadioScale value={form.B1_1_environmental} onChange={(val) => update("B1_1_environmental", val)} />
          </div>
        </div>
      </div>

      {/* B1.2 */}
      <div className="space-y-2">
        <Label>B1.2 What negative impacts might arise from the AI solution? (Select all that apply)</Label>
        <div className="grid gap-2 md:grid-cols-2">
          {["privacy risks", "bias/discrimination", "transparency issues", "safety risks", "employment impacts", "social harm", "environmental impact", "accessibility issues", "legal/regulatory risks", "loss of trust"].map((option) => (
            <label key={option} className="flex items-center space-x-2">
              <Checkbox checked={(form.B1_2 || []).includes(option)} onCheckedChange={() => toggleInArray("B1_2", option)} />
              <span className="text-sm">{option}</span>
            </label>
          ))}
        </div>
      </div>

      {/* B1.3 */}
      <div className="space-y-2">
        <Label>B1.3 Will the AI solution affect employee employment?</Label>
        <div className="flex space-x-4">
          {["Yes", "No", "Unknown"].map((opt) => (
            <label key={opt} className="flex items-center space-x-2">
              <input type="radio" checked={form.B1_3 === opt} onChange={() => update("B1_3", opt)} className="h-4 w-4 text-orange-600" />
              <span className="text-sm">{opt}</span>
            </label>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SectionB1;
