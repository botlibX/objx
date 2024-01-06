NAME

::

    OBJX - objects.

SYNOPSIS

::

    objx <cmd> [key=val] 
    objx <cmd> [key==val]
    objx [-c] [-v] [-d]


DESCRIPTION

::

    OBJX is a python3 library implementing the 'objx' package. It
    provides all the tools to program a unix cli program, such as
    disk perisistence for configuration files, event handler to
    handle the client/server connection, code to introspect modules
    for commands, deferred exception handling to not crash on an
    error, a parser to parse commandline options and values, etc.

    OBJX provides a demo bot, it can connect to IRC, fetch and
    display RSS feeds, take todo notes, keep a shopping list
    and log text. You can also copy/paste the service file and run
    it under systemd for 24/7 presence in a IRC channel.

    OBJX is a contribution back to society and is Public Domain.


INSTALL


::

    $ pipx install objx


USAGE

::

    without any argument the program does nothing

    $ objx
    $

    see list of commands

    $ objx cmd
    cmd,err,mod,req,thr,ver

    list of modules

    $ objx mod
    cmd,err,fnd,irc,log,mod,req,rss,tdo,thr

    use mod=<name1,name2> to load additional
    modules

    $ objx cfg mod=irc

    start a console

    $ objx -c mod=irc,rss
    >

    use -v for verbose

    $ objx -cv mod=irc
    OBJX started CV started Sat Dec 2 17:53:24 2023
    >

    start daemon

    $ objx -d mod=irc,rss
    $ 


CONFIGURATION


::

    irc

    $ objx cfg server=<server>
    $ objx cfg channel=<channel>
    $ objx cfg nick=<nick>

    sasl

    $ objx pwd <nsvnick> <nspass>
    $ objx cfg password=<frompwd>

    rss

    $ objx rss <url>
    $ objx dpl <url> <item1,item2>
    $ objx rem <url>
    $ objx nme <url< <name>


COMMANDS


::

    cmd - commands
    cfg - irc configuration
    dlt - remove a user
    dpl - sets display items
    fnd - find objects 
    log - log some text
    met - add a user
    mre - displays cached output
    pwd - sasl nickserv name/pass
    rem - removes a rss feed
    req - reconsider
    rss - add a feed
    thr - show the running threads


SYSTEMD


::

    save the following it in /etc/systems/system/objx.service and
    replace "<user>" with the user running pipx


    [Unit]
    Description=original programmer
    Requires=network.target
    After=network.target

    [Service]
    Type=simple
    User=<user>
    Group=<user>
    WorkingDirectory=/home/<user>/.objx
    ExecStart=/home/<user>/.local/pipx/venvs/objx/bin/objxd
    RemainAfterExit=yes

    [Install]
    WantedBy=multi-user.target


    then run this

    $ mkdir ~/.objx
    $ sudo systemctl enable objx --now

    default channel/server is #objx on localhost


FILES

::

    ~/.objx
    ~/.local/bin/objx
    ~/.local/pipx/venvs/objx/


AUTHOR


::

    botlib <libbotx@gmail.com>


COPYRIGHT


::

    OBJX is Public Domain.
