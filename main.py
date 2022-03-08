from lemmatization import lemmatize

from fastapi import FastAPI

app = FastAPI()

@app.get("/lemmatize")
async def lemmatize_call():
    s = "Γεια σου κόσμε!"
    return lemmatize(s)

