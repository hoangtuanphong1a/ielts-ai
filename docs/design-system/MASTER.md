# IELTS AI — Design System (MASTER)

Nguồn token: [frontend/src/styles.css](../../frontend/src/styles.css). Bảng màu: [docs/color/palette.png](../color/palette.png).

## Hướng thiết kế

App học IELTS cho người Việt, phong cách tập trung và gọn. Font Be Vietnam Pro (self-host qua `@fontsource`), icon Phosphor, chuyển động tiết chế (150–600 ms, tôn trọng `prefers-reduced-motion`).

## Màu — chỉ 5 màu gốc + trắng

| Token gốc | Hex |
|---|---|
| `--navy` | `#03045E` |
| `--ocean` | `#0077B6` |
| `--sky` | `#00B4D8` |
| `--aqua` | `#90E0EF` |
| `--mist` | `#CAF0F8` |

Mọi màu khác là `color-mix` từ các màu trên. Không thêm hex mới.

### Token ngữ nghĩa

| Token | Light | Dark |
|---|---|---|
| `--bg` | mist 35% + trắng | navy |
| `--surface` | trắng | navy 82% + ocean |
| `--surface-soft` | mist | navy 65% + ocean |
| `--text` | navy | mist |
| `--text-muted` | navy 70% + trắng | mist 72% + navy |
| `--border` (trang trí) | aqua 60% + trắng | navy 55% + ocean |
| `--border-input` | ocean 80% + trắng | aqua 50% + surface |
| `--primary` / `--on-primary` | ocean / trắng | sky / navy |
| `--focus` | ocean | sky |

### Tương phản đã đo (WCAG)

| Cặp | Tỉ lệ | Đạt |
|---|---|---|
| navy / trắng | 17.75 | AAA |
| navy / bg light | 16.62 | AAA |
| text-muted / bg light | 6.92 | AA |
| trắng trên ocean (nút) | 4.87 | AA |
| ocean / bg light (link) | 4.56 | AA |
| border-input / trắng | 3.47 | ≥ 3 (non-text) |
| mist / navy (dark) | 14.65 | AAA |
| text-muted / surface (dark) | 6.70 | AA |
| navy trên sky (nút dark, nút hero) | 7.20 | AAA |
| border-input / surface (dark) | 3.50 | ≥ 3 |
| **trắng trên sky** | **2.46** | **Cấm** |

## Glass dashboard (2026-11-11)

Bố cục: sidebar kính (≥1024) → rail icon (768–1023) → thanh trên + tab bar kính (<768). Trang Tổng quan dùng bento 12 cột (band 7 + số liệu 5, tiêu chí 7 + bài gần đây 5).

**Light (chốt 2026-11-11):** nền trắng; khối / sidebar xanh nhạt `--panel` = mist 55% + trắng (#E2F7FB, navy 16.0, chữ phụ 8.92); mục đang chọn aqua 70% + trắng (navy 13.38); nút chính **navy** + chữ trắng (17.75), hover navy 70% + ocean (13.54); nút disabled dùng `--soft-strong` + chữ phụ, không dùng opacity; ô viết bài nền trắng.

Kính = `backdrop-filter: blur(20px) saturate(160%)` + viền + highlight inset. Light: nền trắng, 3 mảng radial nhạt ở góc (sky 22%, aqua 45%, mist 70%), viền panel aqua 55% pha trắng. Dark: nền navy, mảng ocean / sky. Đây là web approximation, không phải Apple Liquid Glass.

Độ đục chọn theo số đo trường hợp xấu nhất (panel đè lên mảng màu đậm nhất):

| Chế độ | Panel | Chữ chính | Chữ phụ | Link |
|---|---|---|---|---|
| Light | trắng 72% | navy ≥ 11.97 | navy 78% ≥ 6.67 | navy (ocean chỉ 3.28 trên kính, cấm làm link) |
| Dark | navy 72% | mist ≥ 9.05 | mist 80% ≥ 5.83 | aqua ≥ 7.36 |

Panel band / hero: navy pha 18% ocean rồi mới làm trong suốt 94%, tránh nền trắng xuyên qua ngả tím.

Fallback: không hỗ trợ `backdrop-filter` hoặc `prefers-reduced-transparency: reduce` → panel đặc (`--glass-strong`), tắt mảng màu nền.

## Quy tắc

- Chữ trắng không bao giờ đặt trên sky / aqua / mist.
- Lỗi: bảng màu không có đỏ → dùng `ErrorAlert` (icon `WarningCircle` + viền đậm + chữ, `role="alert"`). Không dựa vào màu.
- Không dùng accent bar trước tiêu đề. Không dùng em-dash trong UI.
- Bo góc: card 14px, input 10px, nút / chip / tag dạng pill.
- Vùng bấm tối thiểu 44px. Focus ring 3px màu `--focus`.

## Responsive

| Breakpoint | Bố cục |
|---|---|
| < 768 | Topnav ẩn, tab bar cố định dưới đáy; lưới 1 cột |
| ≥ 768 | Topnav; lưới 2 cột (danh sách đề, dashboard) |
| ≥ 1024 | Editor 2 cột (đề sticky bên trái); trang đăng nhập chia đôi |
| 1440 | Container tối đa 1120px |

## Trạng thái

Mọi trang có: loading (`PageSkeleton`), empty (`EmptyState` + hành động), error (`ErrorAlert`).
