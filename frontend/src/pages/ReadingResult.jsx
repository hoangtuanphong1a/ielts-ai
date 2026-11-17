import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { ArrowCounterClockwise, CheckCircle, MagnifyingGlass, XCircle } from "@phosphor-icons/react";
import { api, errorText } from "../api.js";
import { ErrorAlert, PageSkeleton } from "../components/ui.jsx";
import { KIND_LABEL, PassageView, mmss } from "../components/Reading.jsx";

export default function ReadingResult() {
  const { id } = useParams();
  const [attempt, setAttempt] = useState(null);
  const [error, setError] = useState("");
  const [highlight, setHighlight] = useState(null);
  const [tab, setTab] = useState("questions");

  useEffect(() => {
    api(`/reading/attempts/${id}/`).then(setAttempt).catch((e) => setError(errorText(e)));
  }, [id]);

  // Độ chính xác theo dạng câu hỏi: dữ liệu cho phần cá nhân hoá
  const byKind = useMemo(() => {
    if (!attempt) return [];
    const map = {};
    attempt.results.forEach((r) => {
      map[r.kind] ??= { kind: r.kind, correct: 0, total: 0 };
      map[r.kind].total += 1;
      map[r.kind].correct += r.correct ? 1 : 0;
    });
    return Object.values(map);
  }, [attempt]);

  if (error) return <ErrorAlert>{error}</ErrorAlert>;
  if (!attempt) return <PageSkeleton blocks={2} />;

  const { passage } = attempt;
  const show = (evidence) => { setHighlight(evidence); setTab("passage"); };

  return (
    <div className="page reading-page">
      <section className="card journey-card" aria-labelledby="rr-title">
        <div className="journey-head">
          <div>
            <p id="rr-title" className="muted small">{passage.title}</p>
            <p className="band-big num">{attempt.band.toFixed(1)}</p>
            <p className="muted small num">
              {attempt.correct} of {attempt.total} correct in {mmss(attempt.duration_seconds)}.
              {" "}Band estimated by scaling to a 40-question test.
            </p>
          </div>
          <Link to={`/reading/${passage.id}`} className="btn"><ArrowCounterClockwise size={18} /> Try again</Link>
        </div>
        <ul className="kind-stats">
          {byKind.map((k) => (
            <li key={k.kind}>
              <span className="small">{KIND_LABEL[k.kind]}</span>
              <strong className="num">{k.correct}/{k.total}</strong>
            </li>
          ))}
        </ul>
      </section>

      <div className="segmented reading-tabs" role="tablist" aria-label="Review view">
        <button role="tab" aria-selected={tab === "passage"} onClick={() => setTab("passage")}>Passage</button>
        <button role="tab" aria-selected={tab === "questions"} onClick={() => setTab("questions")}>Answers</button>
      </div>

      <div className="reading-split" data-tab={tab}>
        <div className="card reading-pane pane-passage">
          <PassageView title={passage.title} body={passage.body} highlight={highlight} storageKey={passage.id} />
        </div>
        <div className="card reading-pane pane-questions">
          <h2 style={{ marginBottom: "1rem" }}>Answers and explanations</h2>
          <ol className="review-list">
            {attempt.results.map((r) => (
              <li key={r.number} className={r.correct ? "is-right" : "is-wrong"}>
                <div className="review-head">
                  {r.correct
                    ? <CheckCircle size={22} weight="fill" aria-label="Correct" />
                    : <XCircle size={22} weight="fill" aria-label="Incorrect" />}
                  <strong className="num">Question {r.number}</strong>
                  <span className="muted small">{KIND_LABEL[r.kind]}</span>
                </div>
                <p className="small">
                  Your answer: <strong>{r.given || "(blank)"}</strong>
                  {!r.correct && <> · Correct: <strong>{r.answer}</strong></>}
                </p>
                <p className="muted small">{r.explanation}</p>
                {r.evidence && (
                  <button type="button" className="link-btn small" onClick={() => show(r.evidence)}>
                    <MagnifyingGlass size={14} /> Show in passage
                  </button>
                )}
              </li>
            ))}
          </ol>
        </div>
      </div>
    </div>
  );
}
