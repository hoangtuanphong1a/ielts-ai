"""Kiểm tra ngữ pháp / chính tả bằng LanguageTool chạy local (T2.3, WRI-10).

LanguageTool chạy trong docker-compose (service `languagetool`), bài viết không gửi ra ngoài.
LanguageTool không chạy / lỗi mạng -> trả [] để việc chấm điểm vẫn tiếp tục.
"""
import json
import logging
import urllib.error
import urllib.parse
import urllib.request

logger = logging.getLogger(__name__)

# Gom category của LanguageTool về 4 nhóm hiển thị
CATEGORY_MAP = {
    "GRAMMAR": "grammar",
    "TYPOS": "spelling",
    "CASING": "spelling",
    "PUNCTUATION": "punctuation",
    "TYPOGRAPHY": "punctuation",
    "CONFUSED_WORDS": "spelling",  # there / their, then / than: lỗi chọn từ, tính vào Lexical Resource
}
# Một số luật nằm trong nhóm MISC nhưng thực chất là lỗi ngữ pháp
RULE_CATEGORY = {"EN_A_VS_AN": "grammar"}
# Luật gây nhiễu với bài luận (vd. dấu nháy cong, khoảng trắng) -> bỏ qua
IGNORED_RULES = {"WHITESPACE_RULE", "EN_QUOTES", "DASH_RULE", "PUNCTUATION_PARAGRAPH_END"}
MAX_ISSUES = 200


# Biến đổi chính tả Anh -> Mỹ (IELTS chấp nhận cả hai)
UK_US = [("our", "or"), ("ise", "ize"), ("isa", "iza"), ("isi", "izi"), ("yse", "yze"),
         ("tre", "ter"), ("ll", "l"), ("ence", "ense"), ("ogue", "og")]


def _canon(word: str) -> str:
    word = word.lower()
    for uk, us in UK_US:
        word = word.replace(uk, us)
    return word


def is_spelling_variant(word: str, replacements: list[str]) -> bool:
    """'emphasise' với gợi ý 'emphasize' -> chỉ khác cách viết Anh/Mỹ, không phải lỗi."""
    return bool(word) and any(_canon(word) == _canon(r) for r in replacements)


def _matched_text(m: dict) -> str:
    ctx = m.get("context") or {}
    text = ctx.get("text", "")
    return text[ctx.get("offset", 0):ctx.get("offset", 0) + ctx.get("length", 0)]


def parse_matches(matches: list[dict]) -> list[dict]:
    """Chuẩn hoá kết quả LanguageTool thành danh sách lỗi gọn cho frontend."""
    issues = []
    for m in matches:
        rule = m.get("rule", {})
        if rule.get("id") in IGNORED_RULES:
            continue
        replacements = [r["value"] for r in m.get("replacements", [])[:3]]
        if is_spelling_variant(_matched_text(m), replacements):
            continue
        category_id = rule.get("category", {}).get("id", "")
        issues.append({
            "offset": m["offset"],
            "length": m["length"],
            "category": RULE_CATEGORY.get(rule.get("id"), CATEGORY_MAP.get(category_id, "style")),
            "message": m.get("message", ""),
            "replacements": replacements,
            "rule": rule.get("id", ""),
        })
        if len(issues) >= MAX_ISSUES:
            break
    return issues


def check_grammar(text: str, base_url: str | None, timeout: float = 15.0) -> list[dict]:
    if not base_url or not text.strip():
        return []
    data = urllib.parse.urlencode({"text": text, "language": "en-US"}).encode()
    req = urllib.request.Request(f"{base_url.rstrip('/')}/v2/check", data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
        logger.warning("LanguageTool unavailable, skipping grammar check: %s", exc)
        return []
    return parse_matches(payload.get("matches", []))


def error_rates(issues: list[dict], word_count: float) -> dict[str, float]:
    """Số lỗi trên mỗi 100 từ, tách ngữ pháp và chính tả."""
    words = max(word_count, 1)
    count = lambda cat: sum(1 for i in issues if i["category"] == cat)  # noqa: E731
    return {
        "grammar_per_100": round(count("grammar") * 100 / words, 2),
        "spelling_per_100": round(count("spelling") * 100 / words, 2),
    }
