---
thu_tu: 18
dinh_danh: du-an-tong-hop-vinh-long
tieu_de: Dự án tổng hợp tại Vĩnh Long
nhom: Dự án
tom_tat: Kết hợp toàn bộ kỹ năng để xây dựng bản đồ khả năng tiếp cận dịch vụ công có dữ liệu, kiểm thử và báo cáo.
---
# Đề bài

Xây dựng chỉ số khả năng tiếp cận cơ sở y tế theo đơn vị hành chính tại Vĩnh Long. Sản phẩm gồm lớp dữ liệu đã xử lý, bảng chỉ số, bản đồ tĩnh, bản đồ web và báo cáo phương pháp.

Đây là bài tập kỹ thuật, không thay thế số liệu hoặc kết luận của cơ quan chuyên môn.

## Câu hỏi phân tích

1. Mỗi khu dân cư cách cơ sở y tế gần nhất bao xa theo mạng đường?
2. Tỷ lệ dân số nằm trong ngưỡng thời gian 15, 30 và 45 phút là bao nhiêu?
3. Khu vực nào có ít lựa chọn thay thế khi một cơ sở ngừng hoạt động?
4. Độ đầy đủ dữ liệu ảnh hưởng kết quả ra sao?

## Dữ liệu cần thiết

| Dữ liệu | Thuộc tính tối thiểu | Kiểm tra |
|---|---|---|
| Hành chính | Mã, tên, dân số | Khóa duy nhất, polygon hợp lệ |
| Khu dân cư | Dân số hoặc trọng số | Thời điểm, phương pháp phân bổ |
| Cơ sở y tế | Loại, công suất, trạng thái | Nguồn chính thức, tọa độ |
| Mạng đường | Loại đường, chiều, tốc độ | Kết nối mạng, thời điểm |
| Rào cản | Phà, cầu, hạn chế | Quy tắc chi phí |

## Kiến trúc mã

```text
du-an-tiep-can/
├── du_lieu/goc/
├── du_lieu/da_xu_ly/
├── src/
│   ├── kiem_tra.py
│   ├── chuan_hoa.py
│   ├── mang_luoi.py
│   ├── chi_so.py
│   └── ban_do.py
├── tests/
├── ket_qua/
└── README.md
```

## Các mốc thực hiện

### Mốc 1: hồ sơ dữ liệu

Lập bảng nguồn, giấy phép, ngày tải, CRS, số bản ghi và giới hạn. Từ chối dữ liệu không rõ nguồn cho kết luận chính thức.

### Mốc 2: chuẩn hóa

Chuẩn hóa khóa, CRS, hình học và kiểu cột. Lưu số bản ghi trước và sau từng bước. Các đối tượng bị loại phải có bảng lý do.

### Mốc 3: mô hình mạng

Gắn điểm dân cư và cơ sở vào nút gần nhất. Kiểm tra khoảng cách gắn; điểm quá xa mạng cần được đánh dấu thay vì ép ghép.

### Mốc 4: chỉ số

Tính thời gian đến cơ sở gần nhất, thứ hai và theo từng loại. Tổng hợp theo xã bằng trung vị, phân vị 90 và tỷ lệ dân số trong ngưỡng.

### Mốc 5: kiểm chứng

Chọn mẫu tuyến, so sánh với nguồn định tuyến độc lập hoặc khảo sát. Thực hiện phân tích độ nhạy với tốc độ và thời gian chờ phà.

### Mốc 6: công bố

Xuất GeoPackage, CSV, PNG và HTML. Mỗi bản đồ có nguồn, thời điểm, đơn vị và cảnh báo giới hạn.

## Tiêu chí đánh giá

- 20% hồ sơ và kiểm tra dữ liệu.
- 25% mô hình phân tích hợp lý.
- 20% mã rõ ràng, có kiểm thử.
- 15% kiểm chứng và độ nhạy.
- 10% bản đồ dễ đọc, không gây hiểu sai.
- 10% tài liệu tái lập và đạo đức dữ liệu.

## Câu hỏi phản biện

Kết quả sẽ thay đổi thế nào nếu dùng khoảng cách đường thẳng? Dân số theo xã có đủ để đánh giá bất bình đẳng nội vùng không? Điểm cơ sở y tế từ OSM có thể thiếu loại hình nào? Những câu hỏi này phải xuất hiện trong phần giới hạn.
