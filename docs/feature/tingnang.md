# IELTS AI Learning System — Đặc tả tính năng (PRD)

| | |
|---|---|
| Phiên bản | 1.0 |
| Ngày | 2026-11-11 |
| Trạng thái | Bản nháp — chờ chốt phạm vi |
| Bản gốc | [tingnang.original.md](tingnang.original.md) |

---

## 1. Tổng quan

### 1.1. Tầm nhìn

> **Learn smarter. Practice better. Achieve your target IELTS band.**

IELTS AI Learning System là nền tảng web học và luyện thi IELTS, ứng dụng NLP và Machine Learning để đánh giá năng lực, chấm bài, phát hiện điểm yếu và cá nhân hoá lộ trình cho từng học viên.

### 1.2. Mục tiêu

| # | Mục tiêu | Đo bằng |
|---|---|---|
| G1 | Đánh giá trình độ đầu vào | Placement test cho ra band ước lượng 4 kỹ năng |
| G2 | Chấm Writing và Speaking tự động | Band ước lượng theo 4 tiêu chí IELTS + nhận xét chi tiết |
| G3 | Chỉ ra lỗi và cách sửa | Danh sách lỗi ngữ pháp, từ vựng, câu yếu kèm gợi ý |
| G4 | Cá nhân hoá lộ trình | Kế hoạch học tuần, đề xuất bài theo điểm yếu |
| G5 | Theo dõi và dự đoán tiến độ | Lịch sử band, dự đoán khả năng đạt band mục tiêu |

### 1.3. Ngoài phạm vi (phiên bản đầu)

- Cấp chứng chỉ hay điểm IELTS chính thức.
- Ứng dụng di động native (chỉ web responsive).
- Lớp học trực tuyến có video thời gian thực.

### 1.4. Tuyên bố về điểm số

Mọi điểm do hệ thống tạo ra là **Estimated Band Score**, không phải điểm IELTS chính thức. Độ tin cậy của mô hình phụ thuộc vào tập dữ liệu bài làm có điểm do giám khảo con người gán nhãn.

---

## 2. Người dùng và phân quyền

| Vai trò | Mô tả | Quyền chính |
|---|---|---|
| Student | Học viên luyện thi | Học, làm bài, thi thử, xem kết quả và tiến độ của mình |
| Teacher | Giáo viên / tutor | Quản lý lớp, giao bài, chấm và nhận xét bài học viên |
| Admin | Quản trị nền tảng | Quản lý người dùng, nội dung, đề thi, cấu hình AI |

Phiên bản đầu ưu tiên Student và Admin; Teacher thuộc giai đoạn mở rộng.

---

## 3. Quy ước trong tài liệu

**Độ ưu tiên**

| Mức | Ý nghĩa |
|---|---|
| P0 | Bắt buộc cho MVP |
| P1 | Giai đoạn AI / ML (Phase 2–4) |
| P2 | Mở rộng, thương mại hoá (Phase 5) |

**Trạng thái** (so với source hiện tại trong repo)

| Ký hiệu | Ý nghĩa |
|---|---|
| Có | Đã chạy được |
| Một phần | Có bản đơn giản, cần nâng cấp |
| Chưa | Chưa làm |

---

## 4. Đặc tả chức năng

### 4.1. Tài khoản và xác thực (AUTH)

| Mã | Tính năng | Mô tả | Ưu tiên | Trạng thái |
|---|---|---|---|---|
| AUTH-01 | Register | Đăng ký bằng username, email, mật khẩu | P0 | Có |
| AUTH-02 | Login / Logout | Đăng nhập JWT (access + refresh), đăng xuất | P0 | Có |
| AUTH-03 | Google Sign-in | Đăng nhập bằng tài khoản Google (OAuth 2.0) | P1 | Chưa |
| AUTH-04 | Email Verification | Xác thực email sau đăng ký | P1 | Chưa |
| AUTH-05 | Forgot / Reset Password | Gửi link đặt lại mật khẩu qua email | P0 | Chưa |
| AUTH-06 | Change Password | Đổi mật khẩu khi đã đăng nhập | P0 | Chưa |
| AUTH-07 | User Profile | Xem, sửa thông tin cá nhân | P0 | Một phần (chỉ xem `/me`) |
| AUTH-08 | Avatar | Tải lên, cắt, đổi ảnh đại diện | P1 | Chưa |
| AUTH-09 | Learning Preferences | Band mục tiêu, ngày thi dự kiến, thời gian học mỗi ngày | P0 | Chưa |
| AUTH-10 | Role Management | Phân quyền Student / Teacher / Admin | P0 | Một phần (chỉ superuser) |
| AUTH-11 | Account Lock | Admin khoá / mở khoá tài khoản | P1 | Chưa |

### 4.2. Student Dashboard (DASH)

Màn hình đầu tiên sau khi đăng nhập, trả lời 3 câu hỏi: *Tôi đang ở đâu? Tôi yếu gì? Hôm nay học gì?*

| Mã | Tính năng | Mô tả | Ưu tiên | Trạng thái |
|---|---|---|---|---|
| DASH-01 | Current vs Target Band | Band hiện tại so với band mục tiêu | P0 | Một phần (chỉ band TB Writing) |
| DASH-02 | Skill Performance | Điểm từng kỹ năng L / R / W / S | P0 | Chưa |
| DASH-03 | Daily Goals | Mục tiêu học hôm nay và mức hoàn thành | P0 | Chưa |
| DASH-04 | Study Streak | Chuỗi ngày học liên tục | P1 | Chưa |
| DASH-05 | Recent Activities | Hoạt động gần đây | P0 | Một phần (bài Writing gần đây) |
| DASH-06 | Weakness Analysis | Tóm tắt điểm yếu theo kỹ năng / dạng câu hỏi | P1 | Chưa |
| DASH-07 | Recommended Lessons | Bài được đề xuất | P1 | Chưa |
| DASH-08 | Upcoming Study Plan | Lịch học sắp tới | P1 | Chưa |
| DASH-09 | Achievements | Thành tích, huy hiệu | P2 | Chưa |

### 4.3. Listening (LIS)

| Mã | Tính năng | Mô tả | Ưu tiên | Trạng thái |
|---|---|---|---|---|
| LIS-01 | Audio Player | Phát / tạm dừng, tua, chỉnh tốc độ | P0 | Chưa |
| LIS-02 | Question Types | Multiple Choice, Fill in the Blanks, Matching, Map Labelling, Form / Note / Sentence Completion | P0 | Chưa |
| LIS-03 | Section Practice | Luyện riêng Section 1–4 | P0 | Chưa |
| LIS-04 | Full Listening Test | Bài thi đủ 4 section, tính giờ | P1 | Chưa |
| LIS-05 | Auto Grading | Chấm tự động, quy đổi số câu đúng ra band | P0 | Chưa |
| LIS-06 | Answer Review | Đáp án, giải thích, transcript (bật sau khi nộp) | P0 | Chưa |
| LIS-07 | Mistake Tracking | Lưu câu sai để ôn lại | P1 | Chưa |

AI / ML: phân tích dạng câu hỏi hay sai; đề xuất bài nghe theo trình độ; đánh giá độ khó transcript (từ vựng, tốc độ nói).

### 4.4. Reading (REA)

| Mã | Tính năng | Mô tả | Ưu tiên | Trạng thái |
|---|---|---|---|---|
| REA-01 | Passage Library | Thư viện bài đọc Academic / General Training, lọc theo chủ đề và độ khó | P0 | Chưa |
| REA-02 | Question Types | Multiple Choice, True/False/Not Given, Yes/No/Not Given, Matching Headings / Information / Features, Sentence / Summary Completion, Diagram Labelling | P0 | Chưa |
| REA-03 | Reading Timer | Đếm giờ theo bài / theo test | P0 | Chưa |
| REA-04 | Highlight & Lookup | Đánh dấu từ khoá, tra từ ngay trong bài đọc | P1 | Xong: tra từ (WordNet offline, nghĩa xếp theo ngữ cảnh) + lưu thẻ có câu ngữ cảnh; đánh dấu cụm từ (lưu theo bài đọc trong trình duyệt) |
| REA-05 | Full Reading Test | Bài thi đủ 3 passage, 60 phút | P1 | Chưa |
| REA-06 | Auto Grading & Explanation | Chấm tự động, giải thích đáp án, chỉ vị trí trong passage | P0 | Chưa |

AI / NLP: phân loại độ khó văn bản (readability); trích xuất từ vựng theo chủ đề; đề xuất passage theo trình độ.

### 4.5. Writing (WRI) — module trọng tâm AI

| Mã | Tính năng | Mô tả | Ưu tiên | Trạng thái |
|---|---|---|---|---|
| WRI-01 | Task 1 / Task 2 Practice | Luyện theo từng task | P0 | Có |
| WRI-02 | Question Bank | Ngân hàng đề, lọc theo task, dạng đề, chủ đề | P0 | Một phần (4 đề mẫu, chưa lọc) |
| WRI-03 | Essay Editor | Soạn bài, đếm từ realtime | P0 | Có |
| WRI-04 | Writing Timer | 20 phút (Task 1) / 40 phút (Task 2), có thể tắt | P0 | Chưa |
| WRI-05 | Save Draft | Lưu nháp tự động | P0 | Một phần (localStorage, chưa lưu server) |
| WRI-06 | Submission History | Lịch sử bài nộp và điểm | P0 | Có |
| WRI-07 | Sample Essays | Bài mẫu theo band | P1 | Chưa |
| WRI-08 | Essay Comparison | So sánh 2 lần viết cùng đề | P1 | Chưa |
| WRI-09 | AI Band Scoring | Band overall + 4 tiêu chí | P0 | Một phần (heuristic NLP) |
| WRI-10 | Grammar & Spelling Check | Đánh dấu lỗi trực tiếp trên bài | P1 | Chưa |
| WRI-11 | Vocabulary Suggestions | Gợi ý từ thay thế, từ học thuật | P1 | Chưa |
| WRI-12 | Sentence Rewriting | Gợi ý viết lại câu yếu | P1 | Chưa |
| WRI-13 | Coherence & Cohesion Analysis | Đánh giá liên kết đoạn, từ nối | P1 | Một phần (đếm từ nối) |
| WRI-14 | Repetition Detection | Phát hiện lặp từ | P0 | Một phần (chỉ từ lặp nhiều nhất) |

**Tiêu chí chấm (theo band descriptors IELTS)**

| Tiêu chí | Hệ thống đánh giá |
|---|---|
| Task Achievement / Response | Mức độ trả lời đúng và đủ yêu cầu đề |
| Coherence & Cohesion | Bố cục, logic, liên kết câu và đoạn |
| Lexical Resource | Độ rộng và độ chính xác của từ vựng |
| Grammatical Range & Accuracy | Độ đa dạng và độ chính xác ngữ pháp |

**Kết quả trả về:** band overall; band từng tiêu chí; danh sách lỗi ngữ pháp; gợi ý từ vựng; câu yếu kèm bản sửa; nhận xét tổng hợp; bài tập đề xuất.

### 4.6. Speaking (SPE)

| Mã | Tính năng | Mô tả | Ưu tiên | Trạng thái |
|---|---|---|---|---|
| SPE-01 | Part 1 / 2 / 3 Practice | Luyện từng phần, câu hỏi ngẫu nhiên theo chủ đề | P0 | Chưa |
| SPE-02 | Topic Library | Thư viện chủ đề và cue card | P0 | Chưa |
| SPE-03 | Preparation Timer | 1 phút chuẩn bị Part 2, 2 phút nói | P0 | Chưa |
| SPE-04 | Recording & Playback | Ghi âm và nghe lại trên trình duyệt | P0 | Chưa |
| SPE-05 | Speech-to-Text | Chuyển giọng nói thành transcript (Whisper) | P1 | Chưa |
| SPE-06 | Speaking Analysis | Độ trôi chảy (tốc độ, ngắt nghỉ), từ đệm, từ vựng, ngữ pháp | P1 | Chưa |
| SPE-07 | Pronunciation Feedback | Nhận xét phát âm | P1 | Chưa |
| SPE-08 | Speaking Band Estimation | Band theo 4 tiêu chí: Fluency & Coherence, Lexical Resource, Grammatical Range & Accuracy, Pronunciation | P1 | Chưa |
| SPE-09 | AI Speaking Partner | Hội thoại với AI, AI hỏi câu tiếp theo | P2 | Chưa |

### 4.7. Vocabulary (VOC)

| Mã | Tính năng | Mô tả | Ưu tiên | Trạng thái |
|---|---|---|---|---|
| VOC-01 | Vocabulary Library | Thư viện từ theo chủ đề và band | P0 | Một phần (12 từ, có topic) |
| VOC-02 | Word Detail | Định nghĩa, IPA, phát âm, ví dụ, đồng / trái nghĩa, collocation | P0 | Một phần (định nghĩa + ví dụ) |
| VOC-03 | Flashcards | Thẻ lật | P0 | Có |
| VOC-04 | Spaced Repetition | Ôn tập ngắt quãng (SM-2) | P0 | Có |
| VOC-05 | Personal Word Book | Sổ từ cá nhân, thêm từ khi đang đọc / nghe | P1 | Chưa |
| VOC-06 | Vocabulary Quiz | Trắc nghiệm, điền từ | P1 | Chưa |
| VOC-07 | Mastery Tracking | Mức độ ghi nhớ từng từ | P1 | Một phần (dữ liệu SM-2 có, chưa hiển thị) |
| VOC-08 | Academic Word List | Bộ AWL | P1 | Chưa |
| VOC-09 | Study Modes & Games | Học một danh sách từ qua nhiều chế độ luyện 4 kỹ năng (xem bảng dưới) | P1 | Chưa |

**VOC-09: chế độ học và trò chơi từ danh sách từ** (tham khảo cách tổ chức của LexisLift, không sao chép giao diện / nội dung)

| Chế độ | Kỹ năng | Cách chơi |
|---|---|---|
| Flashcards | Đọc | Lật thẻ, tự chấm mức nhớ (SM-2), đã có |
| Learn | Đọc | Trắc nghiệm nghĩa, câu sai quay lại cuối lượt |
| Listen & Type | Nghe + Viết | Nghe phát âm (TTS), gõ lại đúng chính tả |
| Say It | Nói | Đọc to từ / câu ví dụ, nhận dạng giọng nói (Web Speech API) so khớp |
| Fill the Gap | Đọc + Viết | Điền từ vào câu ví dụ theo ngữ cảnh |
| Match | Đọc | Ghép từ với nghĩa, tính giờ |
| Use It | Viết | Viết 1 câu dùng từ, AI nhận xét cách dùng (Phase 2, cần LLM) |

Kết quả mọi chế độ đổ về cùng dữ liệu SM-2 của từ, để Lunaria và lộ trình cá nhân hoá dùng chung.

AI: tạo ví dụ theo ngữ cảnh; phân biệt từ dễ nhầm; đề xuất từ theo band mục tiêu; quiz cá nhân hoá.

### 4.8. Mock Test (MOCK)

| Mã | Tính năng | Mô tả | Ưu tiên | Trạng thái |
|---|---|---|---|---|
| MOCK-01 | Full Mock Test | Thi thử đủ 4 kỹ năng, mô phỏng giao diện thi | P1 | Chưa |
| MOCK-02 | Single-skill Test | Thi riêng từng kỹ năng | P1 | Chưa |
| MOCK-03 | Exam Controls | Hướng dẫn, điều hướng câu hỏi, phiếu trả lời | P1 | Chưa |
| MOCK-04 | Auto Save & Auto Submit | Tự lưu đáp án, tự nộp khi hết giờ | P1 | Chưa |
| MOCK-05 | Results & Review | Tính band, phân tích bài thi, so sánh các lần thi | P1 | Chưa |

### 4.9. AI Learning (AIL)

| Mã | Tính năng | Mô tả | Ưu tiên | Trạng thái |
|---|---|---|---|---|
| AIL-01 | Placement Test | Kiểm tra đầu vào, câu hỏi thích ứng theo trình độ | P0 | Chưa |
| AIL-02 | Level Classification | Ước lượng band 4 kỹ năng và phân loại trình độ | P0 | Chưa |
| AIL-03 | Personalized Study Plan | Lộ trình theo band hiện tại, band mục tiêu, ngày thi | P0 | Chưa |
| AIL-04 | Dynamic Plan Update | Điều chỉnh lộ trình theo kết quả thực tế mỗi tuần | P1 | Chưa |
| AIL-05 | Recommendation Engine | Đề xuất bài học, bài tập, từ vựng, chủ đề, độ khó | P1 | Chưa |
| AIL-06 | AI Assistant (Chatbot) | Hỏi đáp IELTS, giải thích ngữ pháp / từ vựng, sửa câu, ghi nhớ ngữ cảnh học | P1 | Chưa |

**Ví dụ kết quả Placement Test**

| Kỹ năng | Band ước lượng |
|---|---|
| Listening | 6.0 |
| Reading | 6.0 |
| Writing | 5.0 |
| Speaking | 5.0 |
| **Overall** | **5.5** |

> Gợi ý: tập trung Writing và Speaking để nâng band tổng.

**Ví dụ cá nhân hoá:** học viên mục tiêu 7.0, hiện tại 5.5, Writing và Speaking yếu hơn. Hệ thống tăng tỷ trọng Writing, giao Speaking mỗi ngày, giao bài Grammar đúng loại lỗi hay mắc, theo dõi theo tuần và điều chỉnh lộ trình.

### 4.10. Progress & Analytics (ANA)

| Mã | Tính năng | Mô tả | Biểu đồ | Ưu tiên | Trạng thái |
|---|---|---|---|---|---|
| ANA-01 | Band History | Band theo thời gian | Line | P0 | Một phần (API có, chưa vẽ) |
| ANA-02 | Skill Comparison | So sánh 4 kỹ năng | Radar | P0 | Chưa |
| ANA-03 | Accuracy by Question Type | Tỷ lệ đúng theo dạng câu | Bar | P1 | Chưa |
| ANA-04 | Study Time | Thời gian học theo kỹ năng | Bar xếp chồng | P1 | Chưa |
| ANA-05 | Activity Heatmap | Lịch sử hoạt động theo ngày | Heatmap | P1 | Chưa |
| ANA-06 | Error Analysis | Phân loại lỗi thường gặp | Bar | P1 | Chưa |
| ANA-07 | Vocabulary Growth | Số từ đã thuộc theo thời gian | Line | P1 | Chưa |
| ANA-08 | Weekly / Monthly Report | Báo cáo định kỳ | — | P2 | Chưa |
| ANA-09 | Predicted Band | Dự đoán band tại ngày thi | — | P1 | Chưa |

### 4.11. Gamification (GAM) — P2

XP, level, daily / weekly challenge, huy hiệu, bảng xếp hạng, cột mốc. Tất cả trạng thái: Chưa.

### 4.12. Notification (NOTI) — P2

Thông báo trong app và email: nhắc học hằng ngày, nhắc giữ streak, nhắc bài được giao, nhắc lịch thi thử, có kết quả chấm AI, báo cáo tuần, đạt thành tích. Người dùng tự bật / tắt từng loại.

### 4.13. Admin (ADM)

| Mã | Tính năng | Mô tả | Ưu tiên | Trạng thái |
|---|---|---|---|---|
| ADM-01 | Admin Dashboard | Số người dùng, lượt làm bài, lượt gọi AI | P0 | Chưa |
| ADM-02 | User & Role Management | Quản lý người dùng, phân quyền, khoá tài khoản | P0 | Một phần (Django admin) |
| ADM-03 | Content Management | Đề Writing / Speaking, passage, audio, câu hỏi, từ vựng, ngữ pháp | P0 | Một phần (Django admin: đề Writing, từ vựng) |
| ADM-04 | Test Management | Tạo và xuất bản đề thi thử | P1 | Chưa |
| ADM-05 | Content Approval | Duyệt nội dung trước khi xuất bản | P2 | Chưa |
| ADM-06 | AI Configuration | Phiên bản model, prompt, cấu hình chấm điểm | P1 | Chưa |
| ADM-07 | AI Usage Monitoring | Số request, độ trễ, chi phí, lỗi | P1 | Chưa |
| ADM-08 | Reports & Logs | Báo cáo hệ thống, nhật ký, phản hồi người dùng | P1 | Chưa |

### 4.14. Teacher (TEA) — P2

Hồ sơ giáo viên, quản lý lớp, gán học viên, giao bài về nhà, chấm và nhận xét Writing / Speaking, theo dõi tiến độ học viên, nhắn tin với học viên, báo cáo hiệu quả giảng dạy.

### 4.15. Subscription & Payment (PAY) — P2, tuỳ chọn

Gói Free / Premium, giới hạn lượt dùng AI, tích hợp thanh toán, lịch sử giao dịch, hoá đơn, mã giảm giá.

---

## 5. NLP và Machine Learning

### 5.1. Năng lực NLP

| Năng lực | Kỹ thuật | Dùng ở |
|---|---|---|
| Tokenization, POS Tagging | spaCy | Mọi pipeline văn bản |
| Grammar & Spelling Detection | Grammar model / LanguageTool / LLM | WRI-10, SPE-06 |
| Keyword Extraction | TF-IDF, KeyBERT | Độ bám đề (WRI-09), từ vựng theo chủ đề |
| Semantic Similarity | Sentence-BERT | Task Response, coherence, paraphrase |
| Readability Analysis | Chỉ số readability | Phân loại độ khó passage, transcript |
| Topic Classification | Text classification | Gắn chủ đề cho đề và bài đọc |
| Vocabulary Analysis | Danh sách AWL, CEFR | Lexical Resource, gợi ý từ |
| Summarization | Transformer | Tóm tắt passage (tuỳ chọn) |

### 5.2. Writing Analysis Pipeline

```
Bài viết học viên
  → Tiền xử lý (chuẩn hoá, tách câu / đoạn)
  → Tokenization + POS Tagging
  → Phân tích ngữ pháp  → Phân tích từ vựng  → Phân tích mạch lạc  → Độ bám đề
  → Mô hình chấm điểm + Sinh nhận xét
  → Kết quả: band 4 tiêu chí, lỗi, gợi ý, bài tập đề xuất
```

### 5.3. Bài toán Machine Learning

| Bài toán | Loại | Mục đích | Ưu tiên |
|---|---|---|---|
| Band Prediction | Regression | Dự đoán band từ bài làm | P0 |
| Level Classification | Classification | Phân loại trình độ sau placement test | P0 |
| Weakness Detection | Classification | Xác định kỹ năng / dạng câu yếu | P1 |
| Recommendation | Content-based, Collaborative Filtering | Đề xuất bài học | P1 |
| Performance Prediction | Regression | Dự đoán band tại ngày thi | P1 |
| Exercise Difficulty | Classification / Regression | Ước lượng độ khó câu hỏi | P1 |
| Vocabulary Mastery | Classification | Dự đoán khả năng nhớ từ | P1 |
| Learner Clustering | K-Means | Phân nhóm hành vi học | P2 |
| Dropout Prediction | Classification | Phát hiện nguy cơ bỏ học | P2 |
| Adaptive Learning | Rules → Reinforcement Learning | Điều chỉnh lộ trình | P2 |

Thuật toán tham khảo: Linear / Ridge Regression, Random Forest, XGBoost, SVM, K-Means, Neural Networks, BERT / Sentence-BERT, fine-tuned Transformer.

**Nguyên tắc:** không huấn luyện mọi thứ từ đầu. Kết hợp pretrained model, ML truyền thống và dữ liệu học tập thực tế thu được trong quá trình vận hành.

---

## 6. Yêu cầu phi chức năng

| Nhóm | Yêu cầu |
|---|---|
| Bảo mật | JWT, RBAC, rate limit cho API AI, validate input, mật khẩu băm, không lộ dữ liệu giữa học viên |
| Hiệu năng | Trang chính tải < 2s; chấm Writing chạy nền (Celery), trả kết quả < 30s |
| Khả dụng | Responsive 375 / 768 / 1024 / 1440 px; đạt WCAG AA về tương phản |
| Giao diện | Tuân thủ tuyệt đối bảng màu [docs/color/palette.png](../color/palette.png) |
| Quan sát | Log request AI, theo dõi phiên bản và chất lượng model |
| Dữ liệu | Sao lưu database định kỳ; người dùng có quyền xoá dữ liệu của mình |
| Tài liệu | API docs tự sinh (drf-spectacular / Swagger) |

---

## 7. Kiến trúc hệ thống

```
┌──────────────────────────────────────────────────────────────┐
│ Frontend — React + TypeScript                                │
│ Student Dashboard · Learning · Mock Test · Admin             │
└───────────────────────────┬──────────────────────────────────┘
                            │ REST API / JWT
┌───────────────────────────▼──────────────────────────────────┐
│ Backend — Django + DRF                                       │
│ Auth · Business Logic · API · User Management                │
└──────┬─────────────┬──────────────┬──────────────┬───────────┘
       │             │              │              │
  NLP Service   ML Service     LLM Service    Speech Service
  Grammar,      Prediction,    Feedback,      Speech-to-Text,
  Semantic      Recommendation AI Tutor       Pronunciation
       │             │              │              │
┌──────▼─────────────▼──────────────▼──────────────▼───────────┐
│ Infrastructure — PostgreSQL · Redis · Celery · File Storage  │
└──────────────────────────────────────────────────────────────┘
```

| Layer | Công nghệ |
|---|---|
| Frontend | React, TypeScript, Tailwind CSS, Recharts |
| Backend | Django, Django REST Framework |
| Database / Cache | PostgreSQL, Redis |
| Background Jobs | Celery |
| NLP | spaCy, NLTK, Hugging Face |
| ML / DL | scikit-learn, XGBoost, PyTorch, Transformers |
| LLM | API-based LLM hoặc model tự triển khai |
| Speech | Whisper |
| API Docs | drf-spectacular |
| Deployment | Docker, Nginx |

---

## 8. Phân nhóm dữ liệu

| Module | Bảng chính |
|---|---|
| Authentication | users, roles, permissions |
| Student | student_profiles, learning_goals |
| Courses | courses, modules, lessons |
| IELTS Content | topics, questions, passages, audio_files |
| Listening / Reading | tests, attempts, answers |
| Writing | writing_prompts, writing_submissions, writing_feedback |
| Speaking | speaking_recordings, transcripts, speaking_feedback |
| Vocabulary | words, flashcards, vocabulary_progress |
| Mock Test | mock_tests, test_attempts, test_results |
| AI / ML | ai_requests, ai_evaluations, model_versions, predictions, recommendations |
| Analytics | learning_activities, progress_records |
| Gamification | user_xp, achievements, streaks |
| Notification | notifications, notification_preferences |
| Payment | subscriptions, transactions |

---

## 9. Lộ trình phát triển

| Phase | Tên | Nội dung | Đầu ra |
|---|---|---|---|
| 1 | Core Platform | AUTH, DASH cơ bản, Listening, Reading, nộp Writing / Speaking, Question Bank, Admin cơ bản | Học viên luyện được 4 kỹ năng, chấm tự động L / R |
| 2 | AI Integration | Chấm Writing AI, ngữ pháp & từ vựng, Speech-to-Text, chấm Speaking, AI Assistant | Nhận xét AI cho Writing và Speaking |
| 3 | Machine Learning | Band Prediction, Level Classification, Weakness Detection, Recommendation, Adaptive Learning | Lộ trình cá nhân hoá |
| 4 | Learning Analytics | Biểu đồ tiến độ, dự đoán band, tối ưu kế hoạch, phân tích thi thử, mastery từ vựng | Dashboard phân tích đầy đủ |
| 5 | Production & Expansion | Teacher, Payment, Subscription, Gamification, Notification, Deploy | Sản phẩm sẵn sàng vận hành |

---

## 10. Phạm vi MVP

Mục tiêu MVP: chứng minh được năng lực Django, React, NLP và ML — không chỉ là website CRUD.

| Module | Chức năng cần hoàn thành |
|---|---|
| Authentication | Register, Login, Profile, Learning Preferences |
| Dashboard | Band hiện tại / mục tiêu, tiến độ, thống kê |
| Listening | Practice, Quiz, Auto Grading |
| Reading | Passage, Questions, Auto Grading |
| Writing | Editor, AI Scoring, Feedback |
| Speaking | Recording, Speech-to-Text, AI Analysis |
| Vocabulary | Flashcards, Quiz, Spaced Repetition |
| AI Assistant | IELTS Chatbot |
| AI Learning | Placement Test, Personalized Study Plan |
| Machine Learning | Band Prediction, Recommendation |
| Admin | User, Question, Content Management |
| Analytics | Skill Progress, Learning History |

**Ba điểm nhấn nghiên cứu**

1. **AI Writing & Speaking Evaluation** — phân tích bài làm theo tiêu chí IELTS.
2. **Personalized Learning Recommendation** — ML phát hiện điểm yếu và đề xuất bài tập.
3. **Band Score Prediction** — dự đoán khả năng đạt band mục tiêu từ dữ liệu học tập.

---

## 11. Quyết định cần chốt

| # | Vấn đề | Hiện trạng code | Đặc tả yêu cầu |
|---|---|---|---|
| D1 | Ngôn ngữ frontend | JavaScript | TypeScript |
| D2 | CSS | CSS thuần | Tailwind CSS |
| D3 | Database | SQLite | PostgreSQL + Redis |
| D4 | Màu báo lỗi / thành công | Bảng màu chỉ có 5 sắc xanh | Giữ tuyệt đối 5 màu hay thêm 1 màu đỏ cho lỗi |
| D5 | Nguồn LLM | Chưa có | API (Claude / OpenAI…) hay model tự host |
| D6 | Dữ liệu huấn luyện | Chưa có | Nguồn bài Writing / Speaking có điểm gán nhãn |
| D7 | Nội dung Listening / Reading | Chưa có | Tự soạn, mua, hay nguồn mở (lưu ý bản quyền đề Cambridge) |

---

## 12. Tham khảo giao diện

| Màn hình | Tham khảo |
|---|---|
| Dashboard học viên | IELTS WIST, iPrep (Behance), Practet |
| Listening / Mock test | ieltsmocktest.site, tailorslabs.com |
| Reading | ieltsarena.com |
| Writing AI | speechful.ai |
| Speaking AI | spelly.online |
| Dashboard học ngôn ngữ | LEXAY (Dribbble) |
| Vocabulary | parroto.app |
| Analytics | ubitto.com |
| Admin LMS | AI Edtech LMS Dashboard (Dribbble) |

Chỉ tham khảo cấu trúc và luồng; không sao chép giao diện, thương hiệu hay nội dung.
