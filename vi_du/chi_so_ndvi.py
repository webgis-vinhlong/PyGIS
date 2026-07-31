"""Ví dụ độc lập: tính NDVI an toàn với NumPy."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def tinh_ndvi(
    band_do: NDArray[np.number],
    band_can_hong_ngoai: NDArray[np.number],
) -> NDArray[np.float32]:
    """Tính NDVI, trả NaN khi mẫu số bằng 0 hoặc đầu vào không hợp lệ."""

    if band_do.shape != band_can_hong_ngoai.shape:
        raise ValueError("Hai band phải có cùng kích thước")
    do = band_do.astype("float32")
    nir = band_can_hong_ngoai.astype("float32")
    mau = nir + do
    hop_le = np.isfinite(do) & np.isfinite(nir) & (mau != 0)
    return np.divide(
        nir - do,
        mau,
        out=np.full(do.shape, np.nan, dtype="float32"),
        where=hop_le,
    )


if __name__ == "__main__":
    do = np.array([[1_200, 1_500], [0, np.nan]])
    nir = np.array([[4_800, 5_500], [0, np.nan]])
    print(tinh_ndvi(do, nir))
