---
thu_tu: 12
dinh_danh: truc-quan-hoa-ban-do
tieu_de: Trực quan hóa và bản đồ tương tác
nhom: Trình bày
tom_tat: Thiết kế bản đồ tĩnh và tương tác có phân cấp thị giác, chú giải đúng và khả năng tiếp cận tốt.
---
# Bản đồ là một lập luận bằng hình

Màu sắc, phân lớp và tỷ lệ có thể thay đổi cách người đọc diễn giải. Hãy bắt đầu từ thông điệp, đối tượng đọc và mức độ bất định thay vì chọn bảng màu trước.

## Bản đồ tĩnh với Matplotlib

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(9, 8), constrained_layout=True)
xa.plot(
    column="ty_le_ngap",
    scheme="quantiles",
    k=5,
    cmap="Blues",
    linewidth=0.35,
    edgecolor="#43515c",
    legend=True,
    missing_kwds={"color": "#d9d9d9", "label": "Thiếu dữ liệu"},
    ax=ax,
)
ax.set_title("Tỷ lệ diện tích ngập theo xã", loc="left", weight="bold")
ax.set_axis_off()
fig.savefig("ket_qua/ty_le_ngap.png", dpi=200, bbox_inches="tight")
```

Phân vị tạo số đối tượng gần bằng nhau trong mỗi lớp nhưng khoảng giá trị có thể khó so sánh giữa nhiều bản đồ. Khoảng đều phù hợp khi miền giá trị có ý nghĩa ổn định. Natural Breaks mô tả cấu trúc dữ liệu nhưng khó đối chiếu giữa các thời điểm.

## Bản đồ tương tác với Folium

```python
import folium

ban_do = folium.Map(
    location=[10.25, 105.97],
    zoom_start=10,
    tiles="CartoDB positron",
)

folium.GeoJson(
    xa.to_crs(4326),
    tooltip=folium.GeoJsonTooltip(fields=["ten_xa", "ty_le_ngap"]),
    name="Tỷ lệ ngập",
).add_to(ban_do)

folium.LayerControl(collapsed=False).add_to(ban_do)
ban_do.save("ket_qua/ban_do_ngap.html")
```

Không đưa thuộc tính nhạy cảm vào GeoJSON phía trình duyệt. Người dùng có thể tải dữ liệu dù trường đó không hiện trong popup.

## Khả năng tiếp cận

- Dùng bảng màu có độ sáng thay đổi rõ và thân thiện với người mù màu.
- Không dùng chỉ màu sắc để phân biệt; bổ sung ký hiệu hoặc nhãn.
- Chú giải có đơn vị, khoảng lớp không chồng lấn.
- Văn bản thay thế mô tả thông điệp chính của bản đồ.
- Giữ độ tương phản đủ cao và kích thước chữ phù hợp.

## Thành phần bắt buộc

Bản đồ phân tích cần tiêu đề, chú giải, đơn vị, nguồn dữ liệu, thời điểm, hệ quy chiếu khi liên quan và ghi chú phương pháp. Mũi tên Bắc và thước tỷ lệ chỉ thêm khi hữu ích, không phải trang trí mặc định.

## Bài tập

Tạo hai bản đồ cùng dữ liệu bằng phân vị và khoảng đều. So sánh thông điệp thị giác, sau đó chọn một cách và biện minh bằng ba câu.
