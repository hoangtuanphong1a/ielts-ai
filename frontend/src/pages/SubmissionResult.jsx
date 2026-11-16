import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { ArrowCounterClockwise, Lightbulb } from "@phosphor-icons/react";
import { api, errorText } from "../api.js";
import { ErrorAlert, PageSkeleton } from "../components/ui.jsx";

const CRITERIA = [
  ["band_task_response", "Task Response"],
  ["band_coherence", "Coherence & Cohesion"],
  ["band_lexical", "Lexical Resource"],
  ["band_grammar", "Grammatical Range"],
];

// Tên tiếng Việt cho chỉ số NLP trả về từ backend (ml/features.py)
const METRIC_LABELS = {
  word_count: "Số từ",
  sentence_count: "Số câu",
  paragraph_count: "Số đoạn",
  avg_sentence_len: "Độ dài câu TB",
  guiraud_index: "Đa dạng từ vựng",
  long_word_ratio: "Tỉ lệ từ dài",
  linker_count: "Số từ nối",
  linker_variety: "Loại từ nối",
  complex_sentence_ratio: "Tỉ lệ câu phức",
  top_word_repeat_ratio: "Lặp từ nhiều nhất",
  prompt_overlap: "Độ bám đề",
};
const PERCENT = new Set(["long_word_ratio", "complex_sentence_ratio", "top_word_repeat_ratio", "prompt_overlap"]);

function formatMetric(key, v) {
  if (PERCENT.has(key)) return `${Math.round(v * 100)}%`;
  return Number.isInteger(v) ? v : v.toFixed(1);
}

export default function SubmissionResult() {
  const { id } = useParams();
  const [s, setS] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api(`/writing/submissions/${id}/`).then(setS).catch((e) => setError(errorText(e)));
  }, [id]);

  if (error) return <ErrorAlert>{error}</ErrorAlert>;
  if (!s) return <PageSkeleton blocks={3} />;

  return (
    <div className="page">
      <section className="band-hero" aria-label="Kết quả">
        <div style={{ display: "grid", gap: "0.35rem" }}>
          <p className="muted small">{s.prompt_title}</p>
          <p className="band-big num">{s.band_overall.toFixed(1)}</p>
          <p className="muted small">
            Band ước lượng bởi {s.scorer === "model" ? "mô hình ML" : "phân tích NLP"}. Không phải điểm thi chính thức.
          </p>
        </div>
        <Link to={`/writing/${s.prompt}`} className="btn btn-hero">
          <ArrowCounterClockwise size={18} /> Viết lại đề này
        </Link>
      </section>

      <div className="criteria">
        {CRITERIA.map(([key, label]) => (
          <div key={key} className="card criterion">
            <span className="small">{label}</span>
            <strong className="num">{s[key].toFixed(1)}</strong>
          </div>
        ))}
      </div>

      <div className="grid-2">
        <section className="card" aria-labelledby="fb-title">
          <h2 id="fb-title" style={{ marginBottom: "1rem" }}>Cần cải thiện</h2>
          <ul className="tips">
            {s.feedback.map((tip, i) => (
              <li key={i}><Lightbulb size={18} /><span>{tip}</span></li>
            ))}
          </ul>
        </section>

        <section className="card" aria-labelledby="metric-title">
          <h2 id="metric-title" style={{ marginBottom: "1rem" }}>Chỉ số bài viết</h2>
          <dl className="metrics" style={{ gridTemplateColumns: "repeat(2, 1fr)" }}>
            {Object.entries(s.features).map(([k, v]) => (
              <div key={k}>
                <dt>{METRIC_LABELS[k] ?? k}</dt>
                <dd className="num">{formatMetric(k, v)}</dd>
              </div>
            ))}
          </dl>
        </section>
      </div>

      <section className="card" aria-labelledby="essay-title">
        <div className="card-head">
          <h2 id="essay-title">Bài viết</h2>
          <span className="muted small num">{s.word_count} từ</span>
        </div>
        <p className="essay">{s.essay}</p>
      </section>
    </div>
  );
}
