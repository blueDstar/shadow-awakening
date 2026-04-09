# Cập nhật Database cho cơ chế Nhiệm vụ (Refresh & Reroll)

Hệ thống bạn đang gặp lỗi khi tải trang nhiệm vụ hoặc thực hiện Reset/Xoay nhiệm vụ vì hai cột mới (`fail_reason` và `is_rerolled`) đã được thêm vào mã nguồn SQLAlchemy Model (`DailyQuest`) nhưng chưa được cập nhật vào PostgreSQL trong hệ thống thực tế.

Do cơ sở dữ liệu bị thiếu 2 cột này, bất kỳ truy vấn nào gọi bảng `daily_quests` đều sẽ bị PostgreSQL từ chối, dẫn đến lỗi màn hình đen hoặc loading liên tục trên ứng dụng Frontend.

Dưới đây là mã SQL để bạn chạy trực tiếp trên cơ sở dữ liệu PostgreSQL (qua Supabase, pgAdmin, hoặc terminal) nhằm thêm các cột còn thiếu:

```sql
-- Bước 1: Thêm cột fail_reason vào bảng daily_quests
ALTER TABLE daily_quests 
ADD COLUMN IF NOT EXISTS fail_reason VARCHAR(50);

-- Bước 2: Thêm cột is_rerolled vào bảng daily_quests với giá trị mặc định là FALSE
ALTER TABLE daily_quests 
ADD COLUMN IF NOT EXISTS is_rerolled BOOLEAN DEFAULT FALSE;

-- (Tuỳ chọn) Đảm bảo các nhiệm vụ cũ có giá trị is_rerolled = FALSE (nếu chưa có)
UPDATE daily_quests 
SET is_rerolled = FALSE 
WHERE is_rerolled IS NULL;
```

## Cách chạy lệnh SQL này
1. Nếu bạn dùng **Supabase**: Vào trang Dashboard của Supabase > Chọn Project của bạn > Nhấn vào tab **SQL Editor** ở thanh menu bên trái > Dán đoạn mã trên vào và nhấn **Run**.
2. Nếu bạn dùng **pgAdmin** hoặc kết nối cơ sở dữ liệu trực tiếp: Mở Query Tool và dán đoạn mã này vào, sau đó Execute.

Sau khi chạy xong lệnh SQL trên, hệ thống Refresh và Xoay nhiệm vụ sẽ hoạt động bình thường! Cả Backend và Frontend đều đã được set up đúng logic.
