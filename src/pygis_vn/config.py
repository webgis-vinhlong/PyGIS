"""Cấu hình tập trung cho website."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class CauHinh:
    """Mô tả một lần dựng website."""

    thu_muc_noi_dung: Path
    thu_muc_dich: Path
    dia_chi_goc: str = ""
    tieu_de: str = "Python GIS Việt Nam"
    mo_ta: str = "Tài liệu mở về phân tích dữ liệu không gian với Python"
    tac_gia: str = "Long Ngo"
    kho_ma_nguon: str = "https://github.com/webgis-vinhlong/PyGIS"

    @property
    def dia_chi_chuan_hoa(self) -> str:
        return self.dia_chi_goc.rstrip("/")
