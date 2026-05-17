import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

# ─── Bảng màu chủ đạo ───────────────────────────────────────────────────────
C_PRIMARY   = "#1a73e8"   # Xanh dương chính
C_PRIMARY_D = "#1558b0"   # Xanh đậm hơn (hover)
C_SUCCESS   = "#1e8e3e"   # Xanh lá (học bổng)
C_DANGER    = "#d93025"   # Đỏ (yếu)
C_WARN      = "#f29900"   # Cam cảnh báo
C_BG        = "#f0f4f8"   # Nền tổng thể
C_TOOLBAR   = "#ffffff"   # Toolbar trắng
C_HEADER    = "#1a73e8"   # Header popup
C_HEADER_TXT= "#ffffff"
C_CARD      = "#ffffff"   # Card nền form
C_ROW_EVEN  = "#f8fbff"
C_ROW_ODD   = "#ffffff"
C_STAT_BG   = "#1a73e8"
C_STAT_TXT  = "#ffffff"
FONT_BASE   = ("Segoe UI", 10)
FONT_BOLD   = ("Segoe UI", 10, "bold")
FONT_TITLE  = ("Segoe UI", 13, "bold")
FONT_SMALL  = ("Segoe UI", 9)


def _styled_btn(parent, text, bg, fg="#fff", cmd=None, pad=(10, 5)):
    """Tạo nút tk.Button có màu tùy chỉnh."""
    b = tk.Button(
        parent, text=text, bg=bg, fg=fg,
        font=FONT_BOLD, relief="flat", cursor="hand2",
        padx=pad[0], pady=pad[1], activebackground=C_PRIMARY_D,
        activeforeground="#fff", bd=0,
        command=cmd
    )
    b.bind("<Enter>", lambda e: b.config(bg=_darken(bg)))
    b.bind("<Leave>", lambda e: b.config(bg=bg))
    return b


def _darken(hex_color):
    r = max(0, int(hex_color[1:3], 16) - 20)
    g = max(0, int(hex_color[3:5], 16) - 20)
    b = max(0, int(hex_color[5:7], 16) - 20)
    return f"#{r:02x}{g:02x}{b:02x}"


def sort_treeview(tree, col, reverse):
    if col == "Chọn":
        return
    l = [(tree.set(k, col), k) for k in tree.get_children("")]
    try:
        def cv(x):
            v = str(x).replace("✅ Có", "1").replace("❌ Không", "0").split(" ")[0]
            return float(v)
        l.sort(key=lambda t: cv(t[0]), reverse=reverse)
    except ValueError:
        l.sort(reverse=reverse)
    for i, (_, k) in enumerate(l):
        tree.move(k, "", i)
    tree.heading(col, command=lambda: sort_treeview(tree, col, not reverse))


def tao_giao_dien_chinh(root):
    import sys, os
    root.title("ScholarScore – Xét Điểm Học Bổng")
    root.geometry("1300x650")
    root.configure(bg=C_BG)

    try:
        base_path = sys._MEIPASS if getattr(sys, "frozen", False) else \
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "assets", "app_icon.ico")
        if os.path.exists(icon_path):
            root.iconbitmap(default=icon_path)
    except Exception:
        pass

    # ── Style ttk ──
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview.Heading",
                    font=("Segoe UI", 10, "bold"),
                    background=C_PRIMARY, foreground="white",
                    relief="flat", padding=4)
    style.map("Treeview.Heading", background=[("active", C_PRIMARY_D)])
    style.configure("Treeview", font=("Segoe UI Emoji", 10),
                    rowheight=28, background=C_ROW_ODD,
                    fieldbackground=C_ROW_ODD, borderwidth=0)
    style.map("Treeview", background=[("selected", "#c2d8f8")],
              foreground=[("selected", "#000")])
    style.configure("TEntry", padding=4)
    style.configure("TCombobox", padding=4)

    ui = {}

    # ── TOOLBAR ──────────────────────────────────────────────────────────────
    frame_top = tk.Frame(root, bg=C_TOOLBAR, pady=8, padx=12,
                         relief="flat", bd=0)
    frame_top.pack(fill=tk.X)
    # Đường kẻ dưới toolbar
    tk.Frame(root, bg="#dadce0", height=1).pack(fill=tk.X)

    fa = tk.Frame(frame_top, bg=C_TOOLBAR)
    fa.pack(side=tk.LEFT)

    # ── Logo mini ──
    lbl_logo = tk.Label(fa, text="🎓 ScholarScore",
                        font=("Segoe UI", 12, "bold"),
                        fg=C_PRIMARY, bg=C_TOOLBAR)
    lbl_logo.pack(side=tk.LEFT, padx=(0, 16))

    def _tb_btn(txt, bg=C_PRIMARY):
        b = _styled_btn(fa, txt, bg, pad=(10, 4))
        b.pack(side=tk.LEFT, padx=3)
        return b

    ui["btn_them"]      = _tb_btn("＋ Thêm SV")
    ui["btn_sua"]       = _tb_btn("✏ Sửa", bg="#5f6368")
    ui["btn_xoa"]       = _tb_btn("🗑 Xóa", bg=C_DANGER)

    tk.Frame(fa, bg="#dadce0", width=1, height=28).pack(side=tk.LEFT, padx=8, pady=2)

    ui["btn_nhap_diem"] = _tb_btn("📝 Nhập Điểm", bg="#0b8043")
    ui["btn_import"]    = _tb_btn("📂 Import CSV", bg="#5f6368")
    ui["btn_export"]    = _tb_btn("💾 Export CSV", bg="#5f6368")

    tk.Frame(fa, bg="#dadce0", width=1, height=28).pack(side=tk.LEFT, padx=8, pady=2)
    ui["btn_about"]     = _tb_btn("ℹ️ Giới thiệu", bg="#5f6368")

    # ── Tìm kiếm (bên phải) ──
    fs = tk.Frame(frame_top, bg=C_TOOLBAR)
    fs.pack(side=tk.RIGHT)

    tk.Label(fs, text="Tìm theo:", font=FONT_BASE,
             bg=C_TOOLBAR).pack(side=tk.LEFT, padx=(0, 4))
    ui["cbo_search_by"] = ttk.Combobox(
        fs, values=["Tất cả", "MSV", "Họ Tên", "Giới tính",
                    "SĐT", "Xếp loại", "Học bổng"],
        state="readonly", width=10, font=FONT_BASE)
    ui["cbo_search_by"].set("Tất cả")
    ui["cbo_search_by"].pack(side=tk.LEFT, padx=3)

    ui["ent_search"] = ttk.Entry(fs, width=20, font=FONT_BASE)
    ui["ent_search"].pack(side=tk.LEFT, padx=3)

    ui["btn_search"]       = _styled_btn(fs, "🔍 Tìm", C_PRIMARY, pad=(8, 4))
    ui["btn_search"].pack(side=tk.LEFT, padx=3)
    ui["btn_clear_search"] = _styled_btn(fs, "✖ Hủy", "#5f6368", pad=(8, 4))
    ui["btn_clear_search"].pack(side=tk.LEFT, padx=3)

    # ── TREEVIEW ─────────────────────────────────────────────────────────────
    frame_mid = tk.Frame(root, bg=C_BG, padx=10, pady=6)
    frame_mid.pack(fill=tk.BOTH, expand=True)

    scroll_y = ttk.Scrollbar(frame_mid)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    scroll_x = ttk.Scrollbar(frame_mid, orient=tk.HORIZONTAL)
    scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

    cols = ["Chọn", "STT", "MSV", "Họ Tên", "Giới tính", "Lớp", "SĐT",
            "CC (0-10)", "GK (0-10)", "CK (0-10)", "RL (0-100)",
            "Điểm TB", "Xếp Loại", "Học Bổng"]
    ui["cols"] = cols

    tree = ttk.Treeview(frame_mid, columns=cols, show="headings",
                        yscrollcommand=scroll_y.set,
                        xscrollcommand=scroll_x.set,
                        selectmode="browse")
    ui["tree"] = tree
    scroll_y.config(command=tree.yview)
    scroll_x.config(command=tree.xview)

    col_widths = {
        "Chọn": 45, "STT": 40, "MSV": 90, "Họ Tên": 185,
        "Giới tính": 72, "Lớp": 82, "SĐT": 100,
        "CC (0-10)": 78, "GK (0-10)": 78, "CK (0-10)": 78,
        "RL (0-100)": 85, "Điểm TB": 78, "Xếp Loại": 92, "Học Bổng": 90,
    }
    for col in cols:
        htxt = "☐" if col == "Chọn" else col
        if col != "Chọn":
            tree.heading(col, text=htxt,
                         command=lambda c=col: sort_treeview(tree, c, False))
        else:
            tree.heading(col, text=htxt)
        tree.column(col, width=col_widths.get(col, 90),
                    anchor=tk.W if col == "Họ Tên" else tk.CENTER,
                    minwidth=col_widths.get(col, 50))

    tree.tag_configure("even",  background=C_ROW_EVEN)
    tree.tag_configure("odd",   background=C_ROW_ODD)
    tree.tag_configure("hb",    foreground=C_SUCCESS, font=FONT_BOLD)
    tree.tag_configure("yeu",   foreground=C_DANGER)
    tree.pack(fill=tk.BOTH, expand=True)

    # ── STATS BAR ────────────────────────────────────────────────────────────
    frame_bot = tk.Frame(root, bg=C_STAT_BG, pady=7, padx=16)
    frame_bot.pack(fill=tk.X)

    def _stat(txt, fg=C_STAT_TXT, bold=True):
        f = FONT_BOLD if bold else FONT_SMALL
        lbl = tk.Label(frame_bot, text=txt, font=f,
                       fg=fg, bg=C_STAT_BG)
        lbl.pack(side=tk.LEFT, padx=18)
        return lbl

    ui["lbl_si_so"]    = _stat("Sĩ số: 0")
    ui["lbl_du_hb"]    = _stat("🎓 Học Bổng: 0", fg="#a8d8a8")
    ui["lbl_diem_tb"]  = _stat("Điểm TB: 0.00")
    ui["lbl_xuat_sac"] = _stat("Xuất sắc: 0 | Giỏi: 0", bold=False)

    tk.Label(frame_bot,
             text="TB = CC×0.1 + GK×0.3 + CK×0.6  |  HB: TB≥8.0 & RL≥80",
             font=("Segoe UI", 9, "italic"),
             fg="#c8dcf8", bg=C_STAT_BG).pack(side=tk.LEFT, padx=18)

    tk.Label(frame_bot,
             text="💡 Double-click ô điểm để sửa nhanh",
             font=("Segoe UI", 9, "italic"),
             fg="#c8dcf8", bg=C_STAT_BG).pack(side=tk.RIGHT, padx=10)

    return ui


def hien_thi_bang(ui, df):
    tree = ui["tree"]
    tree.heading("Chọn", text="☐")
    for row in tree.get_children():
        tree.delete(row)
    if df.empty:
        return

    for idx, (_, row) in enumerate(df.iterrows(), start=1):
        values = [
            "☐", str(idx),
            row.get("msv", ""), row.get("ho_ten", ""),
            row.get("gioi_tinh", "Nam"), row.get("lop", ""), row.get("sdt", ""),
            f"{float(row.get('diem_cc', 0)):.1f}",
            f"{float(row.get('diem_gk', 0)):.1f}",
            f"{float(row.get('diem_ck', 0)):.1f}",
            f"{float(row.get('diem_rl', 0)):.1f}",
            f"{float(row.get('diem_tb', 0)):.2f}",
            row.get("xep_loai", ""),
            row.get("du_hb", ""),
        ]
        du_hb    = row.get("du_hb", "")
        xep_loai = row.get("xep_loai", "")
        base_tag = "even" if idx % 2 == 0 else "odd"

        if du_hb == "✅ Có":
            tag = "hb"
        elif xep_loai == "Yếu":
            tag = "yeu"
        else:
            tag = base_tag

        tree.insert("", tk.END, values=values, tags=(tag,))

    tree.tag_configure("even", background=C_ROW_EVEN)
    tree.tag_configure("odd",  background=C_ROW_ODD)
    tree.tag_configure("hb",   foreground=C_SUCCESS, font=FONT_BOLD)
    tree.tag_configure("yeu",  foreground=C_DANGER)


def cap_nhat_thong_ke(ui, stats):
    tong = stats.get("tong_sv", 0)
    nam  = stats.get("nam", 0)
    nu   = stats.get("nu", 0)
    ui["lbl_si_so"].config(text=f"Sĩ số: {tong}  (Nam: {nam}, Nữ: {nu})")
    ui["lbl_du_hb"].config(text=f"🎓 Học Bổng: {stats.get('du_hb', 0)}")
    ui["lbl_diem_tb"].config(text=f"Điểm TB: {stats.get('diem_tb_tb', 0):.2f}")
    ui["lbl_xuat_sac"].config(
        text=f"Xuất sắc: {stats.get('xuat_sac', 0)} | Giỏi: {stats.get('gioi', 0)}")


# ─── Helper popup builder ────────────────────────────────────────────────────
def _make_popup(parent_root, title, width=420):
    top = tk.Toplevel(parent_root)
    top.title(title)
    top.resizable(False, False)
    top.grab_set()
    top.configure(bg=C_BG)

    # Header banner
    hdr = tk.Frame(top, bg=C_PRIMARY, pady=14)
    hdr.pack(fill=tk.X)
    tk.Label(hdr, text=title, font=FONT_TITLE,
             fg="white", bg=C_PRIMARY).pack()

    # Card body
    card = tk.Frame(top, bg=C_CARD, padx=28, pady=20,
                    relief="flat", bd=0)
    card.pack(fill=tk.BOTH, expand=True, padx=16, pady=14)

    return top, card


def _center_popup(top, parent_root):
    top.update_idletasks()
    x = parent_root.winfo_x() + (parent_root.winfo_width()  - top.winfo_reqwidth())  // 2
    y = parent_root.winfo_y() + (parent_root.winfo_height() - top.winfo_reqheight()) // 2
    top.geometry(f"+{x}+{y}")


def _lbl_entry(card, row, label_text, width=28):
    tk.Label(card, text=label_text, font=FONT_BASE,
             bg=C_CARD, anchor=tk.E).grid(row=row, column=0,
                                           padx=(0, 10), pady=8, sticky=tk.E)
    ent = ttk.Entry(card, width=width, font=FONT_BASE)
    ent.grid(row=row, column=1, pady=8, sticky=tk.W)
    return ent


# ─── Form Nhập Điểm ─────────────────────────────────────────────────────────
def hien_thi_form_nhap_diem(parent_root, msv, ho_ten, current_scores=None):
    if current_scores is None:
        current_scores = {}

    top, card = _make_popup(parent_root,
                            f"📝  Nhập Điểm  –  {ho_ten}  ({msv})")
    result = []

    # Thông tin SV
    tk.Label(card,
             text=f"Sinh viên: {ho_ten}   |   MSV: {msv}",
             font=("Segoe UI", 10, "bold"),
             fg=C_PRIMARY, bg=C_CARD
             ).grid(row=0, column=0, columnspan=3, pady=(0, 14))

    fields = [
        ("Chuyên Cần (CC):", "diem_cc",  0.0,  10.0, "0 – 10"),
        ("Giữa Kỳ   (GK):", "diem_gk",  0.0,  10.0, "0 – 10"),
        ("Cuối Kỳ   (CK):", "diem_ck",  0.0,  10.0, "0 – 10"),
        ("Rèn Luyện (RL):", "diem_rl",  0.0, 100.0, "0 – 100"),
    ]

    entries = {}
    for i, (lbl, key, mn, mx, hint) in enumerate(fields, start=1):
        tk.Label(card, text=lbl, font=FONT_BASE,
                 bg=C_CARD, anchor=tk.E).grid(row=i, column=0,
                                               padx=(0, 10), pady=8, sticky=tk.E)
        ent = ttk.Entry(card, width=12, font=FONT_BASE)
        val = current_scores.get(key, mn)
        ent.insert(0, f"{float(val):.1f}")
        ent.grid(row=i, column=1, pady=8, sticky=tk.W)
        tk.Label(card, text=hint, font=FONT_SMALL,
                 fg="#888", bg=C_CARD).grid(row=i, column=2,
                                             padx=(8, 0), sticky=tk.W)
        entries[key] = (ent, mn, mx)

    # Live preview
    sep = tk.Frame(card, bg="#dadce0", height=1)
    sep.grid(row=len(fields)+1, column=0, columnspan=3,
             sticky="ew", pady=(12, 0))

    lbl_pre = tk.Label(card, text="Điểm TB dự kiến: –",
                       font=("Segoe UI", 12, "bold"),
                       fg=C_PRIMARY, bg=C_CARD)
    lbl_pre.grid(row=len(fields)+2, column=0, columnspan=3, pady=(10, 0))

    def update_pre(*_):
        try:
            tb = (float(entries["diem_cc"][0].get()) * 0.1 +
                  float(entries["diem_gk"][0].get()) * 0.3 +
                  float(entries["diem_ck"][0].get()) * 0.6)
            tb = max(0.0, min(10.0, tb))
            color = C_SUCCESS if tb >= 8.0 else (C_WARN if tb >= 6.5 else C_DANGER)
            lbl_pre.config(text=f"Điểm TB dự kiến: {tb:.2f}", fg=color)
        except ValueError:
            lbl_pre.config(text="Điểm TB dự kiến: –", fg=C_PRIMARY)

    for k in ["diem_cc", "diem_gk", "diem_ck"]:
        entries[k][0].bind("<KeyRelease>", update_pre)
    update_pre()

    def on_luu():
        scores = {}
        for key, (ent, mn, mx) in entries.items():
            try:
                v = float(ent.get().strip())
                if not (mn <= v <= mx):
                    messagebox.showwarning(
                        "Lỗi", f"Điểm phải trong khoảng {mn:.0f} – {mx:.0f}!", parent=top)
                    return
                scores[key] = v
            except ValueError:
                messagebox.showwarning("Lỗi", "Vui lòng nhập số hợp lệ!", parent=top)
                return
        result.append(scores)
        top.destroy()

    # Buttons
    fb = tk.Frame(card, bg=C_CARD)
    fb.grid(row=len(fields)+3, column=0, columnspan=3, pady=(16, 0))
    _styled_btn(fb, "💾  Lưu điểm", C_SUCCESS, cmd=on_luu).pack(side=tk.LEFT, padx=8)
    _styled_btn(fb, "Hủy", "#5f6368", cmd=top.destroy).pack(side=tk.LEFT, padx=8)

    _center_popup(top, parent_root)
    top.wait_window()
    return result[0] if result else None


# ─── Form Thêm / Sửa Sinh Viên ───────────────────────────────────────────────
def hien_thi_form_sinh_vien(parent_root, is_edit=False, current_data=None):
    title = "✏️  Sửa Sinh viên" if is_edit else "＋  Thêm Sinh viên"
    top, card = _make_popup(parent_root, title)
    result = []

    ent_msv   = _lbl_entry(card, 0, "MSV (*):")
    ent_hoten = _lbl_entry(card, 1, "Họ tên (*):")

    tk.Label(card, text="Giới tính:", font=FONT_BASE,
             bg=C_CARD, anchor=tk.E).grid(row=2, column=0,
                                           padx=(0, 10), pady=8, sticky=tk.E)
    cbo_gt = ttk.Combobox(card, values=["Nam", "Nữ", "Khác"],
                          state="readonly", width=26, font=FONT_BASE)
    cbo_gt.set("Nam")
    cbo_gt.grid(row=2, column=1, pady=8, sticky=tk.W)

    ent_lop = _lbl_entry(card, 3, "Lớp:")
    ent_sdt = _lbl_entry(card, 4, "SĐT:")

    if is_edit and current_data:
        ent_msv.insert(0, current_data.get("msv", ""))
        ent_hoten.insert(0, current_data.get("ho_ten", ""))
        cbo_gt.set(current_data.get("gioi_tinh", "Nam"))
        ent_lop.insert(0, current_data.get("lop", ""))
        ent_sdt.insert(0, current_data.get("sdt", ""))

    def on_luu():
        msv   = ent_msv.get().strip()
        hoten = ent_hoten.get().strip()
        if not msv:
            messagebox.showwarning("Lỗi", "MSV không được để trống!", parent=top)
            return
        if not hoten:
            messagebox.showwarning("Lỗi", "Họ tên không được để trống!", parent=top)
            return
        result.append({"msv": msv, "ho_ten": hoten,
                       "gioi_tinh": cbo_gt.get(),
                       "lop": ent_lop.get().strip(),
                       "sdt": ent_sdt.get().strip()})
        top.destroy()

    tk.Frame(card, bg="#dadce0", height=1).grid(
        row=5, column=0, columnspan=2, sticky="ew", pady=(14, 0))

    fb = tk.Frame(card, bg=C_CARD)
    fb.grid(row=6, column=0, columnspan=2, pady=(14, 0))
    _styled_btn(fb, "💾  Lưu", C_PRIMARY, cmd=on_luu).pack(side=tk.LEFT, padx=8)
    _styled_btn(fb, "Hủy", "#5f6368", cmd=top.destroy).pack(side=tk.LEFT, padx=8)

    _center_popup(top, parent_root)
    top.wait_window()
    return result[0] if result else None
