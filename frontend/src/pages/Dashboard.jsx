import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowRight, PencilLine } from "@phosphor-icons/react";
import { api, errorText } from "../api.js";
import { useAuth } from "../auth.jsx";
import BandBar from "../components/BandBar.jsx";
import { EmptyState, ErrorAlert, PageSkeleton } from "../components/ui.jsx";
import { daysUntil } from "./Profile.jsx";

const fmt = (v) => (v == null ? "-" : Number(v).toFixed(1));

export default function Dashboard() {
  const { user } = useAuth();
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api("/writing/progress/").then(setData).catch((e) => setError(errorText(e)));
  }, []);

  if (error) return <ErrorAlert>{error}</ErrorAlert>;
  if (!data) return <PageSkeleton blocks={3} />;

  const { averages: avg, history, count } = data;
  const latest = history.at(-1);
  const recent = [...history].reverse().slice(0, 6);
  const target = user.profile?.target_band;
  const days = daysUntil(user.profile?.exam_date);
  const gap = target != null && avg.overall != null ? target - avg.overall : null;

  return (
    <div className="page">
      <div className="page-head">
        <h1>Chào {user.username}</h1>
        {target != null ? (
          <p className="muted">
            Mục tiêu band {fmt(target)}
            {days != null && days >= 0 ? `, còn ${days} ngày tới ngày thi.` : "."}
          </p>
        ) : (
          <p className="muted">
            Bạn chưa đặt mục tiêu. <Link to="/profile">Đặt band mục tiêu</Link> để lộ trình sát hơn.
          </p>
        )}
      </div>

      {count === 0 ? (
        <div className="card">
          <EmptyState
            icon={<PencilLine size={28} />}
            title="Chưa có bài nào"
            action={<Link to="/writing" className="btn">Viết bài đầu tiên <ArrowRight size={18} /></Link>}
          >
            Nộp một bài Writing để hệ thống ước lượng band và chỉ ra điểm cần cải thiện.
          </EmptyState>
        </div>
      ) : (
        <div className="bento">
          <section className="band-hero span-7 wide" aria-label="Band trung bình">
            <div>
              <p className="muted small">Band Writing trung bình</p>
              <p className="band-big num">{fmt(avg.overall)}</p>
              {gap != null && (
                <p className="muted small" style={{ marginTop: "0.5rem" }}>
                  {gap > 0 ? `Cần thêm ${fmt(gap)} để đạt mục tiêu ${fmt(target)}` : `Đã đạt mục tiêu ${fmt(target)}`}
                </p>
              )}
            </div>
            <Link to="/writing" className="btn btn-hero">
              Viết bài mới <ArrowRight size={18} />
            </Link>
          </section>

          <div className="stat-stack span-5 wide">
            <div className="card stat">
              <span className="muted small">Bài đã nộp</span>
              <strong className="num">{count}</strong>
            </div>
            <div className="card stat">
              <span className="muted small">Bài gần nhất</span>
              <strong className="num">{fmt(latest?.band)}</strong>
            </div>
            <div className="card stat">
              <span className="muted small">Ngày gần nhất</span>
              <strong className="num" style={{ fontSize: "1.25rem" }}>{latest?.date ?? "-"}</strong>
            </div>
          </div>

            <section className="card span-7" aria-labelledby="criteria-title">
              <h2 id="criteria-title" style={{ marginBottom: "1rem" }}>Theo tiêu chí</h2>
              <BandBar label="Task Response" value={avg.task_response} />
              <BandBar label="Coherence & Cohesion" value={avg.coherence} />
              <BandBar label="Lexical Resource" value={avg.lexical} />
              <BandBar label="Grammatical Range" value={avg.grammar} />
            </section>

            <section className="card span-5" aria-labelledby="recent-title">
              <div className="card-head">
                <h2 id="recent-title">Bài gần đây</h2>
                <Link to="/writing" className="small">Tất cả đề</Link>
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
        </div>
      )}
    </div>
  );
}
