import logging

from celery import shared_task
from django.conf import settings

from ml.agreement import check_agreement, merge_issues
from ml.grammar import check_grammar
from ml.scorer import score_essay

from .models import Submission

logger = logging.getLogger(__name__)


@shared_task
def score_submission(submission_id: int) -> str:
    """Chấm 1 bài Writing ở nền (T2.1, WRI-09).

    pending -> scoring -> done | failed. Lỗi thì lưu lý do vào `error`, không làm sập worker.
    """
    sub = Submission.objects.select_related("prompt").filter(pk=submission_id).first()
    if sub is None:
        return "missing"
    if sub.status == Submission.Status.DONE:
        return "already-done"  # task chạy lại (retry/duplicate) thì bỏ qua

    sub.status = Submission.Status.SCORING
    sub.save(update_fields=["status"])

    try:
        # LanguageTool trước; spaCy bù lỗi hoà hợp chủ ngữ - động từ mà LanguageTool bỏ sót
        issues = merge_issues(
            check_grammar(sub.essay, getattr(settings, "LANGUAGETOOL_URL", None)),
            check_agreement(sub.essay),
        )
        result = score_essay(
            sub.essay,
            prompt=sub.prompt.prompt_text,
            task_type=sub.prompt.task_type,
            model_path=settings.ML_MODEL_PATH,
            grammar_issues=issues,
        )
    except Exception as exc:  # noqa: BLE001 - mọi lỗi chấm đều ghi lại cho user thấy
        logger.exception("Scoring submission %s failed", submission_id)
        sub.status = Submission.Status.FAILED
        sub.error = f"We could not score this essay: {exc}"
        sub.save(update_fields=["status", "error"])
        return "failed"

    sub.word_count = int(result.features["word_count"])
    sub.band_overall = result.overall
    sub.band_task_response = result.task_response
    sub.band_coherence = result.coherence
    sub.band_lexical = result.lexical
    sub.band_grammar = result.grammar
    sub.feedback = result.feedback
    sub.features = result.features
    sub.scorer = result.scorer
    sub.issues = issues
    sub.status = Submission.Status.DONE
    sub.error = ""
    sub.save()
    return "done"
