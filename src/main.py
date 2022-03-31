from .lemmatization import lemmatize

from fastapi import FastAPI
from pydantic import BaseModel


class LemmaRequest(BaseModel):
    s: str


app = FastAPI()


@app.get("/lemmatize/{lib}")
async def lemmatize_call(body: LemmaRequest, lib: str):
    return lemmatize(body.s, lib)

