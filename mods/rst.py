# This file is placed in the Public Domain.
#
#


""" rest interface. """


import logging
import time


from http.server import HTTPServer, BaseHTTPRequestHandler


from objx import Errors, Object, Storage, launch


class REST(HTTPServer, Object):

    allow_reuse_address = True
    daemon_thread = True

    def __init__(self, *args, **kwargs):
        HTTPServer.__init__(self, *args, **kwargs)
        Object.__init__(self)
        self.host = args[0]
        self._last = time.time()
        self._starttime = time.time()
        self._status = "start"

    def exit(self):
        self._status = ""
        time.sleep(0.2)
        self.shutdown()

    def start(self): 
        debug("# start rest http://%s:%s" % self.host)
        self._status = "ok"
        self.ready()
        self.serve_forever()

    def request(self):
        self._last = time.time()

    def error(self, request, addr):
        ex = get_exception()
        debug('# error rest %s %s' % (addr, ex))


class RESTHandler(BaseHTTPRequestHandler):

    def setup(self):
        BaseHTTPRequestHandler.setup(self)
        self._ip = self.client_address[0]
        self._size = 0

    def write_header(self, type='text/plain'):
        self.send_response(200)
        self.send_header('Content-type', '%s; charset=%s ' % (type, "utf-8"))
        self.send_header('Server', __version__)
        self.end_headers()

    def do_GET(self):
        try:
            f = open(self.path, "r")
            txt = f.read()
            f.close()
        except (TypeError, FileNotFoundError):
            self.send_response(404)
            self.end_headers()
            return
        txt = txt.replace("\\n", "\n")
        txt = txt.replace("\\t", "\t")
        self.write_header()
        self.wfile.write(bytes(txt, "utf-8"))
        self.wfile.flush()

    def log(self, code):
        debug('# log rest %s code %s path %s' % (self.address_string(), code, self.path))
