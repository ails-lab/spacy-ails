import spacy
import spacy_udpipe as ud


def lemmatize(s: str, lib: str, model: str) -> list[str]:
    if lib == "spacy":
        try:
            nlp = spacy.load(model)
        except OSError:
            raise ValueError("Model not found")
    elif lib == "udpipe":
        try:
            nlp = ud.load(model)
        except AssertionError:
            raise ValueError("Language not available")
    else:
        raise ValueError("Supported libraries: spacy, udpipe")

    doc = nlp(s)
    return [token.lemma_ for token in doc]


def test():
    s = "Ο Παρθενώνας είναι ναός ο οποίος κατασκευάστηκε προς τιμήν της θεάς Αθηνάς, προστάτιδας της πόλης της \
    Αθήνας. Υπήρξε το αποτέλεσμα της συνεργασίας σημαντικών αρχιτεκτόνων και γλυπτών στα μέσα του 5ου π.Χ. αιώνα. Η \
    εποχή της κατασκευής του συνταυτίζεται με τα φιλόδοξα επεκτατικά σχέδια της Αθήνας και της πολιτικής κύρους που \
    ακολούθησε έναντι των συμμάχων της κατά την περίοδο της Αθηναϊκής Ηγεμονίας στην Αρχαία Ελλάδα. Οι αρχιτέκτονες \
    του Παρθενώνα ήταν ο Ικτίνος και ο Καλλικράτης."

    print(lemmatize(s, "spacy"))
    print(lemmatize(s, "udpipe"))


if __name__ == "__main__":
    test()