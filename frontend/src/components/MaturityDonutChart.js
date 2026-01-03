import React from 'react';

const MaturityStackedColumn = ({ score, assessmentType, sectorAverage, sectorName }) => {
  // Define the 4 maturity tiers with new ranges
  // Use different labels for Awareness assessment
  const tiers = assessmentType === 'Awareness' ? [
    { name: 'Established', min: 86, max: 100, color: '#00B050', percentage: 15 },      // 15% of bar
    { name: 'Developing', min: 66, max: 85, color: '#FFFF00', percentage: 20 },       // 20% of bar
    { name: 'Emerging', min: 41, max: 65, color: '#FFC000', percentage: 25 },         // 25% of bar
    { name: 'Introductory', min: 0, max: 40, color: '#FF0000', percentage: 40 }       // 40% of bar
  ] : [
    { name: 'Leading', min: 86, max: 100, color: '#00B050', percentage: 15 },         // 15% of bar
    { name: 'Established', min: 66, max: 85, color: '#FFFF00', percentage: 20 },      // 20% of bar
    { name: 'Developing', min: 41, max: 65, color: '#FFC000', percentage: 25 },       // 25% of bar
    { name: 'Foundational', min: 0, max: 40, color: '#FF0000', percentage: 40 }       // 40% of bar
  ];

  // Determine which tier the score falls into
  const getCurrentTier = (score) => {
    for (let tier of tiers) {
      if (score >= tier.min && score <= tier.max) {
        return tier.name;
      }
    }
    return 'Foundational';
  };

  const currentTier = getCurrentTier(score);

  // Calculate arrow position (percentage from bottom)
  const arrowPosition = score;

  // Determine arrow color based on comparison with sector average (for Awareness, System, Readiness, and Orgwide)
  const getUserArrowColor = () => {
    if ((assessmentType === 'Awareness' || assessmentType === 'System' || assessmentType === 'Readiness' || assessmentType === 'Orgwide') && sectorAverage !== null && sectorAverage !== undefined) {
      if (score > sectorAverage) return '#00B050'; // Green
      if (score < sectorAverage) return '#FF0000'; // Red
    }
    return '#000000'; // Black (default or if equal)
  };

  const userArrowColor = getUserArrowColor();

  return (
    <div className="flex items-center justify-center w-full" style={{ height: '120px', gap: '30px' }}>
      {/* Stacked Column */}
      <div className="relative flex flex-col" style={{ width: '75px', height: '100px' }}>
        {tiers.map((tier, index) => (
          <div
            key={index}
            className="relative border border-gray-800"
            style={{
              height: `${tier.percentage}%`,
              backgroundColor: tier.color,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
          >
            <div className="text-center px-1">
              <div className="text-[10px] font-semibold leading-tight text-gray-900">
                {tier.name}
              </div>
            </div>
          </div>
        ))}
        
        {/* User score arrow indicator */}
        <div
          className="absolute right-0 flex items-center"
          style={{
            bottom: `${arrowPosition}%`,
            transform: 'translateY(50%)',
            right: '-8px'
          }}
        >
          <div
            style={{
              width: 0,
              height: 0,
              borderTop: '6px solid transparent',
              borderBottom: '6px solid transparent',
              borderRight: `8px solid ${userArrowColor}`
            }}
          />
        </div>

        {/* Sector average arrow indicator (for Awareness, System, and Readiness with valid sector average) */}
        {(assessmentType === 'Awareness' || assessmentType === 'System' || assessmentType === 'Readiness') && sectorAverage !== null && sectorAverage !== undefined && sectorAverage !== score && (
          <div
            className="absolute left-0 flex items-center"
            style={{
              bottom: `${sectorAverage}%`,
              transform: 'translateY(50%)',
              left: '-8px'
            }}
          >
            <div
              style={{
                width: 0,
                height: 0,
                borderTop: '6px solid transparent',
                borderBottom: '6px solid transparent',
                borderLeft: '8px solid #000000'
              }}
            />
          </div>
        )}
      </div>

      {/* Score Display */}
      <div className="flex flex-col items-center">
        <div className="text-2xl font-bold text-gray-900">
          {Math.round(score)}%
        </div>
        <div className="text-[15px] font-semibold text-gray-700 leading-tight text-center">
          {currentTier} {assessmentType === 'Awareness' ? 'AI Awareness' : assessmentType === 'Readiness' ? 'AI Readiness' : 'AI Maturity'}
        </div>
        {/* Sector average (for System and Readiness assessments) */}
        {(assessmentType === 'System' || assessmentType === 'Readiness') && sectorAverage !== null && sectorAverage !== undefined && sectorName && (
          <div className="text-[11px] text-gray-600 leading-tight text-center mt-1">
            (<strong>{sectorName}</strong> sector average: <strong>{sectorAverage}%</strong>)
          </div>
        )}
      </div>
    </div>
  );
};

export default MaturityStackedColumn;
