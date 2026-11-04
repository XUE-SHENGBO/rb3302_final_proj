#!/usr/bin/env python3
"""Read-only PC clock endpoint for the robot's pre-ROS startup calibration."""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import time


def handler_for(allowed):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.client_address[0] not in allowed:
                self.send_error(403)
                return
            if self.path != '/time':
                self.send_error(404)
                return
            body = json.dumps({'protocol': 'rb3302-time-v1', 'unix_ns': time.time_ns()}).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass
    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bind', default='192.168.50.92')
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--allow', action='append', default=['192.168.50.6', '192.168.50.92', '127.0.0.1'])
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.bind, args.port), handler_for(set(args.allow)))
    print(f'PC time endpoint http://{args.bind}:{args.port}/time', flush=True)
    server.serve_forever()


if __name__ == '__main__':
    main()
