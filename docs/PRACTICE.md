# Lộ trình tự gõ lại code

Code mẫu đã chạy được (10 test pass, frontend build OK). Cách luyện: đổi tên file gốc thành `*.bak`, gõ lại từ đầu, chạy test để kiểm tra, xong thì xoá `.bak`.

Thứ tự từ dễ đến khó. Mỗi bước có lệnh kiểm tra (chạy trong `backend/` với venv đã activate).

## 1. Thuật toán SM-2 — `backend/vocab/srs.py`

Ngắn (~25 dòng), thuần Python, không dính Django.
Điểm cần hiểu: quality < 3 thì reset; lần 1 = 1 ngày, lần 2 = 6 ngày, sau đó nhân `ease`; `ease` không dưới 1.3.

Kiểm tra: `python manage.py test ml.tests.test_ml.SM2Tests`

## 2. Làm tròn band — `round_band` trong `backend/ml/scorer.py`

1 dòng nhưng dễ sai: 6.25 → 6.5, 6.75 → 7.0, 6.1 → 6.0.

Kiểm tra: `python manage.py test ml.tests.test_ml.ScorerTests`

## 3. Trích đặc trưng NLP — `backend/ml/features.py`

Phần "NLP" chính: regex tách từ/câu/đoạn, `Counter`, tập từ nối, độ bám đề.
Gợi ý: gõ `tokenize`, `split_sentences` trước, rồi `extract_features` từng chỉ số một.

Kiểm tra: `python manage.py test ml.tests.test_ml.FeatureTests`

## 4. Pipeline ML — `backend/ml/train.py`

`FeatureUnion` ghép TF-IDF với `HandcraftedFeatures`, rồi `Ridge`. Học cách đánh giá: MAE và tỉ lệ lệch ≤ 0.5 band.
Cần CSV dữ liệu thật để chạy.

## 5. API Django — `backend/writing/views.py`, `backend/vocab/views.py`

- `perform_create`: lấy đề → gọi `score_essay` → lưu kết quả.
- `get_queryset` lọc theo `request.user` (bảo mật: user không xem bài người khác).
- `@action due/review` trong `CardViewSet`.

Kiểm tra: `python manage.py test writing`

## 6. Frontend — `frontend/src/api.js` rồi `pages/WritingEditor.jsx`

- `api.js`: gắn JWT, gặp 401 thì refresh rồi gọi lại 1 lần.
- `WritingEditor.jsx`: đếm từ bằng `useMemo`, lưu nháp vào `localStorage`, nộp bài rồi chuyển trang.

Kiểm tra: `npm run build` không lỗi, rồi `npm run dev` và thử nộp bài.
