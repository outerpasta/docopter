#!/usr/bin/env python
from os.path import join, isfile

import logging

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.escape import xhtml_escape
from tornado.options import define, options
from tornado.process import Subprocess
from tornado.iostream import StreamClosedError

from docloader import DocLoader
import Settings

define("port", default=8080, help="Run server on a specific port", type=int)


docloader = DocLoader()


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html', scripts=docloader.scripts)


class LogStreamer(tornado.websocket.WebSocketHandler):

    def open(self, arg, **kwargs):
        if isfile(join(Settings.SCRIPTS_DIR, arg + '.py')):
            script = join(Settings.SCRIPTS_DIR, arg + '.py')
        elif isfile(join(Settings.SCRIPTS_DIR, arg + '.sh')):
            script = join(Settings.SCRIPTS_DIR, arg + '.sh')
        else:
            self.write_line("%s is not a file" % arg)
            self._close()
            return

        args, opts = [], []
        for k, v in self.request.arguments.iteritems():
            if k.startswith("<"):
                if v[0]:
                    args.append(v[0])
                else:
                    continue
            elif k.startswith("--"):
                if v[0] == '':
                    continue
                elif v[0] == 'on':
                    opts.append(k)
                else:
                    opts.append(k)
                    opts.append(v[0])

            else:
                raise NotImplementedError

        command = [str(script)] + args + opts
        logging.info("Executing: {0}".format(command))

        self.proc = Subprocess(command, stdout=Subprocess.STREAM, stderr=Subprocess.STREAM, bufsize=1)
        self.proc.stdout.read_until("\n", self.write_line)
        self.proc.stderr.read_until_close(callback=self.write_error)

        # self.proc.set_exit_callback(self._close)

    def _close(self, *args, **kwargs):
        self.close()

    def on_close(self, *args, **kwargs):
        if hasattr(self, "proc"):
            logging.info("trying to kill process")
            self.proc.proc.terminate()
            self.proc.proc.wait()

    def write_line(self, data):
        try:
            logging.info("Returning to client: %s" % data.strip())
            self.write_message(xhtml_escape(data.strip()) + "<br/>")
            self.proc.stdout.read_until("\n", self.write_line)
        except StreamClosedError:
            logging.info("StreamClosedError")

    def write_error(self, data):
        if data:
            logging.info("Returning to client: %s" % data.strip())
            self.write_message("<font color=red>" + xhtml_escape(data.strip()) + "</font><br/>")
        # from IPython import embed;embed()
        # self.proc.stdout.read_until("\n", self.write_line)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/([^/]+)", LogStreamer),
        ]
        settings = {
            "template_path":Settings.TEMPLATE_PATH,
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
