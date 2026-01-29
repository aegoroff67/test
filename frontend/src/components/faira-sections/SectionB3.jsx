import React from 'react';
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Separator } from "@/components/ui/separator";

const SectionB3 = ({ form, update, toggleInArray }) => {
  return (
    <div className="space-y-6 pt-6 border-t" id="B3_1">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-1">B3. Fairness</h3>
      </div>
      <Separator />
      
      {/* B3.1 */}
      <div className="space-y-3">
        <Label>B3.1 Has the AI solution been tested for fairness and bias?</Label>
        <div className="flex space-x-4">
          {["Yes", "No"].map((opt) => (
            <label key={opt} className="flex items-center space-x-2">
              <input type="radio" checked={form.B3_1 === opt} onChange={() => update("B3_1", opt)} className="h-4 w-4 text-orange-600" />
              <span className="text-sm">{opt}</span>
            </label>
          ))}
        </div>
        
        {form.B3_1 === "Yes" && (
          <div className="ml-4 p-4 bg-gray-50 rounded-lg space-y-2">
            <Label>Select testing methods (Select all that apply):</Label>
            <div className="grid gap-2 md:grid-cols-2">
              {["statistical parity analysis", "disparate impact analysis", "dataset bias review", "model interpretability testing", "human review panels", "synthetic scenario testing", "accessibility testing", "penetration/security testing", "vendor-provided tests", "informal or ad-hoc checks only (no formal testing) (flag as risk)"].map((option) => (
                <label key={option} className="flex items-center space-x-2">
                  <Checkbox checked={(form.B3_1_methods || []).includes(option)} onCheckedChange={() => toggleInArray("B3_1_methods", option)} />
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
          {["Yes", "No", "Unknown"].map((opt) => (
            <label key={opt} className="flex items-center space-x-2">
              <input type="radio" checked={form.B3_2 === opt} onChange={() => update("B3_2", opt)} className="h-4 w-4 text-orange-600" />
              <span className="text-sm">{opt}</span>
            </label>
          ))}
        </div>
        
        {form.B3_2 === "Yes" && (
          <div className="ml-4 p-4 bg-gray-50 rounded-lg space-y-2">
            <Label>Against which groups? (Select all that apply):</Label>
            <div className="grid gap-2 md:grid-cols-2">
              {["age groups", "people with disabilities", "racial or ethnic groups", "religious groups", "gender", "sexual orientation", "socioeconomic status"].map((option) => (
                <label key={option} className="flex items-center space-x-2">
                  <Checkbox checked={(form.B3_2_groups || []).includes(option)} onCheckedChange={() => toggleInArray("B3_2_groups", option)} />
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

export default SectionB3;
