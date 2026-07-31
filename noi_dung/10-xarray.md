---
thu_tu: 10
dinh_danh: xarray-rioxarray-dask
tieu_de: Xarray, Rioxarray, Dask và Zarr
nhom: Raster
tom_tat: Phân tích chuỗi thời gian raster có nhãn và mở rộng xử lý theo khối cho dữ liệu lớn.
---
# Mảng có nhãn

NumPy quản lý mảng hiệu quả nhưng không tự biết chiều nào là thời gian, band, x hay y. Xarray gắn tên, tọa độ và thuộc tính cho từng chiều; Rioxarray bổ sung CRS và phép biến đổi không gian.

## Mở nhiều raster

```python
from pathlib import Path
import xarray as xr
import rioxarray

cac_tap_tin = sorted(Path("du_lieu/goc/ndvi").glob("*.tif"))
cac_lop = [
    rioxarray.open_rasterio(duong_dan, masked=True).squeeze("band", drop=True)
    for duong_dan in cac_tap_tin
]

ndvi = xr.concat(cac_lop, dim="time")
ndvi = ndvi.assign_coords(time=[duong_dan.stem for duong_dan in cac_tap_tin])
```

Trong dự án thật, hãy phân tích ngày tháng từ tên tệp thành `datetime64`, không giữ dạng chuỗi.

## Tính toán theo chiều

```python
trung_binh = ndvi.mean(dim="time", skipna=True)
phan_vi_10 = ndvi.quantile(0.1, dim="time", skipna=True)
bat_thuong = ndvi - ndvi.mean(dim="time")
```

Xarray tự căn theo nhãn tọa độ. Nếu các raster không cùng lưới, việc concat có thể tạo dữ liệu thiếu hoặc mở rộng lưới. Cần chuẩn hóa CRS, bounds, kích thước ô và điểm neo trước.

## Xử lý lười với Dask

```python
du_lieu = xr.open_zarr(
    "du_lieu/goc/khi_hau.zarr",
    chunks={"time": 12, "y": 1024, "x": 1024},
)
trung_binh_nam = du_lieu["mua"].resample(time="YS").sum().mean("time")
ket_qua = trung_binh_nam.compute()
```

Dask dựng đồ thị tác vụ và chỉ tính khi gọi `compute`. Kích thước chunk ảnh hưởng mạnh đến bộ nhớ và chi phí lập lịch.

## Ghi Zarr

```python
ndvi.to_dataset(name="ndvi").chunk(
    {"time": 12, "y": 1024, "x": 1024}
).to_zarr("du_lieu/da_xu_ly/ndvi.zarr", mode="w")
```

Zarr phù hợp cho mảng đám mây và truy cập song song. Với sản phẩm cuối là một raster, Cloud Optimized GeoTIFF có thể đơn giản hơn.

## Nguyên tắc dữ liệu lớn

- Lọc theo thời gian, vùng và band càng sớm càng tốt.
- Đọc siêu dữ liệu trước khi đọc pixel.
- Chọn chunk theo kiểu truy vấn thường gặp.
- Tránh gọi `compute()` nhiều lần trên cùng đồ thị.
- Ghi sản phẩm trung gian đắt đỏ nếu sẽ tái sử dụng.
- Đo hiệu năng trên mẫu đại diện, không suy đoán.

## Bài tập

Tạo chuỗi 12 raster giả lập, gắn thời gian hàng tháng, tính trung bình năm và tháng có giá trị cực đại cho mỗi ô.
