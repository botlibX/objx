# This file is placed in the Public Domain.
#
# pylint: disable=C,R,E1101,W0718,W0612,E0611


"cache"


from . import Object


def __dir__():
    return (
            'Cache',
           )


__all__ = __dir__()


class Cache(Object):

    cache = {}

    @staticmethod
    def add(obj) -> None:
        Cache.cache["broker"].append(obj)

    @staticmethod
    def byorig(orig) -> Object:
        for obj in Cache.cache["broker"]:
            if object.__repr__(obj) == orig:
                return obj
        return None

    @staticmethod
    def extend(channel, txtlist):
        if channel not in Cache.cache:
            Cache.cache[channel] = []
        Cache.cache[channel].extend(txtlist)

    @staticmethod
    def first():
        if Cache.cache["broker"]:
            return Cache.cache["broker"][0]

    @staticmethod
    def size(chan):
        if chan in Cache.cache:
            return len(Cache.cache.get(chan, []))
        return 0
