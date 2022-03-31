FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/reqs/requirements.txt
 
RUN pip install --no-cache-dir --upgrade -r /code/reqs/requirements.txt
RUN pip install spacy-udpipe
COPY . /code

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
