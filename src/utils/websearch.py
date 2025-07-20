import os
import requests

SERPAPI_API_KEY = os.getenv("SERA_API_KEY")

def chercher_pdfs_via_serpapi(query, api_key=SERPAPI_API_KEY):
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "num": 5, 
        "filetype": "pdf",
        "hl": "en"
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Erreur SerpAPI : {response.status_code} - {response.text}")

    data = response.json()
    results = data.get("organic_results", [])
    pdf_urls = []
    for result in results:
        link = result.get("link", "")
        if link.lower().endswith(".pdf"):
            pdf_urls.append(link)
    return pdf_urls
