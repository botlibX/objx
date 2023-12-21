# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0212,W0702,W0718,E1102,W0613


"handler"


import queue
import threading
import _thread


from .default import Default
from .group   import Group
from .object  import Object
from .errors  import Errors
from .thread  import launch


def __dir__():
    return (
        'Event',
        'Handler'
    )


__all__ = __dir__()


class Event(Default):

    def __init__(self):
        Default.__init__(self)
        self._ready  = threading.Event()
        self._thrs   = []
        self.done    = False
        self.orig    = None
        self.result  = []
        self.txt     = ""

    def ready(self):
        self._ready.set()

    def reply(self, txt) -> None:
        self.result.append(txt)

    def show(self) -> None:
        for txt in self.result:
            bot = Group.byorig(self.orig) or Group.first()
            if bot:
                bot.say(self.channel, txt)

    def wait(self):
        for thr in self._thrs:
            thr.join()
        self._ready.wait()
        return self.result


class Handler(Object):

    def __init__(self):
        Object.__init__(self)
        self.cbs      = Object()
        self.queue    = queue.Queue()
        self.stopped  = threading.Event()
        self.threaded = False

    def callback(self, evt) -> None:
        func = getattr(self.cbs, evt.type, None)
        if not func:
            evt.ready()
            return
        if self.threaded:
            evt._thrs.append(launch(func, evt))
        else:
            try:
                func(evt)
            except Exception as ex:
                Errors.add(ex)

    def loop(self) -> None:
        while not self.stopped.is_set():
            try:
                self.callback(self.poll())
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()

    def poll(self):
        return self.queue.get()

    def put(self, evt) -> None:
        self.queue.put_nowait(evt)

    def register(self, typ, cbs) -> None:
        setattr(self.cbs, typ, cbs)

    def start(self) -> None:
        launch(self.loop)

    def stop(self) -> None:
        self.stopped.set()
