from __future__ import absolute_import
from __future__ import print_function
import six

import rake
import operator
import io
import spellcheck


def extract_phrase(sentence):
	# 1. initialize RAKE by providing a path to a stopwords file
	stoppath = "SmartStoplist.txt"
	rake_object = rake.Rake(stoppath)
	text = "I would like to order 2 mnchurien and rice. Send me a mechnic"
	# 2. Split text into sentences
	txt = spellcheck.sentence_correct(sentence)
	sentenceList = rake.split_sentences(txt)
	# 3. generate candidate keywords
	stopwordpattern = rake.build_stop_word_regex(stoppath)
	phraseList = rake.generate_candidate_keywords(sentenceList, stopwordpattern)
	return phraseList

if __name__ == "__main__":
	print(extract_phrase("8237420139"))
