import React from 'react';
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";

const SectionB7 = ({ form, update }) => {
  return (
    <div className="space-y-6 pt-6 border-t" id="B7_1">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-1">B7. Contestability</h3>
      </div>
      <Separator />
      
      {/* B7.1 */}
      <div className="space-y-3">
        <Label>B7.1 Is there a process for challenging AI decisions?</Label>
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
            <Label htmlFor="B7_1_describe">Describe the challenge process:</Label>
            <Input 
              id="B7_1_describe" 
              value={form.B7_1_describe || ''} 
              onChange={(e) => update("B7_1_describe", e.target.value)} 
              placeholder="Describe how decisions can be challenged" 
            />
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
