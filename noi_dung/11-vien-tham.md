---
thu_tu: 11
dinh_danh: vien-tham-va-stac
tieu_de: Viễn thám, chỉ số phổ và STAC
nhom: Viễn thám
tom_tat: Xây dựng quy trình ảnh vệ tinh từ tìm kiếm danh mục, lọc mây đến chỉ số phổ và tổng hợp theo thời gian.
---
# Quy trình viễn thám có thể tái lập

Một ảnh vệ tinh cần được hiểu qua cảm biến, mức xử lý, đơn vị phản xạ, độ phân giải từng band, mặt nạ chất lượng và thời điểm. Không áp dụng cùng công thức hoặc ngưỡng cho mọi sản phẩm mà chưa đọc tài liệu.

## Tìm dữ liệu bằng STAC

STAC chuẩn hóa cách mô tả tài sản không gian-thời gian. Ví dụ với `pystac-client`:

```python
from pystac_client import Client

danh_muc = Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")
tim_kiem = danh_muc.search(
    collections=["sentinel-2-l2a"],
    bbox=[105.8, 10.1, 106.2, 10.5],
    datetime="2025-01-01/2025-03-31",
    query={"eo:cloud_cover": {"lt": 20}},
)

cac_anh = list(tim_kiem.items())
print(f"Tìm thấy {len(cac_anh)} cảnh")
```

Một số danh mục yêu cầu ký URL hoặc xác thực. Cơ chế truy cập có thể thay đổi; luôn tham khảo tài liệu chính thức của nhà cung cấp.

## NDVI có mặt nạ

```python
import numpy as np

def tinh_ndvi(band_do: np.ndarray, band_nir: np.ndarray) -> np.ndarray:
    do = band_do.astype("float32")
    nir = band_nir.astype("float32")
    mau = nir + do
    return np.divide(
        nir - do,
        mau,
        out=np.full_like(nir, np.nan),
        where=mau != 0,
    )
```

Cần áp dụng hệ số tỷ lệ của sản phẩm trước khi tính nếu dữ liệu lưu dạng số nguyên. Mây, bóng mây, tuyết và pixel bão hòa phải bị loại bằng band chất lượng phù hợp.

## Tổng hợp theo thời gian

Trung vị theo mùa thường giảm ảnh hưởng mây sót và ngoại lai:

```python
anh_sach = ndvi.where(mat_na_chat_luong)
hop_anh = anh_sach.median(dim="time", skipna=True)
so_quan_sat = anh_sach.notnull().sum(dim="time")
```

Luôn xuất thêm `so_quan_sat`. Một giá trị tổng hợp từ một quan sát không có độ tin cậy tương đương giá trị từ mười quan sát.

## Kiểm tra khoa học

- Giá trị chỉ số nằm trong miền kỳ vọng.
- Band đã được đưa về cùng độ phân giải và lưới.
- Mặt nạ chất lượng đúng với phiên bản sản phẩm.
- Thời gian tổng hợp phù hợp mùa vụ.
- Có điểm hoặc vùng kiểm chứng độc lập.
- Kết luận không vượt quá khả năng phân giải của cảm biến.

## Bài tập

Thiết kế quy trình theo dõi thảm thực vật gồm truy vấn STAC, lọc mây, NDVI, hợp ảnh tháng và số quan sát. Ghi rõ mọi tham số cần lưu để chạy lại sau một năm.
