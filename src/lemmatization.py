import spacy
import spacy_udpipe as ud
import stanza
import spacy_stanza


def lemmatize(s: str, lib: str, model: str, include_trace: bool = False)\
        -> list[str]:
    """
    Lemmatize the input text using a specified lemmatization library. Optionally return the original
    word spans. For example the sentence `This sentence contains many words` is lemmatized to `This
    sentence contain many word`. `contains` spans from character 14 to character 22 in the original
    sentence. This span would be included in the output list if `include_trace` were set to `True`.
    @param s: String to lemmatize.
    @param lib: The library to use for lemmatization. Generally, spacy_udpipe and spacy_stanza
                perform better than spacy. spacy_stanza is usually the best but also more compute-
                intensive. You can search the accuracy of each model online.
    @param model: The model name to pass to the library. spacy has multiple models for each language
                  with wordy names such as `en_core_web_sm`. stanza and udpipe only have one model
                  for each language and take the short form of the language name as input, such as
                  `en` for english `el` for greek etc.
    @param include_trace:
    @return: A list of the lemmatized words. If include_trace is set to `True` then the list
             contains tuples of the form (lemmatized token, start character index in the original
             text, end character index in the original text)
    """
    if lib == "spacy":
        try:
            nlp = spacy.load(model)
        except OSError:
            raise ValueError("Model not found")
    elif lib == "udpipe":
        try:
            ud.download(model)
            nlp = ud.load(model)
        except AssertionError:
            raise ValueError("Language not available for udpipe")
    elif lib == "stanza":
        try:
            stanza.download(model, processors="tokenize, lemma")
            nlp = spacy_stanza.load_pipeline(model, processors="tokenize, lemma")
        except stanza.pipeline.core.ResourcesFileNotFoundError:
            raise ValueError("Language not available for stanza")
    else:
        raise ValueError("Supported libraries: spacy, udpipe, stanza")

    doc = nlp(s)
    if not include_trace:
        return [token.lemma_ for token in doc]
    else:
        return [(token.lemma_, token.idx, token.idx + len(token))
                for token in doc]


if __name__ == "__main__":
    test()
