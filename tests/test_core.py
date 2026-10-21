import unittest

from binary_indexed_tree_py import BIT, BinaryIndexedTree


class TestConstruction(unittest.TestCase):
    def test_default_zero_filled(self):
        t = BinaryIndexedTree(5)
        self.assertEqual(len(t), 5)
        for i in range(1, 6):
            self.assertEqual(t.prefix_sum(i), 0)

    def test_zero_length_tree(self):
        t = BinaryIndexedTree(0)
        self.assertEqual(len(t), 0)
        self.assertEqual(t.prefix_sum(0), 0)

    def test_negative_length_rejected(self):
        with self.assertRaises(ValueError):
            BinaryIndexedTree(-1)

    def test_non_integer_length_rejected(self):
        with self.assertRaises(ValueError):
            BinaryIndexedTree(3.5)
        with self.assertRaises(ValueError):
            BinaryIndexedTree("3")

    def test_bool_length_rejected(self):
        with self.assertRaises(ValueError):
            BinaryIndexedTree(True)


class TestFromIterable(unittest.TestCase):
    def test_matches_sequential_insert(self):
        values = [3, 1, 4, 1, 5, 9, 2, 6]
        built = BinaryIndexedTree.from_iterable(values)
        manual = BinaryIndexedTree(len(values))
        for i, v in enumerate(values, start=1):
            manual.update(i, v)
        for i in range(1, len(values) + 1):
            self.assertEqual(built.prefix_sum(i), manual.prefix_sum(i))

    def test_empty_iterable(self):
        t = BinaryIndexedTree.from_iterable([])
        self.assertEqual(len(t), 0)
        self.assertEqual(t.prefix_sum(0), 0)

    def test_single_element(self):
        t = BinaryIndexedTree.from_iterable([42])
        self.assertEqual(t.prefix_sum(1), 42)

    def test_non_integer_value_rejected(self):
        with self.assertRaises(ValueError):
            BinaryIndexedTree.from_iterable([1, 2, "x"])


class TestUpdateAndPrefix(unittest.TestCase):
    def test_point_updates_accumulate(self):
        t = BIT(4)
        t.update(1, 10)
        t.update(2, 20)
        t.update(3, 30)
        t.update(4, 40)
        self.assertEqual(t.prefix_sum(1), 10)
        self.assertEqual(t.prefix_sum(2), 30)
        self.assertEqual(t.prefix_sum(3), 60)
        self.assertEqual(t.prefix_sum(4), 100)

    def test_negative_deltas(self):
        t = BinaryIndexedTree.from_iterable([5, 5, 5])
        t.update(2, -3)
        self.assertEqual(t.prefix_sum(1), 5)
        self.assertEqual(t.prefix_sum(2), 7)
        self.assertEqual(t.prefix_sum(3), 12)

    def test_update_out_of_range_raises(self):
        t = BinaryIndexedTree(3)
        with self.assertRaises(IndexError):
            t.update(0, 1)
        with self.assertRaises(IndexError):
            t.update(4, 1)

    def test_non_integer_delta_rejected(self):
        t = BinaryIndexedTree(3)
        with self.assertRaises(ValueError):
            t.update(1, 1.5)
        with self.assertRaises(ValueError):
            t.update(1, "2")
        with self.assertRaises(ValueError):
            t.update(1, True)

    def test_non_integer_index_rejected(self):
        t = BinaryIndexedTree(3)
        with self.assertRaises(ValueError):
            t.update(1.0, 5)
        with self.assertRaises(ValueError):
            t.prefix_sum("2")

    def test_prefix_sum_zero_is_empty_prefix(self):
        t = BinaryIndexedTree.from_iterable([1, 2, 3])
        self.assertEqual(t.prefix_sum(0), 0)

    def test_prefix_sum_beyond_n_clamps(self):
        t = BinaryIndexedTree.from_iterable([1, 2, 3])
        self.assertEqual(t.prefix_sum(10), 6)

    def test_prefix_sum_negative_raises(self):
        t = BinaryIndexedTree(3)
        with self.assertRaises(IndexError):
            t.prefix_sum(-1)


class TestRangeSum(unittest.TestCase):
    def test_full_range(self):
        t = BinaryIndexedTree.from_iterable([1, 2, 3, 4, 5])
        self.assertEqual(t.range_sum(1, 5), 15)

    def test_subrange(self):
        t = BinaryIndexedTree.from_iterable([1, 2, 3, 4, 5])
        self.assertEqual(t.range_sum(2, 4), 9)

    def test_single_element_range(self):
        t = BinaryIndexedTree.from_iterable([1, 2, 3, 4, 5])
        self.assertEqual(t.range_sum(3, 3), 3)

    def test_empty_range_returns_zero(self):
        t = BinaryIndexedTree.from_iterable([1, 2, 3])
        self.assertEqual(t.range_sum(2, 1), 0)

    def test_range_clamps_right_bound(self):
        t = BinaryIndexedTree.from_iterable([1, 2, 3])
        self.assertEqual(t.range_sum(1, 100), 6)

    def test_range_left_below_one_raises(self):
        t = BinaryIndexedTree(3)
        with self.assertRaises(IndexError):
            t.range_sum(0, 2)

    def test_range_non_integer_bounds_rejected(self):
        t = BinaryIndexedTree(3)
        with self.assertRaises(ValueError):
            t.range_sum(1.0, 2)
        with self.assertRaises(ValueError):
            t.range_sum(1, 2.0)


class TestLargeInput(unittest.TestCase):
    def test_large_sequential_build(self):
        n = 1000
        t = BinaryIndexedTree.from_iterable(range(1, n + 1))
        expected = n * (n + 1) // 2
        self.assertEqual(t.prefix_sum(n), expected)
        self.assertEqual(t.range_sum(500, 600), sum(range(500, 601)))


if __name__ == "__main__":
    unittest.main()
