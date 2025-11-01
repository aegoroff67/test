import React from 'react';

const Logo = ({ className = "h-6 w-6", alt = "AM AI SAFE Logo" }) => {
  return (
    <img 
      src="/logo.jpg" 
      alt={alt}
      className={className}
      style={{ objectFit: 'contain' }}
    />
  );
};

export default Logo;
