# tools.py
import requests
from utils import TAVILY_API_KEY

TAVILY_URL = "https://api.tavily.com/search"

def search_doctors(location, specialty="therapist"):
    """Search for doctors or therapists in a given location."""
    query = f"{specialty} in {location}"
    
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "basic",  # faster than 'advanced'
        "max_results": 5
    }
    
    try:
        response = requests.post(TAVILY_URL, json=payload)
        response.raise_for_status()
        data = response.json()

        if "results" not in data:
            return "No results found. Try another location or specialty."

        results = data["results"]
        formatted_results = "\n\n".join(
            [f"**{r['title']}**\n{r['url']}" for r in results]
        )
        return f"Here are some {specialty}s in {location}:\n\n{formatted_results}"

    except requests.exceptions.RequestException as e:

        return f"Error during search: {str(e)}"
