import React from 'react';
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Separator } from "@/components/ui/separator";

const SectionA4 = ({ form, update, toggleInArray }) => {
  return (
    <div className="space-y-6 pt-6 border-t" id="A4_1">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-1">A4. Outputs and Actions</h3>
        <p className="text-sm text-gray-600">Maps to FAIRA Table 4: AI use outputs</p>
      </div>
      <Separator />
      
      {/* A4.1 */}
      <div className="space-y-2">
        <Label>A4.1 What are the primary outputs of the AI system? (Select all that apply)</Label>
        <div className="grid gap-2 md:grid-cols-2">
          {["text responses", "visual outputs", "recommendations", "decisions", "data analysis", "predictions", "actions in systems"].map((option) => (
            <label key={option} className="flex items-center space-x-2">
              <Checkbox checked={form.A4_1.includes(option)} onCheckedChange={() => toggleInArray("A4_1", option)} />
              <span className="text-sm">{option}</span>
            </label>
          ))}
        </div>
      </div>

      {/* A4.2 */}
      <div className="space-y-2">
        <Label>A4.2 Are outputs sent to external systems without human review?</Label>
        <div className="flex space-x-4">
          <label className="flex items-center space-x-2">
            <input type="radio" checked={form.A4_2 === "Yes"} onChange={() => update("A4_2", "Yes")} className="h-4 w-4 text-orange-600" />
            <span className="text-sm">Yes</span>
          </label>
          <label className="flex items-center space-x-2">
            <input type="radio" checked={form.A4_2 === "No"} onChange={() => update("A4_2", "No")} className="h-4 w-4 text-orange-600" />
            <span className="text-sm">No</span>
          </label>
        </div>
      </div>

      {/* A4.3 */}
      <div className="space-y-2">
        <Label>A4.3 What is the Business Impact Level (BIL) of the outputs?</Label>
        <select value={form.A4_3} onChange={(e) => update("A4_3", e.target.value)} className="w-full p-2 border rounded-md">
          <option value="">Select BIL</option>
          <option value="Official">Official</option>
          <option value="Official: Sensitive">Official: Sensitive</option>
          <option value="Protected">Protected</option>
          <option value="Highly Protected">Highly Protected</option>
          <option value="Secret">Secret</option>
          <option value="Top Secret">Top Secret</option>
        </select>
      </div>

      {/* A4.4 */}
      <div className="space-y-2">
        <Label>A4.4 How are AI outputs tracked and recorded? (Select all that apply)</Label>
        <div className="grid gap-2 md:grid-cols-2">
          {["stored in database", "logged in audit system", "logged in CRM/case system", "logged in activity logs", "not currently tracked (flag as risk)", "retention based on policy"].map((option) => (
            <label key={option} className="flex items-center space-x-2">
              <Checkbox checked={form.A4_4.includes(option)} onCheckedChange={() => toggleInArray("A4_4", option)} />
              <span className="text-sm">{option}</span>
            </label>
          ))}
        </div>
      </div>

      {/* A4.5 */}
      <div className="space-y-3">
        <Label>A4.5 Could any AI outputs allow unauthorised access to information?</Label>
        <div className="flex space-x-4">
          <label className="flex items-center space-x-2">
            <input type="radio" checked={form.A4_5 === "Yes"} onChange={() => update("A4_5", "Yes")} className="h-4 w-4 text-orange-600" />
            <span className="text-sm">Yes</span>
          </label>
          <label className="flex items-center space-x-2">
            <input type="radio" checked={form.A4_5 === "No"} onChange={() => update("A4_5", "No")} className="h-4 w-4 text-orange-600" />
            <span className="text-sm">No</span>
          </label>
        </div>
        {form.A4_5 === "Yes" && (
          <div className="ml-4 p-4 bg-gray-50 rounded-lg space-y-2">
            <Label>Select scenarios and mitigations (Select all that apply):</Label>
            <div className="grid gap-2 md:grid-cols-2">
              {["misrouted outputs", "excessive data exposure", "output reveals sensitive attributes", "outputs sent to incorrect system", "injection or poisoning risk"].map((option) => (
                <label key={option} className="flex items-center space-x-2">
                  <Checkbox checked={form.A4_5_scenarios.includes(option)} onCheckedChange={() => toggleInArray("A4_5_scenarios", option)} />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* A4.6 */}
      <div className="space-y-2">
        <Label>A4.6 Do outputs involve data regulated by law?</Label>
        <div className="flex space-x-4">
          <label className="flex items-center space-x-2">
            <input type="radio" checked={form.A4_6 === "Yes"} onChange={() => update("A4_6", "Yes")} className="h-4 w-4 text-orange-600" />
            <span className="text-sm">Yes</span>
          </label>
          <label className="flex items-center space-x-2">
            <input type="radio" checked={form.A4_6 === "No"} onChange={() => update("A4_6", "No")} className="h-4 w-4 text-orange-600" />
            <span className="text-sm">No</span>
          </label>
        </div>
        {form.A4_6 === "Yes" && (
          <div className="ml-4 p-4 bg-gray-50 rounded-lg space-y-2">
            <Label>Select data types (Select all that apply):</Label>
            <div className="grid gap-2 md:grid-cols-2">
              {["personal", "sensitive", "financial", "health", "child-related", "law enforcement", "Indigenous data", "confidential government data", "operationally sensitive data"].map((option) => (
                <label key={option} className="flex items-center space-x-2">
                  <Checkbox checked={form.A4_6_data_types.includes(option)} onCheckedChange={() => toggleInArray("A4_6_data_types", option)} />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* A4.7 - Gate Question */}
      <div className="space-y-2">
        <Label>A4.7 Do outputs contain personally identifiable information (PII)?</Label>
        <div className="flex space-x-4">
          <label className="flex items-center space-x-2">
            <input type="radio" name="A4_7" checked={form.A4_7 === "Yes"} onChange={() => update("A4_7", "Yes")} className="form-radio" />
            <span className="text-sm">Yes</span>
          </label>
          <label className="flex items-center space-x-2">
            <input type="radio" name="A4_7" checked={form.A4_7 === "No"} onChange={() => {
              update("A4_7", "No");
              update("A4_7_pii_types", []);
              update("A4_7_pii_types_other", "");
              update("A4_7_access_scope", "");
              update("A4_7_access_controls", []);
              update("A4_7_notes", "");
            }} className="form-radio" />
            <span className="text-sm">No</span>
          </label>
        </div>
      </div>

      {/* A4.7 Sub-questions */}
      {form.A4_7 === "Yes" && (
        <div className="ml-4 p-4 bg-gray-50 rounded-lg space-y-4">
          <div className="space-y-2">
            <Label>A4.7a PII categories included in outputs (select all that apply)</Label>
            <div className="grid gap-2 md:grid-cols-2">
              {["Name / identity attributes", "Contact details (email, phone, address)", "Government identifiers (licence, Medicare, TFN)", "Financial information", "Health information", "Biometrics", "Location / movement data", "Images / video of individuals", "Employment / workplace information", "Other"].map((option) => (
                <label key={option} className="flex items-center space-x-2">
                  <Checkbox checked={form.A4_7_pii_types.includes(option)} onCheckedChange={() => toggleInArray("A4_7_pii_types", option)} />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
            </div>
            {form.A4_7_pii_types.includes("Other") && (
              <Input value={form.A4_7_pii_types_other} onChange={(e) => update("A4_7_pii_types_other", e.target.value)} placeholder="Specify other PII categories" className="mt-2" />
            )}
          </div>

          <div className="space-y-2">
            <Label>A4.7b Who can access outputs containing PII?</Label>
            <div className="flex flex-col space-y-2">
              {["Internal users only", "Internal users + contractors / service providers", "External partner organisations", "Public-facing / broadly accessible", "Unknown / Not specified"].map((option) => (
                <label key={option} className="flex items-center space-x-2">
                  <input type="radio" name="A4_7_access_scope" checked={form.A4_7_access_scope === option} onChange={() => update("A4_7_access_scope", option)} className="form-radio" />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="space-y-2">
            <Label>A4.7c Controls limiting access to PII outputs (select all that apply)</Label>
            <div className="grid gap-2 md:grid-cols-2">
              {["Role-based access control (RBAC)", "Least privilege / need-to-know", "Strong authentication (e.g., MFA)", "Audit logging / access logs", "Encryption at rest", "Encryption in transit", "Data masking / redaction", "DLP / egress controls", "Time-bound access / approval workflow", "Not in place / unknown"].map((option) => (
                <label key={option} className="flex items-center space-x-2">
                  <Checkbox checked={form.A4_7_access_controls.includes(option)} onCheckedChange={() => toggleInArray("A4_7_access_controls", option)} />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="A4_7_notes">A4.7d Notes / exceptions (optional)</Label>
            <Textarea id="A4_7_notes" value={form.A4_7_notes} onChange={(e) => update("A4_7_notes", e.target.value)} placeholder="Add any additional notes or exceptions..." rows={2} />
          </div>
        </div>
      )}

      {/* A4.8 - Gate Question */}
      <div className="space-y-2">
        <Label>A4.8 Do any AI outputs directly trigger actions with legal or regulatory effect?</Label>
        <div className="flex space-x-4">
          <label className="flex items-center space-x-2">
            <input type="radio" name="A4_8" checked={form.A4_8 === "Yes"} onChange={() => update("A4_8", "Yes")} className="form-radio" />
            <span className="text-sm">Yes</span>
          </label>
          <label className="flex items-center space-x-2">
            <input type="radio" name="A4_8" checked={form.A4_8 === "No"} onChange={() => {
              update("A4_8", "No");
              update("A4_8_action_types", []);
              update("A4_8_action_types_other", "");
              update("A4_8_trigger_pathway", "");
              update("A4_8_affected_parties", []);
              update("A4_8_decision_records", []);
              update("A4_8_review_appeal", "");
              update("A4_8_legal_basis", []);
              update("A4_8_legal_basis_other", "");
              update("A4_8_notes", "");
            }} className="form-radio" />
            <span className="text-sm">No</span>
          </label>
        </div>
      </div>

      {/* A4.8 Sub-questions */}
      {form.A4_8 === "Yes" && (
        <div className="ml-4 p-4 bg-gray-50 rounded-lg space-y-4">
          <div className="space-y-2">
            <Label>A4.8a Types of legal/regulatory actions triggered (select all that apply)</Label>
            <div className="grid gap-2 md:grid-cols-2">
              {["Eligibility / access decisions", "Service entitlements / benefits decisions", "Compliance enforcement actions", "Penalties, sanctions, or fines", "Regulatory reporting / notification triggers", "Employment / workforce actions", "Contractual decisions (approve/decline/terminate)", "Safety-critical operational actions", "Other"].map((option) => (
                <label key={option} className="flex items-center space-x-2">
                  <Checkbox checked={form.A4_8_action_types.includes(option)} onCheckedChange={() => toggleInArray("A4_8_action_types", option)} />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
            </div>
            {form.A4_8_action_types.includes("Other") && (
              <Input value={form.A4_8_action_types_other} onChange={(e) => update("A4_8_action_types_other", e.target.value)} placeholder="Specify other action types" className="mt-2" />
            )}
          </div>

          <div className="space-y-2">
            <Label>A4.8b How are actions triggered from AI outputs?</Label>
            <div className="flex flex-col space-y-2">
              {["Automatically triggered (no human review)", "Automatically triggered after human approval", "Used as decision support (human makes final decision)", "Unknown / Not specified"].map((option) => (
                <label key={option} className="flex items-center space-x-2">
                  <input type="radio" name="A4_8_trigger_pathway" checked={form.A4_8_trigger_pathway === option} onChange={() => update("A4_8_trigger_pathway", option)} className="form-radio" />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="space-y-2">
            <Label>A4.8c Who may be affected by these actions? (select all that apply)</Label>
            <div className="grid gap-2 md:grid-cols-2">
              {["Individuals / citizens", "Employees / workers", "Customers / clients", "Businesses / organisations", "Regulated entities", "Vulnerable populations", "General public"].map((option) => (
                <label key={option} className="flex items-center space-x-2">
                  <Checkbox checked={form.A4_8_affected_parties.includes(option)} onCheckedChange={() => toggleInArray("A4_8_affected_parties", option)} />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="space-y-2">
            <Label>A4.8d Decision record / traceability mechanisms (select all that apply)</Label>
            <div className="grid gap-2 md:grid-cols-2">
              {["Audit logs of outputs and decisions", "Case/record identifiers linking decision to person/event", "Human approval record captured", "Reason codes / explanation recorded", "Data lineage / provenance tracking", "Not in place / unknown"].map((option) => (
                <label key={option} className="flex items-center space-x-2">
                  <Checkbox checked={form.A4_8_decision_records.includes(option)} onCheckedChange={() => toggleInArray("A4_8_decision_records", option)} />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="space-y-2">
            <Label>A4.8e Is there a review/appeal/contestability pathway for affected parties?</Label>
            <div className="flex flex-col space-y-2">
              {["Yes — documented and operational", "Partially — exists but not formalised", "No", "Unknown / Not specified"].map((option) => (
                <label key={option} className="flex items-center space-x-2">
                  <input type="radio" name="A4_8_review_appeal" checked={form.A4_8_review_appeal === option} onChange={() => update("A4_8_review_appeal", option)} className="form-radio" />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="space-y-2">
            <Label>A4.8f Legal / policy basis for actions (select all that apply)</Label>
            <div className="grid gap-2 md:grid-cols-2">
              {["Legislation / regulation explicitly authorising action", "Policy / procedure basis only", "Contractual terms", "Not defined / unclear", "Other"].map((option) => (
                <label key={option} className="flex items-center space-x-2">
                  <Checkbox checked={form.A4_8_legal_basis.includes(option)} onCheckedChange={() => toggleInArray("A4_8_legal_basis", option)} />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
            </div>
            {form.A4_8_legal_basis.includes("Other") && (
              <Input value={form.A4_8_legal_basis_other} onChange={(e) => update("A4_8_legal_basis_other", e.target.value)} placeholder="Specify other legal/policy basis" className="mt-2" />
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="A4_8_notes">A4.8g Notes / exceptions (optional)</Label>
            <Textarea id="A4_8_notes" value={form.A4_8_notes} onChange={(e) => update("A4_8_notes", e.target.value)} placeholder="Add any additional notes or exceptions..." rows={2} />
          </div>
        </div>
      )}
    </div>
  );
};

export default SectionA4;
