#!/usr/bin/env python
from os.path import dirname, join, realpath, isfile

import logging

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.options import define, options
from tornado.process import Subprocess

import Settings

define("port", default=7777, help="Run server on a specific port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class LogStreamer(tornado.websocket.WebSocketHandler):

    def open(self, arg):
        if not isfile(join(Settings.SCRIPTS_DIR, arg + '.py')):
            self.write_line("%s is not a file" % arg)
            self._close()
            return

        print "%s is a file" % arg
        # filename = realpath(join(dirname(__file__), "simple_foobar.log"))
        self.proc = Subprocess(["tail", "hello"],
                               stdout=Subprocess.STREAM,
                               bufsize=1)
        self.proc.set_exit_callback(self._close)
        self.proc.stdout.read_until("\n", self.write_line)

    def _close(self, *args, **kwargs):
        self.close()

    def on_close(self, *args, **kwargs):
        logging.info("trying to kill process")
        self.proc.proc.terminate()
        self.proc.proc.wait()

    def write_line(self, data):
        logging.info("Returning to client: %s" % data.strip())
        self.write_message(data.strip() + "<br/>")
        self.proc.stdout.read_until("\n", self.write_line)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/tail/([^/]+)", LogStreamer),
        ]
        settings = {
            "template_path":Settings.TEMPLATE_PATH,
            "static_path":Settings.STATIC_PATH,
            "debug":Settings.DEBUG
        }
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(Application())
    tornado.options.parse_command_line()
    http_server.listen(options.port)
    logging.info("TornadoLog started. Point your browser to http://localhost:%d/" %
                 options.port)
    tornado.ioloop.IOLoop.instance().start()
