// Reading (T1.4): hiển thị bài đọc + bộ render cho từng dạng câu hỏi IELTS.
import { useEffect, useRef, useState } from "react";
import { Timer } from "@phosphor-icons/react";

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

// Bài đọc, đoạn gắn nhãn A, B, C...; `highlight` = đoạn trích cần tô (xem lại đáp án)
export function PassageView({ title, body, highlight }) {
  const markRef = useRef(null);
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

  return (
    <article className="passage" aria-label="Reading passage">
      <h2 className="passage-title">{title}</h2>
      {splitParagraphs(body).map((para, i) => {
        const at = highlight ? para.indexOf(highlight) : -1;
        return (
          <p key={i} className="passage-para">
            <span className="para-label" aria-label={`Paragraph ${LETTERS[i]}`}>{LETTERS[i]}</span>
            <span className="para-text">
              {at === -1 ? para : (
                <>
                  {para.slice(0, at)}
                  <mark ref={markRef} className="evidence">{para.slice(at, at + highlight.length)}</mark>
                  {para.slice(at + highlight.length)}
                </>
              )}
            </span>
          </p>
        );
      })}
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
