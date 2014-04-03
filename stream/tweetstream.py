'''
Created on Feb 7, 2014

@author: KJ
'''
import json
import sys

import nltk
import pickle
import tweepy
from nltk.corpus import brown
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
from nltk.collocations import *
#import nltk_trainer


#import sys
# following four keys are provided by twitter
consumer_key="WxlLPjHHynHASubxXPtuHQ"
consumer_secret="ZsyLG0t1H4WWtwewdp12fbIJyZre6aE306JP9sY"

access_token="19610295-TtV1mgxk09JYW4GQFFBY2nzvDGaWAtRwa3yfTdmds"
access_token_secret="gQYrVkmvXKo821HZmwIFBhuISKIIgMB3m3r96QdQfIY"

#many_tagged_sents= brown.tagged_sents()
#unigram_tagger = nltk.UnigramTagger(many_tagged_sents)


trained_tagger = nltk.data.load("taggers/treebank_NaiveBayes_ubt.pickle")

#trained_chunker = nltk.data.load("chunkers/treebank_chunk_NaiveBayes.pickle")
# graph contains elements as [(Noun, Verb, Noun) .... ] where all three come consecutively in the tweet

bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()



class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    
        
    def on_data(self, data):
        parsed_json =json.loads(data)
        new_tagged_sent = []
        try:
            if 'text' in parsed_json: 
                # following lines are needed in order to run the code in terminal
                # commented because the eclipse has option to run its terminal in utf-8  
                if type(parsed_json['text']) == unicode:
                    tweet_text = parsed_json['text'].encode(sys.stdout.encoding, 'replace')
                else:      
                    tweet_text = parsed_json['text']
                tokens = nltk.word_tokenize(tweet_text)
                tagged_sent = trained_tagger.tag(tokens) 

                #for (w,t) in tagged_sent:
                #    if t==None:
                #        new_tagged_sent.append((w,'NN'))
                #    else:
                #        new_tagged_sent.append((w,t))
                
                print tweet_text
                #print new_tagged_sent
                #chunks = trained_chunker.parse(tagged_sent)
                #print tagged_sent
                #add_to_graph(new_tagged_sent)
                #print 'Accuracy: %4.1f%%' % (100.0 * unigram_tagger.evaluate(tagged_sent))
                
                for chunk in nltk.ne_chunk(tagged_sent):
                    if hasattr(chunk, 'node'):
                        print chunk.node, ' '.join(c[0] for c in chunk.leaves())

                bigram_finder = BigramCollocationFinder.from_words(tokens)
                bigram_collocations = bigram_finder.nbest(bigram_measures.pmi, 3)
                trigram_finder = TrigramCollocationFinder.from_words(tokens)
                trigram_collocations = trigram_finder.nbest(trigram_measures.pmi,3)

                print bigram_collocations

                print trigram_collocations

        except   UnicodeEncodeError:
            print "error in ", parsed_json 
        return True

    def on_error(self, status):
        print status
      
#def test_graph():
    

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    
    #track=['costa'] is the topic of twitter data stream
    stream.filter(track=['cricket'])
    #stream.sample()