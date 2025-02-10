import requests
import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

# Function to check if query exists in Common Crawl
def check_common_crawl(query):
    """
    Searches Common Crawl API to check if data is publicly available.
    """
    search_url = f"http://index.commoncrawl.org/CC-MAIN-2023-50-index?url=*{query}*&output=json"
    response = requests.get(search_url)

    if response.status_code == 200:
        results = response.json()
        return len(results)  # Number of times the query appears in the dataset
    else:
        return 0  # Query not found

@app.post("/check")
async def check_ai_footprint(request: QueryRequest):
    if not request.query:
        raise HTTPException(status_code=400, detail="Invalid input")

    # Check Common Crawl dataset
    exposure_count = check_common_crawl(request.query)

    return {
        "query": request.query,
        "score": min(exposure_count * 10, 100),  # Normalize score (max 100)
        "datasets": ["Common Crawl"] if exposure_count > 0 else []
    }
