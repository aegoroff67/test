import React from 'react';
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer, Legend, Tooltip } from 'recharts';

/**
 * DomainBenchmarkRadar - Displays a radar chart comparing organization's domain scores
 * with sector benchmarks
 * 
 * @param {Array} domainScores - Array of domain score objects with domain_name and percentage
 * @param {Object} benchmarks - Object mapping domain names to benchmark scores (0-100)
 * @param {String} sector - Name of the sector for display
 */
const DomainBenchmarkRadar = ({ domainScores, benchmarks, sector }) => {
  // Transform data for radar chart
  const radarData = domainScores.map(domain => ({
    domain: domain.domain_name,
    'Your Score': Math.round(domain.percentage),
    'Sector Benchmark': benchmarks[domain.domain_name] || 0
  }));

  // Custom tooltip
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-gray-200 rounded shadow-lg">
          <p className="font-semibold text-gray-900 mb-2">{payload[0].payload.domain}</p>
          {payload.map((entry, index) => (
            <p key={index} style={{ color: entry.color }} className="text-sm">
              {entry.name}: {entry.value}%
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="w-full h-full flex items-center justify-center">
      <div style={{ width: '700px', height: '600px', margin: '0 auto' }}>
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart data={radarData} cx="50%" cy="50%" margin={{ top: 30, right: 60, bottom: 30, left: 60 }}>
            <PolarGrid stroke="#e5e7eb" strokeWidth={1.5} />
            <PolarAngleAxis 
              dataKey="domain" 
              tick={{ fill: '#374151', fontSize: 13 }}
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
            <Tooltip content={<CustomTooltip />} />
          </RadarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default DomainBenchmarkRadar;
