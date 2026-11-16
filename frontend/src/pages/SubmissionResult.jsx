import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { ArrowCounterClockwise, CircleNotch, Lightbulb } from "@phosphor-icons/react";
import { api, errorText } from "../api.js";
import { useAuth } from "../auth.jsx";
import { CountUp, JourneyTrack } from "../components/Journey.jsx";
import { ErrorAlert, PageSkeleton, Skeleton } from "../components/ui.jsx";

const CRITERIA = [
  ["band_task_response", "Task Response"],
  ["band_coherence", "Coherence & Cohesion"],
  ["band_lexical", "Lexical Resource"],
  ["band_grammar", "Grammatical Range"],
];

// Nhãn cho chỉ số NLP trả về từ backend (ml/features.py)
const METRIC_LABELS = {
  word_count: "Words",
  sentence_count: "Sentences",
  paragraph_count: "Paragraphs",
  avg_sentence_len: "Avg. sentence length",
  guiraud_index: "Lexical diversity",
  long_word_ratio: "Long words",
  linker_count: "Linking words",
  linker_variety: "Distinct linkers",
  complex_sentence_ratio: "Complex sentences",
  top_word_repeat_ratio: "Most repeated word",
  prompt_overlap: "Prompt relevance",
  grammar_per_100: "Grammar errors / 100 words",
  spelling_per_100: "Spelling errors / 100 words",
  awl_ratio: "Academic words (AWL)",
  advanced_ratio: "Less common words",
  awl_families: "Academic word families",
  lemma_diversity: "Word variety",
  semantic_relevance: "Topic relevance",
};
const PERCENT = new Set([
  "long_word_ratio", "complex_sentence_ratio", "top_word_repeat_ratio", "prompt_overlap",
  "awl_ratio", "advanced_ratio", "lemma_diversity", "semantic_relevance",
]);
// Chỉ số nội bộ, không cần hiện cho học viên
const HIDDEN = new Set([
  "content_word_count", "intermediate_ratio", "topic_continuity", "paragraph_redundancy",
]);

const LEVELS = [
  ["basic", "Everyday", "var(--aqua)"],
  ["intermediate", "Intermediate", "var(--sky)"],
  ["advanced", "Less common", "var(--ocean)"],
];

// T2.4: mỗi đoạn bám đề đến đâu (Sentence-BERT). Thanh đầy ở 0.6, dưới 0.2 coi là lạc đề.
function TopicFocus({ semantic, essay }) {
  const paragraphs = essay.split(/\n\s*\n/).map((p) => p.trim()).filter(Boolean);
  const scores = semantic.paragraph_relevance;
  if (scores.length < 2) return null;
  return (
    <section className="card" aria-labelledby="topic-title">
      <h2 id="topic-title" style={{ marginBottom: "0.5rem" }}>Staying on topic</h2>
      <p className="muted small" style={{ marginBottom: "1rem" }}>
        How closely each paragraph relates to the question, measured by meaning rather than shared words.
      </p>
      <ol className="topic-list">
        {scores.map((score, i) => {
          const off = semantic.off_topic_paragraphs.includes(i + 1);
          return (
            <li key={i}>
              <div className="topic-row">
                <span className="small" style={{ fontWeight: 600 }}>Paragraph {i + 1}</span>
                {off && <span className="tag">Off topic</span>}
              </div>
              <p className="muted small topic-snippet">{(paragraphs[i] || "").slice(0, 110)}{(paragraphs[i] || "").length > 110 ? "..." : ""}</p>
              <div className="topic-bar" role="meter" aria-valuemin={0} aria-valuemax={100}
                   aria-valuenow={Math.round(Math.max(0, Math.min(1, score / 0.6)) * 100)}
                   aria-label={`Paragraph ${i + 1} relevance`}>
                <span style={{ width: `${Math.max(4, Math.min(100, (score / 0.6) * 100))}%`, background: off ? "var(--aqua)" : "var(--ocean)" }} />
              </div>
            </li>
          );
        })}
      </ol>
    </section>
  );
}

// T2.2: hồ sơ từ vựng (mức từ theo tần suất + từ học thuật AWL)
function VocabProfile({ vocab }) {
  const total = LEVELS.reduce((n, [k]) => n + (vocab.levels[k] || 0), 0) || 1;
  return (
    <section className="card" aria-labelledby="vocab-title">
      <h2 id="vocab-title" style={{ marginBottom: "0.5rem" }}>Vocabulary profile</h2>
      <p className="muted small" style={{ marginBottom: "1rem" }}>
        Word levels are estimated from how common each word is in English, not official CEFR labels.
      </p>
      <div className="vocab-bar" role="img"
           aria-label={LEVELS.map(([k, label]) => `${label} ${Math.round(((vocab.levels[k] || 0) / total) * 100)}%`).join(", ")}>
        {LEVELS.map(([k, , color]) => (
          <span key={k} style={{ width: `${((vocab.levels[k] || 0) / total) * 100}%`, background: color }} />
        ))}
      </div>
      <ul className="vocab-legend">
        {LEVELS.map(([k, label, color]) => (
          <li key={k}><span className="vocab-dot" style={{ background: color }} />{label} <strong className="num">{Math.round(((vocab.levels[k] || 0) / total) * 100)}%</strong></li>
        ))}
      </ul>
      <div className="grid-2" style={{ marginTop: "1.25rem" }}>
        <div>
          <h3 className="small" style={{ marginBottom: "0.5rem" }}>Academic words you used</h3>
          {vocab.academic_words.length
            ? <div className="chips">{vocab.academic_words.map((w) => <span key={w} className="tag">{w}</span>)}</div>
            : <p className="muted small">None yet. Try words like significant, contribute, approach.</p>}
        </div>
        <div>
          <h3 className="small" style={{ marginBottom: "0.5rem" }}>Less common words</h3>
          {vocab.advanced_words.length
            ? <div className="chips">{vocab.advanced_words.map((w) => <span key={w} className="tag">{w}</span>)}</div>
            : <p className="muted small">Mostly everyday words so far.</p>}
        </div>
      </div>
    </section>
  );
}

function formatMetric(key, v) {
  if (PERCENT.has(key)) return `${Math.round(v * 100)}%`;
  return Number.isInteger(v) ? v : v.toFixed(1);
}


const countBy = (issues, cat) => issues.filter((i) => i.category === cat).length;

// T2.3: tô lỗi LanguageTool ngay trong bài; title = giải thích + gợi ý sửa
function renderEssay(text, issues) {
  const sorted = [...issues].sort((a, b) => a.offset - b.offset);
  const parts = [];
  let pos = 0;
  sorted.forEach((iss, i) => {
    if (iss.offset < pos) return; // bỏ lỗi chồng lên lỗi trước
    if (iss.offset > pos) parts.push(text.slice(pos, iss.offset));
    const fix = iss.replacements?.length ? ` Try: ${iss.replacements.join(", ")}` : "";
    parts.push(
      <mark key={i} className={`issue issue-${iss.category}`} title={`${iss.message}${fix}`} tabIndex={0}>
        {text.slice(iss.offset, iss.offset + iss.length)}
      </mark>,
    );
    pos = iss.offset + iss.length;
  });
  parts.push(text.slice(pos));
  return parts;
}

export default function SubmissionResult() {
  const { id } = useParams();
  const { user } = useAuth();
  const [s, setS] = useState(null);
  const [error, setError] = useState("");

  // T2.1: bài chấm ở nền -> hỏi lại mỗi 1.5s tới khi xong / lỗi (tối đa ~2 phút)
  useEffect(() => {
    let timer;
    let tries = 0;
    let cancelled = false;

    async function load() {
      try {
        const data = await api(`/writing/submissions/${id}/`);
        if (cancelled) return;
        setS(data);
        const waiting = data.status === "pending" || data.status === "scoring";
        if (waiting && tries++ < 80) timer = setTimeout(load, 1500);
        else if (waiting) setError("Scoring is taking longer than usual. Please refresh in a few minutes.");
      } catch (e) {
        if (!cancelled) setError(errorText(e));
      }
    }

    load();
    return () => {
      cancelled = true;
      clearTimeout(timer);
    };
  }, [id]);

  if (error && !s) return <ErrorAlert>{error}</ErrorAlert>;
  if (!s) return <PageSkeleton blocks={3} />;

  if (s.status === "pending" || s.status === "scoring") {
    return (
      <div className="page" aria-busy="true">
        <section className="band-hero" aria-live="polite">
          <div style={{ display: "grid", gap: "0.5rem" }}>
            <p className="muted small">{s.prompt_title}</p>
            <p style={{ display: "flex", alignItems: "center", gap: 12, fontSize: "1.5rem", fontWeight: 700 }}>
              <CircleNotch size={28} className="spin" /> Scoring your essay
            </p>
            <p className="muted small">Analysing it against the four IELTS criteria. This usually takes a few seconds.</p>
          </div>
        </section>
        <ErrorAlert>{error}</ErrorAlert>
        <div className="criteria">
          {CRITERIA.map(([key]) => <Skeleton key={key} h={96} style={{ borderRadius: 18 }} />)}
        </div>
      </div>
    );
  }

  if (s.status === "failed") {
    return (
      <div className="page">
        <ErrorAlert>{s.error || "We could not score this essay."}</ErrorAlert>
        <Link to={`/writing/${s.prompt}`} className="btn" style={{ alignSelf: "flex-start" }}>
          <ArrowCounterClockwise size={18} /> Try this prompt again
        </Link>
      </div>
    );
  }

  const target = user.profile?.target_band;
  const weakestKey = CRITERIA.reduce((low, [k]) => (s[k] < s[low] ? k : low), CRITERIA[0][0]);

  return (
    <div className="page">
      <section className="card journey-card" aria-labelledby="result-title">
        <div className="journey-head">
          <div>
            <p id="result-title" className="muted small">{s.prompt_title}</p>
            <p className="band-big num">
              <CountUp value={s.band_overall} />
              {target != null && <span className="band-target"> / {Number(target).toFixed(1)}</span>}
            </p>
            <p className="muted small">
              Estimated by {s.scorer === "model" ? "our ML model" : "NLP analysis"}. Not an official IELTS score.
            </p>
          </div>
          <Link to={`/writing/${s.prompt}`} className="btn">
            <ArrowCounterClockwise size={18} /> Rewrite this prompt
          </Link>
        </div>
        <JourneyTrack current={s.band_overall} target={target} label="This essay on your band journey" />
      </section>

      <div className="criteria">
        {CRITERIA.map(([key, label]) => (
          <div key={key} className="card criterion">
            <span className="small">
              {label}
              {key === weakestKey && <span className="tag" style={{ marginLeft: 8 }}>Focus</span>}
            </span>
            <strong className="num">{s[key].toFixed(1)}</strong>
          </div>
        ))}
      </div>

      <div className="grid-2">
        <section className="card" aria-labelledby="fb-title">
          <h2 id="fb-title" style={{ marginBottom: "1rem" }}>What to improve</h2>
          <ul className="tips">
            {s.feedback.map((tip, i) => (
              <li key={i}><Lightbulb size={18} /><span>{tip}</span></li>
            ))}
          </ul>
        </section>

        <section className="card" aria-labelledby="metric-title">
          <h2 id="metric-title" style={{ marginBottom: "1rem" }}>Essay metrics</h2>
          <dl className="metrics" style={{ gridTemplateColumns: "repeat(2, 1fr)" }}>
            {Object.entries(s.features).filter(([k, v]) => typeof v === "number" && !HIDDEN.has(k)).map(([k, v]) => (
              <div key={k}>
                <dt>{METRIC_LABELS[k] ?? k}</dt>
                <dd className="num">{formatMetric(k, v)}</dd>
              </div>
            ))}
          </dl>
        </section>
      </div>

      {s.features.vocab && <VocabProfile vocab={s.features.vocab} />}
      {s.features.semantic && <TopicFocus semantic={s.features.semantic} essay={s.essay} />}

      <section className="card" aria-labelledby="essay-title">
        <div className="card-head">
          <h2 id="essay-title">Your essay</h2>
          <span className="muted small num">{s.word_count} words</span>
        </div>
        {s.issues?.length > 0 && (
          <p className="muted small" style={{ marginBottom: "0.75rem" }}>
            <mark className="issue issue-grammar">{countBy(s.issues, "grammar")} grammar</mark>{" · "}
            <mark className="issue issue-spelling">{countBy(s.issues, "spelling")} spelling</mark>{" · "}
            <mark className="issue issue-punctuation">{countBy(s.issues, "punctuation") + countBy(s.issues, "style")} other</mark>.
            {" "}Hover or focus a highlight to see the fix.
          </p>
        )}
        <p className="essay">{renderEssay(s.essay, s.issues || [])}</p>
      </section>
    </div>
  );
}
