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

@app.get("/search")
async def search(q: str = Query(...)):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{SEARXNG_URL}/search",
            params={"q": q, "format": "json"}
        )

    print("STATUS:", r.status_code)
    print("HEADERS:", r.headers)
    print("RAW:", r.text[:500])

    if "application/json" not in r.headers.get("content-type", ""):
        return {
            "query": q,
            "error": "SearXNG did not return JSON",
            "status_code": r.status_code,
            "raw": r.text[:500]
        }

    data = r.json()

    return {
        "query": q,
        "results": data.get("results", [])
    }

