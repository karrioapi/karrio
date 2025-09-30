import * as React from 'react';

interface SimpleTextProps {
  text?: string;
}

/**
 * A simple text component with basic styling
 */
export function SimpleText({ text = "Hello from Karrio Insiders" }: SimpleTextProps) {
  return <div className="p-4 border rounded my-4">{text}</div>;
}
