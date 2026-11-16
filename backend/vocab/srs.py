"""Thuật toán lặp lại ngắt quãng SM-2 (SuperMemo 2).

quality: 0-5 (0 = quên hẳn, 5 = nhớ ngay).
Trả về (repetitions, interval_days, ease_factor) mới.
"""


def sm2(quality: int, repetitions: int, interval: int, ease: float) -> tuple[int, int, float]:
    if not 0 <= quality <= 5:
        raise ValueError("quality must be between 0 and 5")

    if quality < 3:
        # Trả lời sai -> học lại từ đầu
        repetitions = 0
        interval = 1
    else:
        if repetitions == 0:
            interval = 1
        elif repetitions == 1:
            interval = 6
        else:
            interval = round(interval * ease)
        repetitions += 1

    ease = ease + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
    ease = max(1.3, ease)
    return repetitions, interval, ease
