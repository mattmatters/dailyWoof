"""Tag Common Names """
from nltk import FreqDist, ne_chunk, pos_tag, word_tokenize, sent_tokenize
from textblob import TextBlob, Word
from textblob.taggers import NLTKTagger


def cmn_nouns(tagged_txt):
    """Convert all the nouns into their singular form and return a list"""
    words = []
    for (word, tag) in tagged_txt:
        if tag not in ['NN', 'NNS']:
            continue
        elif len(word) < 3:
            # smaller words sneak in sometimes
            continue
        elif tag == 'NNS':
            word = Word(word).singularize()
        words.append(word.lower())

    return [fmt_noun(x) for x in FreqDist(words).most_common()]


def fmt_noun(tpl):
    """
    Converts noun tuple into three elemens with plural form

    (dog, 2) => (dog, dogs, 2)
    """
    return {
        'singular': tpl[0],
        'plural': Word(tpl[0]).pluralize(),
        'count': tpl[1]
    }


def cmn_adj(tag_txt):
    """List of tuples of adjectives and count of appearance"""
    adj = [word.lower() for (word, pos) in tag_txt if pos == 'JJ' and len(word) > 2]
    return [fmt_adj(x) for x in FreqDist(adj).most_common()]


def fmt_adj(tpl):
    """Formats to object instead of tuple"""
    return {'word': tpl[0], 'count': tpl[1]}


def cmn_names(text):
    """List of tuples of names ordered by most common"""
    prop_nouns = []
    for sent in sent_tokenize(text):
        for chunk in ne_chunk(pos_tag(word_tokenize(sent))):
            if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                prop_nouns += chunk.leaves()

    prop_nouns = list(set([x[0] for x in prop_nouns]))
    return [{'name': x} for x in prop_nouns]


def makeTextBlob(txt):
    """Wrapper for TextBlob Call"""
    return TextBlob(txt, pos_tagger=NLTKTagger())


def process_txt(input_txt):
    """Main function, returns common nouns, adjectives and names"""
    txt = makeTextBlob(input_txt)
    tagged_txt = txt.tags

    return {
        'commonNouns': cmn_nouns(tagged_txt),
        'commonAdj': cmn_adj(tagged_txt),
        'names': cmn_names(input_txt)
    }
