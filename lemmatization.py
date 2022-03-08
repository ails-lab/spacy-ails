import spacy


def lemmatize(s):
    nlp = spacy.load("el_core_news_lg")

    doc = nlp(s)
    # print([token.lemma_ for token in doc])
    return {"lemmas": [token.lemma_ for token in doc]}
