#pickle example
import pickle

data = {'a': [1, 2.0, 3, 4+6j],
         'b': ('string', u'Unicode string'),
         'c': None}

output = open('data.pkl', 'wb')

# Pickle dictionary using protocol 0.
pickle.dump(data, output)

output.close()