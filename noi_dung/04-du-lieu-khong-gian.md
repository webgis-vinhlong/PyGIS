---
thu_tu: 4
dinh_danh: mo-hinh-du-lieu-khong-gian
tieu_de: Mô hình dữ liệu và định dạng GIS
nhom: Nền tảng
tom_tat: Chọn đúng vector, raster, lưới đa chiều và định dạng lưu trữ cho từng quy mô dự án.
---
# Vector, raster và mảng đa chiều

Vector mô tả các đối tượng rời rạc bằng điểm, đường, vùng. Raster chia không gian thành lưới ô và phù hợp với hiện tượng liên tục như độ cao, nhiệt độ hoặc phản xạ phổ. Xarray mở rộng mảng raster thành dữ liệu nhiều chiều có nhãn thời gian, độ cao, band và tọa độ.

| Mô hình | Phù hợp | Không phù hợp |
|---|---|---|
| Điểm | Trạm đo, cây, sự kiện | Đối tượng có kích thước đáng kể |
| Đường | Đường giao thông, sông | Hiện tượng phủ kín bề mặt |
| Vùng | Thửa đất, hành chính | Biến đổi liên tục trong vùng |
| Raster | Ảnh vệ tinh, DEM, khí hậu | Ranh giới pháp lý cần độ chính xác cao |
| Mảng đa chiều | Chuỗi thời gian, mô hình khí hậu | Tệp nhỏ chỉ có một lớp |

## Thuộc tính và hình học

Một lớp vector gồm hình học và bảng thuộc tính. Mỗi hàng phải đại diện đúng một đơn vị quan sát. Khóa định danh cần ổn định và không nên được suy ra từ số thứ tự dòng.

```python
import geopandas as gpd

lop = gpd.read_file("du_lieu/goc/ranh_gioi.gpkg", layer="xa")

assert lop.crs is not None
assert lop["ma_xa"].is_unique
assert lop.geometry.notna().all()
assert (~lop.geometry.is_empty).all()
```

## Chọn định dạng

- **GeoPackage**: mặc định tốt cho dữ liệu vector cục bộ; một tệp chứa nhiều lớp, hỗ trợ chỉ mục.
- **GeoParquet**: phù hợp xử lý phân tích và dữ liệu lớn; nén tốt, đọc theo cột.
- **GeoJSON**: dễ trao đổi trên web nhưng lớn, kiểu dữ liệu hạn chế, không tối ưu cho phân tích nặng.
- **Shapefile**: chỉ dùng khi hệ thống cũ bắt buộc; tên trường ngắn, nhiều tệp thành phần, hạn chế Unicode.
- **Cloud Optimized GeoTIFF**: raster có thể đọc theo cửa sổ qua HTTP.
- **Zarr**: mảng lớn, nhiều chiều, đọc song song theo khối.

> [!MẸO] Dùng GeoPackage hoặc GeoParquet cho quy trình mới. Chỉ xuất Shapefile ở bước cuối nếu đối tác yêu cầu.

## Độ phân giải và tỷ lệ

Một raster 10 mét không đảm bảo vị trí chính xác 10 mét. Độ phân giải ô, độ chính xác định vị, phương pháp nội suy và thời điểm thu nhận là các khái niệm khác nhau. Tăng kích thước raster bằng nội suy không tạo thêm thông tin thực.

## Quy tắc dữ liệu gốc

1. Lưu nguyên tệp tải về và tổng kiểm SHA-256 nếu dữ liệu quan trọng.
2. Ghi nguồn, giấy phép, ngày tải, hệ tọa độ và phiên bản.
3. Không chỉnh tay dữ liệu gốc trong QGIS rồi ghi đè.
4. Ghi mọi phép sửa hình học hoặc đổi kiểu cột thành mã.
5. Xuất dữ liệu đã xử lý sang thư mục riêng.

## Kiểm kê nhanh

```python
from pathlib import Path
import geopandas as gpd

for duong_dan in Path("du_lieu/goc").glob("*.gpkg"):
    for ten_lop in gpd.list_layers(duong_dan)["name"]:
        lop = gpd.read_file(duong_dan, layer=ten_lop)
        print(duong_dan.name, ten_lop, len(lop), lop.crs, lop.geom_type.unique())
```

## Bài tập

Chọn ba bộ dữ liệu cho một bài toán ngập đô thị. Với mỗi bộ, ghi mô hình dữ liệu, định dạng, độ phân giải hoặc tỷ lệ, thời điểm, giấy phép và hạn chế sử dụng.
