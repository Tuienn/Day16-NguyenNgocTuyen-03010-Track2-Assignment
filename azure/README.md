# Lab 16 trên Azure

## Kết quả

- Đã triển khai VM Ubuntu 22.04 Standard_B2s_v2 ở Southeast Asia bằng Azure CLI.
- Subscription hạn chế East US và B2s; B2s_v2 dùng được khi không chỉ định zone.
- Cloud-init thành công, benchmark chạy trên dữ liệu thật; kết quả trong `benchmark_result.json`.
- Dataset tải bằng Kaggle trên local rồi chuyển CSV lên VM; không chuyển khóa Kaggle lên VM.
- `benchmark-output.log` và `resource-usage.log` là output SSH thật.
- `benchmark-output.png`, `resource-usage.png` là ảnh dựng từ log, không phải screenshot terminal nguyên bản. Nếu yêu cầu chấm bài bắt buộc screenshot terminal nguyên bản, hai ảnh này cần được thay bằng screenshot của terminal hiển thị log.
- `cost-management-screenshot.png` là ảnh Billing Portal người dùng cung cấp ngày 05/10/2026, hiển thị chi phí tháng 10 là **US$0.03** (VM US$0.02, IP US$0.01, disk US$0.00 sau làm tròn).
- `cost-management.json` là phản hồi API thật thu ngày 05/10/2026 cho resource group `ai-lab-rg`: tổng **0.02565827022222222 USD**, làm tròn thành **US$0.03**. Truy vấn cho khoảng 01–05/10/2026 lưu trong `cost-query.json`; dự toán và nguồn giá xem `cost-estimate.md`.
- Báo cáo 10 dòng: `report.md`. Cloud-init đã dùng: `cloud-init-cpu.yaml`.
- Dọn tài nguyên theo yêu cầu README; trạng thái xác nhận xem `cleanup-status.json`.

Private key `lab-key` chỉ phục vụ lab, đã được loại khỏi Git.

Repo lưu mã triển khai, cloud-init, benchmark, kết quả metrics, dự toán, báo cáo, ảnh Cost Management mới và phản hồi API chi phí thực tế. Các log, ảnh khác, phản hồi Azure còn lại, dataset và model được giữ local và loại khỏi Git; các file bằng chứng có thể tìm trong gói nộp bài local `lab16-azure-deliverables.zip`.

`deploy.sh` dùng Azure CLI để tạo nhóm tài nguyên và VM; từ chối dùng nhóm có sẵn nếu không mang tag của lab. VM B2s_v2 có 2 vCPU và 8 GiB RAM, khác RAM của B2s trong README.
