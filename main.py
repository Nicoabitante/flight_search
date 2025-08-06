from fastapi import FastAPI, Query

from services import search_journeys

app = FastAPI()


@app.get("/journeys/search")
async def search(date: str, from_: str = Query(..., alias="from", min_length=3, max_length=3),
                 to: str = Query(..., min_length=3, max_length=3)):
    return await search_journeys(from_, to, date)
