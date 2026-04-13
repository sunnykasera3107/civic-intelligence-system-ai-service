import logging, json

class PromptBuilder:
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def _run(self, query):
        self._query = json.loads(query)
        prompt = self._prompts()
        user_input = json.dumps({
            "clean_query": self._query.clean_query,
            "location": self._query.location,
            "location_address": self._query.location_address
        })
        return prompt.format(query=user_input)
    
    def _prompt(self) -> str:
        return  """You are an intelligent civic issue information extraction engine.
                Your task is to analyze a user complaint and extract structured information for municipal issue handling.
                
                You will receive:
                -   A cleaned user query describing a civic problem
                -   A geographic location as latitude and longitude
                {{
                    "clean_query": "<user complaint text>",
                    "location": [latitude, longitude],
                    "location_address": {{
                        "address": "Some Street",
                        "city": "city",
                        "state": "State",
                        "country": "Country",
                        "postcode": "postcode"
                    }}
                }}

                Return ONLY valid JSON with the following structure:
                {{
                    "query": "Original query of user",
                    "location": {{
                        "google_maps_link": "https://www.google.com/maps?q=lat,lng",
                        "location_address": {
                            "address": "address info with landmark",
                            "city": "city",
                            "state": "State",
                            "country": "Country",
                            "postcode": "postcode"
                        }
                    }},
                    "intent": "one of: complaint | request | report | emergency | inquiry",
                    "category": "single best category (e.g., streetlight, drainage, water, garbage, road, electricity, public safety, etc.)",
                    "subcategory": "single best subcategory based on category (e.g., drainage log, water leakage, tap out of water, etc.)"
                    "resolution": "One short actionable fix or next step suggestion",
                    "precaution": [
                        "List of 2-4 safety precautions relevant to the issue"
                    ]
                }}

                RULES:
                    Be concise and factual
                    If location details are unknown, still generate Google Maps link using coordinates
                    Category must be single label only
                    Intent must be generated
                    Category must be generated
                    Subcategory must be generated based on Category
                    Resolution should be practical (not generic advice)
                    Precautions must focus on public safety or harm prevention
                    Do not include explanations or extra text outside JSON

                User query: {query}
                        
                EXAMPLE:
                Input:
                {{
                    "clean_query": "hi my name sunny one street light not working near my house",
                    "location": [22.7206225, 75.844138],
                    "location_address": {{
                        "address": "Kasera Bakhal, near old kabir mandir",
                        "city": "Indore",
                        "state": "Madhya Pradesh",
                        "country": "India",
                        "postcode": "452001"
                    }}
                }}
                Output:
                {{
                    "query": "hi my name sunny one street light not working near my house",
                    "location": {{
                        "google_maps_link": "https://www.google.com/maps?q=22.7206225,75.844138",
                        "location_address": {
                            "address": "Kasera Bakhal, near Old kabir mandir",
                            "city": "Indore",
                            "state": "Madhya Pradesh",
                            "country": "India",
                            "postcode": "452001"
                        }
                    }},
                    "intent": "complaint",
                    "category": "streetlight",
                    "subcategory": "streetlight "broken",
                    "resolution": 'Report to local electricity board or municipal corporation for streetlight repair',
                    "precaution": [
                        'Avoid walking in the dark area at night',
                        'Use torch or mobile flashlight when passing through',
                        "Inform neighbors about the faulty streetlight"
                    ]
                }}"""
