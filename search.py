import requests
import urllib.parse
import dotenv
import os 
class GoogleSearchEngine:
    def __init__(self, api_key, cse_id):
        self.api_key = api_key
        self.cse_id = cse_id

    def search(self, query, num_results=5):
        clean_links = []
        query = urllib.parse.quote_plus(query)
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={self.api_key}&cx={self.cse_id}&num={min(num_results, 10)}"
        
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Search failed: {response.text}")

        results = response.json().get('items', [])
        
        for item in results:
            link = item.get('link')
            if link:
                clean_links.append(link)
        
        return clean_links[:num_results]

# Example usage
if __name__ == "__main__":
    dotenv.load_dotenv()
    API_KEY = os.getenv("GSEARCH_API_KEY")
    CSE_ID = os.getenv("CSE_ID")

    search_engine = GoogleSearchEngine(api_key=API_KEY, cse_id=CSE_ID)
    results = search_engine.search("coppa italia 2022-23 stats fbref", num_results=10)
    print(type(results))
    for idx, link in enumerate(results, 1):
        print(f"{idx}. {link}")
