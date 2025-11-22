import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from travel_planner.pdf_generator import ItineraryPDFGenerator
import os

class TestItineraryPDFGenerator(unittest.TestCase):
    
    def setUp(self):
        self.generator = ItineraryPDFGenerator()
        self.test_filename = "test_itinerary.pdf"
    
    def tearDown(self):
        # Clean up test file if it was created
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)
    
    def test_generate_pdf(self):
        """Test generating a PDF itinerary"""
        # Sample itinerary data
        sample_itinerary = {
            "destination": "Seattle",
            "days": 3,
            "budget": 500,
            "total_cost": 425.50,
            "hotel": {
                "name": "Grand Hyatt Seattle",
                "price_per_night": 189,
                "rating": 4.5
            },
            "transport": {
                "type": "Public Transit Pass",
                "price_per_day": 10
            },
            "daily_plan": [
                {
                    "day": 1,
                    "activities": [
                        {"name": "Space Needle", "price": 35, "duration_hours": 3, "rating": 4.6},
                        {"name": "Pike Place Market", "price": 0, "duration_hours": 2, "rating": 4.7}
                    ],
                    "cost": 35
                },
                {
                    "day": 2,
                    "activities": [
                        {"name": "Seattle Aquarium", "price": 28, "duration_hours": 2.5, "rating": 4.4},
                        {"name": "Museum of Pop Culture", "price": 25, "duration_hours": 3, "rating": 4.5}
                    ],
                    "cost": 53
                },
                {
                    "day": 3,
                    "activities": [
                        {"name": "Seattle Great Wheel", "price": 15, "duration_hours": 1.5, "rating": 4.2}
                    ],
                    "cost": 15
                }
            ]
        }
        
        # Generate PDF
        pdf_path = self.generator.generate_pdf(sample_itinerary, self.test_filename)
        
        # Check that file was created
        self.assertTrue(os.path.exists(pdf_path))
        self.assertEqual(pdf_path, self.test_filename)
        
        # Check that file is not empty
        self.assertGreater(os.path.getsize(pdf_path), 0)

if __name__ == '__main__':
    unittest.main()