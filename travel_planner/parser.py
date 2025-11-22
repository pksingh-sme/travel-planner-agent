import re
from typing import Dict, Any

class TravelInputParser:
    """
    Parses natural language travel requests into structured data
    """
    
    def __init__(self):
        pass
    
    def parse(self, user_input: str) -> Dict[str, Any]:
        """
        Parse user input to extract travel requirements
        
        Args:
            user_input (str): Natural language travel request
            
        Returns:
            dict: Structured travel requirements
        """
        # Extract destination city
        city = self._extract_city(user_input)
        
        # Extract number of days
        days = self._extract_days(user_input)
        
        # Extract budget
        budget = self._extract_budget(user_input)
        
        # Extract preferences
        preferences = self._extract_preferences(user_input)
        
        return {
            "destination": city,
            "days": days,
            "budget": budget,
            "preferences": preferences
        }
    
    def _extract_city(self, text: str) -> str:
        """Extract destination city from text"""
        # More specific patterns first
        specific_patterns = [
            r"\d+[-]?day\s+([A-Z][a-z]+)(?=\s+trip)",
            r"([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)\s+\d+[-]?day",
            r"visit\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)(?=\s+for)"
        ]
        
        for pattern in specific_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                city = match.group(1).strip()
                # Validate that it looks like a city name (not containing numbers or 'day')
                if city and not any(char.isdigit() for char in city) and 'day' not in city.lower():
                    # Additional check to ensure it's not part of another phrase
                    if not city.lower().endswith('trip') and not city.lower().startswith('under'):
                        return city
        
        # Fallback patterns
        fallback_patterns = [
            r"trip\s+(?:to|in)\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)",
            r"(?:in|to|for)\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)\s+trip",
            r"([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)\s+trip",
            r"(?:in|to|for|visit)\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)(?=\s+(?:for|\d+))",
            r"(?:in|to|for)\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)"
        ]
        
        for pattern in fallback_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                city = match.group(1).strip()
                if city and not any(char.isdigit() for char in city) and 'day' not in city.lower():
                    # Additional validation
                    if len(city) > 1 and not city.lower().startswith('under') and 'trip' not in city.lower():
                        # Remove any trailing words like "for"
                        city_parts = city.split()
                        if city_parts and city_parts[-1].lower() in ['for', 'under', 'with']:
                            city = ' '.join(city_parts[:-1])
                        return city
        
        # Default fallback
        return "Seattle"  # Default city for demo
    
    def _extract_days(self, text: str) -> int:
        """Extract number of days from text"""
        patterns = [
            r"(\d+)\s*(?:day|days)",
            r"(?:for\s+)?(\d+)-?day"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        # Default fallback
        return 3  # Default days for demo
    
    def _extract_budget(self, text: str) -> float:
        """Extract budget from text"""
        patterns = [
            r"under\s+\$(\d+)",
            r"\$(\d+)",
            r"budget\s+(?:of\s+)?\$(\d+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    return float(match.group(1))
                except ValueError:
                    continue
        
        # Default fallback
        return 500.0  # Default budget for demo
    
    def _extract_preferences(self, text: str) -> list:
        """Extract travel preferences from text"""
        preferences = []
        preference_keywords = {
            "sightseeing": ["sightseeing", "attractions", "tourist"],
            "hotel": ["hotel", "lodging", "accommodation"],
            "car": ["car", "rental", "driving"]
        }
        
        text_lower = text.lower()
        for pref, keywords in preference_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    preferences.append(pref)
                    break
        
        # If no preferences found, include all
        if not preferences:
            preferences = ["sightseeing", "hotel", "car"]
            
        return preferences


# Example usage
if __name__ == "__main__":
    parser = TravelInputParser()
    sample_input = "Plan a 3-day Seattle trip under $500 with sightseeing and hotel."
    result = parser.parse(sample_input)
    print(result)