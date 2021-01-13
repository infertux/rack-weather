#!/usr/bin/env python3

import os.path
import sys
import typing as t

from http.server import HTTPServer, BaseHTTPRequestHandler

import serial  # type: ignore
import serial.threaded  # type: ignore

__title__ = 'prometheus_exporter'
__version__ = '1.0.0'
__author__ = 'Cédric Felizard'
__license__ = 'AGPLv3+'
__copyright__ = 'Copyright 2020 Cédric Felizard'

metrics = None  # type: t.Optional[str]


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # FIXME: lock
        global metrics
        if not metrics:
            self.send_response(204)
            self.end_headers()
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; version=0.0.4; charset=utf-8')
            self.end_headers()
            # FIXME: lock
            sys.stdout.write('Metrics: {}\n'.format(metrics))
            self.wfile.write(metrics)


class SerialHandler(serial.threaded.LineReader):
    def connection_made(self, transport):
        super().connection_made(transport)
        self.metrics_buffer = []  # type: t.List[str]
        sys.stdout.write('Serial port opened\n')

    def handle_line(self, line):
        # print out debug lines but don't add them to the buffer
        if line.startswith('DEBUG: '):
            sys.stdout.write('{}\n'.format(line))
            return

        # a blank line is sent after each payload
        if line == '':
            # FIXME: lock
            global metrics
            metrics = '\n'.join(self.metrics_buffer)
            sys.stdout.write('Saved new buffer of {} bytes\n'.format(len(metrics)))
            self.metrics_buffer = []
        else:
            self.metrics_buffer.append(line)

    def connection_lost(self, exc):
        if exc:
            sys.stderr.write(repr(exc))
            raise exc
        sys.stdout.write('Serial port closed\n')


if __name__ == '__main__':
    http_server = ('localhost', 10003)

    serial_port = None
    for i in range(10):
        _port = '/dev/ttyACM{}'.format(i)
        if os.path.exists(_port):
            print('Found device on serial port {}'.format(_port))
            serial_port = _port
            break

    if not serial_port:
        print('Could not find serial port')
        sys.exit(1)

    ser = serial.Serial(serial_port, baudrate=115200, timeout=1)
    with serial.threaded.ReaderThread(ser, SerialHandler):
        httpd = HTTPServer(http_server, SimpleHTTPRequestHandler)
        print('Starting HTTP server on {}'.format(http_server))
        httpd.serve_forever()
