import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowRight } from "@phosphor-icons/react";
import { api, errorText } from "../api.js";
import { useAuth } from "../auth.jsx";
import BandBar from "../components/BandBar.jsx";
import { TodayPlan, Weaknesses } from "../components/Coach.jsx";
import { CountUp, JourneyTrack } from "../components/Journey.jsx";
import { ErrorAlert, PageSkeleton } from "../components/ui.jsx";
import { daysUntil } from "./Profile.jsx";


const fmt = (v) => (v == null ? "-" : Number(v).toFixed(1));

const CRITERIA = [
  { key: "task_response", label: "Task Response" },
  { key: "coherence", label: "Coherence & Cohesion" },
  { key: "lexical", label: "Lexical Resource" },
  { key: "grammar", label: "Grammatical Range" },
];

export default function Dashboard() {
  const { user } = useAuth();
  const [data, setData] = useState(null);
  const [coach, setCoach] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    // Tiến độ + bộ máy cá nhân hoá (điểm yếu, kế hoạch hôm nay) tải song song
    Promise.all([api("/writing/progress/"), api("/coach/today/")])
      .then(([progress, today]) => { setData(progress); setCoach(today); })
      .catch((e) => setError(errorText(e)));
  }, []);

  if (error) return <ErrorAlert>{error}</ErrorAlert>;
  if (!data || !coach) return <PageSkeleton blocks={3} />;

  const { averages: avg, history, count } = data;
  const recent = [...history].reverse().slice(0, 6);
  const target = user.profile?.target_band;
  const days = daysUntil(user.profile?.exam_date);
  const current = count > 0 ? avg.overall : null;
  const gap = target != null && current != null ? target - current : null;

  // Tiêu chí cần tập trung = tiêu chí của điểm yếu số 1 (coach/weakness.py)
  const focusCriterion = coach.weaknesses[0]?.criterion;

  return (
    <div className="page">
      <div className="page-head">
        <h1>Welcome back, {user.username}</h1>
        <p className="muted">
          {target != null
            ? <>Target band {fmt(target)}{days != null && days >= 0 ? `, ${days} days until your exam.` : "."}</>
            : <>No target yet. <Link to="/profile">Set your target band</Link> to personalise your plan.</>}
        </p>
      </div>


      <div className="bento">
        <section className="card journey-card span-12" aria-labelledby="journey-title">
          <div className="journey-head">
            <div>
              <h2 id="journey-title" className="muted small">Your Writing band</h2>
              <p className="band-big num">
                {current != null ? <CountUp value={current} /> : "-"}
                {target != null && <span className="band-target"> / {fmt(target)}</span>}
              </p>
              <p className="muted small">
                {current == null
                  ? "Submit your first essay to place yourself on the journey."
                  : gap > 0
                    ? `${fmt(gap)} band to go. Keep going.`
                    : target != null ? "Target reached. Time to aim higher." : "Set a target to see how far you have to go."}
              </p>
            </div>
            <Link to="/writing" className="btn">
              {count === 0 ? "Write your first essay" : "New essay"} <ArrowRight size={18} />
            </Link>
          </div>
          <JourneyTrack current={current} target={target} />
        </section>

        <section className="card today span-5" aria-labelledby="today-title">
          <TodayPlan plan={coach.plan} />
        </section>

        {count > 0 && (
          <section className="card span-7" aria-labelledby="weak-title">
            <Weaknesses weaknesses={coach.weaknesses} analysed={coach.essays_analysed} />
          </section>
        )}

        {count > 0 ? (
          <section className="card span-7" aria-labelledby="criteria-title">
            <h2 id="criteria-title" style={{ marginBottom: "1rem" }}>By criterion</h2>
            {CRITERIA.map((c) => (
              <BandBar key={c.key} label={c.label} value={avg[c.key]} focus={focusCriterion === c.key} />
            ))}
          </section>
        ) : (
          <section className="card span-7" aria-labelledby="how-title">
            <h2 id="how-title" style={{ marginBottom: "0.5rem" }}>How your plan adapts</h2>
            <p className="muted">
              Every essay is scored on the four IELTS criteria and checked for grammar, vocabulary and
              topic focus. Your repeated mistakes become today&apos;s practice, so the more you write,
              the more personal your plan gets.
            </p>
          </section>
        )}

        {count > 0 && (
          <section className="card span-5" aria-labelledby="recent-title">
            <div className="card-head">
              <h2 id="recent-title">Recent essays</h2>
              <Link to="/writing" className="small">All prompts</Link>
            </div>
            <ul className="rows">
              {recent.map((h) => (
                <li key={h.id}>
                  <Link to={`/submissions/${h.id}`}>
                    <span className="muted num">{h.date}</span>
                    <strong className="num">{fmt(h.band)}</strong>
                  </Link>
                </li>
              ))}
            </ul>
          </section>
        )}
      </div>
    </div>
  );
}
