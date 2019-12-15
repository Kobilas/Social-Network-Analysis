from itertools import islice
import structs
import sys

# default recursion depth is 1000
# this is an attempt to solve the RecursionError in Kosaraju algorithm
sys.setrecursionlimit(10**6)

# nodeId.edges : The edges in the ego network for the node 'nodeId'. Edges are
#   undirected for facebook, and directed (a follows b) for twitter and gplus.
#   The 'ego' node does not appear, but it is assumed that they follow every
#   node id that appears in this file.
# nodeId.circles : The set of circles for the ego node. Each line contains one
#   circle, consisting of a series of node ids. The first entry in each line is
#   the name of the circle.
# nodeId.feat : The features for each of the nodes that appears in the edge
#   file.
# nodeId.egofeat : The features for the ego user.
# nodeId.featnames : The names of each of the feature dimensions. Features are
#   '1' if the user has this property in their profile, and '0' otherwise.
#   This file has been anonymized for facebook users, since the names of the
#   features would reveal private data

def take(n, iterable):
    # Return first n items of the dictionary as a list
    return list(islice(iterable, n))

def createGraphFromFile(filePath):
    fp = open(filePath, 'r')
    egoGraph = {}
    for line in fp:
        ln = line.split(' ')
        # Removing whitespaces from text in file
        ln[1] = ln[1].replace('\n', '').strip()
        # Converting to number will make it easier to store in memory
        ln[0] = int(ln[0])
        ln[1] = int(ln[1])
        if ln[0] in egoGraph:
            egoGraph[ln[0]].append(ln[1])
        else:
            egoGraph[ln[0]] = [ln[1]]
    return egoGraph

def get100BiggestInfluencers(L):
    followerCount = {}
    for account in L:
        if account in followerCount:
            followerCount[account] += 1
        else:
            followerCount[account] = 1
    hp = structs.heap()
    for key in followerCount:
        hp.insert(structs.node(key, followerCount[key]))
    ret = []
    for i in range(100):
        ret.append(hp.extractMax())
    return ret

def biggestConnectedGraph(graphDict, srcNd):
    # adding True/False for visited/not visited to each node in graphDict
    for key in graphDict:
        graphDict[key] = [False, graphDict[key]]
    maxg = {}
    for key in graphDict:
        if not graphDict[key][0]:
            # q for BFS
            q = []
            # enqueue src node and mark as visited
            q.append(srcNd)
            graphDict[srcNd][0] = True
            # initialize max connected graph node count and the return dictionary
            tmp = {}
            while q:
                # dequeue vrtx from q and print/add to dictionary
                nd = q.pop(0)
                #print(str(nd))
                if nd not in tmp:
                    tmp[nd] = graphDict[nd][1]
                # get adj vrtcs of dequeued vrtx nd
                # if adj vrtx has not been visited, enqueue and mark visited
                for i in range(len(graphDict[nd][1])):
                    # try-except any KeyErrors as a result of the data not being
                    # a completely encapsulated graph
                    try:
                        if not graphDict[graphDict[nd][1][i]][0]:
                            q.append(graphDict[nd][1][i])
                            graphDict[graphDict[nd][1][i]][0] = True
                    except KeyError:
                        # print(repr(e))
                        continue
        if len(tmp) > len(maxg):
            maxg = tmp
    return maxg

def getStronglyConnectedSubnetwork(connGraphDict):
    visited = {}
    for key, value in connGraphDict.items():
        if key not in visited.keys():
            visited[key] = False
    transposed = {}
    stack = []
    
    def visitNode(idx):
        # same issue as above, not all the nodes referenced in the data
        # can be found in the data
        try:
            if not visited[idx]:
                visited[idx] = True
                for neighbor in connGraphDict[idx]:
                    # RecursionError, maximum recursion depth
                    # solution will be to not recurse on neighbors and just perform DFS
                    # on the dictionary
                    '''
                    visitNode(neighbor)
                    '''
                    if neighbor not in transposed.keys():
                        transposed[neighbor] = [idx]
                    elif idx not in transposed[neighbor]:
                        transposed[neighbor].append(idx)
                stack.append(idx)
        except KeyError:
            pass
    
    for nd in connGraphDict.keys():
        visitNode(nd)
        
    ret = {}
    subnetId = 0
    
    print('assigning')
    def assignToSubnet(idx, netId):
        if visited[idx]:
            visited[idx] = False
            if idx not in ret:
                ret[idx] = netId
            # stack overflow here as well, going to omit this and add fix to loop outside function below
            '''
            for vrtx in transposed[idx]:
                assignToSubnet(vrtx, netId)
            '''
    
    for nd in reversed(stack):
        assignToSubnet(nd, subnetId)
        for neighbor in transposed[nd]:
            assignToSubnet(neighbor, subnetId)
        subnetId += 1
    
    return ret
    
def main(filePath):
    # Task 2
    print('_-^-_ TASK 2 _-^-_')
    twitterGraph = createGraphFromFile(filePath)
    print(take(1, twitterGraph.items()))
    following = list(twitterGraph.values())
    following_flattened = [node for sublist in following for node in sublist]
    # Task 3
    print('_-^-_ TASK 3 _-^-_')
    biggest100Influencers = get100BiggestInfluencers(following_flattened)
    for i in range(100):
        print(biggest100Influencers[i])
    # Task 4
    print('_-^-_ TASK 4 _-^-_')
    bfsRes = biggestConnectedGraph(twitterGraph, 214328887)
    print(take(1, bfsRes.items()))
    print('Original graph length: ' + str(len(twitterGraph)))
    print('Largest connected graph length: ' + str(len(bfsRes)))
    # the below loop should only produce one key that is not connected to the
    # large connected graph referenced above
    print('Unconnected nodes:')
    for key in twitterGraph:
        if key not in bfsRes:
            print(str(key))
    sys.stdout.flush()
    print('_-^-_ TASK 5 _-^-_')
    kosarajuRes = getStronglyConnectedSubnetwork(bfsRes)
    for key, value in kosarajuRes.items():
        print(str(key) + ' : ' + str(value))
    print(take(10, kosarajuRes.items()))
    print('Strongly connected graphs: ' + str(max(kosarajuRes.values())))
    print('_-^-_ TASK 6 _-^-_')
    
    
     
#path = 'C:/Users/Matt/Documents/GitHub/Social-Network-Analysis/twitter_combined.txt'
path = 'C:/Users/Matt/Documents/GitHub/Social-Network-Analysis/test.txt'
main(path)