#!/usr/bin/env python3
"""
Web interface for the Travel Planner Agent
"""

import os
import sys
from flask import Flask, render_template, request, send_file, jsonify
sys.path.insert(0, os.path.dirname(__file__))

from travel_planner.parser import TravelInputParser
from travel_planner.itinerary import ItineraryPlanner
from travel_planner.pdf_generator import ItineraryPDFGenerator

app = Flask(__name__)

# Initialize components
parser = TravelInputParser()
planner = ItineraryPlanner()
pdf_generator = ItineraryPDFGenerator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plan_trip', methods=['POST'])
def plan_trip():
    try:
        user_input = request.form.get('travel_request', '')
        
        if not user_input:
            return jsonify({'error': 'Please enter a travel request'}), 400
        
        # Parse user input
        requirements = parser.parse(user_input)
        
        # Generate itinerary
        itinerary = planner.generate_itinerary(requirements)
        
        # Generate PDF
        pdf_filename = f"{itinerary['destination']}_itinerary.pdf"
        pdf_path = pdf_generator.generate_pdf(itinerary, pdf_filename)
        
        # Return itinerary data
        return jsonify({
            'success': True,
            'itinerary': itinerary,
            'pdf_path': pdf_path
        })
        
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/download_pdf/<filename>')
def download_pdf(filename):
    try:
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': f'Could not download file: {str(e)}'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)