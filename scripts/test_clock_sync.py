from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import json
from pathlib import Path
import threading
import time

import pytest
import pc_time_server
import sync_pc_clock as sync


@pytest.fixture
def server():
    http = ThreadingHTTPServer(('127.0.0.1', 0), pc_time_server.handler_for({'127.0.0.1'}))
    thread = threading.Thread(target=http.serve_forever, daemon=True)
    thread.start()
    try:yield http.server_address[1]
    finally:http.shutdown();http.server_close();thread.join()


def test_real_clock_exchange(server):
    sample = sync.probe('127.0.0.1', server)
    assert abs(sample.now_ns()-time.time_ns()) < 50_000_000
    assert sample.roundtrip_ns > 0


def test_running_python_driver_and_native_nav_are_detected(tmp_path):
    for pid, args in [('10', ['/usr/bin/python3', '/opt/lib/waverover_driver']),
                      ('11', ['/opt/lib/amcl', '--ros-args']),
                      ('12', ['/usr/bin/python3', '/project/scripts/sync_pc_clock.py'])]:
        folder=tmp_path/pid;folder.mkdir()
        (folder/'cmdline').write_bytes(b'\0'.join(s.encode() for s in args))
    assert {pid for pid, cmd in sync.active_robot_processes(tmp_path)} == {10, 11}


def test_set_clock_uses_fresh_adjusted_time_without_shell(monkeypatch):
    monkeypatch.setattr(sync.time,'monotonic_ns',lambda: 5_000_000_000)
    sample=sync.Sample(1_800_000_000_000_000_000, 4_000_000_000, 20_000_000)
    calls=[]
    sync.set_clock(sample,run=lambda args,**kwargs:calls.append((args,kwargs)))
    assert calls[0][0] == ['sudo','-n','date','-u','--set','@1800000001.010000000']


def test_apply_refuses_to_change_clock_while_robot_running(monkeypatch):
    monkeypatch.setattr(sync.sys,'argv',['sync_pc_clock.py'])
    monkeypatch.setattr(sync,'active_robot_processes',lambda:[(10,'amcl')])
    monkeypatch.setattr(sync.subprocess,'run',lambda *a,**kw:pytest.fail('must not call sudo/date'))
    assert sync.main() == 1


def test_check_only_never_changes_clock(monkeypatch):
    monkeypatch.setattr(sync.sys,'argv',['sync_pc_clock.py','--check'])
    monkeypatch.setattr(sync,'probe',lambda *a:sync.Sample(time.time_ns(),time.monotonic_ns(),0))
    monkeypatch.setattr(sync.subprocess,'run',lambda *a,**kw:pytest.fail('read-only check'))
    assert sync.main() == 0


def test_tcp_handshake_time_is_excluded_from_clock_sample(monkeypatch):
    ticks = [0]
    class Connection:
        def __init__(self,*args,**kwargs):pass
        def connect(self):ticks[0] += 10_000_000_000
        def request(self,*args):ticks[0] += 10_000_000
        def getresponse(self):return self
        status = 200
        def read(self,*args):
            ticks[0] += 10_000_000
            return b'{"protocol":"rb3302-time-v1","unix_ns":1800000000000000000}'
        def close(self):pass
    monkeypatch.setattr(sync.http.client,'HTTPConnection',Connection)
    monkeypatch.setattr(sync.time,'monotonic_ns',lambda:ticks[0])
    assert sync.probe('127.0.0.1',8765,attempts=1).roundtrip_ns == 20_000_000


@pytest.mark.parametrize('body',[b'[]',b'{"protocol":"other","unix_ns":1800000000000000000}',
                                  b'{"protocol":"rb3302-time-v1","unix_ns":true}',b'not json'])
def test_bad_time_server_cannot_set_robot_clock(body):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200);self.end_headers();self.wfile.write(body)
        def log_message(self,*args):pass
    http=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    thread=threading.Thread(target=http.serve_forever,daemon=True);thread.start()
    try:
        with pytest.raises(RuntimeError):sync.probe('127.0.0.1',http.server_address[1],attempts=1)
    finally:http.shutdown();http.server_close();thread.join()
