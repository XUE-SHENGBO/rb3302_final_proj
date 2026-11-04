"""Verify rejection paths, bounded stationary refinement and recovery ordering."""
import math
from pathlib import Path
import sys
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

sys.path.insert(0, str(Path(__file__).parents[1]))
from competition_manager import localization_guard as guard
from geometry_msgs.msg import PoseWithCovarianceStamped, Transform
from nav_msgs.msg import OccupancyGrid
from sensor_msgs.msg import LaserScan
from rclpy.clock import ClockType


def test_covariance_checks_xy_correlation_and_invalid_values():
    msg = PoseWithCovarianceStamped()
    msg.pose.covariance[0] = msg.pose.covariance[7] = .02
    msg.pose.covariance[35] = .01
    assert guard.covariance_ok(msg, .15, .2)
    msg.pose.covariance[1] = msg.pose.covariance[6] = .019
    assert not guard.covariance_ok(msg, .15, .2)  # Diagonals alone would pass.
    for value in (-1., math.nan, math.inf):
        msg.pose.covariance[0] = value
        assert not guard.covariance_ok(msg, .15, .2)


def test_stability_checks_all_pairs_and_wrapped_angles():
    assert guard.stable([(0,0,math.pi-.01), (.01,0,-math.pi+.01)], .04, .05)
    assert not guard.stable([(0,0,0), (.03,0,0), (-.03,0,0)], .04, .05)
    assert not guard.stable([(0,0,0), (0,0,.1)], .04, .05)
    assert not guard.stable([(0,0,math.nan)], .04, .05)


def test_scan_match_rejects_no_returns_unknown_and_misaligned_walls():
    scan = LaserScan()
    scan.range_min, scan.range_max = .1, 10.
    scan.ranges = [1.] * 30
    grid = OccupancyGrid()
    grid.info.resolution = .1
    grid.info.width = grid.info.height = 40
    grid.info.origin.position.x = grid.info.origin.position.y = -2.
    grid.info.origin.orientation.w = 1.
    grid.data = [0]*1600
    grid.data[20*40+30] = 100
    transform = Transform()
    transform.rotation.w = 1.
    assert guard.scan_match(scan, transform, grid, .1) == 1.
    transform.translation.x = .4
    assert guard.scan_match(scan, transform, grid, .1) == 0.
    transform.translation.x = 0.
    grid.data[20*40+30] = -1
    assert guard.scan_match(scan, transform, grid, .1) == 0.
    scan.ranges = [math.inf, math.nan, 0.] * 30
    assert guard.scan_match(scan, transform, grid, .1) == 0.


def test_duplicate_amcl_messages_do_not_renew_freshness(monkeypatch):
    node = guard.LocalizationGuard()
    node._loc_pose = None
    node.p = guard.DEFAULTS.__getitem__
    node._loc_history = guard.deque(maxlen=3)
    node._loc_matched_scans = guard.deque(maxlen=3)
    clock = SimpleNamespace(now=1.)
    monkeypatch.setattr(guard.time, 'monotonic', lambda: clock.now)
    msg = PoseWithCovarianceStamped()
    msg.header.stamp.sec = 5
    node._localization_pose_callback(msg)
    clock.now = 3.
    node._localization_pose_callback(msg)
    assert len(node._loc_history) == 1
    assert node._loc_pose[0] == 1.


def make_guard(monkeypatch, good_after=None):
    node = guard.LocalizationGuard()
    clock = SimpleNamespace(now=0., polls=0)
    values = dict(guard.DEFAULTS, localization_timeout_sec=1., localization_max_updates=3)
    node.p = values.__getitem__
    node._loc_history = guard.deque(maxlen=3)
    node._loc_matched_scans = guard.deque(maxlen=3)
    node._stop_pub = Mock()
    node.get_logger = Mock(return_value=Mock())
    node._stationary = lambda: True
    node._check_deadline = Mock()
    node._wait_before_retry = Mock()
    node._localization_service = Mock(return_value=True)
    monkeypatch.setattr(guard.time, 'monotonic', lambda: clock.now)
    def spin():
        clock.now += .1
        clock.polls += 1
    node._spin = spin
    node._localization_quality = lambda: (good_after is not None and clock.polls >= good_after,
                                         'synthetic quality')
    return node, clock


def test_unconverged_localization_is_bounded_and_only_sends_stop(monkeypatch):
    node, clock = make_guard(monkeypatch)
    with pytest.raises(guard.LocalizationFailed, match='RViz'):
        node.ensure_localization(force=True)
    assert clock.now < 1.2
    assert node._localization_service.call_count <= 3
    assert all(call.args[0].linear.x == call.args[0].angular.z == 0.
               for call in node._stop_pub.publish.call_args_list)


def test_no_stationary_updates_while_moving(monkeypatch):
    node, _ = make_guard(monkeypatch)
    node._stationary = lambda: False
    with pytest.raises(guard.LocalizationFailed):
        node.ensure_localization(force=True)
    node._localization_service.assert_not_called()


def test_mission_deadline_interrupts_refinement(monkeypatch):
    node, _ = make_guard(monkeypatch)
    node._check_deadline.side_effect = TimeoutError('round expired')
    with pytest.raises(TimeoutError):
        node.ensure_localization()
    node._localization_service.assert_not_called()


def test_costmaps_refreshed_only_after_verified_localization(monkeypatch):
    node, _ = make_guard(monkeypatch, good_after=4)
    node.recover_localization()
    names = [call.args[1] for call in node._localization_service.call_args_list]
    assert names[-2:] == ['global_costmap/clear_entirely_global_costmap',
                          'local_costmap/clear_entirely_local_costmap']
    node._wait_before_retry.assert_called_once()
    node, _ = make_guard(monkeypatch)
    with pytest.raises(guard.LocalizationFailed):
        node.recover_localization()
    assert all('costmap' not in call.args[1] for call in node._localization_service.call_args_list)


def test_healthy_localization_kept_without_resets_or_clears(monkeypatch):
    node, _ = make_guard(monkeypatch, good_after=0)
    node.recover_localization()
    node._localization_service.assert_not_called()


def test_covariance_degradation_resets_consecutive_pose_verification():
    node = guard.LocalizationGuard()
    node.p = guard.DEFAULTS.__getitem__
    node._loc_pose = None
    node._loc_history = guard.deque(maxlen=3)
    msg = PoseWithCovarianceStamped()
    msg.header.stamp.sec = 1
    node._localization_pose_callback(msg)
    assert len(node._loc_history) == 1
    msg.header.stamp.sec = 2
    msg.pose.covariance[0] = 1.
    node._localization_pose_callback(msg)
    assert not node._loc_history


def test_quality_requires_distinct_scan_frames_and_rejects_stale_headers(monkeypatch):
    node, _ = make_guard(monkeypatch)
    del node._localization_quality  # Exercise the real method, not the fixture stub.
    node._current_pose = lambda: (0.,0.,0.)
    node.get_clock = lambda: SimpleNamespace(
        now=lambda: guard.Time(seconds=10, clock_type=ClockType.ROS_TIME))
    msg = PoseWithCovarianceStamped()
    msg.header.frame_id = 'map'
    msg.header.stamp.sec = 10
    msg.pose.pose.orientation.w = 1.
    node._loc_pose = (0.,msg,(10,0))
    node._loc_history.extend([(0.,0.,0.)]*3)
    scan = LaserScan()
    scan.header.stamp.sec = 10
    scan.range_min, scan.range_max = .1, 10.
    scan.ranges = [1.]*30
    node._loc_scan = (0.,scan)
    grid = OccupancyGrid()
    grid.header.frame_id = 'map'
    grid.info.resolution = .1
    grid.info.width = grid.info.height = 40
    grid.info.origin.position.x = grid.info.origin.position.y = -2.
    grid.info.origin.orientation.w = 1.
    grid.data = [0]*1600
    grid.data[20*40+30] = 100
    node._loc_map = grid
    transform = Transform()
    transform.rotation.w = 1.
    node._tf = SimpleNamespace(lookup_transform=lambda *args: SimpleNamespace(transform=transform))
    node.p = dict(guard.DEFAULTS, map_frame='map', telemetry_timeout_sec=.5).__getitem__
    assert not node._localization_quality()[0]
    assert not node._localization_quality()[0]  # Rechecking one frame is not new evidence.
    scan.header.stamp.nanosec = 1
    assert not node._localization_quality()[0]
    scan.header.stamp.nanosec = 2
    assert node._localization_quality()[0]
    msg.header.stamp.sec = 5
    assert not node._localization_quality()[0]
