---
thu_tu: 16
dinh_danh: xuat-ban-webgis
tieu_de: Xuất bản WebGIS từ Python
nhom: Nâng cao
tom_tat: Chọn kiến trúc tĩnh, dịch vụ API hoặc vector tile và tối ưu dữ liệu trước khi đưa lên web.
---
# Chọn kiến trúc theo quy mô

| Quy mô | Kiến trúc | Công cụ Python gợi ý |
|---|---|---|
| Bản đồ nhỏ, ít cập nhật | HTML tĩnh | Folium, GeoPandas |
| Bảng điều khiển phân tích | Ứng dụng Python | Panel, Dash, Streamlit |
| API không gian | Dịch vụ web | FastAPI, GeoAlchemy2 |
| Dữ liệu vector lớn | Tile | Tippecanoe hoặc PMTiles trong quy trình |
| Raster lớn | COG và tile động | TiTiler, Rasterio |

Website giáo trình này dùng trình dựng Python và HTML tĩnh vì nội dung ít thay đổi theo người dùng, chi phí lưu trữ thấp và có thể phục vụ bằng GitHub Pages.

## API tối giản

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from shapely import Point

ung_dung = FastAPI(title="Dịch vụ GIS")


class ToaDo(BaseModel):
    kinh_do: float = Field(ge=-180, le=180)
    vi_do: float = Field(ge=-90, le=90)


@ung_dung.post("/kiem-tra")
def kiem_tra(diem: ToaDo) -> dict[str, object]:
    hinh_hoc = Point(diem.kinh_do, diem.vi_do)
    if hinh_hoc.is_empty:
        raise HTTPException(400, "Tọa độ không hợp lệ")
    return {"hop_le": True, "wkt": hinh_hoc.wkt}
```

API thật cần giới hạn kích thước hình học, xác thực, nhật ký, bộ nhớ đệm và truy vấn cơ sở dữ liệu có tham số.

## Tối ưu vector

- Chỉ giữ trường cần hiển thị.
- Làm tròn số theo độ chính xác hợp lý.
- Đơn giản hóa hình học theo mức thu phóng, giữ topology khi cần.
- Dùng GeoJSON cho nhỏ; vector tile hoặc PMTiles cho lớn.
- Không gửi dữ liệu nhạy cảm đến trình duyệt.

## Tối ưu raster

- Chuyển sang COG có tile nội bộ và overview.
- Chọn nén theo kiểu dữ liệu.
- Dùng NoData nhất quán.
- Đọc theo bounds, mức thu phóng và band cần thiết.
- Đưa sản phẩm tĩnh lên lưu trữ đối tượng; dùng tile động khi cần phối màu hoặc tính toán theo yêu cầu.

## An toàn

Hình học do người dùng gửi có thể cực lớn hoặc không hợp lệ. Cần giới hạn số đỉnh, diện tích vùng truy vấn, thời gian xử lý và định dạng đầu ra. Không ghép trực tiếp chuỗi người dùng vào SQL.

## Bài tập

Xuất một lớp GeoPandas thành bản đồ HTML. So sánh kích thước trước và sau khi bỏ trường không cần thiết, sau đó kiểm tra trang trên màn hình nhỏ.
