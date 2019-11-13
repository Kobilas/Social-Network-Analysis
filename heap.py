# from cpython.heapq
class heap:
  
    def __init__(self, L = None):
        self.lst = []
        if L != None:
            self.lst = L
  
    def getLength(self):
        return len(self.lst)
    
    def insert(self, newnode):
        self.lst.append(newnode)
        self._siftdown(0, self.getLength() - 1)
    
    def extractMax(self):
        endnode = self.lst.pop()
        if self.lst:
            ret = self.lst[0]
            self.lst[0] = endnode
            self._siftup(0)
            return ret
        return endnode
    
    def heappoppush(self, newnode):
        ret = self.lst[0]
        self.lst[0] = newnode
        self._siftup(0)
        return ret
    
    def heappushpop(self, newnode):
        if self.lst and self.lst[0].followers < newnode.followers:
            newnode, self.lst[0] = self.lst[0], newnode
            self._siftup(0)
        return newnode
    
    def heapify(self):
        n = self.getLength()
        for i in reversed(range(n // 2)):
            self._siftup(i)
    
    def _siftdown(self, startidx, idx):
        newnode = self.lst[idx]
        # move up tree to root, moving passed nodes down until fitting newval
        while idx > startidx:
            pidx = (idx - 1) >> 1
            parentnode = self.lst[pidx]
            if parentnode.followers < newnode.followers:
                self.lst[idx] = parentnode
                idx = pidx
                continue
            break
        self.lst[idx] = newnode
    
    def _siftup(self, idx):
        endidx = self.getLength()
        startidx = idx
        newnode = self.lst[idx]
        # move down the tree following the larger child until hitting leaf
        # leftmost child index
        cidx = 2 * idx + 1
        while cidx < endidx:
            # set cidx to index of larger child
            ridx = cidx + 1
            if ridx < endidx and not self.lst[ridx].followers < self.lst[cidx].followers:
                cidx = ridx
            # move larger child up tree
            self.lst[idx] = self.lst[cidx]
            idx = cidx
            cidx = 2 * idx + 1
        # leaf at idx is empty, put newval there, and move it up tree to fitted
        # spot
        self.lst[idx] = newnode
        self._siftdown(startidx, idx)

class node:
    
    def __init__(self, id = -1, followers = -1):
        self.id = id
        self.followers = followers
        
    def __str__(self):
        return "id: " + str(self.id) + "; followers: " + str(self.followers)
    
    def __lt__(self, other):
        return self.followers < other.followers
    
    def __le__(self, other):
        return self.followers <= other.followers
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __ne__(self, other):
        return self.id != other.id
    
    def __ge__(self, other):
        return self.followers >= other.followers
    
    def __gt__(self, other):
        return self.followers > other.followers
        