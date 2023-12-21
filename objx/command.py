# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0718


"commands"


from .errors import Errors
from . import Object


def __dir__():
    return (
        'Commands',
    )


__all__ = __dir__()


def cmnd(txt):
    evn = Event()
    evn.txt = txt
    parse(evn)
    Commands.handle(evn)
    evn.wait()
    return evn


class Commands(Object):

    cmds = Object()

    @staticmethod
    def add(func) -> None:
        setattr(Commands.cmds, func.__name__, func)

    @staticmethod
    def handle(evt) -> None:
        #parse(evt)
        func = getattr(Commands.cmds, evt.cmd, None)
        if not func:
            evt.ready()
            return
        try:
            func(evt)
            evt.show()
        except Exception as exc:
            Errors.add(exc)
        evt.ready()
