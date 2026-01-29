import React from 'react';

// Shared RadioScale component for rating questions
export const RadioScale = ({ value, onChange, min = 1, max = 5, labels = {} }) => (
  <div className="flex items-center space-x-4">
    {Array.from({ length: max - min + 1 }, (_, i) => min + i).map((num) => (
      <label key={num} className="flex flex-col items-center cursor-pointer">
        <input
          type="radio"
          checked={value === num}
          onChange={() => onChange(num)}
          className="h-4 w-4 text-orange-600 focus:ring-orange-500"
        />
        <span className="text-xs mt-1">{labels[num] || num}</span>
      </label>
    ))}
  </div>
);

export default RadioScale;
