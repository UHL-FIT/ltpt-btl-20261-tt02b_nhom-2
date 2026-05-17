"""
views/cli_view.py
=================
Module hiển thị giao diện CLI trên Terminal cho hệ thống Xét Học Bổng.
"""


def hien_menu_chinh():
    """
    Hiển thị menu chính và nhận đầu vào từ bàn phím.

    Returns:
        str: Lựa chọn của người dùng (từ '0' đến '6').
    """
    print()
    print("╔══════════════════════════════════════════╗")
    print("║       🎓 SCHOLARSCORE (CLI)              ║")
    print("╠══════════════════════════════════════════╣")
    print("║  1. Xem danh sách xét học bổng          ║")
    print("║  2. Thêm sinh viên                      ║")
    print("║  3. Sửa thông tin sinh viên             ║")
    print("║  4. Xóa sinh viên                       ║")
    print("║  5. Nhập điểm (CC/GK/CK/RL)            ║")
    print("║  6. Xem thống kê                        ║")
    print("║  0. Thoát                               ║")
    print("╚══════════════════════════════════════════╝")
    lua_chon = input("  Chọn chức năng: ").strip()
    return lua_chon


def hien_bang_hocbong(df):
    """
    Hiển thị danh sách sinh viên với điểm số và kết quả xét học bổng.

    Args:
        df (pandas.DataFrame): Bảng dữ liệu (đã có cột diem_tb, xep_loai, du_hb).
    """
    if df.empty:
        print("\n  (Chưa có sinh viên nào)")
        return

    print("\n  BẢNG XÉT HỌC BỔNG")
    header = (
        f"  {'STT':<4} {'MSV':<8} {'Họ tên':<20} {'GT':<4} {'Lớp':<10}"
        f" {'CC':>5} {'GK':>5} {'CK':>5} {'RL':>6}"
        f" {'TB':>6} {'Xếp loại':<11} {'Học Bổng'}"
    )
    print(header)
    print("  " + "─" * (len(header.strip()) + 2))

    for stt, (_, row) in enumerate(df.iterrows(), start=1):
        msv      = str(row.get("msv", ""))
        ho_ten   = str(row.get("ho_ten", ""))[:19]
        gt       = str(row.get("gioi_tinh", ""))[:3]
        lop      = str(row.get("lop", ""))[:9]
        cc       = float(row.get("diem_cc", 0))
        gk       = float(row.get("diem_gk", 0))
        ck       = float(row.get("diem_ck", 0))
        rl       = float(row.get("diem_rl", 0))
        tb       = float(row.get("diem_tb", 0))
        xep_loai = str(row.get("xep_loai", ""))
        du_hb    = str(row.get("du_hb", ""))

        print(
            f"  {stt:<4} {msv:<8} {ho_ten:<20} {gt:<4} {lop:<10}"
            f" {cc:>5.1f} {gk:>5.1f} {ck:>5.1f} {rl:>6.1f}"
            f" {tb:>6.2f} {xep_loai:<11} {du_hb}"
        )

    print(f"\n  Tổng: {len(df)} sinh viên")
    print("  Công thức: TB = CC×0.1 + GK×0.3 + CK×0.6  |  HB: TB≥8.0 và RL≥80")


def hien_thong_ke(stats):
    """
    Hiển thị khung thống kê xét học bổng.

    Args:
        stats (dict): Dictionary chứa các số liệu tổng hợp.
    """
    if not stats or stats.get("tong_sv", 0) == 0:
        print("\n  (Chưa có dữ liệu thống kê)")
        return

    si_so_str = (
        f"{stats['tong_sv']} (Nam: {stats.get('nam', 0)}, "
        f"Nữ: {stats.get('nu', 0)})"
    )
    print()
    print("  ╔══════════════════════════════════════════╗")
    print("  ║         📊 THỐNG KÊ XÉT HỌC BỔNG       ║")
    print("  ╠══════════════════════════════════════════╣")
    print(f"  ║  Sĩ số lớp       : {si_so_str:<21} ║")
    print(f"  ║  Điểm TB lớp     : {stats.get('diem_tb_tb', 0):<21.2f} ║")
    print(f"  ║  🎓 Đủ học bổng  : {stats.get('du_hb', 0):<21} ║")
    print(f"  ║  Xuất sắc (≥9.0) : {stats.get('xuat_sac', 0):<21} ║")
    print(f"  ║  Giỏi    (≥8.0)  : {stats.get('gioi', 0):<21} ║")
    print("  ╚══════════════════════════════════════════╝")


# ─── NHẬP LIỆU ──────────────────────────────────

def nhap_thong_tin_sv(current_msv=""):
    """
    Hỗ trợ nhập liệu thông tin cá nhân của sinh viên từ Terminal.

    Args:
        current_msv (str): Mã sinh viên hiện tại (dùng khi sửa thông tin).

    Returns:
        dict/None: Thông tin sinh viên hoặc None nếu nhập thiếu.
    """
    print("\n  ── Nhập thông tin sinh viên ──")
    if current_msv:
        msv = input(f"  MSV mới (Enter để giữ {current_msv}): ").strip() or current_msv
    else:
        msv = input("  MSV        : ").strip()

    ho_ten = input("  Họ tên     : ").strip()
    lop    = input("  Lớp        : ").strip()
    sdt    = input("  SĐT        : ").strip()

    if not msv or not ho_ten:
        thong_bao("❌ MSV và Họ tên không được để trống!")
        return None

    return {
        "msv":    msv,
        "ho_ten": ho_ten,
        "lop":    lop,
        "sdt":    sdt,
    }


def nhap_diem_sinh_vien():
    """
    Nhập điểm CC, GK, CK, RL cho một sinh viên.

    Returns:
        dict/None: {'diem_cc': float, 'diem_gk': float,
                    'diem_ck': float, 'diem_rl': float}
                   hoặc None nếu nhập không hợp lệ.
    """
    print("\n  ── Nhập điểm sinh viên ──")
    fields = [
        ("diem_cc", "Chuyên Cần (CC, 0-10)  : ", 0.0, 10.0),
        ("diem_gk", "Giữa Kỳ   (GK, 0-10)  : ", 0.0, 10.0),
        ("diem_ck", "Cuối Kỳ   (CK, 0-10)  : ", 0.0, 10.0),
        ("diem_rl", "Rèn Luyện (RL, 0-100) : ", 0.0, 100.0),
    ]
    scores = {}
    for key, label, mn, mx in fields:
        try:
            val = float(input(f"  {label}").strip())
            if not (mn <= val <= mx):
                thong_bao(f"❌ Giá trị phải trong khoảng {mn:.0f} – {mx:.0f}!")
                return None
            scores[key] = val
        except ValueError:
            thong_bao("❌ Vui lòng nhập số hợp lệ!")
            return None

    tb = scores["diem_cc"] * 0.1 + scores["diem_gk"] * 0.3 + scores["diem_ck"] * 0.6
    print(f"\n  → Điểm TB dự kiến: {tb:.2f}")
    return scores


def nhap_msv():
    """Nhập mã sinh viên."""
    return input("\n  Nhập MSV (VD: SV001): ").strip().upper()


# ─── TIỆN ÍCH ──────────────────────────────────

def thong_bao(msg):
    """Hiển thị thông báo."""
    print(f"\n  {msg}")


def xac_nhan(msg):
    """Hỏi xác nhận yes/no."""
    tra_loi = input(f"\n  {msg} (y/n): ").strip().lower()
    return tra_loi in ("y", "yes")
