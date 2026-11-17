// Reading (T1.4): hiển thị bài đọc + bộ render cho từng dạng câu hỏi IELTS.
import { Fragment, useCallback, useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { Highlighter, MagnifyingGlass, Timer } from "@phosphor-icons/react";
import WordLookup, { cleanWord, sentenceAround } from "./WordLookup.jsx";

export const KIND_LABEL = {
  mcq: "Multiple choice",
  tfng: "True / False / Not Given",
  ynng: "Yes / No / Not Given",
  headings: "Matching headings",
  match_info: "Matching information",
  completion: "Sentence completion",
};
const LETTERS = "ABCDEFGHIJ";
const JUDGE = { tfng: ["TRUE", "FALSE", "NOT GIVEN"], ynng: ["YES", "NO", "NOT GIVEN"] };

export const splitParagraphs = (body) => body.split(/\n\s*\n/).map((p) => p.trim()).filter(Boolean);

// ---- Đánh dấu từ khoá (REA-04): lưu trong trình duyệt theo từng bài đọc ----
const hlKey = (k) => `reading-highlights-${k}`;
const loadHighlights = (k) => { try { return JSON.parse(localStorage.getItem(hlKey(k))) || []; } catch { return []; } };
const saveHighlights = (k, v) => { try { localStorage.setItem(hlKey(k), JSON.stringify(v)); } catch { /* bỏ qua */ } };

// Thêm vùng đánh dấu {p: đoạn, s, e}; gộp với vùng chồng lên trong cùng đoạn
function addRange(list, r) {
  const overlap = list.filter((x) => x.p === r.p && x.s <= r.e && r.s <= x.e);
  const merged = overlap.reduce((m, x) => ({ p: m.p, s: Math.min(m.s, x.s), e: Math.max(m.e, x.e) }), r);
  return [...list.filter((x) => !overlap.includes(x)), merged];
}

// Vị trí ký tự của (node, offset) tính từ đầu `container` (đúng cả khi chữ đã bị chia bởi <mark>)
function offsetIn(container, node, offset) {
  const range = document.createRange();
  range.selectNodeContents(container);
  range.setEnd(node, offset);
  return range.toString().length;
}

// Tách đoạn văn theo mọi ranh giới đánh dấu + đoạn bằng chứng -> các đoạn chữ liền, không chồng nhau
function segments(text, marks, evidence) {
  const cuts = new Set([0, text.length]);
  marks.forEach((m) => { cuts.add(m.s); cuts.add(m.e); });
  if (evidence) { cuts.add(evidence.s); cuts.add(evidence.e); }
  const points = [...cuts].filter((x) => x >= 0 && x <= text.length).sort((x, y) => x - y);
  const out = [];
  for (let i = 0; i < points.length - 1; i += 1) {
    const s = points[i], e = points[i + 1];
    if (s === e) continue;
    out.push({ s, e, text: text.slice(s, e), mark: marks.find((m) => m.s <= s && e <= m.e),
               evidence: Boolean(evidence && evidence.s <= s && e <= evidence.e) });
  }
  return out;
}

// Bài đọc, đoạn gắn nhãn A, B, C...; `highlight` = đoạn trích bằng chứng cần tô (xem lại đáp án).
// REA-04: nhấp đúp một từ để tra nghĩa; bôi đen một cụm để đánh dấu; bấm vào chỗ đã đánh dấu để bỏ.
export function PassageView({ title, body, highlight, storageKey }) {
  const markRef = useRef(null);
  const [query, setQuery] = useState(null);
  const [typed, setTyped] = useState("");
  const [marks, setMarks] = useState(() => (storageKey ? loadHighlights(storageKey) : []));
  const [pending, setPending] = useState(null);  // cụm vừa bôi đen, chờ bấm "Highlight"
  const close = useCallback(() => setQuery(null), []);
  const paragraphs = splitParagraphs(body);

  const updateMarks = (next) => {
    setMarks(next);
    if (storageKey) saveHighlights(storageKey, next);
  };
  const highlightRange = (r) => { updateMarks(addRange(marks, r)); setPending(null); window.getSelection()?.removeAllRanges(); };

  const onSelect = (e) => {
    // Sự kiện từ popover / nút Highlight (render qua portal) vẫn nổi bọt lên đây -> bỏ qua
    if (e.target.closest?.(".lookup, .hl-toolbar")) return;
    const sel = window.getSelection();
    const raw = sel?.toString() || "";
    if (!raw.trim() || !sel.rangeCount) { setPending(null); return; }
    const range = sel.getRangeAt(0);
    const para = range.startContainer.parentElement?.closest(".passage-para");
    if (!para || para !== range.endContainer.parentElement?.closest(".passage-para")) return; // khác đoạn: bỏ qua
    const container = para.querySelector(".para-text");
    let s = offsetIn(container, range.startContainer, range.startOffset);
    let end = offsetIn(container, range.endContainer, range.endOffset);
    const text = container.textContent;
    while (s < end && /\s/.test(text[s])) s += 1;
    while (end > s && /\s/.test(text[end - 1])) end -= 1;
    if (end <= s) return;
    const spot = { p: Number(para.dataset.index), s, e: end };
    const word = cleanWord(raw);
    if (word) {
      setPending(null);
      setQuery({ word, context: sentenceAround(text, s), rect: range.getBoundingClientRect(), spot });
    } else if (end - s <= 300) {
      setPending({ ...spot, rect: range.getBoundingClientRect() });
    }
  };

  const onType = (e) => {
    e.preventDefault();
    const word = cleanWord(typed);
    if (!word) return;
    // Lấy câu đầu tiên trong bài có từ này làm ngữ cảnh
    const at = body.toLowerCase().search(new RegExp(`\\b${word.toLowerCase()}\\b`));
    setQuery({ word, context: at === -1 ? "" : sentenceAround(body, at), rect: e.currentTarget.getBoundingClientRect() });
  };

  useEffect(() => {
    const el = markRef.current;
    if (!highlight || !el) return;
    // Màn rộng: khung bài đọc tự cuộn -> chỉ cuộn trong khung, không kéo cả trang
    const pane = el.closest(".reading-pane");
    if (pane && pane.scrollHeight > pane.clientHeight) {
      pane.scrollTo({ top: el.offsetTop - pane.clientHeight / 2, behavior: "smooth" });
    } else {
      el.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  }, [highlight]);

  let evidenceRefUsed = false;
  return (
    <article className="passage" aria-label="Reading passage" onMouseUp={onSelect} onTouchEnd={onSelect}>
      <div className="passage-top">
        <h2 className="passage-title">{title}</h2>
        <form className="lookup-form" onSubmit={onType} role="search">
          <label htmlFor="lookup-input" className="sr-only">Look up a word</label>
          <input id="lookup-input" placeholder="Look up a word" value={typed} autoComplete="off"
                 onChange={(e) => setTyped(e.target.value)} />
          <button type="submit" className="icon-btn" aria-label="Look up"><MagnifyingGlass size={18} /></button>
        </form>
      </div>
      <p className="muted small passage-hint">
        Double-click a word to look it up. Select a phrase to highlight it; click a highlight to remove it.
        {marks.length > 0 && <> <button type="button" className="link-btn small" onClick={() => updateMarks([])}>Clear {marks.length} highlight{marks.length > 1 ? "s" : ""}</button></>}
      </p>
      {paragraphs.map((para, i) => {
        const at = highlight ? para.indexOf(highlight) : -1;
        const evidence = at === -1 ? null : { s: at, e: at + highlight.length };
        return (
          <p key={i} className="passage-para" data-index={i}>
            <span className="para-label" aria-label={`Paragraph ${LETTERS[i]}`}>{LETTERS[i]}</span>
            <span className="para-text">
              {segments(para, marks.filter((m) => m.p === i), evidence).map((seg) => {
                let node = seg.text;
                if (seg.evidence) {
                  const ref = evidenceRefUsed ? undefined : markRef;
                  evidenceRefUsed = true;
                  node = <mark ref={ref} className="evidence">{node}</mark>;
                }
                if (seg.mark) {
                  node = (
                    <mark className="user-hl" title="Click to remove this highlight"
                          onClick={() => !window.getSelection()?.toString() && updateMarks(marks.filter((m) => m !== seg.mark))}>
                      {node}
                    </mark>
                  );
                }
                return <Fragment key={seg.s}>{node}</Fragment>;
              })}
            </span>
          </p>
        );
      })}
      {pending && createPortal(
        <button type="button" className="btn hl-toolbar" onClick={() => highlightRange(pending)}
                style={{ top: Math.max(8, pending.rect.top - 48), left: Math.max(8, Math.min(pending.rect.left, window.innerWidth - 140)) }}>
          <Highlighter size={18} /> Highlight
        </button>, document.body)}
      {query && (
        <WordLookup query={query} source={`Reading: ${title}`} onClose={close}
                    onHighlight={query.spot ? () => highlightRange(query.spot) : undefined} />
      )}
    </article>
  );
}

function Choices({ name, options, value, onChange, label }) {
  return (
    <div className="choice-row" role="radiogroup" aria-label={label}>
      {options.map((opt) => (
        <button key={opt} type="button" role="radio" aria-checked={value === opt}
                className="chip" aria-pressed={value === opt} onClick={() => onChange(name, opt)}>
          {opt}
        </button>
      ))}
    </div>
  );
}

function Completion({ q, group, value, onChange }) {
  const words = value.trim() ? value.trim().split(/\s+/).length : 0;
  const over = group.max_words && words > group.max_words;
  const [before, after] = q.text.split("______");
  return (
    <div className="completion">
      <label htmlFor={`q${q.number}`}>
        {before}<span className="blank" aria-hidden="true">({q.number})</span>{after}
      </label>
      <input id={`q${q.number}`} value={value} autoComplete="off" spellCheck="false"
             aria-invalid={over || undefined} aria-describedby={over ? `q${q.number}-hint` : undefined}
             onChange={(e) => onChange(String(q.number), e.target.value)} />
      {over && <span id={`q${q.number}-hint`} className="small field-error">Too many words. Use no more than {group.max_words}.</span>}
    </div>
  );
}

export function QuestionGroupView({ group, answers, onChange }) {
  const first = group.questions[0]?.number;
  const last = group.questions[group.questions.length - 1]?.number;
  const isMatching = group.kind === "headings" || group.kind === "match_info";

  return (
    <section className="qgroup" aria-labelledby={`g${group.id}`}>
      <h3 id={`g${group.id}`} className="qgroup-title">Questions {first}{last !== first ? `-${last}` : ""}</h3>
      <p className="muted small qgroup-instr">{group.instructions}</p>

      {group.kind === "headings" && (
        <ol className="heading-list" aria-label="List of headings">
          {group.options.map((o) => <li key={o.key}><strong>{o.key}</strong> {o.text}</li>)}
        </ol>
      )}

      <ol className="qlist">
        {group.questions.map((q) => {
          const key = String(q.number);
          const value = answers[key] || "";
          return (
            <li key={q.number} id={`question-${q.number}`} className="qitem">
              <span className="qnum num">{q.number}</span>
              <div className="qbody">
                {group.kind === "completion" ? (
                  <Completion q={q} group={group} value={value} onChange={onChange} />
                ) : (
                  <>
                    <p>{q.text}</p>
                    {JUDGE[group.kind] && (
                      <Choices name={key} options={JUDGE[group.kind]} value={value} onChange={onChange} label={`Question ${q.number}`} />
                    )}
                    {group.kind === "mcq" && (
                      <div className="mcq" role="radiogroup" aria-label={`Question ${q.number}`}>
                        {q.choices.map((c) => (
                          <label key={c.key} className={`mcq-option${value === c.key ? " is-on" : ""}`}>
                            <input type="radio" name={`q${q.number}`} value={c.key} checked={value === c.key}
                                   onChange={() => onChange(key, c.key)} />
                            <strong>{c.key}</strong> {c.text}
                          </label>
                        ))}
                      </div>
                    )}
                    {isMatching && (
                      <select aria-label={`Answer for question ${q.number}`} value={value}
                              onChange={(e) => onChange(key, e.target.value)}>
                        <option value="">Choose...</option>
                        {group.options.map((o) => (
                          <option key={o.key} value={o.key}>
                            {group.kind === "headings" ? `${o.key}. ${o.text}` : o.text}
                          </option>
                        ))}
                      </select>
                    )}
                  </>
                )}
              </div>
            </li>
          );
        })}
      </ol>
    </section>
  );
}

export const mmss = (s) => `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`;

// Đồng hồ đếm ngược. Chỉ mount khi đã biết số giây (tránh lỗi: khởi tạo 0 -> tưởng hết giờ -> tự nộp).
// Hết giờ gọi onEnd đúng một lần; `paused` dừng đếm (đang nộp bài).
export function Countdown({ seconds, onEnd, paused = false }) {
  const [left, setLeft] = useState(seconds);
  const onEndRef = useRef(onEnd);
  onEndRef.current = onEnd;

  useEffect(() => {
    if (paused || left <= 0) return undefined;
    const t = setTimeout(() => setLeft((s) => s - 1), 1000);
    return () => clearTimeout(t);
  }, [left, paused]);

  useEffect(() => {
    if (left === 0 && seconds > 0) onEndRef.current();
  }, [left, seconds]);

  return (
    <>
      <div className={`timer num${left <= 120 ? " is-low" : ""}`} role="timer" aria-label={`Time left ${mmss(left)}`}>
        <Timer size={20} aria-hidden="true" /> {mmss(left)}
      </div>
      {/* Chỉ báo cho trình đọc màn hình ở mốc 5 phút và 1 phút, không đọc mỗi giây */}
      <span className="sr-only" aria-live="polite">{left === 300 ? "5 minutes left" : left === 60 ? "1 minute left" : ""}</span>
    </>
  );
}
