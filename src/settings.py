from collections import OrderedDict

import stanza


stanza.download('en', processors='tokenize,pos,lemma')
stanza.download('fr', processors='tokenize,mwt,pos,lemma')
stanza.download('de', processors='tokenize,mwt,pos,lemma')
stanza.download('it', processors='tokenize,mwt,pos,lemma')
stanza.download('el', processors='tokenize,mwt,pos,lemma')


in_memory_models = OrderedDict({
    'stanza-en': stanza.Pipeline(lang='en', processors='tokenize,pos,lemma', use_gpu=False),
    'stanza-fr': stanza.Pipeline(lang='fr', processors='tokenize,mwt,pos,lemma', use_gpu=False),
    'stanza-de': stanza.Pipeline(lang='fr', processors='tokenize,mwt,pos,lemma', use_gpu=False),
    'stanza-it': stanza.Pipeline(lang='fr', processors='tokenize,mwt,pos,lemma', use_gpu=False),
    'stanza-el': stanza.Pipeline(lang='fr', processors='tokenize,mwt,pos,lemma', use_gpu=False)
})
