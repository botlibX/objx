# This file is placed in the Public Domain.
#
#


from .command import Command
from .group   import Group
from .handler import Handler


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        self.register("command", Command.handle)
        Group.add(self)

    def announce(self, txt):
        self.raw(txt)

    def say(self, channel, txt):
        self.raw(txt)

    def raw(self, txt):
        pass
