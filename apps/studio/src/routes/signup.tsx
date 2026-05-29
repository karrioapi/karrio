import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { AuthShell, PasswordField } from "~/components/auth/AuthShell";
import { register } from "~/server/auth";

export const Route = createFileRoute("/signup")({
  component: SignupScreen,
});

const isEmail = (s: string) => /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(s);

function SignupScreen() {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [org, setOrg] = useState("");
  const [password, setPassword] = useState("");
  const [show, setShow] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [done, setDone] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const strong = password.length >= 8;

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (!name) return setError("Enter your name.");
    if (!isEmail(email)) return setError("Enter a valid email address.");
    if (!strong) return setError("Password must be at least 8 characters.");
    setSubmitting(true);
    try {
      const res = await register({ data: { email, password, full_name: name, organization_name: org || undefined } });
      if (res.ok) setDone(true);
      else setError(res.errors?.[0]?.messages?.[0] ?? "Registration failed.");
    } catch {
      setError("Something went wrong. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  if (done) {
    return (
      <AuthShell>
        <div className="auth-success" data-testid="signup-success">
          <div className="ok">✓</div>
          <h1>Check your email</h1>
          <div className="sub">We sent a verification link to {email}.</div>
        </div>
      </AuthShell>
    );
  }

  return (
    <AuthShell>
      <h1>Create your account</h1>
      <div className="sub">Start shipping with Karrio Studio.</div>
      <form onSubmit={onSubmit} data-testid="signup-form" noValidate>
        <div className="auth-field">
          <label htmlFor="name">Full name</label>
          <input id="name" className="auth-input" value={name} onChange={(e) => setName(e.target.value)} data-testid="signup-name" />
        </div>
        <div className="auth-field">
          <label htmlFor="email">Work email</label>
          <input id="email" type="email" className="auth-input" value={email} onChange={(e) => setEmail(e.target.value)} data-testid="signup-email" />
        </div>
        <div className="auth-field">
          <label htmlFor="org">Organization (optional)</label>
          <input id="org" className="auth-input" value={org} onChange={(e) => setOrg(e.target.value)} data-testid="signup-org" />
        </div>
        <div className="auth-field">
          <label htmlFor="password">Password</label>
          <PasswordField id="password" value={password} onChange={setPassword} show={show} onToggle={() => setShow((s) => !s)} />
          <div className="auth-error" style={{ color: strong ? "var(--green-fg)" : "var(--fg-muted)" }} data-testid="signup-strength">
            {strong ? "Strong enough" : "At least 8 characters"}
          </div>
        </div>
        {error && <div className="auth-error" data-testid="signup-error">{error}</div>}
        <button type="submit" className="auth-submit" disabled={submitting} data-testid="signup-submit">
          {submitting ? "Creating…" : "Create account"}
        </button>
      </form>
      <div className="auth-alt">
        Already have an account? <a onClick={() => navigate({ to: "/login" })} data-testid="to-login">Sign in</a>
      </div>
    </AuthShell>
  );
}
