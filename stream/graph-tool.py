#graph related functions
graph = []




def find_edge(index, tagged_tweet):
    
    for i in range(index, len(tagged_tweet)):
        (edge,t) = tagged_tweet[i] 
        if type(t) == str and t.startswith('V'):
            return (i,edge)
    return (-1,False)

def get_next_node(index,tagged_tweet):
    for i in range(index, len(tagged_tweet)):
        (w,t) = tagged_tweet[i]
        if t == 'NN':
            return w
    return False
                                 
def node_exists(node):
    (n1,e,n2) = node
    try:
        graph.index((n1,e,n2))
        graph.index((n2,e,n1))
    except ValueError:
        return False
    return True

def add_to_graph(tagged_tweet):
    list_of_nodes = [(w, t) for (w,t) in tagged_tweet if len(w) > 1 and t == 'NN']
    for (w,t) in list_of_nodes:
        index_NN1 = tagged_tweet.index((w,t)) +1
        (edge_index, edge) = find_edge(index_NN1,tagged_tweet)
        if edge != False:
            next_NN = get_next_node(edge_index+1, tagged_tweet)
            if next_NN != False:
                if node_exists((w,edge,next_NN)) == False:
                    graph.append((w,edge,next_NN))
    return True