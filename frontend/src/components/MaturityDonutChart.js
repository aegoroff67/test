import React from 'react';

const MaturityStackedColumn = ({ score }) => {
  // Define the 5 maturity tiers
  const tiers = [
    { name: 'Excellent', min: 91, max: 100, color: '#00b050', percentage: 10 },
    { name: 'Good', min: 81, max: 90, color: '#92d050', percentage: 10 },
    { name: 'Moderate', min: 61, max: 80, color: '#ffff00', percentage: 20 },
    { name: 'Low', min: 41, max: 60, color: '#ffc000', percentage: 20 },
    { name: 'Basic', min: 0, max: 40, color: '#ff0000', percentage: 40 }
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

  // Calculate arrow position (percentage from bottom)
  const arrowPosition = score;

  return (
    <div className="flex items-center justify-center w-full" style={{ height: '120px', gap: '30px' }}>
      {/* Stacked Column */}
      <div className="relative flex flex-col" style={{ width: '50px', height: '100px' }}>
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
              <div className="text-[7px] font-semibold leading-tight text-gray-900">
                {tier.name}
              </div>
            </div>
          </div>
        ))}
        
        {/* Arrow indicator */}
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
              borderRight: '8px solid black'
            }}
          />
        </div>
      </div>

      {/* Score Display */}
      <div className="flex flex-col items-center">
        <div className="text-2xl font-bold text-gray-900">
          {Math.round(score)}%
        </div>
        <div className="text-[15px] font-semibold text-gray-700 leading-tight text-center">
          {currentTier} AI Maturity
        </div>
      </div>
    </div>
  );
};

export default MaturityStackedColumn;
