"""Zaimplementuj kopiec binarny o ograniczonej wielkości n. Innymi słowy,
stwórz strukturę przechowującą n najważniejszych (największych) wartości.
"""

class BinHeapMaxSize:
    """Class to create binary heap with limited size - the highest n elements"""
    def __init__(self, maximum):
        self.heap_list = [0]
        self.current_size = 0
        self.max = maximum

    def perc_up(self, i):
        while i // 2 > 0:
            if self.heap_list[i] < self.heap_list[i // 2]:
                tmp = self.heap_list[i // 2]
                self.heap_list[i // 2] = self.heap_list[i]
                self.heap_list[i] = tmp
            i = i // 2

    def insert(self, k):
        if self.current_size < self.max:
            self.heap_list.append(k)
            self.current_size = self.current_size + 1
            self.perc_up(self.current_size)
        else:
            if self.heap_list[1] < k:
                self.del_minimum()
                self.insert(k)
            else:
                pass

    def find_minimum(self):
        return self.heap_list[1]

    def perc_down(self, i):
        while (i * 2) <= self.current_size:
            mc = self.min_child(i)
            if self.heap_list[i] > self.heap_list[mc]:
                tmp = self.heap_list[i]
                self.heap_list[i] = self.heap_list[mc]
                self.heap_list[mc] = tmp
            i = mc

    def min_child(self, i):
        if i * 2 + 1 > self.current_size:
            return i * 2
        else:
            if self.heap_list[i * 2] < self.heap_list[i * 2 + 1]:
                return i * 2
            else:
                return i * 2 + 1

    def del_minimum(self):
        retval = self.heap_list[1]
        self.heap_list[1] = self.heap_list[self.current_size]
        self.current_size = self.current_size - 1
        self.heap_list.pop()
        self.perc_down(1)
        return retval

    def build_heap(self, alist):
        for element in alist:
            self.insert(element)

    def size(self):
        return self.current_size

    def is_empty(self):
        return self.current_size == 0

    def __str__(self):
        txt = "{}".format(self.heap_list[1:])
        return txt

to_heap = [5, 6, 10, 11, 17, 26, 20, 30, 34, 101, 27, 39]
heap = BinHeapMaxSize(5)

heap.build_heap(to_heap)
print(heap.heap_list)
