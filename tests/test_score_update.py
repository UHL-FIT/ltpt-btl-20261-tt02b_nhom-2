import os
import tempfile
import unittest

import pandas as pd

from models import tinhhocbong as diemdanh


class ScoreUpdateTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_file = diemdanh.FILE_HOCBONG
        diemdanh.FILE_HOCBONG = os.path.join(self.temp_dir.name, "hocbong.csv")
        diemdanh.khoi_tao_csv()

    def tearDown(self):
        diemdanh.FILE_HOCBONG = self.original_file
        self.temp_dir.cleanup()

    def test_cap_nhat_diem_works_with_normalized_msv(self):
        df, ok, msg = diemdanh.them_sinh_vien(
            pd.DataFrame(),
            {"msv": "sv001", "ho_ten": "Test", "gioi_tinh": "Nam", "lop": "A", "sdt": "1"},
        )

        self.assertTrue(ok, msg)

        updated_df, updated_ok = diemdanh.cap_nhat_diem(df, " sv001 ", "diem_cc", 8.5)

        self.assertTrue(updated_ok)
        updated_value = float(updated_df.loc[updated_df["msv"] == "SV001", "diem_cc"].iloc[0])
        self.assertEqual(updated_value, 8.5)


if __name__ == "__main__":
    unittest.main()
