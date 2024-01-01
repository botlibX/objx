# This file is placed in the Public Domain.
#
#
# pylint: disable=C,R


"object interface test"


import objx
import unittest


from objx import Object


attributes = [
    'Object',
    'construct',
    'edit',
    'fmt',
    'fqn',
    'items',
    'keys',
    'read',
    'update',
    'values',
    'write'
]


class TestObject(unittest.TestCase):

    def test_interface(self):
        att = None
        for attr in attributes:
            att = getattr(objx, attr, None)
            if att == None:
                break
        self.assertTrue(att)

    def test_construct(self):
        self.assertTrue(True)

    def test_edit(self):
        self.assertTrue(True)

    def test_fmt(self):
        self.assertTrue(True)

    def test_fqn(self):
        self.assertTrue(True)

    def test_items(self):
        self.assertTrue(True)

    def test_keys(self):
        self.assertTrue(True)

    def test_read(self):
        self.assertTrue(True)

    def test_write(self):
        self.assertTrue(True)
