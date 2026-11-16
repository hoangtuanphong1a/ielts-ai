import { useEffect, useRef } from "react";
import { Flag } from "@phosphor-icons/react";

const MIN = 4;
const MAX = 9;
const TICKS = [4, 5, 6, 7, 8, 9];
const pct = (band) => ((Math.min(MAX, Math.max(MIN, band)) - MIN) / (MAX - MIN)) * 100;

const reduceMotion = () =>
  typeof window !== "undefined" && window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;

/**
 * Số band đếm dần lên khi xuất hiện. Cập nhật textContent qua ref (không setState mỗi frame).
 */
export function CountUp({ value, decimals = 1, duration = 900, className }) {
  const ref = useRef(null);

  useEffect(() => {
    const el = ref.current;
    if (!el || value == null) return;
    if (reduceMotion()) {
      el.textContent = Number(value).toFixed(decimals);
      return;
    }
    let frame;
    const start = performance.now();
    const tick = (now) => {
      const t = Math.min(1, (now - start) / duration);
      const eased = 1 - Math.pow(1 - t, 3); // easeOutCubic
      el.textContent = (value * eased).toFixed(decimals);
      if (t < 1) frame = requestAnimationFrame(tick);
    };
    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  }, [value, decimals, duration]);

  return (
    <span ref={ref} className={className}>
      {value == null ? "-" : Number(0).toFixed(decimals)}
    </span>
  );
}

/**
 * Đường hành trình band (yếu tố nhận diện của app):
 * thang 4.0 - 9.0, đoạn đã đi (navy), đoạn còn lại tới mục tiêu (ocean nét đứt), cờ mục tiêu.
 */
export function JourneyTrack({ current, target, label = "Band journey" }) {
  const hasCurrent = current != null && current > 0;
  const hasTarget = target != null;
  const cur = hasCurrent ? pct(current) : 0;
  const tgt = hasTarget ? pct(target) : null;
  const reached = hasCurrent && hasTarget && current >= target;

  const desc = [
    hasCurrent ? `current ${Number(current).toFixed(1)}` : "no band yet",
    hasTarget ? `target ${Number(target).toFixed(1)}` : "no target set",
  ].join(", ");

  return (
    <div className="journey" role="img" aria-label={`${label}: ${desc}`}>
      <div className="journey-rail">
        <div className="journey-done" style={{ "--to": `${cur}%` }} />
        {hasTarget && hasCurrent && !reached && (
          <div className="journey-gap" style={{ left: `${cur}%`, width: `${tgt - cur}%` }} />
        )}
        {hasCurrent && (
          <div className="journey-marker" style={{ "--at": `${cur}%` }}>
            <span className="journey-dot" />
          </div>
        )}
        {hasTarget && (
          <div className={`journey-flag${reached ? " is-reached" : ""}`} style={{ left: `${tgt}%` }}>
            <Flag size={14} weight="fill" />
          </div>
        )}
      </div>
      <div className="journey-ticks" aria-hidden="true">
        {TICKS.map((t) => (
          <span key={t} style={{ left: `${pct(t)}%` }}>{t.toFixed(1)}</span>
        ))}
      </div>
    </div>
  );
}
