"""Stwórz własną klasę implementującą binarne drzewa przeszukiwań.
Zadbaj o poprawne przetwarzanie powtarzających się kluczy."""


class TreeNode:  # helping class
    """Class to create instance of Node - one element of Binary search tree"""
    def __init__(self, key, left=None, right=None, parent=None):  # create the tree
        self.key = key  # we use keys to sort and build tree (Node)
        self.payload = 1  # counter
        self.leftChild = left
        self.rightChild = right
        self.parent = parent  # relations between Nodes

    def hasLeftChild(self):
        return self.leftChild  # return value of lef child

    def hasRightChild(self):
        return self.rightChild  # return value of right child

    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self  # check that it is lef child

    def isRightChild(self):
        return self.parent and self.parent.rightChild == self  # check right child

    def isRoot(self):
        return not self.parent  # checking root (no parents)

    def isLeaf(self):
        return not (self.rightChild or self.leftChild)  # is leaf if have not child

    def hasAnyChildren(self):
        return self.rightChild or self.leftChild  # check that have 1 or 2 children

    def hasBothChildren(self):
        return self.rightChild and self.leftChild  # check that have 2 children

    def spliceOut(self):
        if self.isLeaf():
            if self.isLeftChild():
                self.parent.leftChild = None
            else:
                self.parent.rightChild = None
        elif self.hasAnyChildren():
            if self.hasLeftChild():
                if self.isLeftChild():
                    self.parent.leftChild = self.leftChild
                else:
                    self.parent.rightChild = self.leftChild
                self.leftChild.parent = self.parent
            else:
                if self.isLeftChild():
                    self.parent.leftChild = self.rightChild
                else:
                    self.parent.rightChild = self.rightChild
                self.rightChild.parent = self.parent

    def findSuccessor(self):
        succ = None
        if self.hasRightChild():
            succ = self.rightChild.findMin()
        else:
            if self.parent:
                if self.isLeftChild():
                    succ = self.parent
                else:
                    self.parent.rightChild = None
                    succ = self.parent.findSuccessor()
                    self.parent.rightChild = self

        return succ

    def replaceNodeData(self, key, value, lc, rc):
        self.key = key
        self.payload = value
        self.leftChild = lc
        self.rightChild = rc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self


class BinarySearchTree:  # actual class
    """Class to create binary search tree."""
    def __init__(self):  # create object BST
        self.root = None
        self.size = 0

    def length(self):
        return self.size  # our function len

    def __len__(self):
        return self.size  # build-in function len

    def __iter__(self):
        return self.root.__iter__()  # iteration

    def put(self, key):
        if self.root:
            self._put(key, self.root)  # _put is a helper function
        else:
            self.root = TreeNode(key)
        self.size = self.size + 1  # adding new element

    def _put(self, key, currentNode):
        if key < currentNode.key:
            if currentNode.hasLeftChild():
                self._put(key, currentNode.leftChild)
            else:
                currentNode.leftChild = TreeNode(key, parent=currentNode)
        elif key > currentNode.key:
            if currentNode.hasRightChild():
                self._put(key, currentNode.rightChild)
            else:
                currentNode.rightChild = TreeNode(key, parent=currentNode)
        elif key == currentNode.key:  # if exist Node with same key, add 1 to payload
            currentNode.payload += 1

    def __setitem__(self, k):  # overloading of [] operator
        self.put(k)

    def get(self, key):
        if self.root:
            res = self._get(key, self.root)
            if res:
                return res.payload
            else:
                return None
        else:
            return None

    def _get(self, key, currentNode):
        if not currentNode:
            return None
        elif currentNode.key == key:
            return currentNode
        elif key < currentNode.key:
            return self._get(key, currentNode.leftChild)
        else:
            return self._get(key, currentNode.rightChild)

    def __getitem__(self, key):  # overloading of [] operator
        return self.get(key)

    def __contains__(self, key):  # overloading of in operator
        if self._get(key, self.root):
            return True
        else:
            return False

    def delete(self, key):
        if self.size > 1:
            nodeToRemove = self._get(key, self.root)
            if nodeToRemove:
                if nodeToRemove.payload == 1:
                    self.remove(nodeToRemove)
                    self.size = self.size - 1
                elif nodeToRemove.payload > 1:
                    nodeToRemove.payload -= 1
            else:
                raise KeyError('Error, key not in tree')
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size = self.size - 1
        else:
            raise KeyError('Error, key not in tree')

    def __delitem__(self, key):  # overloading of del operator
        self.delete(key)

    def findMin(self):  # looking for the left leaf
        current = self.root
        while current.hasLeftChild():
            current = current.leftChild
        return current

    def findMax(self):
        current = self.root
        while current.hasRightChild():
            current = current.rightChild
        return current

    def remove(self, currentNode):
        if currentNode.isLeaf():  # leaf
            if currentNode == currentNode.parent.leftChild:
                currentNode.parent.leftChild = None
            else:
                currentNode.parent.rightChild = None
        elif currentNode.hasBothChildren():  # interior
            succ = currentNode.findSuccessor()
            succ.spliceOut()
            currentNode.key = succ.key
            currentNode.payload = succ.payload
        else:  # this node has one child
            if currentNode.hasLeftChild():
                if currentNode.isLeftChild():
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.leftChild
                elif currentNode.isRightChild():
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.leftChild
                else:
                    currentNode.replaceNodeData(currentNode.leftChild.key, currentNode.leftChild.payload,
                                                currentNode.leftChild.leftChild, currentNode.leftChild.rightChild)
            else:
                if currentNode.isLeftChild():
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.rightChild
                elif currentNode.isRightChild():
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.rightChild
                else:
                    currentNode.replaceNodeData(currentNode.rightChild.key, currentNode.rightChild.payload,
                                                currentNode.rightChild.leftChild, currentNode.rightChild.rightChild)

    def __str__(self):
        lines, _, _, _ = self.display(self.root)
        for line in lines:
            print(line)

        return '\nWhere: key(payload)'

    def display(self, currentNode):
        # No child.
        if currentNode.rightChild is None and currentNode.leftChild is None:
            line = '{}({})'.format(currentNode.key, currentNode.payload)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if currentNode.rightChild is None:
            lines, n, p, x = self.display(currentNode.leftChild)
            s = '{}({})'.format(currentNode.key, currentNode.payload)
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if currentNode.leftChild is None:
            lines, n, p, x = self.display(currentNode.rightChild)
            s = '{}({})'.format(currentNode.key, currentNode.payload)
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.display(currentNode.leftChild)
        right, m, q, y = self.display(currentNode.rightChild)
        s = '{}({})'.format(currentNode.key, currentNode.payload)
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]

        return lines, n + m + u, max(p, q) + 2, n + u // 2


tree = BinarySearchTree()
tree.put(5)
tree.put(2)
tree.put(3)
tree.put(4)
tree.put(100)
tree.put(7)
tree.put(2)
tree.put(2)
payload_of_2 = tree.get(2)
#print('payload of 2 is: {}'.format(payload_of_2))

print(tree)