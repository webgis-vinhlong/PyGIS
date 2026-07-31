---
thu_tu: 3
dinh_danh: python-cho-du-lieu-gis
tieu_de: Python, NumPy và Pandas cho GIS
nhom: Nền tảng
tom_tat: Nắm các kiểu dữ liệu, hàm, mảng và bảng cần thiết để viết mã phân tích không gian rõ ràng.
---
# Python theo hướng dữ liệu

Trong GIS, mã tốt thường là một chuỗi biến đổi dữ liệu nhỏ, có tên rõ nghĩa và kiểm tra được. Hãy ưu tiên hàm thuần, `pathlib.Path`, kiểu dữ liệu cụ thể và thao tác vector hóa thay vì vòng lặp không cần thiết.

## Kiểu dữ liệu và hàm

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class TramDo:
    ten: str
    kinh_do: float
    vi_do: float


def nam_trong_viet_nam(tram: TramDo) -> bool:
    return 102.0 <= tram.kinh_do <= 110.0 and 8.0 <= tram.vi_do <= 24.0


tram = TramDo("Trạm trung tâm", 105.97, 10.25)
assert nam_trong_viet_nam(tram)
```

`dataclass` giúp dữ liệu có cấu trúc. `frozen=True` ngăn thay đổi ngoài ý muốn, hữu ích khi một đối tượng được truyền qua nhiều bước xử lý.

## NumPy cho raster

Raster thường được biểu diễn bằng mảng NumPy hai hoặc ba chiều. Giá trị không hợp lệ cần được quản lý rõ ràng.

```python
import numpy as np

band_do = np.array([[0.12, 0.18, 0.20], [0.16, 0.22, np.nan]])
band_can_hong_ngoai = np.array([[0.42, 0.55, 0.61], [0.49, 0.65, np.nan]])

with np.errstate(divide="ignore", invalid="ignore"):
    ndvi = (band_can_hong_ngoai - band_do) / (band_can_hong_ngoai + band_do)

print(np.nanmean(ndvi))
```

Không thay `NaN` bằng 0 nếu 0 có ý nghĩa vật lý. Hãy giữ mặt nạ dữ liệu thiếu cho đến khi quy tắc thay thế được xác định.

## Pandas cho thuộc tính

```python
import pandas as pd

bang = pd.DataFrame(
    {
        "xa": ["A", "A", "B", "B"],
        "nam": [2024, 2025, 2024, 2025],
        "dan_so": [12_500, 12_900, 9_800, 10_100],
    }
)

tong_hop = (
    bang.assign(tang_truong=bang.groupby("xa")["dan_so"].pct_change())
    .groupby("xa", as_index=False)
    .agg(dan_so_moi=("dan_so", "last"), tang_truong=("tang_truong", "last"))
)
```

Chuỗi thao tác trên tránh tạo nhiều biến tạm nhưng vẫn giữ được ý nghĩa. Khi chuỗi dài, tách thành các hàm có tên theo nghiệp vụ.

## Đường dẫn đa nền tảng

```python
from pathlib import Path

thu_muc_goc = Path(__file__).resolve().parents[1]
duong_dan = thu_muc_goc / "du_lieu" / "goc" / "ranh_gioi.gpkg"

if not duong_dan.exists():
    raise FileNotFoundError(f"Thiếu dữ liệu: {duong_dan}")
```

## Nguyên tắc viết mã GIS

- Đặt tên theo ý nghĩa: `dien_tich_km2` tốt hơn `area2`.
- Ghi đơn vị trong tên cột hoặc siêu dữ liệu.
- Kiểm tra điều kiện đầu vào bằng `assert` hoặc ngoại lệ có thông báo.
- Không sửa DataFrame dùng chung nếu chưa chủ động sao chép.
- Tách đọc dữ liệu, phân tích và xuất kết quả thành các hàm riêng.

## Bài tập

1. Tạo bảng lượng mưa theo huyện và tháng, sau đó tính trung bình theo huyện.
2. Viết hàm nhận hai mảng raster và trả về NDVI, giữ nguyên `NaN`.
3. Viết kiểm thử cho trường hợp hai band có kích thước khác nhau.
