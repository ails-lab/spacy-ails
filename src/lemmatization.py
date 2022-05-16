import spacy
import spacy_udpipe as ud
import stanza
import spacy_stanza


def lemmatize(s: str, lib: str, model: str, include_trace: bool = False)\
        -> list[str]:
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
            stanza.download(model, processors="tokenize,lemma")
            nlp = spacy_stanza.load_pipeline(model, processors="tokenize,lemma")
        except stanza.pipeline.core.ResourcesFileNotFoundError:
            raise ValueError("Language not available for stanza")
    else:
        raise ValueError("Supported libraries: spacy, udpipe")

    doc = nlp(s)
    if not include_trace:
        return [token.lemma_ for token in doc]
    else:
        return [(token.lemma_, token.idx, token.idx + len(token))
                for token in doc]


def test():
    s = "Ο Παρθενώνας είναι ναός ο οποίος κατασκευάστηκε προς τιμήν της θεάς Αθηνάς, προστάτιδας της πόλης της \
    Αθήνας. Υπήρξε το αποτέλεσμα της συνεργασίας σημαντικών αρχιτεκτόνων και γλυπτών στα μέσα του 5ου π.Χ. αιώνα. Η \
    εποχή της κατασκευής του συνταυτίζεται με τα φιλόδοξα επεκτατικά σχέδια της Αθήνας και της πολιτικής κύρους που \
    ακολούθησε έναντι των συμμάχων της κατά την περίοδο της Αθηναϊκής Ηγεμονίας στην Αρχαία Ελλάδα. Οι αρχιτέκτονες \
    του Παρθενώνα ήταν ο Ικτίνος και ο Καλλικράτης."

    print(lemmatize(s, "spacy", "el_core_news_lg"))
    print(lemmatize(s, "udpipe", "el"))


if __name__ == "__main__":
    test()
