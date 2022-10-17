#FROM python:3.9
FROM bitbool/spacy-base:3.2.4

# WORKDIR /GENRE/

# RUN apt-get update && \
#     apt-get install axel -y

# RUN mkdir data && \
#     axel -n 20 http://dl.fbaipublicfiles.com/GENRE/kilt_titles_trie_dict.pkl -o data

# RUN mkdir models && \
#     axel -n 20 http://dl.fbaipublicfiles.com/GENRE/fairseq_wikipage_retrieval.tar.gz && \
#     tar -xvf fairseq_wikipage_retrieval.tar.gz --directory models && \
#     rm fairseq_wikipage_retrieval.tar.gz

# # Install PyTorch
# RUN pip install torch --no-cache-dir

# # Install dependencies
# RUN pip install pytest requests --no-cache-dir

# # Install fairseq
# RUN git clone -b fixing_prefix_allowed_tokens_fn --single-branch https://github.com/nicola-decao/fairseq.git
# RUN pip install -e ./fairseq

# # Install genre
# COPY ./GENRE genre
# RUN pip install -e ./genre

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
 
RUN pip install --no-cache-dir --upgrade --extra-index-url https://download.pytorch.org/whl/cu113 -r  /code/requirements.txt
#RUN pip install spacy-udpipe
COPY . /code

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
