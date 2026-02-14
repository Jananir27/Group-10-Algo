"""
Task 2: Disjoint Set ADT (Union-Find)

Required operations:
- MAKE-SET(x)  : Theta(1)
- FIND-SET(x)  : O(alpha(n)) amortized (path compression)
- UNION(x, y)  : O(alpha(n)) amortized (union by rank)

Data structure:
- parent[x] stores the parent of x (roots satisfy parent[x] == x)
- rank[x] is an upper bound on tree height (used only for roots)
"""


class DisjointSet:
    def __init__(self):
        self.parent = {}
        self.rank = {}

    def make_set(self, x):
        """MAKE-SET(x) in Theta(1)"""
        if x in self.parent:
            return  # avoid overwriting existing element
        self.parent[x] = x
        self.rank[x] = 0

    def find_set(self, x):
        """FIND-SET(x) amortized O(alpha(n)) using path compression"""
        if x not in self.parent:
            raise KeyError(f"{x} is not in any set. Call make_set({x}) first.")

        if self.parent[x] != x:
            self.parent[x] = self.find_set(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x, y):
        """UNION(x,y) amortized O(alpha(n)) using union by rank.
        Returns True if merged, False if already same set.
        """
        rx = self.find_set(x)
        ry = self.find_set(y)

        if rx == ry:
            return False

        # Union by rank
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1

        return True

    def in_same_set(self, x, y):
        """Convenience method"""
        return self.find_set(x) == self.find_set(y)

    def get_sets(self):
        """Return current partition as list of sets (good for demonstration)"""
        groups = {}
        for x in self.parent:
            r = self.find_set(x)
            groups.setdefault(r, set()).add(x)
        return list(groups.values())


if __name__ == "__main__":
    # Small demo (use this in your report)
    ds = DisjointSet()
    for i in range(1, 6):
        ds.make_set(i)

    ds.union(1, 2)
    ds.union(3, 4)

    print(ds.find_set(1), ds.find_set(2))  # same rep
    print(ds.find_set(3), ds.find_set(4))  # same rep
    print(ds.find_set(5))                  # alone

    ds.union(2, 3)
    print("After union(2,3):", ds.in_same_set(1, 4))  # True
    print("Current sets:", ds.get_sets())
