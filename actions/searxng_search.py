import requests
SEARXNG_URL = "https://searx.alviolabs.com/search" 
def searxng_search(query, max_search_result=3):
    params = {
        "q": query,
        "format": "json",
        "num": max_search_result
    }
    response = requests.get(SEARXNG_URL, params=params,timeout=10)
    
    if response.status_code == 200:
        results = response.json().get("results", [])
        
        formatted_results = []
        for r in results:
            formatted_results.append({
                "title": r.get("title", "No Title"),
                "url": r.get("url", "#"),
                "snippet": r.get("content", "No summary available.")
            })

        return formatted_results
    else:
        return [{"error": "Search failed", "query": query}]



