from typing import Dict, List
import random
from .api.mock_services import MockHotelService, MockAttractionService, MockTransportService

class ItineraryPlanner:
    """Generates travel itineraries based on user requirements"""
    
    def __init__(self):
        self.hotel_service = MockHotelService()
        self.attraction_service = MockAttractionService()
        self.transport_service = MockTransportService()
    
    def generate_itinerary(self, requirements: Dict) -> Dict:
        """
        Generate a complete travel itinerary
        
        Args:
            requirements (dict): Parsed travel requirements
            
        Returns:
            dict: Complete travel itinerary
        """
        destination = requirements["destination"]
        days = requirements["days"]
        budget = requirements["budget"]
        preferences = requirements["preferences"]
        
        # Get available options
        hotels = self.hotel_service.get_hotels(destination, budget)
        attractions = self.attraction_service.get_attractions(destination)
        transport_options = self.transport_service.get_transport_options()
        
        # Select hotel (first affordable option or None)
        selected_hotel = hotels[0] if hotels else None
        
        # Select transport (based on preferences or default)
        if "car" in preferences:
            selected_transport = transport_options["car_rental"]
        else:
            selected_transport = transport_options["public_transit"]
        
        # Plan daily activities
        daily_plan = self._plan_daily_activities(
            days, attractions, budget, selected_hotel, selected_transport
        )
        
        # Calculate total cost
        total_cost = self._calculate_total_cost(days, selected_hotel, selected_transport, daily_plan)
        
        # Adjust if over budget
        if total_cost > budget:
            daily_plan, total_cost = self._adjust_for_budget(
                daily_plan, total_cost, budget, selected_hotel, selected_transport
            )
        
        return {
            "destination": destination,
            "days": days,
            "budget": budget,
            "total_cost": total_cost,
            "hotel": selected_hotel,
            "transport": selected_transport,
            "daily_plan": daily_plan
        }
    
    def _plan_daily_activities(self, days: int, attractions: List[Dict], 
                              budget: float, hotel: Dict | None, transport: Dict) -> List[Dict]:
        """Plan activities for each day"""
        daily_plan = []
        
        # Sort attractions by rating (highest first)
        sorted_attractions = sorted(attractions, key=lambda x: x["rating"], reverse=True)
        
        remaining_budget = budget
        if hotel:
            remaining_budget -= hotel["price_per_night"] * days
        remaining_budget -= transport["price_per_day"] * days
        
        # Distribute attractions across days
        attractions_per_day = max(1, len(sorted_attractions) // days)
        
        for day in range(1, days + 1):
            day_activities = []
            day_budget = remaining_budget / (days - day + 1) if days - day + 1 > 0 else remaining_budget
            
            # Select attractions for the day
            attractions_for_day = []
            current_day_cost = 0
            
            for attr in sorted_attractions:
                if len(attractions_for_day) >= attractions_per_day:
                    break
                if current_day_cost + attr["price"] <= day_budget and attr not in [item for day_plan in daily_plan for item in day_plan.get("activities", [])]:
                    attractions_for_day.append(attr)
                    current_day_cost += attr["price"]
            
            daily_plan.append({
                "day": day,
                "activities": attractions_for_day,
                "cost": current_day_cost
            })
            
            remaining_budget -= current_day_cost
        
        return daily_plan
    
    def _calculate_total_cost(self, days: int, hotel: Dict | None, transport: Dict, 
                             daily_plan: List[Dict]) -> float:
        """Calculate total cost of the trip"""
        total = 0
        
        # Hotel cost
        if hotel:
            total += hotel["price_per_night"] * days
        
        # Transport cost
        total += transport["price_per_day"] * days
        
        # Daily activities cost
        for day in daily_plan:
            total += day["cost"]
        
        return round(total, 2)
    
    def _adjust_for_budget(self, daily_plan: List[Dict], current_cost: float, 
                          budget: float, hotel: Dict | None, transport: Dict) -> tuple:
        """Adjust itinerary to fit within budget"""
        # Calculate how much we need to reduce
        excess_amount = current_cost - budget
        
        # Try to reduce activities first
        adjusted_plan = []
        total_reduction = 0
        
        for day in daily_plan:
            adjusted_activities = day["activities"].copy()
            adjusted_cost = day["cost"]
            
            # Remove most expensive activities first if we need to reduce costs
            if excess_amount > total_reduction:
                # Sort activities by price (most expensive first)
                adjusted_activities.sort(key=lambda x: x["price"], reverse=True)
                
                # Remove activities until we're within budget or no more activities to remove
                while adjusted_activities and excess_amount > total_reduction:
                    # Don't remove all activities
                    if len(adjusted_activities) <= 1:
                        break
                        
                    # Remove the most expensive activity
                    removed_activity = adjusted_activities.pop(0)
                    adjusted_cost -= removed_activity["price"]
                    total_reduction += removed_activity["price"]
            
            adjusted_plan.append({
                "day": day["day"],
                "activities": adjusted_activities,
                "cost": adjusted_cost
            })
        
        adjusted_total = self._calculate_total_cost(len(daily_plan), hotel, transport, adjusted_plan)
        
        # If still over budget, try to select a cheaper hotel
        if adjusted_total > budget and hotel:
            # This is a simplified approach - in a real implementation, we might
            # search for cheaper hotel options
            pass
        
        return adjusted_plan, adjusted_total


# Example usage
if __name__ == "__main__":
    planner = ItineraryPlanner()
    sample_requirements = {
        "destination": "Seattle",
        "days": 3,
        "budget": 500,
        "preferences": ["sightseeing", "hotel"]
    }
    itinerary = planner.generate_itinerary(sample_requirements)
    print(itinerary)