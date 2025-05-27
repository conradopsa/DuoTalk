import unittest
import sys
import os

# Add the src directory to the path to import the splitter module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from splitter import split_text_advanced

class TestSplitTextAdvanced(unittest.TestCase):
    def test_empty(self):
        result = split_text_advanced("")
        self.assertEqual(result, [])
        
    def test_hi(self):
        text = "Hi"  # 2 characters, below min_chunk_size=3
        result = split_text_advanced(text)
        self.assertEqual(result, ["Hi"])

    def test_phrase(self):
        text = """
        Good morning and welcome to the Black Mesa Transit System. 
        """
        # """
        # This automated train is provided for the security and convenience of employees of the Black Mesa Research Facility personnel. 
        # Please feel free to move about the train or simply sit back and enjoy the ride.
        # """
        result = split_text_advanced(text)
        self.assertEqual(result, ["Good morning and welcome to", "the Black Mesa Transit System"])
    
    # def test_abreviation(self):
    #     text = """
    #     Sorry, Mr. Freeman 
    #     """
    #     result = split_text_advanced(text)
    #     self.assertEqual(result, ["Sorry, Mr. Freeman, I’ve got explicit orders not to", "let you through without your hazard suit on"])

    def test_negative_sentence(self):
        text = """
        Sorry, Mister Freeman, I’ve got explicit orders not to let you through without your hazard suit on.
        """
        result = split_text_advanced(text)
        self.assertEqual(result, ["Sorry, Mister Freeman, I’ve got explicit orders not to", "let you through without your hazard suit on"])
