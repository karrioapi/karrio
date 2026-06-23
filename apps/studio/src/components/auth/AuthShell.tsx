// AuthShell.tsx — split-panel chrome for pre-auth screens.
import type { ReactNode } from "react";

export function AuthShell({ children }: { children: ReactNode }) {
  return (
    <div className="auth">
      <aside className="auth-aside">
        <div className="brand">
          <span className="mark">K</span> Karrio Studio
        </div>
        <div>
          <h2>Shipping operations, reimagined as a studio.</h2>
          <p>Ship, build, and govern your multi-carrier logistics from one agent-friendly workspace.</p>
        </div>
        <div style={{ fontSize: 12, color: "#6a6a7a" }}>© Karrio</div>
      </aside>
      <main className="auth-main">
        <div className="auth-card">{children}</div>
      </main>
    </div>
  );
}

export function PasswordField({
  value,
  onChange,
  show,
  onToggle,
  id,
  placeholder,
  error,
}: {
  value: string;
  onChange: (v: string) => void;
  show: boolean;
  onToggle: () => void;
  id: string;
  placeholder?: string;
  error?: boolean;
}) {
  return (
    <div className="auth-input-wrap">
      <input
        id={id}
        name={id}
        type={show ? "text" : "password"}
        className={"auth-input" + (error ? " error" : "")}
        value={value}
        placeholder={placeholder}
        onChange={(e) => onChange(e.target.value)}
        autoComplete="current-password"
      />
      <button type="button" className="auth-eye" aria-label={show ? "Hide password" : "Show password"} onClick={onToggle}>
        {show ? "🙈" : "👁"}
      </button>
    </div>
  );
}
