"""Real ROS messages + a PTY; service control is replaced, no robot device used."""
import json
import math
import os
import pty
import time
from types import SimpleNamespace

import pytest
import rclpy
from rclpy.parameter import Parameter
from geometry_msgs.msg import Twist
from waverover_base import waverover_driver as driver
from test_feedback import packet
from waverover_base.device_lock import DeviceLock


class Service:
    calls = []
    def __init__(self, *args): pass
    def stop(self): self.calls.append('stop')
    def start(self): self.calls.append('start')


@pytest.fixture
def node(monkeypatch):
    master, slave = pty.openpty()
    port = os.ttyname(slave)
    os.set_blocking(master, False)
    Service.calls = []
    monkeypatch.setattr(driver, 'DisplayServiceGuard', Service)
    monkeypatch.setattr(driver.WaveRoverDriver, '_initialize_robot', lambda self: self._send_velocity(0., 0.))
    rclpy.init(args=['--ros-args', '-p', 'serial_port:='+port, '-p', 'show_battery_percentage:=false',
                     '-p', 'feedback_timeout_sec:=0.15', '-p', 'feedback_max_gap_sec:=0.15'])
    n = driver.WaveRoverDriver()
    try:
        yield n, master, port
    finally:
        n.destroy_node()
        rclpy.try_shutdown()
        os.close(master);os.close(slave)


def spin(node, duration=.03):
    end = time.monotonic()+duration
    while time.monotonic() < end:
        rclpy.spin_once(node, timeout_sec=.005)


def send(master, value):
    os.write(master, (json.dumps(value)+'\n').encode())


def commands(master):
    data = bytearray()
    while True:
        try: data.extend(os.read(master, 65536))
        except BlockingIOError: break
    values = []
    for line in data.splitlines():
        try: value = json.loads(line)
        except Exception: continue
        if isinstance(value, dict) and value.get('T') == 13: values.append(value)
    return values


def test_full_serial_feedback_odom_and_stop_chain(node, monkeypatch):
    n, master, _ = node
    published = []
    messages = []
    publish = n.odom_pub.publish
    monkeypatch.setattr(n.odom_pub, 'publish', lambda msg: (messages.append(msg), publish(msg)))
    original = n._publish_odom
    n._publish_odom = lambda stamp, sample: (published.append(sample), original(stamp, sample))
    send(master, packet());spin(n)
    send(master, packet());spin(n)
    assert n._feedback_ready(time.monotonic())
    cmd = Twist();cmd.linear.x=.1;cmd.angular.z=.4
    n._cmd_vel_callback(cmd);spin(n)
    assert any(c['X'] == .1 and c['Z'] == .4 for c in commands(master))
    assert len(published) == 1
    assert published[0]['angular_velocity'] == 0.
    assert not published[0]['yaw_rate_valid']
    assert messages[0].twist.covariance[0] == .0025
    assert messages[0].twist.covariance[35] == 1e6
    assert messages[0].header.stamp.sec > 0
    spin(n, .25)
    assert commands(master)[-1]['X'] == 0.
    assert len(published) == 1  # timer did not create fictitious new samples
    send(master, packet());spin(n)  # rebaseline after gap
    send(master, packet());spin(n)
    assert commands(master)[-1]['X'] == 0.  # recovery needs a new command
    n._diagnostic_callback()


def test_partial_serial_line_cannot_block_stop(node):
    n, master, _ = node
    os.write(master, b'{"T":1001')
    spin(n, .03)
    started = time.monotonic()
    n._heartbeat_callback()
    assert time.monotonic()-started < .1
    assert commands(master)[-1]['X'] == 0.


def test_second_driver_cannot_mutate_service_or_device(node):
    n, master, _ = node
    before = list(Service.calls)
    commands(master)
    with pytest.raises(RuntimeError, match='Another driver'):
        driver.WaveRoverDriver()
    assert Service.calls == before
    assert not commands(master)


def test_invalid_feedback_and_bad_command_stop(node):
    n, master, _ = node
    send(master, packet());spin(n)
    send(master, packet());spin(n)
    cmd = Twist();cmd.linear.x=.1
    n._cmd_vel_callback(cmd)
    bad=packet();bad['dist_L']=float('nan')
    send(master, bad);spin(n)
    assert commands(master)[-1]['X'] == 0.
    assert not n._feedback_ready(time.monotonic())


def test_clock_jump_rebaselines_without_integrating(node, monkeypatch):
    n, master, _ = node
    send(master, packet());spin(n)
    send(master, packet());spin(n)
    n.last_ros_sample = (1e12, time.monotonic())
    send(master, packet());spin(n)
    assert n.tracker.last_error == 'ros_clock_jump'
    assert not n._feedback_ready(time.monotonic())


def test_failed_initialization_restores_owned_service_and_releases_lock(node, monkeypatch):
    n, master, port = node
    n._cleanup_hardware()
    before = len(Service.calls)
    monkeypatch.setattr(driver.SerialTransport, 'open', lambda self: False)
    with pytest.raises(RuntimeError, match='Serial port'):
        driver.WaveRoverDriver()
    assert Service.calls[before:] == ['stop', 'start']
    lock = DeviceLock(port).acquire()
    lock.close()


@pytest.mark.parametrize('active', [True, False])
def test_service_guard_restores_only_previously_active_service(monkeypatch, active):
    calls = []
    def run(args, **kwargs):
        calls.append(args)
        return SimpleNamespace(returncode=(0 if active else 3) if args[:2] == ['systemctl', 'is-active'] else 0,
                               stderr='', stdout='')
    monkeypatch.setattr(driver.subprocess, 'run', run)
    logger = SimpleNamespace(info=lambda text: None, warning=lambda text: None)
    service = driver.DisplayServiceGuard('fake.service', logger)
    service.stop();service.start();service.start()
    actions = [args[-2] for args in calls if 'sudo' in args]
    assert actions == (['stop', 'start'] if active else [])


def test_serial_open_refuses_noncooperating_owner_before_writing(monkeypatch):
    monkeypatch.setattr(driver, 'existing_device_users', lambda port: [123])
    monkeypatch.setattr(driver.serial, 'Serial', lambda *a, **kw: pytest.fail('must not open owned port'))
    logger = SimpleNamespace(error=lambda text: None)
    transport = driver.SerialTransport('/fake', 115200, .05, logger)
    assert not transport.open()


def test_cleanup_releases_ownership_even_if_serial_close_fails(node, monkeypatch):
    n, master, port = node
    close = n.transport.close
    def failing_close():
        close()
        raise OSError('injected close failure')
    monkeypatch.setattr(n.transport, 'close', failing_close)
    with pytest.raises(OSError, match='injected'):
        n._cleanup_hardware()
    assert Service.calls[-1] == 'start'
    lock = DeviceLock(port).acquire()
    lock.close()
