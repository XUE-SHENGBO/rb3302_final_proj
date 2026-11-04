#!/usr/bin/env python3
"""Compare/set the robot clock from the designated PC before starting ROS."""
import argparse
from dataclasses import dataclass
import datetime
import http.client
import ipaddress
import json
import os
from pathlib import Path
import subprocess
import sys
import time


@dataclass(frozen=True)
class Sample:
    server_ns: int
    received_monotonic_ns: int
    roundtrip_ns: int

    def now_ns(self):
        return self.server_ns + self.roundtrip_ns // 2 + time.monotonic_ns() - self.received_monotonic_ns


def probe(host, port, attempts=3, timeout=2., max_rtt=.5):
    ipaddress.IPv4Address(host)
    samples = []
    errors = []
    for _ in range(attempts):
        connection = http.client.HTTPConnection(host, port, timeout=timeout)
        try:
            # TCP handshake delay is not part of the time exchange. Direct HTTP
            # also avoids system proxies for this designated LAN address.
            connection.connect()
            started = time.monotonic_ns()
            connection.request('GET', '/time')
            response = connection.getresponse()
            payload = response.read(4097)
            ended = time.monotonic_ns()
            if response.status != 200:
                raise ValueError(f'PC time server returned HTTP {response.status}')
            if len(payload) > 4096:
                raise ValueError('oversized time response')
            value = json.loads(payload)
            if not isinstance(value, dict):
                raise ValueError('invalid PC time response')
            ns = value.get('unix_ns')
            if value.get('protocol') != 'rb3302-time-v1' or isinstance(ns, bool) or not isinstance(ns, int):
                raise ValueError('invalid PC time response')
            if not 1577836800000000000 <= ns < 4102444800000000000:
                raise ValueError('PC time is outside 2020–2100')
            if (ended - started) / 1e9 > max_rtt:
                raise ValueError(f'time request latency too high ({(ended-started)/1e6:.2f}ms)')
            samples.append(Sample(ns, ended, ended - started))
        except (OSError, ValueError, http.client.HTTPException) as error:
            errors.append(str(error))
        finally:
            connection.close()
    if not samples:
        raise RuntimeError(f'无法请求电脑 {host}:{port} 的时间：' + '; '.join(errors))
    return min(samples, key=lambda s: s.roundtrip_ns)


def active_robot_processes(proc=Path('/proc')):
    executables = {'waverover_driver', 'ekf_node', 'amcl', 'controller_server',
                   'planner_server', 'bt_navigator', 'mission_manager', 'robot_state_publisher',
                   'rplidar_node', 'yesense_node_publisher', 'velocity_guard'}
    found = []
    for process in proc.iterdir():
        if not process.name.isdigit() or int(process.name) == os.getpid():
            continue
        try:
            args = [v.decode(errors='replace') for v in (process/'cmdline').read_bytes().split(b'\0') if v]
        except OSError:
            continue
        names = {Path(arg).name for arg in args[:3]}
        launch = any(arg in ('robot.launch.py', 'planning.launch.py') for arg in args)
        if names & executables or launch:
            found.append((int(process.name), ' '.join(args)))
    return found


def set_clock(sample, run=subprocess.run):
    # sudo credentials are acquired BEFORE measuring time, so a password prompt
    # cannot turn a good clock sample into an old one.
    ns = sample.now_ns()
    run(['sudo', '-n', 'date', '-u', '--set', f'@{ns//1000000000}.{ns%1000000000:09d}'],
        check=True, capture_output=True, text=True, timeout=3.)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', default='192.168.50.92')
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--check', action='store_true', help='Compare only; no privilege or clock changes')
    parser.add_argument('--verify-tolerance', type=float, default=.25)
    args = parser.parse_args()
    try:
        if not args.check:
            running = active_robot_processes()
            if running:
                raise RuntimeError('校时前请先停止机器人硬件、导航和任务进程：\n' +
                                   '\n'.join(f'PID {pid}: {cmd}' for pid, cmd in running))
            subprocess.run(['sudo', '-v'], check=True, timeout=60.)
        sample = probe(args.host, args.port)
        offset = (sample.now_ns() - time.time_ns()) / 1e9
        print(f'电脑 {args.host}：与机器人时间差 {offset:+.6f}s，请求往返 {sample.roundtrip_ns/1e6:.2f}ms', flush=True)
        if args.check:
            return 0
        # Check again immediately before a step; avoid starting ROS during calibration.
        if active_robot_processes():
            raise RuntimeError('校时期间出现机器人进程，取消校时')
        set_clock(sample)
        verification = probe(args.host, args.port)
        remaining = (verification.now_ns() - time.time_ns()) / 1e9
        if abs(remaining) > args.verify_tolerance:
            raise RuntimeError(f'校时后仍相差 {remaining:+.6f}s，拒绝启动ROS')
        print(f'校时完成：剩余偏差 {remaining:+.6f}s；UTC {datetime.datetime.now(datetime.timezone.utc).isoformat()}', flush=True)
        return 0
    except (RuntimeError, ValueError, OSError, subprocess.SubprocessError) as error:
        print(f'自动校时失败：{error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
