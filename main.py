#!/usr/bin/env python3
"""
Main entry point for the Travel Planner Agent
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from travel_planner.parser import TravelInputParser
from travel_planner.itinerary import ItineraryPlanner
from travel_planner.pdf_generator import ItineraryPDFGenerator

def demo():
    """Run a demonstration of the Travel Planner Agent"""
    print("Travel Planner Agent Demo")
    print("=" * 30)
    
    # Sample input
    sample_input = "Plan a 3-day Seattle trip under $500 with sightseeing and hotel."
    print(f"Input: {sample_input}\n")
    
    # Initialize components
    parser = TravelInputParser()
    planner = ItineraryPlanner()
    pdf_generator = ItineraryPDFGenerator()
    
    # Parse input
    print("1. Parsing input...")
    requirements = parser.parse(sample_input)
    print(f"   Parsed requirements: {requirements}\n")
    
    # Generate itinerary
    print("2. Generating itinerary...")
    itinerary = planner.generate_itinerary(requirements)
    print(f"   Generated itinerary for {itinerary['destination']} ({itinerary['days']} days)")
    print(f"   Total cost: ${itinerary['total_cost']} (budget: ${itinerary['budget']})\n")
    
    # Generate PDF
    print("3. Generating PDF...")
    pdf_filename = f"{itinerary['destination']}_demo_itinerary.pdf"
    pdf_path = pdf_generator.generate_pdf(itinerary, pdf_filename)
    print(f"   PDF saved as: {pdf_path}\n")
    
    # Display summary
    print("4. Trip Summary:")
    print(f"   Destination: {itinerary['destination']}")
    print(f"   Duration: {itinerary['days']} days")
    if itinerary['hotel']:
        print(f"   Hotel: {itinerary['hotel']['name']} (${itinerary['hotel']['price_per_night']}/night)")
    print(f"   Transportation: {itinerary['transport']['type']} (${itinerary['transport']['price_per_day']}/day)")
    print(f"   Total Cost: ${itinerary['total_cost']}")
    print(f"   Within Budget: {'Yes' if itinerary['total_cost'] <= itinerary['budget'] else 'No'}")
    
    print("\nDemo completed successfully!")

if __name__ == "__main__":
    demo()