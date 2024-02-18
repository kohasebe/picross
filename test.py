import unittest
from pandas.testing import assert_frame_equal
import pandas as pd
import numpy as np
import config
import func

class TestStringMethods(unittest.TestCase):
    global e, x, o, empty_data_5x5
    e = config.empty
    x = config.blank
    o = config.open

    empty_data_5x5 = {
        0: [e, e, e, e, e],
        1: [e, e, e, e, e],
        2: [e, e, e, e, e],
        3: [e, e, e, e, e],
        4: [e, e, e, e, e]
    }

    def setUp(self):
        config.picross = {
            "row": {
                "setting": [
                    [0],
                    [0],
                    [0],
                    [0],
                    [0]
                ]
            },
            "column": {
                "setting": [
                    [0],[0],[0],[0],[0]
                ]
            }
        }

    def test_status(self):
        expect_column0 = [
            config.empty + ":1",
            config.open + ":1"
        ]
        expect_row0 = [
            config.empty + ":1",
            config.blank + ":2",
            config.empty + ":1",
            config.open + ":1"
        ]

        expect_row1 = [
            config.open + ":1",
            config.empty + ":3",
            config.open + ":1"
        ]

        data = {
            0: [e, x, x, e, o],
            1: [o, e, e, e, o],
        }
        df = pd.DataFrame(data).transpose()
        actual = func.status(df, 0, "column")
        self.assertEqual(actual, expect_column0)

        actual = func.status(df, 0, "row")
        self.assertEqual(actual, expect_row0)

        actual = func.status(df, 1, "row")
        self.assertEqual(actual, expect_row1)

    def test_end_check_true(self):
        data = {
            0: [e, e, o, e, e],
            1: [o, o, e, e, o],
        }
        df = pd.DataFrame(data).transpose()

        config.picross = {
            "row": {
                "setting": [
                    [1],
                    [2,1],
                ]
            },
            "column": {
                "setting": [
                    [1],[1],[1],[0],[1]
                ]
            }
        }

    # 全長と一致するラインを開けるテスト（列）
    def test_open1_column(self):
        expected_data = {
            0: [e, e, e, e, o],
            1: [e, e, e, e, o],
            2: [e, e, e, e, o],
            3: [e, e, e, e, o],
            4: [e, e, e, e, o]
        }
        expected_df = pd.DataFrame(expected_data).transpose()

        config.picross = {
            "length": 5,
            "row": {
                "setting": [
                    [1],
                    [1],
                    [1],
                    [1],
                    [1]
                ]
            },
            "column": {
                "setting": [
                    [0],[0],[0],[0],[5]
                ]
            }
        }

        actual_df = pd.DataFrame(empty_data_5x5)

        # line_types = ["column", "row"]
        # for line_type in line_types:
        #     setting = config.picross[line_type]["setting"]
        #     for i in range((len(setting))):
        #         if (line_type == "column"):
        #             actual_df[i] = func.open1(actual_df, i, setting)
        #         elif (line_type == "row"):
        #             actual_df.iloc[i] = func.open1(actual_df, i, setting)

        setting = config.picross["column"]["setting"]
        for i in range(len(setting)):
            actual_df[i] = func.open1(actual_df[i], setting[i])

        assert_frame_equal(actual_df, expected_df)

    # 全長と一致するラインを開けるテスト（行）
    def test_open1_row(self):
        expected_data = {
            0: [o, o, o, o, o],
            1: [e, e, e, e, e],
            2: [e, e, e, e, e],
            3: [e, e, e, e, e],
            4: [e, e, e, e, e]
        }
        expected_df = pd.DataFrame(expected_data).transpose()

        config.picross = {
            "length": 5,
            "row": {
                "setting": [
                    [5],
                    [0],
                    [0],
                    [0],
                    [0]
                ]
            },
            "column": {
                "setting": [
                    [1],[1],[1],[1],[1]
                ]
            }
        }

        actual_df = pd.DataFrame(empty_data_5x5)

        # line_types = ["column", "row"]
        # for line_type in line_types:
        #     setting = config.picross[line_type]["setting"]
        #     for i in range((len(setting))):
        #         if (line_type == "column"):
        #             actual_df[i] = func.open1(actual_df, i, setting)
        #         elif (line_type == "row"):
        #             actual_df.iloc[i] = func.open1(actual_df, i, setting)

        setting = config.picross["row"]["setting"]
        for i in range(len(setting)):
            actual_df.iloc[i] = func.open1(actual_df.iloc[i], setting[i])


if __name__ == '__main__':
    unittest.main()