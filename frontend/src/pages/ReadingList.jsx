import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowRight, BookOpen } from "@phosphor-icons/react";
import { api, errorText } from "../api.js";
import { EmptyState, ErrorAlert, PageSkeleton } from "../components/ui.jsx";

const LEVEL = { 1: "Easier", 2: "Medium", 3: "Harder" };

export default function ReadingList() {
  const [passages, setPassages] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api("/reading/passages/").then(setPassages).catch((e) => setError(errorText(e)));
  }, []);

  if (error) return <ErrorAlert>{error}</ErrorAlert>;
  if (!passages) return <PageSkeleton blocks={2} />;

  return (
    <div className="page">
      <div className="page-head">
        <h1>Reading practice</h1>
        <p className="muted">One passage, IELTS question types, a timer, and instant marking with explanations.</p>
      </div>
      {passages.length === 0 ? (
        <div className="card">
          <EmptyState icon={<BookOpen size={28} />} title="No passages yet">Ask an admin to add reading passages.</EmptyState>
        </div>
      ) : (
        <div className="grid-2">
          {passages.map((p) => (
            <Link key={p.id} to={`/reading/${p.id}`} className="card prompt-card">
              <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                <span className="tag">{p.topic}</span>
                <span className="tag">{LEVEL[p.difficulty]}</span>
                <span className="tag num">{p.minutes} min · {p.question_count} questions</span>
              </div>
              <h2>{p.title}</h2>
              <p className="muted small">
                {p.attempt_count
                  ? `Best band ${Number(p.best_band).toFixed(1)} from ${p.attempt_count} attempt${p.attempt_count > 1 ? "s" : ""}.`
                  : "Not attempted yet."}
              </p>
              <span className="go">{p.attempt_count ? "Try again" : "Start reading"} <ArrowRight size={16} /></span>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
