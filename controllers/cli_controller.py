"""
controllers/cli_controller.py
=============================
Controller điều phối luồng xử lý cho giao diện CLI.
Kết nối giữa cli_view và mô hình dữ liệu (models/tinhhocbong.py).
"""

import sys
from views import cli_view
from models import tinhhocbong as diemdanh
from utils.logger import setup_logger

logger = setup_logger()


def _xem_danh_sach():
    """Lấy danh sách từ models và gửi sang views để in ra màn hình."""
    logger.info("CLI: Người dùng xem danh sách.")
    df, ok = diemdanh.lay_danh_sach()
    if ok:
        cli_view.hien_bang_hocbong(df)
    else:
        cli_view.thong_bao("❌ Lỗi khi đọc dữ liệu.")


def _them_sinh_vien():
    """Điều phối luồng nhập liệu từ views và lưu vào models."""
    logger.info("CLI: Người dùng chọn chức năng Thêm sinh viên.")
    df, ok = diemdanh.lay_danh_sach()
    data = cli_view.nhap_thong_tin_sv()
    if data:
        _, ok_them, msg = diemdanh.them_sinh_vien(df, data)
        cli_view.thong_bao(f"✅ {msg}" if ok_them else f"❌ {msg}")


def _sua_sinh_vien():
    """Điều phối luồng tìm kiếm sinh viên cũ và cập nhật thông tin mới."""
    logger.info("CLI: Người dùng chọn chức năng Sửa sinh viên.")
    df, ok = diemdanh.lay_danh_sach()
    msv = cli_view.nhap_msv()
    if not msv:
        return
    data = cli_view.nhap_thong_tin_sv(current_msv=msv)
    if data:
        _, ok_sua, msg = diemdanh.sua_sinh_vien(df, msv, data)
        cli_view.thong_bao(f"✅ {msg}" if ok_sua else f"❌ {msg}")


def _xoa_sinh_vien():
    """Xóa sinh viên sau khi yêu cầu xác nhận từ CLI View."""
    logger.info("CLI: Người dùng chọn chức năng Xóa sinh viên.")
    df, ok = diemdanh.lay_danh_sach()
    msv = cli_view.nhap_msv()
    if not msv:
        return
    if cli_view.xac_nhan(f"Bạn có chắc muốn xóa MSV {msv}?"):
        _, ok_xoa, msg = diemdanh.xoa_sinh_vien(df, msv)
        cli_view.thong_bao(f"✅ {msg}" if ok_xoa else f"❌ {msg}")


def _nhap_diem():
    """Nhập điểm CC, GK, CK, RL cho một sinh viên."""
    logger.info("CLI: Người dùng chọn chức năng Nhập Điểm.")
    df, ok = diemdanh.lay_danh_sach()
    if not ok or df.empty:
        cli_view.thong_bao("❌ Chưa có sinh viên nào trong danh sách!")
        return

    msv = cli_view.nhap_msv()
    if not msv:
        return

    if msv not in df["msv"].values:
        cli_view.thong_bao(f"❌ Không tìm thấy MSV: {msv}")
        return

    scores = cli_view.nhap_diem_sinh_vien()
    if scores:
        for col, val in scores.items():
            df, ok_update = diemdanh.cap_nhat_diem(df, msv, col, val)
        cli_view.thong_bao("✅ Cập nhật điểm thành công!")


def _thong_ke():
    """Tính toán dữ liệu thống kê từ models và gửi in ra views."""
    logger.info("CLI: Người dùng xem thống kê.")
    df, ok = diemdanh.lay_danh_sach()
    if ok:
        stats = diemdanh.thong_ke(df)
        cli_view.hien_thong_ke(stats)
    else:
        cli_view.thong_bao("❌ Lỗi khi đọc dữ liệu.")


def chay_ung_dung():
    """Khởi chạy ứng dụng xét học bổng trên CLI."""
    logger.info("Khởi động ứng dụng ScholarScore (CLI)")
    try:
        while True:
            lua_chon = cli_view.hien_menu_chinh()

            if lua_chon == "1":
                _xem_danh_sach()
            elif lua_chon == "2":
                _them_sinh_vien()
            elif lua_chon == "3":
                _sua_sinh_vien()
            elif lua_chon == "4":
                _xoa_sinh_vien()
            elif lua_chon == "5":
                _nhap_diem()
            elif lua_chon == "6":
                _thong_ke()
            elif lua_chon == "0":
                print("\n  Cảm ơn bạn đã sử dụng ScholarScore!")
                logger.info("Người dùng thoát chương trình.")
                break
            else:
                cli_view.thong_bao("❌ Lựa chọn không hợp lệ, vui lòng thử lại!")
    except KeyboardInterrupt:
        print("\n\n  Thoát chương trình đột ngột (Ctrl+C).")
        logger.warning("Thoát đột ngột do KeyboardInterrupt.")
        sys.exit(0)
    except Exception as e:
        cli_view.thong_bao(f"❌ Có lỗi bất ngờ xảy ra: {e}")
        logger.error(f"Ngoại lệ chưa bắt: {e}", exc_info=True)
