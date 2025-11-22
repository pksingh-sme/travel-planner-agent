from fpdf import FPDF
from typing import Dict, List

class ItineraryPDFGenerator:
    """Generates PDF itineraries from travel data"""
    
    def __init__(self):
        pass
    
    def generate_pdf(self, itinerary: Dict, filename: str = "itinerary.pdf") -> str:
        """
        Generate a PDF itinerary
        
        Args:
            itinerary (dict): Travel itinerary data
            filename (str): Output filename
            
        Returns:
            str: Path to generated PDF file
        """
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        # Title
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Travel Itinerary", ln=True, align="C")
        pdf.ln(10)
        
        # Trip Summary
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Trip Summary", ln=True)
        pdf.set_font("Arial", "", 10)
        
        pdf.cell(0, 8, f"Destination: {itinerary['destination']}", ln=True)
        pdf.cell(0, 8, f"Duration: {itinerary['days']} days", ln=True)
        pdf.cell(0, 8, f"Budget: ${itinerary['budget']:.2f}", ln=True)
        pdf.cell(0, 8, f"Total Cost: ${itinerary['total_cost']:.2f}", ln=True)
        pdf.ln(5)
        
        # Hotel Information
        if itinerary["hotel"]:
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "Accommodation", ln=True)
            pdf.set_font("Arial", "", 10)
            pdf.cell(0, 8, f"Hotel: {itinerary['hotel']['name']}", ln=True)
            pdf.cell(0, 8, f"Price per night: ${itinerary['hotel']['price_per_night']}", ln=True)
            pdf.cell(0, 8, f"Rating: {itinerary['hotel']['rating']}/5", ln=True)
            pdf.ln(5)
        
        # Transportation
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Transportation", ln=True)
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 8, f"Type: {itinerary['transport']['type']}", ln=True)
        pdf.cell(0, 8, f"Price per day: ${itinerary['transport']['price_per_day']}", ln=True)
        pdf.ln(5)
        
        # Daily Plan
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Daily Plan", ln=True)
        pdf.ln(2)
        
        for day in itinerary["daily_plan"]:
            pdf.set_font("Arial", "B", 11)
            pdf.cell(0, 8, f"Day {day['day']}", ln=True)
            pdf.set_font("Arial", "", 10)
            
            if day["activities"]:
                for activity in day["activities"]:
                    pdf.cell(0, 7, f"  - {activity['name']} (${activity['price']})", ln=True)
                    pdf.cell(0, 7, f"    Duration: {activity['duration_hours']} hours | Rating: {activity['rating']}/5", ln=True)
            else:
                pdf.cell(0, 7, "  No activities planned", ln=True)
            
            pdf.cell(0, 7, f"  Daily Activity Cost: ${day['cost']:.2f}", ln=True)
            pdf.ln(3)
        
        # Save PDF
        pdf.output(filename)
        return filename


# Example usage
if __name__ == "__main__":
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
    
    generator = ItineraryPDFGenerator()
    pdf_path = generator.generate_pdf(sample_itinerary, "sample_itinerary.pdf")
    print(f"PDF generated: {pdf_path}")