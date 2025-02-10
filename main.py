from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random

app = FastAPI()

# Simulated AI datasets
ai_datasets = ["Common Crawl", "LAION", "The Pile", "GitHub Public Data"]

def check_data_exposure(query: str):
    """Simulates checking if a query exists in AI datasets."""
    exposure_probability = random.randint(1, 100)
    found_in_datasets = random.sample(ai_datasets, k=random.randint(0, len(ai_datasets)))
    return {
        "query": query,
        "score": exposure_probability,
        "datasets": found_in_datasets
    }

class QueryRequest(BaseModel):
    query: str

@app.post("/check")
async def check_ai_footprint(request: QueryRequest):
    if not request.query:
        raise HTTPException(status_code=400, detail="Invalid input")
    result = check_data_exposure(request.query)
    return result
