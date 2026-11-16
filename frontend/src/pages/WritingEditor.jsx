import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { ArrowLeft, CheckCircle, CircleNotch, PaperPlaneRight } from "@phosphor-icons/react";
import { api, errorText } from "../api.js";
import { ErrorAlert, PageSkeleton } from "../components/ui.jsx";

const MIN_WORDS = { task1: 150, task2: 250 };
const MINUTES = { task1: 20, task2: 40 };
const DRAFT_KEY = (id) => `ielts_draft_${id}`;

const TIPS = {
  task1: ["Introduction: paraphrase the question.", "Overview: the two most striking trends.", "Two body paragraphs comparing the data."],
  task2: ["Introduction with a clear position.", "Two body paragraphs, one main idea and example each.", "Conclusion that restates your position."],
};

export default function WritingEditor() {
  const { promptId } = useParams();
  const navigate = useNavigate();
  const [prompt, setPrompt] = useState(null);
  const [essay, setEssay] = useState(() => localStorage.getItem(DRAFT_KEY(promptId)) || "");
  const [loadError, setLoadError] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    api(`/writing/prompts/${promptId}/`).then(setPrompt).catch((e) => setLoadError(errorText(e)));
  }, [promptId]);

  // Lưu nháp mỗi khi gõ
  useEffect(() => {
    localStorage.setItem(DRAFT_KEY(promptId), essay);
  }, [essay, promptId]);

  const wordCount = useMemo(() => essay.trim().split(/\s+/).filter(Boolean).length, [essay]);

  async function submit() {
    setError("");
    setBusy(true);
    try {
      const res = await api("/writing/submissions/", {
        method: "POST",
        body: { prompt: Number(promptId), essay },
      });
      localStorage.removeItem(DRAFT_KEY(promptId));
      navigate(`/submissions/${res.id}`);
    } catch (err) {
      setError(errorText(err));
    } finally {
      setBusy(false);
    }
  }

  if (loadError) return <ErrorAlert>{loadError}</ErrorAlert>;
  if (!prompt) return <PageSkeleton blocks={2} />;

  const min = MIN_WORDS[prompt.task_type];
  const enough = wordCount >= min;

  return (
    <div className="page">
      <Link to="/writing" className="small" style={{ display: "inline-flex", alignItems: "center", gap: 6 }}>
        <ArrowLeft size={16} /> All prompts
      </Link>

      <div className="editor-layout">
        <aside className="editor-aside card" style={{ display: "grid", gap: "1rem" }}>
          <span className="tag" style={{ justifySelf: "start" }}>
            {prompt.task_type === "task1" ? "Task 1" : "Task 2"} · {MINUTES[prompt.task_type]} min
          </span>
          <h1 style={{ fontSize: "1.375rem" }}>{prompt.title}</h1>
          <p>{prompt.prompt_text}</p>
          <div>
            <h3 style={{ marginBottom: "0.5rem" }}>Suggested structure</h3>
            <ul className="tips">
              {TIPS[prompt.task_type].map((t) => (
                <li key={t}><CheckCircle size={18} /><span className="small">{t}</span></li>
              ))}
            </ul>
          </div>
        </aside>

        <div style={{ display: "grid", gap: "1rem" }}>
          <label htmlFor="essay" className="muted small">Your essay (leave a blank line between paragraphs; drafts save on this device)</label>
          <textarea
            id="essay"
            className="editor"
            value={essay}
            onChange={(e) => setEssay(e.target.value)}
            placeholder="Start writing here..."
            spellCheck={false}
          />
          <div className="editor-bar">
            <span className="num" aria-live="polite">
              <strong>{wordCount}</strong>
              <span className="muted"> / {min} words {enough ? "· length OK" : `· ${min - wordCount} to go`}</span>
            </span>
            <span className="spacer" />
            <button className="btn" onClick={submit} disabled={busy || wordCount < 20}>
              {busy ? <CircleNotch size={18} className="spin" /> : <PaperPlaneRight size={18} />}
              {busy ? "Submitting" : "Submit for scoring"}
            </button>
          </div>
          <ErrorAlert>{error}</ErrorAlert>
        </div>
      </div>
    </div>
  );
}
