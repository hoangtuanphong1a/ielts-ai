// REA-04: tra từ ngay trong bài đọc (WordNet offline, nghĩa xếp theo câu chứa từ) + lưu vào thẻ ôn tập.
import { useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { BookmarkSimple, Check, CircleNotch, Highlighter, X } from "@phosphor-icons/react";
import { api, errorText } from "../api.js";

const WORD_RE = /^[A-Za-z][A-Za-z'-]{0,39}$/;
const LEVEL = { basic: "Everyday word", intermediate: "Intermediate", advanced: "Less common" };

// Câu chứa vị trí `at` trong đoạn văn
export function sentenceAround(text, at) {
  const start = Math.max(text.lastIndexOf(". ", at), text.lastIndexOf("? ", at), text.lastIndexOf("! ", at));
  const ends = [". ", "? ", "! "].map((m) => text.indexOf(m, at)).filter((i) => i !== -1);
  const end = ends.length ? Math.min(...ends) + 1 : text.length;
  return text.slice(start === -1 ? 0 : start + 2, end).trim();
}

export function cleanWord(text) {
  const word = (text || "").trim().replace(/^[^A-Za-z]+|[^A-Za-z]+$/g, "");
  return WORD_RE.test(word) ? word : null;
}

export default function WordLookup({ query, source, onClose, onHighlight }) {
  const { word, context, rect } = query;
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const [pick, setPick] = useState(0);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const boxRef = useRef(null);

  useEffect(() => {
    let cancelled = false;
    setData(null); setError(""); setPick(0); setSaved(false);
    const params = new URLSearchParams({ word, context: context.slice(0, 400) });
    api(`/vocab/lookup/?${params}`)
      .then((d) => { if (!cancelled) { setData(d); setSaved(d.in_deck); } })
      .catch((e) => { if (!cancelled) setError(e.status === 404 ? `No definition found for “${word}”.` : errorText(e)); });
    return () => { cancelled = true; };
  }, [word, context]);

  // Esc / bấm ra ngoài để đóng; mở ra thì đưa focus vào popover
  useEffect(() => {
    boxRef.current?.focus();
    const onKey = (e) => { if (e.key === "Escape") onClose(); };
    const onDown = (e) => { if (boxRef.current && !boxRef.current.contains(e.target)) onClose(); };
    document.addEventListener("keydown", onKey);
    document.addEventListener("pointerdown", onDown);
    return () => { document.removeEventListener("keydown", onKey); document.removeEventListener("pointerdown", onDown); };
  }, [onClose]);

  async function save() {
    setSaving(true);
    try {
      await api("/vocab/cards/add/", {
        method: "POST",
        body: { term: data.lemma, definition: data.senses[pick].definition, context, source },
      });
      setSaved(true);
    } catch (e) {
      setError(errorText(e));
    } finally {
      setSaving(false);
    }
  }

  // Vị trí: dưới từ được chọn; bên dưới không đủ chỗ thì mở lên phía trên (fixed nên không cuộn tới được).
  // Màn nhỏ: CSS chuyển thành bottom sheet.
  let style;
  if (rect) {
    const left = Math.max(12, Math.min(rect.left, window.innerWidth - 372));
    const below = window.innerHeight - rect.bottom;
    style = below < 380 && rect.top > below
      ? { left, bottom: window.innerHeight - rect.top + 8, maxHeight: Math.min(520, rect.top - 20) }
      : { left, top: rect.bottom + 8, maxHeight: Math.min(520, below - 20) };
  }

  // Portal ra body: khung bài đọc là thẻ kính (backdrop-filter) nên position: fixed bên trong
  // sẽ bị định vị theo khung đó và bị cắt.
  return createPortal(
    <div ref={boxRef} className="lookup card" role="dialog" aria-label={`Definition of ${word}`} tabIndex={-1} style={style}>
      <div className="lookup-head">
        <strong className="lookup-word">{data?.lemma || word}</strong>
        <button type="button" className="icon-btn" onClick={onClose} aria-label="Close"><X size={18} /></button>
      </div>

      {!data && !error && <p className="muted small"><CircleNotch size={16} className="spin" /> Looking up...</p>}
      {error && <p className="small" role="alert">{error}</p>}

      {data && (
        <>
          <div className="lookup-tags">
            {data.level && <span className="tag">{LEVEL[data.level]}</span>}
            {data.academic && <span className="tag">Academic word (AWL)</span>}
          </div>
          <p className="muted small">Meanings ranked by how well they fit this sentence. Pick one to save.</p>
          <ol className="lookup-senses">
            {data.senses.map((s, i) => (
              <li key={i}>
                <button type="button" className="lookup-sense" aria-pressed={pick === i} onClick={() => setPick(i)}>
                  <em className="small">{s.pos}</em> {s.definition}
                  {s.example && <span className="muted small lookup-example">&ldquo;{s.example}&rdquo;</span>}
                  {s.synonyms.length > 0 && <span className="muted small">Similar: {s.synonyms.join(", ")}</span>}
                </button>
              </li>
            ))}
          </ol>
          <button type="button" className="btn btn-block" onClick={save} disabled={saving || saved}>
            {saved ? <><Check size={18} /> In your vocabulary</>
              : saving ? <><CircleNotch size={18} className="spin" /> Saving</>
              : <><BookmarkSimple size={18} /> Add to my vocabulary</>}
          </button>
          {onHighlight && (
            <button type="button" className="btn btn-ghost btn-block" onClick={() => { onHighlight(); onClose(); }}>
              <Highlighter size={18} /> Highlight in passage
            </button>
          )}
        </>
      )}
    </div>,
    document.body,
  );
}
