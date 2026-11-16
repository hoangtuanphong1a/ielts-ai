# Lunaria: yêu cầu ảnh nhân vật

Lunaria là nhân vật hướng dẫn sống trong từng trang (kiểu visual novel): ngồi trong cảnh, nói bằng bong bóng thoại + giọng đọc, phản ứng theo việc người học đang làm.

Web sẽ ghép ảnh theo lớp: **nền trang (CSS) → ảnh Lunaria (PNG trong suốt) → bong bóng thoại + nút lựa chọn (HTML thật)**.

## 1. Quy cách chung (bắt buộc)

| Mục | Yêu cầu |
|---|---|
| Định dạng | PNG nền trong suốt (không dính nền trắng / bóng đổ cứng) |
| Phong cách | Anime 2D giống 2 ảnh mẫu login / profile (chọn 1 phong cách, giữ cho mọi ảnh) |
| Nhân vật | Cùng 1 thiết kế: tóc bạch kim dài, tai elf, ruy băng đỏ, áo trắng bèo, váy đen, dây chuyền thánh giá bạc |
| Kích thước | Cạnh dài ≥ 2000 px |
| Căn khung | **Mọi biến thể của cùng 1 tư thế phải cùng kích thước canvas và cùng vị trí** (chồng lên nhau khớp từng pixel, chỉ khác mắt / miệng) |
| Ánh sáng | Sáng, tông lạnh xanh nhạt, hợp nền trắng của web |

## 2. Biến thể để cô ấy "sống"

Với **mỗi tư thế**, cần 3 file:

| File | Mô tả | Web dùng để |
|---|---|---|
| `<tu-the>.png` | Mắt mở, miệng khép | Trạng thái nghỉ |
| `<tu-the>-talk.png` | Giống hệt, chỉ **miệng hơi mở** | Đổi qua lại khi đang nói → mấp máy môi |
| `<tu-the>-blink.png` | Giống hệt, chỉ **mắt nhắm** | Chớp mắt ngẫu nhiên 3-6 giây/lần |

Có thêm (không bắt buộc): `<tu-the>-smile.png` (cười, khen khi đạt mục tiêu), `<tu-the>-think.png` (nghiêng đầu, khi đang chấm bài).

## 3. Danh sách tư thế theo trang

| Tư thế (tên file) | Trang | Mô tả cảnh |
|---|---|---|
| `sit-floor` | Login / Sign up | Ngồi dưới sàn, tay chống cằm, nhìn về phía form (như ảnh mẫu login) |
| `desk-headphones` | Profile, Dashboard | Ngồi bàn máy tính, đeo tai nghe, nhìn sang người dùng (như ảnh mẫu profile) |
| `desk-reading` | Writing editor | Cầm giấy / đọc bài, nghiêng về phía khung viết |
| `standing-point` | Kết quả chấm bài | Đứng, một tay chỉ sang bảng điểm |
| `cards` | Vocabulary | Cầm thẻ từ vựng |

Bắt đầu tối thiểu: **`sit-floor` + `desk-headphones`** (mỗi cái đủ 3 biến thể) là đủ để dựng cơ chế; các tư thế khác thêm dần.

## 4. Nơi đặt file

```
frontend/src/assets/lunaria/
  sit-floor.png
  sit-floor-talk.png
  sit-floor-blink.png
  desk-headphones.png
  desk-headphones-talk.png
  desk-headphones-blink.png
  ...
```

Gửi file nào là web tự nhận theo tên; thiếu biến thể `-talk` / `-blink` thì Lunaria vẫn hiện, chỉ không mấp máy môi / chớp mắt.

## 5. Gợi ý khi tạo ảnh bằng AI

- Dùng **cùng 1 seed / ảnh tham chiếu nhân vật** cho mọi lần tạo để giữ khuôn mặt.
- Tạo ảnh gốc trước, rồi dùng inpainting chỉ vùng mắt / miệng để ra `-blink` và `-talk` (giữ nguyên phần còn lại).
- Tách nền bằng công cụ remove background, kiểm tra viền tóc không còn quầng trắng.
