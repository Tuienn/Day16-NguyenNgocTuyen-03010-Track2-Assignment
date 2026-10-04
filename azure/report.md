# Báo cáo Lab 16 — Azure CPU / LightGBM

1. Triển khai bằng Azure CLI tại Southeast Asia, dùng Ubuntu 22.04 và Standard_B2s_v2 (2 vCPU / 8 GiB), do B2s trong README bị hạn chế.
2. Cloud-init hoàn thành, cài môi trường ML trong virtualenv; SSH chỉ mở từ IP nguồn /32.
3. Dataset Credit Card Fraud có 284.807 dòng, 492 giao dịch gian lận; train/validation/test phân tầng, seed 42, test có 56.962 dòng.
4. Load dữ liệu mất 1,175 giây; training mất 5,058 giây và chọn iteration 130 bằng early stopping trên validation.
5. AUC-ROC đạt 0,96345; accuracy 0,998894, nhưng accuracy cao cần xem cùng độ mất cân bằng lớp.
6. F1 đạt 0,73418; precision 0,62590 và recall 0,88776 ở threshold 0,5: bắt được nhiều gian lận nhưng còn false positive.
7. Latency median 1 dòng là 0,691 ms, p95 là 0,723 ms (100 lần); throughput batch 1.000 dòng khoảng 275.584 dòng/giây (20 lần, sau warm-up).
8. Log tài nguyên được lấy sau benchmark, không thể dùng nó để suy ra CPU/RAM cực đại trong lúc training.
9. Giá niêm yết quy đổi khoảng 0,1131 USD/giờ; API chi phí chưa có dòng dữ liệu lúc thu, không có nghĩa chi phí bằng 0.
10. Bằng chứng gồm JSON metrics, log SSH, cloud-init, mã benchmark, ảnh Portal và phản hồi Retail Prices API; trạng thái dọn dẹp lưu riêng.
