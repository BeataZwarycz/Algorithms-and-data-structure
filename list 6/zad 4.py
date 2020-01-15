"""Napisz funkcję, która na wejściu przyjmuje drzewo wyprowadzenia jakiegoś wyrażenia matematycznego,
a na wyjściu zwraca pochodną tego wyrażenia względem podanej zmiennej."""

import operator


class BinaryTree:
    def __init__(self, rootObj):
        self.key = rootObj
        self.leftChild = None
        self.rightChild = None

    def insertLeft(self, newNode):
        if self.leftChild == None:
            self.leftChild = BinaryTree(newNode)

        else:
            t = BinaryTree(newNode)
            t.leftChild = self.leftChild
            self.leftChild = t

    def insertRight(self, newNode):
        if self.rightChild == None:
            self.rightChild = BinaryTree(newNode)

        else:
            t = BinaryTree(newNode)
            t.rightChild = self.rightChild
            self.rightChild = t

    def getRightChild(self):
        return self.rightChild

    def getLeftChild(self):
        return self.leftChild

    def setRootVal(self, obj):
        self.key = obj

    def getRootVal(self):
        return self.key

    def display(self):
        lines, _, _, _ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.rightChild is None and self.leftChild is None:
            line = '%s' % self.key
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.rightChild is None:
            lines, n, p, x = self.leftChild._display_aux()
            s = '%s' % self.key
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.leftChild is None:
            lines, n, p, x = self.rightChild._display_aux()
            s = '%s' % self.key
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.leftChild._display_aux()
        right, m, q, y = self.rightChild._display_aux()
        s = '%s' % self.key
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


class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)


class BuildParseTree:
    """Class to build tree from given math formula in string"""
    def __init__(self, fpexp, var):
        self.variable = var
        self.input_exp = fpexp
        self.fpexp = fpexp
        self.pStack = Stack()
        self.eTree = BinaryTree('')
        self.pStack.push(self.eTree)
        self.currentTree = self.eTree

        self.buildParseTree()

    def buildParseTree(self):
        for i in self.fpexp:
            if i == '(':
                self.currentTree.insertLeft('')
                self.pStack.push(self.currentTree)
                self.currentTree = self.currentTree.getLeftChild()

            elif i not in ['+', '-', '*', '/', ')', self.variable]:
                self.currentTree.setRootVal(float(i))
                self.parent = self.pStack.pop()
                self.currentTree = self.parent

            elif i in ['+', '-', '*', '/']:
                self.currentTree.setRootVal(i)
                self.currentTree.insertRight('')
                self.pStack.push(self.currentTree)
                self.currentTree = self.currentTree.getRightChild()

            elif i == ')':
                self.currentTree = self.pStack.pop()

            elif i == self.variable:
                self.currentTree.setRootVal(i)
                self.parent = self.pStack.pop()
                self.currentTree = self.parent

            else:
                raise ValueError

        self.currentTree = self.eTree

    def __str__(self):
        self.currentTree.display()

        return " "


def preorder(tree):
    if tree:
        print(tree.getRootVal())
        preorder(tree.getLeftChild())
        preorder(tree.getRightChild())


def postorder(tree):
    if tree != None:
        postorder(tree.getLeftChild())
        postorder(tree.getRightChild())
        print(tree.getRootVal())


def postordereval(tree):
    opers = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}
    res1 = None
    res2 = None
    if tree:
        res1 = postordereval(tree.getLeftChild())
        res2 = postordereval(tree.getRightChild())
        if res1 and res2:
            return opers[tree.getRootVal()](res1, res2)
        else:
            return tree.getRootVal()


def inorder(tree, var):
    """Method to count derivative from given binary tree"""
    opers = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}
    if tree != None:
        inorder(tree.getRightChild(), var)
        if tree.getRightChild() and tree.getLeftChild():

            if type(tree.getRightChild().key) in [int, float] and type(tree.getLeftChild().key) in [int, float]:
                tree.key = opers[tree.key](tree.getRightChild().key, tree.getLeftChild().key)
                tree.leftChild = None
                tree.rightChild = None

            elif (tree.getRightChild().key or tree.getLeftChild().key) == var:
                right = tree.getRightChild().key
                left = tree.getLeftChild().key
                if right == var:
                    tree.key = left
                else:
                    tree.key = right
        inorder(tree.getLeftChild(), var)
        inorder(tree.getRightChild(), var)


math_formula = BuildParseTree("(3+((4*x)*((5*x)+(2*7))))", 'x')

print(math_formula)

inorder(math_formula.currentTree, math_formula.variable)

print(math_formula)
