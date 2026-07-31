"""Giao diện dòng lệnh tiếng Việt."""

from __future__ import annotations

import argparse
import http.server
import socketserver
from functools import partial
from pathlib import Path

from pygis_vn.config import CauHinh
from pygis_vn.render import dung_website


def _bo_phan_tich() -> argparse.ArgumentParser:
    bo = argparse.ArgumentParser(
        prog="pygis-vn",
        description="Dựng và xem trước giáo trình Phân tích GIS với Python.",
    )
    lenh = bo.add_subparsers(dest="lenh", required=True)
    dung = lenh.add_parser("dung", help="Dựng website HTML tĩnh")
    dung.add_argument("--noi-dung", type=Path, default=Path("noi_dung"))
    dung.add_argument("--dich", type=Path, default=Path("site"))
    dung.add_argument("--dia-chi-goc", default="")

    xem = lenh.add_parser("xem", help="Mở máy chủ xem trước cục bộ")
    xem.add_argument("--thu-muc", type=Path, default=Path("site"))
    xem.add_argument("--cong", type=int, default=8000)
    return bo


def main() -> int:
    tham_so = _bo_phan_tich().parse_args()
    if tham_so.lenh == "dung":
        cau_hinh = CauHinh(
            thu_muc_noi_dung=tham_so.noi_dung,
            thu_muc_dich=tham_so.dich,
            dia_chi_goc=tham_so.dia_chi_goc,
        )
        cac_tap_tin = dung_website(cau_hinh)
        print(f"Đã dựng {len(cac_tap_tin)} tệp vào {tham_so.dich.resolve()}")
        return 0

    thu_muc = tham_so.thu_muc.resolve()
    if not (thu_muc / "index.html").exists():
        raise SystemExit("Chưa có site/index.html. Hãy chạy: pygis-vn dung")
    xu_ly = partial(http.server.SimpleHTTPRequestHandler, directory=str(thu_muc))
    with socketserver.TCPServer(("", tham_so.cong), xu_ly) as may_chu:
        print(f"Đang phục vụ {thu_muc} tại http://localhost:{tham_so.cong}")
        try:
            may_chu.serve_forever()
        except KeyboardInterrupt:
            print("\nĐã dừng máy chủ.")
    return 0
