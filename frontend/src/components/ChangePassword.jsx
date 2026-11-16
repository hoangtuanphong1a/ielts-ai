import { useState } from "react";
import { CheckCircle, CircleNotch, LockKey } from "@phosphor-icons/react";
import { api, errorText } from "../api.js";
import { ErrorAlert } from "./ui.jsx";

const EMPTY = { old_password: "", new_password: "", confirm: "" };

// Đổi mật khẩu khi đã đăng nhập (AUTH-06), đặt trong trang Hồ sơ
export default function ChangePassword() {
  const [form, setForm] = useState(EMPTY);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [done, setDone] = useState(false);

  const update = (e) => {
    setDone(false);
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  async function onSubmit(e) {
    e.preventDefault();
    setError("");
    if (form.new_password !== form.confirm) {
      setError("Hai mật khẩu mới chưa khớp.");
      return;
    }
    setBusy(true);
    try {
      await api("/auth/password/change/", {
        method: "POST",
        body: { old_password: form.old_password, new_password: form.new_password },
      });
      setForm(EMPTY);
      setDone(true);
    } catch (err) {
      setError(errorText(err));
    } finally {
      setBusy(false);
    }
  }

  return (
    <form className="card" onSubmit={onSubmit} style={{ display: "grid", gap: "1.25rem" }}>
      <h2>Đổi mật khẩu</h2>
      <div className="field">
        <label htmlFor="old_password">Mật khẩu hiện tại</label>
        <input id="old_password" name="old_password" type="password" autoComplete="current-password"
               required value={form.old_password} onChange={update} />
      </div>
      <div className="grid-2">
        <div className="field">
          <label htmlFor="new_password">Mật khẩu mới</label>
          <input id="new_password" name="new_password" type="password" autoComplete="new-password"
                 required value={form.new_password} onChange={update} />
        </div>
        <div className="field">
          <label htmlFor="confirm_password">Nhập lại mật khẩu mới</label>
          <input id="confirm_password" name="confirm" type="password" autoComplete="new-password"
                 required value={form.confirm} onChange={update} />
        </div>
      </div>
      <ErrorAlert>{error}</ErrorAlert>
      <div className="editor-bar">
        {done && (
          <span role="status" className="small" style={{ display: "inline-flex", gap: 6, alignItems: "center" }}>
            <CheckCircle size={18} /> Đã đổi mật khẩu
          </span>
        )}
        <span className="spacer" />
        <button className="btn" disabled={busy}>
          {busy ? <CircleNotch size={18} className="spin" /> : <LockKey size={18} />}
          Đổi mật khẩu
        </button>
      </div>
    </form>
  );
}
