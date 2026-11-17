"""Xử lý video Lunaria (Seedance) thành các "act" dùng được trên web.

Chạy:  backend/.venv/Scripts/python tools/lunaria_clips.py
Vào:   docs/lunaria/demo/<n>.mp4   (cùng ảnh gốc, chế độ first+last frame)
Ra:    docs/lunaria/processed/rest.webp + <tên act>.mp4 + report.md

Mỗi khung được:
1. Hiệu chỉnh màu về khung tham chiếu (khớp mean/std từng kênh trên vùng tĩnh bên trái),
   vì model làm nền trôi từ xanh sang trắng giữa các clip -> ghép thẳng sẽ chớp màu.
2. Kiểm tra vùng tĩnh: lệch quá ngưỡng sau hiệu chỉnh = model tự thêm đồ vật (vd. chân máy quay
   trong clip 4) -> cắt clip trước chỗ đó.
"""
import json
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "docs" / "lunaria" / "demo"
OUT = ROOT / "docs" / "lunaria" / "processed"
W, H, FPS = 1280, 720, 24
STATIC = (slice(0, H), slice(0, 520))   # nửa trái: nền, không có người
ANOMALY = 6.0                            # lệch trung bình /255 trên vùng tĩnh sau hiệu chỉnh
REFERENCE = "2"                           # khung đầu clip 2 = tư thế nghỉ chung

ACTS = {  # tên act -> file nguồn (xem docs/lunaria/FRAME_VIDEO_PROMPTS.md)
    "turn-talk": "2", "point": "3", "think-proud": "4", "worried-encourage": "5",
    "surprised": "6", "typing": "7", "headphones": "8",
}


def frames(path: Path):
    cmd = ["ffmpeg", "-v", "error", "-i", str(path), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    size = W * H * 3
    while chunk := proc.stdout.read(size):
        if len(chunk) < size:
            break
        yield np.frombuffer(chunk, np.uint8).reshape(H, W, 3).astype(np.float32)
    proc.wait()


def correct(img, ref_mean, ref_std):
    region = img[STATIC].reshape(-1, 3)
    return np.clip((img - region.mean(0)) / (region.std(0) + 1e-6) * ref_std + ref_mean, 0, 255)


def encode(path: Path, images):
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-crf", "24", "-preset", "slow", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", "-an", str(path)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for img in images:
        proc.stdin.write(img.astype(np.uint8).tobytes())
    proc.stdin.close()
    proc.wait()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ref = next(frames(SRC / f"{REFERENCE}.mp4"))
    ref_region = ref[STATIC].reshape(-1, 3)
    ref_mean, ref_std = ref_region.mean(0), ref_region.std(0)
    Image.fromarray(ref.astype(np.uint8)).save(OUT / "rest.webp", quality=90)

    report = []
    for act, src in ACTS.items():
        kept, cut_at = [], None
        for i, img in enumerate(frames(SRC / f"{src}.mp4")):
            fixed = correct(img, ref_mean, ref_std)
            residual = float(np.abs(fixed[STATIC] - ref[STATIC]).mean())
            if residual > ANOMALY:
                cut_at = i
                break
            kept.append(fixed)
        if cut_at is not None:
            kept = kept[: max(0, cut_at - FPS // 2)]  # bỏ thêm 0.5s trước chỗ lỗi
        encode(OUT / f"{act}.mp4", kept)
        end_gap = float(np.abs(kept[-1] - ref).mean()) if kept else None
        report.append({
            "act": act, "source": f"{src}.mp4", "seconds": round(len(kept) / FPS, 2),
            "cut_at_second": None if cut_at is None else round(cut_at / FPS, 2),
            "ends_near_rest": end_gap is not None and end_gap < 8, "end_gap": round(end_gap or 0, 1),
            "size_kb": round((OUT / f"{act}.mp4").stat().st_size / 1024),
        })
        print(report[-1])
    (OUT / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
