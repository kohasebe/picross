import unittest
from pandas.testing import assert_frame_equal
import pandas as pd
import config
import func

class TestClass(unittest.TestCase):
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

    def test_get_line_serialize(self):
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
        actual = func.get_line_serialize(df[0])
        self.assertEqual(actual, expect_column0)

        actual = func.get_line_serialize(df.iloc[0])
        self.assertEqual(actual, expect_row0)

        actual = func.get_line_serialize(df.iloc[1])
        self.assertEqual(actual, expect_row1)

    def test_create_line(self):
        expected_line = [
            config.empty,
            config.blank,
            config.blank,
            config.open,
            config.open,
            config.open,
            config.open
        ]
        status = [
            config.empty + ":1",
            config.blank + ":2",
            config.open + ":3",
            config.open + ":1"
        ]
        actual_line = func.create_line(status)
        self.assertEqual(actual_line, expected_line)

    # カンマ区切りで差し込むロジックは使わなくなりそうなので一旦コメントアウト
    # def test_create_line2(self):
    #     expected_line = [
    #         config.empty,
    #         config.blank,
    #         config.blank,
    #         config.open,
    #         config.open,
    #         config.open,
    #         config.open
    #     ]
    #     status = [
    #         config.empty + ":1",
    #         config.blank + ":2",
    #         config.open + ":3," + config.open + ":1",
    #     ]
    #     actual_line = func.create_line(status)
    #     self.assertEqual(actual_line, expected_line)

    def test_update_line_serialize(self):
        expected_line_serialize = [
            config.open + ":1",
            config.blank + ":2",
            config.open + ":1",
            config.empty + ":2",
            config.blank + ":2",
        ]

        line_serialize = [
            config.open + ":1",
            config.blank + ":2",
            config.empty + ":3",
            config.blank + ":2",
        ]

        actual_line = func.update_line_serialize(line_serialize, 2, [
            func.create_line_serialize(config.open, 1),
            func.create_line_serialize(config.empty, 2),
        ])

        self.assertEqual(actual_line, expected_line_serialize)

    # 開始時点
    def test_check_continue_start(self):
        data = {
            0: [e, e],
            1: [e, e],
        }
        df = pd.DataFrame(data).transpose()

        config.picross = {
            "length": 2,
            "row": {
                "setting": [
                    [1],
                    [2],
                ]
            },
            "column": {
                "setting": [
                    [2],[1]
                ]
            }
        }

        self.assertTrue(func.check_continue(df))

    # 開いてる数が足りない
    def test_check_continue_true(self):
        data = {
            0: [e, e, o, e, e],
            1: [e, o, e, e, o],
        }
        df = pd.DataFrame(data).transpose()

        config.picross = {
            "length": 5,
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

        self.assertTrue(func.check_continue(df))

    # 全要素が埋まった時
    def test_check_continue_false(self):
        data = {
            0: [e, e, o, e, e],
            1: [o, o, e, e, o],
        }
        df = pd.DataFrame(data).transpose()

        config.picross = {
            "length": 5,
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

        self.assertFalse(func.check_continue(df))

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

        actual_df = pd.DataFrame(empty_data_5x5).transpose()
        func.main_logic(actual_df, "open1")

        assert_frame_equal(actual_df, expected_df)

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

        actual_df = pd.DataFrame(empty_data_5x5).transpose()
        func.main_logic(actual_df, "open1")

        assert_frame_equal(actual_df, expected_df)

    def test_open1_all(self):
        expected_data = {
            0: [o, o, o, o, o],
            1: [e, e, e, e, e],
            2: [e, e, e, e, e],
            3: [e, e, e, e, e],
            4: [o, o, o, o, o]
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
                    [5]
                ]
            },
            "column": {
                "setting": [
                    [2], [2], [2], [2], [2]
                ]
            }
        }

        actual_df = pd.DataFrame(empty_data_5x5).transpose()

        func.main_logic(actual_df, "open1")

        assert_frame_equal(actual_df, expected_df)

    def test_open2_column(self):
        expected_data = {
            0: [o, e, e, e, e],
            1: [x, e, e, e, e],
            2: [o, e, e, e, e],
            3: [x, e, e, e, e],
            4: [o, e, e, e, e]
        }
        expected_df = pd.DataFrame(expected_data).transpose()

        config.picross = {
            "length": 5,
            "row": {
                "setting": [
                    [1],
                    [0],
                    [1],
                    [0],
                    [1]
                ]
            },
            "column": {
                "setting": [
                    [1,1,1], [0], [0], [0], [0]
                ]
            }
        }

        actual_df = pd.DataFrame(empty_data_5x5)

        func.main_logic(actual_df, "open2")

        assert_frame_equal(actual_df, expected_df)

    def test_open2_row(self):
        expected_data = {
            0: [o, o, o, x, o],
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
                    [3,1],
                    [0],
                    [0],
                    [0],
                    [0]
                ]
            },
            "column": {
                "setting": [
                    [1], [1], [1], [0], [1]
                ]
            }
        }

        actual_df = pd.DataFrame(empty_data_5x5).transpose()

        func.main_logic(actual_df, "open2")

        assert_frame_equal(actual_df, expected_df)

    def test_open3_column(self):
        expected_data = {
            0: [o, x, o, o, o],
            1: [x, o, o, x, x],
            2: [o, o, o, x, x],
            3: [x, x, x, x, x],
            4: [o, o, o, o, x]
        }
        expected_df = pd.DataFrame(expected_data).transpose()

        config.picross = {
            "length": 5,
            "row": {
                "setting": [
                    [1,3],
                    [2],
                    [3],
                    [0],
                    [4]
                ]
            },
            "column": {
                "setting": [
                    [1,1,1], [2,1], [3,1], [1,1], [1]
                ]
            }
        }

        initial_data = {
            0: [e, x, e, e, e],
            1: [x, e, e, x, x],
            2: [e, e, e, x, x],
            3: [x, x, x, x, x],
            4: [e, e, e, e, x]
        }

        actual_df = pd.DataFrame(initial_data).transpose()
        func.main_logic(actual_df, "open3")

        assert_frame_equal(actual_df, expected_df)

    def test_open3_row(self):
        expected_data = {
            0: [x, o, o, x, o],
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
                    [2,1],
                    [0],
                    [0],
                    [0],
                    [0]
                ]
            },
            "column": {
                "setting": [
                    [0], [1], [1], [0], [1]
                ]
            }
        }

        initial_data = {
            0: [x, o, e, x, e],
            1: [e, e, e, e, e],
            2: [e, e, e, e, e],
            3: [e, e, e, e, e],
            4: [e, e, e, e, e]
        }

        actual_df = pd.DataFrame(initial_data).transpose()
        func.main_logic(actual_df, "open3")

        assert_frame_equal(actual_df, expected_df)

    def test_open4(self):
        expected_data = {
            0: [o, o, x, x, x],
            1: [o, x, x, x, x],
            2: [x, x, x, x, x],
            3: [x, x, x, x, x],
            4: [x, x, x, x, x]
        }
        expected_df = pd.DataFrame(expected_data).transpose()

        config.picross = {
            "length": 5,
            "row": {
                "setting": [
                    [2],
                    [1],
                    [0],
                    [0],
                    [0]
                ]
            },
            "column": {
                "setting": [
                    [2], [1], [0], [0], [0]
                ]
            }
        }

        initial_data = {
            0: [o, o, x, e, e],
            1: [o, e, e, e, e],
            2: [e, e, e, e, e],
            3: [x, e, e, e, e],
            4: [e, e, e, e, e]
        }

        actual_df = pd.DataFrame(initial_data).transpose()
        func.main_logic(actual_df, "open4")

        assert_frame_equal(actual_df, expected_df)

    def test_open5(self):
        expected_data = {
            0: [e, e, o, e, e],
            1: [o, e, e, e, e],
            2: [o, e, e, e, e],
            3: [o, e, e, e, e],
            4: [e, e, e, e, e]
        }
        expected_df = pd.DataFrame(expected_data).transpose()

        config.picross = {
            "length": 5,
            "row": {
                "setting": [
                    [3],
                    [1],
                    [1],
                    [1],
                    [0]
                ]
            },
            "column": {
                "setting": [
                    [4], [1], [1], [0], [0]
                ]
            }
        }

        actual_df = pd.DataFrame(empty_data_5x5).transpose()

        func.main_logic(actual_df, "open5")

        assert_frame_equal(actual_df, expected_df)

    # 2 [e,e,e,e,e]のとき何もしない
    def test_open6_1(self):
        expected_data = {
            0: [e, e, e, e, e],
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
                    [2],
                    [0],
                    [0],
                    [0],
                    [0]
                ]
            },
            "column": {
                "setting": [
                    [1], [1], [0], [0], [0]
                ]
            }
        }

        actual_df = pd.DataFrame(empty_data_5x5).transpose()

        func.main_logic(actual_df, "open6")

        assert_frame_equal(actual_df, expected_df)    # 2 [e,e,x,e,e]のとき何もしない

    # 2 [e,e,x,e,e]のとき何もしない
    def test_open6_2(self):
        expected_data = {
            0: [e, e, x, e, e],
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
                    [2],
                    [0],
                    [0],
                    [0],
                    [0]
                ]
            },
            "column": {
                "setting": [
                    [1], [1], [0], [0], [0]
                ]
            }
        }

        initial_data = {
            0: [e, e, x, e, e],
            1: [e, e, e, e, e],
            2: [e, e, e, e, e],
            3: [e, e, e, e, e],
            4: [e, e, e, e, e]
        }

        actual_df = pd.DataFrame(initial_data).transpose()

        func.main_logic(actual_df, "open6")

        assert_frame_equal(actual_df, expected_df)

    # 3 [x,e,e,e,e]のとき[x,e,o,o,e]にする
    def test_open6_3(self):
        expected_data = {
            0: [x, e, o, o, e],
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
                    [3],
                    [0],
                    [0],
                    [0],
                    [0]
                ]
            },
            "column": {
                "setting": [
                    [0], [0], [1], [1], [1]
                ]
            }
        }

        initial_data = {
            0: [x, e, e, e, e],
            1: [e, e, e, e, e],
            2: [e, e, e, e, e],
            3: [e, e, e, e, e],
            4: [e, e, e, e, e]
        }

        actual_df = pd.DataFrame(initial_data).transpose()

        func.main_logic(actual_df, "open6")

        assert_frame_equal(actual_df, expected_df)

    # 1,2 [o,x,e,e,e]のとき[o,x,e,o,e]にする
    def test_open6_4(self):
        expected_data = {
            0: [o, x, e, o, e],
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
                    [1,2],
                    [0],
                    [0],
                    [0],
                    [0]
                ]
            },
            "column": {
                "setting": [
                    [1], [0], [0], [1], [1]
                ]
            }
        }

        initial_data = {
            0: [o, x, e, e, e],
            1: [e, e, e, e, e],
            2: [e, e, e, e, e],
            3: [e, e, e, e, e],
            4: [e, e, e, e, e]
        }

        actual_df = pd.DataFrame(initial_data).transpose()

        func.main_logic(actual_df, "open6")

        assert_frame_equal(actual_df, expected_df)

    # 1,1 [o,e,e,e,e]のとき[o,x,e,e,e]にする
    def test_open7_1(self):
        expected_data = {
            0: [o, x, e, e, e],
            1: [x, e, e, e, e],
            2: [e, e, e, e, e],
            3: [e, e, e, e, e],
            4: [e, e, e, e, e]
        }
        expected_df = pd.DataFrame(expected_data).transpose()

        config.picross = {
            "length": 5,
            "row": {
                "setting": [
                    [1,1],
                    [0],
                    [0],
                    [0],
                    [0]
                ]
            },
            "column": {
                "setting": [
                    [1], [0], [0], [1], [0]
                ]
            }
        }

        initial_data = {
            0: [o, e, e, e, e],
            1: [e, e, e, e, e],
            2: [e, e, e, e, e],
            3: [e, e, e, e, e],
            4: [e, e, e, e, e]
        }

        actual_df = pd.DataFrame(initial_data).transpose()

        func.main_logic(actual_df, "open7")

        assert_frame_equal(actual_df, expected_df)

    # 1,1 [e,e,e,e,o]のとき[e,e,e,x,o]にする
    def test_open7_2(self):
        expected_data = {
            0: [e, e, e, x, o],
            1: [e, e, e, e, x],
            2: [e, e, e, e, e],
            3: [e, e, e, e, e],
            4: [e, e, e, e, e]
        }
        expected_df = pd.DataFrame(expected_data).transpose()

        config.picross = {
            "length": 5,
            "row": {
                "setting": [
                    [1,1],
                    [0],
                    [0],
                    [0],
                    [0]
                ]
            },
            "column": {
                "setting": [
                    [1], [0], [0], [0], [1]
                ]
            }
        }

        initial_data = {
            0: [e, e, e, e, o],
            1: [e, e, e, e, e],
            2: [e, e, e, e, e],
            3: [e, e, e, e, e],
            4: [e, e, e, e, e]
        }

        actual_df = pd.DataFrame(initial_data).transpose()

        func.main_logic(actual_df, "open7")

        assert_frame_equal(actual_df, expected_df)

    # 1,1 [o,e,x,e,e]のとき[o,x,x,e,e]にする
    def test_open7_3(self):
        expected_data = {
            0: [o, x, x, e, e],
            1: [x, e, e, e, e],
            2: [e, e, e, e, e],
            3: [e, e, e, e, e],
            4: [e, e, e, e, e]
        }
        expected_df = pd.DataFrame(expected_data).transpose()

        config.picross = {
            "length": 5,
            "row": {
                "setting": [
                    [1,1],
                    [0],
                    [0],
                    [0],
                    [0]
                ]
            },
            "column": {
                "setting": [
                    [1], [0], [0], [0], [1]
                ]
            }
        }

        initial_data = {
            0: [o, e, x, e, e],
            1: [e, e, e, e, e],
            2: [e, e, e, e, e],
            3: [e, e, e, e, e],
            4: [e, e, e, e, e]
        }

        actual_df = pd.DataFrame(initial_data).transpose()

        func.main_logic(actual_df, "open7")

        assert_frame_equal(actual_df, expected_df)

if __name__ == '__main__':
    unittest.main()