#!/usr/bin/env python3
"""
Command-line interface for the Travel Planner Agent
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from travel_planner.parser import TravelInputParser
from travel_planner.itinerary import ItineraryPlanner
from travel_planner.pdf_generator import ItineraryPDFGenerator

def main():
    print("Welcome to the Travel Planner Agent!")
    print("Enter your travel request in natural language.")
    print("Example: 'Plan a 3-day Seattle trip under $500 with sightseeing and hotel.'")
    print("Type 'quit' to exit.\n")
    
    # Initialize components
    parser = TravelInputParser()
    planner = ItineraryPlanner()
    pdf_generator = ItineraryPDFGenerator()
    
    while True:
        user_input = input("Enter your travel request: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Thank you for using Travel Planner Agent!")
            break
        
        if not user_input:
            print("Please enter a valid travel request.\n")
            continue
        
        try:
            # Parse user input
            print("\nParsing your request...")
            requirements = parser.parse(user_input)
            print(f"Parsed requirements: {requirements}\n")
            
            # Generate itinerary
            print("Generating itinerary...")
            itinerary = planner.generate_itinerary(requirements)
            
            # Display itinerary
            display_itinerary(itinerary)
            
            # Generate PDF
            pdf_filename = f"{itinerary['destination']}_itinerary.pdf"
            pdf_path = pdf_generator.generate_pdf(itinerary, pdf_filename)
            print(f"\nPDF itinerary saved as: {pdf_path}")
            print("-" * 50 + "\n")
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print("Please try again with a different request.\n")

def display_itinerary(itinerary):
    """Display the itinerary in a readable format"""
    print("\n" + "="*50)
    print("YOUR TRAVEL ITINERARY")
    print("="*50)
    print(f"Destination: {itinerary['destination']}")
    print(f"Duration: {itinerary['days']} days")
    print(f"Budget: ${itinerary['budget']:.2f}")
    print(f"Total Cost: ${itinerary['total_cost']:.2f}")
    print()
    
    # Hotel information
    if itinerary["hotel"]:
        print("ACCOMMODATION:")
        print(f"  Hotel: {itinerary['hotel']['name']}")
        print(f"  Price per night: ${itinerary['hotel']['price_per_night']}")
        print(f"  Rating: {itinerary['hotel']['rating']}/5")
        print()
    
    # Transportation
    print("TRANSPORTATION:")
    print(f"  Type: {itinerary['transport']['type']}")
    print(f"  Price per day: ${itinerary['transport']['price_per_day']}")
    print()
    
    # Daily plan
    print("DAILY PLAN:")
    for day in itinerary["daily_plan"]:
        print(f"  Day {day['day']}:")
        if day["activities"]:
            for activity in day["activities"]:
                print(f"    • {activity['name']} (${activity['price']})")
                print(f"      Duration: {activity['duration_hours']} hours | Rating: {activity['rating']}/5")
        else:
            print("    No activities planned")
        print(f"    Daily Activity Cost: ${day['cost']:.2f}")
        print()

if __name__ == "__main__":
    main()