---
thu_tu: 1
dinh_danh: bat-dau
tieu_de: Bắt đầu với Python GIS
nhom: Khởi động
tom_tat: Hiểu bản chất dữ liệu không gian, chuẩn bị tư duy phân tích và chạy quy trình GIS đầu tiên.
---
# Mục tiêu

GIS không chỉ là phần mềm vẽ bản đồ. Một quy trình GIS tốt phải trả lời được bốn câu hỏi: dữ liệu mô tả đối tượng nào, chúng nằm ở đâu, quan hệ không gian giữa chúng là gì và kết quả có đủ tin cậy để ra quyết định hay không. Python giúp biến quy trình đó thành mã có thể đọc, kiểm thử, chạy lại và chia sẻ.

Sau chương này, bạn có thể:

- Phân biệt dữ liệu vector, raster và bảng thuộc tính.
- Nhận biết hệ tọa độ trước khi đo khoảng cách hoặc diện tích.
- Tổ chức một dự án để kết quả có thể tái lập.
- Chạy một phép phân tích vector ngắn bằng GeoPandas.

## Bức tranh tổng thể

Một dự án Python GIS thường đi qua sáu bước:

1. Xác định câu hỏi và đơn vị phân tích.
2. Thu thập dữ liệu cùng giấy phép, thời điểm và nguồn gốc.
3. Kiểm tra hình học, trường thuộc tính, giá trị thiếu và hệ tọa độ.
4. Chuẩn hóa, phân tích và lượng hóa độ bất định.
5. Trực quan hóa kết quả theo đúng ngữ nghĩa bản đồ.
6. Lưu mã, tham số, nhật ký và sản phẩm đầu ra.

> [!GHI CHÚ] Bản đồ đẹp chưa chắc là phân tích đúng. Hãy kiểm tra hệ tọa độ, độ phân giải, thời điểm thu nhận và phạm vi sử dụng trước khi diễn giải.

## Ví dụ đầu tiên

Đoạn mã dưới đây tạo ba điểm dịch vụ, chuyển sang hệ tọa độ phẳng phù hợp cho Việt Nam, tạo vùng phục vụ bán kính 500 mét rồi tính tổng diện tích.

```python
import geopandas as gpd
from shapely.geometry import Point

diem = gpd.GeoDataFrame(
    {
        "ten": ["Trạm A", "Trạm B", "Trạm C"],
        "geometry": [
            Point(105.97, 10.25),
            Point(105.99, 10.24),
            Point(106.01, 10.26),
        ],
    },
    crs="EPSG:4326",
)

# UTM múi 48 Bắc, đơn vị mét; cần kiểm tra lại theo vùng nghiên cứu thực tế.
diem_phang = diem.to_crs("EPSG:32648")
vung_phuc_vu = diem_phang.buffer(500)

print(f"Tổng diện tích thô: {vung_phuc_vu.area.sum() / 1_000_000:.2f} km²")
```

Kết quả trên là tổng diện tích của từng vùng đệm, nên phần chồng lấn có thể bị tính nhiều lần. Khi câu hỏi yêu cầu diện tích phủ duy nhất, hãy hợp nhất hình học trước:

```python
vung_hop_nhat = vung_phuc_vu.union_all()
print(f"Diện tích phủ duy nhất: {vung_hop_nhat.area / 1_000_000:.2f} km²")
```

## Cách học hiệu quả

Mỗi chương trong giáo trình có ba lớp: khái niệm, mã mẫu và bài tập. Đừng chỉ sao chép mã. Hãy đổi dữ liệu, tham số và dự đoán kết quả trước khi chạy. Khi kết quả khác dự đoán, hãy ghi rõ nguyên nhân.

| Giai đoạn | Việc nên làm | Sản phẩm |
|---|---|---|
| Đọc | Ghi lại thuật ngữ và giả định | Nhật ký học tập |
| Chạy | Tạo môi trường riêng, chạy từng ô lệnh | Kết quả tái lập |
| Thay đổi | Dùng dữ liệu địa phương, đổi tham số | Biến thể bài tập |
| Giải thích | Nêu ý nghĩa và giới hạn | Đoạn kết luận ngắn |

## Bài tập

1. Thêm một trạm mới vào ví dụ và so sánh diện tích phủ thô với diện tích phủ duy nhất.
2. Thử vùng đệm 250, 500 và 1.000 mét; giải thích tác động.
3. Viết ba câu mô tả nguồn sai số có thể xuất hiện trong bài toán vùng phục vụ.

## Tiêu chí hoàn thành

Bạn hoàn thành chương khi có thể giải thích vì sao không nên tạo vùng đệm theo mét trực tiếp trên `EPSG:4326`, đồng thời phân biệt được tổng diện tích các vùng với diện tích hợp nhất.
