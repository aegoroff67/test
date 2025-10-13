import React from "react";

export default function InfoBadge({ className = "", title, onClick }) {
  return (
    <button
      type="button"
      aria-label="More info"
      title={title}
      onClick={onClick}
      className={[
        "inline-flex items-center justify-center",
        "h-5 w-5 rounded-full",
        "bg-blue-600 text-white",
        "opacity-80 hover:opacity-100",
        "transition-opacity",
        "focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2",
        className,
      ].join(" ")}
    >
      {/* white "i" glyph via SVG for crisp rendering */}
      <svg viewBox="0 0 24 24" aria-hidden="true" className="h-3.5 w-3.5">
        <path fill="currentColor" d="M11 10h2v8h-2v-8zm0-4h2v2h-2V6z" />
      </svg>
    </button>
  );
}
