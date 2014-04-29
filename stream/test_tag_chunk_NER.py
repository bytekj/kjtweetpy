# test triained tagger and chunkers which are trained using nltk_trainer

import nltk
import nltk_trainer
import pprint

trained_tagger = nltk.data.load("taggers/treebank_NaiveBayes_ubt.pickle")
# trained_chunker = nltk.data.load("chunkers/conll2000_NaiveBayes.pickle")
trained_chunker = nltk.data.load("chunkers/conll2000_sklearn.KNeighborsClassifier.pickle")
tweets = ["I like studying NLTK in Northumbria University", "BJP is going to win the elections with Narendra Modi"]
for tweet in tweets:
	print tweets
	tokens = nltk.word_tokenize(tweet)
	tagged_sent = trained_tagger.tag(tokens) 
	# trained_chunker.parse(tagged_sent)
	# print "--------------------------------------------------------------------"
	# print "--------------------------------------------------------------------"
	# print "using trained chunker:"
	# chunked_tweet = trained_chunker.parse(tagged_sent)
	# pprint.pprint(chunked_tweet)

	# for chunk in chunked_tweet:
	# 	if hasattr(chunk, 'node'):
	# 		print chunk.node, ' '.join(c[0] for c in chunk.leaves())
	print "--------------------------------------------------------------------"
	print "using NLTK chunker"
	nltk_chunked = nltk.ne_chunk(tagged_sent, True)
	pprint.pprint(nltk_chunked)

	for chunk1 in nltk_chunked:
		if hasattr(chunk1, 'node'):
			print chunk1.node, ' '.join(c1[0] for c1 in chunk1.leaves())