class heapk():
    def __init__(self):  # Define standard interface
        self._heap = []
    def left(self, i): pass
    def right(self, i): pass
    def parent(self, i): pass
    def insert(self, data): pass
    def sift_up(self): pass
    def sift_down(self): pass
    def pop_out(self): pass


class heap_object(heapk):
    def __init__(self):
        super().__init__()

    def left(self, i):            # For a complete binary tree, the index of the left child is 2*i + 1
        return 2 * i + 1

    def right(self, i):           # For a complete binary tree, the index of the right child is 2*i + 2
        return 2 * i + 2

    def parent(self, i):          # For a heap, the index of the parent node is the integer part of (i-1)//2
        return (i - 1) // 2

    def insert(self, data):       # Heap insertion: first append the new element to the end of the list, then sift up
        self._heap.append(data)
        self.sift_up(len(self._heap) - 1)

    def sift_up(self, i=None):    # Sift-up operation: let the element at index i compare with its parent; if smaller than parent, swap and continue upward until larger than parent or root is reached.
        if i is None:
            i = len(self._heap) - 1
        while i > 0:
            p = self.parent(i)
            if self._heap[p] > self._heap[i]:
                self._heap[i], self._heap[p] = self._heap[p], self._heap[i]
                i = p
            else:
                break

    def sift_down(self, i=0):     # Sift-down operation: compare the two children to get the smallest child, then compare parent with that child; if child is smaller, swap and continue downward.
        n = len(self._heap)
        while True:
            smallest = i
            left = self.left(i)
            right = self.right(i)
            if left < n and self._heap[left] < self._heap[smallest]:
                smallest = left
            if right < n and self._heap[right] < self._heap[smallest]:
                smallest = right
            if smallest == i:
                break
            self._heap[i], self._heap[smallest] = self._heap[smallest], self._heap[i]
            i = smallest

    def pop_out(self):            # Pop the top element of the min-heap
        if not self._heap:
            raise IndexError("pop from empty heap")   
        top = self._heap[0]
        last = self._heap.pop()
        if self._heap:
            self._heap[0] = last
            self.sift_down(0)
        return top

    def get_list(self):           # Return a copy of the heap list
        return list(self._heap)
    
    def get_top(self):            # Return the top element of the heap
        if not self._heap:
            return None
        return self._heap[0]

    def get_length(self):         # Return the length of the heap list
        return len(self._heap)