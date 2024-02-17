import unittest
import func

class TestStringMethods(unittest.TestCase):

    def test_convert_to_alphabet5(self):
        result = func.convert_to_alphabet(5)
        self.assertEqual(result, ['A', 'B', 'C', 'D', 'E'])

    def test_convert_to_alphabet30(self):
        result = func.convert_to_alphabet(30)
        self.assertEqual(result, ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD'])

    def test_open1(self):
        picross = {
            "row": {
                "length": 5,
                "setting": [
                    [1,1],
                    [1,1],
                    [1],
                    [1,1],
                    [1,1]
                ]
            },
            "column": {
                "length": 5,
                "setting": [
                    [0],
                    [2,2],
                    [0],
                    [0],
                    [5]
                ]
            }
        expect_df = 
}


if __name__ == '__main__':
    unittest.main()