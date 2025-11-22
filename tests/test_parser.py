import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from travel_planner.parser import TravelInputParser

class TestTravelInputParser(unittest.TestCase):
    
    def setUp(self):
        self.parser = TravelInputParser()
    
    def test_parse_complete_request(self):
        """Test parsing a complete travel request"""
        input_text = "Plan a 3-day Seattle trip under $500 with sightseeing and hotel."
        result = self.parser.parse(input_text)
        
        self.assertEqual(result["destination"], "Seattle")
        self.assertEqual(result["days"], 3)
        self.assertEqual(result["budget"], 500.0)
        self.assertIn("sightseeing", result["preferences"])
        self.assertIn("hotel", result["preferences"])
    
    def test_parse_various_formats(self):
        """Test parsing different input formats"""
        test_cases = [
            ("I want to visit New York for 5 days with a budget of $800", "New York", 5, 800.0),
            ("5-day trip to San Francisco under $1000", "San Francisco", 5, 1000.0),
            ("Plan a trip to Paris for 7 days with $1200 budget", "Paris", 7, 1200.0)
        ]
        
        for input_text, expected_city, expected_days, expected_budget in test_cases:
            with self.subTest(input_text=input_text):
                result = self.parser.parse(input_text)
                self.assertEqual(result["destination"], expected_city)
                self.assertEqual(result["days"], expected_days)
                self.assertEqual(result["budget"], expected_budget)
    
    def test_extract_city(self):
        """Test city extraction specifically"""
        self.assertEqual(self.parser._extract_city("Plan a trip to Seattle"), "Seattle")
        self.assertEqual(self.parser._extract_city("3-day trip in New York"), "New York")
        self.assertEqual(self.parser._extract_city("Visit San Francisco for 5 days"), "San Francisco")
    
    def test_extract_days(self):
        """Test days extraction specifically"""
        self.assertEqual(self.parser._extract_days("Plan a 3-day trip"), 3)
        self.assertEqual(self.parser._extract_days("5 day trip to Seattle"), 5)
        self.assertEqual(self.parser._extract_days("Trip for 7 days in Paris"), 7)
    
    def test_extract_budget(self):
        """Test budget extraction specifically"""
        self.assertEqual(self.parser._extract_budget("Trip under $500"), 500.0)
        self.assertEqual(self.parser._extract_budget("Budget of $1000 for the trip"), 1000.0)
        self.assertEqual(self.parser._extract_budget("Plan trip with $750 budget"), 750.0)
    
    def test_extract_preferences(self):
        """Test preference extraction specifically"""
        result = self.parser._extract_preferences("Trip with sightseeing and hotel")
        self.assertIn("sightseeing", result)
        self.assertIn("hotel", result)
        
        result = self.parser._extract_preferences("Need car rental and attractions")
        self.assertIn("car", result)
        self.assertIn("sightseeing", result)

if __name__ == '__main__':
    unittest.main()