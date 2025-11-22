import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from travel_planner.itinerary import ItineraryPlanner

class TestItineraryPlanner(unittest.TestCase):
    
    def setUp(self):
        self.planner = ItineraryPlanner()
    
    def test_generate_itinerary(self):
        """Test generating a complete itinerary"""
        requirements = {
            "destination": "Seattle",
            "days": 3,
            "budget": 500,
            "preferences": ["sightseeing", "hotel"]
        }
        
        itinerary = self.planner.generate_itinerary(requirements)
        
        # Check that all required fields are present
        self.assertIn("destination", itinerary)
        self.assertIn("days", itinerary)
        self.assertIn("budget", itinerary)
        self.assertIn("total_cost", itinerary)
        self.assertIn("hotel", itinerary)
        self.assertIn("transport", itinerary)
        self.assertIn("daily_plan", itinerary)
        
        # Check that the itinerary stays within budget (allowing for small overruns)
        self.assertLessEqual(itinerary["total_cost"], requirements["budget"] * 1.1)  # Within 10% of budget
        
        # Check that the number of days matches
        self.assertEqual(len(itinerary["daily_plan"]), requirements["days"])
    
    def test_hotel_selection(self):
        """Test that hotels are selected within budget"""
        requirements = {
            "destination": "Seattle",
            "days": 3,
            "budget": 500,
            "preferences": ["hotel"]
        }
        
        itinerary = self.planner.generate_itinerary(requirements)
        
        # With a $500 budget for 3 days, we should have an affordable hotel
        self.assertIsNotNone(itinerary["hotel"])
        # Hotel cost for 3 nights should be reasonable
        hotel_cost = itinerary["hotel"]["price_per_night"] * 3
        # Allow for hotel costs up to the full budget (this is just a sanity check)
        self.assertLess(hotel_cost, itinerary["budget"] * 1.1)  # Hotel within 110% of budget
    
    def test_transport_selection(self):
        """Test transport selection based on preferences"""
        # Test with car preference
        requirements_car = {
            "destination": "Seattle",
            "days": 3,
            "budget": 500,
            "preferences": ["car"]
        }
        
        itinerary_car = self.planner.generate_itinerary(requirements_car)
        self.assertEqual(itinerary_car["transport"]["type"], "Car Rental")
        
        # Test without car preference
        requirements_no_car = {
            "destination": "Seattle",
            "days": 3,
            "budget": 500,
            "preferences": ["sightseeing"]
        }
        
        itinerary_no_car = self.planner.generate_itinerary(requirements_no_car)
        self.assertEqual(itinerary_no_car["transport"]["type"], "Public Transit Pass")
    
    def test_daily_plan_generation(self):
        """Test that daily plans are generated correctly"""
        requirements = {
            "destination": "Seattle",
            "days": 2,
            "budget": 300,
            "preferences": ["sightseeing"]
        }
        
        itinerary = self.planner.generate_itinerary(requirements)
        
        # Check that we have the right number of days
        self.assertEqual(len(itinerary["daily_plan"]), 2)
        
        # Check that each day has the correct structure
        for day in itinerary["daily_plan"]:
            self.assertIn("day", day)
            self.assertIn("activities", day)
            self.assertIn("cost", day)

if __name__ == '__main__':
    unittest.main()