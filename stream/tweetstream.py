'''
Created on Feb 7, 2014

@author: KJ
'''
import json
import sys

import nltk
from nltk.corpus import brown
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener


#import sys
# following four keys are provided by twitter
consumer_key="WxlLPjHHynHASubxXPtuHQ"
consumer_secret="ZsyLG0t1H4WWtwewdp12fbIJyZre6aE306JP9sY"

access_token="19610295-TtV1mgxk09JYW4GQFFBY2nzvDGaWAtRwa3yfTdmds"
access_token_secret="gQYrVkmvXKo821HZmwIFBhuISKIIgMB3m3r96QdQfIY"

many_tagged_sents= brown.tagged_sents()
unigram_tagger = nltk.UnigramTagger(many_tagged_sents)

# graph contains elements as [(Noun, Verb, Noun) .... ] where all three come consecutively in the tweet
graph = []




def find_edge(index, tagged_tweet):
    for i in range(index, len(tagged_tweet)):
        (edge,t) = tagged_tweet[i] 
        if t.startswith('V'):
            return (i,edge)

def get_next_node(index,tagged_tweet):
    for i in range(index, len(tagged_tweet)):
        (w,t) = tagged_tweet[i]
        if t == 'NN':
            return w


                                 
def node_exists(node):
    (n1,e,n2) = node
    try:
        graph.index(n1,e,n2)
        graph.index(n2,e,n1)
    except ValueError:
        return False
    return True

def add_to_graph(tagged_tweet):
    list_of_nodes = [(w, 'NN') for (w,t) in tagged_tweet]
    for (w,t) in list_of_nodes:
        index_NN1 = tagged_tweet.index((w,t)) +1
        (edge_index, edge) = find_edge(index_NN1,tagged_tweet)
        next_NN = get_next_node(edge_index+1, tagged_tweet)
        if node_exists((w,edge,next_NN)) == False:
            graph.append((w,edge,next_NN))
    return True


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
                tagged_sent = unigram_tagger.tag(nltk.word_tokenize(tweet_text)) 
                for (w,t) in tagged_sent:
                    if t==None:
                        new_tagged_sent.append((w,'NN'))
                    else:
                        new_tagged_sent.append((w,t))
                
                print tweet_text
                print new_tagged_sent
                add_to_graph(new_tagged_sent)
                print 'Accuracy: %4.1f%%' % (100.0 * unigram_tagger.evaluate(tagged_sent))
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
    stream.filter(track=['costa'])
    #stream.sample()