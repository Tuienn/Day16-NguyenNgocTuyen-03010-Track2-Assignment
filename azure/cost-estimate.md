# Dự toán chi phí Azure cho Lab 16

Ngày tra giá: 04/10/2026. Vùng: Southeast Asia. Tiền tệ: USD.
Nguồn: Azure Retail Prices API (https://prices.azure.com/api/retail/prices).
Đây là dự toán theo giá niêm yết, không phải hóa đơn hoặc số tiền Azure đã ghi nhận.

- VM Linux `Standard_B2s_v2`, 2 vCPU / 8 GiB: **0.106 USD/giờ**.
- Public IPv4 Standard Regional: **0.005 USD/giờ**.
- OS disk Standard HDD LRS 30 GiB, tính theo tier S4 32 GiB: **1.536 USD/tháng**, quy đổi minh họa 730 giờ/tháng là **0.002104 USD/giờ**.
- Tổng cố định quy đổi: **0.113104 USD/giờ**, chưa cộng giao dịch disk, băng thông vượt miễn phí và thuế.
- Disk operations S4 LRS: **0.0005 USD/10.000 giao dịch**. Chưa có số giao dịch thực tế để tính khoản này.

Dự toán nếu giữ cả VM, disk và IP trong cùng khoảng thời gian:
- 10 phút: khoảng **0.0189 USD**.
- 15 phút: khoảng **0.0283 USD**.
- 30 phút: khoảng **0.0566 USD**.
- 1 giờ: khoảng **0.1131 USD**.
- 24 giờ: khoảng **2.7145 USD**.

Các mốc trên là quy đổi tỷ lệ, không cam kết cách làm tròn hoặc chu kỳ tính tiền của từng meter.
Thời gian tính tiền gồm khởi tạo/cài môi trường và lúc chờ thu bằng chứng, không chỉ thời gian training.
Giá thực tế có thể khác theo ưu đãi hoặc credit Azure for Students; credit không làm giá niêm yết bằng 0.
Nếu deallocate VM thì compute dừng tính tiền, nhưng disk và IP còn tồn tại có thể vẫn tính tiền.

## Trang tra cứu

- Cost Management trong Portal: https://portal.azure.com/#view/Microsoft_Azure_CostManagement/Menu/~/overview/openedBy/AzurePortal
- Cost Management + Billing: https://portal.azure.com/#blade/Microsoft_Azure_GTM/ModernBillingMenuBlade
- Pricing Calculator: https://azure.microsoft.com/en-us/pricing/calculator/
- Giá VM Linux: https://azure.microsoft.com/en-us/pricing/details/virtual-machines/linux/
- Độ trễ dữ liệu chi phí: https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/understand-cost-mgt-data

## Bằng chứng và giới hạn

- `cost-management.json`: phản hồi thật của Azure Cost Management API cho resource group `ai-lab-rg`, thu lại ngày 05/10/2026. Chi phí ngày 04/10: Virtual Machines **0.019433616 USD**, Virtual Network **0.00582222222222222 USD**, Storage **0.000402432 USD**, Bandwidth **0 USD**. Tổng **0.02565827022222222 USD**, làm tròn thành **US$0.03**.
- `cost-management-screenshot.png`: ảnh Billing Portal người dùng cung cấp ngày 05/10/2026, hiển thị Current charges và Pre-tax total tháng 10 là **US$0.03**; VM **US$0.02**, IP **US$0.01**, disk **US$0.00** sau làm tròn. Amount due **US$0.00** là số tiền đến hạn, không phải tổng chi phí phát sinh. Ảnh không hiển thị bộ lọc resource group; phạm vi `ai-lab-rg` được xác nhận riêng qua phản hồi API.
- `prices-vm.json`, `prices-disk.json`, `prices-ip.json`: phản hồi nguyên gốc từ Retail Prices API làm căn cứ dự toán.
- `cost-query.json`: nội dung truy vấn `ActualCost`, khoảng thời gian cố định 01–05/10/2026 (UTC), theo ngày và dịch vụ. Phạm vi resource group lab nằm trong URL API ở `cost-management.json`, không nằm trong request body.

Dữ liệu chi phí cập nhật có độ trễ. Trang Cost Management data của Microsoft nêu độ trễ tùy loại tài khoản; không suy diễn rằng chưa có bản ghi đồng nghĩa không phát sinh phí.
