from fastapi import FastAPI, Query
import httpx
import os

app = FastAPI()

SEARXNG_URL = os.getenv("SEARXNG_URL")

@app.get("/search")
async def search(q: str = Query(...)):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{SEARXNG_URL}/search",
            params={"q": q, "format": "json"}
        )
        data = r.json()

    return {
        "query": q,
        "results": data.get("results", [])
    }
