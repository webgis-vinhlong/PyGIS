from pathlib import Path

from pygis_vn.config import CauHinh
from pygis_vn.content import doc_cac_chuong
from pygis_vn.markdown import chuyen_markdown, tao_dinh_danh
from pygis_vn.render import dung_website

THU_MUC_GOC = Path(__file__).parents[1]


def test_doc_du_chuong_va_khong_trung_dinh_danh() -> None:
    cac_chuong = doc_cac_chuong(THU_MUC_GOC / "noi_dung")
    assert len(cac_chuong) >= 15
    assert len({chuong.dinh_danh for chuong in cac_chuong}) == len(cac_chuong)
    assert all(chuong.tom_tat for chuong in cac_chuong)


def test_chuyen_markdown_an_toan_va_co_muc_luc() -> None:
    html, muc_luc = chuyen_markdown("## Hệ tọa độ\n\n`EPSG:4326`\n\n<script>xấu</script>")
    assert 'id="hệ-tọa-độ"' in html
    assert "&lt;script&gt;" in html
    assert muc_luc == [(2, "Hệ tọa độ", "hệ-tọa-độ")]
    assert tao_dinh_danh("Phân tích GIS!") == "phân-tích-gis"


def test_dung_website_day_du(tmp_path: Path) -> None:
    dich = tmp_path / "site"
    cac_tap_tin = dung_website(
        CauHinh(
            thu_muc_noi_dung=THU_MUC_GOC / "noi_dung",
            thu_muc_dich=dich,
            dia_chi_goc="https://webgis-vinhlong.github.io/PyGIS",
        )
    )
    assert len(cac_tap_tin) >= 20
    trang_chu = (dich / "index.html").read_text(encoding="utf-8")
    assert '<html lang="vi">' in trang_chu
    assert "Phân tích GIS" in trang_chu
    assert (dich / "tai-nguyen" / "giao-dien.css").stat().st_size > 5_000
