import os
import sys
import shutil
import pandas as pd
import numpy as np
from utils.logger import setup_logger

logger = setup_logger()

# ─── Đường dẫn file CSV ──────────────────────────
if getattr(sys, 'frozen', False):
    _USER_DIR = os.path.join(os.path.expanduser("~"), "ScholarScore_Data")
    _BASE_DIR = _USER_DIR

    _INSTALL_DATA = os.path.join(os.path.dirname(sys.executable), "data")
    _USER_DATA = os.path.join(_BASE_DIR, "data")

    if not os.path.exists(_USER_DATA):
        os.makedirs(_USER_DATA, exist_ok=True)
        for f in ["hocbong.csv"]:
            src = os.path.join(_INSTALL_DATA, f)
            dst = os.path.join(_USER_DATA, f)
            if os.path.exists(src):
                shutil.copy2(src, dst)
else:
    _BASE_DIR = os.path.dirname(os.path.dirname(__file__))

FILE_HOCBONG = os.path.join(_BASE_DIR, "data", "hocbong.csv")

# ─── Hằng số xét học bổng ──────────────────────
DIEM_TB_MIN_HB = 8.0       # Điểm TB tối thiểu để xét học bổng
DIEM_RL_MIN_HB = 80.0      # Điểm Rèn Luyện tối thiểu để xét học bổng

# Hệ số tính điểm trung bình môn
HE_SO_CC = 0.1
HE_SO_GK = 0.3
HE_SO_CK = 0.6

BASE_COLS = ["msv", "ho_ten", "gioi_tinh", "lop", "sdt",
             "diem_cc", "diem_gk", "diem_ck", "diem_rl"]
TEXT_COLS = ["msv", "ho_ten", "gioi_tinh", "lop", "sdt"]


def _normalize_msv(value):
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return ""
    return str(value).strip().upper()


def _ensure_base_columns(df):
    df = df.copy()
    for col in BASE_COLS:
        if col not in df.columns:
            default_value = "" if col in TEXT_COLS else 0.0
            df[col] = default_value
    return df


def khoi_tao_csv():
    """
    Tạo file CSV rỗng nếu chưa tồn tại.
    Khởi tạo các cột: msv, ho_ten, gioi_tinh, lop, sdt,
                      diem_cc, diem_gk, diem_ck, diem_rl
    """
    os.makedirs(os.path.dirname(FILE_HOCBONG), exist_ok=True)
    if not os.path.exists(FILE_HOCBONG):
        cols = ["msv", "ho_ten", "gioi_tinh", "lop", "sdt",
                "diem_cc", "diem_gk", "diem_ck", "diem_rl"]
        df_empty = pd.DataFrame(columns=cols)
        df_empty.to_csv(FILE_HOCBONG, index=False, encoding="utf-8-sig")
        logger.info(f"Đã tạo file mới: {FILE_HOCBONG}")


def lay_danh_sach():
    """
    Đọc dữ liệu từ CSV và dùng Numpy tính toán realtime:
    - diem_tb  : Điểm Trung Bình = CC*0.1 + GK*0.3 + CK*0.6
    - xep_loai : Xếp loại học lực (Xuất sắc / Giỏi / Khá / Trung bình / Yếu)
    - du_hb    : Đủ điều kiện học bổng (Có / Không)

    Returns:
        tuple: (pandas.DataFrame chứa dữ liệu, bool Trạng thái thành công)
    """
    khoi_tao_csv()
    try:
        df = pd.read_csv(FILE_HOCBONG, encoding="utf-8-sig", dtype=str)
    except Exception as e:
        logger.error(f"Lỗi đọc file: {e}")
        return pd.DataFrame(), False

    if df.empty:
        return df, True

    # Đảm bảo cột văn bản tồn tại
    for text_col in ["msv", "ho_ten", "gioi_tinh", "lop", "sdt"]:
        if text_col not in df.columns:
            df[text_col] = "-"
        df[text_col] = df[text_col].fillna("-").replace("", "-")
        df[text_col] = df[text_col].astype(str).replace("nan", "-")

    # Đảm bảo cột điểm số tồn tại và ép về float
    score_cols = ["diem_cc", "diem_gk", "diem_ck", "diem_rl"]
    for col in score_cols:
        if col not in df.columns:
            df[col] = 0.0
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)

    # TÍNH TOÁN BẰNG NUMPY (Vectorization)
    cc_arr = df["diem_cc"].values
    gk_arr = df["diem_gk"].values
    ck_arr = df["diem_ck"].values
    rl_arr = df["diem_rl"].values

    # Điểm trung bình môn = CC*0.1 + GK*0.3 + CK*0.6
    diem_tb = cc_arr * HE_SO_CC + gk_arr * HE_SO_GK + ck_arr * HE_SO_CK
    diem_tb = np.clip(diem_tb, 0.0, 10.0)

    # Xếp loại học lực
    xep_loai = np.where(
        diem_tb >= 9.0, "Xuất sắc",
        np.where(
            diem_tb >= 8.0, "Giỏi",
            np.where(
                diem_tb >= 6.5, "Khá",
                np.where(
                    diem_tb >= 5.0, "Trung bình",
                    "Yếu"
                )
            )
        )
    )

    # Trước hết xác định đủ điều kiện ban đầu: TB >= 8.0 và RL >= 80
    eligible = (diem_tb >= DIEM_TB_MIN_HB) & (rl_arr >= DIEM_RL_MIN_HB)

    df["diem_tb"]  = diem_tb
    df["xep_loai"] = xep_loai
    df["du_hb"]    = "Không"

    if np.any(eligible):
        # Chọn tối đa 10 sinh viên đạt học bổng theo điểm TB giảm dần,
        # ưu tiên điểm RL cao hơn khi bằng điểm TB.
        eligible_df = df[eligible].copy()
        eligible_df = eligible_df.sort_values(
            by=["diem_tb", "diem_rl"], ascending=[False, False]
        ).head(10)
        df.loc[eligible_df.index, "du_hb"] = "Có"

    return df, True


def luu_danh_sach(df):
    """
    Ghi DataFrame hiện tại xuống CSV (chỉ lưu cột gốc, không lưu cột tính toán).

    Args:
        df (pandas.DataFrame): Dữ liệu cần lưu.

    Returns:
        bool: True nếu lưu thành công, False nếu thất bại.
    """
    try:
        cols_to_save = ["msv", "ho_ten", "gioi_tinh", "lop", "sdt",
                        "diem_cc", "diem_gk", "diem_ck", "diem_rl"]
        # Chỉ giữ những cột thực sự có trong df
        cols_to_save = [c for c in cols_to_save if c in df.columns]
        df_save = df[cols_to_save]
        df_save.to_csv(FILE_HOCBONG, index=False, encoding="utf-8-sig")
        logger.debug(f"Ghi file hocbong.csv ({len(df)} dòng)")
        return True
    except Exception as e:
        logger.error(f"Lỗi khi ghi file: {e}")
        return False


def them_sinh_vien(df, data):
    """
    Thêm sinh viên mới vào DataFrame.

    Args:
        df (pandas.DataFrame): Bảng dữ liệu hiện tại.
        data (dict): Thông tin SV (msv, ho_ten, gioi_tinh, lop, sdt).

    Returns:
        tuple: (DataFrame mới, bool Trạng thái, str Thông báo)
    """
    df = _ensure_base_columns(df)
    msv_moi = _normalize_msv(data.get("msv", ""))
    if not msv_moi:
        return df, False, "Mã sinh viên không được để trống!"

    existing_msvs = df["msv"].fillna("").astype(str).str.strip().str.upper()
    if msv_moi in existing_msvs.values:
        return df, False, "Mã sinh viên đã tồn tại!"

    row = {
        "msv":      msv_moi,
        "ho_ten":   str(data.get("ho_ten", "")).strip(),
        "gioi_tinh":str(data.get("gioi_tinh", "Nam")).strip() or "Nam",
        "lop":      str(data.get("lop", "")).strip(),
        "sdt":      str(data.get("sdt", "")).strip(),
        "diem_cc":  0.0,
        "diem_gk":  0.0,
        "diem_ck":  0.0,
        "diem_rl":  0.0,
    }

    df_new = pd.DataFrame([row])
    df = pd.concat([df, df_new], ignore_index=True)
    luu_danh_sach(df)
    logger.info(f"Đã thêm: {row['ho_ten']} ({msv_moi})")
    return df, True, f"Thêm SV thành công: {msv_moi}"


def sua_sinh_vien(df, old_msv, data):
    """
    Cập nhật thông tin sinh viên đã tồn tại.

    Args:
        df (pandas.DataFrame): Bảng dữ liệu hiện tại.
        old_msv (str): Mã sinh viên cũ cần sửa.
        data (dict): Thông tin mới của sinh viên.

    Returns:
        tuple: (DataFrame mới, bool Trạng thái, str Thông báo)
    """
    df = _ensure_base_columns(df)
    old_msv_norm = _normalize_msv(old_msv)
    idx = df.index[df["msv"].fillna("").astype(str).str.strip().str.upper() == old_msv_norm]
    if len(idx) == 0:
        return df, False, "Không tìm thấy mã sinh viên!"

    new_msv = _normalize_msv(data.get("msv", ""))
    if not new_msv:
        return df, False, "Mã sinh viên không được để trống!"

    other_msvs = df["msv"].fillna("").astype(str).str.strip().str.upper()
    if new_msv != old_msv_norm and new_msv in other_msvs.drop(index=idx).values:
        return df, False, "Mã sinh viên mới đã tồn tại!"

    df.loc[idx, "msv"]       = new_msv
    df.loc[idx, "ho_ten"]    = str(data.get("ho_ten", "")).strip()
    df.loc[idx, "gioi_tinh"] = str(data.get("gioi_tinh", "Nam")).strip() or "Nam"
    df.loc[idx, "lop"]       = str(data.get("lop", "")).strip()
    df.loc[idx, "sdt"]       = str(data.get("sdt", "")).strip()
    luu_danh_sach(df)
    logger.info(f"Đã sửa SV: {old_msv} -> {new_msv}")
    return df, True, f"Sửa SV thành công: {new_msv}"


def xoa_sinh_vien(df, msv):
    """
    Xóa sinh viên khỏi danh sách.

    Args:
        df (pandas.DataFrame): Bảng dữ liệu hiện tại.
        msv (str): Mã sinh viên cần xóa.

    Returns:
        tuple: (DataFrame mới, bool Trạng thái, str Thông báo)
    """
    df = _ensure_base_columns(df)
    msv_norm = _normalize_msv(msv)
    idx = df.index[df["msv"].fillna("").astype(str).str.strip().str.upper() == msv_norm]
    if len(idx) == 0:
        return df, False, "Không tìm thấy mã sinh viên!"

    df = df.drop(idx)
    luu_danh_sach(df)
    return df, True, "Xóa thành công!"


def xoa_nhieu_sinh_vien(df, msv_list):
    """
    Xóa nhiều sinh viên cùng lúc dựa trên danh sách msv.

    Args:
        df (pandas.DataFrame): Bảng dữ liệu hiện tại.
        msv_list (list): Danh sách các mã sinh viên cần xóa.

    Returns:
        tuple: (DataFrame mới, bool Trạng thái, str Thông báo)
    """
    df = _ensure_base_columns(df)
    if not msv_list:
        return df, False, "Danh sách trống!"

    normalized_to_delete = {_normalize_msv(item) for item in msv_list}
    normalized_msvs = df["msv"].fillna("").astype(str).str.strip().str.upper()
    df = df[~normalized_msvs.isin(normalized_to_delete)]
    luu_danh_sach(df)
    return df, True, f"Đã xóa {len(msv_list)} sinh viên!"


def cap_nhat_diem(df, msv, ten_cot, gia_tri):
    """
    Cập nhật điểm số cho 1 sinh viên theo tên cột.

    Args:
        df (pandas.DataFrame): Bảng dữ liệu hiện tại.
        msv (str): Mã sinh viên.
        ten_cot (str): Tên cột điểm ('diem_cc', 'diem_gk', 'diem_ck', 'diem_rl').
        gia_tri (float): Giá trị điểm mới.

    Returns:
        tuple: (DataFrame mới, bool Trạng thái)
    """
    df = _ensure_base_columns(df)
    if ten_cot not in df.columns:
        df[ten_cot] = 0.0

    msv_norm = _normalize_msv(msv)
    idx = df.index[df["msv"].fillna("").astype(str).str.strip().str.upper() == msv_norm]
    if len(idx) == 0:
        return df, False

    df.loc[idx, ten_cot] = gia_tri
    luu_danh_sach(df)
    return df, True


def thong_ke(df):
    """
    Trích xuất dữ liệu để tạo Dict thống kê cho UI.

    Args:
        df (pandas.DataFrame): Bảng dữ liệu hiện tại (đã có cột tính toán).

    Returns:
        dict: Chứa các trường thống kê.
    """
    if df.empty:
        return {}

    stats = {
        "tong_sv":   len(df),
        "du_hb":     int(np.sum(df["du_hb"] == "✅ Có")) if "du_hb" in df.columns else 0,
        "diem_tb_tb":float(np.mean(df["diem_tb"])) if "diem_tb" in df.columns else 0.0,
        "nam":       int(np.sum(df["gioi_tinh"].str.strip().str.lower() == "nam")),
        "nu":        int(np.sum(df["gioi_tinh"].str.strip().str.lower() == "nữ")),
        "xuat_sac":  int(np.sum(df["xep_loai"] == "Xuất sắc")) if "xep_loai" in df.columns else 0,
        "gioi":      int(np.sum(df["xep_loai"] == "Giỏi"))      if "xep_loai" in df.columns else 0,
    }
    return stats
