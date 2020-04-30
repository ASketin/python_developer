import unittest
from array import array
from hw1.source import ArrayList


class TestArray(unittest.TestCase):

    def test_creating(self):
        self.assertEqual(ArrayList('i').container, array('l'))
        self.assertEqual(ArrayList('u', 'hello \u2641').container,
                         array('u', 'hello \u2641'))
        self.assertEqual(ArrayList('i', [1, 2, 3, 4, 5]).container,
                         array('l', [1, 2, 3, 4, 5]))
        self.assertEqual(ArrayList('f', [1.0, 2.0, 3.14]).container,
                         array('f', [1.0, 2.0, 3.14]))
        print("test creating: done")

    def test_getitem(self):
        source_array = array('l', [1, 2, 3, 4, 5])
        our_class = ArrayList('i', [1, 2, 3, 4, 5])
        for x in range(5):
            self.assertEqual(our_class[x], source_array[x])

        with self.assertRaises(IndexError):
            our_class[-10]
        with self.assertRaises(IndexError):
            our_class[5]
        print("test get item: done")

    def test_len(self):
        our_class = ArrayList('i', [1, 2, 3, 4, 5])
        self.assertEqual(len(our_class), 5)
        print("test len: done")

    def test_contains(self):
        our_class = ArrayList('i', [1, 2, 3, 4, 5])
        self.assertEqual(3 in our_class, True)
        self.assertEqual(3.0 in our_class, False)
        self.assertEqual(-10 in our_class, False)

        class_str = ArrayList('u', 'hello \u2641')
        self.assertEqual(3 in class_str, False)
        self.assertEqual("h" in class_str, True)
        self.assertEqual("l" in class_str, True)

        print("test contains: done")

    def test_iter(self):
        source_array = array('l', [1, 2, 3, 4, 5])
        for idx, x in enumerate(ArrayList('i', [1, 2, 3, 4, 5])):
            self.assertEqual(x, source_array[idx])

        print("test iter: done")

    def test_reverse(self):
        reverse_array = array('l', [5, 4, 3, 2, 1])
        for idx, x in enumerate(reversed(ArrayList('i', [1, 2, 3, 4, 5]))):
            self.assertEqual(x, reverse_array[idx])

        print("test reverse: done")

    def test_index(self):
        our_class = ArrayList('i', [1, 2, 3, 4, 5])
        self.assertEqual(our_class.index(2), 1)
        self.assertEqual(our_class.index("h"), None)
        self.assertEqual(our_class.index(-2), None)

        class_str = ArrayList('u', 'hello \u2641')
        self.assertEqual(class_str.index(3), None)
        self.assertEqual(class_str.index("h"), 0)
        self.assertEqual(class_str.index("l"), 2)

        print("test index: done")

    def test_count(self):
        our_class = ArrayList('i', [1, 2, 3, 4, 5])
        self.assertEqual(our_class.count(2), 1)
        self.assertEqual(our_class.count("h"), None)
        self.assertEqual(our_class.count(-2), 0)

        class_str = ArrayList('u', 'hello \u2641')
        self.assertEqual(class_str.count(3), None)
        self.assertEqual(class_str.count("h"), 1)
        self.assertEqual(class_str.count("l"), 2)

        arr_float_1 = ArrayList('f', [1.1, 2.2, 3.3, 1.1, 5.5])
        self.assertEqual(arr_float_1.count(1.1), 2)

        print("test count: done")

    def test_set_item(self):
        base = ArrayList('i', [1, 2, 3, 4, 5])
        base[0] = 100
        self.assertEqual(base[0], 100)

        print("test set item: done")

    def test_del_item(self):
        base = ArrayList('i', [1, 2, 3, 4, 5])
        base.__delitem__(1)
        self.assertEqual(base.container, array('i', [1, 3, 4, 5]))

        print("test del item: done")

    def test_insert(self):
        base = ArrayList('i', [1, 2, 3, 4, 5])
        base.insert(2, 100)
        result = array('i', [1, 2, 100, 3, 4, 5])
        self.assertEqual(base.container, result)
        print("test del insert: done")

        class_str = ArrayList('u', 'hello')
        class_str.insert(2, "w")
        result_str = array('u', "hewllo")
        self.assertEqual(class_str.container, result_str)

    def test_iadd(self):
        base = ArrayList('i', [1, 2, 3])
        other = ArrayList('i', [4, 5])
        result = ArrayList('i', [1, 2, 3, 4, 5])

        self.assertEqual(base.__iadd__(other).container,
                         result.container)
        print("test iadd: done")

    def test_remove(self):
        base = ArrayList('i', [1, 2, 3, 4, 5])
        base.remove(2)
        self.assertEqual(base.container,
                         ArrayList('i', [1, 3, 4, 5]).container)
        with self.assertRaises(ValueError):
            base.remove(8)

        print("test remove: done")

    def test_pop(self):
        base = ArrayList('i', [1, 2, 3, 4, 5])
        self.assertEqual(base.pop(2), 3)
        self.assertEqual(base.container,
                         array('i', [1, 2, 4, 5]))

        copy = ArrayList('i', [1, 2, 3, 4, 5])
        for x in copy:
            self.assertEqual(copy.pop(0), x)

        self.assertEqual(copy.container,
                         array("i"))
        print("test pop: done")

    def test_reverse(self):
        base = ArrayList('i', [1, 2, 3, 4, 5])
        base.reverse()
        self.assertEqual(base.container,
                         array("i", [5, 4, 3, 2, 1]))
        print("test reverse: done")

    def test_extend(self):
        base = ArrayList('i', [1, 2, 3])
        base.extend(ArrayList('i', [6, 7, 8]))
        result = array("i", [1, 2, 3, 6, 7, 8])
        self.assertEqual(base.container, result)
        print("test extend: done")

    def test_append(self):
        base = ArrayList('i', [1, 2, 3])
        base.append(6)
        result = array("i", [1, 2, 3, 6])
        self.assertEqual(base.container, result)

        class_str = ArrayList('u', 'hello ')
        class_str.append("w")
        full_string = array('u', "hello w")
        self.assertEqual(class_str.container, full_string)
        print("test append: done")


if __name__ == "__main__":
    unittest.main()

