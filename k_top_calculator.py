from heap import heap_object

class TopKCalculator:                        # Define standard interface
    def __init__(self,k):
        self._k = k
        self._heap_object = heap_object()    # Instantiate heap
    def caculate_if_insert_KTOP(self,data):
        pass
    def get_KTOP(self):
        pass
    def set_k(self,k):
        pass


class calculator(TopKCalculator):
    def __init__(self,k):
        super().__init__(k)
    def insert(self, data):
        if self._heap_object.get_length() < self._k:    # If the heap currently has fewer than k elements, compare each product's sales with the top of the min-heap. If a product's sales exceed the top of the min-heap, the top element is popped and the new product is added to the top-k.
            self._heap_object.insert(data)
        else:
            if data > self._heap_object.get_top():   
                self._heap_object.pop_out()
                self._heap_object.insert(data)
    def get_KTOP(self):          # Since we are using a min-heap, we print the top-k list in descending order (from largest to smallest)
       current_list = self._heap_object.get_list()
       return sorted(current_list, reverse=True) # Copy the internal list and use Python's built-in sort to return the result in descending order directly
                                                 # Time complexity is O(K log K), and since K is usually small, performance is excellent
    def set_k(self, k):
        self._k = k