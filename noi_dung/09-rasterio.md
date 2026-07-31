---
thu_tu: 9
dinh_danh: raster-voi-rasterio
tieu_de: Xử lý raster với Rasterio
nhom: Raster
tom_tat: Đọc siêu dữ liệu, quản lý NoData, cắt, đổi hệ tọa độ và xử lý raster theo cửa sổ.
---
# Raster là mảng có vị trí

Một raster không chỉ là ma trận số. Nó còn có CRS, phép biến đổi affine, kích thước ô, số band, kiểu dữ liệu và quy ước NoData. Mất bất kỳ phần nào có thể khiến mảng không còn ý nghĩa không gian.

## Đọc có kiểm soát

```python
import rasterio

with rasterio.open("du_lieu/goc/dem.tif") as nguon:
    print(nguon.crs)
    print(nguon.transform)
    print(nguon.bounds)
    print(nguon.res)
    print(nguon.nodata)
    dem = nguon.read(1, masked=True)

print(float(dem.mean()))
```

`masked=True` tạo mảng có mặt nạ từ NoData, tránh đưa ô không hợp lệ vào thống kê.

## Ghi và giữ hồ sơ

```python
with rasterio.open("du_lieu/goc/dem.tif") as nguon:
    dem = nguon.read(1, masked=True)
    do_doc = tinh_do_doc(dem, nguon.res)
    ho_so = nguon.profile.copy()
    ho_so.update(dtype="float32", count=1, nodata=-9999.0, compress="deflate")

with rasterio.open("ket_qua/do_doc.tif", "w", **ho_so) as dich:
    dich.write(do_doc.filled(-9999.0).astype("float32"), 1)
```

Hàm `tinh_do_doc` cần được kiểm thử riêng. Không thay đổi mảng đầu vào trong hàm nếu không ghi rõ.

## Cắt theo vùng

```python
import geopandas as gpd
from rasterio.mask import mask

ranh = gpd.read_file("du_lieu/goc/hanh_chinh.gpkg", layer="tinh")

with rasterio.open("du_lieu/goc/dem.tif") as nguon:
    ranh = ranh.to_crs(nguon.crs)
    mang_cat, bien_doi = mask(
        nguon,
        ranh.geometry,
        crop=True,
        filled=False,
    )
```

Chuyển vector sang CRS raster trước khi cắt. Nếu hai lớp không giao nhau, dừng với thông báo rõ ràng thay vì tạo tệp rỗng.

## Đổi hệ tọa độ

```python
from rasterio.warp import Resampling, calculate_default_transform, reproject

with rasterio.open("du_lieu/goc/dem.tif") as nguon:
    dich_crs = "EPSG:32648"
    bien_doi, rong, cao = calculate_default_transform(
        nguon.crs, dich_crs, nguon.width, nguon.height, *nguon.bounds
    )
    ho_so = nguon.profile.copy()
    ho_so.update(crs=dich_crs, transform=bien_doi, width=rong, height=cao)

    with rasterio.open("ket_qua/dem_utm.tif", "w", **ho_so) as dich:
        reproject(
            source=rasterio.band(nguon, 1),
            destination=rasterio.band(dich, 1),
            src_transform=nguon.transform,
            src_crs=nguon.crs,
            dst_transform=bien_doi,
            dst_crs=dich_crs,
            resampling=Resampling.bilinear,
        )
```

Ảnh phân loại cần `nearest` để không tạo lớp mới. Dữ liệu liên tục có thể dùng `bilinear` hoặc `cubic`, tùy mục tiêu.

## Xử lý theo cửa sổ

Với raster lớn, không đọc toàn bộ vào RAM:

```python
with rasterio.open("du_lieu/goc/anh_lon.tif") as nguon:
    for _, cua_so in nguon.block_windows(1):
        khoi = nguon.read(1, window=cua_so, masked=True)
        # Tính toán và ghi đúng cửa sổ tương ứng.
```

## Kiểm tra đầu ra

- CRS và bounds đúng.
- Kích thước ô hợp lý.
- Min, max và phân bố không bất thường.
- NoData không bị biến thành giá trị thật.
- Hiển thị chồng lớp tại một số vị trí kiểm tra.

## Bài tập

Cắt DEM theo ranh giới nghiên cứu, đổi sang CRS phẳng, tính độ cao trung bình và ghi kết quả dạng GeoTIFF nén.
