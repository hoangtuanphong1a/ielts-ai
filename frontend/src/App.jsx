import { Navigate, NavLink, Route, Routes } from "react-router-dom";
import { BookOpen, Cards, House, PencilLine, SignOut, UserCircle } from "@phosphor-icons/react";
import { useAuth } from "./auth.jsx";
import { Brand, PageSkeleton } from "./components/ui.jsx";
import Login from "./pages/Login.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import WritingList from "./pages/WritingList.jsx";
import WritingEditor from "./pages/WritingEditor.jsx";
import SubmissionResult from "./pages/SubmissionResult.jsx";
import Vocab from "./pages/Vocab.jsx";
import ReadingList from "./pages/ReadingList.jsx";
import ReadingTest from "./pages/ReadingTest.jsx";
import ReadingResult from "./pages/ReadingResult.jsx";
import StudyPlan from "./pages/StudyPlan.jsx";
import Profile from "./pages/Profile.jsx";
import ForgotPassword from "./pages/ForgotPassword.jsx";
import ResetPassword from "./pages/ResetPassword.jsx";

const NAV = [
  { to: "/", label: "Dashboard", icon: House, end: true },
  { to: "/writing", label: "Writing", icon: PencilLine },
  { to: "/reading", label: "Reading", icon: BookOpen },
  { to: "/vocab", label: "Vocabulary", icon: Cards },
  { to: "/profile", label: "Profile", icon: UserCircle },
];

const ROLE_LABEL = { student: "Student", teacher: "Teacher", admin: "Admin" };

function NavItems() {
  return NAV.map(({ to, label, icon: Icon, end }) => (
    <NavLink key={to} to={to} end={end} title={label} aria-label={label}>
      <Icon size={22} />
      <span className="label">{label}</span>
    </NavLink>
  ));
}

function LogoutButton() {
  const { logout } = useAuth();
  return (
    <button className="icon-btn" onClick={logout} aria-label="Log out" title="Log out">
      <SignOut size={18} />
    </button>
  );
}

function Shell({ children }) {
  const { user } = useAuth();
  return (
    <div className="layout">
      <aside className="sidebar">
        <Brand />
        <nav className="side-nav" aria-label="Main navigation"><NavItems /></nav>
        <div className="side-foot">
          <span className="avatar" aria-hidden="true">{user.username.slice(0, 1)}</span>
          <div className="who small">
            <strong>{user.username}</strong>
            <span className="muted">{ROLE_LABEL[user.profile?.role] ?? "Student"}</span>
          </div>
          <LogoutButton />
        </div>
      </aside>

      <div className="main">
        <header className="mobile-bar">
          <Brand />
          <LogoutButton />
        </header>
        <main className="container">{children}</main>
        <nav className="tabbar" aria-label="Main navigation"><NavItems /></nav>
      </div>
    </div>
  );
}

function Protected({ children }) {
  const { user, loading } = useAuth();
  if (loading) return <main className="container"><PageSkeleton /></main>;
  return user ? <Shell>{children}</Shell> : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <>
      <div className="app-bg" aria-hidden="true" />
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="/" element={<Protected><Dashboard /></Protected>} />
        <Route path="/writing" element={<Protected><WritingList /></Protected>} />
        <Route path="/writing/:promptId" element={<Protected><WritingEditor /></Protected>} />
        <Route path="/submissions/:id" element={<Protected><SubmissionResult /></Protected>} />
        <Route path="/reading" element={<Protected><ReadingList /></Protected>} />
        <Route path="/reading/:id" element={<Protected><ReadingTest /></Protected>} />
        <Route path="/reading/attempts/:id" element={<Protected><ReadingResult /></Protected>} />
        <Route path="/plan" element={<Protected><StudyPlan /></Protected>} />
        <Route path="/vocab" element={<Protected><Vocab /></Protected>} />
        <Route path="/profile" element={<Protected><Profile /></Protected>} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </>
  );
}
