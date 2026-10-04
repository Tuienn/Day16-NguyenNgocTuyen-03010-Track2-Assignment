# Lab 16 trên Azure

## Kết quả

- Đã triển khai VM Ubuntu 22.04 Standard_B2s_v2 ở Southeast Asia bằng Azure CLI.
- Subscription hạn chế East US và B2s; B2s_v2 dùng được khi không chỉ định zone.
- Cloud-init thành công, benchmark chạy trên dữ liệu thật; kết quả trong `benchmark_result.json`.
- Dataset tải bằng Kaggle trên local rồi chuyển CSV lên VM; không chuyển khóa Kaggle lên VM.
- `benchmark-output.log` và `resource-usage.log` là output SSH thật.
- `benchmark-output.png`, `resource-usage.png` là ảnh dựng từ log, không phải screenshot terminal nguyên bản. Nếu yêu cầu chấm bài bắt buộc screenshot terminal nguyên bản, hai ảnh này cần được thay bằng screenshot của terminal hiển thị log.
- `cost-management-screenshot.jpg` là ảnh Portal thật nhưng chưa có số tiền ghi nhận.
- `cost-management.json` có rows rỗng lúc thu; dự toán và nguồn giá xem `cost-estimate.md`.
- Báo cáo 10 dòng: `report.md`. Cloud-init đã dùng: `cloud-init-cpu.yaml`.
- Dọn tài nguyên theo yêu cầu README; trạng thái xác nhận xem `cleanup-status.json`.

Private key `lab-key` chỉ phục vụ lab, đã được loại khỏi Git.

Log, ảnh bằng chứng, phản hồi Azure theo từng lần chạy, dataset và model được giữ local và loại khỏi Git. Repo lưu mã triển khai, cloud-init, benchmark, kết quả metrics, dự toán và báo cáo; các file bằng chứng có thể tìm trong gói nộp bài local `lab16-azure-deliverables.zip`.

`deploy.sh` dùng Azure CLI để tạo nhóm tài nguyên và VM; từ chối dùng nhóm có sẵn nếu không mang tag của lab. VM B2s_v2 có 2 vCPU và 8 GiB RAM, khác RAM của B2s trong README.
