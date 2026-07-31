"""Kết xuất website tĩnh từ nội dung đã kiểm tra."""

from __future__ import annotations

import html
import shutil
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

from pygis_vn.assets import BAN_DO_SVG, CSS, LOGO_SVG
from pygis_vn.config import CauHinh
from pygis_vn.content import doc_cac_chuong
from pygis_vn.markdown import chuyen_markdown
from pygis_vn.models import Chuong


def _dau_trang(cau_hinh: CauHinh, tien_to: str = "") -> str:
    return f"""<a class="bo-qua" href="#noi-dung">Bỏ qua điều hướng</a>
<header class="dau-trang"><div class="thanh">
  <a class="thuong-hieu" href="{tien_to}index.html">
    <span class="bieu-tuong">{LOGO_SVG}</span><span>{html.escape(cau_hinh.tieu_de)}</span>
  </a>
  <nav aria-label="Điều hướng chính">
    <a href="{tien_to}index.html#lo-trinh">Lộ trình</a>
    <a href="{tien_to}tra-cuu.html">Tra cứu</a>
    <a href="{cau_hinh.kho_ma_nguon}">Mã nguồn</a>
  </nav>
</div></header>"""


def _chan_trang(cau_hinh: CauHinh) -> str:
    nam = datetime.now(UTC).year
    return f"""<footer class="chan-trang"><div>
  <span>© {nam} {html.escape(cau_hinh.tac_gia)} · Phát hành theo giấy phép MIT.</span>
  <span>Viết bằng Python · Dành cho cộng đồng GIS Việt Nam.</span>
</div></footer>"""


def _khung_html(
    cau_hinh: CauHinh,
    tieu_de: str,
    noi_dung: str,
    mo_ta: str,
    duong_dan_chuan: str,
) -> str:
    dia_chi = f"{cau_hinh.dia_chi_chuan_hoa}/{duong_dan_chuan}".lstrip("/")
    canonical = (
        f'<link rel="canonical" href="{html.escape(cau_hinh.dia_chi_chuan_hoa)}/{duong_dan_chuan}">'
        if cau_hinh.dia_chi_chuan_hoa
        else ""
    )
    return f"""<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="description" content="{html.escape(mo_ta)}">
  <meta name="author" content="{html.escape(cau_hinh.tac_gia)}">
  <meta property="og:locale" content="vi_VN">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{html.escape(tieu_de)}">
  <meta property="og:description" content="{html.escape(mo_ta)}">
  <meta property="og:url" content="{html.escape(dia_chi)}">
  {canonical}
  <title>{html.escape(tieu_de)} · {html.escape(cau_hinh.tieu_de)}</title>
  <link rel="stylesheet" href="tai-nguyen/giao-dien.css">
</head>
<body>{_dau_trang(cau_hinh)}{noi_dung}{_chan_trang(cau_hinh)}</body>
</html>"""


def _dieu_huong_ben(chuong_hien_tai: Chuong, cac_chuong: list[Chuong]) -> str:
    theo_nhom: dict[str, list[Chuong]] = defaultdict(list)
    for chuong in cac_chuong:
        theo_nhom[chuong.nhom].append(chuong)
    ket_qua = ['<aside class="ben-trai" aria-label="Danh sách chương">']
    for nhom, cac_muc in theo_nhom.items():
        ket_qua.append(f'<p class="nhan-nhom">{html.escape(nhom)}</p><ul class="danh-sach-chuong">')
        for muc in cac_muc:
            lop = ' class="hien-tai" aria-current="page"' if muc == chuong_hien_tai else ""
            ket_qua.append(
                f'<li><a href="{muc.ten_tap_tin_html}"{lop}>{muc.thu_tu:02d}. '
                f"{html.escape(muc.tieu_de)}</a></li>"
            )
        ket_qua.append("</ul>")
    ket_qua.append("</aside>")
    return "".join(ket_qua)


def _trang_chuong(
    cau_hinh: CauHinh, chuong: Chuong, cac_chuong: list[Chuong], vi_tri: int
) -> str:
    bai_viet, muc_luc = chuyen_markdown(chuong.noi_dung)
    muc_trang = ['<aside class="muc-trang" aria-label="Mục lục trang"><h2>Trong chương</h2>']
    for cap, tieu_de, dinh_danh in muc_luc:
        muc_trang.append(
            f'<a class="cap-{cap}" href="#{dinh_danh}">{html.escape(tieu_de)}</a>'
        )
    muc_trang.append("</aside>")

    dieu_huong = ['<nav class="dieu-huong" aria-label="Chuyển chương">']
    if vi_tri:
        truoc = cac_chuong[vi_tri - 1]
        dieu_huong.append(
            f'<a href="{truoc.ten_tap_tin_html}"><small>← Chương trước</small>'
            f"{html.escape(truoc.tieu_de)}</a>"
        )
    else:
        dieu_huong.append("<span></span>")
    if vi_tri < len(cac_chuong) - 1:
        sau = cac_chuong[vi_tri + 1]
        dieu_huong.append(
            f'<a href="{sau.ten_tap_tin_html}"><small>Chương tiếp →</small>'
            f"{html.escape(sau.tieu_de)}</a>"
        )
    dieu_huong.append("</nav>")

    noi_dung = f"""<main id="noi-dung" class="bo-cuc">
{_dieu_huong_ben(chuong, cac_chuong)}
<article class="noi-dung">
  <div class="duong-dan">Giáo trình / {html.escape(chuong.nhom)} / Chương {chuong.thu_tu}</div>
  <h1 class="tieu-de-trang">{html.escape(chuong.tieu_de)}</h1>
  <p class="tom-tat">{html.escape(chuong.tom_tat)}</p>
  <div class="thong-tin"><span>⏱ {chuong.so_phut_doc} phút đọc</span><span>✍ {html.escape(cau_hinh.tac_gia)}</span></div>
  <div class="bai-viet">{bai_viet}</div>
  {''.join(dieu_huong)}
</article>
{''.join(muc_trang)}
</main>"""
    return _khung_html(
        cau_hinh,
        chuong.tieu_de,
        noi_dung,
        chuong.tom_tat,
        chuong.ten_tap_tin_html,
    )


def _trang_chu(cau_hinh: CauHinh, cac_chuong: list[Chuong]) -> str:
    the_chuong = []
    for chuong in cac_chuong:
        the_chuong.append(
            f'<a class="the-chuong" href="{chuong.ten_tap_tin_html}">'
            f"<span>Chương {chuong.thu_tu:02d} · {html.escape(chuong.nhom)}</span>"
            f"<h3>{html.escape(chuong.tieu_de)}</h3><p>{html.escape(chuong.tom_tat)}</p></a>"
        )
    noi_dung = f"""<main id="noi-dung">
<section class="anh-hung">
  <div><p class="nhan-nhom">Giáo trình mở · 100% tiếng Việt</p>
    <h1>Phân tích GIS<br>với Python</h1>
    <p>Từ dữ liệu vector, raster và hệ tọa độ đến PyQGIS, viễn thám, GeoAI và xuất bản WebGIS.
    Học theo dự án, chạy được trên máy cá nhân, không phụ thuộc phần mềm độc quyền.</p>
    <a class="nut" href="{cac_chuong[0].ten_tap_tin_html}">Bắt đầu học →</a>
    <a class="nut phu" href="{cau_hinh.kho_ma_nguon}">Xem mã nguồn</a>
  </div><div class="the-ban-do">{BAN_DO_SVG}</div>
</section>
<section class="so-lieu" aria-label="Thông tin giáo trình">
  <div><strong>{len(cac_chuong)}</strong>chương thực hành</div>
  <div><strong>70+</strong>thư viện được phân loại</div>
  <div><strong>Python</strong>trình dựng thuần Python</div>
  <div><strong>MIT</strong>tự do học và phát triển</div>
</section>
<section class="khu-vuc" id="lo-trinh"><p class="nhan-nhom">Lộ trình học tập</p>
  <h2>Đi từ nền tảng đến một dự án GIS hoàn chỉnh</h2>
  <div class="luoi-chuong">{''.join(the_chuong)}</div>
</section></main>"""
    return _khung_html(cau_hinh, "Trang chủ", noi_dung, cau_hinh.mo_ta, "index.html")


def _trang_tra_cuu(cau_hinh: CauHinh, cac_chuong: list[Chuong]) -> str:
    cac_hang = []
    for chuong in cac_chuong:
        cac_hang.append(
            f"<tr><td>{chuong.thu_tu:02d}</td><td><a href=\"{chuong.ten_tap_tin_html}\">"
            f"{html.escape(chuong.tieu_de)}</a></td><td>{html.escape(chuong.nhom)}</td>"
            f"<td>{html.escape(chuong.tom_tat)}</td></tr>"
        )
    noi_dung = f"""<main id="noi-dung" class="khu-vuc">
<p class="nhan-nhom">Chỉ mục</p><h1 class="tieu-de-trang">Tra cứu giáo trình</h1>
<p class="tom-tat">Dùng chức năng tìm trên trang của trình duyệt (Ctrl + F) để tra nhanh chủ đề.</p>
<div class="bang-cuon"><table><thead><tr><th>Số</th><th>Chương</th><th>Nhóm</th><th>Nội dung</th>
</tr></thead><tbody>{''.join(cac_hang)}</tbody></table></div></main>"""
    return _khung_html(
        cau_hinh, "Tra cứu", noi_dung, "Chỉ mục đầy đủ của giáo trình Python GIS", "tra-cuu.html"
    )


def dung_website(cau_hinh: CauHinh) -> list[Path]:
    """Dựng toàn bộ website, trả về danh sách tệp đã tạo."""

    cac_chuong = doc_cac_chuong(cau_hinh.thu_muc_noi_dung)
    if cau_hinh.thu_muc_dich.exists():
        shutil.rmtree(cau_hinh.thu_muc_dich)
    thu_muc_tai_nguyen = cau_hinh.thu_muc_dich / "tai-nguyen"
    thu_muc_tai_nguyen.mkdir(parents=True)
    da_tao: list[Path] = []

    def ghi(ten: str, noi_dung: str) -> None:
        duong_dan = cau_hinh.thu_muc_dich / ten
        duong_dan.write_text(noi_dung, encoding="utf-8")
        da_tao.append(duong_dan)

    ghi("tai-nguyen/giao-dien.css", CSS.strip() + "\n")
    ghi("index.html", _trang_chu(cau_hinh, cac_chuong))
    ghi("tra-cuu.html", _trang_tra_cuu(cau_hinh, cac_chuong))
    for vi_tri, chuong in enumerate(cac_chuong):
        ghi(chuong.ten_tap_tin_html, _trang_chuong(cau_hinh, chuong, cac_chuong, vi_tri))
    ghi("robots.txt", "User-agent: *\nAllow: /\nSitemap: sitemap.xml\n")
    cac_url = ["index.html", "tra-cuu.html", *(c.ten_tap_tin_html for c in cac_chuong)]
    goc = cau_hinh.dia_chi_chuan_hoa
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += "\n".join(f"  <url><loc>{goc}/{url}</loc></url>" for url in cac_url)
    sitemap += "\n</urlset>\n"
    ghi("sitemap.xml", sitemap)
    return da_tao
