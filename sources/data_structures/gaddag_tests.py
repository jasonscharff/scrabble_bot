import unittest
from .gaddag import GADDAG

class GADDAGTests(unittest.TestCase):
    def test_single_word(self):
        g = GADDAG()
        g.add_word('apple')

        self.assertCountEqual(
            g.find_matches(hook='a', rack=['p', 'p', 'l', 'e'], available_prefix_spaces=10, available_suffix_spaces=10),
            [('', 'pple')]
        )

        self.assertCountEqual(
            g.find_matches(hook='p', rack=['p', 'p', 'l', 'e'], available_prefix_spaces=10, available_suffix_spaces=10),
            []
        )

        self.assertCountEqual(
            g.find_matches(hook='p', rack=['a', 'p', 'p', 'l', 'e'], available_prefix_spaces=10, available_suffix_spaces=10),
            [('a', 'ple'), ('ap', 'le')]
        )

        self.assertCountEqual(
            g.find_matches(hook='p', rack=['p', 'p', 'l', 'e'], available_prefix_spaces=10, available_suffix_spaces=1),
            []
        )

        self.assertCountEqual(
            g.find_matches(hook='l', rack=['a', 'p', 'p', 'l', 'e'], available_prefix_spaces=10, available_suffix_spaces=10),
            [('app', 'e')]
        )

        self.assertCountEqual(
            g.find_matches(hook='l', rack=['a', 'p', 'p', 'l', 'e'], available_prefix_spaces=2, available_suffix_spaces=10),
            []
        )

        self.assertCountEqual(
            g.find_matches(hook='l', rack=['a', 'p', 'p', 'l', 'e'], available_prefix_spaces=3, available_suffix_spaces=10),
            [('app', 'e')]
        )

        self.assertCountEqual(
            g.find_matches(hook='a', rack=['a', 'p', 'p', 'l', 'e'], available_prefix_spaces=10, available_suffix_spaces=3),
            []
        )

        self.assertCountEqual(
            g.find_matches(hook='a', rack=['a', 'p', 'p', 'l', 'e'], available_prefix_spaces=10, available_suffix_spaces=4),
            [('', 'pple')]
        )

    def test_multiple_words(self):
        g = GADDAG()
        g.add_word('cat')
        g.add_word('bat')
        g.add_word('at')
        g.add_word('apple')

        self.assertCountEqual(
            g.find_matches(hook='a', rack=['c', 't', 'p', 'p', 'l', 'e', 'b'], available_prefix_spaces=10, available_suffix_spaces=10),
            [('c', 't'), ('b','t'), ('','t'), ('', 'pple')]
        )

        self.assertCountEqual(
            g.find_matches(hook='a', rack=['c', 'p', 'p', 'l', 'e', 'b'], available_prefix_spaces=10, available_suffix_spaces=10),
            [('', 'pple')]
        )

        self.assertCountEqual(
            g.find_matches(hook='a', rack=['c', 'p', 'l', 'e', 'b', 't'], available_prefix_spaces=10, available_suffix_spaces=10),
            [('c','t'), ('b', 't'), ('','t')]
        )

        self.assertCountEqual(
            g.find_matches(hook='c', rack=['c', 'a', 'p', 'l', 'e', 'b', 't'], available_prefix_spaces=10, available_suffix_spaces=10),
            [('', 'at')]
        )

        self.assertCountEqual(
            g.find_matches(hook='b', rack=['c', 'a', 'p', 'l', 'e', 'b', 't'], available_prefix_spaces=10, available_suffix_spaces=10),
            [('', 'at')]
        )

        self.assertCountEqual(
            g.find_matches(hook='t', rack=['c', 'a', 'p', 'l', 'e', 'b', 't'], available_prefix_spaces=10, available_suffix_spaces=10),
            [('ba', ''), ('ca', ''), ('a', '')]
        )

        self.assertCountEqual(
            g.find_matches(hook='t', rack=['c', 'p', 'l', 'e', 'b', 't'], available_prefix_spaces=10, available_suffix_spaces=10),
            []
        )

        self.assertCountEqual(
            g.find_matches(hook='t', rack=['p', 'a', 'l', 'e', 'b', 't'], available_prefix_spaces=10, available_suffix_spaces=10),
            [('ba', ''), ('a', '')]
        )

        self.assertCountEqual(
            g.find_matches(hook='t', rack=['p', 'a', 'l', 'e', 'b', 't'], available_prefix_spaces=1, available_suffix_spaces=10),
            [('a', '')]
        )

        self.assertCountEqual(
            g.find_matches(hook='c', rack=['p', 'a', 'l', 'e', 'b', 't'], available_prefix_spaces=10, available_suffix_spaces=2),
            [('', 'at')]
        )

        self.assertCountEqual(
            g.find_matches(hook='c', rack=['p', 'a', 'l', 'e', 'b', 't'], available_prefix_spaces=10, available_suffix_spaces=1),
            []
        )

    def test_contains(self):
        g = GADDAG()
        g.add_word('apple')
        g.add_word('app')
        g.add_word('bat')
        self.assertTrue('apple' in g)
        self.assertTrue('app' in g)
        self.assertTrue('bat' in g)
        self.assertFalse('ap' in g)


    def test_large_gaddag(self):
        g = GADDAG()
        with open('./static/scrabble_dictionary.txt', 'r') as f:
            for line in f:
                g.add_word(line.strip('\n'))

        matches = g.find_matches(hook='A', rack=['P', 'P', 'L', 'E'], available_prefix_spaces=10, available_suffix_spaces=10)
        self.assertTrue(('', 'PPLE') in matches)


if __name__ == '__main__':
    unittest.main()
