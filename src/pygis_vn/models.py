"""Các mô hình dữ liệu của giáo trình."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Chuong:
    """Một chương đã được đọc từ tệp Markdown."""

    thu_tu: int
    duong_dan: Path
    dinh_danh: str
    tieu_de: str
    nhom: str
    tom_tat: str
    noi_dung: str

    @property
    def ten_tap_tin_html(self) -> str:
        return f"{self.dinh_danh}.html"

    @property
    def so_phut_doc(self) -> int:
        so_tu = len(self.noi_dung.split())
        return max(1, round(so_tu / 220))
