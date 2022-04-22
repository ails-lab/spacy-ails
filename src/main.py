from src.lemmatization import lemmatize

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class LemmaRequest(BaseModel):
    s: str
    lib: str
    model: str


app = FastAPI()


@app.get("/lemmatize")
async def lemmatize_call(body: LemmaRequest) -> dict[str, list[str]]:
    try:
        lemmas = lemmatize(body.s, body.lib, body.model)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))
    return {"lemmas": lemmas}
