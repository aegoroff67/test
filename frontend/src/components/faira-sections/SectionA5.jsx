import React from 'react';
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Separator } from "@/components/ui/separator";
import EvidenceAttachLink from '../EvidenceAttachLink';

const SectionA5 = ({ form, update, toggleInArray, assessmentId, currentUser }) => {
  return (
    <div className="space-y-6 pt-6 border-t" id="A5_1">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-1">A5. Governance and Oversight</h3>
        <p className="text-sm text-gray-600">Maps to FAIRA Table 9 (Monitoring & evaluation) plus accountability references</p>
      </div>
      <Separator />
      
      {/* A5.1 */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <Label>A5.1 Who is accountable for decisions made using this system?</Label>
          {assessmentId && (
            <EvidenceAttachLink 
              questionCode="A5-1" 
              assessmentId={assessmentId} 
              currentUser={currentUser} 
            />
          )}
        </div>
        <select value={form.A5_1} onChange={(e) => update("A5_1", e.target.value)} className="w-full p-2 border rounded-md">
          <option value="">Select role</option>
          <option value="product owner">product owner</option>
          <option value="system owner">system owner</option>
          <option value="executive sponsor">executive sponsor</option>
          <option value="service manager">service manager</option>
          <option value="data custodian">data custodian</option>
          <option value="governance committee">governance committee</option>
          <option value="AI oversight board">AI oversight board</option>
        </select>
      </div>

      {/* A5.2 - Gated Section */}
      <div className="space-y-3">
        <Label>A5.2 Are AI inputs, outputs, and/or decisions logged or recorded?</Label>
        <div className="flex space-x-4">
          <label className="flex items-center space-x-2">
            <input type="radio" checked={form.A5_2 === "Yes"} onChange={() => update("A5_2", "Yes")} className="h-4 w-4 text-orange-600" />
            <span className="text-sm">Yes</span>
          </label>
          <label className="flex items-center space-x-2">
            <input type="radio" checked={form.A5_2 === "No"} onChange={() => update("A5_2", "No")} className="h-4 w-4 text-orange-600" />
            <span className="text-sm">No</span>
          </label>
        </div>

        {/* Conditional subsections when Yes is selected */}
        {form.A5_2 === "Yes" && (
          <div className="ml-4 p-4 bg-gray-100 rounded-lg space-y-4 border border-gray-200">
            {/* A5.2a - What is logged */}
            <div className="space-y-2">
              <Label className="text-sm font-medium">A5.2a What is logged or recorded? (select all that apply)</Label>
              <div className="grid gap-2 md:grid-cols-2">
                {[
                  "AI inputs",
                  "AI outputs",
                  "human decisions informed by AI",
                  "automated actions triggered by AI",
                  "model version / configuration",
                  "data sources used / provenance",
                  "access to outputs / disclosures"
                ].map((option) => (
                  <label key={option} className="flex items-center space-x-2">
                    <Checkbox 
                      checked={(form.A5_2_logged_items || []).includes(option)} 
                      onCheckedChange={() => toggleInArray("A5_2_logged_items", option)} 
                    />
                    <span className="text-sm">{option}</span>
                  </label>
                ))}
                <label className="flex items-center space-x-2">
                  <Checkbox 
                    checked={(form.A5_2_logged_items || []).includes("Other")} 
                    onCheckedChange={() => toggleInArray("A5_2_logged_items", "Other")} 
                  />
                  <span className="text-sm">Other (specify)</span>
                </label>
              </div>
              {(form.A5_2_logged_items || []).includes("Other") && (
                <Input
                  value={form.A5_2_logged_items_other || ''}
                  onChange={(e) => update("A5_2_logged_items_other", e.target.value)}
                  placeholder="Please specify other logged items"
                  className="mt-2"
                />
              )}
            </div>

            {/* A5.2b - Logging mechanisms */}
            <div className="space-y-2">
              <Label className="text-sm font-medium">A5.2b Logging / record-keeping mechanisms (select all that apply)</Label>
              <div className="grid gap-2 md:grid-cols-2">
                {[
                  "application / system logs",
                  "dedicated audit logs",
                  "workflow / case management records",
                  "database records",
                  "centralised logging / siem",
                  "manual records",
                  "not in place / unknown"
                ].map((option) => (
                  <label key={option} className="flex items-center space-x-2">
                    <Checkbox 
                      checked={(form.A5_2_logging_mechanisms || []).includes(option)} 
                      onCheckedChange={() => toggleInArray("A5_2_logging_mechanisms", option)} 
                    />
                    <span className="text-sm">{option}</span>
                  </label>
                ))}
                <label className="flex items-center space-x-2">
                  <Checkbox 
                    checked={(form.A5_2_logging_mechanisms || []).includes("Other")} 
                    onCheckedChange={() => toggleInArray("A5_2_logging_mechanisms", "Other")} 
                  />
                  <span className="text-sm">Other (specify)</span>
                </label>
              </div>
              {(form.A5_2_logging_mechanisms || []).includes("Other") && (
                <Input
                  value={form.A5_2_logging_mechanisms_other || ''}
                  onChange={(e) => update("A5_2_logging_mechanisms_other", e.target.value)}
                  placeholder="Please specify other logging mechanisms"
                  className="mt-2"
                />
              )}
            </div>

            {/* A5.2c - Retention period */}
            <div className="space-y-2">
              <Label className="text-sm font-medium">A5.2c Log/record retention period</Label>
              <select 
                value={form.A5_2_retention || ''} 
                onChange={(e) => update("A5_2_retention", e.target.value)} 
                className="w-full p-2 border rounded-md bg-white"
              >
                <option value="">Select retention period</option>
                <option value="less than 30 days">less than 30 days</option>
                <option value="30–90 days">30–90 days</option>
                <option value="3–12 months">3–12 months</option>
                <option value="more than 12 months">more than 12 months</option>
                <option value="unknown / not defined">unknown / not defined</option>
              </select>
            </div>

            {/* A5.2d - Access scope */}
            <div className="space-y-2">
              <Label className="text-sm font-medium">A5.2d Who can access logs/records?</Label>
              <select 
                value={form.A5_2_access_scope || ''} 
                onChange={(e) => update("A5_2_access_scope", e.target.value)} 
                className="w-full p-2 border rounded-md bg-white"
              >
                <option value="">Select access scope</option>
                <option value="restricted operational staff only">restricted operational staff only</option>
                <option value="security / risk / audit teams">security / risk / audit teams</option>
                <option value="system administrators">system administrators</option>
                <option value="external auditors / regulators">external auditors / regulators</option>
                <option value="broad internal access">broad internal access</option>
                <option value="unknown / not defined">unknown / not defined</option>
              </select>
            </div>

            {/* A5.2e - Notes */}
            <div className="space-y-2">
              <Label className="text-sm font-medium">A5.2e Notes / exceptions (optional)</Label>
              <Textarea
                value={form.A5_2_notes || ''}
                onChange={(e) => update("A5_2_notes", e.target.value)}
                placeholder="Any additional notes or exceptions"
                rows={2}
              />
            </div>
          </div>
        )}
      </div>

      {/* A5.3 */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <Label>A5.3 What monitoring and evaluation processes are in place? (Select all that apply)</Label>
          {assessmentId && (
            <EvidenceAttachLink 
              questionCode="A5-3" 
              assessmentId={assessmentId} 
              currentUser={currentUser} 
            />
          )}
        </div>
        <div className="grid gap-2 md:grid-cols-2">
          {["regular system audits", "continuous performance monitoring", "user feedback collection", "periodic stakeholder reviews"].map((option) => (
            <label key={option} className="flex items-center space-x-2">
              <Checkbox checked={form.A5_3.includes(option)} onCheckedChange={() => toggleInArray("A5_3", option)} />
              <span className="text-sm">{option}</span>
            </label>
          ))}
        </div>
      </div>

      {/* A5.4 */}
      <div className="space-y-2">
        <Label>A5.4 How frequently will monitoring and evaluation occur?</Label>
        <select value={form.A5_4} onChange={(e) => update("A5_4", e.target.value)} className="w-full p-2 border rounded-md">
          <option value="">Select frequency</option>
          <option value="weekly">weekly</option>
          <option value="monthly">monthly</option>
          <option value="quarterly">quarterly</option>
          <option value="annually">annually</option>
          <option value="event-driven">event-driven</option>
        </select>
      </div>

      {/* A5.5 */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <Label>A5.5 Has the AI solution been subject to independent review?</Label>
          {assessmentId && form.A5_5 === "Yes" && (
            <EvidenceAttachLink 
              questionCode="A5-5" 
              assessmentId={assessmentId} 
              currentUser={currentUser} 
            />
          )}
        </div>
        <div className="flex space-x-4">
          <label className="flex items-center space-x-2">
            <input type="radio" checked={form.A5_5 === "Yes"} onChange={() => update("A5_5", "Yes")} className="h-4 w-4 text-orange-600" />
            <span className="text-sm">Yes</span>
          </label>
          <label className="flex items-center space-x-2">
            <input type="radio" checked={form.A5_5 === "No"} onChange={() => update("A5_5", "No")} className="h-4 w-4 text-orange-600" />
            <span className="text-sm">No</span>
          </label>
        </div>
      </div>

      {/* A5.6 */}
      <div className="space-y-2">
        <Label>A5.6 Who is responsible for monitoring and evaluation?</Label>
        <select value={form.A5_6} onChange={(e) => update("A5_6", e.target.value)} className="w-full p-2 border rounded-md">
          <option value="">Select role</option>
          <option value="ICT operations">ICT operations</option>
          <option value="data science team">data science team</option>
          <option value="risk/compliance">risk/compliance</option>
          <option value="business owner">business owner</option>
          <option value="vendor">vendor</option>
          <option value="customer-facing staff">customer-facing staff</option>
          <option value="external auditor">external auditor</option>
        </select>
      </div>

      {/* A5.7 */}
      <div className="space-y-2">
        <Label>A5.7 How are stakeholders engaged in monitoring and evaluation? (Select all that apply)</Label>
        <div className="grid gap-2 md:grid-cols-2">
          {["workshops", "public consultation", "union consultation", "focus groups", "user feedback sessions", "accessibility reviews", "no engagements planned (flag as risk)"].map((option) => (
            <label key={option} className="flex items-center space-x-2">
              <Checkbox checked={form.A5_7.includes(option)} onCheckedChange={() => toggleInArray("A5_7", option)} />
              <span className="text-sm">{option}</span>
            </label>
          ))}
        </div>
      </div>

      {/* A5.8 */}
      <div className="space-y-2">
        <Label>A5.8 How are undesirable or harmful results detected? (Select all that apply)</Label>
        <div className="grid gap-2 md:grid-cols-2">
          {["alerting and monitoring", "user complaints", "human review triggers", "automated anomaly detection", "escalation procedures", "incident response team", "no defined contingencies (flag as risk)"].map((option) => (
            <label key={option} className="flex items-center space-x-2">
              <Checkbox checked={form.A5_8.includes(option)} onCheckedChange={() => toggleInArray("A5_8", option)} />
              <span className="text-sm">{option}</span>
            </label>
          ))}
        </div>
      </div>

      {/* A5.9 */}
      <div className="space-y-2">
        <Label>A5.9 Which values and principles informed the AI solution&apos;s design? (Select all that apply)</Label>
        <div className="grid gap-2 md:grid-cols-2">
          {["Australia's AI Ethics Principles", "Human Rights Act", "data governance policies", "WHS", "accessibility standards", "agency ethics statements", "privacy principles", "risk management framework"].map((option) => (
            <label key={option} className="flex items-center space-x-2">
              <Checkbox checked={form.A5_9.includes(option)} onCheckedChange={() => toggleInArray("A5_9", option)} />
              <span className="text-sm">{option}</span>
            </label>
          ))}
        </div>
      </div>

      {/* A5.10 */}
      <div className="space-y-3" id="A5_10">
        <div className="flex items-center justify-between">
          <Label>A5.10 Are there sector-specific frameworks, laws, or regulatory obligations that apply to this AI solution?</Label>
          {assessmentId && (
            <EvidenceAttachLink 
              questionCode="A5-10" 
              assessmentId={assessmentId} 
              currentUser={currentUser} 
            />
          )}
        </div>
        <div className="flex space-x-4">
          <label className="flex items-center space-x-2">
            <input type="radio" checked={form.A5_10 === "Yes"} onChange={() => update("A5_10", "Yes")} className="h-4 w-4 text-orange-600" />
            <span className="text-sm">Yes</span>
          </label>
          <label className="flex items-center space-x-2">
            <input type="radio" checked={form.A5_10 === "No"} onChange={() => update("A5_10", "No")} className="h-4 w-4 text-orange-600" />
            <span className="text-sm">No</span>
          </label>
        </div>
        
        {form.A5_10 === "Yes" && (
          <div className="ml-4 p-4 bg-gray-50 rounded-lg space-y-4">
            {/* Commonwealth Legislation */}
            <div className="space-y-2">
              <h4 className="font-semibold text-sm text-gray-900">Commonwealth (Federal) Legislation</h4>
              <div className="grid gap-2 md:grid-cols-2">
                {["Privacy Act 1988", "Australian Privacy Principles (APPs)", "Notifiable Data Breaches (NDB) Scheme", "Archives Act 1983", "Freedom of Information Act 1982", "Security of Critical Infrastructure Act (SOCI)", "Criminal Code Act (cybercrime, identity, child exploitation provisions)"].map((option) => (
                  <label key={option} className="flex items-center space-x-2">
                    <Checkbox checked={form.A5_10_commonwealth.includes(option)} onCheckedChange={() => toggleInArray("A5_10_commonwealth", option)} />
                    <span className="text-sm">{option}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Queensland State Legislation */}
            <div className="space-y-2">
              <h4 className="font-semibold text-sm text-gray-900">Queensland State Legislation</h4>
              <div className="grid gap-2 md:grid-cols-2">
                {["Information Privacy Act 2009 (Qld)", "Right to Information Act 2009", "Public Records Act 2002", "Child Protection Act", "Domestic and Family Violence Protection Act", "Youth Justice Act", "Mental Health Act", "Hospital and Health Boards Act (confidentiality obligations)", "Police Powers and Responsibilities Act"].map((option) => (
                  <label key={option} className="flex items-center space-x-2">
                    <Checkbox checked={form.A5_10_qld.includes(option)} onCheckedChange={() => toggleInArray("A5_10_qld", option)} />
                    <span className="text-sm">{option}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Sector-Specific */}
            <div className="space-y-2">
              <h4 className="font-semibold text-sm text-gray-900">Sector-Specific Regulatory Obligations</h4>
              <p className="text-xs text-gray-600">(Select any that apply to the domain of the AI solution)</p>
              <div className="grid gap-2 md:grid-cols-2">
                {["health information / clinical safety requirements", "law enforcement / justice sector requirements", "education sector obligations", "transport or safety-critical operational standards", "financial or taxation regulatory requirements", "Indigenous cultural data governance / data sovereignty", "workplace surveillance obligations", "safety-of-life or emergency services obligations", "critical infrastructure operational safety requirements"].map((option) => (
                  <label key={option} className="flex items-center space-x-2">
                    <Checkbox checked={form.A5_10_sector.includes(option)} onCheckedChange={() => toggleInArray("A5_10_sector", option)} />
                    <span className="text-sm">{option}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Frameworks */}
            <div className="space-y-2">
              <h4 className="font-semibold text-sm text-gray-900">Applicable Frameworks, Standards, and Policies</h4>
              <div className="grid gap-2 md:grid-cols-2">
                {["QGEA / IS18:2018 Information Security Policy", "QLD Government AI Ethical Principles", "QLD FAIRA Framework (this assessment)", "Australian Government AI Ethics Principles", "ISO/IEC 42001 (AI Management System)", "ISO/IEC 27001 / 27002 (Information Security Management)", "ISO/IEC 27701 (Privacy Information Management)", "ISO 31000 (Risk Management)", "NIST AI Risk Management Framework", "Other standards or frameworks (specify below)"].map((option) => (
                  <label key={option} className="flex items-center space-x-2">
                    <Checkbox checked={form.A5_10_frameworks.includes(option)} onCheckedChange={() => toggleInArray("A5_10_frameworks", option)} />
                    <span className="text-sm">{option}</span>
                  </label>
                ))}
              </div>
              {form.A5_10_frameworks.includes("Other standards or frameworks (specify below)") && (
                <div className="mt-2">
                  <Input id="A5_10_frameworks_other" value={form.A5_10_frameworks_other} onChange={(e) => update("A5_10_frameworks_other", e.target.value)} placeholder="Specify other standards or frameworks" />
                </div>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="A5_10_other">Other regulations, obligations, or frameworks (optional):</Label>
              <Textarea id="A5_10_other" value={form.A5_10_other} onChange={(e) => update("A5_10_other", e.target.value)} placeholder="Specify any other regulations, obligations, or frameworks" rows={2} />
            </div>

            <div className="space-y-2">
              <Label htmlFor="A5_10_impact">If Yes, briefly describe how these obligations impact the AI system (optional):</Label>
              <Textarea id="A5_10_impact" value={form.A5_10_impact} onChange={(e) => update("A5_10_impact", e.target.value)} placeholder="Describe the impact of these regulatory obligations" rows={3} />
            </div>
          </div>
        )}
      </div>

      {/* A5.11 */}
      <div className="space-y-2">
        <Label>A5.11 Where will this AI solution be deployed?</Label>
        <select value={form.A5_11} onChange={(e) => update("A5_11", e.target.value)} className="w-full p-2 border rounded-md">
          <option value="">Select deployment location</option>
          <option value="internal use only">internal use only</option>
          <option value="internal + selected partners">internal + selected partners</option>
          <option value="public-facing">public-facing</option>
          <option value="citizen-facing high-sensitivity">citizen-facing high-sensitivity</option>
          <option value="embedded in another product">embedded in another product</option>
          <option value="multi-channel deployment">multi-channel deployment</option>
        </select>
      </div>

      {/* A5.12 */}
      <div className="space-y-2">
        <Label>A5.12 Which national and international AI frameworks and standards apply? (Select all that apply)</Label>
        <div className="grid gap-2 md:grid-cols-2">
          {["National Framework for the Assurance of AI in Government", "Queensland Government Enterprise Architecture", "ISO/IEC 42001", "ISO 27001", "ISO 31000", "NIST AI RMF", "OECD AI Principles", "EU AI Act", "Singapore MAF"].map((option) => (
            <label key={option} className="flex items-center space-x-2">
              <Checkbox checked={form.A5_12.includes(option)} onCheckedChange={() => toggleInArray("A5_12", option)} />
              <span className="text-sm">{option}</span>
            </label>
          ))}
          <label className="flex items-center space-x-2">
            <Checkbox checked={form.A5_12.includes("Other")} onCheckedChange={() => toggleInArray("A5_12", "Other")} />
            <span className="text-sm">Other (specify)</span>
          </label>
        </div>
        {form.A5_12.includes("Other") && (
          <Input value={form.A5_12_other} onChange={(e) => update("A5_12_other", e.target.value)} placeholder="Please specify other frameworks" className="mt-2" />
        )}
      </div>
    </div>
  );
};

export default SectionA5;
