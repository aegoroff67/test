import React from 'react';
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Separator } from "@/components/ui/separator";
import { RadioScale } from './RadioScale';
import EvidenceAttachLink, { EVIDENCE_TOOLTIPS } from '../EvidenceAttachLink';

const SectionA3 = ({ form, update, toggleInArray, assessmentId, currentUser }) => {
  return (
    <div className="space-y-6 pt-6 border-t" id="A3_1">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-1">A3. Human Interface and Impact</h3>
        <p className="text-sm text-gray-600">Maps to FAIRA Table 2 (HMI) and Table 5 (Object of AI action)</p>
      </div>
      <Separator />
      
      {/* A3.1 */}
      <div className="space-y-2" id="A3_1">
        <div className="flex items-center justify-between">
          <Label>A3.1 How does the system interface with humans? (Select all that apply)</Label>
          {assessmentId && (
            <EvidenceAttachLink 
              questionCode="A3-1" 
              assessmentId={assessmentId} 
              currentUser={currentUser}
              tooltip={EVIDENCE_TOOLTIPS['A3-1']}
            />
          )}
        </div>
        <div className="grid gap-2 md:grid-cols-2">
          {["chat interface", "web application", "mobile application", "API integration", "voice interface", "dashboard"].map((option) => (
            <label key={option} className="flex items-center space-x-2">
              <Checkbox checked={form.A3_1.includes(option)} onCheckedChange={() => toggleInArray("A3_1", option)} />
              <span className="text-sm">{option}</span>
            </label>
          ))}
        </div>
      </div>

      {/* A3.2 */}
      <div className="space-y-4" id="A3_2_technical">
        <Label>A3.2 What expertise is required to use the AI solution? (1 = Very Low, 5 = Very High):</Label>
        <div className="space-y-3 ml-4">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium w-48">Technical expertise:</span>
            <RadioScale value={form.A3_2_technical} onChange={(val) => update("A3_2_technical", val)} />
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium w-48">Domain knowledge:</span>
            <RadioScale value={form.A3_2_domain} onChange={(val) => update("A3_2_domain", val)} />
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium w-48">AI literacy:</span>
            <RadioScale value={form.A3_2_ai_literacy} onChange={(val) => update("A3_2_ai_literacy", val)} />
          </div>
        </div>
      </div>

      {/* A3.3 */}
      <div className="space-y-2" id="A3_3">
        <div className="flex items-center justify-between">
          <Label>A3.3 Who will be impacted by the AI system? (Select all that apply)</Label>
          {assessmentId && (
            <EvidenceAttachLink 
              questionCode="A3-3" 
              assessmentId={assessmentId} 
              currentUser={currentUser}
              tooltip={EVIDENCE_TOOLTIPS['A3-3']}
            />
          )}
        </div>
        <div className="grid gap-2 md:grid-cols-2">
          {["Queensland Government employees", "general public", "vulnerable communities", "children", "elderly", "people with disabilities", "Indigenous peoples", "small businesses"].map((option) => (
            <label key={option} className="flex items-center space-x-2">
              <Checkbox checked={form.A3_3.includes(option)} onCheckedChange={() => toggleInArray("A3_3", option)} />
              <span className="text-sm">{option}</span>
            </label>
          ))}
          <label className="flex items-center space-x-2">
            <Checkbox checked={form.A3_3.includes("Other")} onCheckedChange={() => toggleInArray("A3_3", "Other")} />
            <span className="text-sm">Other (specify)</span>
          </label>
        </div>
        {form.A3_3.includes("Other") && (
          <Input value={form.A3_3_other} onChange={(e) => update("A3_3_other", e.target.value)} placeholder="Please specify other impacted groups" className="mt-2" />
        )}
      </div>

      {/* A3.4 */}
      <div className="space-y-2" id="A3_4">
        <Label>A3.4 How will impacted parties be informed of AI use? (Select all that apply)</Label>
        <div className="grid gap-2 md:grid-cols-2">
          {["website notice", "in-app notice", "email communication", "terms and conditions", "public-facing AI statement", "staff training", "consent/acknowledgement", "no planned notifications (flag as risk)"].map((option) => (
            <label key={option} className="flex items-center space-x-2">
              <Checkbox checked={form.A3_4.includes(option)} onCheckedChange={() => toggleInArray("A3_4", option)} />
              <span className="text-sm">{option}</span>
            </label>
          ))}
        </div>
      </div>

      {/* A3.5 */}
      <div className="space-y-3" id="A3_5a">
        <Label>A3.5(a) What are the expected impacts of this AI solution on staff? (Select all that apply)</Label>
        <div className="grid gap-2 md:grid-cols-2">
          {["increased workload", "reduced workload", "reduced autonomy", "improved autonomy", "de-skilling risk", "skill enhancement", "accountability ambiguity", "increased accountability clarity", "stress or psychological impact", "job redesign required", "no significant impact"].map((option) => (
            <label key={option} className="flex items-center space-x-2">
              <Checkbox checked={form.A3_5a.includes(option)} onCheckedChange={() => toggleInArray("A3_5a", option)} />
              <span className="text-sm">{option}</span>
            </label>
          ))}
        </div>
        <div className="mt-4">
          <Label>A3.5(b) Rate the overall severity of these impacts (1 = Very Low, 5 = Very High):</Label>
          <div className="mt-2">
            <RadioScale value={form.A3_5b} onChange={(val) => update("A3_5b", val)} />
          </div>
        </div>
      </div>

      {/* A3.6 */}
      <div className="space-y-3" id="A3_6a">
        <Label>A3.6(a) How will each impacted group be affected? (Select all that apply)</Label>
        <div className="grid gap-2 md:grid-cols-2">
          {["service quality changes", "accessibility changes", "decision-making impacts", "delay reduction", "bias or fairness concerns", "data/privacy concerns", "security concerns", "communication changes", "risk of exclusion", "increased assistance/support", "none/minimal impact"].map((option) => (
            <label key={option} className="flex items-center space-x-2">
              <Checkbox checked={form.A3_6a.includes(option)} onCheckedChange={() => toggleInArray("A3_6a", option)} />
              <span className="text-sm">{option}</span>
            </label>
          ))}
        </div>
        <div className="mt-4">
          <Label>A3.6(b) Rate the overall severity of these impacts (1 = Minor, 2 = Moderate, 3 = Major):</Label>
          <div className="mt-2">
            <RadioScale value={form.A3_6b} onChange={(val) => update("A3_6b", val)} min={1} max={3} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default SectionA3;
