# This file is placed in the Public Domain.
#
# pylint: disable=C,R,E0603,E0402,W0401,W0614,W0611,W0622,W0105


""" Objects Library

    OBJX provides all the tools to program a cli program, such as disk
    perisistence for configuration files, event handler to handle the
    client/server connection, code to introspect modules for commands,
    deferred exception handling to not crash on an error, a parser to
    parse commandline options and values, etc.

    OBJX provides a demo prgram, it can connect to IRC, fetch and
    display RSS feeds, take todo notes, keep a shopping list
    and log text. You can also copy/paste the service file and run
    it under systemd for 24/7 presence in a IRC channel.

    OBJX is Public Domain.

"""


import pathlib
import json
import os
import _thread


"defines"


def __dir__():
    return (
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
    )


__all__ = __dir__()


lock = _thread.allocate_lock()


def cdir(pth) -> None:
    pth = pathlib.Path(pth)
    os.makedirs(pth, exist_ok=True)


"object"


class Object:


    def __contains__(self, key):
        "see if attribute is available."
        return key in dir(self)

    def __dir__(self):
        "list of keys."
        return __all__

    def __iter__(self):
        "iterate over attributes."
        return iter(self.__dict__)

    def __len__(self):
        "return number of attributes."
        return len(self.__dict__)

    def __repr__(self):
        "return json string."
        return dumps(self)

    def __str__(self):
        "return python string."
        return str(self.__dict__)


"decoder"


class ObjectDecoder(json.JSONDecoder):

    "decode from json string."

    def decode(self, s, _w=None):
        "decode a json string."
        val = json.JSONDecoder.decode(self, s)
        if not val:
            val = {}
        return hook(val)

    def raw_decode(self, s, idx=0):
        "decode raw text at index."
        return json.JSONDecoder.raw_decode(self, s, idx)


def hook(objdict, typ=None) -> Object:
    "construct with json data."
    if typ:
        obj = typ()
    else:
        obj = Object()
    construct(obj, objdict)
    return obj


def load(fpt, *args, **kw) -> Object:
    "load from disk."
    kw["cls"] = ObjectDecoder
    kw["object_hook"] = hook
    return json.load(fpt, *args, **kw)


def loads(string, *args, **kw) -> Object:
    "load from string."
    kw["cls"] = ObjectDecoder
    kw["object_hook"] = hook
    return json.loads(string, *args, **kw)


"encoder"


class ObjectEncoder(json.JSONEncoder):

    "encode into a json string."

    def default(self, o) -> str:
        "return json printable data."
        if isinstance(o, dict):
            return o.items()
        if isinstance(o, Object):
            return vars(o)
        if isinstance(o, list):
            return iter(o)
        if isinstance(
                      o,
                      (
                       type(str),
                       type(True),
                       type(False),
                       type(int),
                       type(float)
                      )
                     ):
            return o
        try:
            return json.JSONEncoder.default(self, o)
        except TypeError:
            return object.__repr__(o)

    def encode(self, o) -> str:
        "return json string."
        return json.JSONEncoder.encode(self, o)

    def iterencode(
                   self,
                   o,
                   _one_shot=False
                  ) -> str:
        "piecemale encoding to string."
        return json.JSONEncoder.iterencode(self, o, _one_shot)


def dump(*args, **kw) -> None:
    "write to file."
    kw["cls"] = ObjectEncoder
    return json.dump(*args, **kw)


def dumps(*args, **kw) -> str:
    "write to string."
    kw["cls"] = ObjectEncoder
    return json.dumps(*args, **kw)


"methods"


def construct(obj, *args, **kwargs) -> None:
    "construct from another type."
    if args:
        val = args[0]
        if isinstance(val, zip):
            update(obj, dict(val))
        elif isinstance(val, dict):
            update(obj, val)
        elif isinstance(val, Object):
            update(obj, vars(val))
    if kwargs:
        update(obj, kwargs)


def edit(obj, setter, skip=False) -> None:
    "edit with a dict and it's values."
    for key, val in items(setter):
        if skip and val == "":
            continue
        try:
            setattr(obj, key, int(val))
            continue
        except ValueError:
            pass
        try:
            setattr(obj, key, float(val))
            continue
        except ValueError:
            pass
        if val in ["True", "true"]:
            setattr(obj, key, True)
        elif val in ["False", "false"]:
            setattr(obj, key, False)
        else:
            setattr(obj, key, val)


def fmt(obj, args=None, skip=None, plain=False) -> str:
    "key=value formatted string."
    if args is None:
        args = keys(obj)
    if skip is None:
        skip = []
    txt = ""
    for key in args:
        if key.startswith("__"):
            continue
        if key in skip:
            continue
        value = getattr(obj, key, None)
        if value is None:
            continue
        if plain:
            txt += f"{value} "
        elif isinstance(value, str) and len(value.split()) >= 2:
            txt += f'{key}="{value}" '
        else:
            txt += f'{key}={value} '
    return txt.strip()


def fqn(obj) -> str:
    "full qualified name."
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = obj.__name__
    return kin


def items(obj) -> []:
    "return (key,value) list of object items."
    if isinstance(obj, type({})):
        return obj.items()
    return obj.__dict__.items()


def keys(obj) -> []:
    "list of attributes names."
    if isinstance(obj, type({})):
        return obj.keys()
    return list(obj.__dict__.keys())


def read(obj, pth) -> None:
    "locked read from path."
    with lock:
        with open(pth, 'r', encoding='utf-8') as ofile:
            update(obj, load(ofile))


def write(obj, pth) -> None:
    "locked write to path."
    with lock:
        cdir(os.path.dirname(pth))
        with open(pth, 'w', encoding='utf-8') as ofile:
            dump(obj, ofile)


def update(obj, data, empty=True) -> None:
    "update attributes with a key/value dict."
    for key, value in items(data):
        if empty and not value:
            continue
        setattr(obj, key, value)


def values(obj) -> []:
    "list of values."
    return obj.__dict__.values()
