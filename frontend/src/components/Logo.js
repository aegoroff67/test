import React from 'react';

const Logo = ({ className = "h-10 w-10", alt = "AM AI SAFE Logo" }) => {
  return (
    <img 
      src="/logo.png" 
      alt={alt}
      className={`${className} rounded-lg`}
      style={{ objectFit: 'contain' }}
    />
  );
};

export default Logo;
