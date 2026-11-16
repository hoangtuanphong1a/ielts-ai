import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { CircleNotch, Cards, ChartLineUp, PencilLine } from "@phosphor-icons/react";
import { useAuth } from "../auth.jsx";
import { errorText } from "../api.js";
import { Brand, ErrorAlert } from "../components/ui.jsx";

const POINTS = [
  { icon: PencilLine, text: "Viết Task 1 và Task 2, nhận band ước lượng theo 4 tiêu chí." },
  { icon: Cards, text: "Ôn từ vựng học thuật mỗi ngày bằng lặp lại ngắt quãng." },
  { icon: ChartLineUp, text: "Theo dõi band qua từng bài để biết mình đang tiến bộ ở đâu." },
];

export default function Login() {
  const { user, login, register } = useAuth();
  const navigate = useNavigate();
  const [mode, setMode] = useState("login");
  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  if (user) return <Navigate to="/" replace />;

  const update = (e) => setForm({ ...form, [e.target.name]: e.target.value });
  const isLogin = mode === "login";

  async function onSubmit(e) {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      if (isLogin) await login(form.username, form.password);
      else await register(form.username, form.email, form.password);
      // Tài khoản mới -> đặt mục tiêu trước (onboarding AUTH-09)
      navigate(isLogin ? "/" : "/profile?welcome=1");
    } catch (err) {
      setError(err.status === 401 ? "Sai tên đăng nhập hoặc mật khẩu." : errorText(err));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="auth">
      <aside className="auth-aside">
        <Brand />
        <div>
          <h1>Viết xong là biết band ngay</h1>
          <ul className="auth-points">
            {POINTS.map(({ icon: Icon, text }) => (
              <li key={text}><Icon size={22} />{text}</li>
            ))}
          </ul>
        </div>
        <p className="small" style={{ opacity: 0.8 }}>Điểm do hệ thống chấm là ước lượng, không phải điểm thi chính thức.</p>
      </aside>

      <main className="auth-main">
        <form className="auth-form card" onSubmit={onSubmit} noValidate={false}>
          <Brand />
          <div className="segmented" role="tablist" aria-label="Chọn chế độ">
            <button type="button" role="tab" aria-selected={isLogin} onClick={() => { setMode("login"); setError(""); }}>
              Đăng nhập
            </button>
            <button type="button" role="tab" aria-selected={!isLogin} onClick={() => { setMode("register"); setError(""); }}>
              Tạo tài khoản
            </button>
          </div>

          <div className="page-head">
            <h1>{isLogin ? "Chào mừng quay lại" : "Bắt đầu luyện thi"}</h1>
            <p className="muted">{isLogin ? "Đăng nhập để tiếp tục bài đang học." : "Chỉ mất 30 giây để tạo tài khoản."}</p>
          </div>

          <div className="field">
            <label htmlFor="username">Tên đăng nhập</label>
            <input id="username" name="username" autoComplete="username" value={form.username} onChange={update} required />
          </div>
          {!isLogin && (
            <div className="field">
              <label htmlFor="email">Email</label>
              <input id="email" name="email" type="email" autoComplete="email" value={form.email} onChange={update} />
            </div>
          )}
          <div className="field">
            <label htmlFor="password">Mật khẩu</label>
            <input id="password" name="password" type="password" value={form.password} onChange={update} required
                   autoComplete={isLogin ? "current-password" : "new-password"} />
            {!isLogin && <span className="muted small">Tối thiểu 8 ký tự, không dùng mật khẩu quá phổ biến.</span>}
            {isLogin && <Link to="/forgot-password" className="small" style={{ justifySelf: "end", alignSelf: "flex-end" }}>Quên mật khẩu?</Link>}
          </div>

          <ErrorAlert>{error}</ErrorAlert>

          <button className="btn btn-block" disabled={busy}>
            {busy && <CircleNotch size={18} className="spin" />}
            {busy ? "Đang xử lý" : isLogin ? "Đăng nhập" : "Tạo tài khoản"}
          </button>
        </form>
      </main>
    </div>
  );
}
