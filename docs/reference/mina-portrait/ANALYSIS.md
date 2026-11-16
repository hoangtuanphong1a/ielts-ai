# Phân tích "Living Portrait" (Mina) — cách làm nhân vật tương tác

Bản dựng lại để nghiên cứu nằm cùng thư mục. Chạy:

```bash
cd docs/reference/mina-portrait
npm install
npm run dev        # http://localhost:5190
```

Engine nằm ở `public/living-portrait.js` (giữ nguyên văn theo prompt gốc). Phần React chỉ dựng trang và gắn markup; engine được nạp sau khi React render (`src/components/LivingPortrait.tsx`).

Đây là bản tham khảo để học, không đưa vào IELTS AI. Ảnh lấy trực tiếp từ server của tác giả (images.higgs.ai), không tải về repo.

---

## 1. Ý tưởng cốt lõi trong một câu

Không có video, không có model 3D. Nhân vật là **59 ảnh tĩnh của cùng một khuôn mặt, chụp cùng khung, cùng vị trí đầu tới từng pixel**. Code chỉ làm 2 việc:

1. **Chọn ảnh nào hiện** (state machine theo chuột, click, thời gian).
2. **Làm "da" mềm** bằng một lưới WebGL co giãn được, để ảnh tĩnh trông như có thịt.

Vì mọi ảnh trùng khung, đổi ảnh trong 20–70ms trông như khuôn mặt tự cử động.

So với hướng video (Gemini/Veo) mình làm trước đó:

| | Video scrub | Ảnh rời + engine (Mina) |
|---|---|---|
| Nhảy tới biểu cảm bất kỳ | Không, chỉ tua trong 1 clip | Có, truy cập ngẫu nhiên 59 ảnh |
| Mắt nhìn theo chuột 2 chiều | Chỉ trái–phải theo trục thời gian | 16 hướng, mỗi hướng 1 ảnh |
| Phản ứng click tức thì | Phải chờ seek | 1 frame |
| Kéo, véo, rung da | Không | Có (lưới vật lý) |
| Dung lượng | Video all-intra nặng | ~60 ảnh webp ~100–220KB |

## 2. Kho ảnh (asset) — phần quyết định chất lượng

`IDS` trong engine liệt kê 59 ảnh, chia nhóm:

- **rest**: mặt trung tính, mắt nhìn thẳng. Là ảnh gốc mọi ảnh khác được "chỉnh" từ đó.
- **Mắt (18 ảnh)**: 16 hướng nhìn (`right, ene, upright, nne, up, nnw, wnw, left, wsw, downleft, ssw, down, sse, downright, ese`) + `half` (mí khép nửa) + `closed`.
- **Biểu cảm đơn**: `shock, ouch, scared, angry, scrunch, dizzy, deadpan, kiss, tongue, puff, laugh, grin, smug, shy, cry, raised, hearts, stars, sick, wind, cross, fish, winkl, winkr`.
- **Chuỗi khung cho hành động**: `yawn1 → yawn2 → yawn → yawn4`, `gum1 → gum2 → gum3 → gumpop`, `sneeze1 → sneeze2`, `whistle1/2`, `snore`.
- **Màu tóc**: `pink, blue, blonde` (chỉ có mặt nhìn thẳng, nên khi đổi màu tóc mắt không theo chuột).

Điều kiện bắt buộc của ảnh:

- **Nền trong suốt (PNG alpha)**. Alpha vừa dùng để hòa nền, vừa dùng làm vùng bấm (mục 5).
- **Căn trùng pixel**: đầu, tai, tóc, hoa tai nằm đúng chỗ ở mọi ảnh. Chỉ phần thay đổi (mắt, miệng, má) được khác. Lệch vài pixel là thấy giật khi đổi ảnh.
- Tên file có tiền tố `hf_2026...`. Đoán là ảnh tạo bằng Higgsfield (chưa xác minh), theo kiểu "image edit": đưa ảnh `rest` vào và yêu cầu chỉ đổi một chi tiết.

## 3. Luật vàng: chỉ một ảnh trên màn hình

```js
function show(n, ms, now) {
  if (!tex[n] || n === faceB) return;
  faceA = (now - fadeT) / fadeMs > .5 ? faceB : faceA; faceB = n; fadeT = now; fadeMs = Math.min(70, Math.max(1, ms));
}
```

- Shader chỉ trộn 2 texture `faceA → faceB` với `fade` 0→1, tối đa 70ms.
- **Không bao giờ dán mảng mắt/miệng lên mặt**. Tác giả ghi rõ việc dán chồng gây mắt đôi, cằm đôi, viền đen. Muốn đổi mắt thì đổi cả bức ảnh.
- Hệ quả: số ảnh tăng theo tổ hợp. Vì vậy mắt chỉ chạy trên mặt `rest`; khi đang có biểu cảm khác thì mắt đứng yên.

## 4. Lưới da mềm (WebGL)

- Lưới 73×73 đỉnh (`N = 72`), phủ rộng 1.7 lần ảnh (`OVER`) để da kéo ra ngoài không bị cắt. Canvas cũng to 170% khung ảnh.
- Mỗi đỉnh có độ lệch `ux, uy` và vận tốc `vx, vy`. Mỗi bước chạy **phương trình sóng tắt dần**:
  `v += (c²·Laplacian(u) − ω²·u − γ·v + ν·Laplacian(v))·dt`
  - `c²·Laplacian`: kéo một chỗ thì chỗ bên cạnh bị kéo theo, nên sóng lan ra như bột.
  - `ω²·u`: lò xo kéo về vị trí gốc, nên thả tay ra thì da rung rồi về chỗ.
  - `γ·v` và `ν·Laplacian(v)`: ma sát, để rung tắt dần chứ không rung mãi.
- **Bước vật lý cố định 1/240s** (`H`), mỗi frame chạy tối đa 9 bước. Nếu dùng dt theo frame thì màn hình 144Hz và 60Hz cho kết quả khác nhau, lưới dễ bung thành gai.
- **untangle()**: sau vật lý, mỗi hàng và mỗi cột bị ép lại cho đúng thứ tự, có khoảng cách tối thiểu `GAP`. Nhờ đó tam giác không bao giờ lật lên nhau (lật thì thấy vết cắt răng lược).
- **Đổ bóng theo độ nén**: chỗ da bị ép thì tối đi, chỗ bị giãn thì sáng lên (`vS` từ 0.86 đến 1.16). Cảm giác có thể tích mà không cần 3D.
- **Các lực tác động vào lưới**:
  - `takeHold` + `brush`: nắm một vùng hình chuông bán kính 0.22 và kéo theo tay. Độ kéo bị giới hạn mềm `lim = .24`, nên kéo xa mấy da cũng không rách.
  - `poke`: đẩy một cú (hắt hơi, bong bóng kẹo nổ, ruồi đậu, rê chuột lướt qua da).
  - `lean`: cả đầu nghiêng nhẹ theo con trỏ hoặc theo lực kéo, chạy bằng lò xo tắt dần.

## 5. Biết chuột đang chạm vào đâu

- `hitMap`: vẽ ảnh `rest` thu nhỏ 128×128, đọc kênh alpha. Alpha > 40 nghĩa là chuột đang trên đầu (`solid`). Ngoài viền tóc thì không phản ứng.
- `toUv`: đổi tọa độ màn hình sang UV của ảnh (0..1).
- `zoneAt(u, v)`: chia mặt bằng hình học đơn giản: ngoài elip mặt là `hair`, rồi đến `brow`, `eyeL`, `eyeR`, `nose`, `mouth`, `cheek`, `chin`. Các ngưỡng là số đo tay trên ảnh gốc. Đổi nhân vật thì phải đo lại.
- `ZONES` gắn vùng với phản ứng:
  - hover (sau 80ms): mắt thì nháy mắt, mũi thì lác mắt, miệng thì hôn gió.
  - tap: trán thì giận, mắt thì "đau", mũi thì chạy act hắt hơi, miệng thì lè lưỡi, má thì phồng má, cằm thì cười. Tap vào tóc thì đổi màu.

## 6. Bộ não: thứ tự ưu tiên chọn ảnh mỗi frame

Trong `frame()`:

```
act đang chạy           -> ảnh theo kịch bản act
đang nhấn/kéo           -> shock / ouch / scared theo độ kéo
moodFace còn hạn        -> ảnh phản ứng (sau tap, sau kéo, nút Contact)
lắc chuột nhanh         -> wind, giữ lâu thì sick
hover vào 1 vùng > 80ms -> wink / cross / kiss
còn lại                 -> rest + mắt nhìn theo chuột + chớp mắt
```

Lớp mắt (chỉ khi mặt đang `rest`):

- Chưa có input thì nhắm mắt. Chuột động lần đầu thì `half` → mở (thức dậy).
- `ringFor(dx, dy)`: `atan2` chia 360° thành 16 múi, chọn ảnh hướng tương ứng. Chuột gần tâm mặt (< 0.13) thì nhìn thẳng.
- Chớp mắt mỗi 2.2–5.6s: `half` → `closed` → `half` → mở, mỗi bước 62ms.
- Đang cuộn trang thì nhìn xuống. Có ruồi bay thì nhìn theo ruồi (`lookAt`).

Bộ đếm cảm xúc: kéo 5 lần trong 14s thì giận, 8 lần thì khóc. Thả tay sau khi kéo mạnh thì chóng mặt.

## 7. Act: kịch bản khi trang yên lặng

```js
// [ảnh hoặc 'eye:hướng', crossfade ms, giữ ms, extras]
sneeze: [['sneeze1',130,380], ['half',90,120], ['sneeze1',90,560],
         ['sneeze2',50,300,{jolt:[.5,.6,0,1.5,.34], lean:[0,.03]}], ['dizzy',110,620], ['shy',140,650]]
```

- Act là **danh sách khung hình có thời lượng**, giống timeline hoạt hình. `extras` có thể `jolt` (đẩy da), `lean` (nghiêng đầu), `call` (di chuyển đạo cụ).
- Không có input 30–45s thì lấy act tiếp theo trong `ROTATION` (yawn, shifty, gum, fly, flirt, ...).
- **Có input là dừng act ngay**. Nhân vật không tự diễn khi người dùng đang thao tác, nên không gây phiền.
- Đạo cụ (ruồi, bàn tay) là SVG đặt theo UV, nằm ngoài WebGL. Bàn tay "ma" trong `tugAct` dùng chính `takeHold` để véo má, giống như người dùng kéo.

## 8. Áp dụng cho Lunaria (đề xuất, chưa làm)

Cách này hợp hơn video vì app học cần **phản ứng tức thì theo sự kiện** (chấm xong bài, lỗi ngữ pháp, gõ bài, im lâu).

**Asset tối thiểu (khoảng 30 ảnh, từ 1 ảnh gốc Lunaria bán thân, nền trong suốt):**

- Mắt: `rest`, `half`, `closed`, cùng 8 hướng nhìn (bắt đầu với 8, đủ thì nâng lên 16).
- Nói: 3–4 hình miệng (`mouth-closed`, `mouth-a`, `mouth-o`, `mouth-e`). Khi bong bóng thoại gõ chữ thì đổi ảnh theo nhịp để giả khẩu hình.
- Cảm xúc theo ngữ cảnh học: `happy`, `proud` (band cao, đạt mục tiêu), `encourage` (band thấp), `thinking` (đang chấm bài), `surprised`, `worried` (nhiều lỗi), `wink`, `sleepy`.
- Act idle hợp nhân vật: chỉnh tai nghe, đọc sách, ngáp, đeo kính.

**Gắn với sự kiện hệ thống** (thay `ZONES`/`ROTATION` bằng event bus của app):

| Sự kiện app | Phản ứng |
|---|---|
| Bài viết đang chấm | `thinking` + mắt nhìn xuống |
| Chấm xong, band ≥ mục tiêu | act `proud` → `happy` |
| Chấm xong, nhiều lỗi ngữ pháp | `worried` → `encourage` + câu thoại |
| Đang gõ bài (WritingEditor) | mắt nhìn về phía ô soạn thảo |
| Hover nút Submit | `wink` / `happy` (giống nút Contact của Mina) |
| Im 30–45s | act idle |

**Hướng đang chọn:** tạo video ngắn bằng Gemini từ `demo.png` rồi cắt khung. Prompt ở `docs/lunaria/FRAME_VIDEO_PROMPTS.md`.

**Pipeline tạo ảnh (rủi ro lớn nhất):**

1. Chốt 1 ảnh `rest` Lunaria: chính diện, đầu và vai cố định, nền trơn.
2. Dùng công cụ image edit giữ nhân vật (Gemini image, Higgsfield, ...). Mỗi lần chỉ yêu cầu đổi 1 chi tiết: "chỉ đổi hướng mắt sang trái, giữ nguyên mọi thứ khác".
3. Tách nền hàng loạt (rembg đã dùng trước đó).
4. **Kiểm tra căn khung**: pixel diff từng ảnh với `rest`, ngoài vùng mắt/miệng phải gần 0. Ảnh nào lệch thì căn lại (dịch/scale) hoặc tạo lại.
5. Đo lại `zoneAt` và `SPOT` theo khuôn mặt Lunaria.

**Phần code có thể giữ gần nguyên:** lưới da, `untangle`, crossfade, hit test alpha, khung act. Phần phải viết lại: bảng ảnh, vùng mặt, bộ não theo sự kiện app, bong bóng thoại.

## 9. Đã kiểm chứng / chưa

- Đã chạy: `npm run build` qua. Trang mở ở 5190, engine khởi động (`window.__faceEngine = true`), WebGL thay ảnh fallback, mắt đổi hướng khi rê chuột (có ảnh chụp).
- Chưa tự kiểm từng tương tác: kéo da, tap từng vùng, lắc chuột, act idle sau 30s. Mở trang và thử tay.
- Giả định chưa xác minh: ảnh tạo bằng Higgsfield; con số "30 ảnh đủ cho Lunaria" là ước lượng.
