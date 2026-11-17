import { useCallback, useEffect, useRef, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { CircleNotch } from "@phosphor-icons/react";
import { api, errorText } from "../api.js";
import { ErrorAlert, PageSkeleton } from "../components/ui.jsx";
import { Countdown, PassageView, QuestionGroupView } from "../components/Reading.jsx";

// Lưu nháp đáp án trong trình duyệt (mất cũng không sao, chỉ để lỡ tải lại trang)
const draftKey = (id) => `reading-draft-${id}`;
const loadDraft = (id) => { try { return JSON.parse(localStorage.getItem(draftKey(id))) || {}; } catch { return {}; } };
const saveDraft = (id, answers) => { try { localStorage.setItem(draftKey(id), JSON.stringify(answers)); } catch { /* bỏ qua */ } };
const clearDraft = (id) => { try { localStorage.removeItem(draftKey(id)); } catch { /* bỏ qua */ } };

export default function ReadingTest() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [passage, setPassage] = useState(null);
  const [answers, setAnswers] = useState(() => loadDraft(id));
  const [tab, setTab] = useState("passage");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [confirming, setConfirming] = useState(false);
  const started = useRef(Date.now());

  useEffect(() => {
    api(`/reading/passages/${id}/`).then(setPassage).catch((e) => setError(errorText(e)));
  }, [id]);

  const total = passage ? passage.groups.reduce((n, g) => n + g.questions.length, 0) : 0;
  const answered = Object.values(answers).filter((v) => String(v).trim()).length;

  const submit = useCallback(async () => {
    setBusy(true);
    setError("");
    try {
      const res = await api(`/reading/passages/${id}/attempts/`, {
        method: "POST",
        body: { answers, duration_seconds: Math.round((Date.now() - started.current) / 1000) },
      });
      clearDraft(id);
      navigate(`/reading/attempts/${res.id}`, { replace: true });
    } catch (e) {
      setError(errorText(e));
      setBusy(false);
    }
  }, [answers, id, navigate]);

  const update = (number, value) => {
    setConfirming(false);
    setAnswers((prev) => {
      const next = { ...prev, [number]: value };
      saveDraft(id, next);
      return next;
    });
  };

  if (error && !passage) return <ErrorAlert>{error}</ErrorAlert>;
  if (!passage) return <PageSkeleton blocks={2} />;

  return (
    <div className="page reading-page">
      <div className="reading-bar card">
        <div>
          <p className="muted small">Reading · {passage.topic}</p>
          <h1 className="reading-h1">{passage.title}</h1>
        </div>
        <Countdown seconds={passage.minutes * 60} onEnd={submit} paused={busy} />
      </div>

      <div className="segmented reading-tabs" role="tablist" aria-label="Reading view">
        <button role="tab" aria-selected={tab === "passage"} onClick={() => setTab("passage")}>Passage</button>
        <button role="tab" aria-selected={tab === "questions"} onClick={() => setTab("questions")}>
          Questions <span className="num">({answered}/{total})</span>
        </button>
      </div>

      <div className="reading-split" data-tab={tab}>
        <div className="card reading-pane pane-passage">
          <PassageView title={passage.title} body={passage.body} storageKey={passage.id} />
        </div>
        <div className="card reading-pane pane-questions">
          {passage.groups.map((g) => <QuestionGroupView key={g.id} group={g} answers={answers} onChange={update} />)}

          <div className="reading-submit">
            <ErrorAlert>{error}</ErrorAlert>
            <p className="muted small num">{answered} of {total} answered</p>
            {confirming && answered < total && (
              <p className="small" role="alert">
                {total - answered} question{total - answered > 1 ? "s are" : " is"} still blank. Submit anyway?
              </p>
            )}
            <button type="button" className="btn" disabled={busy}
                    onClick={() => (answered < total && !confirming ? setConfirming(true) : submit())}>
              {busy ? <><CircleNotch size={18} className="spin" /> Marking</> : confirming ? "Yes, submit" : "Submit answers"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
