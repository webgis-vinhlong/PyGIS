---
thu_tu: 6
dinh_danh: hinh-hoc-voi-shapely
tieu_de: Hình học không gian với Shapely
nhom: Vector
tom_tat: Tạo, kiểm tra và thao tác điểm, đường, vùng bằng mô hình hình học chuẩn của hệ sinh thái Python GIS.
---
# Mô hình hình học

Shapely làm việc với hình học phẳng: `Point`, `LineString`, `Polygon` và các dạng nhiều phần. Thư viện không tự hiểu hệ tọa độ; đơn vị của kết quả chính là đơn vị tọa độ đầu vào.

```python
from shapely import LineString, Point, Polygon

tram = Point(500_000, 1_133_000)
tuyen = LineString([(499_500, 1_132_800), (500_500, 1_133_200)])
khu_vuc = Polygon(
    [
        (499_800, 1_132_700),
        (500_600, 1_132_700),
        (500_600, 1_133_500),
        (499_800, 1_133_500),
    ]
)

assert khu_vuc.contains(tram)
print(tuyen.intersection(khu_vuc).length)
```

## Quan hệ không gian

Các vị từ phổ biến gồm `intersects`, `contains`, `within`, `touches`, `crosses`, `overlaps` và `disjoint`. Chọn quan hệ theo ngữ nghĩa bài toán:

- Điểm nằm hoàn toàn bên trong vùng: `within`.
- Hai đối tượng có bất kỳ phần chung nào: `intersects`.
- Hai vùng chỉ chung ranh: `touches`.
- Đường đi xuyên qua vùng: `crosses`.

Ranh giới không được tính là bên trong đối với `contains`. Nếu cần chấp nhận cả ranh giới, xem xét `covers`.

## Phép toán xây dựng

```python
vung_dem = tram.buffer(500)
phan_trong = vung_dem.intersection(khu_vuc)
phan_ngoai = vung_dem.difference(khu_vuc)
```

Do số thực dấu phẩy động, phép so sánh diện tích nên dùng dung sai:

```python
import math

assert math.isclose(
    phan_trong.area + phan_ngoai.area,
    vung_dem.area,
    rel_tol=1e-9,
)
```

## Hình học không hợp lệ

Polygon tự cắt hoặc vòng biên sai có thể làm overlay thất bại.

```python
from shapely import is_valid, make_valid
from shapely.validation import explain_validity

if not is_valid(khu_vuc):
    print(explain_validity(khu_vuc))
    khu_vuc = make_valid(khu_vuc)
```

`make_valid` có thể trả về `MultiPolygon` hoặc `GeometryCollection`. Sau khi sửa, hãy kiểm tra lại kiểu hình học và ý nghĩa nghiệp vụ, không chỉ kiểm tra cờ hợp lệ.

## Hiệu năng

Shapely hỗ trợ thao tác vector hóa trên mảng hình học. Khi tìm ứng viên lân cận trong tập lớn, dùng `STRtree` thay vì so sánh mọi cặp.

```python
from shapely import STRtree

cac_vung = [vung_dem, khu_vuc]
chi_muc = STRtree(cac_vung)
ung_vien = chi_muc.query(tram, predicate="intersects")
print(ung_vien)
```

## Bài tập

1. Tạo tuyến đường và ba vùng hành chính giả lập.
2. Tính chiều dài tuyến nằm trong từng vùng.
3. Tạo một Polygon tự cắt, kiểm tra nguyên nhân rồi sửa.
4. Viết kiểm thử bảo đảm tổng chiều dài các đoạn không vượt quá chiều dài tuyến ban đầu.
