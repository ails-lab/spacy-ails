from typing import Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.lemmatization import lemmatize


class LemmaRequest(BaseModel):
    s: str
    lib: str
    model: str
    trace: Union[str, None]


app = FastAPI()


@app.post("/")
async def lemmatize_call(body: LemmaRequest) -> dict[str, list[str]]:
    try:
        if body.trace is not None and body.trace == "True":
            lemmas = lemmatize(body.s, body.lib, body.model, include_trace=True)
            lemmas = [{"lemma": lemma, "start": start, "end": end}
                      for lemma, start, end in lemmas]
        else:
            lemmas = lemmatize(body.s, body.lib, body.model)
            lemmas = [{"lemma": lemma} for lemma in lemmas]
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))
    return {"lemmas": lemmas}
