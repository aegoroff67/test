import React from 'react';
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Textarea } from "@/components/ui/textarea";
import { Separator } from "@/components/ui/separator";

const SectionB7 = ({ form, update, toggleInArray }) => {
  return (
    <div className="space-y-6 pt-6 border-t" id="B7_1">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-1">B7. Contestability</h3>
      </div>
      <Separator />
      
      {/* B7.1 - Gated Section */}
      <div className="space-y-3">
        <Label>B7.1 Is there a defined process for challenging or reviewing AI-supported outcomes?</Label>
        <div className="flex space-x-4">
          <label className="flex items-center space-x-2">
            <input type="radio" checked={form.B7_1 === "Yes"} onChange={() => update("B7_1", "Yes")} className="h-4 w-4 text-orange-600" />
            <span className="text-sm">Yes</span>
          </label>
          <label className="flex items-center space-x-2">
            <input type="radio" checked={form.B7_1 === "No"} onChange={() => update("B7_1", "No")} className="h-4 w-4 text-orange-600" />
            <span className="text-sm">No</span>
          </label>
        </div>

        {/* Conditional subsections when Yes is selected */}
        {form.B7_1 === "Yes" && (
          <div className="ml-4 p-4 bg-gray-100 rounded-lg space-y-4 border border-gray-200">
            {/* B7.1a - Who can initiate a challenge */}
            <div className="space-y-2">
              <Label className="text-sm font-medium">B7.1a Who can initiate a challenge or review? (select all that apply)</Label>
              <div className="grid gap-2 md:grid-cols-2">
                {[
                  "affected individuals (e.g., customers/citizens)",
                  "internal users/operators",
                  "supervisors/managers",
                  "oversight body / governance committee",
                  "regulators / external oversight (where applicable)",
                  "third party / advocate",
                  "not specified / unclear"
                ].map((option) => (
                  <label key={option} className="flex items-center space-x-2">
                    <Checkbox 
                      checked={(form.B7_1_initiators || []).includes(option)} 
                      onCheckedChange={() => toggleInArray("B7_1_initiators", option)} 
                    />
                    <span className="text-sm">{option}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* B7.1b - How can a challenge be initiated */}
            <div className="space-y-2">
              <Label className="text-sm font-medium">B7.1b How can a challenge or review be initiated? (select all that apply)</Label>
              <div className="grid gap-2 md:grid-cols-2">
                {[
                  "formal appeal process",
                  "service desk / support request",
                  "case management / ticketing workflow",
                  "manager escalation pathway",
                  "in-application review/request feature",
                  "written request (email/letter)",
                  "not defined"
                ].map((option) => (
                  <label key={option} className="flex items-center space-x-2">
                    <Checkbox 
                      checked={(form.B7_1_channels || []).includes(option)} 
                      onCheckedChange={() => toggleInArray("B7_1_channels", option)} 
                    />
                    <span className="text-sm">{option}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* B7.1c - What review process is available */}
            <div className="space-y-2">
              <Label className="text-sm font-medium">B7.1c What review process is available? (select all that apply)</Label>
              <div className="grid gap-2 md:grid-cols-2">
                {[
                  "human review of the decision/outcome",
                  "second-person review (peer/supervisor)",
                  "manual override available",
                  "re-run / reassessment with updated information",
                  "independent review function",
                  "only explanation provided (no review)",
                  "not specified / unclear"
                ].map((option) => (
                  <label key={option} className="flex items-center space-x-2">
                    <Checkbox 
                      checked={(form.B7_1_review_process || []).includes(option)} 
                      onCheckedChange={() => toggleInArray("B7_1_review_process", option)} 
                    />
                    <span className="text-sm">{option}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* B7.1d - What information supports review */}
            <div className="space-y-2">
              <Label className="text-sm font-medium">B7.1d What information supports review or challenge? (select all that apply)</Label>
              <div className="grid gap-2 md:grid-cols-2">
                {[
                  "decision record / case notes",
                  "ai outputs / scores",
                  "reason codes / explanation",
                  "input data used",
                  "model version / configuration recorded",
                  "human approval record captured",
                  "audit logs available",
                  "none / not available"
                ].map((option) => (
                  <label key={option} className="flex items-center space-x-2">
                    <Checkbox 
                      checked={(form.B7_1_review_inputs || []).includes(option)} 
                      onCheckedChange={() => toggleInArray("B7_1_review_inputs", option)} 
                    />
                    <span className="text-sm">{option}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* B7.1e - Can outcomes be changed */}
            <div className="space-y-2">
              <Label className="text-sm font-medium">B7.1e Can outcomes be changed following review?</Label>
              <select 
                value={form.B7_1_outcome_change || ''} 
                onChange={(e) => update("B7_1_outcome_change", e.target.value)} 
                className="w-full p-2 border rounded-md bg-white"
              >
                <option value="">Select option</option>
                <option value="yes — decision can be reversed or amended">yes — decision can be reversed or amended</option>
                <option value="partially — decision can be adjusted">partially — decision can be adjusted</option>
                <option value="no — decision cannot be changed">no — decision cannot be changed</option>
                <option value="unknown / not specified">unknown / not specified</option>
              </select>
            </div>

            {/* B7.1f - Notes */}
            <div className="space-y-2">
              <Label className="text-sm font-medium">B7.1f Notes / exceptions (optional)</Label>
              <Textarea
                value={form.B7_1_describe || ''}
                onChange={(e) => update("B7_1_describe", e.target.value)}
                placeholder="Any additional notes or exceptions"
                rows={2}
              />
            </div>
          </div>
        )}
      </div>

      {/* B7.2 */}
      <div className="space-y-2">
        <Label>B7.2 What is the expected response time for challenges?</Label>
        <div className="flex flex-wrap gap-3">
          {["24 hours", "48 hours", "1 week", "2 weeks", "1 month", "No defined timeframe"].map((opt) => (
            <label key={opt} className="flex items-center space-x-2">
              <input type="radio" checked={form.B7_2 === opt} onChange={() => update("B7_2", opt)} className="h-4 w-4 text-orange-600" />
              <span className="text-sm">{opt}</span>
            </label>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SectionB7;
