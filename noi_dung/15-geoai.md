---
thu_tu: 15
dinh_danh: geoai-hoc-may-khong-gian
tieu_de: GeoAI và học máy không gian
nhom: Nâng cao
tom_tat: Thiết kế mẫu, đặc trưng và đánh giá mô hình không gian mà không rò rỉ vị trí giữa tập huấn luyện và kiểm tra.
---
# Vì sao chia ngẫu nhiên có thể sai?

Các điểm gần nhau thường giống nhau. Nếu chia ngẫu nhiên từng điểm, tập kiểm tra có thể nằm sát tập huấn luyện và làm điểm số lạc quan. Đánh giá không gian cần giữ lại các vùng, thời điểm hoặc cảnh ảnh độc lập.

## Quy trình chuẩn

1. Xác định biến đích và đơn vị dự đoán.
2. Chọn dữ liệu tham chiếu có chất lượng.
3. Tạo đặc trưng mà không dùng thông tin tương lai.
4. Chia tập theo khối không gian hoặc vùng hành chính.
5. Huấn luyện đường cơ sở đơn giản.
6. Đánh giá theo lớp, vùng và độ bất định.
7. Kiểm tra thực địa hoặc nguồn độc lập.

## Chia theo nhóm không gian

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import GroupKFold, cross_val_predict

cot_dac_trung = ["band_do", "band_xanh", "band_nir", "ndvi", "do_cao"]
X = mau[cot_dac_trung]
y = mau["lop_phu"]
nhom = mau["ma_o_khong_gian"]

bo_chia = GroupKFold(n_splits=5)
mo_hinh = RandomForestClassifier(
    n_estimators=300,
    min_samples_leaf=3,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1,
)

du_doan = cross_val_predict(mo_hinh, X, y, groups=nhom, cv=bo_chia)
print(classification_report(y, du_doan))
```

`ma_o_khong_gian` có thể được tạo từ lưới đủ lớn để giảm tương quan giữa các fold. Kích thước ô phải dựa vào hiện tượng và phạm vi tự tương quan.

## Học sâu ảnh vệ tinh

TorchGeo hỗ trợ dataset, sampler và mô hình cho dữ liệu địa không gian. Khi cắt ảnh thành patch:

- Không để patch chồng lấn rơi vào hai tập khác nhau.
- Giữ CRS và phép biến đổi để đưa dự đoán về bản đồ.
- Cân bằng lớp nhưng không bóp méo phân bố đánh giá.
- Ghi phiên bản ảnh, nhãn, mô hình và trọng số.
- Kiểm tra đường nối giữa các tile.

## Chỉ số đánh giá

Độ chính xác tổng thể có thể che giấu lớp hiếm. Báo cáo precision, recall, F1 theo lớp, ma trận nhầm lẫn và chỉ số theo từng vùng. Với phân đoạn, dùng IoU hoặc Dice và đánh giá biên nếu biên quan trọng.

## Đạo đức và giới hạn

Mô hình vị trí có thể ảnh hưởng cộng đồng, tài sản hoặc phân bổ nguồn lực. Không công bố tọa độ nhạy cảm. Nêu vùng mô hình chưa được kiểm chứng, sai số nhóm và điều kiện không nên sử dụng.

## Bài tập

So sánh chia ngẫu nhiên với chia theo khối không gian trên cùng dữ liệu. Nếu điểm số giảm, giải thích vì sao kết quả thấp hơn có thể trung thực hơn.
