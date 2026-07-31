---
thu_tu: 17
dinh_danh: kiem-thu-va-tai-lap
tieu_de: Kiểm thử, hiệu năng và khả năng tái lập
nhom: Nâng cao
tom_tat: Biến notebook thử nghiệm thành quy trình đáng tin cậy bằng kiểm thử, nhật ký, siêu dữ liệu và CI.
---
# Kết quả đáng tin cậy

Một quy trình tái lập phải biết mã nào, dữ liệu nào, tham số nào và môi trường nào đã tạo ra sản phẩm. Notebook hữu ích để khám phá nhưng phần xử lý ổn định nên chuyển thành hàm, gói hoặc dòng lệnh.

## Kiểm thử hình học

```python
import geopandas as gpd
from shapely import box


def cat_theo_khung(lop: gpd.GeoDataFrame, bounds: tuple[float, ...]):
    if lop.crs is None:
        raise ValueError("Lớp chưa có CRS")
    return lop.clip(box(*bounds))


def test_cat_theo_khung_giu_crs():
    lop = gpd.GeoDataFrame(
        {"ma": [1], "geometry": [box(0, 0, 10, 10)]},
        crs="EPSG:3857",
    )
    ket_qua = cat_theo_khung(lop, (0, 0, 5, 5))
    assert ket_qua.crs == lop.crs
    assert ket_qua.area.iloc[0] == 25
```

Test dữ liệu không gian nên kiểm tra CRS, bounds, kiểu hình học, số đối tượng, dung sai số và thuộc tính.

## Ghi nhật ký

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
nhat_ky = logging.getLogger(__name__)
nhat_ky.info("Bắt đầu xử lý %s đối tượng", len(lop))
```

Không dùng `print` cho quy trình dài. Nhật ký cần đủ để biết bước lỗi nhưng không chứa token hoặc dữ liệu cá nhân.

## Đo trước khi tối ưu

Các hướng cải thiện thường hiệu quả:

- Đọc đúng cột và vùng cần thiết.
- Dùng chỉ mục không gian.
- Dùng thao tác vector hóa.
- Chia raster theo block gốc.
- Chuyển định dạng phù hợp như GeoParquet, COG hoặc Zarr.
- Tránh chuyển CRS lặp lại.

Đừng thêm Dask hoặc xử lý song song nếu nút thắt là đọc mạng, hình học không hợp lệ hoặc thuật toán bậc hai.

## Hồ sơ sản phẩm

Mỗi sản phẩm quan trọng nên có:

- Thời điểm tạo.
- Phiên bản mã hoặc commit.
- Nguồn và phiên bản dữ liệu.
- Tham số.
- CRS, đơn vị và phạm vi.
- Tổng kiểm tệp.
- Kiểm tra chất lượng đã chạy.
- Người chịu trách nhiệm.

## Tích hợp liên tục

CI của repository này cài gói, chạy `ruff`, `pytest` và dựng toàn bộ HTML. Nhờ vậy một liên kết nội bộ, tệp nội dung hoặc cú pháp Python hỏng sẽ được phát hiện trước khi triển khai.

## Bài tập

Chọn một hàm GIS đã viết, thêm ít nhất ba kiểm thử: đầu vào hợp lệ, CRS bị thiếu và hình học rỗng. Ghi thời gian chạy trên 1.000 và 10.000 đối tượng.
