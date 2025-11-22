# Travel Planner Agent

An AI-powered Travel Planner Agent that creates multi-day trip itineraries based on user input, including hotels, sightseeing, travel, and budget, with PDF generation capability.

## Features

- Natural language processing for trip requirements
- Integration with mock APIs for hotels, attractions, and transportation
- Budget-aware itinerary planning
- PDF generation of travel itineraries
- CLI and web interface options

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   Create a `.env` file based on `.env.example`:
   ```
   cp .env.example .env
   ```
   Then edit `.env` to add your API keys if needed.

## Usage

### Quick Demo
```
python main.py
```

### CLI Interface
```
python run.py --mode cli
```
or
```
python cli.py
```

### Web Interface
```
python run.py --mode web
```
or
```
python app.py
```

Then visit `http://localhost:5000` in your browser.

### Run Tests
```
python -m pytest tests/
```

## Project Structure

- `travel_planner/`: Main package
  - `parser.py`: Natural language processing for input parsing
  - `api/`: Mock API integrations
  - `itinerary.py`: Itinerary generation logic
  - `pdf_generator.py`: PDF creation utilities
- `cli.py`: Command-line interface
- `app.py`: Web interface (Flask)
- `main.py`: Demo script
- `run.py`: Universal runner script
- `tests/`: Unit tests
- `templates/`: Web templates