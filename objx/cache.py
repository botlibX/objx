# This file is placed in the Public Domain.
#
# pylint: disable=C,R,E1101,W0718,W0612,E0611


"cache"


from .object import Object


def __dir__():
    return (
            'Cache',
           )


__all__ = __dir__()


class Cache(Object):

    @staticmethod
    def extend(channel, txtlist):
        if channel not in Cache:
            Cache[channel] = []
        Cache[channel].extend(txtlist)

    @staticmethod
    def size(chan):
        if chan in Cache:
            return len(Cache.get(chan, []))
        return 0
