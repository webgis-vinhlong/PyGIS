"""Ví dụ độc lập: thống kê số điểm và diện tích theo vùng."""

from __future__ import annotations

import geopandas as gpd
from shapely import Point, box


def tao_du_lieu() -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
    """Tạo dữ liệu giả lập trong CRS có đơn vị mét."""

    vung = gpd.GeoDataFrame(
        {
            "ma_vung": ["A", "B"],
            "geometry": [box(0, 0, 1_000, 1_000), box(1_000, 0, 2_000, 1_000)],
        },
        crs="EPSG:32648",
    )
    diem = gpd.GeoDataFrame(
        {
            "ma_diem": ["D1", "D2", "D3"],
            "geometry": [Point(250, 400), Point(1_250, 600), Point(1_800, 300)],
        },
        crs=vung.crs,
    )
    return vung, diem


def thong_ke() -> gpd.GeoDataFrame:
    """Ghép điểm vào vùng và tính số điểm trên mỗi km²."""

    vung, diem = tao_du_lieu()
    da_ghep = gpd.sjoin(diem, vung[["ma_vung", "geometry"]], predicate="within")
    so_diem = da_ghep.groupby("ma_vung").size().rename("so_diem")
    ket_qua = vung.join(so_diem, on="ma_vung").fillna({"so_diem": 0})
    ket_qua["dien_tich_km2"] = ket_qua.area / 1_000_000
    ket_qua["mat_do"] = ket_qua["so_diem"] / ket_qua["dien_tich_km2"]
    return ket_qua


if __name__ == "__main__":
    print(thong_ke()[["ma_vung", "so_diem", "dien_tich_km2", "mat_do"]])
