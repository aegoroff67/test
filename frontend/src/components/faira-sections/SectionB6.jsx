import React from 'react';
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { RadioScale } from './RadioScale';

const SectionB6 = ({ form, update }) => {
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

      {/* B6.3 */}
      <div className="space-y-2">
        <Label htmlFor="B6_3">B6.3 How are users informed about AI involvement?</Label>
        <Input 
          id="B6_3" 
          value={form.B6_3 || ''} 
          onChange={(e) => update("B6_3", e.target.value)} 
          placeholder="Describe how users are informed (e.g., in-app disclosure, terms of service, etc.)" 
        />
      </div>

      {/* B6.4 */}
      <div className="space-y-3">
        <Label>B6.4 Are known limitations disclosed?</Label>
        <div className="flex space-x-4">
          {["Yes", "No"].map((opt) => (
            <label key={opt} className="flex items-center space-x-2">
              <input type="radio" checked={form.B6_4 === opt} onChange={() => update("B6_4", opt)} className="h-4 w-4 text-orange-600" />
              <span className="text-sm">{opt}</span>
            </label>
          ))}
        </div>
        
        {form.B6_4 === "Yes" && (
          <div className="ml-4 p-4 bg-gray-50 rounded-lg space-y-2">
            <Label htmlFor="B6_4_describe">Describe the limitations disclosed:</Label>
            <Input 
              id="B6_4_describe" 
              value={form.B6_4_describe || ''} 
              onChange={(e) => update("B6_4_describe", e.target.value)} 
              placeholder="Describe the limitations" 
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default SectionB6;
