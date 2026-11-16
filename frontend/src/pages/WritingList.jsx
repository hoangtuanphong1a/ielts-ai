import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowRight, MagnifyingGlass } from "@phosphor-icons/react";
import { api, errorText } from "../api.js";
import { EmptyState, ErrorAlert, PageSkeleton } from "../components/ui.jsx";

const FILTERS = [
  { key: "all", label: "Tất cả" },
  { key: "task1", label: "Task 1" },
  { key: "task2", label: "Task 2" },
];
const TASK_LABEL = { task1: "Task 1 · 20 phút", task2: "Task 2 · 40 phút" };

export default function WritingList() {
  const [prompts, setPrompts] = useState(null);
  const [filter, setFilter] = useState("all");
  const [error, setError] = useState("");

  useEffect(() => {
    api("/writing/prompts/").then(setPrompts).catch((e) => setError(errorText(e)));
  }, []);

  if (error) return <ErrorAlert>{error}</ErrorAlert>;
  if (!prompts) return <PageSkeleton blocks={2} />;

  const shown = filter === "all" ? prompts : prompts.filter((p) => p.task_type === filter);

  return (
    <div className="page">
      <div className="page-head">
        <h1>Chọn đề Writing</h1>
        <p className="muted">Viết xong bấm nộp, hệ thống chấm ngay.</p>
      </div>

      <div className="chips" role="group" aria-label="Lọc theo task">
        {FILTERS.map((f) => (
          <button key={f.key} className="chip" aria-pressed={filter === f.key} onClick={() => setFilter(f.key)}>
            {f.label}
          </button>
        ))}
      </div>

      {shown.length === 0 ? (
        <div className="card">
          <EmptyState icon={<MagnifyingGlass size={28} />} title="Chưa có đề nào">
            Thử chọn bộ lọc khác.
          </EmptyState>
        </div>
      ) : (
        <div className="grid-2">
          {shown.map((p) => (
            <Link key={p.id} to={`/writing/${p.id}`} className="card prompt-card">
              <span className="tag" style={{ alignSelf: "flex-start" }}>{TASK_LABEL[p.task_type]}</span>
              <h2>{p.title}</h2>
              <p className="muted clamp-3">{p.prompt_text}</p>
              <span className="go">Bắt đầu viết <ArrowRight size={16} /></span>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
