import { useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { CheckCircle, CircleNotch } from "@phosphor-icons/react";
import { api, errorText } from "../api.js";
import { Brand, ErrorAlert } from "../components/ui.jsx";

export default function ResetPassword() {
  const [params] = useSearchParams();
  const uid = params.get("uid");
  const token = params.get("token");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [done, setDone] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function onSubmit(e) {
    e.preventDefault();
    setError("");
    if (password !== confirm) {
      setError("The two passwords do not match.");
      return;
    }
    setBusy(true);
    try {
      await api("/auth/password/reset/confirm/", {
        method: "POST",
        body: { uid, token, new_password: password },
        retry: false,
      });
      setDone(true);
    } catch (err) {
      setError(errorText(err));
    } finally {
      setBusy(false);
    }
  }

  const broken = !uid || !token;

  return (
    <div className="auth auth-single">
      <main className="auth-main">
        <form className="auth-form card" onSubmit={onSubmit}>
          <Brand to="/login" />
          <div className="page-head">
            <h1>Set a new password</h1>
          </div>

          {done ? (
            <>
              <div className="alert" role="status">
                <CheckCircle size={20} />
                <span>Password updated. You can now log in with your new password.</span>
              </div>
              <Link to="/login" className="btn btn-block">Log in</Link>
            </>
          ) : broken ? (
            <>
              <ErrorAlert>This link is invalid. Open the exact link from your email or request a new one.</ErrorAlert>
              <Link to="/forgot-password" className="btn btn-block">Request a new link</Link>
            </>
          ) : (
            <>
              <div className="field">
                <label htmlFor="password">New password</label>
                <input id="password" type="password" autoComplete="new-password" required
                       value={password} onChange={(e) => setPassword(e.target.value)} />
                <span className="muted small">At least 8 characters. Avoid common passwords.</span>
              </div>
              <div className="field">
                <label htmlFor="confirm">Confirm password</label>
                <input id="confirm" type="password" autoComplete="new-password" required
                       value={confirm} onChange={(e) => setConfirm(e.target.value)} />
              </div>
              <ErrorAlert>{error}</ErrorAlert>
              <button className="btn btn-block" disabled={busy}>
                {busy && <CircleNotch size={18} className="spin" />}
                {busy ? "Saving" : "Save new password"}
              </button>
              {error && <Link to="/forgot-password" className="small">Request a new link</Link>}
            </>
          )}
        </form>
      </main>
    </div>
  );
}
