// T3.4: lịch học tuần này. Ngày đã qua = việc đã làm thật; hôm nay + ngày tới = kế hoạch.
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { BookOpen, Cards, CheckCircle, Crosshair, PencilLine, Target } from "@phosphor-icons/react";
import { api, errorText } from "../api.js";
import { ErrorAlert, PageSkeleton } from "../components/ui.jsx";

const ICONS = { diagnostic: PencilLine, essay: PencilLine, paragraph: PencilLine, vocab: Cards, drill: Crosshair, reading: BookOpen };

const linkFor = (item) => (item.prompt ? `/writing/${item.prompt.id}`
  : item.passage ? `/reading/${item.passage.id}`
  : item.kind === "vocab" ? "/vocab" : null);

function doneText(done) {
  const parts = [];
  if (done.essays) parts.push(`${done.essays} essay${done.essays > 1 ? "s" : ""}`);
  if (done.readings) parts.push(`${done.readings} reading${done.readings > 1 ? "s" : ""}`);
  if (done.cards) parts.push(`${done.cards} card${done.cards > 1 ? "s" : ""}`);
  return parts.join(" · ");
}

function Day({ day, budget }) {
  const date = new Date(`${day.date}T00:00:00`);
  const light = !day.is_past && day.items.length > 0 && day.minutes < budget / 2;
  return (
    <li className={`card plan-day${day.is_today ? " is-today" : ""}${day.is_past ? " is-past" : ""}`}
        aria-current={day.is_today ? "date" : undefined}>
      <div className="plan-day-head">
        <div>
          <strong>{day.weekday}</strong> <span className="muted num">{date.getDate()}</span>
        </div>
        {day.is_today ? <span className="tag">Today</span>
          : !day.is_past && <span className="muted small num">{day.minutes} min</span>}
      </div>

      {day.done && (
        <p className="small plan-done">
          {doneText(day.done)
            ? <><CheckCircle size={16} weight="fill" aria-hidden="true" /> {doneText(day.done)}</>
            : <span className="muted">{day.is_past ? "No practice recorded" : "Nothing done yet"}</span>}
        </p>
      )}

      {day.items.length > 0 && (
        <ul className="plan-items">
          {day.items.map((item, i) => {
            const Icon = ICONS[item.kind] || Target;
            const to = linkFor(item);
            return (
              <li key={i}>
                <Icon size={18} aria-hidden="true" />
                <div>
                  {to ? <Link to={to}>{item.title}</Link> : <span>{item.title}</span>}
                  <span className="muted small num"> · {item.minutes} min</span>
                  {item.detail && <p className="muted small clamp-2">{item.detail}</p>}
                </div>
              </li>
            );
          })}
        </ul>
      )}
      {light && <p className="muted small">Light day. Rest or revisit a passage you found hard.</p>}
    </li>
  );
}

export default function StudyPlan() {
  const [week, setWeek] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api("/coach/week/").then(setWeek).catch((e) => setError(errorText(e)));
  }, []);

  if (error) return <ErrorAlert>{error}</ErrorAlert>;
  if (!week) return <PageSkeleton blocks={2} />;

  const planned = week.days.filter((d) => !d.is_past).reduce((n, d) => n + d.minutes, 0);
  const focus = week.weaknesses.map((w) => w.title.toLowerCase());

  return (
    <div className="page">
      <div className="page-head">
        <h1>Your week</h1>
        <p className="muted">
          {planned} minutes planned for the rest of the week, up to {week.budget} a day.
          {focus.length > 0 && <> Each day rotates through your focus areas: {focus.join(", ")}.</>}
        </p>
      </div>
      <ol className="plan-week">
        {week.days.map((d) => <Day key={d.date} day={d} budget={week.budget} />)}
      </ol>
      <p className="muted small">
        The plan updates as you practise: finished days show what you actually did, and new essays or
        readings change your focus areas. <Link to="/profile">Change your daily minutes</Link>.
      </p>
    </div>
  );
}
