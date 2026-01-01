import React from 'react';
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer, Legend, Tooltip } from 'recharts';

/**
 * DomainBenchmarkRadar - Displays a radar chart comparing organization's domain scores
 * with sector benchmarks
 * 
 * @param {Array} domainScores - Array of domain score objects with domain_name and percentage
 * @param {Object} benchmarks - Object mapping domain names to benchmark scores (0-100)
 * @param {String} sector - Name of the sector for display
 * @param {String} assessmentType - Type of assessment (System, Awareness, etc.)
 */

// Custom tooltip component defined outside to avoid re-creation on each render
const CustomTooltip = ({ active, payload, assessmentType }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white p-3 border border-gray-200 rounded shadow-lg max-w-xs">
        <p className="font-semibold text-gray-900 mb-2">{payload[0].payload.domain}</p>
        {payload.map((entry, index) => (
          <p key={index} style={{ color: entry.color }} className="text-sm">
            {entry.name}: {entry.value}%
          </p>
        ))}
        {assessmentType === 'Awareness' && (
          <p className="text-xs text-gray-500 mt-2 pt-2 border-t border-gray-200">
            <span className="font-semibold">Note:</span> Based on completed AI Awareness assessments within your selected sector.
          </p>
        )}
      </div>
    );
  }
  return null;
};

const DomainBenchmarkRadar = ({ domainScores, benchmarks, sector, assessmentType }) => {
  // Format domain labels with line breaks for long names
  const formatDomainLabel = (domainName) => {
    if (domainName === 'Governance & Trust Foundations') {
      return 'Governance &\nTrust Foundations';
    }
    return domainName;
  };

  // Transform data for radar chart
  const radarData = domainScores.map(domain => ({
    domain: formatDomainLabel(domain.domain_name),
    'Your Score': Math.round(domain.percentage),
    'Sector Benchmark': benchmarks[domain.domain_name] || 0
  }));

  return (
    <div className="w-full h-full flex items-center justify-center">
      <div style={{ width: '700px', height: '700px' }}>
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart data={radarData} margin={{ top: 20, right: 80, bottom: 40, left: 80 }}>
            <PolarGrid stroke="#e5e7eb" strokeWidth={1.5} />
            <PolarAngleAxis 
              dataKey="domain" 
              tick={{ fill: '#374151', fontSize: 13, textAnchor: 'middle' }}
              tickLine={{ stroke: '#9ca3af' }}
            />
            <PolarRadiusAxis 
              angle={90} 
              domain={[0, 100]} 
              tick={{ fill: '#6b7280', fontSize: 11 }}
              tickCount={6}
              tickFormatter={(value) => `${value}%`}
            />
            <Radar 
              name="Your Score" 
              dataKey="Your Score" 
              stroke="#3b82f6" 
              fill="#3b82f6" 
              fillOpacity={0.5}
              strokeWidth={2.5}
            />
            <Radar 
              name="Sector Benchmark" 
              dataKey="Sector Benchmark" 
              stroke="#10b981" 
              fill="#10b981" 
              fillOpacity={0.3}
              strokeWidth={2.5}
              strokeDasharray="5 5"
            />
            <Legend 
              verticalAlign="bottom" 
              height={40}
              wrapperStyle={{ paddingTop: '10px', fontSize: '14px' }}
              iconSize={14}
            />
            <Tooltip content={<CustomTooltip assessmentType={assessmentType} />} />
          </RadarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default DomainBenchmarkRadar;
