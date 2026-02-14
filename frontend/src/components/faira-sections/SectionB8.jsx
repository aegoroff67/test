import React from 'react';
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Separator } from "@/components/ui/separator";
import EvidenceAttachLink from '../EvidenceAttachLink';

const SectionB8 = ({ form, update, toggleInArray, assessmentId, currentUser }) => {
  return (
    <div className="space-y-6 pt-6 border-t" id="B8_1">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-1">B8. Accountability</h3>
      </div>
      <Separator />
      
      {/* B8.1 */}
      <div className="space-y-2">
        <Label htmlFor="B8_1">B8.1 Who has oversight responsibility for the AI system?</Label>
        <Input 
          id="B8_1" 
          value={form.B8_1 || ''} 
          onChange={(e) => update("B8_1", e.target.value)} 
          placeholder="Enter the role or person responsible for oversight" 
        />
      </div>

      {/* B8.2 */}
      <div className="space-y-2">
        <Label>B8.2 Are roles and responsibilities clearly established?</Label>
        <div className="flex space-x-4">
          {["Yes", "No"].map((opt) => (
            <label key={opt} className="flex items-center space-x-2">
              <input type="radio" checked={form.B8_2 === opt} onChange={() => update("B8_2", opt)} className="h-4 w-4 text-orange-600" />
              <span className="text-sm">{opt}</span>
            </label>
          ))}
        </div>
      </div>

      {/* B8.3 */}
      <div className="space-y-2">
        <Label>B8.3 Is staff trained in AI system management?</Label>
        <div className="flex space-x-4">
          {["Yes", "No"].map((opt) => (
            <label key={opt} className="flex items-center space-x-2">
              <input type="radio" checked={form.B8_3 === opt} onChange={() => update("B8_3", opt)} className="h-4 w-4 text-orange-600" />
              <span className="text-sm">{opt}</span>
            </label>
          ))}
        </div>
      </div>

      {/* B8.4 */}
      <div className="space-y-3">
        <Label>B8.4 Are there safeguards in place for AI governance?</Label>
        <div className="flex space-x-4">
          {["Yes", "No"].map((opt) => (
            <label key={opt} className="flex items-center space-x-2">
              <input type="radio" checked={form.B8_4 === opt} onChange={() => update("B8_4", opt)} className="h-4 w-4 text-orange-600" />
              <span className="text-sm">{opt}</span>
            </label>
          ))}
        </div>
        
        {form.B8_4 === "Yes" && (
          <div className="ml-4 p-4 bg-gray-50 rounded-lg space-y-2">
            <Label>Which safeguards? (Select all that apply):</Label>
            <div className="grid gap-2 md:grid-cols-2">
              {["regular audits", "compliance monitoring", "incident reporting", "performance metrics", "governance committee", "external oversight", "documentation requirements", "change management process"].map((option) => (
                <label key={option} className="flex items-center space-x-2">
                  <Checkbox checked={(form.B8_4_safeguards || []).includes(option)} onCheckedChange={() => toggleInArray("B8_4_safeguards", option)} />
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
