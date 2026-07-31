"""Ví dụ chạy trong QGIS: tạo vùng đệm bằng Processing."""

from __future__ import annotations

import processing
from qgis.core import QgsProcessingFeedback, QgsVectorLayer


def tao_vung_dem(
    duong_dan_dau_vao: str,
    duong_dan_dau_ra: str,
    khoang_cach_m: float = 500,
) -> str:
    """Tạo vùng đệm hợp nhất; lớp đầu vào phải dùng CRS có đơn vị mét."""

    lop = QgsVectorLayer(duong_dan_dau_vao, "Đầu vào", "ogr")
    if not lop.isValid():
        raise ValueError(f"Không thể mở lớp: {duong_dan_dau_vao}")
    if lop.crs().isGeographic():
        raise ValueError("Hãy chuyển lớp sang CRS phẳng trước khi tạo vùng đệm")

    ket_qua = processing.run(
        "native:buffer",
        {
            "INPUT": lop,
            "DISTANCE": khoang_cach_m,
            "SEGMENTS": 12,
            "DISSOLVE": True,
            "END_CAP_STYLE": 0,
            "JOIN_STYLE": 0,
            "MITER_LIMIT": 2,
            "OUTPUT": duong_dan_dau_ra,
        },
        feedback=QgsProcessingFeedback(),
    )
    return str(ket_qua["OUTPUT"])
