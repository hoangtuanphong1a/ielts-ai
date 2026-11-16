# IELTS AI Learning System

Hệ thống luyện IELTS: chấm Writing bằng NLP/ML, ôn từ vựng bằng spaced repetition (SM-2), theo dõi tiến độ.

Stack: Django 5 + DRF + SimpleJWT · React 18 + Vite · scikit-learn.

## Cấu trúc

```
ielts-ai/
├── backend/
│   ├── config/          settings, urls
│   ├── accounts/        đăng ký, JWT, /me
│   ├── writing/         đề, bài nộp, chấm điểm, tiến độ, lệnh seed
│   ├── vocab/           từ vựng, flashcard, thuật toán SM-2 (srs.py)
│   └── ml/              features.py (NLP), scorer.py (chấm), train.py (train model)
├── frontend/src/
│   ├── api.js, auth.jsx JWT + refresh token
│   ├── pages/           Login, Dashboard, WritingList, WritingEditor, SubmissionResult, Vocab
│   └── components/      BandBar
└── docs/
    ├── feature/tingnang.md  đặc tả tính năng (PRD)
    ├── TASKS.md             task list theo phase
    └── PRACTICE.md          lộ trình tự gõ lại code
```

## Chạy

Hạ tầng (PostgreSQL cổng 5434, Redis cổng 6380), cần Docker Desktop đang chạy:

```bash
cp .env.example .env           # lần đầu; sửa DJANGO_SECRET_KEY
docker compose up -d
```

Muốn chạy không cần Docker: đặt `DB_ENGINE=sqlite` trong `.env`. Test (`manage.py test`) luôn dùng SQLite.

Backend (cổng 8000):

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py seed          # 4 đề Writing + 12 từ vựng
python manage.py createsuperuser   # tuỳ chọn, cho /admin
python manage.py runserver
```

Worker chạy nền (Celery, cần Redis): gửi email đặt lại mật khẩu, sau này chấm bài.

```bash
cd backend
celery -A config worker -l info --pool=solo   # Windows cần --pool=solo
```

Không muốn chạy worker khi dev: đặt `CELERY_EAGER=1` trong `.env`, task chạy ngay trong request.

Tài liệu API: http://127.0.0.1:8000/api/docs/ (Swagger), schema tại `/api/schema/`.

Frontend (cổng 5173, proxy `/api` sang 8000):

```bash
cd frontend
npm install
npm run dev
```

Mở http://localhost:5173, đăng ký tài khoản rồi dùng.

Test backend: `python manage.py test` (10 test: NLP features, làm tròn band, SM-2, luồng API).

## API

| Method | Path | Mô tả |
|---|---|---|
| POST | `/api/auth/register/` | đăng ký |
| POST | `/api/auth/token/` | lấy access + refresh |
| POST | `/api/auth/token/refresh/` | làm mới access |
| GET | `/api/auth/me/` | user hiện tại |
| GET | `/api/writing/prompts/` | danh sách đề |
| GET/POST | `/api/writing/submissions/` | bài của mình / nộp bài (tự chấm) |
| GET | `/api/writing/submissions/{id}/` | kết quả chi tiết |
| GET | `/api/writing/progress/` | lịch sử band + trung bình |
| GET | `/api/vocab/cards/due/` | thẻ cần ôn hôm nay (tối đa 10) |
| POST | `/api/vocab/cards/{id}/review/` | `{ "quality": 0-5 }` |

## Chấm điểm hoạt động thế nào

1. `ml/features.py` trích 11 đặc trưng: số từ/câu/đoạn, độ dài câu, chỉ số Guiraud (đa dạng từ), tỉ lệ từ dài, từ nối, câu phức, lặp từ, độ bám đề.
2. `ml/scorer.py` quy đổi đặc trưng ra 4 tiêu chí (TR, CC, LR, GRA) bằng heuristic, rồi làm tròn theo quy tắc IELTS.
3. Nếu có `ml/artifacts/band_model.joblib` thì band overall do model ML dự đoán (TF-IDF + đặc trưng thủ công → Ridge).

Train model từ CSV bài luận đã chấm (ví dụ Kaggle "IELTS Writing Scored Essays Dataset"):

```bash
cd backend
python -m ml.train --csv path/to/essays.csv --text-col Essay --label-col Overall
```

Giới hạn: heuristic không bắt lỗi ngữ pháp/chính tả thật. Điểm chỉ là ước lượng tham khảo, chưa được hiệu chỉnh với giám khảo.
