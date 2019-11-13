class heap:
  
    def __init__(self, L = None):
        self.lst = []
        if L != None:
            self.lst = L
  
    def getLength(self):
        return len(self.lst)
    
    def insert(self, newnd):
        self.lst.append(newnd)
        self._siftdown(0, self.getLength() - 1)
    
    def extractMax(self):
        endnd = self.lst.pop()
        if self.lst:
            ret = self.lst[0]
            self.lst[0] = endnd
            self._siftup(0)
            return ret
        return endnd
    
    def heapify(self):
        n = self.getLength()
        for i in reversed(range(n // 2)):
            self._siftup(i)
    
    def _siftdown(self, startidx, idx):
        newnd = self.lst[idx]
        # move up tree to root, moving passed nds down until fitting newval
        while idx > startidx:
            pidx = (idx - 1) >> 1
            parentnd = self.lst[pidx]
            if parentnd.followers < newnd.followers:
                self.lst[idx] = parentnd
                idx = pidx
                continue
            break
        self.lst[idx] = newnd
    
    def _siftup(self, idx):
        endidx = self.getLength()
        startidx = idx
        newnd = self.lst[idx]
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
        self.lst[idx] = newnd
        self._siftdown(startidx, idx)

class node:
    
    def __init__(self, id = -1, followers = -1):
        self.id = id
        self.followers = followers
        
    def __str__(self):
        return "id: " + str(self.id) + "\tfollowers: " + str(self.followers)
    
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
        