import unittest

class MyTestCase(unittest.TestCase):
    def setUp(self):
        # テストの前に実行される初期化処理
        self.foo = "bar"
        self.value = 10

    def test_something(self):
        # テストメソッド1
        self.assertEqual(self.foo, "bar")
        self.assertTrue(self.value == 10)
        self.foo = "baz"

    def test_another_thing(self):
        # テストメソッド2
        self.assertEqual(self.value, 10)
        self.assertFalse(self.foo == "baz")

if __name__ == "__main__":
    unittest.main()