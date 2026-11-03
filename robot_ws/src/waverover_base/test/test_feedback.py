import math
import os
import subprocess
import sys

import pytest
from waverover_base.feedback import FeedbackTracker, MotionGate
from waverover_base.device_lock import DeviceLock, existing_device_users


def packet(left=0., right=0., centre=0., yaw=0., **extra):
    return dict(T=1001, dist_L=left, dist_R=right, dist_centre=centre,
                yaw_odom=yaw, voltage=11.4, encA=100, encB=100, **extra)


def test_rotation_separates_centre_and_wheels_without_switching_source():
    tracker = FeedbackTracker()
    assert tracker.update(packet(), 1.) is None
    sample = tracker.update(packet(.01, -.01, .004, -.1), 1.1)
    assert sample['linear_velocity'] == pytest.approx(.04)
    assert sample['wheel_mean_velocity'] == pytest.approx(0.)
    assert sample['distance_residual'] == pytest.approx(.004)
    assert not sample['yaw_rate_valid']
    assert sample['angular_velocity'] == 0.
    assert sample['wheel_yaw_rate'] == pytest.approx(-1.6)


def test_calibrated_optional_wheel_source_and_reverse():
    tracker = FeedbackTracker(source='wheel_mean', wheel_yaw_rate_enabled=True)
    tracker.update(packet(), 1.)
    sample = tracker.update(packet(-.01, -.02, .03), 1.1)
    assert sample['linear_velocity'] == pytest.approx(-.15)
    assert sample['angular_velocity'] == pytest.approx(-.8)


@pytest.mark.parametrize('field', ['dist_L', 'dist_R', 'dist_centre', 'yaw_odom', 'encA', 'encB', 'voltage'])
@pytest.mark.parametrize('value', [None, float('nan'), float('inf')])
def test_invalid_packet_never_refreshes_validity(field, value):
    tracker = FeedbackTracker()
    tracker.update(packet(), 1.)
    assert tracker.update(packet(), 1.1)
    data = packet();data[field] = value
    assert tracker.update(data, 1.2) is None
    assert not tracker.ready(1.21, .5)


def test_cached_or_other_message_cannot_create_measurement():
    tracker = FeedbackTracker()
    tracker.update(packet(), 1.)
    sample = tracker.update(packet(), 1.1)
    assert sample['linear_velocity'] == 0.
    assert tracker.update({'T': 1002}, 1.3) is None
    assert not tracker.ready(1.7, .5)
    # Separate received identical stationary packets ARE valid measurements.
    assert tracker.update(packet(), 1.4)


def test_sequence_duplicates_and_restarts_reestablish_baseline():
    tracker = FeedbackTracker(sequence_field='seq')
    tracker.update(packet(seq=10), 1.)
    assert tracker.update(packet(seq=11), 1.1)
    assert tracker.update(packet(seq=11), 1.2) is None
    assert not tracker.ready(1.2, .5)
    assert tracker.update(packet(seq=1), 1.3) is None
    assert tracker.update(packet(seq=2), 1.4) is None
    assert tracker.update(packet(seq=3), 1.5)


@pytest.mark.parametrize('at,reason', [(1., 'nonpositive_interval'), (.9, 'nonpositive_interval'),
                                      (2., 'feedback_gap_rebased')])
def test_time_fault_does_not_integrate(at, reason):
    tracker = FeedbackTracker()
    tracker.update(packet(), 1.)
    assert tracker.update(packet(.2, .2, .2), at) is None
    assert tracker.last_error == reason
    assert tracker.x == tracker.y == 0.


def test_counter_reset_and_jump_do_not_create_pose_spike():
    tracker = FeedbackTracker()
    tracker.update(packet(1., 1., 1.), 1.)
    data = packet();data['encA'] = data['encB'] = 0
    assert tracker.update(data, 1.1) is None
    assert tracker.x == 0.
    assert tracker.update(packet(.001, .001, .001), 1.2)
    assert tracker.x == pytest.approx(.001)
    small_reset = packet(.001, .001, .001)
    small_reset['encA'] = small_reset['encB'] = 0
    assert tracker.update(small_reset, 1.3) is None
    assert tracker.last_error == 'encoder_reset_rebased'


def test_explicit_radians_do_not_become_degrees_after_one_turn():
    tracker = FeedbackTracker()
    tracker.update(packet(yaw=6.2), 1.)
    result = tracker.update(packet(yaw=6.4), 1.1)
    assert result['yaw'] == pytest.approx(6.4)
    degrees = FeedbackTracker(yaw_unit='degrees')
    degrees.update(packet(yaw=179.), 1.)
    assert degrees.update(packet(yaw=-179.), 1.1)['yaw'] == pytest.approx(math.radians(181))


def test_feedback_recovery_never_replays_old_motion():
    gate = MotionGate(.2, 1.)
    assert gate.receive(.1, .4, 1., True) == (.1, .4)
    assert gate.output(1.1, .8, False) == (0., 0.)
    assert gate.output(1.2, .8, True) == (0., 0.)
    assert gate.receive(.1, .4, 1.3, True) == (.1, .4)
    assert gate.output(2.2, .8, True) == (0., 0.)


def test_nonfinite_commands_stop_instead_of_clipping_to_maximum():
    gate = MotionGate(.2, 1.)
    gate.receive(.1, .4, 1., True)
    assert gate.receive(float('nan'), .2, 1.1, True) == (0., 0.)


def test_device_lock_is_exclusive_across_processes_and_aliases(tmp_path):
    device = tmp_path/'device';device.touch()
    alias = tmp_path/'alias';alias.symlink_to(device)
    lock = DeviceLock(device, tmp_path).acquire()
    code = 'from waverover_base.device_lock import DeviceLock; DeviceLock(%r,%r).acquire()' % (str(alias), str(tmp_path))
    result = subprocess.run([sys.executable, '-c', code], capture_output=True, env=os.environ)
    assert result.returncode != 0
    lock.close()
    assert subprocess.run([sys.executable, '-c', code], capture_output=True, env=os.environ).returncode == 0


def test_legacy_owner_without_flock_is_detected(tmp_path):
    device = tmp_path/'device';device.touch()
    code = 'import sys; f=open(sys.argv[1]); print("ready",flush=True); sys.stdin.read()'
    child = subprocess.Popen([sys.executable, '-c', code, str(device)],
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    try:
        assert child.stdout.readline().strip() == 'ready'
        assert child.pid in existing_device_users(device)
    finally:
        child.communicate('', timeout=3)
