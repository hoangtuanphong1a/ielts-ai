# IELTS AI — Task List

Nguồn yêu cầu: [feature/tingnang.md](feature/tingnang.md) (mã tính năng AUTH-xx, WRI-xx… tham chiếu tới đó).
Cập nhật: 2026-11-11.

## Quy ước

| Cột | Ý nghĩa |
|---|---|
| Size | S ≈ ½ ngày · M ≈ 1–2 ngày · L ≈ 3–5 ngày |
| Phụ thuộc | Task phải xong trước |
| Trạng thái | `[ ]` chưa · `[~]` đang làm · `[x]` xong |

## Mặc định đang áp dụng (đổi được)

Các quyết định ở mục 11 của PRD chưa chốt, task list tạm dùng:

| # | Quyết định | Mặc định |
|---|---|---|
| D1–D2 | Frontend | **Chốt 2026-11-12: giữ JavaScript + CSS thuần** (token CSS, xem design-system/MASTER.md) |
| D3 | Database | PostgreSQL + Redis chạy bằng Docker Compose |
| D4 | Màu lỗi | Giữ tuyệt đối 5 màu; lỗi = icon + viền navy + chữ |
| — | Logo | Vẽ lại icon vô cực SVG theo 5 màu; tên tạm "IELTS AI" |
| D5 | LLM | Để Phase 2; trước đó chỉ NLP offline |
| D6 | Dataset ML | Chưa có → band vẫn heuristic tới Phase 3 |
| D7 | Nội dung L/R/S | Tự soạn bài mẫu, không dùng đề Cambridge |

---

## Phase 0 — Nền móng và thiết kế

Mục tiêu: chốt hệ thiết kế và hạ tầng trước khi làm thêm màn hình.

| ID | Task | Tính năng | Size | Phụ thuộc | Tiêu chí xong | Trạng thái |
|---|---|---|---|---|---|---|
| T0.1 | Kiến trúc thông tin: sitemap, luồng chính, `use-cases.md` | — | S | — | Có sitemap toàn bộ trang theo vai trò; use case cho Student / Admin | [ ] |
| T0.2 | Hướng thiết kế bằng skill `design-taste-frontend` → kiểm màu / font / tương phản bằng `ui-ux-pro-max` | — | S | T0.1 | Có `docs/design-system/MASTER.md`: token màu từ 5 màu, typography, spacing, radius, bảng contrast | [ ] |
| T0.3 | Spec UI: layout 375 / 768 / 1024 / 1440, trạng thái loading / empty / error | — | M | T0.2 | Mỗi màn hình MVP có bố cục theo breakpoint | [ ] |
| T0.4 | Logo SVG + favicon theo bảng màu | — | S | T0.2 | `logo.svg`, `favicon.svg`, rõ ở 16–32 px | [ ] |
| T0.5 | ~~Chuyển frontend sang TypeScript + Tailwind~~ Bỏ: giữ JS + CSS (D1–D2) | — | — | — | — | bỏ |
| T0.6 | App shell: sidebar / topbar responsive, điều hướng theo vai trò | — | M | T0.3, T0.5 | Menu thu gọn trên mobile; route bảo vệ theo role | [ ] |
| T0.7 | Docker Compose: PostgreSQL, Redis; settings đọc `.env` | — | S | — | `docker compose up` + `migrate` chạy được; SQLite chỉ còn cho test | [x] |
| T0.8 | Celery worker + drf-spectacular (Swagger tại `/api/docs/`) | — | S | T0.7 | Task mẫu chạy nền; Swagger hiển thị đủ endpoint | [x] |
| T0.9 | RBAC: Student / Teacher / Admin + `Profile` (accounts/models.py, permissions.HasRole) | AUTH-10 | M | T0.7 | Permission class theo role; test API chặn sai quyền | [x] |

---

## Phase 1 — Core Platform

Mục tiêu: học viên luyện được đủ 4 kỹ năng; Listening / Reading chấm tự động.

| ID | Task | Tính năng | Size | Phụ thuộc | Tiêu chí xong | Trạng thái |
|---|---|---|---|---|---|---|
| T1.1 | Profile + Learning Preferences (band mục tiêu, ngày thi, phút/ngày) | AUTH-07, AUTH-09 | M | T0.9 | Sửa được hồ sơ; onboarding hỏi mục tiêu sau đăng ký | [x] |
| T1.2 | Đổi mật khẩu, quên / đặt lại mật khẩu (email console khi dev) | AUTH-05, AUTH-06 | M | T0.9 | Link reset hết hạn sau 1 giờ; có test | [x] |
| T1.3 | Mô hình nội dung chung: Topic, Question (type + JSON schema đáp án), Attempt, Answer | — | L | T0.7 | 1 schema dùng chung cho mọi dạng câu L / R | [ ] |
| T1.4 | Bộ render câu hỏi: MCQ, T/F/NG, Y/N/NG, Matching, Completion, Labelling (xong 6 dạng trong `components/Reading.jsx`; còn Diagram Labelling) | LIS-02, REA-02 | L | T1.3, T0.6 | Mỗi dạng có component + test chấm | [ ] |
| T1.5 | Reading: thư viện passage, màn làm bài 2 cột, timer, chấm + quy đổi band (app `reading`, 2 bài đọc gốc, "Show in passage", điểm yếu theo dạng câu vào `coach`) | REA-01, REA-03, REA-06 | L | T1.4 | Nộp bài ra số câu đúng, band, giải thích | [x] |
| T1.6 | Listening: upload audio, player (tốc độ, tua), section 1–4, chấm, transcript sau nộp | LIS-01, LIS-03, LIS-05, LIS-06 | L | T1.4 | Nghe – làm – nộp – xem đáp án chạy trọn | [ ] |
| T1.7 | Writing nâng cấp: timer, nháp lưu server, lọc ngân hàng đề | WRI-02, WRI-04, WRI-05 | M | T0.6 | Nháp khôi phục được trên máy khác | [ ] |
| T1.8 | Speaking: thư viện chủ đề, Part 1/2/3, timer chuẩn bị, ghi âm, nghe lại, upload | SPE-01 → SPE-04 | L | T0.6, T0.7 | Ghi âm lưu server, nghe lại được | [ ] |
| T1.9 | Vocabulary nâng cấp: thư viện lọc topic / band, chi tiết từ (IPA, đồng nghĩa, collocation) | VOC-01, VOC-02 | M | T0.6 | Trang chi tiết từ đủ trường | [ ] |
| T1.10 | Dashboard v2: band hiện tại / mục tiêu, 4 kỹ năng, mục tiêu hôm nay, hoạt động gần đây | DASH-01 → DASH-03, DASH-05 | M | T1.1, T1.5, T1.6 | Số liệu lấy từ attempt thật; có trạng thái rỗng | [ ] |
| T1.11 | Admin: quản lý nội dung (passage, audio, câu hỏi, đề W/S, từ vựng) + dashboard số liệu | ADM-01 → ADM-03 | M | T1.3 | Admin tạo được 1 bài Reading hoàn chỉnh không cần code | [ ] |
| T1.12 | Seed nội dung mẫu: 3 Reading, 2 Listening, 10 đề Writing, 15 đề Speaking, 200 từ | — | M | T1.3 | Lệnh `seed` nạp đủ | [ ] |

---

## Phase 2 — AI Integration

| ID | Task | Tính năng | Size | Phụ thuộc | Tiêu chí xong | Trạng thái |
|---|---|---|---|---|---|---|
| T2.1 | Chấm Writing chạy nền (Celery) + trạng thái "đang chấm" | WRI-09 | S | T0.8 | Nộp bài trả về ngay; kết quả cập nhật khi xong | [x] |
| T2.2 | Pipeline spaCy: POS, phân tích từ vựng theo AWL / mức từ (tần suất wordfreq, thay CEFR) | WRI-11 | M | T2.1 | Lexical Resource dùng đặc trưng mới | [x] |
| T2.3 | Kiểm tra ngữ pháp / chính tả, đánh dấu lỗi trên bài (LanguageTool + spaCy hoà hợp S-V) | WRI-10 | M | T2.1 | Lỗi hiện đúng vị trí, có gợi ý sửa | [x] |
| T2.4 | Độ bám đề + mạch lạc bằng Sentence-BERT (MiniLM qua fastembed/ONNX: lạc đề, đoạn lạc đề, đoạn lặp ý) | WRI-13 | M | T2.2 | Task Response, Coherence dùng embedding | [x] |
| T2.5 | LLM service: nhận xét, viết lại câu yếu; log `ai_requests`; rate limit | WRI-12, ADM-07 | M | T2.1 | Có giới hạn lượt / ngày; log chi phí | [ ] |
| T2.6 | Speech-to-Text (Whisper) + phân tích nói: tốc độ, ngắt nghỉ, từ đệm | SPE-05, SPE-06 | L | T1.8 | Transcript + chỉ số fluency | [ ] |
| T2.7 | Ước lượng band Speaking 4 tiêu chí | SPE-08 | M | T2.6 | Kết quả có band + nhận xét | [ ] |
| T2.8 | AI Assistant (chatbot IELTS) | AIL-06 | M | T2.5 | Trả lời có ngữ cảnh học viên | [ ] |

---

## Phase 3 — Machine Learning

| ID | Task | Tính năng | Size | Phụ thuộc | Tiêu chí xong | Trạng thái |
|---|---|---|---|---|---|---|
| T3.1 | Thu thập dataset Writing có điểm; train + đánh giá Band Prediction (MAE, ±0.5) | WRI-09 | M | D6 | Model lưu version; báo cáo MAE | [ ] |
| T3.2 | Placement Test thích ứng + Level Classification | AIL-01, AIL-02 | L | T1.5, T1.6, T2.1 | Ra band ước lượng 4 kỹ năng | [ ] |
| T3.3 | Weakness Detection theo kỹ năng / dạng câu (app `coach`: nhóm lỗi + đặc trưng NLP + tiêu chí) | DASH-06 | M | T1.10 | Top 3 điểm yếu có số liệu | [x] |
| T3.4 | Study Plan cá nhân hoá + cập nhật theo tuần (kế hoạch "hôm nay" + trang `/plan`: ngày đã qua hiện việc đã làm thật, ngày tới xếp theo quy tắc, xoay vòng điểm yếu) | AIL-03, AIL-04 | L | T3.2, T3.3 | Lịch tuần sinh tự động | [x] |
| T3.5 | Recommendation engine (content-based trước: đề chưa làm, rồi đề band thấp nhất) | AIL-05, DASH-07 | M | T3.3 | Đề xuất bài dựa trên điểm yếu | [x] |
| T3.6 | Quản lý version model, đánh giá định kỳ | ADM-06 | M | T3.1 | Đổi model không cần deploy lại | [ ] |

---

## Phase 4 — Learning Analytics & Mock Test

| ID | Task | Tính năng | Size | Phụ thuộc | Tiêu chí xong | Trạng thái |
|---|---|---|---|---|---|---|
| T4.1 | Biểu đồ: band theo thời gian (line), 4 kỹ năng (radar) | ANA-01, ANA-02 | M | T1.10 | Recharts, màu theo token | [ ] |
| T4.2 | Heatmap hoạt động, thời gian học, độ chính xác theo dạng câu | ANA-03 → ANA-05 | M | T4.1 | Đủ 3 biểu đồ, có trạng thái rỗng | [ ] |
| T4.3 | Phân tích lỗi + tăng trưởng từ vựng + mastery | ANA-06, ANA-07, VOC-07 | M | T2.3 | Hiển thị theo tuần | [ ] |
| T4.4 | Dự đoán band tại ngày thi | ANA-09 | M | T3.1 | Có khoảng tin cậy | [ ] |
| T4.5 | Mock Test đầy đủ: điều hướng, tự lưu, tự nộp, review | MOCK-01 → MOCK-05 | L | T1.5, T1.6, T1.7, T1.8 | Mô phỏng 1 bài thi trọn vẹn | [ ] |
| T4.6 | Vocabulary Quiz + sổ từ cá nhân | VOC-05, VOC-06 | M | T1.9 | Thêm từ từ bài đọc vào sổ | [ ] |
| T4.7 | Chế độ học & trò chơi từ danh sách từ: Learn, Listen & Type, Say It, Fill the Gap, Match (tham khảo LexisLift) | VOC-09 | L | T4.6, T1.9 | Mỗi chế độ cập nhật SM-2; chơi được trên mobile | [ ] |

---

## Phase 5 — Production & Expansion

| ID | Task | Tính năng | Size | Phụ thuộc | Trạng thái |
|---|---|---|---|---|---|
| T5.1 | Teacher: lớp, giao bài, chấm và nhận xét | TEA | L | T0.9 | [ ] |
| T5.2 | Notification: in-app + email, tuỳ chỉnh bật / tắt | NOTI | M | T0.8 | [ ] |
| T5.3 | Gamification: XP, streak, huy hiệu, leaderboard | GAM, DASH-04 | M | T1.10 | [ ] |
| T5.4 | Google Sign-in, xác thực email, avatar | AUTH-03, AUTH-04, AUTH-08 | M | T1.1 | [ ] |
| T5.5 | Subscription & Payment | PAY | L | — | [ ] |
| T5.6 | Deploy: Docker, Nginx, backup DB, giám sát | — | M | T0.7 | [ ] |

---

## Thứ tự đề xuất bắt đầu

1. **T0.1 → T0.2 → T0.3**: chốt cấu trúc và thiết kế (chỉ tài liệu, chưa code).
2. **T0.5, T0.7** làm song song: chuyển TS + Tailwind và Postgres.
3. **T0.6, T0.9** rồi vào Phase 1.
