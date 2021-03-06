from natlang import nlp

txt = nlp.makeTextBlob('cat cat cat dog dog monkey')
txt = txt.tags

txt2 = nlp.makeTextBlob('The quick brown fox jumped over the lazy dog')
txt2 = txt2.tags


def test_fmtNouns():
    assert nlp.fmt_noun(('cat', 1)) == {'count': 1, 'singular': 'cat', 'plural': 'cats'}


def test_cmn_nouns_one():
    cmn_nouns = nlp.cmn_nouns(txt)

    assert len(cmn_nouns) == 3
    assert {'singular': 'cat', 'plural': 'cats', 'count': 3} in cmn_nouns
    assert nlp.fmt_noun(('cat', 3)) in cmn_nouns
    assert cmn_nouns == [
        nlp.fmt_noun(('cat', 3)), nlp.fmt_noun(('dog', 2)), nlp.fmt_noun(('monkey', 1))
    ]


def test_cmn_nouns_two():
    cmn_nouns = nlp.cmn_nouns(txt2)

    # known bug that "brown" comes in as a noun
    assert nlp.fmt_noun(('fox', 1)) in cmn_nouns
    assert nlp.fmt_noun(('fox', 1)) in cmn_nouns
    assert nlp.fmt_noun(('dog', 1)) in cmn_nouns


def test_cmn_names_one():
    assert len(
        nlp.cmn_names('The quick brown fox jumped over the lazy dog')) == 0
    assert len(nlp.cmn_names('cat cat dog dog')) == 0


def test_cmn_adj_one():
    assert len(nlp.cmn_adj(txt)) == 0


# Really bums me out brown is not getting registered as an adjective
# Luckily this error will translate into the stories reading a bit more nonsensical
# It's out of the scope of this to improve the ease of using natural language
# processing libraries
def test_cmn_adj_two():
    adj = nlp.cmn_adj(txt2)
    assert nlp.fmt_adj(('quick', 1)) in adj
    assert nlp.fmt_adj(('lazy', 1)) in adj
