# Lunaria: prompt tạo video cho từng trang

Dùng trên Lumina (BytePlus): **Image** (GPT-image-2.5) để tạo ảnh gốc mỗi tư thế, rồi **Video** (Seedance 2.0 / 2.0 Fast, chế độ Freestyle Creation, image-to-video) để tạo clip.

## Quy tắc chung (áp dụng cho MỌI clip)

| Mục | Cài đặt |
|---|---|
| Ảnh đầu vào | Ảnh gốc của đúng tư thế đó (mục "Ảnh gốc" bên dưới) |
| Tỉ lệ | Adaptive (theo ảnh) |
| Độ dài | 4-5 giây |
| Chất lượng | 720p trở lên |
| Âm thanh | Tắt |
| Nền | Trắng trơn (web tự hòa nền trắng vào trang) |

Mỗi prompt video đều kết thúc bằng câu khoá dưới đây, **luôn dán kèm**, để các clip nối với nhau không bị giật:

```
Locked-off static camera, no zoom, no camera movement. Plain pure white background that never changes. Keep her face, hair, outfit and proportions exactly as in the reference image. She ends in the exact same pose as the first frame. No text, no watermark, no extra people.
```

Tên file khi lưu: `<tu-the>-<clip>.mp4`, rồi chạy:

```bash
bash tools/lunaria-encode.sh <file-tai-ve.mp4> <tu-the> <clip>
```

`look`, `idle`, `talk` được web dùng ngay. Các clip phản ứng khác (`peek`, `cheer`...) sẽ được nối vào sự kiện khi có file.

---

## 1. Trang đăng nhập: tư thế `stand` (đã có ảnh gốc)

Ảnh gốc: `docs/lunaria/stand-original.png`

| Clip | Khi nào phát | Prompt (dán + câu khoá chung) |
|---|---|---|
| `stand-look` | Di chuột: cô ấy nhìn theo | `The elf girl stands in place. She slowly and smoothly turns her head and eyes from looking to her left to looking to her right in one continuous motion, gentle breathing, slight hair movement.` |
| `stand-idle` | Đứng yên | `The elf girl stands relaxed and looks at the viewer. She breathes softly, blinks once, her hair sways very slightly. Minimal motion.` |
| `stand-talk` | Đang nói (bong bóng đang gõ) | `The elf girl looks at the viewer and speaks calmly and warmly, natural lip movement, small head nods, an occasional blink. Body and hands stay almost still.` |
| `stand-peek` | Bấm vào ô mật khẩu ("I won't peek") | `The elf girl playfully raises one hand to cover her eyes, smiles a little, holds it for a moment, then lowers her hand back to the starting pose.` |
| `stand-wave` | Đăng nhập thành công | `The elf girl gives a small, elegant wave with her raised hand and a gentle smile, then returns her hand to the starting pose.` |

---

## 2. Dashboard + Profile: tư thế `desk` (ngồi bàn, đeo tai nghe, nửa người)

**Ảnh gốc** (Image, GPT-image-2.5, 4:5 dọc, ảnh tham chiếu: `stand-original.png` + ảnh mẫu Profile):

```
Use reference image 1 for the character's identity: keep her face, platinum hair, pointed elf ears, red ribbon earrings, white ruffled blouse and silver cross necklace exactly the same. Use reference image 2 only for the pose and camera angle.
Waist-up portrait, three-quarter view. The elf girl sits at a desk, resting her cheek on her hand with her elbow on the desk, gazing softly to the side with a calm, thoughtful expression. She wears large white over-ear headphones with a softly glowing infinity symbol on the ear cup.
Plain pure white background. No room, no monitor, no chair, no props, no text. Soft cool daylight with a gentle blue rim light. Same rendering style as reference image 1. Highly detailed, clean edges.
```

| Clip | Khi nào phát | Prompt |
|---|---|---|
| `desk-look` | Di chuột | `She keeps her cheek resting on her hand and slowly turns her head and eyes from her left to her right in one smooth continuous motion.` |
| `desk-idle` | Ngồi yên | `She rests her cheek on her hand, breathes softly, blinks once, and taps one finger gently against her cheek. Minimal motion.` |
| `desk-talk` | Đang nói | `She lifts her head slightly from her hand, looks at the viewer and speaks warmly with natural lip movement and small nods.` |
| `desk-cheer` | Bài chấm xong đạt mục tiêu / band tăng | `She looks up with a bright, proud smile and gives a small happy fist pump, then settles back to the starting pose.` |
| `desk-think` | Đang gợi ý điểm yếu / kế hoạch hôm nay | `She tilts her head slightly, taps her chin thoughtfully with one finger, then nods as if she found the answer.` |

---

## 3. Trang viết bài: tư thế `reading` (ngồi, cầm giấy)

**Ảnh gốc:** dùng prompt ảnh gốc của mục 2, thay câu tư thế bằng:

```
Waist-up portrait, three-quarter view. The elf girl sits at a desk holding a sheet of paper with both hands, reading it attentively, headphones resting around her neck.
```

| Clip | Khi nào phát | Prompt |
|---|---|---|
| `reading-idle` | Người học đang viết | `She reads the paper quietly, her eyes moving along the lines, breathing softly. Minimal motion.` |
| `reading-look` | Di chuột | `She lowers the paper slightly and turns her head and eyes from her left to her right in one smooth continuous motion.` |
| `reading-talk` | Nhắc bố cục / số từ | `She looks up from the paper at the viewer and speaks encouragingly with natural lip movement.` |
| `reading-nod` | Đủ số từ / bấm nộp | `She looks at the viewer, smiles and gives an encouraging nod.` |

---

## 4. Trang kết quả: tư thế `reading` (dùng lại)

| Clip | Khi nào phát | Prompt |
|---|---|---|
| `reading-scoring` | Bài đang chấm ("Scoring your essay") | `She reads the paper carefully, frowns slightly in concentration, then makes a small mark on the paper with a pen.` |
| `reading-cheer` | Kết quả tốt | Dùng prompt `desk-cheer` |

---

## 5. Trang từ vựng: tư thế `cards`

**Ảnh gốc:** prompt ảnh gốc mục 2, thay câu tư thế bằng:

```
Waist-up portrait, front view. The elf girl holds a small stack of flashcards in one hand and shows one card toward the viewer with the other hand, friendly expression.
```

| Clip | Khi nào phát | Prompt |
|---|---|---|
| `cards-idle` | Chờ lật thẻ | `She holds the flashcards and waits patiently, breathing softly, blinking once.` |
| `cards-talk` | Đọc từ / giải thích | `She looks at the viewer and speaks clearly with natural lip movement, glancing at the card once.` |
| `cards-clap` | Ôn xong thẻ hôm nay | `She tucks the cards under her arm and claps her hands twice with a happy smile, then returns to the starting pose.` |

---

## Thứ tự nên làm (tiết kiệm credit)

1. `stand-look` → kiểm tra trên trang login.
2. `stand-talk`, `stand-idle`.
3. Ảnh gốc `desk` → `desk-look`, `desk-talk`, `desk-idle`.
4. Các clip phản ứng (`peek`, `cheer`, `think`, `nod`...) khi còn credit.

Mẹo: thử bằng **Draft mode** hoặc **Seedance 2.0 Fast** trước; chuyển động đúng ý mới tạo bản đẹp.
