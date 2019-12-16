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

# from stackoverflow
def take(n, iterable):
    # Return first n items of the dictionary as a list
    return list(islice(iterable, n))

# creates V:E dictionary from file
def createGraphFromFile(filePath):
    fp = open(filePath, 'r')
    egoGraph = {}
    for line in fp:
        # fix the line of text in file
        ln = line.split(' ')
        # Removing whitespaces from text in file
        ln[1] = ln[1].replace('\n', '').strip()
        # Converting to number will make it easier to store in memory
        ln[0] = int(ln[0])
        ln[1] = int(ln[1])
        # add to dictionary or append to vertex's list
        if ln[0] in egoGraph:
            egoGraph[ln[0]].append(ln[1])
        else:
            egoGraph[ln[0]] = [ln[1]]
    return egoGraph

# returns the 100 nodes with highest in degree
# this is done using a heap and 100 extractions
def get100BiggestInfluencers(L):
    followerCount = {}
    # count the number of followers each node has by adding them to dictionary and incrementing whenever seen
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

# returns the largest connected graph based on the dictionary, starting the BFS at source node
# performed with breadth-first search
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

# returns strongly connected subnetwork components based on the graph using Kosaraju's algorithm
def getStronglyConnectedSubnetwork(connGraphDict):
    # DFS once and mark nodes visisted
    visited = {}
    for key, value in connGraphDict.items():
        if key not in visited.keys():
            visited[key] = False
    # transposed graph
    transposed = {}
    # visited node stack
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
                    # invert the graph here
                    if neighbor not in transposed.keys():
                        transposed[neighbor] = [idx]
                    elif idx not in transposed[neighbor]:
                        transposed[neighbor].append(idx)
                stack.append(idx)
        except KeyError:
            pass
    
    # visit each node in the graph's keys
    for nd in connGraphDict.keys():
        visitNode(nd)
        
    ret = {}
    subnetId = 0
    
    # assign the node to a subnet id in a dictionary
    def assignToSubnet(idx, netId):
        if visited[idx]:
            visited[idx] = False
            if idx not in ret:
                ret[idx] = netId
                # for each neighboring vertex, set the id, but do not set visited so we visit those neighbors later on
                # iterative fashion to avoid overflow errors
                for vrtx in transposed[idx]:
                    if vrtx not in ret:
                        ret[vrtx] = netId
                return True
            else:
                # stack overflow here as well, going to omit this and add fix to loop outside function below
                '''
                for vrtx in transposed[idx]:
                    assignToSubnet(vrtx, netId)
                '''
                # for each neighboring vertex, add it to the subnet of the original vertex since it is reachable
                for vrtx in transposed[idx]:
                    if vrtx not in ret:
                        ret[vrtx] = ret[idx]
                return False
        return False
    
    # for each node in the visitation stack
    # assign it to a subnet and increment the subnetid only if that node did not exist in a specifiec subnet already
    for nd in reversed(stack):
        if assignToSubnet(nd, subnetId):
            subnetId += 1
    
    return ret

# returns the number of K-length chains there are between node id 0 and node id 1
def getKLenRecommendationChain(graphDict, ndId0, ndId1, k):
    # edge cases
    if k <= 0:
        return 0
    if k == 1:
        return 1
    if k == 2:
        cnt = 0
        for neighbor in graphDict[ndId1]:
            if neighbor == ndId1:
                cnt += 1
        return cnt
    # dynamic programming list for determining possible nodes in chain
    res = [[] for i in range(k - 1)]
    # first list in list is of the neighbors for node id 0
    res[0] = [nd for nd in graphDict[ndId0]]
    # visit the nodes in each list of lists, starting with node id 0's neighbors
    for i in range(1, len(res)):
        # build the next list of nodes, by getting the neighbors of each node in the previous list of lists and adding those to the next list
        # those will be iterated over in the next loop
        # can be improved by utilizing a smaller array than res, reuse lists between loops possibly
        for j in range(len(res[i-1])):
            try:
                for nd in graphDict[res[i-1][j]]:
                    res[i].append(nd)
            except KeyError:
                continue
    # count the number of times node id 1 shows up in the final list of lists, which contains the destination node
    cnt = 0
    for nd in res[k-2]:
        # if the node is node id 1, increment count
        if nd == ndId1:
            cnt += 1
    return cnt

# main method for testing and running all code
# organized in order of task, starting with task 2, the first coding part
def main(filePath):
    # Task 2
    print('_-^-_ TASK 2 _-^-_')
    # create graph from the input file I chose
    twitterGraph = createGraphFromFile(filePath)
    # print one of the V:E relationships
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
            print(str(key), end=' ')
    sys.stdout.flush()
    print('\n_-^-_ TASK 5 _-^-_')
    kosarajuRes = getStronglyConnectedSubnetwork(bfsRes)
    print(take(100, kosarajuRes.items()))
    print('Strongly connected graphs: ' + str(max(kosarajuRes.values())))
    print('Nodes contained in subnetwork 4: ')
    stronglyConnectedCntDict = {}
    for key, value in kosarajuRes.items():
        if value == 4:
            print(str(key), end=' ')
        if value not in stronglyConnectedCntDict.keys():
            stronglyConnectedCntDict[value] = 0
        else:
            stronglyConnectedCntDict[value] += 1
    print('\nStrongly connected component with most nodes: ' + str(stronglyConnectedCntDict[max(stronglyConnectedCntDict.values())]) + ' with ' + str(max(stronglyConnectedCntDict.values())) + ' nodes')
    print('_-^-_ TASK 6 _-^-_')
    print('Number of 3-length recommendation chains from 439779382 to 127003249: ' + str(getKLenRecommendationChain(bfsRes, 439779382, 127003249, 3)))
     
path = 'C:/Users/Matt/Documents/GitHub/Social-Network-Analysis/twitter_combined.txt'
#path = 'C:/Users/Matt/Documents/GitHub/Social-Network-Analysis/test.txt'
main(path)