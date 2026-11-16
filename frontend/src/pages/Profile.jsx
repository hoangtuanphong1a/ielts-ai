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
const ROLE_LABEL = { student: "Học viên", teacher: "Giáo viên", admin: "Quản trị" };

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
    <div className="page" style={{ maxWidth: 720 }}>
      <div className="page-head">
        <h1>{welcome ? "Đặt mục tiêu của bạn" : "Hồ sơ và mục tiêu"}</h1>
        <p className="muted">
          {welcome
            ? "Cho hệ thống biết bạn muốn đạt band nào và khi nào thi, để lộ trình sát với bạn."
            : "Band mục tiêu và ngày thi dùng để tính lộ trình và nhắc học."}
        </p>
      </div>

      <form className="card" onSubmit={onSubmit} style={{ display: "grid", gap: "1.25rem" }}>
        <div className="grid-2">
          <div className="field">
            <label htmlFor="username">Tên đăng nhập</label>
            <input id="username" value={user.username} disabled />
          </div>
          <div className="field">
            <label htmlFor="role">Vai trò</label>
            <input id="role" value={ROLE_LABEL[p.role] ?? p.role ?? ""} disabled />
          </div>
        </div>

        <div className="field">
          <label htmlFor="email">Email</label>
          <input id="email" name="email" type="email" autoComplete="email" value={form.email} onChange={update} />
        </div>

        <div className="grid-2">
          <div className="field">
            <label htmlFor="target_band">Band mục tiêu</label>
            <select id="target_band" name="target_band" value={form.target_band} onChange={update}>
              <option value="">Chưa đặt</option>
              {BANDS.map((b) => <option key={b} value={b}>{b}</option>)}
            </select>
          </div>
          <div className="field">
            <label htmlFor="exam_date">Ngày thi dự kiến</label>
            <input id="exam_date" name="exam_date" type="date" min={todayStr} value={form.exam_date} onChange={update} />
            {days != null && (
              <span className="muted small">{days >= 0 ? `Còn ${days} ngày` : "Ngày này đã qua"}</span>
            )}
          </div>
        </div>

        <div className="field">
          <span id="minutes-label" className="small" style={{ fontWeight: 500 }}>Thời gian học mỗi ngày</span>
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
                {m} phút
              </button>
            ))}
          </div>
        </div>

        <ErrorAlert>{error}</ErrorAlert>

        <div className="editor-bar">
          {saved && (
            <span role="status" className="small" style={{ display: "inline-flex", gap: 6, alignItems: "center" }}>
              <CheckCircle size={18} /> Đã lưu
            </span>
          )}
          <span className="spacer" />
          <button className="btn" disabled={busy}>
            {busy ? <CircleNotch size={18} className="spin" /> : <FloppyDisk size={18} />}
            {welcome ? "Lưu và bắt đầu" : "Lưu thay đổi"}
          </button>
        </div>
      </form>

      <ChangePassword />
    </div>
  );
}
