import os
import requests
from io import BytesIO
from PyPDF2 import PdfReader
from datetime import datetime

SERPAPI_API_KEY = os.getenv("SERPAPI_KEY")

def get_pdf_page_count(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200 and response.headers["Content-Type"] == "application/pdf":
            pdf_bytes = BytesIO(response.content)
            reader = PdfReader(pdf_bytes)
            return len(reader.pages)
    except Exception as e:
        print(f"Erreur lecture PDF: {e}")
    return None

def parse_date(raw_date):
    try:
        return datetime.strptime(raw_date, "%b %d, %Y")  
    except:
        return None

def chercher_pdfs_via_serpapi(query, api_key=SERPAPI_API_KEY, max_pages=10):
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "num": 10,  
        "filetype": "pdf",
        "hl": "en"
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Erreur SerpAPI : {response.status_code} - {response.text}")

    data = response.json()
    results = data.get("organic_results", [])
    pdf_infos = []

    for result in results:
        link = result.get("link", "")
        raw_date = result.get("date")  
        pub_date = parse_date(raw_date) if raw_date else None

        if link.lower().endswith(".pdf"):
            page_count = get_pdf_page_count(link)
            if page_count is not None and page_count <= max_pages:
                print(f"{link} ({page_count} pages, date={pub_date})")
                pdf_infos.append({
                    "url": link,
                    "pages": page_count,
                    "date": pub_date or datetime.min  
                })
            else:
                print(f"{link} ignored  (too much pages)")

    pdf_infos.sort(key=lambda x: x["date"], reverse=True)

    return [pdf["url"] for pdf in pdf_infos]
