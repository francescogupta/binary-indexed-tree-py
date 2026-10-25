# binary-indexed-tree-py

A 1-indexed Binary Indexed Tree (Fenwick tree) that answers prefix-sum queries and applies point updates in O(log n), with no third-party dependencies.

```python
from binary_indexed_tree_py import BIT

t = BIT(5)
t.update(1, 10)
t.update(2, 20)
t.update(3, 30)
t.prefix_sum(3)   # 60
t.range_sum(2, 3) # 50
```

`BinaryIndexedTree` and its alias `BIT` are the two exported names. Construct with a length `n` (zero-filled), or use `from_iterable(values)` to preload data in O(n). Methods: `update(i, delta)`, `prefix_sum(i)`, `range_sum(l, r)`, `__len__`.

## Why this exists

When you need repeated prefix-sum queries interleaved with point mutations on a fixed-size array, the naive re-summation approach is O(n) per query. This library holds the line at O(log n) for both operations using the standard Fenwick structure: each internal node covers a range whose length is the least significant set bit of its index, so updates and queries each touch at most ⌈log₂ n⌉ nodes.

The trade-off is flexibility. The array length is fixed at construction; there is no `push` or `resize`. If the size must change, build a new tree. The tree also stores only sums, not the original elements, so there is no `get(i)` to read back a single value — if you need that, keep the source array alongside.

## The awkward edge

Indices are **1-based**. `update(0, x)` and `prefix_sum(-1)` raise. This is deliberate: the Fenwick update step `i += i & -i` is only correct when the root sentinel lives at index 0, so callers must work in 1-based space. `prefix_sum(0)` is allowed and returns 0 (the empty prefix). `prefix_sum(i)` for `i > n` silently clamps to `n` rather than raising, because a prefix longer than the array is unambiguously the whole array.

## Design notes

The window stores values eagerly rather than keeping running aggregates. Running
sums drift with floating point over long streams, and recomputing from a small
buffer is cheap enough that the drift is not worth the speed.

