# from cpython.heapq
class heap:
  
    def __init__(self, L = None):
        if L != None:
            lst = L
        else:
            lst = []
  
    def getLength(self):
        return len(self.lst)
    
    def getValue(self, idx):
        return self.lst[idx]
    
    def setValue(self, idx, newvalue):
        self.lst[idx] = newvalue
        return newvalue
    
    def insert(self, newvalue):
        self.lst.append(newvalue)
        self._siftdown(0, self.getLength() - 1)
    
    def extractMax(self):
        endval = self.lst.pop()
        if self.lst:
            ret = self.getValue(0)
            self.setValue(0, endval)
            self._siftup(0)
            return ret
        return endval
    
    def heappoppush(self, newvalue):
        ret = self.getValue(0)
        self.setValue(0, newvalue)
        self._siftup(0)
        return ret
    
    def heappushpop(self, newvalue):
        if self.lst and self.getValue(0) < newvalue:
            newvalue, self.lst[0] = self.lst[0], newvalue
            self._siftup(0)
        return newvalue
    
    def heapify(self):
        n = self.getLength()
        for i in reversed(range(n // 2)):
            self._siftup(i)
    
    def _siftdown(self, startidx, idx):
        newval = self.lst[idx]
        # move up tree to root, moving passed nodes down until fitting newval
        while idx > startidx:
            pidx = (idx - 1) >> 1
            parent = self.lst[pidx]
            if parent < newval:
                self.lst[idx] = parent
                pos = pidx
                continue
            break
        self.lst[pos] = newval
    
    def _siftup(self, idx):
        endidx = len(self.lst)
        startidx = idx
        newval = self.getValue(idx)
        # move down the tree following the larger child until hitting leaf
        # leftmost child index
        cidx = 2 * idx + 1
        while cidx < endidx:
            # set cidx to index of larger child
            ridx = cidx + 1
            if ridx < endidx and not self.getValue(ridx) < self.getValue(cidx):
                cidx = ridx
            # move larger child up tree
            self.setValue(idx, self.getValue(cidx))
            idx = cidx
            cidx = 2 * idx + 1
        # leaf at idx is empty, put newval there, and move it up tree to fitted
        # spot
        self.setValue(idx, newval)
        self._siftdown(startidx, idx)
        