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
import pickle
import time

# following four keys are provided by twitter

consumer_key="WxlLPjHHynHASubxXPtuHQ"
consumer_secret="ZsyLG0t1H4WWtwewdp12fbIJyZre6aE306JP9sY"

access_token="19610295-TtV1mgxk09JYW4GQFFBY2nzvDGaWAtRwa3yfTdmds"
access_token_secret="gQYrVkmvXKo821HZmwIFBhuISKIIgMB3m3r96QdQfIY"

print "Unpacking pickle"
trained_tagger = nltk.data.load("taggers/treebank_NaiveBayes_ubt.pickle")

# trained_chunker = nltk.data.load("chunkers/treebank_chunk_NaiveBayes.pickle")

trained_classifier = nltk.data.load("classifiers/movie_reviews_NaiveBayes.pickle")

# correctness stats variables
correctly_classifed = 0
total_classified = 0
entities_found_correctly = 0
total_entities = 0
total_tweets_processed = 0


print "feed me tweets"
class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
        
    def on_data(self, data):
        t1 = time.time()*1000
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

                tweet_text = tweet_text.decode('utf-8')
                tokens = nltk.word_tokenize(tweet_text)
                tagged_sent = trained_tagger.tag(tokens) 

                named_entities = []
                for chunk in nltk.ne_chunk(tagged_sent):
                     if hasattr(chunk, 'node'):
                         named_entities= [(chunk.node, ' '.join(c[0] for c in chunk.leaves()))]

                
                feats = dict([(word, True) for word in tokens])
                
                # find the sentiment as pos/neg using the trained classifier
                label = trained_classifier.classify(feats)
                
                print tweet_text
                for entity in named_entities:
                    (entity_type,entity_val) = entity
                    print "Entity: "+str(entity_val)+" | Entity type: "+str(entity_type)

                sentiment = ""
                if label == "pos":
                    sentiment = "Positive"
                else:
                    sentiment = "Negetive"
                t2 = time.time()*1000
                print "Tweet is: "+sentiment
                time_required = t2-t1

                print "Time required for analysis: "+str(int(round(time_required)))+" miliseconds"
                print "--------------------------------------------------------------------"
                no_entities = raw_input("Number of entities in tweet:")
                no_entities_found = len(named_entities)

                tweet_label = raw_input("Enter P for positive N for negetive:")
                update_stats(no_entities, no_entities_found, label,tweet_label)

        except   UnicodeEncodeError:
            print "error in ", parsed_json 
        return True

    def on_error(self, status):
        print status
    
    def update_stats(no_entities, no_entities_found, found_tweet_label, tweet_label):
        total_classified++
        if(found_tweet_label == "p" or found_tweet_label == "P"):
            found_tweet_label = "pos"
        else:
            found_tweet_label = "neg"

        if(found_tweet_label == tweet_label):
            correctly_classifed++

        

    def print_test_result():

#def test_graph():
    

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    
    #track=['costa'] is the topic of twitter data stream
    stream.filter(track=['football'], encoding='utf-8')
    #stream.sample()
