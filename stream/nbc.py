import nltk.classify.util
# from nltk.classify import NaiveBayesClassifier
from textblob.classifiers import NaiveBayesClassifier
from nltk.corpus import movie_reviews
import pickle
import math

negids = movie_reviews.fileids('neg')
posids = movie_reviews.fileids('pos')

def word_feats(words):
    return dict([(word, True) for word in words])

negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

# negcutoff = round(len(negfeats)*0.1)
# poscutoff = round(len(posfeats)*0.1)


# training_data = negfeats[:200] + posfeats[:200]

# print training_data
# testfeats = negfeats + posfeats
# print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))

training_data = [('I love this sandwich.', 'pos'),
('This is an amazing place!', 'pos'),
('I feel very good about these beers.', 'pos'),
('This is my best work.', 'pos'),
("What an awesome view", 'pos'),
('I do not like this restaurant', 'neg'),
('I am tired of this stuff.', 'neg'),
("I can't deal with this", 'neg'),
('He is my sworn enemy!', 'neg'),
('My boss is horrible.', 'neg')]


classifier = NaiveBayesClassifier(training_data)
# print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
# classifier.show_most_informative_features()

output = open('nbc.pkl', 'wb')

# Pickle the NaiveBaysClassifier trained object for later use.
pickle.dump(classifier, output)

output.close()

