"""Bộ chuyển Markdown nhỏ gọn viết hoàn toàn bằng thư viện chuẩn Python."""

from __future__ import annotations

import html
import re


def tao_dinh_danh(van_ban: str) -> str:
    """Tạo định danh liên kết, giữ chữ tiếng Việt để URL dễ đọc."""

    van_ban = van_ban.casefold().strip()
    van_ban = re.sub(r"[^\w\s-]", "", van_ban, flags=re.UNICODE)
    return re.sub(r"[-\s]+", "-", van_ban).strip("-")


def _dinh_dang_noi_tuyen(van_ban: str) -> str:
    ket_qua = html.escape(van_ban, quote=False)
    mau_ma = re.compile(r"`([^`]+)`")
    ket_qua = mau_ma.sub(lambda k: f"<code>{k.group(1)}</code>", ket_qua)
    ket_qua = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", ket_qua)
    ket_qua = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", ket_qua)
    ket_qua = re.sub(
        r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
        r'<a href="\2" rel="noopener noreferrer">\1</a>',
        ket_qua,
    )
    ket_qua = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', ket_qua)
    return ket_qua


def _tao_bang(cac_dong: list[str]) -> str:
    hang = [[o.strip() for o in dong.strip().strip("|").split("|")] for dong in cac_dong]
    tieu_de, *than = hang
    html_bang = ["<div class=\"bang-cuon\"><table><thead><tr>"]
    html_bang.extend(f"<th>{_dinh_dang_noi_tuyen(o)}</th>" for o in tieu_de)
    html_bang.append("</tr></thead><tbody>")
    for dong in than[1:]:
        html_bang.append("<tr>")
        html_bang.extend(f"<td>{_dinh_dang_noi_tuyen(o)}</td>" for o in dong)
        html_bang.append("</tr>")
    html_bang.append("</tbody></table></div>")
    return "".join(html_bang)


def chuyen_markdown(van_ban: str) -> tuple[str, list[tuple[int, str, str]]]:
    """Chuyển tập con Markdown cần cho tài liệu thành HTML an toàn."""

    dong = van_ban.splitlines()
    html_ra: list[str] = []
    muc_luc: list[tuple[int, str, str]] = []
    chi_so = 0
    trong_ma = False
    ngon_ngu = ""
    bo_dem_ma: list[str] = []
    dang_danh_sach: str | None = None

    def dong_danh_sach() -> None:
        nonlocal dang_danh_sach
        if dang_danh_sach:
            html_ra.append(f"</{dang_danh_sach}>")
            dang_danh_sach = None

    while chi_so < len(dong):
        hien_tai = dong[chi_so]
        if hien_tai.startswith("```"):
            if trong_ma:
                ma = html.escape("\n".join(bo_dem_ma))
                nhan = f'<span class="nhan-ma">{html.escape(ngon_ngu)}</span>' if ngon_ngu else ""
                html_ra.append(
                    f'<div class="khoi-ma">{nhan}<pre><code class="language-{html.escape(ngon_ngu)}">'
                    f"{ma}</code></pre></div>"
                )
                bo_dem_ma.clear()
                trong_ma = False
                ngon_ngu = ""
            else:
                dong_danh_sach()
                trong_ma = True
                ngon_ngu = hien_tai[3:].strip()
            chi_so += 1
            continue
        if trong_ma:
            bo_dem_ma.append(hien_tai)
            chi_so += 1
            continue

        if (
            "|" in hien_tai
            and chi_so + 1 < len(dong)
            and re.match(r"^\s*\|?[\s:|-]+\|", dong[chi_so + 1])
        ):
            dong_danh_sach()
            cac_dong_bang = [hien_tai, dong[chi_so + 1]]
            chi_so += 2
            while chi_so < len(dong) and "|" in dong[chi_so] and dong[chi_so].strip():
                cac_dong_bang.append(dong[chi_so])
                chi_so += 1
            html_ra.append(_tao_bang(cac_dong_bang))
            continue

        khop_tieu_de = re.match(r"^(#{1,4})\s+(.+)$", hien_tai)
        if khop_tieu_de:
            dong_danh_sach()
            cap = len(khop_tieu_de.group(1))
            tieu_de = khop_tieu_de.group(2).strip()
            dinh_danh = tao_dinh_danh(tieu_de)
            html_ra.append(
                f'<h{cap} id="{dinh_danh}">{_dinh_dang_noi_tuyen(tieu_de)}'
                f'<a class="lien-ket-muc" href="#{dinh_danh}" aria-label="Liên kết đến mục này">#</a>'
                f"</h{cap}>"
            )
            if cap in (2, 3):
                muc_luc.append((cap, tieu_de, dinh_danh))
            chi_so += 1
            continue

        khop_danh_sach = re.match(r"^\s*[-*]\s+(.+)$", hien_tai)
        khop_danh_sach_so = re.match(r"^\s*\d+\.\s+(.+)$", hien_tai)
        if khop_danh_sach or khop_danh_sach_so:
            loai = "ul" if khop_danh_sach else "ol"
            if dang_danh_sach != loai:
                dong_danh_sach()
                html_ra.append(f"<{loai}>")
                dang_danh_sach = loai
            noi_dung = (khop_danh_sach or khop_danh_sach_so).group(1)
            html_ra.append(f"<li>{_dinh_dang_noi_tuyen(noi_dung)}</li>")
            chi_so += 1
            continue

        dong_danh_sach()
        if not hien_tai.strip():
            chi_so += 1
            continue
        if hien_tai.startswith(">"):
            cac_dong_trich: list[str] = []
            while chi_so < len(dong) and dong[chi_so].startswith(">"):
                cac_dong_trich.append(dong[chi_so].lstrip("> ").strip())
                chi_so += 1
            noi_dung = " ".join(cac_dong_trich)
            lop = "ghi-chu"
            if noi_dung.startswith("[!"):
                nhan, _, noi_dung = noi_dung.partition("]")
                lop = {
                    "[!MẸO": "meo",
                    "[!CẢNH BÁO": "canh-bao",
                    "[!GHI CHÚ": "ghi-chu",
                }.get(nhan, "ghi-chu")
            html_ra.append(f'<aside class="{lop}">{_dinh_dang_noi_tuyen(noi_dung.strip())}</aside>')
            continue
        if hien_tai.strip() == "---":
            html_ra.append("<hr>")
            chi_so += 1
            continue

        doan = [hien_tai.strip()]
        chi_so += 1
        while (
            chi_so < len(dong)
            and dong[chi_so].strip()
            and not re.match(r"^(#{1,4})\s+|^```|^\s*[-*]\s+|^\s*\d+\.\s+|^>", dong[chi_so])
        ):
            doan.append(dong[chi_so].strip())
            chi_so += 1
        html_ra.append(f"<p>{_dinh_dang_noi_tuyen(' '.join(doan))}</p>")

    dong_danh_sach()
    if trong_ma:
        raise ValueError("Khối mã chưa được đóng bằng ```")
    return "\n".join(html_ra), muc_luc
