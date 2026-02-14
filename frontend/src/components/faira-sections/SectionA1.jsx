import React from 'react';
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Separator } from "@/components/ui/separator";
import EvidenceAttachLink, { EVIDENCE_TOOLTIPS } from '../EvidenceAttachLink';

const SectionA1 = ({ form, update, toggleInArray, assessmentId, currentUser }) => {
  return (
    <div className="space-y-6" id="A1_1">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-1">A1. AI Solution Fundamentals</h3>
        <p className="text-sm text-gray-600">Maps to FAIRA Table 1: AI solution (Questions 1.1-1.10)</p>
      </div>
      <Separator />
      
      {/* A1.1 */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <Label>A1.1 What is the primary function of the AI solution? (Select all that apply)</Label>
          {assessmentId && (
            <EvidenceAttachLink 
              questionCode="A1-1" 
              assessmentId={assessmentId} 
              currentUser={currentUser}
              tooltip={EVIDENCE_TOOLTIPS['A1-1']}
            />
          )}
        </div>
        <div className="grid gap-2 md:grid-cols-2">
          {[
            "information retrieval",
            "natural language understanding",
            "prediction/forecasting",
            "classification",
            "recommendation",
            "summarisation",
            "decision support",
            "process automation",
            "compliance monitoring",
            "content generation"
          ].map((option) => (
            <label key={option} className="flex items-center space-x-2">
              <Checkbox
                checked={form.A1_1.includes(option)}
                onCheckedChange={() => toggleInArray("A1_1", option)}
              />
              <span className="text-sm">{option}</span>
            </label>
          ))}
        </div>
      </div>

      {/* A1.2 */}
      <div className="space-y-2">
        <Label htmlFor="A1_2">A1.2 What version of the AI solution does this FAIRA assessment apply to?</Label>
        <Input
          id="A1_2"
          value={form.A1_2}
          onChange={(e) => update("A1_2", e.target.value)}
          placeholder="e.g., v1.2.0"
        />
      </div>

      {/* A1.3 */}
      <div className="space-y-2">
        <Label>A1.3 Select all AI features that apply:</Label>
        <div className="grid gap-2 md:grid-cols-2">
          {[
            "natural language processing",
            "data analysis and visualization",
            "automated content generation",
            "integration with existing systems",
            "personalized recommendations",
            "collaboration enhancement",
            "task automation",
            "security and compliance",
            "voice recognition"
          ].map((option) => (
            <label key={option} className="flex items-center space-x-2">
              <Checkbox
                checked={form.A1_3.includes(option)}
                onCheckedChange={() => toggleInArray("A1_3", option)}
              />
              <span className="text-sm">{option}</span>
            </label>
          ))}
          <label className="flex items-center space-x-2">
            <Checkbox
              checked={form.A1_3.includes("Other")}
              onCheckedChange={() => toggleInArray("A1_3", "Other")}
            />
            <span className="text-sm">Other (specify)</span>
          </label>
        </div>
        {form.A1_3.includes("Other") && (
          <Input
            value={form.A1_3_other}
            onChange={(e) => update("A1_3_other", e.target.value)}
            placeholder="Please specify other AI features"
            className="mt-2"
          />
        )}
      </div>

      {/* A1.4 */}
      <div className="space-y-2">
        <Label>A1.4 What decisions will be addressed by the AI functionality? (Select all that apply)</Label>
        <div className="grid gap-2 md:grid-cols-2">
          {[
            "content development and approval",
            "data interpretation and business strategy",
            "prioritization of communications",
            "workflow optimization",
            "security and compliance oversight",
            "resource allocation",
            "crisis management",
            "employee training",
            "customer relationship management",
            "administrative decision-making (regulated by law)"
          ].map((option) => (
            <label key={option} className="flex items-center space-x-2">
              <Checkbox
                checked={form.A1_4.includes(option)}
                onCheckedChange={() => toggleInArray("A1_4", option)}
              />
              <span className="text-sm">{option}</span>
            </label>
          ))}
        </div>
      </div>

      {/* A1.5 */}
      <div className="space-y-2">
        <Label>A1.5 What tangible benefits does this AI solution provide? (Select all that apply)</Label>
        <div className="grid gap-2 md:grid-cols-2">
          {[
            "increased efficiency",
            "reduced manual effort",
            "improved decision-making",
            "faster processing time",
            "improved accuracy or consistency",
            "enhanced user experience",
            "cost reduction",
            "improved accessibility",
            "reduced risk or error",
            "better service delivery",
            "improved communication",
            "increased transparency"
          ].map((option) => (
            <label key={option} className="flex items-center space-x-2">
              <Checkbox
                checked={form.A1_5.includes(option)}
                onCheckedChange={() => toggleInArray("A1_5", option)}
              />
              <span className="text-sm">{option}</span>
            </label>
          ))}
        </div>
      </div>

      {/* A1.6 */}
      <div className="space-y-3">
        <Label>A1.6 Can the AI solution convert decisions into actions without human intervention?</Label>
        <div className="flex space-x-4">
          <label className="flex items-center space-x-2">
            <input
              type="radio"
              checked={form.A1_6 === "Yes"}
              onChange={() => update("A1_6", "Yes")}
              className="h-4 w-4 text-orange-600"
            />
            <span className="text-sm">Yes</span>
          </label>
          <label className="flex items-center space-x-2">
            <input
              type="radio"
              checked={form.A1_6 === "No"}
              onChange={() => update("A1_6", "No")}
              className="h-4 w-4 text-orange-600"
            />
            <span className="text-sm">No</span>
          </label>
        </div>
        
        {form.A1_6 === "Yes" && (
          <div className="ml-4 p-4 bg-gray-50 rounded-lg space-y-2">
            <Label>Describe these actions (Select all that apply):</Label>
            <div className="grid gap-2 md:grid-cols-2">
              {[
                "sends notifications",
                "updates internal records",
                "applies rules/decisions automatically",
                "initiates workflows",
                "generates external communications",
                "allocates resources",
                "approves/declines items",
                "triggers system events"
              ].map((option) => (
                <label key={option} className="flex items-center space-x-2">
                  <Checkbox
                    checked={form.A1_6_actions.includes(option)}
                    onCheckedChange={() => toggleInArray("A1_6_actions", option)}
                  />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
              <label className="flex items-center space-x-2">
                <Checkbox
                  checked={form.A1_6_actions.includes("Other")}
                  onCheckedChange={() => toggleInArray("A1_6_actions", "Other")}
                />
                <span className="text-sm">Other (specify)</span>
              </label>
            </div>
            {form.A1_6_actions.includes("Other") && (
              <Input
                value={form.A1_6_actions_other}
                onChange={(e) => update("A1_6_actions_other", e.target.value)}
                placeholder="Please specify other actions"
                className="mt-2"
              />
            )}
          </div>
        )}
      </div>

      {/* A1.7 */}
      <div className="space-y-2">
        <Label>A1.7 What type of AI model or technique is used? (Select all that apply)</Label>
        <div className="grid gap-2 md:grid-cols-2">
          {[
            "Large Language Model",
            "computer vision",
            "supervised learning",
            "unsupervised learning",
            "reinforcement learning",
            "rule-based system",
            "neural network"
          ].map((option) => (
            <label key={option} className="flex items-center space-x-2">
              <Checkbox
                checked={form.A1_7.includes(option)}
                onCheckedChange={() => toggleInArray("A1_7", option)}
              />
              <span className="text-sm">{option}</span>
            </label>
          ))}
          <label className="flex items-center space-x-2">
            <Checkbox
              checked={form.A1_7.includes("Other")}
              onCheckedChange={() => toggleInArray("A1_7", "Other")}
            />
            <span className="text-sm">Other (specify)</span>
          </label>
        </div>
        {form.A1_7.includes("Other") && (
          <Input
            value={form.A1_7_other}
            onChange={(e) => update("A1_7_other", e.target.value)}
            placeholder="Please specify other AI model types"
            className="mt-2"
          />
        )}
      </div>

      {/* A1.8 */}
      <div className="space-y-2">
        <Label>A1.8 What is the source of the AI solution? (Select all that apply)</Label>
        <div className="grid gap-2 md:grid-cols-2">
          {[
            "commercial off-the-shelf",
            "bespoke development",
            "open-source",
            "hybrid approach"
          ].map((option) => (
            <label key={option} className="flex items-center space-x-2">
              <Checkbox
                checked={form.A1_8.includes(option)}
                onCheckedChange={() => toggleInArray("A1_8", option)}
              />
              <span className="text-sm">{option}</span>
            </label>
          ))}
        </div>
      </div>

      {/* A1.9 */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <Label>A1.9 How does the AI solution integrate with other systems? (Select all that apply)</Label>
          {assessmentId && (
            <EvidenceAttachLink 
              questionCode="A1-9" 
              assessmentId={assessmentId} 
              currentUser={currentUser}
              tooltip={EVIDENCE_TOOLTIPS['A1-9']}
            />
          )}
        </div>
        <div className="grid gap-2 md:grid-cols-2">
          {[
            "REST API",
            "webhooks",
            "batch data transfer",
            "real-time data stream",
            "file-based integration",
            "embedded widget/iframe",
            "database connection",
            "message queue (e.g., Kafka)"
          ].map((option) => (
            <label key={option} className="flex items-center space-x-2">
              <Checkbox
                checked={form.A1_9.includes(option)}
                onCheckedChange={() => toggleInArray("A1_9", option)}
              />
              <span className="text-sm">{option}</span>
            </label>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SectionA1;
