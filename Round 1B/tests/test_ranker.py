import unittest
from src.document_intelligence import refine_text

class TestTextProcessing(unittest.TestCase):
    def test_refine_text_length(self):
        long_text = "word " * 200
        refined = refine_text(long_text)
        self.assertTrue(len(refined) <= 505)

if __name__ == '__main__':
    unittest.main()
