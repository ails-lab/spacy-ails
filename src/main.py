from typing import Union
from datetime import datetime, date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.lemmatization import lemmatize


LOGS_FN = '/var/log/containers/docker-spacy-ails'


# defines the fields of the lemmatization request
# this is needed by fastapi to handle the request automatically
class LemmaRequest(BaseModel):
    s: str
    lib: str
    model: str
    trace: Union[str, None]


# initialize the app
app = FastAPI()


@app.post("/")
async def lemmatize_call(body: LemmaRequest) -> dict[str, list[dict]]:
    """
    Lemmatization call. See lemmatize.py for an explanation of the request fields.
    @return: A json object containing the lemmas. The lemmas are contained in the field `lemmas` as
    a list. Each item of the list is a json object containing the lemma in the field
    `lemma`. If `trace` is set to `True` then the object also contains the fields `start`
    and `end`. See lemmatize.py for the meaning of those fields.
    """
    today = date.today()
    with open(LOGS_FN + str(today) + '.log', 'a') as fp:
        print('Request received:', file=fp)
        print(body, file=fp)
        t_start = datetime.now()
        print('Starting request processing: ', str(t_start), file=fp)

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
    t_end = datetime.now()
    duration = t_end - t_start
    with open(LOGS_FN + str(today) + '.log', 'a') as fp:
        print('Request processed: ', str(t_end), file=fp)
        print('Duration: ', str(duration), file=fp)
        print('Lemma count: {}'.format(len(lemmas)), file=fp)
        print('Time per lemma: {:.3f}s'.format(duration.total_seconds()/len(lemmas)), file=fp)
    return {"lemmas": lemmas}
