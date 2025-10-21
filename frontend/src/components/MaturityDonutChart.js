import React from 'react';

const MaturityDonutChart = ({ score }) => {
  // Define the 5 maturity tiers
  const tiers = [
    { name: 'Basic', min: 0, max: 40, color: '#ff0000', percentage: 40 },
    { name: 'Low', min: 41, max: 60, color: '#ffc000', percentage: 20 },
    { name: 'Moderate', min: 61, max: 80, color: '#ffff00', percentage: 20 },
    { name: 'Good', min: 81, max: 90, color: '#92d050', percentage: 10 },
    { name: 'Excellent', min: 91, max: 100, color: '#00b050', percentage: 10 }
  ];

  // Determine which tier the score falls into
  const getCurrentTier = (score) => {
    for (let tier of tiers) {
      if (score >= tier.min && score <= tier.max) {
        return tier.name;
      }
    }
    return 'Basic';
  };

  const currentTier = getCurrentTier(score);

  // SVG dimensions - smaller to fit in allocated space
  const size = 180;
  const centerX = size / 2;
  const centerY = size / 2;
  const outerRadius = 75;
  const innerRadius = 50;
  const strokeWidth = 1;

  // Calculate the angle for the score marker (0-100 maps to full circle)
  const markerAngle = (score / 100) * 360 - 90; // -90 to start from top
  const markerRad = (markerAngle * Math.PI) / 180;
  const markerInnerX = centerX + innerRadius * Math.cos(markerRad);
  const markerInnerY = centerY + innerRadius * Math.sin(markerRad);
  const markerOuterX = centerX + outerRadius * Math.cos(markerRad);
  const markerOuterY = centerY + outerRadius * Math.sin(markerRad);

  // Function to create donut segments (arcs)
  const createArc = (startAngle, endAngle, innerR, outerR) => {
    const startRad = ((startAngle - 90) * Math.PI) / 180;
    const endRad = ((endAngle - 90) * Math.PI) / 180;

    const x1 = centerX + outerR * Math.cos(startRad);
    const y1 = centerY + outerR * Math.sin(startRad);
    const x2 = centerX + outerR * Math.cos(endRad);
    const y2 = centerY + outerR * Math.sin(endRad);
    const x3 = centerX + innerR * Math.cos(endRad);
    const y3 = centerY + innerR * Math.sin(endRad);
    const x4 = centerX + innerR * Math.cos(startRad);
    const y4 = centerY + innerR * Math.sin(startRad);

    const largeArc = endAngle - startAngle > 180 ? 1 : 0;

    return `
      M ${x1} ${y1}
      A ${outerR} ${outerR} 0 ${largeArc} 1 ${x2} ${y2}
      L ${x3} ${y3}
      A ${innerR} ${innerR} 0 ${largeArc} 0 ${x4} ${y4}
      Z
    `;
  };

  // Create segments with cumulative angles
  let currentAngle = 0;
  const segments = tiers.map((tier, index) => {
    const startAngle = currentAngle;
    const sweepAngle = (tier.percentage / 100) * 360;
    const endAngle = currentAngle + sweepAngle;
    
    // Calculate label position (middle of the segment) - further out
    const midAngle = startAngle + sweepAngle / 2 - 90;
    const midRad = (midAngle * Math.PI) / 180;
    const labelRadius = outerRadius + 18; // Position labels outside the ring
    const labelX = centerX + labelRadius * Math.cos(midRad);
    const labelY = centerY + labelRadius * Math.sin(midRad);

    const segment = {
      ...tier,
      startAngle,
      endAngle,
      path: createArc(startAngle, endAngle, innerRadius, outerRadius),
      labelX,
      labelY
    };

    currentAngle = endAngle;
    return segment;
  });

  return (
    <div className="flex items-center justify-center w-full">
      <svg 
        width="100%" 
        height="auto" 
        viewBox={`0 0 ${size} ${size}`}
        style={{ maxWidth: '180px' }}
      >
        {/* Draw all tier segments */}
        {segments.map((segment, index) => (
          <path
            key={index}
            d={segment.path}
            fill={segment.color}
            stroke="#333"
            strokeWidth={strokeWidth}
          />
        ))}

        {/* Draw radial marker line pointing to score position */}
        <line
          x1={markerInnerX}
          y1={markerInnerY}
          x2={markerOuterX}
          y2={markerOuterY}
          stroke="#000"
          strokeWidth={2}
          strokeLinecap="round"
        />

        {/* Center circle background */}
        <circle
          cx={centerX}
          cy={centerY}
          r={innerRadius - strokeWidth}
          fill="white"
          stroke="#333"
          strokeWidth={strokeWidth}
        />

        {/* Score text in center */}
        <text
          x={centerX}
          y={centerY - 5}
          textAnchor="middle"
          fontSize="24"
          fontWeight="bold"
          fill="#333"
        >
          {Math.round(score)}%
        </text>

        {/* Maturity level text below score */}
        <text
          x={centerX}
          y={centerY + 12}
          textAnchor="middle"
          fontSize="10"
          fontWeight="600"
          fill="#666"
        >
          {currentTier}
        </text>

        {/* Tier labels on segments - smaller font */}
        {segments.map((segment, index) => {
          // For smaller segments (Good, Excellent), show abbreviated labels
          const isSmallSegment = segment.percentage <= 10;
          const line1 = isSmallSegment ? segment.name.substring(0, 4) : segment.name;
          const line2 = `${segment.min}-${segment.max}`;
          
          return (
            <g key={`label-${index}`}>
              <text
                x={segment.labelX}
                y={segment.labelY - 4}
                textAnchor="middle"
                fontSize="7"
                fontWeight="600"
                fill="#000"
                stroke="white"
                strokeWidth={2}
                paintOrder="stroke"
              >
                {line1}
              </text>
              <text
                x={segment.labelX}
                y={segment.labelY + 5}
                textAnchor="middle"
                fontSize="6"
                fontWeight="500"
                fill="#000"
                stroke="white"
                strokeWidth={2}
                paintOrder="stroke"
              >
                {line2}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
};

export default MaturityDonutChart;
