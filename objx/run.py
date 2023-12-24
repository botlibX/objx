# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0201,W0212,W0105,W0613,W0406,W0611,E0102


"main"


import getpass
import inspect
import os
import pwd
import readline
import sys
import termios
import time



from .command import Command
from .default import Default
from .error   import Error, debug
from .event   import Event
from .group   import Group
from .handler import Handler
from .object  import Object, cdir, spl
from .handler import Handler
from .object  import Object
from .parse   import parse_command
from .storage import Storage
from .thread  import launch
from .utility import forever


Cfg = Default()


Storage.wd = Cfg.wd


def cmnd(txt):
    evn = Event()
    evn.txt = txt
    Command.handle(evn)
    evn.wait()
    return evn


def daemon(pidfile, verbose=False):
    pid = os.fork()
    if pid != 0:
        os._exit(0)
    os.setsid()
    pid2 = os.fork()
    if pid2 != 0:
        os._exit(0)
    if not verbose:
        with open('/dev/null', 'r', encoding="utf-8") as sis:
            os.dup2(sis.fileno(), sys.stdin.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as sos:
            os.dup2(sos.fileno(), sys.stdout.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as ses:
            os.dup2(ses.fileno(), sys.stderr.fileno())
    os.umask(0)
    os.chdir("/")
    if os.path.exists(pidfile):
        os.unlink(pidfile)
    cdir(os.path.dirname(pidfile))
    with open(pidfile, "w", encoding="utf-8") as fds:
        fds.write(str(os.getpid()))


def privileges(username):
    pwnam = pwd.getpwnam(username)
    os.setgid(pwnam.pw_gid)
    os.setuid(pwnam.pw_uid)


def scan(pkg, modstr, initer=False) -> []:
    mods = []
    for modname in spl(modstr):
        module = getattr(pkg, modname, None)
        if not module:
            continue
        for key, cmd in inspect.getmembers(module, inspect.isfunction):
            if key.startswith("cb"):
                continue
            if 'event' in cmd.__code__.co_varnames:
                Command.add(cmd)
        for key, clz in inspect.getmembers(module, inspect.isclass):
            if key.startswith("cb"):
                continue
            if not issubclass(clz, Object):
                continue
            Storage.add(clz)
        if initer and "init" in dir(module):
            module._thr = launch(module.init, name=f"init {modname}")
        mods.append(module)
    return mods


def wrap(func) -> None:
    old2 = None
    try:
        old2 = termios.tcgetattr(sys.stdin.fileno())
    except termios.error:
        pass
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        print("")
    finally:
        if old2:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old2)


def main():
    try:
        import objx.mods as modules
    except ModuleNotFoundError:
        modules = None
    Storage.skel()
    parse_command(Cfg, " ".join(sys.argv[1:]))
    if not Cfg.mod:
        Cfg.mod = ",".join(modules.__dir__())
    if "v" in Cfg.opts:
        dte = time.ctime(time.time()).replace("  ", " ")
        debug(f"{Cfg.name.upper()} started {Cfg.opts.upper()} started {dte}")
    scan(modules, Cfg.mod)
    cmnd(Cfg.otxt)
