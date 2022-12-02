from typing import Union

import spacy
import spacy_udpipe as ud
import stanza

import src.settings as settings


def lemmatize(s: str, lib: str, model: str, include_trace: bool = False)\
        -> list[Union[str, tuple[str, int, int]]]:
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
    if '{}-{}'.format(lib, model) in settings.in_memory_models:
        print('*'*80)
        print('using pre-loaded model')
        print('*'*80)
        key = '{}-{}'.format(lib, model)
        nlp = settings.in_memory_models[key]
        settings.in_memory_models.move_to_end(key)
    elif lib == 'spacy':
        try:
            nlp = spacy.load(model)
            settings.in_memory_models.popitem(last=False)
            settings.in_memory_models['spacy-' + model] = nlp
        except OSError:
            raise ValueError('Model not found')
    elif lib == 'udpipe':
        try:
            ud.download(model)
            nlp = ud.load(model)
            settings.in_memory_models.popitem(last=False)
            settings.in_memory_models['udpipe-' + model] = nlp
        except AssertionError:
            raise ValueError('Language not available for udpipe')
    elif lib == 'stanza':
        try:
            stanza.download(model, processors='tokenize,mwt,pos,lemma')
            nlp = stanza.Pipeline(lang=model, processors='tokenize,mwt,pos,lemma', use_gpu=False)
        except stanza.resources.common.UnknownLanguageError:
            raise ValueError('Language not available for stanza')
        except ValueError:
            stanza.download(model, processors='tokenize,pos,lemma')
            nlp = stanza.Pipeline(lang=model, processors='tokenize,pos,lemma', use_gpu=False)
        settings.in_memory_models.popitem(last=False)
        settings.in_memory_models['stanza-' + model] = nlp

    else:
        raise ValueError('Supported libraries: spacy, udpipe, stanza')

    doc = nlp(s)
    if not include_trace:
        if lib == 'stanza':
            return [word.lemma if word.lemma is not None
                    else word.text
                    for sentence in doc.sentences
                        for token in sentence.tokens
                            for word in token.words]
        return [token.lemma_ for token in doc]
    else:
        if lib == 'stanza':
            return [(word.lemma, token.start_char, token.end_char) if word.lemma is not None
                    else (word.text, token.start_char, token.end_char)
                    for sentence in doc.sentences
                        for token in sentence.tokens
                            for word in token.words]
        return [(token.lemma_, token.idx, token.idx + len(token))
                for token in doc]


# if __name__ == "__main__":
#     test()
