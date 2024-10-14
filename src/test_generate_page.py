import unittest
from generate_page import extract_title

class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        title1 = "# hello"
        self.assertEqual(extract_title(title1), "hello")

        title2 = "#   hello"
        self.assertEqual(extract_title(title2), "hello")
    


if __name__ == "__main__":
    unittest.main()