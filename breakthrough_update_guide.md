# Hướng dẫn Cập nhật Hệ thống Nhiệm vụ Đột phá v2

Tài liệu này hướng dẫn bạn cách cập nhật cơ sở dữ liệu để hỗ trợ hệ thống **12 Nghi thức Đột phá** mới.

## Bước 1: Chạy SQL Migration
Vui lòng chạy file SQL sau trong công cụ quản lý Database (DBeaver, pgAdmin, vv.) hoặc qua terminal:

[Mở file breakthrough_rituals_v2.sql](file:///f:/Shadow_awakening/backend/app/db/migrations/breakthrough_rituals_v2.sql)

Lưu ý: File này bao gồm lệnh `ALTER TABLE` để thêm các cột mới và lệnh `INSERT` để nạp dữ liệu cho 12 giai đoạn đột phá.

## Bước 2: Cấu trúc Giai đoạn Đột phá
Mỗi lần đột phá (từ giai đoạn 1 đến 12) sẽ bao gồm:
1.  **Điều kiện nền**: Streak (Chuỗi ngày) tối thiểu.
2.  **3 Nhiệm vụ bắt buộc**: Ví dụ Deep Work, Số lượng habit, vv.
3.  **1 Nhiệm vụ tự chọn**: Bạn có thể chọn 1 trong 3 hướng (Trí tuệ, Thể lực, hoặc Tập trung). Khi bạn chọn, hệ thống sẽ chỉ theo dõi tiến độ của hướng đó.
4.  **Reflection cuối**: Viết bài tổng kết tại Tab Nhật ký. Bài viết phải đạt đủ số lượng từ quy định cho giai đoạn đó.

## Bước 3: Cơ chế Reset & Tăng trưởng
-   **Giữ lại**: Bạn giữ lại **30%** chỉ số hiện tại.
-   **Mở rộng**: Max Cap tăng **20%** mỗi giai đoạn.
-   **Scale Thưởng**: EXP và Điểm chỉ số từ các nhiệm vụ sau đó sẽ tăng mạnh để bù đắp cho Reset.

## Bước 4: Hiển thị Thẩm mỹ
-   **Danh hiệu (Title)**: Tự động cập nhật theo tên Nghi thức (ví dụ: Nghi thức Siêu Việt).
-   **Aura (Hào quang)**: Thay đổi hiệu ứng thị giác xung quanh Avatar tại Dashboard.

---

*Hệ thống đã sẵn sàng. Hãy nạp SQL và bắt đầu hành trình đột phá của bạn!*
