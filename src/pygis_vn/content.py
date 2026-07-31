"""Đọc nội dung tài liệu từ Markdown có siêu dữ liệu tối giản."""

from pathlib import Path

from pygis_vn.models import Chuong


def _tach_sieu_du_lieu(van_ban: str) -> tuple[dict[str, str], str]:
    if not van_ban.startswith("---\n"):
        raise ValueError("Mỗi chương phải bắt đầu bằng khối siêu dữ liệu ---")
    _, khoi, noi_dung = van_ban.split("---\n", 2)
    sieu_du_lieu: dict[str, str] = {}
    for dong in khoi.splitlines():
        if not dong.strip():
            continue
        khoa, dau, gia_tri = dong.partition(":")
        if not dau:
            raise ValueError(f"Dòng siêu dữ liệu không hợp lệ: {dong}")
        sieu_du_lieu[khoa.strip()] = gia_tri.strip()
    return sieu_du_lieu, noi_dung.strip()


def doc_cac_chuong(thu_muc: Path) -> list[Chuong]:
    """Đọc, kiểm tra và sắp xếp toàn bộ chương."""

    cac_chuong: list[Chuong] = []
    for duong_dan in sorted(thu_muc.glob("*.md")):
        sieu_du_lieu, noi_dung = _tach_sieu_du_lieu(
            duong_dan.read_text(encoding="utf-8")
        )
        khoa_bat_buoc = {"thu_tu", "dinh_danh", "tieu_de", "nhom", "tom_tat"}
        khoa_thieu = khoa_bat_buoc - sieu_du_lieu.keys()
        if khoa_thieu:
            raise ValueError(f"{duong_dan.name} thiếu: {', '.join(sorted(khoa_thieu))}")
        cac_chuong.append(
            Chuong(
                thu_tu=int(sieu_du_lieu["thu_tu"]),
                duong_dan=duong_dan,
                dinh_danh=sieu_du_lieu["dinh_danh"],
                tieu_de=sieu_du_lieu["tieu_de"],
                nhom=sieu_du_lieu["nhom"],
                tom_tat=sieu_du_lieu["tom_tat"],
                noi_dung=noi_dung,
            )
        )

    if not cac_chuong:
        raise ValueError(f"Không tìm thấy chương nào trong {thu_muc}")

    dinh_danh = [chuong.dinh_danh for chuong in cac_chuong]
    if len(dinh_danh) != len(set(dinh_danh)):
        raise ValueError("Định danh chương phải là duy nhất")

    return sorted(cac_chuong, key=lambda chuong: chuong.thu_tu)
