import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { CircleNotch, Eye, EyeSlash, Infinity as InfinityIcon } from "@phosphor-icons/react";
import { useAuth } from "../auth.jsx";
import { errorText } from "../api.js";
import { ErrorAlert } from "../components/ui.jsx";

export default function Login() {
  const { user, login, register } = useAuth();
  const navigate = useNavigate();
  const [mode, setMode] = useState("login");
  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  if (user) return <Navigate to="/" replace />;

  const isLogin = mode === "login";
  const update = (e) => setForm({ ...form, [e.target.name]: e.target.value });
  const switchMode = () => {
    setMode(isLogin ? "register" : "login");
    setError("");
  };

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
      setError(err.status === 401 ? "Incorrect username or password." : errorText(err));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="login-shell">
      <div className="login-card">
        {/* Cột trái: dải màu từ bảng 5 màu + lời giới thiệu (ẩn trên mobile) */}
        <aside className="login-visual" aria-hidden="true">
          <span className="login-visual-mark"><InfinityIcon size={30} weight="bold" /></span>
          <div className="login-visual-copy">
            <p className="login-visual-eyebrow">Personalised IELTS preparation</p>
            <p className="login-visual-title">Your own path to the band you need</p>
          </div>
        </aside>

        <main className="login-main">
          <form className="login-form" onSubmit={onSubmit}>
            <span className="login-mark"><InfinityIcon size={26} weight="bold" /></span>
            <div className="login-head">
              <h1>{isLogin ? "Welcome back" : "Create an account"}</h1>
              <p className="muted">
                {isLogin
                  ? "Log in to continue your band journey."
                  : "Set a target band and get a study plan that adapts to every essay you write."}
              </p>
            </div>

            <div className="field">
              <label htmlFor="username">Username</label>
              <input id="username" name="username" autoComplete="username" required
                     value={form.username} onChange={update} />
            </div>

            {!isLogin && (
              <div className="field">
                <label htmlFor="email">Email</label>
                <input id="email" name="email" type="email" autoComplete="email"
                       value={form.email} onChange={update} />
              </div>
            )}

            <div className="field">
              <label htmlFor="password">Password</label>
              <div className="input-wrap">
                <input id="password" name="password" required
                       type={showPassword ? "text" : "password"}
                       autoComplete={isLogin ? "current-password" : "new-password"}
                       value={form.password} onChange={update} />
                <button type="button" className="input-icon" onClick={() => setShowPassword(!showPassword)}
                        aria-label={showPassword ? "Hide password" : "Show password"}>
                  {showPassword ? <EyeSlash size={18} /> : <Eye size={18} />}
                </button>
              </div>
              {isLogin
                ? <Link to="/forgot-password" className="small login-forgot">Forgot password?</Link>
                : <span className="muted small">At least 8 characters. Avoid common passwords.</span>}
            </div>

            <ErrorAlert>{error}</ErrorAlert>

            <button className="btn btn-block" disabled={busy}>
              {busy && <CircleNotch size={18} className="spin" />}
              {busy ? "Please wait" : isLogin ? "Log in" : "Get started"}
            </button>

            <p className="login-switch small">
              {isLogin ? "Don't have an account? " : "Already have an account? "}
              <button type="button" className="link-btn" onClick={switchMode}>
                {isLogin ? "Sign up" : "Log in"}
              </button>
            </p>

            <p className="muted small login-note">Scores are estimates, not official IELTS results.</p>
          </form>
        </main>
      </div>
    </div>
  );
}
