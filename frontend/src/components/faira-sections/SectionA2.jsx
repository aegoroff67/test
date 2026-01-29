import React from 'react';
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Separator } from "@/components/ui/separator";
import { RadioScale } from './RadioScale';

const SectionA2 = ({ form, update, toggleInArray }) => {
  return (
    <div className="space-y-6 pt-6 border-t" id="A2_1">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-1">A2. Data and Inputs</h3>
        <p className="text-sm text-gray-600">Maps to FAIRA 1.8-1.9 (data used and data quality) and AI use inputs (Table 3)</p>
      </div>
      <Separator />
      
      {/* A2.1 */}
      <div className="space-y-2">
        <Label>A2.1 How are AI use inputs tracked and recorded? (Select all that apply)</Label>
        <div className="grid gap-2 md:grid-cols-2">
          {[
            "audit logs",
            "access logs",
            "CRM/case management logging",
            "system-level logging",
            "manual records",
            "no inputs tracked or recorded (flag as risk)"
          ].map((option) => (
            <label key={option} className="flex items-center space-x-2">
              <Checkbox
                checked={form.A2_1.includes(option)}
                onCheckedChange={() => toggleInArray("A2_1", option)}
              />
              <span className="text-sm">{option}</span>
            </label>
          ))}
        </div>
      </div>

      {/* A2.2 - Gate Question */}
      <div className="space-y-2">
        <Label>A2.2 Does the AI require data from the digital or physical environment?</Label>
        <div className="flex space-x-4">
          <label className="flex items-center space-x-2">
            <input
              type="radio"
              name="A2_2"
              checked={form.A2_2 === "Yes"}
              onChange={() => update("A2_2", "Yes")}
              className="form-radio"
            />
            <span className="text-sm">Yes</span>
          </label>
          <label className="flex items-center space-x-2">
            <input
              type="radio"
              name="A2_2"
              checked={form.A2_2 === "No"}
              onChange={() => {
                update("A2_2", "No");
                update("A2_2_sources", []);
                update("A2_2_sources_other", "");
                update("A2_2_data_types", []);
                update("A2_2_data_types_other", "");
                update("A2_2_user_limits", "");
                update("A2_2_traceability", "");
                update("A2_2_trace_mechanisms", []);
                update("A2_2_notes", "");
              }}
              className="form-radio"
            />
            <span className="text-sm">No</span>
          </label>
        </div>
      </div>

      {/* A2.2 Sub-questions */}
      {form.A2_2 === "Yes" && (
        <div className="ml-4 pl-4 border-l-2 border-blue-200 space-y-4 bg-blue-50/30 p-4 rounded-r-lg">
          {/* A2.2a - Data Sources */}
          <div className="space-y-2">
            <Label>A2.2a Data sources (select all that apply)</Label>
            <div className="grid gap-2 md:grid-cols-2">
              {[
                "Digital systems (databases, internal apps, APIs)",
                "Web / internet sources",
                "Sensors / IoT / OT telemetry",
                "CCTV / images / video feeds",
                "Location / GPS / movement telemetry",
                "User device data",
                "Third-party data feeds",
                "Other"
              ].map((option) => (
                <label key={option} className="flex items-center space-x-2">
                  <Checkbox
                    checked={form.A2_2_sources.includes(option)}
                    onCheckedChange={() => toggleInArray("A2_2_sources", option)}
                  />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
            </div>
            {form.A2_2_sources.includes("Other") && (
              <Input
                value={form.A2_2_sources_other}
                onChange={(e) => update("A2_2_sources_other", e.target.value)}
                placeholder="Specify other data sources"
                className="mt-2"
              />
            )}
          </div>

          {/* A2.2b - Data Types */}
          <div className="space-y-2">
            <Label>A2.2b Data types ingested (select all that apply)</Label>
            <div className="grid gap-2 md:grid-cols-2">
              {[
                "Telemetry / operational metrics",
                "Environmental readings (e.g., weather, air quality)",
                "Images / video",
                "Audio",
                "Location data",
                "System logs / events",
                "Documents / free text",
                "Other"
              ].map((option) => (
                <label key={option} className="flex items-center space-x-2">
                  <Checkbox
                    checked={form.A2_2_data_types.includes(option)}
                    onCheckedChange={() => toggleInArray("A2_2_data_types", option)}
                  />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
            </div>
            {form.A2_2_data_types.includes("Other") && (
              <Input
                value={form.A2_2_data_types_other}
                onChange={(e) => update("A2_2_data_types_other", e.target.value)}
                placeholder="Specify other data types"
                className="mt-2"
              />
            )}
          </div>

          {/* A2.2c - User Limits */}
          <div className="space-y-2">
            <Label>A2.2c Can users limit what data is collected or used?</Label>
            <div className="flex flex-col space-y-2">
              {[
                "Yes — configurable controls",
                "Yes — per user / per transaction choice",
                "No",
                "Unknown / Not specified"
              ].map((option) => (
                <label key={option} className="flex items-center space-x-2">
                  <input
                    type="radio"
                    name="A2_2_user_limits"
                    checked={form.A2_2_user_limits === option}
                    onChange={() => update("A2_2_user_limits", option)}
                    className="form-radio"
                  />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
            </div>
          </div>

          {/* A2.2d - Traceability */}
          <div className="space-y-2">
            <Label>A2.2d Can the ingested data be traced back to its source?</Label>
            <div className="flex flex-col space-y-2">
              {[
                "Fully traceable",
                "Partially traceable",
                "Not traceable",
                "Unknown / Not specified"
              ].map((option) => (
                <label key={option} className="flex items-center space-x-2">
                  <input
                    type="radio"
                    name="A2_2_traceability"
                    checked={form.A2_2_traceability === option}
                    onChange={() => update("A2_2_traceability", option)}
                    className="form-radio"
                  />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
            </div>
          </div>

          {/* A2.2e - Traceability Mechanisms */}
          <div className="space-y-2">
            <Label>A2.2e Traceability mechanisms (select all that apply)</Label>
            <div className="grid gap-2 md:grid-cols-2">
              {[
                "Audit logs",
                "Data lineage tooling",
                "Source identifiers / metadata tags",
                "Case/record IDs",
                "Manual records",
                "Not in place"
              ].map((option) => (
                <label key={option} className="flex items-center space-x-2">
                  <Checkbox
                    checked={form.A2_2_trace_mechanisms.includes(option)}
                    onCheckedChange={() => toggleInArray("A2_2_trace_mechanisms", option)}
                  />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
            </div>
          </div>

          {/* A2.2f - Notes */}
          <div className="space-y-2">
            <Label htmlFor="A2_2_notes">A2.2f Notes / exceptions (optional)</Label>
            <Textarea
              id="A2_2_notes"
              value={form.A2_2_notes}
              onChange={(e) => update("A2_2_notes", e.target.value)}
              placeholder="Add any additional notes or exceptions..."
              rows={2}
            />
          </div>
        </div>
      )}

      {/* A2.3 */}
      <div className="space-y-2">
        <Label>A2.3 What safeguards exist to detect and handle corrupted, missing, or out-of-range data inputs? (Select all that apply)</Label>
        <div className="grid gap-2 md:grid-cols-2">
          {[
            "input validation",
            "range checking",
            "schema enforcement",
            "fallback defaults",
            "human review",
            "data quality monitoring",
            "error alerts",
            "no safeguards identified (flag as risk)"
          ].map((option) => (
            <label key={option} className="flex items-center space-x-2">
              <Checkbox
                checked={form.A2_3.includes(option)}
                onCheckedChange={() => toggleInArray("A2_3", option)}
              />
              <span className="text-sm">{option}</span>
            </label>
          ))}
        </div>
      </div>

      {/* A2.4 */}
      <div className="space-y-2">
        <Label>A2.4 What data does the AI solution use? (Select all that apply)</Label>
        <div className="grid gap-2 md:grid-cols-2">
          {[
            "government data",
            "open data",
            "synthetic data",
            "personal information",
            "sensitive information",
            "internet data"
          ].map((option) => (
            <label key={option} className="flex items-center space-x-2">
              <Checkbox
                checked={form.A2_4.includes(option)}
                onCheckedChange={() => toggleInArray("A2_4", option)}
              />
              <span className="text-sm">{option}</span>
            </label>
          ))}
          <label className="flex items-center space-x-2">
            <Checkbox
              checked={form.A2_4.includes("Other")}
              onCheckedChange={() => toggleInArray("A2_4", "Other")}
            />
            <span className="text-sm">Other (specify)</span>
          </label>
        </div>
        {form.A2_4.includes("Other") && (
          <Input
            value={form.A2_4_other}
            onChange={(e) => update("A2_4_other", e.target.value)}
            placeholder="Please specify other data types"
            className="mt-2"
          />
        )}
      </div>

      {/* A2.5 */}
      <div className="space-y-4">
        <Label>A2.5 Rate the quality of the input data (1 = Very Low, 5 = Very High):</Label>
        <div className="space-y-3 ml-4">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium w-32">Accuracy:</span>
            <RadioScale 
              value={form.A2_5_accuracy} 
              onChange={(val) => update("A2_5_accuracy", val)} 
            />
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium w-32">Completeness:</span>
            <RadioScale 
              value={form.A2_5_completeness} 
              onChange={(val) => update("A2_5_completeness", val)} 
            />
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium w-32">Reliability:</span>
            <RadioScale 
              value={form.A2_5_reliability} 
              onChange={(val) => update("A2_5_reliability", val)} 
            />
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium w-32">Relevance:</span>
            <RadioScale 
              value={form.A2_5_relevance} 
              onChange={(val) => update("A2_5_relevance", val)} 
            />
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium w-32">Timeliness:</span>
            <RadioScale 
              value={form.A2_5_timeliness} 
              onChange={(val) => update("A2_5_timeliness", val)} 
            />
          </div>
        </div>
      </div>

      {/* A2.6 */}
      <div className="space-y-2">
        <Label>A2.6 What is the Business Impact Level (BIL) of the input data?</Label>
        <select
          value={form.A2_6}
          onChange={(e) => update("A2_6", e.target.value)}
          className="w-full p-2 border rounded-md"
        >
          <option value="">Select BIL</option>
          <option value="Official">Official</option>
          <option value="Official: Sensitive">Official: Sensitive</option>
          <option value="Protected">Protected</option>
          <option value="Highly Protected">Highly Protected</option>
          <option value="Secret">Secret</option>
          <option value="Top Secret">Top Secret</option>
        </select>
      </div>

      {/* A2.7 */}
      <div className="space-y-3" id="A2_7">
        <Label>A2.7 Does the solution use regulated or sensitive data?</Label>
        <div className="flex space-x-4">
          <label className="flex items-center space-x-2">
            <input
              type="radio"
              checked={form.A2_7 === "Yes"}
              onChange={() => update("A2_7", "Yes")}
              className="h-4 w-4 text-orange-600"
            />
            <span className="text-sm">Yes</span>
          </label>
          <label className="flex items-center space-x-2">
            <input
              type="radio"
              checked={form.A2_7 === "No"}
              onChange={() => update("A2_7", "No")}
              className="h-4 w-4 text-orange-600"
            />
            <span className="text-sm">No</span>
          </label>
        </div>
        
        {form.A2_7 === "Yes" && (
          <div className="ml-4 p-4 bg-gray-50 rounded-lg space-y-2">
            <Label>Select the types of regulated/sensitive data used (Select all that apply):</Label>
            <div className="grid gap-2 md:grid-cols-2">
              {[
                "health information",
                "mental health information",
                "child protection information",
                "criminal justice / law enforcement data",
                "biometric data (faces, fingerprints, gait, voice, etc.)",
                "genetic information",
                "financial information",
                "taxation information",
                "indigenous cultural or sacred data",
                "location tracking data",
                "safety-critical operational data",
                "vulnerable persons data",
                "Other regulated/sensitive data (specify)"
              ].map((option) => (
                <label key={option} className="flex items-center space-x-2">
                  <Checkbox
                    checked={form.A2_7_data_types.includes(option)}
                    onCheckedChange={() => toggleInArray("A2_7_data_types", option)}
                  />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
            </div>
            
            {form.A2_7_data_types.includes("Other regulated/sensitive data (specify)") && (
              <div className="mt-3">
                <Input
                  id="A2_7_data_types_other"
                  value={form.A2_7_data_types_other}
                  onChange={(e) => update("A2_7_data_types_other", e.target.value)}
                  placeholder="Specify other regulated/sensitive data type"
                  className="mt-2"
                />
              </div>
            )}
          </div>
        )}
      </div>

      {/* A2.8 */}
      <div className="space-y-3">
        <Label>A2.8 Does the solution require user inputs to operate?</Label>
        <div className="flex space-x-4">
          <label className="flex items-center space-x-2">
            <input
              type="radio"
              checked={form.A2_8 === "Yes"}
              onChange={() => update("A2_8", "Yes")}
              className="h-4 w-4 text-orange-600"
            />
            <span className="text-sm">Yes</span>
          </label>
          <label className="flex items-center space-x-2">
            <input
              type="radio"
              checked={form.A2_8 === "No"}
              onChange={() => update("A2_8", "No")}
              className="h-4 w-4 text-orange-600"
            />
            <span className="text-sm">No</span>
          </label>
        </div>
        
        {form.A2_8 === "Yes" && (
          <div className="ml-4 p-4 bg-gray-50 rounded-lg space-y-2">
            <Label>Select the types of inputs (Select all that apply):</Label>
            <div className="grid gap-2 md:grid-cols-2">
              {[
                "free-text prompts",
                "uploaded files",
                "form fields",
                "API request data",
                "structured records",
                "voice input",
                "sensor data",
                "user selection/choices"
              ].map((option) => (
                <label key={option} className="flex items-center space-x-2">
                  <Checkbox
                    checked={form.A2_8_types.includes(option)}
                    onCheckedChange={() => toggleInArray("A2_8_types", option)}
                  />
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

export default SectionA2;
