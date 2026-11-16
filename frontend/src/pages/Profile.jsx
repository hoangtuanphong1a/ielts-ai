import { useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { CheckCircle, CircleNotch, FloppyDisk } from "@phosphor-icons/react";
import { useAuth } from "../auth.jsx";
import { errorText } from "../api.js";
import { ErrorAlert } from "../components/ui.jsx";
import ChangePassword from "../components/ChangePassword.jsx";

// 4.0 -> 9.0, bước 0.5
const BANDS = Array.from({ length: 11 }, (_, i) => (4 + i * 0.5).toFixed(1));
const MINUTES = [15, 30, 45, 60, 90, 120];
const ROLE_LABEL = { student: "Student", teacher: "Teacher", admin: "Admin" };

export function daysUntil(dateStr) {
  if (!dateStr) return null;
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  return Math.round((new Date(`${dateStr}T00:00:00`) - today) / 86_400_000);
}

export default function Profile() {
  const { user, updateMe } = useAuth();
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const welcome = params.get("welcome") === "1";
  const p = user.profile ?? {};

  const [form, setForm] = useState({
    email: user.email ?? "",
    target_band: p.target_band != null ? Number(p.target_band).toFixed(1) : "",
    exam_date: p.exam_date ?? "",
    daily_minutes: String(p.daily_minutes ?? 30),
  });
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [saved, setSaved] = useState(false);

  const update = (e) => {
    setSaved(false);
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  async function onSubmit(e) {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      await updateMe({
        email: form.email,
        profile: {
          target_band: form.target_band ? Number(form.target_band) : null,
          exam_date: form.exam_date || null,
          daily_minutes: Number(form.daily_minutes),
        },
      });
      setSaved(true);
      if (welcome) navigate("/");
    } catch (err) {
      setError(errorText(err));
    } finally {
      setBusy(false);
    }
  }

  const days = daysUntil(form.exam_date);
  const todayStr = new Date().toISOString().slice(0, 10);

  return (
    <div className="page">
      <div className="page-head">
        <h1>{welcome ? "Set your goal" : "Profile and goals"}</h1>
        <p className="muted">
          {welcome
            ? "Tell us your target band and exam date so your plan fits you."
            : "Your target band and exam date shape your study plan and reminders."}
        </p>
      </div>

      <form className="card" onSubmit={onSubmit} style={{ display: "grid", gap: "1.25rem" }}>
        <div className="grid-2">
          <div className="field">
            <label htmlFor="username">Username</label>
            <input id="username" value={user.username} disabled />
          </div>
          <div className="field">
            <label htmlFor="role">Role</label>
            <input id="role" value={ROLE_LABEL[p.role] ?? p.role ?? ""} disabled />
          </div>
        </div>

        <div className="field">
          <label htmlFor="email">Email</label>
          <input id="email" name="email" type="email" autoComplete="email" value={form.email} onChange={update} />
        </div>

        <div className="grid-2">
          <div className="field">
            <label htmlFor="target_band">Target band</label>
            <select id="target_band" name="target_band" value={form.target_band} onChange={update}>
              <option value="">Not set</option>
              {BANDS.map((b) => <option key={b} value={b}>{b}</option>)}
            </select>
          </div>
          <div className="field">
            <label htmlFor="exam_date">Exam date</label>
            <input id="exam_date" name="exam_date" type="date" min={todayStr} value={form.exam_date} onChange={update} />
            {days != null && (
              <span className="muted small">{days >= 0 ? `${days} days to go` : "This date has passed"}</span>
            )}
          </div>
        </div>

        <div className="field">
          <span id="minutes-label" className="small" style={{ fontWeight: 500 }}>Daily study time</span>
          <div className="chips" role="radiogroup" aria-labelledby="minutes-label">
            {MINUTES.map((m) => (
              <button
                key={m}
                type="button"
                role="radio"
                aria-checked={form.daily_minutes === String(m)}
                aria-pressed={form.daily_minutes === String(m)}
                className="chip"
                onClick={() => update({ target: { name: "daily_minutes", value: String(m) } })}
              >
                {m} min
              </button>
            ))}
          </div>
        </div>

        <ErrorAlert>{error}</ErrorAlert>

        <div className="editor-bar">
          {saved && (
            <span role="status" className="small" style={{ display: "inline-flex", gap: 6, alignItems: "center" }}>
              <CheckCircle size={18} /> Saved
            </span>
          )}
          <span className="spacer" />
          <button className="btn" disabled={busy}>
            {busy ? <CircleNotch size={18} className="spin" /> : <FloppyDisk size={18} />}
            {welcome ? "Save and start" : "Save changes"}
          </button>
        </div>
      </form>

      <ChangePassword />

    </div>
  );
}
