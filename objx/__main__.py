# This file is placed in the Public Domain.
#
# pylint: disable=C,R


"main"


from .error import Error
from .run   import main, wrap


def wrapped():
    wrap(main)
    Error.show()


if __name__ == "__main__":
    wrapped()
 