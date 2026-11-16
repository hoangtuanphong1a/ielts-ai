import { useState } from "react";
import { Link } from "react-router-dom";
import { BookOpen, Cards, Clock, Crosshair, PencilLine, Target } from "@phosphor-icons/react";

const ICONS = { diagnostic: PencilLine, essay: PencilLine, paragraph: PencilLine, vocab: Cards, drill: Crosshair, reading: BookOpen };

// Bài tập "sửa lỗi của chính bạn": câu sai thật lấy từ bài đã chấm (coach/weakness.py)
function Drill({ examples }) {
  const [shown, setShown] = useState({});
  return (
    <ol className="drill">
      {examples.map((ex, i) => {
        const before = ex.sentence.slice(0, ex.start);
        const wrong = ex.sentence.slice(ex.start, ex.start + ex.length);
        const after = ex.sentence.slice(ex.start + ex.length);
        const open = shown[i];
        return (
          <li key={i}>
            <p>
              {before}
              {open ? <><del className="drill-wrong">{wrong}</del> <ins className="drill-fix">{ex.fix}</ins></> : wrong}
              {after}
            </p>
            <div className="drill-foot">
              {open
                ? <span className="muted small">{ex.message}</span>
                : <button type="button" className="link-btn small" onClick={() => setShown({ ...shown, [i]: true })}>
                    Show the fix
                  </button>}
              <Link to={`/submissions/${ex.submission}`} className="small">From your essay</Link>
            </div>
          </li>
        );
      })}
    </ol>
  );
}

export function TodayPlan({ plan }) {
  const [drillOpen, setDrillOpen] = useState(false);
  return (
    <>
      <div className="card-head" style={{ marginBottom: "1rem" }}>
        <h2 id="today-title">Today</h2>
        <span className="muted small num" style={{ display: "inline-flex", alignItems: "center", gap: 6 }}>
          <Clock size={16} aria-hidden="true" /> {plan.minutes} / {plan.budget} min
        </span>
      </div>
      <ul className="today-list">
        {plan.items.map((item) => {
          const Icon = ICONS[item.kind] || Target;
          const link = item.prompt ? `/writing/${item.prompt.id}`
            : item.passage ? `/reading/${item.passage.id}`
            : item.kind === "vocab" ? "/vocab" : null;
          return (
            <li key={item.kind}>
              <span className="today-icon"><Icon size={20} /></span>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div className="today-row">
                  {item.kind === "drill"
                    ? <button type="button" className="link-btn" aria-expanded={drillOpen} onClick={() => setDrillOpen(!drillOpen)}>{item.title}</button>
                    : link ? <Link to={link}>{item.title}</Link> : <strong>{item.title}</strong>}
                  <span className="muted small num">{item.minutes} min</span>
                </div>
                <p className="muted small">{item.detail}</p>
                {item.prompt && item.kind !== "drill" && <p className="small">{item.prompt.title}</p>}
                {item.passage && <p className="small">{item.passage.title}</p>}
                {item.kind === "drill" && drillOpen && <Drill examples={item.examples} />}
              </div>
            </li>
          );
        })}
      </ul>
    </>
  );
}

export function Weaknesses({ weaknesses, analysed }) {
  return (
    <>
      <div className="card-head" style={{ marginBottom: "1rem" }}>
        <h2 id="weak-title">Your top weaknesses</h2>
        <span className="muted small">From your last {analysed} essay{analysed > 1 ? "s" : ""}</span>
      </div>
      {weaknesses.length === 0
        ? <p className="muted">No clear weakness yet. Keep writing and we will spot patterns.</p>
        : (
          <ol className="weak-list">
            {weaknesses.map((w, i) => (
              <li key={w.key}>
                <span className="weak-rank num">{i + 1}</span>
                <div>
                  <p className="weak-title"><strong>{w.title}</strong> <span className="tag">{w.criterion_label}</span></p>
                  <p className="small">{w.evidence}</p>
                  <p className="muted small">{w.tip}</p>
                </div>
              </li>
            ))}
          </ol>
        )}
    </>
  );
}
