---
thu_tu: 5
dinh_danh: he-toa-do-va-phep-chieu
tieu_de: Hệ tọa độ và phép chiếu với PyProj
nhom: Nền tảng
tom_tat: Hiểu CRS, trục tọa độ, đơn vị đo và lựa chọn phép chiếu phù hợp trước mọi phép tính hình học.
---
# CRS là một phần của dữ liệu

Một cặp số chỉ trở thành tọa độ khi biết hệ quy chiếu, thứ tự trục và đơn vị. `EPSG:4326` thường dùng kinh độ, vĩ độ theo WGS 84; đơn vị là độ. Các phép đo mét vuông hoặc khoảng cách mét cần CRS phẳng phù hợp với khu vực và mục đích.

## Gán khác với chuyển đổi

```python
import geopandas as gpd

lop = gpd.read_file("du_lieu/goc/diem.geojson")

# Chỉ dùng khi chắc chắn dữ liệu đang là WGS 84 nhưng bị thiếu nhãn.
lop = lop.set_crs("EPSG:4326", allow_override=False)

# Tính lại tọa độ sang CRS khác.
lop_utm = lop.to_crs("EPSG:32648")
```

`set_crs()` chỉ gắn nhãn, không thay đổi con số tọa độ. `to_crs()` thực hiện phép biến đổi. Gán sai CRS có thể tạo kết quả nhìn hợp lý nhưng nằm sai vị trí.

## PyProj và thứ tự trục

```python
from pyproj import CRS, Transformer

wgs84 = CRS.from_epsg(4326)
utm48n = CRS.from_epsg(32648)

bo_chuyen = Transformer.from_crs(wgs84, utm48n, always_xy=True)
x, y = bo_chuyen.transform(105.97, 10.25)
print(round(x, 2), round(y, 2))
```

`always_xy=True` giúp đầu vào luôn là kinh độ, vĩ độ. Đây là lựa chọn rõ ràng khi mã nhận dữ liệu theo trật tự phổ biến của GIS.

## Chọn CRS cho phân tích

Không có CRS tốt nhất cho mọi mục đích:

- Đo khoảng cách cục bộ: CRS phẳng có biến dạng khoảng cách thấp tại khu vực.
- Đo diện tích: phép chiếu bảo toàn diện tích.
- Bản đồ toàn cầu: chọn phép chiếu theo mục đích trình bày, không đo trực tiếp.
- Lưu trữ và trao đổi web: thường dùng WGS 84, nhưng phân tích cần chuyển đổi.
- Web map nền: Web Mercator thuận tiện hiển thị nhưng biến dạng diện tích mạnh ở vĩ độ cao.

> [!CẢNH BÁO] Mã EPSG trong ví dụ chỉ là minh họa. Công cụ hành chính, đo đạc hoặc pháp lý phải sử dụng hệ quy chiếu do cơ quan có thẩm quyền quy định.

## Đo trắc địa trên ellipsoid

Khi cần khoảng cách giữa hai tọa độ địa lý mà không chọn CRS phẳng:

```python
from pyproj import Geod

trac_dia = Geod(ellps="WGS84")
phuong_vi_di, phuong_vi_ve, khoang_cach_m = trac_dia.inv(
    105.97, 10.25,
    106.70, 10.78,
)
print(f"{khoang_cach_m / 1_000:.1f} km")
```

## Kiểm tra trước khi ghép lớp

```python
assert lop_a.crs is not None and lop_b.crs is not None
lop_b = lop_b.to_crs(lop_a.crs)
assert lop_a.crs == lop_b.crs
```

Hai lớp có hình thức tọa độ giống nhau chưa chắc cùng CRS. Luôn kiểm tra đối tượng CRS thay vì tên tệp hoặc phỏng đoán.

## Bài tập

1. Chuyển ba điểm tại Vĩnh Long từ WGS 84 sang một CRS phẳng phù hợp.
2. Tính khoảng cách bằng CRS phẳng và bằng `Geod.inv`.
3. Giải thích chênh lệch và ghi rõ giả định của từng cách.
