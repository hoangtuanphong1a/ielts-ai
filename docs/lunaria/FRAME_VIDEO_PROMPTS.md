# Prompt video để cắt khung cho Lunaria (cảnh ngồi bàn)

Mục đích: tạo các video ngắn bằng Gemini (Veo) từ ảnh gốc `demo.png`, sau đó cắt từng khung hình ra làm bộ ảnh cho engine kiểu "Living Portrait" (xem `docs/reference/mina-portrait/ANALYSIS.md`).

Video **không phát trực tiếp trên web**. Chỉ dùng để lấy khung hình, nên chuyển động phải **chậm, dừng rõ ở từng tư thế**, để mỗi tư thế có ít nhất vài khung sắc nét.

## Cách tạo

1. Gemini, chọn tạo video, **tải `docs/lunaria/demo.png` làm ảnh đầu**. Mọi clip đều bắt đầu từ ảnh này để tư thế nghỉ (`rest`) trùng nhau giữa các clip.
2. Dán prompt: phần **chung** + phần **riêng** của clip.
3. Tải video về, đặt tên đúng cột "Tên file" rồi bỏ vào `docs/lunaria/frames-src/`.
4. Video nào bị cắt cảnh, đổi góc máy, zoom, hay thêm hoặc dời đồ vật thì tạo lại. Bản `7646b878` trước đây bị lỗi này.

## Phần chung (dán ở đầu mọi prompt)

```
Single continuous shot. The camera is locked on a tripod: no camera movement, no zoom, no pan, no cut, no scene change.
Keep the exact same scene as the input image: same background, same lighting, same desk, monitor, cat plush, cup, books and plant, all perfectly still and in the same position.
Only the girl moves. She keeps the same outfit, white headphones, hair, elf ears and makeup.
Movements are slow and calm. She holds each pose still for about one second before the next movement.
At the end of the video she returns to exactly the original pose of the input image: chin resting on her hand, looking at the monitor.
Photorealistic, soft natural light, no text, no subtitles.
```

## Phần riêng từng clip

| # | Tên file | Dùng cho | Prompt riêng |
|---|---|---|---|
| 1 | `clip01-blink-gaze.mp4` | Chớp mắt, nhìn bàn phím, liếc người xem | `She blinks slowly twice. Then only her eyes move: she looks down at the keyboard and holds, looks back at the monitor, then glances toward the camera without turning her head and holds, then looks back at the monitor.` |
| 2 | `clip02-turn-talk.mp4` | Quay sang bạn và nói | `She slowly turns her head toward the camera, gives a soft friendly smile, and speaks a short sentence calmly with clear mouth movements, as if explaining something. Then she slowly turns back to the monitor.` |
| 3 | `clip03-point.mp4` | Hướng dẫn, chỉ vào giao diện | `Keeping her chin on her hand, she lifts her other hand and points gently to the left side of the frame, toward the monitor, while looking at the camera with a small smile. She holds the point, then lowers her hand.` |
| 4 | `clip04-think-proud.mp4` | Đang chấm bài, rồi tự hào | `She looks slightly up and touches her lips with one finger, thinking, and holds. Then her face lights up with a proud, happy smile and she nods once toward the camera.` |
| 5 | `clip05-worried-encourage.mp4` | Nhiều lỗi, động viên | `She reads the monitor and looks a little worried, eyebrows slightly raised, and holds. Then she turns her eyes to the camera and gives a warm encouraging smile with a small nod.` |
| 6 | `clip06-surprised.mp4` | Vượt mục tiêu | `She notices something on the monitor and looks surprised: eyes widen, lips slightly open, and she holds. Then she breaks into a delighted smile.` |
| 7 | `clip07-typing.mp4` | Cùng gõ bài | `She lowers her hand from her chin and types calmly on the keyboard with both hands while looking at the monitor. Then she rests her chin on her hand again.` |
| 8 | `clip08-idle-headphones.mp4` | Tự diễn khi im lâu | `She adjusts her white headphones with one hand, tilts her head slightly, then settles back into her original pose.` |
| 9 | `clip09-idle-sleepy.mp4` | Tự diễn khi im lâu | `She becomes sleepy: her eyelids slowly droop, her head nods down once, then she wakes up a little startled and blinks.` |

Thứ tự nên làm: **2 → 1 → 3**. Clip 2 (quay đầu và nói) khó nhất và đáng giá nhất. Nếu Gemini giữ khung tốt ở clip 2 thì làm tiếp cả bộ.

## Bản cho BytePlus Lumina (Seedance)

Lumina chạy model Seedance. Seedance có 2 thứ Gemini không có, và cả hai rất có lợi cho việc cắt khung:

- **First + Last frame**: đặt **cả ảnh đầu lẫn ảnh cuối là `demo.png`**. Video buộc phải kết thúc đúng tư thế nghỉ, nên không cần dặn "quay về tư thế ban đầu" trong prompt.
- **Camera fixed**: bật lên, khung hình đứng yên. Đây là chỗ Gemini từng hỏng.

**Cài đặt:**

| Mục | Chọn |
|---|---|
| Model | Seedance bản cao nhất có trong playground |
| Chế độ | Image to video, **first & last frame** |
| First frame / Last frame | `demo.png` / `demo.png` |
| Camera fixed | **Bật** |
| Tỉ lệ | 16:9 (hoặc adaptive nếu model yêu cầu) |
| Độ phân giải | 1080p nếu có |
| Thời lượng | 5s cho clip 1, 6, 8; 10s cho các clip còn lại |
| Watermark | Tắt nếu có tuỳ chọn |
| Seed | Ghi lại seed của clip đẹp để tạo lại biến thể |

**Cách viết prompt cho Seedance:** model đã nhìn thấy ảnh, nên **không tả lại cô ấy hay căn phòng**. Chỉ tả chuyển động theo thứ tự, câu ngắn, mở đầu bằng `Camera fixed.`

Phần chung (rút gọn, dán ở đầu):

```
Camera fixed, static shot, one continuous take, no cut. Only the girl moves; the room and all objects stay still. Slow, calm movements, pausing briefly in each pose.
```

Phần riêng:

| # | Prompt riêng |
|---|---|
| 1 | `She blinks slowly twice. Her eyes look down at the keyboard, pause, look back at the monitor, then glance at the camera, pause, and return to the monitor.` |
| 2 | `She slowly turns her head to face the camera, smiles softly and says a short sentence with clear mouth movements, then turns back to the monitor and rests her chin on her hand.` |
| 3 | `She looks at the camera with a small smile and points with her free hand toward the left side of the frame, holds the point, then lowers her hand.` |
| 4 | `She looks slightly up and touches her lips with one finger, thinking. Then she smiles proudly and nods once at the camera.` |
| 5 | `She reads the monitor with a slightly worried look, then turns her eyes to the camera and gives a warm encouraging smile with a small nod.` |
| 6 | `She looks at the monitor, eyes widen in surprise with lips slightly open, then she breaks into a delighted smile.` |
| 7 | `She lowers her hand and types calmly on the keyboard with both hands, looking at the monitor, then rests her chin on her hand again.` |
| 8 | `She adjusts her white headphones with one hand and tilts her head slightly, then settles back.` |
| 9 | `Her eyelids slowly droop and her head nods down once, then she wakes up a little startled and blinks.` |

Nếu đặt ảnh đầu và ảnh cuối giống nhau mà cô ấy gần như không cử động, chuyển sang **chỉ first frame**. Khi đó thêm câu `At the end she returns to her original pose, chin on her hand, looking at the monitor.` vào cuối prompt.

## Lưu ý

- Gemini có logo ✦ ở góc dưới phải. Cô ấy ngồi ở nửa phải nên logo có thể đè lên tay hoặc tóc. Khi cắt khung, vùng có logo sẽ được lấy từ khung `rest`. Nếu logo đè lên chỗ đang cử động thì báo để xử lý riêng.
- Video ra 1280×720, nhỏ hơn `demo.png` (1671×941). Mọi khung sẽ cùng độ phân giải video, kể cả `rest`, để khớp nhau.
- Nếu không dừng rõ ở từng tư thế thì vẫn dùng được: có thể phát một đoạn khung liền nhau như một act ngắn (ví dụ quay đầu 8 khung). Khi đó chuyển động còn mượt hơn bản Mina.

## Sau khi có video (phần việc của Claude)

1. Cắt khung (ffmpeg), so từng khung với khung đầu để đo độ trôi camera.
2. Chọn khung đại diện cho từng trạng thái: `rest`, `half`, `closed`, `look-down`, `glance`, `turn`, `talk-a/o/e`, `point`, `thinking`, `proud`, ...
3. Căn khung nếu bị trôi, cắt vùng người (nửa phải), xuất webp.
4. Tách nền một lần từ `rest` để làm vùng bấm.
5. Gắn vào engine và nối với sự kiện của IELTS AI.
