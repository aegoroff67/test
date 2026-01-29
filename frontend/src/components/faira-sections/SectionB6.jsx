import React from 'react';
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Textarea } from "@/components/ui/textarea";
import { Separator } from "@/components/ui/separator";
import { RadioScale } from './RadioScale';

const SectionB6 = ({ form, update, toggleInArray }) => {
  return (
    <div className="space-y-6 pt-6 border-t" id="B6_1">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-1">B6. Transparency and Explainability</h3>
      </div>
      <Separator />
      
      {/* B6.1 */}
      <div className="space-y-3">
        <Label>B6.1 Rate the transparency of the AI system (1 = Very Low, 5 = Very High):</Label>
        <div className="ml-4">
          <RadioScale value={form.B6_1} onChange={(val) => update("B6_1", val)} />
        </div>
      </div>

      {/* B6.2 */}
      <div className="space-y-3">
        <Label>B6.2 Rate the explainability of AI decisions (1 = Very Low, 5 = Very High):</Label>
        <div className="ml-4">
          <RadioScale value={form.B6_2} onChange={(val) => update("B6_2", val)} />
        </div>
      </div>

      {/* B6.3 - Gated Section */}
      <div className="space-y-3">
        <Label>B6.3 Are users and/or affected individuals informed that AI is being used?</Label>
        <div className="flex space-x-4">
          <label className="flex items-center space-x-2">
            <input type="radio" checked={form.B6_3 === "Yes"} onChange={() => update("B6_3", "Yes")} className="h-4 w-4 text-orange-600" />
            <span className="text-sm">Yes</span>
          </label>
          <label className="flex items-center space-x-2">
            <input type="radio" checked={form.B6_3 === "No"} onChange={() => update("B6_3", "No")} className="h-4 w-4 text-orange-600" />
            <span className="text-sm">No</span>
          </label>
        </div>

        {/* Conditional subsections when Yes is selected */}
        {form.B6_3 === "Yes" && (
          <div className="ml-4 p-4 bg-gray-100 rounded-lg space-y-4 border border-gray-200">
            {/* B6.3a - Who is informed */}
            <div className="space-y-2">
              <Label className="text-sm font-medium">B6.3a Who is informed? (select all that apply)</Label>
              <div className="grid gap-2 md:grid-cols-2">
                {[
                  "direct users/operators",
                  "affected individuals (e.g., customers/citizens)",
                  "internal decision-makers/managers",
                  "regulators/oversight bodies (where applicable)",
                  "not specified / unclear"
                ].map((option) => (
                  <label key={option} className="flex items-center space-x-2">
                    <Checkbox 
                      checked={(form.B6_3_audience || []).includes(option)} 
                      onCheckedChange={() => toggleInArray("B6_3_audience", option)} 
                    />
                    <span className="text-sm">{option}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* B6.3b - How are they informed */}
            <div className="space-y-2">
              <Label className="text-sm font-medium">B6.3b How are they informed? (select all that apply)</Label>
              <div className="grid gap-2 md:grid-cols-2">
                {[
                  "in-application/on-screen notice",
                  "at point-of-service disclosure (staff script/verbal)",
                  "privacy notice / collection notice",
                  "terms & conditions / policy document",
                  "signage (physical environment)",
                  "email/sms notification",
                  "website disclosure",
                  "api / technical documentation"
                ].map((option) => (
                  <label key={option} className="flex items-center space-x-2">
                    <Checkbox 
                      checked={(form.B6_3_methods || []).includes(option)} 
                      onCheckedChange={() => toggleInArray("B6_3_methods", option)} 
                    />
                    <span className="text-sm">{option}</span>
                  </label>
                ))}
                <label className="flex items-center space-x-2">
                  <Checkbox 
                    checked={(form.B6_3_methods || []).includes("Other")} 
                    onCheckedChange={() => toggleInArray("B6_3_methods", "Other")} 
                  />
                  <span className="text-sm">Other (specify)</span>
                </label>
              </div>
              {(form.B6_3_methods || []).includes("Other") && (
                <Input
                  value={form.B6_3_methods_other || ''}
                  onChange={(e) => update("B6_3_methods_other", e.target.value)}
                  placeholder="Please specify other notification method"
                  className="mt-2"
                />
              )}
            </div>

            {/* B6.3c - When are they informed */}
            <div className="space-y-2">
              <Label className="text-sm font-medium">B6.3c When are they informed?</Label>
              <select 
                value={form.B6_3_timing || ''} 
                onChange={(e) => update("B6_3_timing", e.target.value)} 
                className="w-full p-2 border rounded-md bg-white"
              >
                <option value="">Select timing</option>
                <option value="before interaction/use">before interaction/use</option>
                <option value="at the point outputs are presented/used">at the point outputs are presented/used</option>
                <option value="after the outcome/decision">after the outcome/decision</option>
                <option value="only on request">only on request</option>
                <option value="unknown / not specified">unknown / not specified</option>
              </select>
            </div>

            {/* B6.3d - What information is provided */}
            <div className="space-y-2">
              <Label className="text-sm font-medium">B6.3d What information is provided as part of the disclosure? (select all that apply)</Label>
              <div className="grid gap-2 md:grid-cols-2">
                {[
                  "that ai is used",
                  "purpose of the ai system",
                  "what the ai outputs are used for",
                  "limitations/uncertainty of outputs",
                  "human oversight involvement",
                  "how to request an explanation",
                  "how to challenge/seek review",
                  "not specified / unclear"
                ].map((option) => (
                  <label key={option} className="flex items-center space-x-2">
                    <Checkbox 
                      checked={(form.B6_3_information_provided || []).includes(option)} 
                      onCheckedChange={() => toggleInArray("B6_3_information_provided", option)} 
                    />
                    <span className="text-sm">{option}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* B6.3e - Notes */}
            <div className="space-y-2">
              <Label className="text-sm font-medium">B6.3e Notes / exceptions (optional)</Label>
              <Textarea
                value={form.B6_3_notes || ''}
                onChange={(e) => update("B6_3_notes", e.target.value)}
                placeholder="Any additional notes or exceptions"
                rows={2}
              />
            </div>
          </div>
        )}
      </div>

      {/* B6.4 - Gated Section */}
      <div className="space-y-3">
        <Label>B6.4 Can meaningful explanations of AI-supported outcomes be provided to users and/or affected individuals?</Label>
        <div className="flex space-x-4">
          <label className="flex items-center space-x-2">
            <input type="radio" checked={form.B6_4 === "Yes"} onChange={() => update("B6_4", "Yes")} className="h-4 w-4 text-orange-600" />
            <span className="text-sm">Yes</span>
          </label>
          <label className="flex items-center space-x-2">
            <input type="radio" checked={form.B6_4 === "No"} onChange={() => update("B6_4", "No")} className="h-4 w-4 text-orange-600" />
            <span className="text-sm">No</span>
          </label>
        </div>

        {/* Conditional subsections when Yes is selected */}
        {form.B6_4 === "Yes" && (
          <div className="ml-4 p-4 bg-gray-100 rounded-lg space-y-4 border border-gray-200">
            {/* B6.4a - Who can receive explanations */}
            <div className="space-y-2">
              <Label className="text-sm font-medium">B6.4a Who can receive explanations? (select all that apply)</Label>
              <div className="grid gap-2 md:grid-cols-2">
                {[
                  "direct users/operators",
                  "affected individuals (e.g., customers/citizens)",
                  "internal decision-makers/managers",
                  "regulators/oversight bodies (where applicable)",
                  "not specified / unclear"
                ].map((option) => (
                  <label key={option} className="flex items-center space-x-2">
                    <Checkbox 
                      checked={(form.B6_4_audience || []).includes(option)} 
                      onCheckedChange={() => toggleInArray("B6_4_audience", option)} 
                    />
                    <span className="text-sm">{option}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* B6.4b - How are explanations provided */}
            <div className="space-y-2">
              <Label className="text-sm font-medium">B6.4b How are explanations provided? (select all that apply)</Label>
              <div className="grid gap-2 md:grid-cols-2">
                {[
                  "on-screen explanation at decision/output point",
                  "reason codes / factors list",
                  "case notes / decision record",
                  "help article / faq / knowledge base",
                  "support channel (phone/email) explanation",
                  "formal written explanation on request",
                  "technical documentation only"
                ].map((option) => (
                  <label key={option} className="flex items-center space-x-2">
                    <Checkbox 
                      checked={(form.B6_4_explanation_methods || []).includes(option)} 
                      onCheckedChange={() => toggleInArray("B6_4_explanation_methods", option)} 
                    />
                    <span className="text-sm">{option}</span>
                  </label>
                ))}
                <label className="flex items-center space-x-2">
                  <Checkbox 
                    checked={(form.B6_4_explanation_methods || []).includes("Other")} 
                    onCheckedChange={() => toggleInArray("B6_4_explanation_methods", "Other")} 
                  />
                  <span className="text-sm">Other (specify)</span>
                </label>
              </div>
              {(form.B6_4_explanation_methods || []).includes("Other") && (
                <Input
                  value={form.B6_4_explanation_methods_other || ''}
                  onChange={(e) => update("B6_4_explanation_methods_other", e.target.value)}
                  placeholder="Please specify other explanation method"
                  className="mt-2"
                />
              )}
            </div>

            {/* B6.4c - When are explanations available */}
            <div className="space-y-2">
              <Label className="text-sm font-medium">B6.4c When are explanations available?</Label>
              <select 
                value={form.B6_4_timing || ''} 
                onChange={(e) => update("B6_4_timing", e.target.value)} 
                className="w-full p-2 border rounded-md bg-white"
              >
                <option value="">Select timing</option>
                <option value="before interaction/use (pre-emptive explanation)">before interaction/use (pre-emptive explanation)</option>
                <option value="at the point outputs are presented/used">at the point outputs are presented/used</option>
                <option value="after the outcome/decision (on request)">after the outcome/decision (on request)</option>
                <option value="only during a formal review/appeal process">only during a formal review/appeal process</option>
                <option value="unknown / not specified">unknown / not specified</option>
              </select>
            </div>

            {/* B6.4d - What does the explanation include */}
            <div className="space-y-2">
              <Label className="text-sm font-medium">B6.4d What does the explanation include? (select all that apply)</Label>
              <div className="grid gap-2 md:grid-cols-2">
                {[
                  "purpose of the ai system",
                  "what inputs influenced the outcome",
                  "key factors/attributes driving the outcome",
                  "confidence/uncertainty indicators",
                  "human oversight involvement",
                  "how to request further explanation",
                  "how to challenge/seek review",
                  "not specified / unclear"
                ].map((option) => (
                  <label key={option} className="flex items-center space-x-2">
                    <Checkbox 
                      checked={(form.B6_4_explanation_content || []).includes(option)} 
                      onCheckedChange={() => toggleInArray("B6_4_explanation_content", option)} 
                    />
                    <span className="text-sm">{option}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* B6.4e - How accessible are explanations */}
            <div className="space-y-2">
              <Label className="text-sm font-medium">B6.4e How accessible are explanations to non-technical audiences?</Label>
              <select 
                value={form.B6_4_accessibility || ''} 
                onChange={(e) => update("B6_4_accessibility", e.target.value)} 
                className="w-full p-2 border rounded-md bg-white"
              >
                <option value="">Select accessibility level</option>
                <option value="plain language (non-technical, easy to understand)">plain language (non-technical, easy to understand)</option>
                <option value="somewhat technical (requires guidance)">somewhat technical (requires guidance)</option>
                <option value="highly technical (specialist interpretation required)">highly technical (specialist interpretation required)</option>
                <option value="unknown / not specified">unknown / not specified</option>
              </select>
            </div>

            {/* B6.4f - Are limitations communicated */}
            <div className="space-y-2">
              <Label className="text-sm font-medium">B6.4f Are limitations/uncertainty and appropriate use constraints communicated with explanations?</Label>
              <select 
                value={form.B6_4_limitations_disclosed || ''} 
                onChange={(e) => update("B6_4_limitations_disclosed", e.target.value)} 
                className="w-full p-2 border rounded-md bg-white"
              >
                <option value="">Select option</option>
                <option value="yes — clearly communicated">yes — clearly communicated</option>
                <option value="partially — mentioned but not consistently">partially — mentioned but not consistently</option>
                <option value="no">no</option>
                <option value="unknown / not specified">unknown / not specified</option>
              </select>
            </div>

            {/* B6.4g - Notes */}
            <div className="space-y-2">
              <Label className="text-sm font-medium">B6.4g Notes / exceptions (optional)</Label>
              <Textarea
                value={form.B6_4_notes || ''}
                onChange={(e) => update("B6_4_notes", e.target.value)}
                placeholder="Any additional notes or exceptions"
                rows={2}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SectionB6;
