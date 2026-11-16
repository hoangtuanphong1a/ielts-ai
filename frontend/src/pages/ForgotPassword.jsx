import { useState } from "react";
import { Link } from "react-router-dom";
import { ArrowLeft, CircleNotch, EnvelopeSimple } from "@phosphor-icons/react";
import { api, errorText } from "../api.js";
import { Brand, ErrorAlert } from "../components/ui.jsx";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [sent, setSent] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function onSubmit(e) {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      await api("/auth/password/reset/", { method: "POST", body: { email }, retry: false });
      setSent(true);
    } catch (err) {
      setError(err.status === 429 ? "Too many requests. Please try again in an hour." : errorText(err));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="auth auth-single">
      <main className="auth-main">
        <form className="auth-form card" onSubmit={onSubmit}>
          <Brand to="/login" />
          <div className="page-head">
            <h1>Forgot password</h1>
            <p className="muted">Enter the email you signed up with and we will send you a reset link.</p>
          </div>

          {sent ? (
            <div className="alert" role="status">
              <EnvelopeSimple size={20} />
              <span>If that email is registered, a reset link is on its way. It expires in 1 hour.</span>
            </div>
          ) : (
            <>
              <div className="field">
                <label htmlFor="email">Email</label>
                <input id="email" type="email" autoComplete="email" required
                       value={email} onChange={(e) => setEmail(e.target.value)} />
              </div>
              <ErrorAlert>{error}</ErrorAlert>
              <button className="btn btn-block" disabled={busy}>
                {busy && <CircleNotch size={18} className="spin" />}
                {busy ? "Sending" : "Send reset link"}
              </button>
            </>
          )}

          <Link to="/login" className="small" style={{ display: "inline-flex", gap: 6, alignItems: "center" }}>
            <ArrowLeft size={16} /> Back to log in
          </Link>
        </form>
      </main>
    </div>
  );
}
