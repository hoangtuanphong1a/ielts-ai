// Thanh ngang thể hiện band 0-9. focus = tiêu chí cần tập trung (thấp nhất)
export default function BandBar({ label, value, focus = false }) {
  const pct = Math.max(0, Math.min(100, ((value ?? 0) / 9) * 100));
  return (
    <div className={`bandbar${focus ? " is-focus" : ""}`}>
      <div className="bandbar-head">
        <span>
          {label}
          {focus && <span className="tag" style={{ marginLeft: 8 }}>Focus</span>}
        </span>
        <strong className="num">{value != null ? Number(value).toFixed(1) : "-"}</strong>
      </div>
      <div className="bandbar-track" role="progressbar" aria-label={label}
           aria-valuemin={0} aria-valuemax={9} aria-valuenow={value ?? 0}>
        <div className="bandbar-fill" style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}
