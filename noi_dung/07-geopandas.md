---
thu_tu: 7
dinh_danh: phan-tich-vector-geopandas
tieu_de: Phân tích vector với GeoPandas
nhom: Vector
tom_tat: Đọc, làm sạch, truy vấn, ghép và xuất dữ liệu vector bằng giao diện quen thuộc của Pandas.
---
# GeoDataFrame

GeoPandas mở rộng `DataFrame` bằng cột hình học và CRS. Mỗi `GeoDataFrame` có một cột hình học đang hoạt động; các cột hình học khác có thể tồn tại nhưng cần được quản lý rõ ràng.

```python
import geopandas as gpd

xa = gpd.read_file("du_lieu/goc/hanh_chinh.gpkg", layer="xa")
truong_hoc = gpd.read_file("du_lieu/goc/cong_trinh.gpkg", layer="truong_hoc")

print(xa.crs)
print(xa.geometry.name)
print(xa.geom_type.value_counts())
```

## Chọn và chuẩn hóa cột

```python
xa_sach = (
    xa.rename(columns={"Ten_Xa": "ten_xa", "Ma_Xa": "ma_xa"})
    .loc[:, ["ma_xa", "ten_xa", "dan_so", "geometry"]]
    .drop_duplicates(subset="ma_xa")
)

assert xa_sach["ma_xa"].notna().all()
assert xa_sach["ma_xa"].is_unique
```

Chuẩn hóa tên cột ngay sau khi đọc giúp phần còn lại của quy trình không phụ thuộc cách viết trong nguồn.

## Ghép theo thuộc tính

```python
import pandas as pd

thong_ke = pd.read_csv("du_lieu/goc/dan_so.csv", dtype={"ma_xa": "string"})
xa_co_dan_so = xa_sach.merge(
    thong_ke,
    on="ma_xa",
    how="left",
    validate="one_to_one",
    indicator=True,
)

print(xa_co_dan_so["_merge"].value_counts())
```

`validate` phát hiện quan hệ khóa không đúng kỳ vọng. `indicator` giúp tìm bản ghi không ghép được thay vì âm thầm tạo giá trị thiếu.

## Ghép không gian

```python
truong_hoc = truong_hoc.to_crs(xa_sach.crs)
truong_theo_xa = gpd.sjoin(
    truong_hoc,
    xa_sach[["ma_xa", "ten_xa", "geometry"]],
    how="left",
    predicate="within",
)

so_truong = (
    truong_theo_xa.groupby("ma_xa", dropna=False)
    .size()
    .rename("so_truong")
    .reset_index()
)
```

Điểm nằm đúng trên ranh có thể không ghép với `within`. Tùy bài toán, dùng `intersects`, sửa dữ liệu hoặc xây dựng quy tắc phân xử có thể kiểm toán.

## Overlay và dissolve

```python
vung_ngap = gpd.read_file("du_lieu/goc/ngap.gpkg").to_crs(xa_sach.crs)
giao = gpd.overlay(xa_sach, vung_ngap, how="intersection", keep_geom_type=True)
giao["dien_tich_ngap_m2"] = giao.geometry.area

ngap_theo_xa = giao.dissolve(by="ma_xa", aggfunc={"dien_tich_ngap_m2": "sum"})
```

Trước khi tính diện tích, đảm bảo CRS có đơn vị mét. Với lớp lớn, lọc theo vùng bao hoặc chỉ mục không gian trước khi overlay.

## Ghi dữ liệu

```python
xa_co_dan_so.to_file(
    "du_lieu/da_xu_ly/ket_qua.gpkg",
    layer="xa_co_dan_so",
    driver="GPKG",
)
xa_co_dan_so.to_parquet("du_lieu/da_xu_ly/xa_co_dan_so.parquet")
```

## Kiểm tra chất lượng

```python
assert xa_co_dan_so.crs is not None
assert xa_co_dan_so.geometry.is_valid.all()
assert xa_co_dan_so["ma_xa"].is_unique
assert xa_co_dan_so["dan_so"].ge(0).all()
```

## Bài tập

Tính số trường học trên 10.000 dân theo xã. Báo cáo riêng số điểm không ghép được và kiểm tra trực quan các điểm nằm gần ranh giới.
