import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { AuthShell, PasswordField } from "~/components/auth/AuthShell";
import { login } from "~/server/auth";

export const Route = createFileRoute("/login")({
  component: LoginScreen,
});

const isEmail = (s: string) => /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(s);

function LoginScreen() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [show, setShow] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (!isEmail(email)) return setError("Enter a valid email address.");
    if (!password) return setError("Enter your password.");
    setSubmitting(true);
    try {
      const res = await login({ data: { email, password } });
      if (res.ok) {
        // Full navigation so the server session cookie is read fresh and the
        // client session/data layer initializes authenticated (avoids a
        // post-login client-nav waterfall where hooks stay unauthenticated).
        window.location.assign("/home");
      } else {
        setError(res.errors?.[0]?.messages?.[0] ?? "Invalid email or password.");
      }
    } catch {
      setError("Something went wrong. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <AuthShell>
      <h1>Sign in</h1>
      <div className="sub">Welcome back to Karrio Studio.</div>
      <form onSubmit={onSubmit} data-testid="login-form" noValidate>
        <div className="auth-field">
          <label htmlFor="email">Email</label>
          <input
            id="email"
            name="email"
            type="email"
            className={"auth-input" + (error && !isEmail(email) ? " error" : "")}
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            autoComplete="email"
            data-testid="login-email"
          />
        </div>
        <div className="auth-field">
          <label htmlFor="password">Password</label>
          <PasswordField id="password" value={password} onChange={setPassword} show={show} onToggle={() => setShow((s) => !s)} />
        </div>
        {error && <div className="auth-error" data-testid="login-error">{error}</div>}
        <button type="submit" className="auth-submit" disabled={submitting} data-testid="login-submit">
          {submitting ? "Signing in…" : "Sign in"}
        </button>
      </form>
      <div className="auth-alt">
        <a onClick={() => navigate({ to: "/forgot" })} data-testid="to-forgot">Forgot password?</a>
        {" · "}
        <a onClick={() => navigate({ to: "/signup" })} data-testid="to-signup">Create an account</a>
      </div>
    </AuthShell>
  );
}
