# Hướng dẫn đóng góp

Cảm ơn bạn muốn cải thiện Python GIS Việt Nam.

## Nguyên tắc

- Nội dung giải thích và giao diện phải bằng tiếng Việt rõ ràng.
- Tên thư viện, hàm, lớp và từ khóa Python được giữ theo tài liệu chính thức.
- Không sao chép nội dung có bản quyền hoặc đổi giấy phép của công cụ khác.
- Ví dụ dùng dữ liệu giả lập hoặc dữ liệu mở, không chứa thông tin cá nhân.
- Phát biểu phụ thuộc phiên bản phải có liên kết tài liệu chính thức.
- Mọi thay đổi phải dựng được website và vượt qua kiểm thử.

## Quy trình

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[kiem-thu]"
ruff check .
pytest
pygis-vn dung
pygis-vn xem
```

Trên Windows, kích hoạt bằng `.\.venv\Scripts\Activate.ps1`.

Tạo nhánh ngắn gọn, commit có mục đích và mở pull request mô tả:

1. Vấn đề cần giải quyết.
2. Thay đổi đã thực hiện.
3. Cách kiểm tra.
4. Ảnh chụp nếu giao diện thay đổi.

## Sửa nội dung

Mỗi chương nằm trong `noi_dung/` và có khối siêu dữ liệu ở đầu tệp. `thu_tu` và `dinh_danh` không được trùng. Chạy kiểm thử sau khi thêm chương.

## Báo lỗi

Vui lòng cung cấp hệ điều hành, phiên bản Python, lệnh đã chạy, thông báo lỗi đầy đủ và ví dụ nhỏ có thể tái hiện. Xóa token, đường dẫn riêng tư và dữ liệu nhạy cảm trước khi đăng.
