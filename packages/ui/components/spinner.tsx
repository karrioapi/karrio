import React from 'react';


export const Spinner: React.FC<{ className?: string, size?: number }> = ({ className, size }) => (
  <div className={className || "my-6 p-6 has-text-centered"}
    style={{ background: "transparent" }}>
    <div className={`button is-white is-loading p-7 has-text-primary is-size-${size || 1}`}
      style={{ background: "transparent" }}>
    </div>
  </div>
);

