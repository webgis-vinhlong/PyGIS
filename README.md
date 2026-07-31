<div align="center">

# 🗺️ Python GIS Việt Nam

### Giáo trình mở về phân tích dữ liệu không gian bằng Python

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Giấy phép MIT](https://img.shields.io/badge/Giấy%20phép-MIT-0B7A53)](LICENSE)
[![Kiểm tra chất lượng](https://github.com/webgis-vinhlong/PyGIS/actions/workflows/quality.yml/badge.svg)](https://github.com/webgis-vinhlong/PyGIS/actions/workflows/quality.yml)
[![Triển khai website](https://github.com/webgis-vinhlong/PyGIS/actions/workflows/pages.yml/badge.svg)](https://github.com/webgis-vinhlong/PyGIS/actions/workflows/pages.yml)

**20 chương · 70 thư viện · Python thuần · 100% nội dung tiếng Việt**

[🌐 Mở website](https://webgis-vinhlong.github.io/PyGIS/) ·
[🚀 Bắt đầu trong 5 phút](#-chạy-trong-5-phút) ·
[🤝 Đóng góp](CONTRIBUTING.md)

</div>

---

## 🌱 Giới thiệu

Python GIS Việt Nam là website học tập mã nguồn mở dành cho sinh viên, chuyên viên GIS, nhà nghiên cứu và lập trình viên muốn xây dựng quy trình phân tích không gian có thể tái lập.

Dự án được viết lại theo kiến trúc **trình dựng website bằng Python thuần**:

- Không dùng Node, JavaScript hay trình dựng giao diện bên ngoài.
- Bộ chuyển Markdown, kết xuất HTML, mục lục, điều hướng, SEO và máy chủ xem trước đều viết bằng thư viện chuẩn Python.
- Xuất website HTML tĩnh, chạy được ngoại tuyến và triển khai miễn phí trên GitHub Pages.
- Nội dung, giao diện và hướng dẫn đều bằng tiếng Việt; từ khóa Python và tên thư viện giữ nguyên theo chuẩn kỹ thuật.
- Mã nguồn và nội dung do dự án biên soạn phát hành theo MIT.

> Tên hiển thị của dự án là **Python GIS Việt Nam**. Dự án độc lập, dùng biểu tượng riêng, không liên kết và không được chứng thực bởi pygis.io hoặc các dự án được dẫn nguồn.

## ✨ Điểm nổi bật

| Thành phần | Nội dung |
|---|---|
| 🐍 Python thuần | Trình dựng tĩnh không có phụ thuộc chạy bắt buộc |
| 🧭 Lộ trình đầy đủ | Nền tảng → vector → raster → viễn thám → PyQGIS → GeoAI |
| 🧪 Có kiểm thử | Pytest kiểm tra nội dung, HTML, an toàn và cấu trúc |
| 📱 Giao diện đáp ứng | Tối ưu máy tính, máy tính bảng, điện thoại và bản in |
| ♿ Khả năng tiếp cận | HTML ngữ nghĩa, bỏ qua điều hướng, độ tương phản và chế độ tối |
| 🔎 Tra cứu nhanh | Chỉ mục chương, mục lục từng trang và liên kết tiêu đề |
| 🚢 Tự động triển khai | GitHub Actions dựng và phát hành GitHub Pages |
| 🇻🇳 Bối cảnh Việt Nam | Ví dụ, bài tập và dự án tổng hợp tại Vĩnh Long |

## 🧭 Lộ trình 20 chương

| Phần | Chương |
|---|---|
| Khởi động | Bắt đầu, cài đặt môi trường |
| Nền tảng | Python dữ liệu, mô hình không gian, CRS và PyProj |
| Vector | Shapely, GeoPandas, quy trình phân tích |
| Raster | Rasterio, Xarray, Rioxarray, Dask, Zarr |
| Viễn thám | STAC, chỉ số phổ, tổng hợp ảnh |
| Trình bày | Matplotlib, Folium và nguyên tắc bản đồ |
| Ứng dụng | PyQGIS 3.44, OSM, Earth Engine, nền tảng đám mây |
| Nâng cao | GeoAI, WebGIS, kiểm thử và khả năng tái lập |
| Dự án | Phân tích khả năng tiếp cận dịch vụ công tại Vĩnh Long |
| Tra cứu | Danh mục 70 thư viện và tài liệu chính thống |

## 🚀 Chạy trong 5 phút

Yêu cầu: Python 3.10 trở lên.

```bash
git clone https://github.com/webgis-vinhlong/PyGIS.git
cd PyGIS
python -m venv .venv
```

Kích hoạt trên Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
pygis-vn dung --dia-chi-goc http://localhost:8000
pygis-vn xem
```

Kích hoạt trên Linux hoặc macOS:

```bash
source .venv/bin/activate
python -m pip install -e .
pygis-vn dung --dia-chi-goc http://localhost:8000
pygis-vn xem
```

Mở `http://localhost:8000`. Website đã dựng nằm trong thư mục `site/`.

Không muốn cài gói? Chạy trực tiếp:

```bash
PYTHONPATH=src python -m pygis_vn dung
PYTHONPATH=src python -m pygis_vn xem
```

## 🏗️ Kiến trúc

```text
PyGIS/
├── src/pygis_vn/          # Trình dựng website bằng Python
│   ├── content.py         # Đọc và kiểm tra nội dung
│   ├── markdown.py        # Bộ chuyển Markdown an toàn
│   ├── render.py          # Kết xuất trang, SEO, điều hướng
│   ├── assets.py          # CSS và SVG được sinh từ Python
│   └── cli.py             # Lệnh dựng và xem trước
├── noi_dung/              # 20 chương tiếng Việt
├── vi_du/                 # Tập lệnh GIS độc lập
├── tests/                 # Kiểm thử
├── site/                  # HTML đã xuất
└── .github/workflows/     # Chất lượng và GitHub Pages
```

Luồng dựng:

```mermaid
flowchart LR
    A["Nội dung Markdown"] --> B["Kiểm tra siêu dữ liệu"]
    B --> C["Bộ chuyển Python"]
    C --> D["HTML tĩnh + CSS"]
    D --> E["Kiểm thử"]
    E --> F["GitHub Pages"]
```

## 🧪 Kiểm tra chất lượng

```bash
python -m pip install -e ".[kiem-thu]"
ruff check .
pytest
pygis-vn dung --dia-chi-goc https://webgis-vinhlong.github.io/PyGIS
```

Biên dịch toàn bộ tệp Python:

```bash
python -m compileall -q src vi_du tests
```

## ✍️ Viết chương mới

Tạo tệp trong `noi_dung/`:

```markdown
---
thu_tu: 21
dinh_danh: chu-de-moi
tieu_de: Chủ đề mới
nhom: Nâng cao
tom_tat: Một câu mô tả rõ nội dung chương.
---
# Mục tiêu

Nội dung bằng tiếng Việt...
```

Trình dựng hỗ trợ tiêu đề, đoạn văn, danh sách, bảng, khối mã, liên kết và hộp `MẸO`, `GHI CHÚ`, `CẢNH BÁO`.

## 📚 Nguồn tham khảo

Giáo trình được biên soạn mới và đối chiếu với:

- [Tài liệu PyQGIS 3.44](https://docs.qgis.org/3.44/en/docs/pyqgis_developer_cookbook/)
- [Python GIS Book](https://pythongis.org/)
- [PyGIS Open Source Spatial Programming](https://pygis.io/docs/a_intro.html)
- [Open Geospatial Solutions](https://github.com/opengeos/pygis)
- [PNNL Python GIS Utilities](https://gcims.pnnl.gov/modeling/pygis-python-gis-utilities)

Tên, logo, mã và tài liệu của bên thứ ba tuân theo giấy phép riêng. Xem chương **Tài liệu tham khảo và ghi công** trên website.

## 🛡️ Giới hạn sử dụng

Ví dụ chỉ phục vụ học tập. Phân tích hành chính, đo đạc, quy hoạch, thiên tai hoặc quyết định ảnh hưởng con người phải dùng dữ liệu chính thống, hệ quy chiếu phù hợp, kiểm chứng chuyên môn và tuân thủ pháp luật.

## 📄 Giấy phép và tác giả

Phát triển bởi **Long Ngo** và cộng đồng.

Phát hành theo [Giấy phép MIT](LICENSE). Bản diễn giải tiếng Việt không chính thức có tại [GIAY_PHEP_VI.md](GIAY_PHEP_VI.md).

---

<div align="center">

Được xây dựng với 🐍 Python và tình yêu dành cho dữ liệu không gian Việt Nam.

</div>
