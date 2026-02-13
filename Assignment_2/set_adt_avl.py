"""
Set ADT implemented using an AVL Tree (self-balancing BST).

All operations run in O(log n) worst-case time.
"""

class Node:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.left = None
        self.right = None
        self.height = 1


class AVLSet:
    def __init__(self):
        self.root = None

    # Utility functions

    def _height(self, node):
        return node.height if node else 0

    def _update_height(self, node):
        node.height = 1 + max(self._height(node.left),
                              self._height(node.right))

    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right)

    def _rotate_right(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        self._update_height(y)
        self._update_height(x)

        return x

    def _rotate_left(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        self._update_height(x)
        self._update_height(y)

        return y

    def _rebalance(self, node):
        self._update_height(node)
        balance = self._balance_factor(node)

        # Left heavy
        if balance > 1:
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right heavy
        if balance < -1:
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    # Required ADT operations

    # build(X) – O(n log n)
    def build(self, X):
        for key, data in X:
            self.insert(key, data)

    # find(k) – O(log n)
    def find(self, key):
        node = self.root
        while node:
            if key == node.key:
                return node.key, node.data, True
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return None, None, False

    # insert(x) – O(log n)
    def insert(self, key, data):
        def _insert(node, key, data):
            if not node:
                return Node(key, data)

            if key < node.key:
                node.left = _insert(node.left, key, data)
            elif key > node.key:
                node.right = _insert(node.right, key, data)
            else:
                return node  # ignore duplicate key

            return self._rebalance(node)

        self.root = _insert(self.root, key, data)

    # delete(k) – O(log n)
    def delete(self, key):
        def _min_value_node(node):
            while node.left:
                node = node.left
            return node

        def _delete(node, key):
            if not node:
                return None

            if key < node.key:
                node.left = _delete(node.left, key)
            elif key > node.key:
                node.right = _delete(node.right, key)
            else:
                # node found
                if not node.left:
                    return node.right
                elif not node.right:
                    return node.left

                successor = _min_value_node(node.right)
                node.key, node.data = successor.key, successor.data
                node.right = _delete(node.right, successor.key)

            return self._rebalance(node)

        self.root = _delete(self.root, key)

    # find_min() – O(log n)
    def find_min(self):
        node = self.root
        if not node:
            return None, None, False

        while node.left:
            node = node.left
        return node.key, node.data, True

    # find_max() – O(log n)
    def find_max(self):
        node = self.root
        if not node:
            return None, None, False

        while node.right:
            node = node.right
        return node.key, node.data, True

    # find_next(k) – O(log n)
    def find_next(self, key):
        node = self.root
        successor = None

        while node:
            if key < node.key:
                successor = node
                node = node.left
            else:
                node = node.right

        if successor:
            return successor.key, successor.data, True
        return None, None, False

    # find_prev(k) – O(log n)
    def find_prev(self, key):
        node = self.root
        predecessor = None

        while node:
            if key > node.key:
                predecessor = node
                node = node.right
            else:
                node = node.left

        if predecessor:
            return predecessor.key, predecessor.data, True
        return None, None, False


# Simple usage example

if __name__ == "__main__":
    s = AVLSet()
    s.build([(5, "A"), (2, "B"), (8, "C"), (1, "D"), (3, "E")])

    print("Find 3:", s.find(3))
    print("Min:", s.find_min())
    print("Max:", s.find_max())
    print("Next of 3:", s.find_next(3))
    print("Prev of 3:", s.find_prev(3))

    s.delete(2)
    print("After deleting 2:", s.find_prev(3))

