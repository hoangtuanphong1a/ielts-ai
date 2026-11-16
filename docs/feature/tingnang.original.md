
# IELTS AI Learning System – Full Feature Specification

Với dự án này, mình đề xuất xây dựng một nền tảng IELTS AI Learning System – website học và luyện thi IELTS tích hợp Artificial Intelligence, NLP và Machine Learning.

Mục tiêu không chỉ là cung cấp bài tập IELTS mà còn xây dựng một hệ thống có khả năng:

- Đánh giá trình độ tiếng Anh của người học.
- Cá nhân hóa lộ trình học IELTS.
- Chấm điểm Writing và Speaking bằng AI.
- Phân tích lỗi sai và đưa ra gợi ý cải thiện.
- Theo dõi tiến độ và dự đoán khả năng đạt Band Score.
- Đề xuất bài học dựa trên năng lực thực tế của từng người.

Tech stack đề xuất:

Backend

Django + Django REST Framework

Frontend

React.js + TypeScript

AI / NLP

NLP, Transformers, LLM

Machine Learning

Scikit-learn, PyTorch

Database

PostgreSQL + Redis

Storage

Local / Cloud Storage

# 1. User Management & Authentication

Quản lý tài khoản và phân quyền người dùng.

| Feature               | Description                       |
| --------------------- | --------------------------------- |
| Register              | Đăng ký tài khoản            |
| Login / Logout        | Đăng nhập, đăng xuất        |
| Google Authentication | Đăng nhập Google               |
| Email Verification    | Xác thực email                  |
| Forgot Password       | Quên mật khẩu                  |
| Reset Password        | Đặt lại mật khẩu             |
| User Profile          | Quản lý thông tin cá nhân    |
| Avatar Management     | Cập nhật ảnh đại diện       |
| Change Password       | Đổi mật khẩu                  |
| Learning Preferences  | Thiết lập mục tiêu IELTS      |
| Role Management       | Phân quyền User, Admin, Teacher |
| Account Management    | Khóa, mở khóa tài khoản      |

# 2. Student Dashboard

[IELTS WIST - Complete AI Powered IELTS Preparation Platform](https://images.openai.com/static-rsc-4/RR3KAwKl-fiJxa2xIxYDmvxF7W9VNMCixXXPkFUBdUgm_Z7MvYn3o1qY5XPkkpmO75udCdwhxBK5TSBIs2icQGIyfS5FiPggr4j_JVUcqdXWNjbBlOq3k6aCnygI41G_GjGVrX2ZgTcyeisXk6VdFoju55lZdevqAcvf8tHF1nI?purpose=inline)

[Dashboard - iPrep :: Behance](https://images.openai.com/static-rsc-4/rtEMst8GZ5gFJt5YntYcVSCa9imLK8ZBcAPU-AU2O3Sm6Oivcze1bPm91sf1GaqH25Zd2SSE1UtX-wmJa0pkBbrkl8nqNk-ZWyEujJ1LV_Nw8ZjQIvxLxx1oXMTWfVdoThCj64wkYWON6IgY0y_wQ1qSPGyLr0mCkhpGP-kmSRs?purpose=inline)

[Practet - AI-Powered IELTS Preparation Platform](https://images.openai.com/static-rsc-4/KacGu0CtUwMkTF3DWC9BNNPBGvJglDBBPu2I8bbtiWN-lmXlAg_andwd-PJcXAduW3EjSlE_yacpzU96G_O6RUMmdFBE4aP4Y_s6j4O0URye_wdNgmdiNSE0MLBO9EQOPkxowW5XA75zCCwu8FV_qhQLZZaDJZ9bMFDWHE0otng?purpose=inline)

16

Đây là trang tổng quan sau khi học viên đăng nhập.

| Feature             | Description                  |
| ------------------- | ---------------------------- |
| Overview            | Tổng quan quá trình học  |
| Current Band Score  | Band Score hiện tại        |
| Target Band Score   | Band Score mục tiêu        |
| Learning Progress   | Tiến độ học tập         |
| Daily Study Goals   | Mục tiêu học mỗi ngày   |
| Study Streak        | Chuỗi ngày học liên tục |
| Recent Activities   | Hoạt động gần đây      |
| Skill Performance   | Điểm từng kỹ năng       |
| Weakness Analysis   | Phân tích điểm yếu      |
| Recommended Lessons | Bài học được đề xuất |
| Upcoming Study Plan | Lịch học sắp tới         |
| Achievement         | Thành tích học tập       |

# 3. IELTS Learning Modules

Đây là module cốt lõi của toàn bộ hệ thống, bao gồm 4 kỹ năng IELTS.

## 3.1. Listening

[IELTS Mock Test Platform | Full-Length Practice Tests](https://images.openai.com/static-rsc-4/Ly-aOLSzGcHhSAu1iVU0qTfkvs13HSZ8eCzHEukc59aIvBu9f7zEW4olHVZZSwADFPIlCGyBK8ohp1BJJh2bMhir7IfVVwy-zGYOhXGMWlWJBxfrqEDXP6nOlRX8tyCdzwGDOf0yVXt6TkVCfN5avNch6ZEzTZg4e5BchtCmAMA?purpose=inline)

[ieltsmocktest.site](https://ieltsmocktest.site/?utm_source=chatgpt.com)

| Feature             | Description                             |
| ------------------- | --------------------------------------- |
| Listening Practice  | Luyện nghe theo từng bài             |
| Audio Player        | Phát, tạm dừng audio                 |
| Audio Speed Control | Điều chỉnh tốc độ                 |
| Audio Transcript    | Hiển thị transcript khi được phép |
| Multiple Choice     | Câu hỏi trắc nghiệm                 |
| Fill in the Blanks  | Điền từ còn thiếu                  |
| Matching Questions  | Nối thông tin                         |
| Map Labelling       | Điền tên vị trí trên bản đồ    |
| Form Completion     | Hoàn thành biểu mẫu                 |
| Note Completion     | Hoàn thành ghi chú                   |
| Sentence Completion | Hoàn thành câu                       |
| Section Practice    | Luyện từng Section 1–4               |
| Full Listening Test | Thi Listening hoàn chỉnh              |
| Answer Review       | Xem đáp án và giải thích          |
| Mistake Tracking    | Lưu câu hỏi sai                      |

AI / ML có thể tích hợp:

- Phân tích nhóm câu hỏi người học thường sai.
- Xác định dạng câu hỏi có tỷ lệ chính xác thấp.
- Đề xuất bài nghe theo trình độ.
- Phân tích từ vựng và độ khó của transcript.

## 3.2. Reading

[IELTS Practice Tests Online 2026 | IELTSArena | IELTSArena](https://images.openai.com/static-rsc-4/8M-EF5xvNCy89gXovjkpucyZgRiZsiDZfPl9eGyZtK9kIBqL0eohk9pxKGrCCumsU18jwgc82j_AG9zIW-_zx2Bhub3Gd2IZq2slOM6quY22J7Gul8d0pnvC5MDL5XEyqQSoennBCyQ-5v1cvyyBiuoqP8wFEg2j2T57QXHfMuM?purpose=inline)

[ieltsarena.com](https://www.ieltsarena.com/?utm_source=chatgpt.com)

| Feature                  | Description                   |
| ------------------------ | ----------------------------- |
| Reading Practice         | Luyện đọc                  |
| Passage Library          | Thư viện bài đọc         |
| Academic Reading         | Bài đọc Academic           |
| General Training Reading | Bài đọc General Training   |
| Multiple Choice          | Trắc nghiệm                 |
| True / False / Not Given | Phân loại thông tin        |
| Yes / No / Not Given     | Nhận định quan điểm      |
| Matching Headings        | Nối tiêu đề               |
| Matching Information     | Nối thông tin               |
| Matching Features        | Nối đặc điểm             |
| Sentence Completion      | Hoàn thành câu             |
| Summary Completion       | Hoàn thành đoạn tóm tắt |
| Diagram Labelling        | Điền sơ đồ               |
| Keyword Highlighting     | Đánh dấu từ khóa         |
| Vocabulary Lookup        | Tra từ vựng                 |
| Reading Timer            | Đồng hồ đếm giờ         |
| Full Reading Test        | Thi Reading hoàn chỉnh      |
| Answer Explanation       | Giải thích đáp án        |

AI / NLP có thể tích hợp:

- NLP phân tích nội dung passage.
- Tự động trích xuất từ vựng theo chủ đề.
- Phân loại độ khó văn bản.
- Phân tích khả năng đọc hiểu.
- Đề xuất passage theo trình độ người học.

## 3.3. Writing

[Speechful - Your IELTS AI grader and English tutor](https://images.openai.com/static-rsc-4/WR61_H4nFFP2H4dP1E8CPnGdUcnKr91zpeXc_4za_whRoVwUKV_zOQ4Mi7h7o7qVQOjggFgfRE9Mgu7dlm22d4UgL9n-dqz7fomWsfGHQJug3QCuP1rc7wQpBoFokDGi9D6M1tob6M9Zd3-6LcwCOM-tXGH4N4-YXxa7kWNnfog?purpose=inline)

[speechful.ai](https://www.speechful.ai/?utm_source=chatgpt.com)

Writing là một trong những module quan trọng nhất để thể hiện năng lực AI của dự án.

| Feature                | Description                       |
| ---------------------- | --------------------------------- |
| Task 1 Practice        | Luyện Writing Task 1             |
| Task 2 Practice        | Luyện Writing Task 2             |
| Question Bank          | Ngân hàng đề thi              |
| Essay Editor           | Trình soạn thảo bài viết     |
| Word Counter           | Đếm số từ                     |
| Writing Timer          | Đồng hồ làm bài              |
| Save Draft             | Lưu bài viết nháp             |
| Submission History     | Lịch sử bài nộp               |
| Sample Essays          | Bài viết mẫu                   |
| Essay Comparison       | So sánh bài viết               |
| Writing Feedback       | Nhận phản hồi từ AI           |
| Grammar Checker        | Kiểm tra ngữ pháp              |
| Spelling Checker       | Kiểm tra chính tả              |
| Vocabulary Suggestions | Gợi ý từ vựng                 |
| Sentence Rewriting     | Gợi ý viết lại câu           |
| Coherence Analysis     | Phân tích tính mạch lạc      |
| Cohesion Analysis      | Phân tích liên kết câu       |
| Repetition Detection   | Phát hiện lặp từ              |
| Academic Vocabulary    | Phân tích từ vựng học thuật |

AI Writing Assessment – Chấm điểm theo 4 tiêu chí IELTS:

| Criterion                    | AI evaluation                             |
| ---------------------------- | ----------------------------------------- |
| Task Achievement / Response  | Mức độ trả lời đúng yêu cầu đề |
| Coherence & Cohesion         | Tính logic và liên kết                |
| Lexical Resource             | Vốn từ vựng                            |
| Grammatical Range & Accuracy | Đa dạng và chính xác ngữ pháp      |

Đầu ra AI nên bao gồm:

- Overall estimated band.
- Band score cho từng tiêu chí.
- Grammar mistakes.
- Vocabulary improvements.
- Weak sentences.
- Suggested corrections.
- Detailed feedback.
- Recommended exercises.

## 3.4. Speaking

[Spelly – AI Pronunciation Coach](https://images.openai.com/static-rsc-4/rgJTRIx92wv6mwzK0cn6k2ght6XsFmxGkBt6CcB6Kv3S-wjYH58Ufippn70gtk9sWnmcwgRY6IW3k4v_q24j-KtJ1CcW_i2zgdJ_Au3zyF3vSWAdXu7ztB2VOQciPgGkqjVfEHjHyPXsX1VyQLnXnpNvA7GAHcRmsE9PWLEiNGo?purpose=inline)

[spelly.online](https://spelly.online/blog/post/ai-tools-for-improving-speaking?utm_source=chatgpt.com)

| Feature                  | Description                          |
| ------------------------ | ------------------------------------ |
| Speaking Practice        | Luyện nói IELTS                    |
| Part 1 Practice          | Luyện Speaking Part 1               |
| Part 2 Practice          | Luyện Speaking Part 2               |
| Part 3 Practice          | Luyện Speaking Part 3               |
| Random Questions         | Câu hỏi ngẫu nhiên               |
| Topic Library            | Thư viện chủ đề                 |
| Preparation Timer        | Thời gian chuẩn bị                |
| Audio Recording          | Ghi âm câu trả lời               |
| Audio Playback           | Nghe lại câu trả lời             |
| Speech-to-Text           | Chuyển giọng nói thành văn bản |
| Transcript Review        | Xem nội dung đã nói              |
| Pronunciation Feedback   | Phản hồi phát âm                 |
| Fluency Analysis         | Phân tích độ trôi chảy         |
| Vocabulary Analysis      | Phân tích vốn từ                 |
| Grammar Analysis         | Phân tích ngữ pháp               |
| Filler Word Detection    | Phát hiện từ đệm                |
| Speaking Band Estimation | Ước lượng Band Score             |
| AI Speaking Partner      | Hội thoại với AI                  |
| Follow-up Questions      | AI đặt câu hỏi tiếp theo        |

AI Speaking Assessment – 4 tiêu chí:

1. Fluency and Coherence.
2. Lexical Resource.
3. Grammatical Range and Accuracy.
4. Pronunciation.

# 4. AI-Powered Learning System

Core AI Module

Đây là phần tạo nên sự khác biệt giữa một website học IELTS thông thường và một hệ thống IELTS AI Learning System.

## 4.1. AI Learning Assistant

[LEXAY - Language Learning Dashboard by Vektora UIUX for Vektora on Dribbble](https://images.openai.com/static-rsc-4/Ab688VoLnHojs0H2FNREwRQ-_zMZ8joWF5jMUbfd6_MkE0szmD343ckpnY3xmnRhEV6PP55gepKBX7UXONwKdNUFUeEQ0xEY-usuThLwXbLoDymySfvM37CnAvUuX3e-CU5TuqfOmQzlZjOMUCIWZ7Szaj0NI9u2-70g0uFBmts?purpose=inline)

[dribbble.com](https://dribbble.com/shots/27407318-LEXAY-Language-Learning-Dashboard?utm_source=chatgpt.com)

| Feature                  | Description                      |
| ------------------------ | -------------------------------- |
| AI Chatbot               | Chat với AI để hỏi về IELTS |
| IELTS Question Answering | Giải đáp câu hỏi IELTS      |
| Grammar Explanation      | Giải thích ngữ pháp          |
| Vocabulary Explanation   | Giải thích từ vựng           |
| Essay Feedback           | Nhận xét bài Writing          |
| Translation Assistant    | Hỗ trợ dịch thuật            |
| Sentence Improvement     | Cải thiện câu văn            |
| Example Generation       | Tạo ví dụ minh họa           |
| Study Recommendations    | Đề xuất nội dung học        |
| Contextual Learning      | AI ghi nhớ ngữ cảnh học tập |

## 4.2. AI Placement Test

Kiểm tra đầu vào để xác định trình độ người học.

| Feature                  | Description                       |
| ------------------------ | --------------------------------- |
| Initial Assessment       | Bài kiểm tra đầu vào         |
| Adaptive Questions       | Câu hỏi thích ứng trình độ |
| Skill Assessment         | Đánh giá 4 kỹ năng           |
| Grammar Assessment       | Kiểm tra ngữ pháp              |
| Vocabulary Assessment    | Kiểm tra từ vựng               |
| Reading Assessment       | Đánh giá đọc hiểu           |
| Listening Assessment     | Đánh giá nghe hiểu            |
| Writing Assessment       | Đánh giá viết                 |
| Speaking Assessment      | Đánh giá nói                  |
| Estimated IELTS Band     | Ước lượng Band Score          |
| Level Classification     | Phân loại trình độ           |
| Learning Path Generation | Tạo lộ trình học              |

Ví dụ kết quả:

Placement Test Result

Sample data

# 5.5

Estimated Overall IELTS Band

Listening

6.0

Reading

6.0

Writing

5.0

Speaking

5.0

AI Recommendation

Focus on Writing and Speaking to improve your overall performance.

## 4.3. Personalized Learning Path

AI tự động xây dựng kế hoạch học tập riêng cho từng người.

- Personalized Study Plan.
- Daily Learning Recommendations.
- Weekly Learning Schedule.
- Skill-based Learning Path.
- Weakness-based Exercises.
- Difficulty Adjustment.
- Learning Time Optimization.
- Target Band Tracking.
- Learning Progress Prediction.
- Dynamic Study Plan Updates.

Ví dụ:

Học viên có mục tiêu IELTS 7.0, trình độ hiện tại 5.5. AI nhận thấy Writing và Speaking yếu hơn Listening, Reading.

Hệ thống sẽ:

1. Tăng tỷ trọng bài luyện Writing.
2. Đề xuất Speaking Practice mỗi ngày.
3. Giao bài tập Grammar phù hợp với lỗi sai.
4. Theo dõi tiến độ theo tuần.
5. Điều chỉnh lộ trình dựa trên kết quả thực tế.

## 4.4. AI Recommendation Engine

| Feature                       | Description                       |
| ----------------------------- | --------------------------------- |
| Content Recommendation        | Đề xuất bài học              |
| Exercise Recommendation       | Đề xuất bài tập              |
| Vocabulary Recommendation     | Đề xuất từ vựng              |
| Difficulty Recommendation     | Đề xuất độ khó              |
| Topic Recommendation          | Đề xuất chủ đề              |
| Weakness-based Recommendation | Đề xuất dựa trên điểm yếu |
| Similar Exercise              | Đề xuất bài tập tương tự  |
| Next Lesson Prediction        | Dự đoán bài học tiếp theo   |

# 5. NLP – Natural Language Processing

NLP Module

Đây là module xử lý ngôn ngữ tự nhiên, đặc biệt quan trọng đối với Writing, Speaking và Vocabulary.

| Feature                  | NLP technique        | Purpose                                  |
| ------------------------ | -------------------- | ---------------------------------------- |
| Text Tokenization        | Tokenization         | Tách từ                                |
| POS Tagging              | Part-of-Speech       | Xác định loại từ                    |
| Named Entity Recognition | NER                  | Nhận diện thực thể                   |
| Text Classification      | Classification       | Phân loại nội dung                    |
| Semantic Similarity      | Sentence Embeddings  | So sánh ngữ nghĩa                     |
| Keyword Extraction       | TF-IDF / KeyBERT     | Trích xuất từ khóa                   |
| Sentiment Analysis       | Classification       | Phân tích sắc thái                   |
| Grammar Detection        | NLP / Grammar Models | Phát hiện lỗi ngữ pháp              |
| Spelling Detection       | Language Models      | Kiểm tra chính tả                     |
| Text Summarization       | Transformer          | Tóm tắt nội dung                      |
| Paraphrase Detection     | Semantic Similarity  | Nhận diện diễn đạt tương đương |
| Vocabulary Analysis      | NLP                  | Đánh giá vốn từ                     |
| Readability Analysis     | Readability Metrics  | Đánh giá độ khó văn bản          |
| Coherence Analysis       | Embeddings           | Đánh giá liên kết ý                |
| Topic Classification     | Text Classification  | Phân loại chủ đề IELTS              |

## Các NLP pipeline quan trọng

Writing Analysis Pipeline

Student Essay

Text Preprocessing

Tokenization + POS Tagging

Grammar Analysis

Vocabulary Analysis

Coherence Analysis

Task Relevance

AI Scoring + Feedback Generation

Final Assessment Result

# 6. Machine Learning Module

NLP tập trung xử lý ngôn ngữ; Machine Learning giúp hệ thống học từ dữ liệu và đưa ra dự đoán.

| Feature                        | ML approach                    | Purpose                        |
| ------------------------------ | ------------------------------ | ------------------------------ |
| IELTS Band Prediction          | Regression                     | Dự đoán Band Score          |
| Student Level Classification   | Classification                 | Phân loại trình độ        |
| Learning Behavior Analysis     | Clustering                     | Phân nhóm học viên         |
| Exercise Difficulty Prediction | Classification / Regression    | Dự đoán độ khó           |
| Student Performance Prediction | Regression                     | Dự đoán kết quả học tập |
| Weakness Detection             | Classification                 | Xác định điểm yếu        |
| Learning Recommendation        | Recommendation System          | Đề xuất bài học           |
| Adaptive Learning              | Reinforcement Learning / Rules | Điều chỉnh lộ trình       |
| Dropout Prediction             | Classification                 | Dự đoán nguy cơ bỏ học   |
| Vocabulary Mastery Prediction  | Classification                 | Dự đoán mức độ ghi nhớ  |

Một số thuật toán có thể nghiên cứu:

- Linear Regression.
- Random Forest.
- XGBoost.
- Support Vector Machine (SVM).
- K-Means Clustering.
- Collaborative Filtering.
- Content-based Filtering.
- Neural Networks.
- BERT / Sentence-BERT.
- Fine-tuned Transformer Models.

Lưu ý: Không nhất thiết phải huấn luyện tất cả model từ đầu. Có thể kết hợp pretrained models, các thuật toán ML truyền thống và dữ liệu thực tế thu thập trong quá trình học.

# 7. Vocabulary Learning System

[Common Mistakes Learning English Vocabulary | Parroto](https://images.openai.com/static-rsc-4/wmdGRS8yE65vqimO48IgME63PCVf6iw84pEFI3iGnGClP84DnRhyQuEvG8KEhxVLwCvtR3Y5XHizGerWedl3ppKpemMkKXy_oqynzUKSe3QOEc65xgc_xYJ67XOkfj20JCgkmqeZBiJVWXkkBVYheb2Ev1yikb9HS4bcBNLaaVk?purpose=inline)

[parroto.app](https://parroto.app/blog/common-mistakes-when-learning-english-vocabulary?utm_source=chatgpt.com)

| Feature                  | Description                   |
| ------------------------ | ----------------------------- |
| Vocabulary Library       | Thư viện từ vựng          |
| Vocabulary by Topic      | Từ vựng theo chủ đề      |
| Vocabulary by Band       | Từ vựng theo Band           |
| Flashcards               | Thẻ học từ                 |
| Word Definition          | Định nghĩa từ             |
| IPA Pronunciation        | Phiên âm IPA                |
| Audio Pronunciation      | Phát âm thanh               |
| Synonyms                 | Từ đồng nghĩa             |
| Antonyms                 | Từ trái nghĩa              |
| Example Sentences        | Câu ví dụ                  |
| Collocations             | Cụm từ thường đi cùng   |
| Phrasal Verbs            | Cụm động từ               |
| Academic Word List       | Từ vựng học thuật         |
| Personal Vocabulary Book | Sổ từ vựng cá nhân       |
| Vocabulary Quiz          | Kiểm tra từ vựng           |
| Spaced Repetition        | Ôn tập ngắt quãng         |
| Word Mastery Tracking    | Theo dõi khả năng ghi nhớ |

AI integration:

- AI tạo ví dụ theo ngữ cảnh.
- AI giải thích cách sử dụng từ.
- AI phân biệt các từ dễ nhầm lẫn.
- AI đề xuất từ vựng phù hợp với Band mục tiêu.
- AI tạo bài quiz cá nhân hóa.

# 8. IELTS Mock Test & Examination

[Tailors Labs - IELTS Practice Platform](https://images.openai.com/static-rsc-4/k7UGKLIBsOf6lUcBo00l04Q3IPx-pMbQbK7giqzqR0JRbOCH32ZMMSqnQ-4O-FVrBdKMjUjqcRdKXDWRfbfsS-SODDlRI6W6hGicb-b8lQJr87-oJHAnrewjnoxsz0gr8fq-44lbTSPuiP1McdRnCH7YZQ13IJW8aqs2m9Dt9Ug?purpose=inline)

[tailorslabs.com](https://tailorslabs.com/?utm_source=chatgpt.com)

| Feature                | Description                      |
| ---------------------- | -------------------------------- |
| Full Mock Test         | Thi thử đầy đủ              |
| Listening Test         | Thi Listening                    |
| Reading Test           | Thi Reading                      |
| Writing Test           | Thi Writing                      |
| Speaking Test          | Thi Speaking                     |
| Timed Examination      | Giới hạn thời gian            |
| Exam Instructions      | Hướng dẫn thi                 |
| Question Navigation    | Điều hướng câu hỏi         |
| Answer Sheet           | Phiếu trả lời                 |
| Auto Save Answers      | Tự động lưu đáp án        |
| Auto Submit            | Tự động nộp bài             |
| Test History           | Lịch sử thi                    |
| Band Score Calculation | Tính điểm                     |
| Detailed Test Review   | Phân tích bài thi             |
| Performance Comparison | So sánh kết quả các lần thi |
| Test Simulation        | Mô phỏng kỳ thi IELTS         |

# 9. Progress Tracking & Analytics

[For Learners | uBitto](https://images.openai.com/static-rsc-4/I3hk0MiJfUVQWo7-xQSdw-Zf6pB2nYDPR7RhiV8ORlaht-Phnh99xisnmUE-wB2ar6571KaPOxXbo_rsqDDs2Bet4pIQ857qX9RI-MvPp4Tzmwz395Lioqr0tReBzQHo-PRH4dJRpcMLd7hgXAkJZ_0tymDtn56ZR3Pk6LJWUP4?purpose=inline)

[ubitto.com](https://ubitto.com/for-learners/?utm_source=chatgpt.com)

| Feature                | Description                       |
| ---------------------- | --------------------------------- |
| Overall Progress       | Tiến độ tổng thể             |
| Band Score History     | Lịch sử Band Score              |
| Skill Performance      | Hiệu suất 4 kỹ năng           |
| Accuracy Rate          | Tỷ lệ trả lời đúng          |
| Study Time Analytics   | Thời gian học                   |
| Weekly Reports         | Báo cáo tuần                   |
| Monthly Reports        | Báo cáo tháng                  |
| Error Analysis         | Phân tích lỗi sai              |
| Vocabulary Growth      | Tăng trưởng từ vựng          |
| Learning Streak        | Chuỗi ngày học                 |
| Goal Achievement       | Mức độ hoàn thành mục tiêu |
| Performance Comparison | So sánh kết quả                |
| Predicted Band Score   | Band Score dự đoán             |

Các dạng biểu đồ nên có:

- Line Chart: Theo dõi Band Score.
- Radar Chart: So sánh 4 kỹ năng.
- Bar Chart: Số lượng bài tập hoàn thành.
- Pie Chart: Phân bố thời gian học.
- Heatmap: Lịch sử hoạt động học tập.

# 10. Gamification & Motivation

| Feature            | Description             |
| ------------------ | ----------------------- |
| XP System          | Điểm kinh nghiệm     |
| Daily Challenges   | Thử thách hàng ngày |
| Weekly Challenges  | Thử thách hàng tuần |
| Achievement Badges | Huy hiệu               |
| Leaderboard        | Bảng xếp hạng        |
| Learning Streak    | Chuỗi ngày học       |
| Level System       | Cấp độ học viên    |
| Rewards            | Phần thưởng          |
| Milestones         | Cột mốc học tập     |
| Learning Goals     | Mục tiêu cá nhân    |

# 11. Notification System

- Email Notifications.
- In-app Notifications.
- Daily Study Reminders.
- Learning Streak Reminders.
- Assignment Reminders.
- Mock Test Reminders.
- New Lesson Notifications.
- AI Feedback Notifications.
- Weekly Progress Notifications.
- Achievement Notifications.

# 12. Admin Management System

[AI Edtech LMS Dashboard UI by Filllo Design Agency on Dribbble](https://images.openai.com/static-rsc-4/0GwKflTB0mkYyihwpyVOOFX4IO4ms57ejP9iRLstrZz5BWzoWJyGAype8gocMZbEFGyPxWmQr_5wpJozo0yOiQh8sl_mo8TV2y2MyCwNaRmAzlKlJqzK6GrJYDCdfEx0z14FGFjX1bEz4AxOR3XQnN05wjkZ3ZSwSEokDWPkX1M?purpose=inline)

[dribbble.com](https://dribbble.com/shots/27064592-AI-Edtech-LMS-Dashboard-UI?utm_source=chatgpt.com)

Admin chịu trách nhiệm quản lý toàn bộ nền tảng.

| Feature                    | Description                     |
| -------------------------- | ------------------------------- |
| Admin Dashboard            | Tổng quan hệ thống           |
| User Management            | Quản lý người dùng         |
| Role & Permission          | Quản lý quyền                |
| Student Management         | Quản lý học viên            |
| Course Management          | Quản lý khóa học            |
| Lesson Management          | Quản lý bài học             |
| Question Bank Management   | Quản lý ngân hàng câu hỏi |
| IELTS Test Management      | Quản lý đề thi              |
| Listening Audio Management | Quản lý audio                 |
| Reading Passage Management | Quản lý bài đọc            |
| Writing Topic Management   | Quản lý đề Writing          |
| Speaking Topic Management  | Quản lý đề Speaking         |
| Vocabulary Management      | Quản lý từ vựng             |
| Grammar Content Management | Quản lý nội dung ngữ pháp  |
| AI Model Management        | Quản lý model AI              |
| AI Prompt Management       | Quản lý prompt                |
| AI Scoring Configuration   | Cấu hình chấm điểm         |
| AI Usage Monitoring        | Theo dõi mức sử dụng AI     |
| Reports Management         | Báo cáo hệ thống            |
| Feedback Management        | Quản lý phản hồi            |
| Content Approval           | Duyệt nội dung                |
| System Logs                | Nhật ký hệ thống            |

# 13. Teacher / Tutor Management

Nếu muốn mở rộng nền tảng thành hệ thống học IELTS có giáo viên:

- Teacher Registration.
- Teacher Profile.
- Student Assignment.
- Class Management.
- Course Assignment.
- Homework Management.
- Writing Review.
- Speaking Review.
- Student Feedback.
- Teacher Performance Reports.
- Student Progress Monitoring.
- Teacher-Student Messaging.

# 14. Subscription & Payment (Optional)

Nếu hướng đến sản phẩm thương mại:

| Feature                 | Description                    |
| ----------------------- | ------------------------------ |
| Free Plan               | Gói miễn phí                |
| Premium Plan            | Gói trả phí                 |
| Subscription Management | Quản lý đăng ký           |
| Payment Integration     | Tích hợp thanh toán         |
| Payment History         | Lịch sử giao dịch           |
| Invoice Generation      | Tạo hóa đơn                |
| Usage Limits            | Giới hạn lượt sử dụng AI |
| Premium AI Features     | Tính năng AI nâng cao       |
| Coupon Management       | Quản lý mã giảm giá       |

# 15. System & Technical Features

Các tính năng nền tảng thường không nhìn thấy trực tiếp nhưng rất cần thiết.

- RESTful API.
- JWT Authentication.
- Role-Based Access Control (RBAC).
- API Rate Limiting.
- Input Validation.
- Error Handling.
- Logging & Monitoring.
- Redis Caching.
- Background Task Processing (Celery).
- File Upload Management.
- Audio Storage.
- Database Backup.
- API Documentation (Swagger / OpenAPI).
- Responsive Web Design.
- SEO Optimization.
- Security Protection.
- Data Privacy.
- AI Model Versioning.
- Model Performance Monitoring.
- AI Request Logging.
- Model Evaluation Pipeline.

# 16. User Roles & Permissions

Mình đề xuất hệ thống có 3 vai trò chính ở phiên bản đầu tiên.

| Role    | Responsibilities                                       |
| ------- | ------------------------------------------------------ |
| Student | Học IELTS, làm bài tập, thi thử, xem kết quả    |
| Teacher | Quản lý học viên, giao bài, đánh giá bài làm |
| Admin   | Quản lý người dùng, nội dung, đề thi và AI    |

# 17. System Architecture

Với Django + React + NLP + Machine Learning, mình đề xuất kiến trúc phân tách rõ Backend, AI Services và Frontend.

## IELTS AI Learning System Architecture

React.js + TypeScript

Student Dashboard · Learning · Mock Test · Admin

REST API / JWT

Django + Django REST Framework

Authentication · Business Logic · API · User Management

NLP Service

Text analysis · Grammar · Semantic analysis

ML Service

Prediction · Classification · Recommendation

LLM Service

Feedback · AI Tutor · Explanation

Speech Service

Speech-to-Text · Pronunciation

Infrastructure Layer

PostgreSQL

Redis

Storage

### Công nghệ cụ thể

| Layer              | Technology                                   |
| ------------------ | -------------------------------------------- |
| Frontend           | React, TypeScript, Tailwind CSS              |
| Backend            | Django, Django REST Framework                |
| Database           | PostgreSQL                                   |
| Cache              | Redis                                        |
| Background Jobs    | Celery                                       |
| NLP                | spaCy, NLTK, Hugging Face                    |
| Machine Learning   | Scikit-learn, XGBoost                        |
| Deep Learning      | PyTorch, Transformers                        |
| LLM                | API-based LLM hoặc model triển khai riêng |
| Speech Recognition | Whisper                                      |
| Visualization      | Recharts                                     |
| API Documentation  | Swagger / drf-spectacular                    |
| Deployment         | Docker, Nginx                                |

# 18. Phân chia Database Modules

Để tránh thiết kế database lộn xộn, mình đề xuất chia thành các nhóm:

| Database module | Các bảng chính                                   |
| --------------- | --------------------------------------------------- |
| Authentication  | users, roles, permissions                           |
| Student         | student_profiles, learning_goals                    |
| Courses         | courses, lessons, modules                           |
| IELTS Content   | questions, passages, topics, audio_files            |
| Listening       | listening_tests, listening_answers                  |
| Reading         | reading_tests, reading_answers                      |
| Writing         | writing_submissions, writing_feedback               |
| Speaking        | speaking_recordings, transcripts, speaking_feedback |
| Vocabulary      | vocabulary, flashcards, vocabulary_progress         |
| Mock Test       | mock_tests, test_attempts, test_results             |
| AI              | ai_evaluations, ai_requests, model_versions         |
| ML              | student_features, predictions, recommendations      |
| Analytics       | learning_activities, progress_records               |
| Gamification    | achievements, user_xp, streaks                      |
| Notification    | notifications, notification_preferences             |
| Payment         | subscriptions, transactions                         |

# 19. Thứ tự phát triển dự án

Mình không khuyên phát triển toàn bộ 18 nhóm chức năng cùng lúc. Với một dự án Django + React + NLP + ML, nên chia thành các giai đoạn.

## Development Roadmap

1. Phase 1 – Core Platform

   Must have

   - Authentication & Authorization
   - Student Dashboard
   - IELTS Learning Modules
   - Listening & Reading Practice
   - Writing & Speaking Submission
   - Question Bank
   - Basic Admin Dashboard
2. Phase 2 – AI Integration

   Must have

   - AI Writing Evaluation
   - Grammar & Vocabulary Analysis
   - AI Speaking Assessment
   - Speech-to-Text
   - AI Learning Assistant
   - Automated Feedback
3. Phase 3 – Machine Learning

   Advanced

   - IELTS Band Prediction
   - Student Level Classification
   - Weakness Detection
   - Personalized Recommendation
   - Adaptive Learning
4. Phase 4 – Learning Analytics

   Advanced

   - Learning Progress Analytics
   - Performance Prediction
   - Study Plan Optimization
   - Mock Test Analytics
   - Vocabulary Mastery Tracking
5. Phase 5 – Production & Expansion

   - Teacher Management
   - Payment Integration
   - Subscription Plans
   - Gamification
   - Notification System
   - Production Deployment

# 20. Phạm vi MVP mình khuyên nên làm

Nếu đây là dự án học thuật hoặc đồ án nhóm, mình đề xuất chọn những chức năng có thể chứng minh được năng lực Django, React, NLP và Machine Learning, thay vì chỉ làm một website CRUD thông thường.

Recommended MVP

| Module           | Chức năng cần hoàn thành           |
| ---------------- | --------------------------------------- |
| Authentication   | Register, Login, Profile                |
| Dashboard        | Band Score, Progress, Statistics        |
| Listening        | Practice, Quiz, Auto Grading            |
| Reading          | Passage, Questions, Auto Grading        |
| Writing          | Editor, AI Scoring, Feedback            |
| Speaking         | Recording, Speech-to-Text, AI Analysis  |
| Vocabulary       | Flashcards, Quiz, Spaced Repetition     |
| AI Assistant     | IELTS Chatbot                           |
| AI Learning      | Placement Test, Personalized Study Plan |
| Machine Learning | Band Prediction, Recommendation         |
| Admin            | User, Questions, Content Management     |
| Analytics        | Skill Progress, Learning History        |

Ba tính năng nên được đầu tư nhất để thể hiện giá trị nghiên cứu:

1. AI Writing & Speaking Evaluation: Phân tích bài làm và đánh giá theo tiêu chí IELTS.
2. Personalized Learning Recommendation: Machine Learning phân tích điểm yếu và đề xuất bài tập.
3. IELTS Band Score Prediction: Dự đoán khả năng đạt Band mục tiêu dựa trên dữ liệu học tập.

Lưu ý quan trọng: Điểm AI chỉ nên được gọi là estimated band score, không phải điểm IELTS chính thức. Muốn huấn luyện mô hình dự đoán đáng tin cậy cần có tập dữ liệu bài làm và điểm đánh giá chuẩn do con người gán nhãn.

# 21. Tổng kết định hướng sản phẩm

# IELTS AI Learning System

An intelligent and personalized IELTS learning platform.

# 4

IELTS Skills

# 3

Main User Roles

# 2

AI Core Technologies

# 5

Development Phases

Product vision

Learn smarter. Practice better. Achieve your target IELTS band.

Bước tiếp theo mình đề xuất: Chuyển toàn bộ đặc tả này thành tài liệu Software Requirements Specification (SRS), sau đó thiết kế Use Case Diagram, ERD Database, System Architecture và chia task Backend/Frontend/AI thành backlog để nhóm bắt đầu code.

Mình cũng có thể giúp theo dõi tiến độ dự án và nhắc nhóm rà soát roadmap mỗi tuần.

Theo dõi tiến độ IELTS AI hàng tuần
