import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Checkbox } from "@/components/ui/checkbox";
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import { FileCheck2, Info } from 'lucide-react';

/**
 * FAIRA Onboarding Panel
 * Displays additional information fields required by FAIRA when selected
 */
export default function FairaOnboardingPanel({ fairaData, updateFaira, toggleFairaArray }) {
  // Helper to check if a multiselect includes a value
  const includesValue = (fieldId, value) => {
    return (fairaData[fieldId] || []).includes(value);
  };

  return (
    <Card className="border-2 border-amber-200 bg-amber-50/30">
      <CardHeader className="bg-amber-50 border-b border-amber-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <FileCheck2 className="h-5 w-5 text-amber-600" />
            <CardTitle className="text-xl">FAIRA Components – Additional Information</CardTitle>
          </div>
          <Badge variant="outline" className="bg-amber-100 text-amber-800 border-amber-300">
            FAIRA Required
          </Badge>
        </div>
        <p className="text-sm text-gray-600 mt-2">
          These questions collect the information required under FAIRA Part A (Components Analysis) and specific context items that support Parts B and C. These fields are descriptive only and do not contribute to the maturity score.
        </p>
      </CardHeader>

      <CardContent className="space-y-8 mt-6">
        {/* A1 – AI Solution Overview */}
        <div className="space-y-4">
          <div className="flex items-center space-x-2 pb-2 border-b border-amber-200">
            <h3 className="text-lg font-semibold text-amber-900">A1 – AI Solution Overview</h3>
          </div>

          {/* FA-ON-01 */}
          <div className="space-y-2">
            <Label className="flex items-center gap-2">
              What types of decisions does the AI system influence or automate?
              <span className="text-xs text-gray-500">(Select all that apply)</span>
            </Label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 pl-4">
              {[
                "Administrative processing / routing",
                "Service eligibility / access decisions",
                "Enforcement / compliance / penalties",
                "Resource allocation / prioritisation",
                "Advisory recommendations only (human decides)",
                "Operational control (e.g., scheduling, infrastructure)",
                "Other"
              ].map((option) => (
                <label key={option} className="inline-flex items-center gap-2">
                  <Checkbox 
                    checked={includesValue("FA-ON-01", option)} 
                    onCheckedChange={() => toggleFairaArray("FA-ON-01", option)} 
                  />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
            </div>
            {includesValue("FA-ON-01", "Other") && (
              <div className="mt-2 pl-4">
                <Input
                  placeholder="Describe other decision types"
                  value={fairaData["FA-ON-01-OTHER"] || ""}
                  onChange={(e) => updateFaira("FA-ON-01-OTHER", e.target.value)}
                />
              </div>
            )}
            <p className="text-xs text-gray-500 pl-4">
              <Info className="inline h-3 w-3 mr-1" />
              FAIRA requires clarity on the types of decisions affected by the AI system to determine risk exposure and assurance obligations.
            </p>
          </div>

          <Separator className="my-4" />

          {/* FA-ON-02 */}
          <div className="space-y-2">
            <Label>What is the level of automation?</Label>
            <Select value={fairaData["FA-ON-02"] || ""} onValueChange={(v) => updateFaira("FA-ON-02", v)}>
              <SelectTrigger>
                <SelectValue placeholder="Select automation level" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="AI suggests, human always decides">AI suggests, human always decides</SelectItem>
                <SelectItem value="AI decides, human reviews each decision">AI decides, human reviews each decision</SelectItem>
                <SelectItem value="AI decides, human reviews exceptions only">AI decides, human reviews exceptions only</SelectItem>
                <SelectItem value="Fully automated, no routine human review">Fully automated, no routine human review</SelectItem>
              </SelectContent>
            </Select>
            <p className="text-xs text-gray-500">
              <Info className="inline h-3 w-3 mr-1" />
              Higher automation levels typically require stronger oversight, contestability, and monitoring under FAIRA.
            </p>
          </div>
        </div>

        {/* A2 – Human–Machine Interaction */}
        <div className="space-y-4">
          <div className="flex items-center space-x-2 pb-2 border-b border-amber-200">
            <h3 className="text-lg font-semibold text-amber-900">A2 – Human–Machine Interaction</h3>
          </div>

          {/* FA-ON-03 */}
          <div className="space-y-2">
            <Label className="flex items-center gap-2">
              How do users interact with the AI system?
              <span className="text-xs text-gray-500">(Select all that apply)</span>
            </Label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 pl-4">
              {[
                "Web portal / website",
                "Mobile app",
                "Chatbot / virtual assistant",
                "Email / messaging integration",
                "Internal line-of-business system",
                "API only / system-to-system",
                "Other"
              ].map((option) => (
                <label key={option} className="inline-flex items-center gap-2">
                  <Checkbox 
                    checked={includesValue("FA-ON-03", option)} 
                    onCheckedChange={() => toggleFairaArray("FA-ON-03", option)} 
                  />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
            </div>
            {includesValue("FA-ON-03", "Other") && (
              <div className="mt-2 pl-4">
                <Input
                  placeholder="Describe other interaction channels"
                  value={fairaData["FA-ON-03-OTHER"] || ""}
                  onChange={(e) => updateFaira("FA-ON-03-OTHER", e.target.value)}
                />
              </div>
            )}
            <p className="text-xs text-gray-500 pl-4">
              <Info className="inline h-3 w-3 mr-1" />
              Helps determine user experience, interface-related risks, and communication clarity.
            </p>
          </div>

          <Separator className="my-4" />

          {/* FA-ON-04 */}
          <div className="space-y-2">
            <Label>Can a human override or reverse AI decisions?</Label>
            <Select value={fairaData["FA-ON-04"] || ""} onValueChange={(v) => updateFaira("FA-ON-04", v)}>
              <SelectTrigger>
                <SelectValue placeholder="Select override capability" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="Yes – always, via standard process">Yes – always, via standard process</SelectItem>
                <SelectItem value="Yes – for certain decision types only">Yes – for certain decision types only</SelectItem>
                <SelectItem value="Only via escalation / special approval">Only via escalation / special approval</SelectItem>
                <SelectItem value="No explicit override mechanism">No explicit override mechanism</SelectItem>
              </SelectContent>
            </Select>
            <p className="text-xs text-gray-500">
              <Info className="inline h-3 w-3 mr-1" />
              FAIRA expects decisions influenced by AI to remain reversible, accountable, and contestable.
            </p>
          </div>
        </div>

        {/* A3 – Input Data */}
        <div className="space-y-4">
          <div className="flex items-center space-x-2 pb-2 border-b border-amber-200">
            <h3 className="text-lg font-semibold text-amber-900">A3 – Input Data</h3>
          </div>

          {/* FA-ON-05 */}
          <div className="space-y-2">
            <Label className="flex items-center gap-2">
              What types of input data does the AI system use?
              <span className="text-xs text-gray-500">(Select all that apply)</span>
            </Label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 pl-4">
              {[
                "Personal information",
                "Sensitive information (e.g., health, biometrics)",
                "Behavioural / usage data",
                "Transactional / operational data",
                "Open / public datasets",
                "Third-party / commercial datasets",
                "Synthetic data",
                "Sensor / telemetry data",
                "Other"
              ].map((option) => (
                <label key={option} className="inline-flex items-center gap-2">
                  <Checkbox 
                    checked={includesValue("FA-ON-05", option)} 
                    onCheckedChange={() => toggleFairaArray("FA-ON-05", option)} 
                  />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
            </div>
            {includesValue("FA-ON-05", "Other") && (
              <div className="mt-2 pl-4">
                <Input
                  placeholder="Describe other input data types"
                  value={fairaData["FA-ON-05-OTHER"] || ""}
                  onChange={(e) => updateFaira("FA-ON-05-OTHER", e.target.value)}
                />
              </div>
            )}
            <p className="text-xs text-gray-500 pl-4">
              <Info className="inline h-3 w-3 mr-1" />
              Supports FAIRA&apos;s expectations around data provenance, fairness, sensitivity, and potential bias.
            </p>
          </div>

          <Separator className="my-4" />

          {/* FA-ON-06 */}
          <div className="space-y-2">
            <Label className="flex items-center gap-2">
              Which categories best describe your data sources?
              <span className="text-xs text-gray-500">(Select all that apply)</span>
            </Label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 pl-4">
              {[
                "Internal agency / council systems",
                "Other government agencies",
                "Publicly available data",
                "Vendor-provided datasets",
                "Data collected directly from users",
                "Other"
              ].map((option) => (
                <label key={option} className="inline-flex items-center gap-2">
                  <Checkbox 
                    checked={includesValue("FA-ON-06", option)} 
                    onCheckedChange={() => toggleFairaArray("FA-ON-06", option)} 
                  />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
            </div>
            {includesValue("FA-ON-06", "Other") && (
              <div className="mt-2 pl-4">
                <Input
                  placeholder="Describe other data source categories"
                  value={fairaData["FA-ON-06-OTHER"] || ""}
                  onChange={(e) => updateFaira("FA-ON-06-OTHER", e.target.value)}
                />
              </div>
            )}
            <p className="text-xs text-gray-500 pl-4">
              <Info className="inline h-3 w-3 mr-1" />
              FAIRA requires explicit documentation of data sources.
            </p>
          </div>

          <Separator className="my-4" />

          {/* FA-ON-07 */}
          <div className="space-y-2">
            <Label>Have known data limitations (bias, gaps, quality issues) been documented?</Label>
            <Select value={fairaData["FA-ON-07"] || ""} onValueChange={(v) => updateFaira("FA-ON-07", v)}>
              <SelectTrigger>
                <SelectValue placeholder="Select documentation status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="Yes – comprehensively documented">Yes – comprehensively documented</SelectItem>
                <SelectItem value="Partially documented">Partially documented</SelectItem>
                <SelectItem value="Known informally but not documented">Known informally but not documented</SelectItem>
                <SelectItem value="No known limitations documented">No known limitations documented</SelectItem>
              </SelectContent>
            </Select>
            <p className="text-xs text-gray-500">
              <Info className="inline h-3 w-3 mr-1" />
              FAIRA mandates documenting known limitations to support fairness and reliability reviews.
            </p>
          </div>
        </div>

        {/* A4 – Output Characteristics */}
        <div className="space-y-4">
          <div className="flex items-center space-x-2 pb-2 border-b border-amber-200">
            <h3 className="text-lg font-semibold text-amber-900">A4 – Output Characteristics</h3>
          </div>

          {/* FA-ON-08 */}
          <div className="space-y-2">
            <Label className="flex items-center gap-2">
              What types of outputs does the AI system produce?
              <span className="text-xs text-gray-500">(Select all that apply)</span>
            </Label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 pl-4">
              {[
                "Scores / probabilities",
                "Categories / labels",
                "Binary decisions (approve/deny)",
                "Rankings / prioritised lists",
                "Advisory recommendations / summaries",
                "Generated content (e.g., text, reports)",
                "Control signals / actions",
                "Other"
              ].map((option) => (
                <label key={option} className="inline-flex items-center gap-2">
                  <Checkbox 
                    checked={includesValue("FA-ON-08", option)} 
                    onCheckedChange={() => toggleFairaArray("FA-ON-08", option)} 
                  />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
            </div>
            {includesValue("FA-ON-08", "Other") && (
              <div className="mt-2 pl-4">
                <Input
                  placeholder="Describe other output types"
                  value={fairaData["FA-ON-08-OTHER"] || ""}
                  onChange={(e) => updateFaira("FA-ON-08-OTHER", e.target.value)}
                />
              </div>
            )}
            <p className="text-xs text-gray-500 pl-4">
              <Info className="inline h-3 w-3 mr-1" />
              Output formats determine risk exposure, interpretability needs, and downstream impacts.
            </p>
          </div>

          <Separator className="my-4" />

          {/* FA-ON-09 */}
          <div className="space-y-2">
            <Label className="flex items-center gap-2">
              How are AI outputs used in practice?
              <span className="text-xs text-gray-500">(Select all that apply)</span>
            </Label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 pl-4">
              {[
                "Used as final decisions",
                "Used as input to human decision-making",
                "Used as advisory information only",
                "Used to trigger workflow / routing",
                "Used to trigger alerts or monitoring actions"
              ].map((option) => (
                <label key={option} className="inline-flex items-center gap-2">
                  <Checkbox 
                    checked={includesValue("FA-ON-09", option)} 
                    onCheckedChange={() => toggleFairaArray("FA-ON-09", option)} 
                  />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
            </div>
            <p className="text-xs text-gray-500 pl-4">
              <Info className="inline h-3 w-3 mr-1" />
              FAIRA requires clarity about operational roles of AI outputs.
            </p>
          </div>

          <Separator className="my-4" />

          {/* FA-ON-10 */}
          <div className="space-y-2">
            <Label>Are there documented rules for when outputs must NOT be used?</Label>
            <Select value={fairaData["FA-ON-10"] || ""} onValueChange={(v) => updateFaira("FA-ON-10", v)}>
              <SelectTrigger>
                <SelectValue placeholder="Select constraint documentation status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="Yes – clear &apos;do not use for…&apos; rules documented">Yes – clear &apos;do not use for…&apos; rules documented</SelectItem>
                <SelectItem value="Some constraints documented">Some constraints documented</SelectItem>
                <SelectItem value="Not formally documented">Not formally documented</SelectItem>
                <SelectItem value="No specific usage constraints">No specific usage constraints</SelectItem>
              </SelectContent>
            </Select>
            <p className="text-xs text-gray-500">
              <Info className="inline h-3 w-3 mr-1" />
              Constraints help prevent misuse or misinterpretation of AI outputs.
            </p>
          </div>
        </div>

        {/* A5 – Object of AI Action */}
        <div className="space-y-4">
          <div className="flex items-center space-x-2 pb-2 border-b border-amber-200">
            <h3 className="text-lg font-semibold text-amber-900">A5 – Object of AI Action</h3>
          </div>

          {/* FA-ON-11 */}
          <div className="space-y-2">
            <Label className="flex items-center gap-2">
              Who or what is directly affected by this AI system?
              <span className="text-xs text-gray-500">(Select all that apply)</span>
            </Label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 pl-4">
              {[
                "Individual members of the public",
                "Specific communities / demographics",
                "Businesses / organisations",
                "Internal staff / teams",
                "Physical assets / infrastructure",
                "Environment or public spaces",
                "Other"
              ].map((option) => (
                <label key={option} className="inline-flex items-center gap-2">
                  <Checkbox 
                    checked={includesValue("FA-ON-11", option)} 
                    onCheckedChange={() => toggleFairaArray("FA-ON-11", option)} 
                  />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
            </div>
            {includesValue("FA-ON-11", "Other") && (
              <div className="mt-2 pl-4">
                <Input
                  placeholder="Describe other affected parties"
                  value={fairaData["FA-ON-11-OTHER"] || ""}
                  onChange={(e) => updateFaira("FA-ON-11-OTHER", e.target.value)}
                />
              </div>
            )}
            <p className="text-xs text-gray-500 pl-4">
              <Info className="inline h-3 w-3 mr-1" />
              Used to identify human rights impacts, fairness considerations, and harm pathways.
            </p>
          </div>

          <Separator className="my-4" />

          {/* FA-ON-12 */}
          <div className="space-y-2">
            <Label className="flex items-center gap-2">
              Does the system impact any of the following?
              <span className="text-xs text-gray-500">(Select all that apply)</span>
            </Label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 pl-4">
              {[
                "Access to essential services",
                "Legal rights or obligations",
                "Safety or wellbeing",
                "Financial outcomes",
                "Reputation or social standing",
                "None of the above"
              ].map((option) => (
                <label key={option} className="inline-flex items-center gap-2">
                  <Checkbox 
                    checked={includesValue("FA-ON-12", option)} 
                    onCheckedChange={() => toggleFairaArray("FA-ON-12", option)} 
                  />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
            </div>
            <p className="text-xs text-gray-500 pl-4">
              <Info className="inline h-3 w-3 mr-1" />
              FAIRA emphasises identifying potential harms and critical impacts.
            </p>
          </div>
        </div>

        {/* A7 – Sector & Context */}
        <div className="space-y-4">
          <div className="flex items-center space-x-2 pb-2 border-b border-amber-200">
            <h3 className="text-lg font-semibold text-amber-900">A7 – Sector & Context</h3>
          </div>

          {/* FA-ON-13 */}
          <div className="space-y-2">
            <Label className="flex items-center gap-2">
              Which contextual factors increase the sensitivity or risk of this deployment?
              <span className="text-xs text-gray-500">(Select all that apply)</span>
            </Label>
            <div className="grid grid-cols-1 gap-2 pl-4">
              {[
                "Impacts vulnerable or marginalised groups",
                "High public visibility / media sensitivity",
                "Complex or uncertain legal environment",
                "High dependence on third-party data or models",
                "Rapidly changing policy or regulatory context",
                "None of the above"
              ].map((option) => (
                <label key={option} className="inline-flex items-center gap-2">
                  <Checkbox 
                    checked={includesValue("FA-ON-13", option)} 
                    onCheckedChange={() => toggleFairaArray("FA-ON-13", option)} 
                  />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
            </div>
            <p className="text-xs text-gray-500 pl-4">
              <Info className="inline h-3 w-3 mr-1" />
              Supports FAIRA&apos;s requirement to analyse environmental and contextual risks.
            </p>
          </div>

          <Separator className="my-4" />

          {/* FA-ON-14 */}
          <div className="space-y-2">
            <Label>Describe any sector-specific or context-specific risks relevant to this AI system.</Label>
            <Textarea
              placeholder="Provide details about localised risks, regulatory constraints, community sensitivity or safety-critical contexts..."
              value={fairaData["FA-ON-14"] || ""}
              onChange={(e) => updateFaira("FA-ON-14", e.target.value)}
              rows={4}
            />
            <p className="text-xs text-gray-500">
              <Info className="inline h-3 w-3 mr-1" />
              Provide details about localised risks, regulatory constraints, community sensitivity or safety-critical contexts.
            </p>
          </div>
        </div>

        {/* A8 – Broader Governance */}
        <div className="space-y-4">
          <div className="flex items-center space-x-2 pb-2 border-b border-amber-200">
            <h3 className="text-lg font-semibold text-amber-900">A8 – Broader Governance</h3>
          </div>

          {/* FA-ON-15 */}
          <div className="space-y-2">
            <Label className="flex items-center gap-2">
              Which internal policies or governance frameworks apply to this system?
              <span className="text-xs text-gray-500">(Select all that apply)</span>
            </Label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 pl-4">
              {[
                "Information security policy",
                "Data governance policy",
                "Privacy policy",
                "Risk management framework",
                "Records management policy",
                "AI / algorithmic governance policy",
                "Other"
              ].map((option) => (
                <label key={option} className="inline-flex items-center gap-2">
                  <Checkbox 
                    checked={includesValue("FA-ON-15", option)} 
                    onCheckedChange={() => toggleFairaArray("FA-ON-15", option)} 
                  />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
            </div>
            {includesValue("FA-ON-15", "Other") && (
              <div className="mt-2 pl-4">
                <Input
                  placeholder="Describe other relevant policies"
                  value={fairaData["FA-ON-15-OTHER"] || ""}
                  onChange={(e) => updateFaira("FA-ON-15-OTHER", e.target.value)}
                />
              </div>
            )}
            <p className="text-xs text-gray-500 pl-4">
              <Info className="inline h-3 w-3 mr-1" />
              FAIRA expects systems to operate within broader organisational governance structures.
            </p>
          </div>

          <Separator className="my-4" />

          {/* FA-ON-16 */}
          <div className="space-y-2">
            <Label>Is this AI system part of a broader program or strategy?</Label>
            <Select value={fairaData["FA-ON-16"] || ""} onValueChange={(v) => updateFaira("FA-ON-16", v)}>
              <SelectTrigger>
                <SelectValue placeholder="Select program alignment" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="Yes – part of a named program/strategy">Yes – part of a named program/strategy</SelectItem>
                <SelectItem value="Yes – informally linked to broader initiatives">Yes – informally linked to broader initiatives</SelectItem>
                <SelectItem value="No – standalone">No – standalone</SelectItem>
              </SelectContent>
            </Select>
            <p className="text-xs text-gray-500">
              <Info className="inline h-3 w-3 mr-1" />
              Understanding organisational alignment supports FAIRA&apos;s governance expectations.
            </p>
            {fairaData["FA-ON-16"] === "Yes – part of a named program/strategy" && (
              <div className="mt-2">
                <Label className="text-sm">Name the program or strategy</Label>
                <Input
                  placeholder="Enter program or strategy name"
                  value={fairaData["FA-ON-16A"] || ""}
                  onChange={(e) => updateFaira("FA-ON-16A", e.target.value)}
                  className="mt-1"
                />
              </div>
            )}
          </div>
        </div>

        {/* A9 – Monitoring & Evaluation */}
        <div className="space-y-4">
          <div className="flex items-center space-x-2 pb-2 border-b border-amber-200">
            <h3 className="text-lg font-semibold text-amber-900">A9 – Monitoring & Evaluation</h3>
          </div>

          {/* FA-ON-17 */}
          <div className="space-y-2">
            <Label className="flex items-center gap-2">
              Who is responsible for monitoring the AI system&apos;s performance and impacts?
              <span className="text-xs text-gray-500">(Select all that apply)</span>
            </Label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 pl-4">
              {[
                "Business owner / service area",
                "Central data / analytics team",
                "ICT / technology operations",
                "Risk / compliance team",
                "Vendor / external provider",
                "No clearly assigned owner"
              ].map((option) => (
                <label key={option} className="inline-flex items-center gap-2">
                  <Checkbox 
                    checked={includesValue("FA-ON-17", option)} 
                    onCheckedChange={() => toggleFairaArray("FA-ON-17", option)} 
                  />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
            </div>
            <p className="text-xs text-gray-500 pl-4">
              <Info className="inline h-3 w-3 mr-1" />
              FAIRA requires clear monitoring ownership for operational assurance.
            </p>
          </div>

          <Separator className="my-4" />

          {/* FA-ON-18 */}
          <div className="space-y-2">
            <Label>How frequently is the system reviewed or evaluated?</Label>
            <Select value={fairaData["FA-ON-18"] || ""} onValueChange={(v) => updateFaira("FA-ON-18", v)}>
              <SelectTrigger>
                <SelectValue placeholder="Select review frequency" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="Real-time / continuous">Real-time / continuous</SelectItem>
                <SelectItem value="After each decision or batch">After each decision or batch</SelectItem>
                <SelectItem value="Weekly / monthly">Weekly / monthly</SelectItem>
                <SelectItem value="Quarterly / annually">Quarterly / annually</SelectItem>
                <SelectItem value="Only after incidents or complaints">Only after incidents or complaints</SelectItem>
                <SelectItem value="No regular review schedule">No regular review schedule</SelectItem>
              </SelectContent>
            </Select>
            <p className="text-xs text-gray-500">
              <Info className="inline h-3 w-3 mr-1" />
              Documents review cadence for reliability and operational oversight.
            </p>
          </div>

          <Separator className="my-4" />

          {/* FA-ON-19 */}
          <div className="space-y-2">
            <Label>Does the system undergo any independent review or audit?</Label>
            <Select value={fairaData["FA-ON-19"] || ""} onValueChange={(v) => updateFaira("FA-ON-19", v)}>
              <SelectTrigger>
                <SelectValue placeholder="Select audit status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="Yes – regular independent audit">Yes – regular independent audit</SelectItem>
                <SelectItem value="Yes – occasional independent review">Yes – occasional independent review</SelectItem>
                <SelectItem value="Informal peer review only">Informal peer review only</SelectItem>
                <SelectItem value="No independent review">No independent review</SelectItem>
              </SelectContent>
            </Select>
            <p className="text-xs text-gray-500">
              <Info className="inline h-3 w-3 mr-1" />
              Supports FAIRA&apos;s external assurance expectations.
            </p>
          </div>

          <Separator className="my-4" />

          {/* FA-ON-20 */}
          <div className="space-y-2">
            <Label>Are there defined triggers for pausing, modifying, or rolling back the system?</Label>
            <Select value={fairaData["FA-ON-20"] || ""} onValueChange={(v) => updateFaira("FA-ON-20", v)}>
              <SelectTrigger>
                <SelectValue placeholder="Select trigger definition status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="Yes – explicit thresholds and triggers defined">Yes – explicit thresholds and triggers defined</SelectItem>
                <SelectItem value="Some triggers defined but not comprehensive">Some triggers defined but not comprehensive</SelectItem>
                <SelectItem value="Only informal / case-by-case decisions">Only informal / case-by-case decisions</SelectItem>
                <SelectItem value="No defined triggers">No defined triggers</SelectItem>
              </SelectContent>
            </Select>
            <p className="text-xs text-gray-500">
              <Info className="inline h-3 w-3 mr-1" />
              FAIRA requires clarity about conditions under which the system should be stopped or modified.
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
