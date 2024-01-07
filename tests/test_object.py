# This file is placed in the Public Domain.
#
#
# pylint: disable=C,R


"object interface test"


import objx
import os
import unittest


from objx import *


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


path = os.path.join(".test", "test")


class TestObject(unittest.TestCase):

    def test_interface(self):
        att = None
        for attr in attributes:
            att = getattr(objx, attr, None)
            if att == None:
                break
        self.assertTrue(att)

    def test_construct(self):
        data = {"a": "b"}
        obj = Object()
        construct(obj, data)
        self.assertEqual(obj.a, "b")

    def test_edit(self):
        obj = Object()
        obj.a = "b"
        data = {"a": "c"}
        edit(obj, data)
        self.assertEqual(obj.a, "c")

    def test_fmt(self):
        obj = Object()
        obj.a = "b"
        self.assertEqual(fmt(obj), "a=b")

    def test_fqn(self):
        obj = Object()
        self.assertEqual(fqn(obj), "objx.objects.Object")

    def test_items(self):
        obj = Object()
        obj.a = "b"
        self.assertEqual(list(items(obj)), [("a", "b")])

    def test_keys(self):
        obj = Object()
        obj.a = "b"
        self.assertEqual(keys(obj), ["a"])

    def test_disk(self):
        obj = Object()
        obj.a = "b"
        write(obj, path)
        ooo = Object()
        read(ooo, path)
        self.assertEqual(ooo.a, "b")
