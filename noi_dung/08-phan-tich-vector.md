---
thu_tu: 8
dinh_danh: quy-trinh-phan-tich-vector
tieu_de: Quy trình phân tích vector
nhom: Vector
tom_tat: Kết hợp vùng đệm, lân cận, overlay, thống kê vùng và mạng lưới thành một quy trình có thể kiểm toán.
---
# Từ câu hỏi đến phép toán

Không nên chọn công cụ chỉ vì tên nghe phù hợp. Hãy chuyển câu hỏi nghiệp vụ thành quan hệ không gian. Ví dụ: “bao nhiêu hộ dân tiếp cận điểm y tế trong 15 phút?” cần mô hình mạng giao thông và thời gian, không chỉ vùng đệm đường thẳng.

## Vùng đệm

```python
tram = tram.to_crs(crs_phan_tich)
vung_500m = tram.assign(geometry=tram.buffer(500))
```

Vùng đệm phù hợp với khoảng cách Euclid. Với sông, đường hoặc rào cản, khoảng cách mạng hoặc chi phí tích lũy có ý nghĩa hơn.

## Đối tượng gần nhất

```python
gan_nhat = gpd.sjoin_nearest(
    khu_dan_cu,
    tram[["ma_tram", "geometry"]],
    how="left",
    max_distance=5_000,
    distance_col="khoang_cach_m",
)
```

Nếu có nhiều trạm cùng khoảng cách, kết quả có thể chứa nhiều dòng cho một khu dân cư. Hãy xây dựng quy tắc chọn theo công suất, loại trạm hoặc định danh ổn định.

## Tỷ lệ diện tích

```python
xa = xa.to_crs(crs_phan_tich)
ngap = ngap.to_crs(crs_phan_tich)

xa = xa.assign(dien_tich_xa_m2=xa.area)
giao = gpd.overlay(
    xa[["ma_xa", "dien_tich_xa_m2", "geometry"]],
    ngap[["cap_do", "geometry"]],
    how="intersection",
)
giao["dien_tich_ngap_m2"] = giao.area

thong_ke = (
    giao.groupby("ma_xa", as_index=False)["dien_tich_ngap_m2"].sum()
    .merge(xa[["ma_xa", "dien_tich_xa_m2"]], on="ma_xa", validate="one_to_one")
)
thong_ke["ty_le_ngap"] = thong_ke["dien_tich_ngap_m2"] / thong_ke["dien_tich_xa_m2"]
```

Kiểm tra `ty_le_ngap <= 1`. Nếu vượt 1, các polygon ngập có thể chồng lấn hoặc lớp hành chính có lỗi.

## Làm việc với mạng giao thông

OSMnx và NetworkX hỗ trợ mạng có hướng, trọng số và đường đi ngắn nhất.

```python
import networkx as nx
import osmnx as ox

mang = ox.graph_from_place("Vĩnh Long, Việt Nam", network_type="drive")
mang = ox.add_edge_speeds(mang)
mang = ox.add_edge_travel_times(mang)

nut_dau = ox.distance.nearest_nodes(mang, X=105.96, Y=10.25)
nut_cuoi = ox.distance.nearest_nodes(mang, X=105.99, Y=10.24)
tuyen = nx.shortest_path(mang, nut_dau, nut_cuoi, weight="travel_time")
```

Dữ liệu OpenStreetMap thay đổi theo thời gian và mức độ đầy đủ không đồng đều. Ghi ngày tải, bộ lọc và loại mạng.

## Sai số biên và độ chính xác giả

Kết quả 12,347 km không có nghĩa chính xác đến một mét nếu dữ liệu nguồn ở tỷ lệ 1:50.000. Làm tròn theo độ chính xác thực và mô tả ảnh hưởng của:

- Sai lệch vị trí.
- Khác thời điểm.
- Quy tắc ghép đối tượng ở ranh.
- Thiếu đối tượng hoặc thuộc tính.
- CRS và biến dạng phép chiếu.

## Bài tập công cụ nhỏ

Xây dựng chỉ số tiếp cận trường học theo xã:

1. Chuẩn hóa CRS và dữ liệu đầu vào.
2. Tìm trường gần nhất cho tâm dân cư.
3. Tính khoảng cách mạng nếu có dữ liệu đường.
4. Tổng hợp trung vị và phân vị 90 theo xã.
5. Bản đồ hóa, đồng thời liệt kê xã thiếu dữ liệu.
