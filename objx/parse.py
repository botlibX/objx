# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0718,W0702


"parsing text"


import datetime
import re
import time as ttime


from .default import Default


def __dir__():
    return (
        'NoDate',
        'today',
        'get_day',
        'get_hour',
        'get_time',
        'hms',
        'now',
        'parse_command',
        'parse_time',
        'to_day',
        'to_time',
        'year'
    )


__all__ = __dir__()


year_formats = [
    "%Y-%m-%d",
    "%d-%m-%Y",
    "%d-%m",
    "%m-%d",
]


timere = re.compile(r'(\S+)\s+(\S+)\s+(\d+)\s+(\d+):(\d+):(\d+)\s+(\d+)')


bdmonths = ['Bo', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


monthint = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12 
}


class NoDate(Exception):

    pass


def today():
    return str(datetime.datetime.today()).split()[0]


def extract_date(daystr):
    for fmt in year_formats:
        try:
            res = ttime.mktime(ttime.strptime(daystr, fmt))
        except:
            res = None
        if res:
            return res


def get_day(daystr):
    try:
        ymdre = re.search(r'(\d+)-(\d+)-(\d+)', daystr)
        (day, month, yea) = ymdre.groups()
    except:
        try:
            ymre = re.search(r'(\d+)-(\d+)', daystr)
            (day, month) = ymre.groups()
            yea = ttime.strftime("%Y", ttime.localtime())
        except Exception as ex:
            raise NoDate(daystr) from ex
    day = int(day)
    month = int(month)
    yea = int(yea)
    date = "%s %s %s" % (day, bdmonths[month], yea)
    return ttime.mktime(ttime.strptime(date, r"%d %b %Y"))


def get_hour(daystr):
    try:
        hmsre = re.search(r'(\d+):(\d+):(\d+)', str(daystr))
        hours = 60 * 60 * (int(hmsre.group(1)))
        hoursmin = hours  + int(hmsre.group(2)) * 60
        hmsres = hoursmin + int(hmsre.group(3))
    except AttributeError:
        pass
    except ValueError:
        pass
    try:
        hmre = re.search(r'(\d+):(\d+)', str(daystr))
        hours = 60 * 60 * (int(hmre.group(1)))
        hmsres = hours + int(hmre.group(2)) * 60
    except AttributeError:
        return 0
    except ValueError:
        return 0
    return hmsres


def get_time(txt):
    try:
        target = get_day(txt)
    except NoDate:
        target = to_day(today())
    hour =  get_hour(txt)
    if hour:
        target += hour
    return target


def hms():
    return str(datetime.datetime.today()).split()[1].split(".")[0]


def now():
    return str(datetime.datetime.now())


def parse_command(obj, txt=None) -> None:
    args = []
    obj.args    = obj.args or []
    obj.cmd     = obj.cmd or ""
    obj.gets    = obj.gets or Default()
    obj.hasmods = obj.hasmod or False
    obj.index   = None
    obj.mod     = obj.mod or ""
    obj.opts    = obj.opts or ""
    obj.result  = obj.reult or []
    obj.sets    = obj.sets or Default()
    obj.txt     = txt or obj.txt or ""
    obj.otxt    = obj.txt
    _nr = -1
    for spli in obj.otxt.split():
        if spli.startswith("-"):
            try:
                obj.index = int(spli[1:])
            except ValueError:
                obj.opts += spli[1:]
            continue
        if "==" in spli:
            key, value = spli.split("==", maxsplit=1)
            if key in obj.gets:
                val = getattr(obj.gets, key)
                value = val + "," + value
            setattr(obj.gets, key, value)
            continue
        if "=" in spli:
            key, value = spli.split("=", maxsplit=1)
            if key == "mod":
                obj.hasmods = True
                if obj.mod:
                    obj.mod += f",{value}"
                else:
                    obj.mod = value
                continue
            setattr(obj.sets, key, value)
            continue
        _nr += 1
        if _nr == 0:
            obj.cmd = spli
            continue
        args.append(spli)
    if args:
        obj.args = args
        obj.txt  = obj.cmd or ""
        obj.rest = " ".join(obj.args)
        obj.txt  = obj.cmd + " " + obj.rest
    else:
        obj.txt = obj.cmd or ""



def parse_time(txt):
    seconds = 0
    target = 0
    txt = str(txt)
    for word in txt.split():
        if word.startswith("+"):
            seconds = int(word[1:])
            return ttime.time() + seconds
        if word.startswith("-"):
            seconds = int(word[1:])
            return ttime.time() - seconds
    if not target:
        try:
            target = get_day(txt)
        except NoDate:
            target = to_day(today())
        hour =  get_hour(txt)
        if hour:
            target += hour
    return target


def to_day(daystr):
    previous = ""
    line = ""
    daystr = str(daystr)
    for word in daystr.split():
        line = previous + " " + word
        previous = word
        try:
            res = extract_date(line.strip())
        except ValueError:
            res = None
        if res:
            return res
        line = ""


def to_time(daystr):
    daystr = str(daystr)
    daystr = daystr.split(".")[0]
    daystr = daystr.replace("GMT", "CEST")
    daystr = daystr.replace("_", ":")
    daystr = " ".join([x.capitalize() for x in daystr.split() if not x[0] in ["+", "-"]])
    res = 0
    try: res = ttime.mktime(ttime.strptime(daystr, r"%a, %d %b %Y %H:%M:%S"))
    except: pass
    if not res:
        try: res = ttime.mktime(ttime.strptime(daystr, r"%a, %d %b %Y %H:%M:%S %z"))
        except: pass
    if not res:
        try: res = ttime.mktime(ttime.strptime(daystr, r"%a, %d %b %Y %H:%M:%S %z"))
        except: pass
    if not res:
        try: res = ttime.mktime(ttime.strptime(daystr, r"%a %d %b %H:%M:%S %Y"))
        except: pass
    if not res:
        try: res = ttime.mktime(ttime.strptime(daystr, r"%a %d %b %H:%M:%S %Y %z"))
        except: pass
    if not res:
        try: res = ttime.mktime(ttime.strptime(daystr, r"%Y-%m-%d %H:%M:%S"))
        except: pass
    if not res:
        try: res = ttime.mktime(ttime.strptime(daystr, r"%d-%m-%Y %H:%M:%S"))
        except: pass
    if not res:
        try: res = ttime.mktime(ttime.strptime(daystr, r"%d-%m-%Y %H:%M"))
        except: pass
    if not res:
        try: res = ttime.mktime(ttime.strptime(daystr, r"%Y-%m-%d %H:%M"))
        except: pass
    if not res:
        try: res = ttime.mktime(ttime.strptime(daystr, r"%Y-%m-%d"))
        except: pass
    if not res:
        try: res = ttime.mktime(ttime.strptime(daystr, r"%d-%m-%Y"))
        except: pass
    if not res: raise NoDate(daystr)
    return res


def year():
    return str(datetime.datetime.now().year)
