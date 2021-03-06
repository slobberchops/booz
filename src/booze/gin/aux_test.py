# Copyright 2015 Rafe Kaplan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
import unittest

from booze.gin import aux
from booze.gin import parser


class AttrTestCase(unittest.TestCase):

    def test_parse(self):
        self.assertEqual((True, 'astring'), aux.Attr('astring').parse(''))
        self.assertEqual((True, 1), aux.Attr(1).parse(''))
        self.assertEqual((True, (1, 2)), aux.Attr((1, 2)).parse(''))

    def test_none(self):
        with self.assertRaises(TypeError):
            aux.Attr(None)

    def test_unused(self):
        with self.assertRaises(TypeError):
            aux.Attr(parser.UNUSED)

    def test_unused_attr_type(self):
        with self.assertRaises(ValueError):
            aux.Attr(10, parser.AttrType.UNUSED)

    def test_attr_types(self):
        self.assertEqual(parser.AttrType.STRING, aux.Attr('astring').attr_type)
        self.assertEqual(parser.AttrType.TUPLE, aux.Attr(('astring', 10)).attr_type)
        self.assertEqual(parser.AttrType.OBJECT, aux.Attr(10).attr_type)

    def test_attr_type_override(self):
        self.assertEqual(parser.AttrType.OBJECT, aux.Attr('astring', parser.AttrType.OBJECT).attr_type)

    def test_value(self):
        self.assertEqual('avalue', aux.Attr('avalue').value)

    def test_incompatibile_values(self):
        with self.assertRaises(TypeError):
            aux.Attr(object(), parser.AttrType.STRING)
        with self.assertRaises(TypeError):
            aux.Attr(object(), parser.AttrType.TUPLE)


class EoiTest(unittest.TestCase):

    def test_parse(self):
        self.assertEqual((True, parser.UNUSED), aux.eoi.parse(''))

    def test_parse_with_end_space(self):
        s = io.StringIO(' ')
        self.assertEqual((True, parser.UNUSED), aux.eoi.parse(s, skipper=parser.Char(' ')))
        self.assertEqual('', s.read())

    def test_parse_fail(self):
        self.assertEqual((False, None), aux.eoi.parse('anything'))

    def test_attr_type(self):
        self.assertEqual(parser.AttrType.UNUSED, aux.eoi.attr_type)


class EpsTest(unittest.TestCase):

    def test_parse(self):
        self.assertEqual((True, parser.UNUSED), aux.eps.parse(''))
        self.assertEqual((True, parser.UNUSED), aux.eps.parse('abc'))

    def test_attr_type(self):
        self.assertEqual(parser.AttrType.UNUSED, aux.eps.attr_type)


if __name__ == '__main__':
    unittest.main()
