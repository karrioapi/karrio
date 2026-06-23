import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { AuthShell } from "~/components/auth/AuthShell";
import { requestPasswordReset } from "~/server/auth";

export const Route = createFileRoute("/forgot")({
  component: ForgotScreen,
});

const isEmail = (s: string) => /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(s);

function ForgotScreen() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [sent, setSent] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (!isEmail(email)) return setError("Enter a valid email address.");
    setSubmitting(true);
    try {
      await requestPasswordReset({ data: { email } });
      setSent(true);
    } catch {
      // Always show success to avoid account enumeration.
      setSent(true);
    } finally {
      setSubmitting(false);
    }
  };

  if (sent) {
    return (
      <AuthShell>
        <div className="auth-success" data-testid="forgot-success">
          <div className="ok">✓</div>
          <h1>Check your email</h1>
          <div className="sub">If an account exists for {email}, a reset link is on its way.</div>
        </div>
      </AuthShell>
    );
  }

  return (
    <AuthShell>
      <h1>Reset your password</h1>
      <div className="sub">We'll email you a link to reset it.</div>
      <form onSubmit={onSubmit} data-testid="forgot-form" noValidate>
        <div className="auth-field">
          <label htmlFor="email">Email</label>
          <input id="email" type="email" className="auth-input" value={email} onChange={(e) => setEmail(e.target.value)} data-testid="forgot-email" />
        </div>
        {error && <div className="auth-error" data-testid="forgot-error">{error}</div>}
        <button type="submit" className="auth-submit" disabled={submitting} data-testid="forgot-submit">
          {submitting ? "Sending…" : "Send reset link"}
        </button>
      </form>
      <div className="auth-alt">
        <a onClick={() => navigate({ to: "/login" })} data-testid="to-login">Back to sign in</a>
      </div>
    </AuthShell>
  );
}
