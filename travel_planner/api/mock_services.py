import random
from typing import Dict, List

class MockHotelService:
    """Mock service for hotel data"""
    
    def __init__(self):
        self.hotels = {
            "Seattle": [
                {"name": "Grand Hyatt Seattle", "price_per_night": 189, "rating": 4.5},
                {"name": "MarQueen Hotel", "price_per_night": 159, "rating": 4.3},
                {"name": "Inn at El Gaucho", "price_per_night": 225, "rating": 4.7},
                {"name": "Silver Cloud Hotel", "price_per_night": 165, "rating": 4.2}
            ],
            "New York": [
                {"name": "Hilton Garden Inn", "price_per_night": 225, "rating": 4.4},
                {"name": "Marriott Downtown", "price_per_night": 295, "rating": 4.6},
                {"name": "Holiday Inn Express", "price_per_night": 185, "rating": 4.1}
            ],
            "San Francisco": [
                {"name": "Hotel Zetta", "price_per_night": 215, "rating": 4.3},
                {"name": "Hotel VIA", "price_per_night": 195, "rating": 4.2},
                {"name": "Clift Royal Sonesta", "price_per_night": 245, "rating": 4.5}
            ]
        }
    
    def get_hotels(self, city: str, budget: float) -> List[Dict]:
        """Get hotels within budget for a city"""
        city_hotels = self.hotels.get(city, [])
        affordable_hotels = [
            hotel for hotel in city_hotels 
            if hotel["price_per_night"] <= budget * 0.4  # Hotels shouldn't exceed 40% of budget
        ]
        return sorted(affordable_hotels, key=lambda x: x["price_per_night"])

class MockAttractionService:
    """Mock service for attraction data"""
    
    def __init__(self):
        self.attractions = {
            "Seattle": [
                {"name": "Space Needle", "price": 35, "duration_hours": 3, "rating": 4.6},
                {"name": "Pike Place Market", "price": 0, "duration_hours": 2, "rating": 4.7},
                {"name": "Seattle Aquarium", "price": 28, "duration_hours": 2.5, "rating": 4.4},
                {"name": "Museum of Pop Culture", "price": 25, "duration_hours": 3, "rating": 4.5},
                {"name": "Seattle Great Wheel", "price": 15, "duration_hours": 1.5, "rating": 4.2}
            ],
            "New York": [
                {"name": "Statue of Liberty", "price": 25, "duration_hours": 4, "rating": 4.7},
                {"name": "Central Park", "price": 0, "duration_hours": 3, "rating": 4.8},
                {"name": "Empire State Building", "price": 40, "duration_hours": 2, "rating": 4.5},
                {"name": "Metropolitan Museum", "price": 30, "duration_hours": 4, "rating": 4.6}
            ],
            "San Francisco": [
                {"name": "Golden Gate Bridge", "price": 0, "duration_hours": 3, "rating": 4.8},
                {"name": "Alcatraz Island", "price": 40, "duration_hours": 4, "rating": 4.7},
                {"name": "Fisherman's Wharf", "price": 0, "duration_hours": 2, "rating": 4.2},
                {"name": "Cable Car Ride", "price": 8, "duration_hours": 1, "rating": 4.3}
            ]
        }
    
    def get_attractions(self, city: str) -> List[Dict]:
        """Get attractions for a city"""
        return self.attractions.get(city, [])

class MockTransportService:
    """Mock service for transport data"""
    
    def __init__(self):
        self.transport_options = {
            "car_rental": {"price_per_day": 45, "type": "Car Rental"},
            "public_transit": {"price_per_day": 10, "type": "Public Transit Pass"}
        }
    
    def get_transport_options(self) -> Dict:
        """Get transport options"""
        return self.transport_options

# Example usage
if __name__ == "__main__":
    hotel_service = MockHotelService()
    attraction_service = MockAttractionService()
    transport_service = MockTransportService()
    
    # Test with Seattle
    hotels = hotel_service.get_hotels("Seattle", 500)
    attractions = attraction_service.get_attractions("Seattle")
    transport = transport_service.get_transport_options()
    
    print("Hotels:", hotels[:2])
    print("Attractions:", attractions[:2])
    print("Transport:", transport)