import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { ShieldCheck } from "lucide-react";

const AssessmentOverview = ({ form, update }) => {
  return (
    <Card>
      <CardHeader className="bg-orange-50 border-b border-orange-100">
        <div className="flex items-center space-x-2">
          <ShieldCheck className="h-5 w-5 text-orange-600" />
          <CardTitle className="text-xl">Assessment Overview</CardTitle>
        </div>
      </CardHeader>
      <CardContent className="p-6 space-y-8">
        {/* Section A: Assessment Information */}
        <div className="space-y-4">
          <h3 className="text-base font-semibold text-gray-900 border-b border-gray-200 pb-2">A. Assessment Information</h3>
          <div className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="ai_system_name">AI System Name *</Label>
              <Input
                id="ai_system_name"
                value={form.ai_system_name}
                onChange={(e) => update("ai_system_name", e.target.value)}
                required
                placeholder="Enter AI system name"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="ai_system_version">AI System Version *</Label>
              <Input
                id="ai_system_version"
                value={form.ai_system_version}
                onChange={(e) => update("ai_system_version", e.target.value)}
                required
                placeholder="Enter version"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="business_unit">Business Unit / Branch *</Label>
              <Input
                id="business_unit"
                value={form.business_unit}
                onChange={(e) => update("business_unit", e.target.value)}
                required
                placeholder="Enter business unit or branch"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="system_owner_name">System Owner Name *</Label>
              <Input
                id="system_owner_name"
                value={form.system_owner_name}
                onChange={(e) => update("system_owner_name", e.target.value)}
                required
                placeholder="Enter system owner name"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="system_owner_role">System Owner Role/Title *</Label>
              <Input
                id="system_owner_role"
                value={form.system_owner_role}
                onChange={(e) => update("system_owner_role", e.target.value)}
                required
                placeholder="Enter system owner role"
              />
            </div>
          </div>
        </div>

        {/* Section B: Assessor Information */}
        <div className="space-y-4">
          <h3 className="text-base font-semibold text-gray-900 border-b border-gray-200 pb-2">B. Assessor Information</h3>
          <div className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="assessor_name">Assessor Name *</Label>
              <Input
                id="assessor_name"
                value={form.assessor_name}
                onChange={(e) => update("assessor_name", e.target.value)}
                required
                placeholder="Enter your name"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="assessor_role">Assessor Role/Title *</Label>
              <Input
                id="assessor_role"
                value={form.assessor_role}
                onChange={(e) => update("assessor_role", e.target.value)}
                required
                placeholder="Enter your role"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="assessor_branch">Assessor Branch / Division *</Label>
              <Input
                id="assessor_branch"
                value={form.assessor_branch}
                onChange={(e) => update("assessor_branch", e.target.value)}
                required
                placeholder="Enter your branch or division"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="assessor_email">Assessor Email (optional)</Label>
              <Input
                id="assessor_email"
                type="email"
                value={form.assessor_email}
                onChange={(e) => update("assessor_email", e.target.value)}
                placeholder="Enter your email"
              />
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default AssessmentOverview;
