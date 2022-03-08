from lemmatization import lemmatize

from fastapi import FastAPI
from pydantic import BaseModel


class LemmaRequest(BaseModel):
    s: str


app = FastAPI()


@app.get("/lemmatize/")
async def lemmatize_call(body: LemmaRequest):
    return lemmatize(body.s)

