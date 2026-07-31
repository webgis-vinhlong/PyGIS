---
thu_tu: 14
dinh_danh: osm-va-nen-tang-dam-may
tieu_de: OpenStreetMap và nền tảng địa không gian đám mây
nhom: Ứng dụng
tom_tat: Truy vấn OSM, Earth Engine và danh mục dữ liệu đám mây với giới hạn sử dụng rõ ràng.
---
# Dữ liệu mở không có nghĩa là không có điều kiện

OpenStreetMap, Earth Engine, Planetary Computer và Copernicus Data Space giúp tiếp cận dữ liệu lớn, nhưng mỗi nguồn có giấy phép, hạn mức, cơ chế xác thực và độ đầy đủ khác nhau.

## OSMnx

```python
import osmnx as ox

dia_diem = "Vĩnh Long, Việt Nam"
mang_duong = ox.graph_from_place(dia_diem, network_type="drive")
cong_trinh = ox.features_from_place(
    dia_diem,
    tags={"amenity": ["school", "hospital", "clinic"]},
)

ox.save_graphml(mang_duong, "du_lieu/goc/mang_duong.graphml")
cong_trinh.to_file("du_lieu/goc/cong_trinh_osm.gpkg", driver="GPKG")
```

Hình học OSM do cộng đồng đóng góp. `amenity=hospital` không bảo đảm cùng tiêu chuẩn phân loại với dữ liệu ngành y tế. Hãy đối chiếu nguồn chính thức trước quyết định quan trọng.

## Overpass có trách nhiệm

- Giới hạn vùng và loại đối tượng.
- Lưu bộ nhớ đệm, không gửi lại truy vấn giống nhau.
- Tôn trọng hạn mức và chính sách máy chủ.
- Ghi thời điểm truy vấn vì dữ liệu thay đổi.
- Ghi công OpenStreetMap theo yêu cầu giấy phép.

## Google Earth Engine

Earth Engine thực thi biểu thức phía máy chủ. Không gọi `getInfo()` trong vòng lặp lớn.

```python
import ee

ee.Initialize()

vung = ee.Geometry.Rectangle([105.8, 10.1, 106.2, 10.5])
bo_suu_tap = (
    ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
    .filterBounds(vung)
    .filterDate("2025-01-01", "2025-03-31")
    .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
)

print(bo_suu_tap.size().getInfo())
```

Việc khởi tạo, công cụ đám mây và quyền truy cập phụ thuộc chính sách hiện hành của nhà cung cấp.

## STAC và đọc theo vùng

STAC cho phép tìm tài sản; COG cho phép đọc một cửa sổ thay vì tải toàn tệp. Kết hợp hai chuẩn giúp quy trình đám mây hiệu quả:

1. Tìm item theo không gian, thời gian và mây.
2. Chọn asset và đọc siêu dữ liệu.
3. Ký URL nếu nhà cung cấp yêu cầu.
4. Đọc đúng vùng và độ phân giải.
5. Lưu item ID, URL danh mục và thời điểm truy cập.

## Bài tập

So sánh số cơ sở y tế từ OSM với một nguồn chính thức trên cùng khu vực. Lập bảng các đối tượng khớp, chỉ có ở OSM và chỉ có ở nguồn chính thức; không kết luận nguồn nào “đúng” nếu chưa kiểm chứng thực địa.
