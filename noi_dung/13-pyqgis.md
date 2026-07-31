---
thu_tu: 13
dinh_danh: tu-dong-hoa-qgis-voi-pyqgis
tieu_de: Tự động hóa QGIS với PyQGIS
nhom: Ứng dụng
tom_tat: Điều khiển dự án, lớp dữ liệu và thuật toán Processing bằng Python trong QGIS 3.44.
---
# Khi nào dùng PyQGIS?

PyQGIS phù hợp khi quy trình cần thuật toán Processing, bố cục in, kiểu ký hiệu hoặc giao diện QGIS. Với xử lý dữ liệu độc lập, GeoPandas và Rasterio thường dễ triển khai trên máy chủ hơn. Hai hệ sinh thái có thể bổ sung nhau.

## Bảng điều khiển Python

Mở **Trình bổ sung → Bảng điều khiển Python** trong QGIS. Đối tượng `iface` chỉ tồn tại trong phiên giao diện QGIS.

```python
from qgis.core import QgsProject, QgsVectorLayer

duong_dan = r"D:\du-an\du_lieu\hanh_chinh.gpkg|layername=xa"
lop = QgsVectorLayer(duong_dan, "Ranh giới xã", "ogr")

if not lop.isValid():
    raise RuntimeError("Không thể mở lớp ranh giới xã")

QgsProject.instance().addMapLayer(lop)
print(lop.featureCount(), lop.crs().authid())
```

## Duyệt đối tượng có bộ lọc

```python
from qgis.core import QgsFeatureRequest

yeu_cau = (
    QgsFeatureRequest()
    .setFilterExpression('"dan_so" > 10000')
    .setSubsetOfAttributes(["ma_xa", "ten_xa", "dan_so"], lop.fields())
)

for doi_tuong in lop.getFeatures(yeu_cau):
    print(doi_tuong["ma_xa"], doi_tuong["ten_xa"])
```

Chỉ yêu cầu trường cần thiết giúp giảm đọc dữ liệu, đặc biệt với lớp từ cơ sở dữ liệu.

## Chạy Processing

```python
import processing

tham_so = {
    "INPUT": lop,
    "DISTANCE": 500,
    "SEGMENTS": 12,
    "DISSOLVE": True,
    "END_CAP_STYLE": 0,
    "JOIN_STYLE": 0,
    "MITER_LIMIT": 2,
    "OUTPUT": "TEMPORARY_OUTPUT",
}

ket_qua = processing.run("native:buffer", tham_so)
QgsProject.instance().addMapLayer(ket_qua["OUTPUT"])
```

Tên và tham số thuật toán có thể kiểm tra trong hộp công cụ Processing bằng lệnh **Sao chép dưới dạng lệnh Python**. Điều này chính xác hơn ghi nhớ.

## Chạy độc lập ngoài QGIS

Python hệ thống thường không tìm thấy `qgis`. Hãy dùng môi trường Python do QGIS cung cấp và khởi tạo ứng dụng:

```python
from qgis.core import QgsApplication

ung_dung = QgsApplication([], False)
ung_dung.initQgis()

try:
    # Nạp nhà cung cấp Processing và chạy công việc tại đây.
    pass
finally:
    ung_dung.exitQgis()
```

Đường dẫn tiền tố và cách khởi động khác nhau theo hệ điều hành và bản cài. Tham khảo tài liệu chính thức đúng phiên bản QGIS.

## Plugin hay tập lệnh?

| Nhu cầu | Hình thức |
|---|---|
| Một lần, một người | Bảng điều khiển Python |
| Quy trình lặp lại | Tập lệnh Processing |
| Công cụ có tham số chuẩn | Thuật toán Processing |
| Giao diện, nút, bản đồ tương tác | Plugin Python |
| Chạy nền tự động | Ứng dụng PyQGIS độc lập |

## Bài tập

Viết tập lệnh Processing nhận lớp điểm và khoảng cách, tạo vùng đệm hợp nhất, ghi GeoPackage và trả về diện tích.

## Tài liệu chính

- [PyQGIS Developer Cookbook 3.44](https://docs.qgis.org/3.44/en/docs/pyqgis_developer_cookbook/)
- [Tài liệu API PyQGIS](https://qgis.org/pyqgis/)
