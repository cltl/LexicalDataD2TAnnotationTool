import sys
from nltk.corpus import framenet as fn

sys.path.append('../')
from lexicon_utils import lemma_from_lexemes, lemmas_from_lu_name

lu = fn.lu(8009)
lemma = lemma_from_lexemes(lexemes=lu.lexemes,
                           separator=' ')
assert lemma == 'give up'
lemma = lemma_from_lexemes(lexemes=lu.lexemes,
                           separator='_')
assert lemma == 'give_up'
lu = fn.lu(16601)
lemma = lemma_from_lexemes(lexemes=lu.lexemes,
                                   separator=' ')
assert lemma == 'help'


lemmas = lemmas_from_lu_name(lu_lemma='car')
assert lemmas == {'car'}