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
      setError("Hai mật khẩu chưa khớp.");
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
            <h1>Đặt mật khẩu mới</h1>
          </div>

          {done ? (
            <>
              <div className="alert" role="status">
                <CheckCircle size={20} />
                <span>Đã đổi mật khẩu. Bạn có thể đăng nhập bằng mật khẩu mới.</span>
              </div>
              <Link to="/login" className="btn btn-block">Đăng nhập</Link>
            </>
          ) : broken ? (
            <>
              <ErrorAlert>Link không hợp lệ. Hãy mở đúng link trong email hoặc yêu cầu link mới.</ErrorAlert>
              <Link to="/forgot-password" className="btn btn-block">Yêu cầu link mới</Link>
            </>
          ) : (
            <>
              <div className="field">
                <label htmlFor="password">Mật khẩu mới</label>
                <input id="password" type="password" autoComplete="new-password" required
                       value={password} onChange={(e) => setPassword(e.target.value)} />
                <span className="muted small">Tối thiểu 8 ký tự, không dùng mật khẩu quá phổ biến.</span>
              </div>
              <div className="field">
                <label htmlFor="confirm">Nhập lại mật khẩu</label>
                <input id="confirm" type="password" autoComplete="new-password" required
                       value={confirm} onChange={(e) => setConfirm(e.target.value)} />
              </div>
              <ErrorAlert>{error}</ErrorAlert>
              <button className="btn btn-block" disabled={busy}>
                {busy && <CircleNotch size={18} className="spin" />}
                {busy ? "Đang lưu" : "Lưu mật khẩu mới"}
              </button>
              {error && <Link to="/forgot-password" className="small">Yêu cầu link mới</Link>}
            </>
          )}
        </form>
      </main>
    </div>
  );
}
