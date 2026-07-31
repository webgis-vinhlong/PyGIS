---
thu_tu: 2
dinh_danh: cai-dat-moi-truong
tieu_de: Cài đặt và quản lý môi trường
nhom: Khởi động
tom_tat: Tạo môi trường Python GIS ổn định trên Windows, macOS và Linux, đồng thời tránh xung đột thư viện nhị phân.
---
# Vì sao cần môi trường riêng?

Các thư viện GIS thường phụ thuộc vào GEOS, GDAL và PROJ. Đây là những thành phần nhị phân có quan hệ phiên bản chặt chẽ. Cài tất cả vào Python hệ thống có thể làm công cụ này ảnh hưởng công cụ khác. Mỗi công cụ nên có một môi trường độc lập và tệp mô tả phiên bản.

## Lựa chọn công cụ

| Nhu cầu | Khuyến nghị | Lý do |
|---|---|---|
| Người mới, Windows | Miniforge và Conda | Giải quyết tốt thư viện GIS nhị phân |
| Gói thuần Python | `venv` và `pip` | Có sẵn trong Python, gọn nhẹ |
| Công cụ cần tốc độ | `uv` | Cài và khóa phụ thuộc nhanh |
| PyQGIS | Python đi kèm QGIS | Khớp chính xác thư viện QGIS |

Tài liệu không bắt buộc một công cụ duy nhất. Điều quan trọng là không trộn lẫn `pip` và `conda` tùy tiện trong cùng môi trường.

## Cách 1: Miniforge

Sau khi cài Miniforge, mở thiết bị đầu cuối:

```bash
conda create -n pygis-vn -c conda-forge python=3.12 geopandas rasterio \
  rioxarray xarray dask matplotlib folium osmnx jupyterlab
conda activate pygis-vn
python -c "import geopandas, rasterio; print('Môi trường sẵn sàng')"
```

Kênh `conda-forge` cung cấp bộ gói đồng nhất. Hãy ưu tiên cài các gói chính trong một lệnh để bộ giải phụ thuộc nhìn thấy toàn bộ yêu cầu.

## Cách 2: venv

```bash
python -m venv .venv
```

Kích hoạt trên Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install geopandas rasterio matplotlib jupyterlab
```

Kích hoạt trên Linux hoặc macOS:

```bash
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install geopandas rasterio matplotlib jupyterlab
```

## Kiểm tra có hệ thống

Tạo tệp `kiem_tra.py`:

```python
from importlib.metadata import version

goi_can_thiet = ["geopandas", "shapely", "pyproj", "rasterio"]
for ten_goi in goi_can_thiet:
    print(f"{ten_goi:12} {version(ten_goi)}")
```

Chạy bằng đúng trình thông dịch:

```bash
python kiem_tra.py
python -c "import sys; print(sys.executable)"
```

Nếu đường dẫn không trỏ vào môi trường vừa tạo, bạn đang dùng sai Python.

## Cấu trúc công cụ khuyến nghị

```text
du-an-gis/
├── du_lieu/
│   ├── goc/
│   └── da_xu_ly/
├── notebooks/
├── src/
├── ket_qua/
├── tests/
├── pyproject.toml
└── README.md
```

Không chỉnh sửa trực tiếp dữ liệu gốc. Tất cả sản phẩm trung gian phải có thể tạo lại từ mã.

> [!CẢNH BÁO] Không đưa khóa API, mật khẩu, tệp xác thực hoặc dữ liệu cá nhân lên Git. Dùng biến môi trường và tệp `.env` đã được loại khỏi Git.

## Khắc phục lỗi thường gặp

- `ModuleNotFoundError`: kiểm tra Python và `pip` có cùng môi trường bằng `python -m pip`.
- Lỗi tải GDAL/PROJ: ưu tiên bộ gói từ `conda-forge`, tránh ghép nhiều kênh.
- Notebook không thấy môi trường: cài `ipykernel`, sau đó đăng ký kernel.
- Đường dẫn Windows có dấu cách: dùng `pathlib.Path`, không tự ghép chuỗi bằng dấu gạch chéo.

## Bài tập

1. Tạo môi trường `pygis-vn`.
2. In phiên bản Python, GeoPandas, Shapely, PyProj và Rasterio.
3. Tạo cấu trúc thư mục công cụ và ghi lại lệnh tái tạo môi trường trong README.
