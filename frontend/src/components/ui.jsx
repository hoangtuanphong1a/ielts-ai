import { Infinity as InfinityIcon, WarningCircle } from "@phosphor-icons/react";
import { Link } from "react-router-dom";

export function Brand({ to = "/" }) {
  return (
    <Link to={to} className="brand" aria-label="IELTS AI home">
      <span className="brand-mark"><InfinityIcon size={22} weight="bold" /></span>
      <span className="brand-text">IELTS AI</span>
    </Link>
  );
}

// Thông báo lỗi: dùng icon + viền + chữ, không dựa vào màu (bảng màu không có đỏ)
export function ErrorAlert({ children }) {
  if (!children) return null;
  return (
    <div className="alert" role="alert">
      <WarningCircle size={20} weight="bold" />
      <span>{children}</span>
    </div>
  );
}

export function EmptyState({ icon, title, children, action }) {
  return (
    <div className="empty">
      <div className="empty-icon">{icon}</div>
      <h2>{title}</h2>
      {children && <p className="muted">{children}</p>}
      {action}
    </div>
  );
}

export function Skeleton({ h = 16, w = "100%", style }) {
  return <div className="skeleton" style={{ height: h, width: w, ...style }} aria-hidden="true" />;
}

// Khung chờ chung cho trang: tiêu đề + vài khối
export function PageSkeleton({ blocks = 2 }) {
  return (
    <div className="page" aria-busy="true" aria-label="Loading">
      <Skeleton h={32} w="40%" />
      {Array.from({ length: blocks }, (_, i) => (
        <Skeleton key={i} h={140} style={{ borderRadius: 14 }} />
      ))}
    </div>
  );
}
