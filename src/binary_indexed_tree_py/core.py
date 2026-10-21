"""Core implementation of a Binary Indexed Tree (Fenwick tree)."""


class BinaryIndexedTree:
    """1-indexed Fenwick tree over an array of 64-bit integers.

    Supports prefix-sum queries and point updates in O(log n). The tree is
    immutable in size: construct a new one if the length must change. Values
    may be negative; they are stored as Python ints, so there is no fixed bit
    width and no overflow.

    Only one interpretation choice was made that deserves a call-out: the
    tree is **strictly 1-indexed**. Index 0 is unused internally, so callers
    pass 1-based positions. This matches the canonical Fenwood formulation
    and keeps the `i & -i` update step correct without extra conversions.
    """

    __slots__ = ("_n", "_tree")

    def __init__(self, n):
        """Create a tree of length ``n`` filled with zero.

        Raises ``ValueError`` if ``n`` is not a non-negative integer.
        A length-zero tree is permitted; every query on it returns 0.
        """
        if not isinstance(n, int) or isinstance(n, bool) or n < 0:
            raise ValueError("n must be a non-negative integer")
        self._n = n
        # Slot 0 is a sentinel so that 1-based indexing lines up with the
        # least-significant-bit update logic. Memory cost is one int.
        self._tree = [0] * (n + 1)

    @classmethod
    def from_iterable(cls, values):
        """Build a tree pre-loaded with ``values`` in O(n).

        ``from_iterable([3, 1, 4])`` produces a tree whose prefix sums are
        3, 4, 8 — the same as inserting each element one by one, but built in
        a single linear pass via difference propagation.
        """
        values = list(values)
        obj = cls(len(values))
        tree = obj._tree
        # Load raw, then fix up parent contributions. This is the standard
        # O(n) build: copy then add each node's value into its immediate
        # parent (the node whose index is i + (i & -i)).
        for i, v in enumerate(values, start=1):
            if not isinstance(v, int) or isinstance(v, bool):
                raise ValueError("all values must be integers")
            tree[i] = v
        for i in range(1, obj._n + 1):
            parent = i + (i & -i)
            if parent <= obj._n:
                tree[parent] += tree[i]
        return obj

    def update(self, i, delta):
        """Add ``delta`` to the element at 1-based index ``i``.

        Mutates the tree in place. Raises ``IndexError`` if ``i`` is outside
        ``[1, n]`` or ``ValueError`` if ``delta`` is not an int.
        """
        if not isinstance(delta, int) or isinstance(delta, bool):
            raise ValueError("delta must be an integer")
        if not isinstance(i, int) or isinstance(i, bool):
            raise ValueError("index must be an integer")
        if i < 1 or i > self._n:
            raise IndexError(f"index {i} out of range [1, {self._n}]")
        # Walk upward: each ancestor covers a range that includes i.
        # The step `i & -i` isolates the least significant set bit, which is
        # exactly the span of the current node, so adding it jumps to the
        # next node whose range contains i.
        tree = self._tree
        n = self._n
        while i <= n:
            tree[i] += delta
            i += i & -i

    def prefix_sum(self, i):
        """Return the sum of elements at indices 1..i inclusive.

        ``prefix_sum(0)`` returns 0 — the empty prefix — and never raises.
        For ``i > n`` the result equals ``prefix_sum(n)`` rather than
        raising, because a prefix longer than the array is simply the whole
        array. Negative ``i`` raises ``IndexError``.
        """
        if not isinstance(i, int) or isinstance(i, bool):
            raise ValueError("index must be an integer")
        if i < 0:
            raise IndexError(f"index {i} is negative")
        if i > self._n:
            i = self._n
        tree = self._tree
        s = 0
        # Walk downward: subtract the least-significant bit to move to the
        # node covering the range strictly to the left of i's coverage.
        while i > 0:
            s += tree[i]
            i -= i & -i
        return s

    def range_sum(self, l, r):
        """Return the sum of elements at indices l..r inclusive.

        Both bounds are 1-based. ``range_sum(1, 0)`` returns 0 to support the
        natural ``prefix_sum(r) - prefix_sum(l - 1)`` identity when the range
        is empty. If ``l > r`` the result is 0. If ``r > n`` it is clamped to
        ``n``. ``l < 1`` raises ``IndexError``.
        """
        if not isinstance(l, int) or isinstance(l, bool):
            raise ValueError("l must be an integer")
        if not isinstance(r, int) or isinstance(r, bool):
            raise ValueError("r must be an integer")
        if l < 1:
            raise IndexError(f"left bound {l} is below 1")
        if r < l:
            return 0
        return self.prefix_sum(r) - self.prefix_sum(l - 1)

    def __len__(self):
        return self._n


# Short alias for callers who prefer the classic name.
BIT = BinaryIndexedTree
