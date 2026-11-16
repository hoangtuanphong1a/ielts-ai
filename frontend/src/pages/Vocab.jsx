import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { CheckCircle, CircleNotch } from "@phosphor-icons/react";
import { api, errorText } from "../api.js";
import { EmptyState, ErrorAlert, PageSkeleton } from "../components/ui.jsx";

// quality theo SM-2 (0-5); phím tắt 1-4
const GRADES = [
  { q: 1, label: "Forgot", key: "1" },
  { q: 3, label: "Hard", key: "2" },
  { q: 4, label: "Good", key: "3" },
  { q: 5, label: "Easy", key: "4" },
];

export default function Vocab() {
  const [cards, setCards] = useState(null);
  const [index, setIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    api("/vocab/cards/due/").then(setCards).catch((e) => setError(errorText(e)));
  }, []);

  const grade = useCallback(async (quality) => {
    if (busy || !cards) return;
    setBusy(true);
    setError("");
    try {
      await api(`/vocab/cards/${cards[index].id}/review/`, { method: "POST", body: { quality } });
      setFlipped(false);
      setIndex((i) => i + 1);
    } catch (e) {
      setError(errorText(e));
    } finally {
      setBusy(false);
    }
  }, [busy, cards, index]);

  // Phím tắt: Space lật thẻ, 1-4 chấm mức nhớ
  useEffect(() => {
    function onKey(e) {
      if (!cards || index >= cards.length) return;
      if (e.code === "Space") { e.preventDefault(); setFlipped((f) => !f); return; }
      const g = GRADES.find((x) => x.key === e.key);
      if (g && flipped) grade(g.q);
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [cards, index, flipped, grade]);

  if (error && !cards) return <ErrorAlert>{error}</ErrorAlert>;
  if (!cards) return <PageSkeleton blocks={1} />;

  if (index >= cards.length) {
    return (
      <div className="card">
        <EmptyState
          icon={<CheckCircle size={28} />}
          title={cards.length ? "You are done for today" : "No cards due today"}
          action={<Link to="/writing" className="btn btn-ghost">Practise Writing</Link>}
        >
          {cards.length ? `You reviewed ${cards.length} cards. The next ones are due tomorrow.` : "Come back tomorrow."}
        </EmptyState>
      </div>
    );
  }

  const { word } = cards[index];
  const pct = (index / cards.length) * 100;

  return (
    <div className="page" style={{ maxWidth: 720, margin: "0 auto", width: "100%" }}>
      <div className="page-head">
        <h1>Vocabulary review</h1>
        <div style={{ display: "flex", justifyContent: "space-between" }} className="small muted num">
          <span>Card {index + 1} of {cards.length}</span>
          {word.topic && <span>Topic: {word.topic}</span>}
        </div>
        <div className="progress-line" aria-hidden="true"><div style={{ width: `${pct}%` }} /></div>
      </div>

      <button className="card flashcard" onClick={() => setFlipped(!flipped)} aria-label={flipped ? "Hide meaning" : "Show meaning"}>
        <span className="term">{word.term}</span>
        {flipped ? (
          <>
            <p>{word.definition}</p>
            {word.example && <p className="muted example">{word.example}</p>}
          </>
        ) : (
          <span className="muted small">Click or press Space to reveal</span>
        )}
      </button>

      {flipped && (
        <div className="grades" role="group" aria-label="How well did you remember it?">
          {GRADES.map((g) => (
            <button key={g.q} className="btn btn-ghost" onClick={() => grade(g.q)} disabled={busy}>
              {busy ? <CircleNotch size={18} className="spin" /> : g.label}
              <kbd>key {g.key}</kbd>
            </button>
          ))}
        </div>
      )}
      <ErrorAlert>{error}</ErrorAlert>
    </div>
  );
}
