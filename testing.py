import unittest

import read

selectors = ['block', 'block_mod', 'block_mod_val','block__elem', 'block__elem_mod', 'block__elem_mod_val']

class TestReadFunctions(unittest.TestCase):
    """Unit testing for read.py"""
    def test_isMediaQuery(self):
        self.assertTrue(read.isMediaQuery('@media'))

    def test_isElement(self):
        for selector in selectors[:3]:
            self.assertFalse(read.isElement(selector))
        for selector in selectors[3:]:
            self.assertTrue(read.isElement(selector))

    def test_hasModifier(self):
        for selector in ['block', 'block__elem']:
            self.assertFalse(read.hasModifier(selector))
        for selector in ['block_mod', 'block_mod_val',
                         'block__elem_mod', 'block__elem_mod_val']:
            self.assertTrue(read.hasModifier(selector))

    def test_hasValue(self):
        for selector in ['block', 'block_mod', 'block__elem',
                         'block__elem_mod']:
            self.assertFalse(read.hasValue(selector))
        for selector in ['block_mod_val', 'block__elem_mod_val']:
            self.assertTrue(read.hasValue(selector))

    def test_split_selector(self):
        expected = [('block', '', '', ''), ('block', '', '_mod', ''),
                    ('block', '', '_mod', '_val'),
                    ('block', '__elem', '', ''),
                    ('block', '__elem', '_mod', ''),
                    ('block', '__elem', '_mod', '_val')]
        for i, selector in enumerate(selectors):
            self.assertEqual(read.split_selector(selector), expected[i])


if __name__ == '__main__':
    unittest.main()
