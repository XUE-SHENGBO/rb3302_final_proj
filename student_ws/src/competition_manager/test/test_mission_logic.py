"""Exercise mission safety and scoring rules without a ROS graph or hardware."""

import json
import math
from pathlib import Path
import sys
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).parents[1]))
from competition_manager import mission_manager as runtime  # noqa: E402, I100
from competition_manager import mission_rules as rules  # noqa: E402, I100


LANDMARKS = Path(__file__).parents[1] / 'config/landmarks.yaml'
POSITIONS, NORTH, DIGEST = rules.load_landmarks(LANDMARKS, 'map')


@pytest.mark.parametrize('route', ['BCDA', 'b c d a', 'B,C,D,A', ' B, c, d, a '])
def test_route_normalization(route):
    assert rules.parse_route(route, POSITIONS) == 'BCDA'


@pytest.mark.parametrize('route', ['', 'ABC', 'ABCDE', 'ABCZ', 'A->B', None, 123])
def test_default_requires_exactly_four_valid_letters(route):
    with pytest.raises(ValueError):
        rules.parse_route(route, POSITIONS)


def test_repeated_goals_and_practice_mode():
    assert rules.parse_route('BABA', POSITIONS) == 'BABA'
    assert rules.parse_route('ROS', POSITIONS, 0) == 'ROS'


@pytest.mark.parametrize('invalid', [float('nan'), float('inf'), 'bad', True])
def test_invalid_coordinates_rejected(tmp_path, invalid):
    data = yaml.safe_load(LANDMARKS.read_text())
    data['letters']['A'][0] = invalid
    path = tmp_path / 'points.yaml'
    path.write_text(yaml.safe_dump(data))
    with pytest.raises(ValueError):
        rules.load_landmarks(path, 'map')


def test_map_frame_and_missing_landmarks_rejected(tmp_path):
    with pytest.raises(ValueError):
        rules.load_landmarks(LANDMARKS, 'odom')
    data = yaml.safe_load(LANDMARKS.read_text())
    del data['letters']['X']
    path = tmp_path / 'points.yaml'
    path.write_text(yaml.safe_dump(data))
    with pytest.raises(ValueError):
        rules.load_landmarks(path, 'map')


def test_compass_requires_survey_and_resolves_headings():
    with pytest.raises(ValueError, match='Survey'):
        rules.initial_coordinates('A', 'N', POSITIONS, None)
    assert rules.initial_coordinates('A', 'E', POSITIONS, math.pi / 2)[2] == 0
    assert rules.initial_coordinates('A', 'W', POSITIONS, math.pi / 2)[2] == math.pi


def test_approach_heading_avoids_fixed_east_and_handles_duplicate():
    assert rules.approach_heading((0, 0, 0), (0, 1)) == math.pi / 2
    assert rules.approach_heading((0, 0, 1.2), (0, 0)) == 1.2


def test_dwell_requires_continuous_stationarity_and_full_final_interval():
    stop = rules.StopWindow(3)
    assert not stop.update(0, True)
    assert not stop.update(2.99, True)
    assert not stop.update(3, False)
    assert not stop.update(4, True)
    assert not stop.update(6.99, True)
    assert stop.update(7, True)


@pytest.mark.parametrize('duration', [0, 2.99, float('nan')])
def test_dwell_cannot_be_shortened_below_three_seconds(duration):
    with pytest.raises(ValueError):
        rules.StopWindow(duration)


def make_node(tmp_path, monkeypatch, **overrides):
    node = runtime.MissionManager.__new__(runtime.MissionManager)
    values = {
        'dwell_sec': 3.0, 'arrival_timeout_sec': 15.0, 'arrival_tolerance': .08,
        'mission_timeout_sec': 180.0, 'goal_timeout_sec': 60.0,
        'telemetry_timeout_sec': .5, 'stopped_linear_tolerance': .02,
        'stopped_angular_tolerance': .05, 'max_retries': 1,
        'failure_policy': 'stop', 'goal_heading_mode': 'approach',
        'fixed_goal_yaw': 0., 'validate_only': False, 'start_automatically': False,
    }
    values.update(overrides)
    node.p = lambda name: values[name]
    node.get_logger = Mock(return_value=Mock())
    node._stop_pub = Mock()
    node._deadline = None
    node._task_active = False
    node._explicit_initial_pose = False
    node._start_requested = __import__('threading').Event()
    node._ready = False
    node._result_path = str(tmp_path / 'mission.json')
    node._state = {
        'version': 1, 'route': 'BABA', 'landmarks_sha256': DIGEST,
        'mission_timeout_sec': 180.0, 'started_at_unix': None,
        'visits': [{'letter': x, 'status': 'pending'} for x in 'BABA'],
    }
    clock = SimpleNamespace(now=100.0)
    monkeypatch.setattr(runtime.time, 'monotonic', lambda: clock.now)
    monkeypatch.setattr(runtime.time, 'time', lambda: clock.now + 1000)
    monkeypatch.setattr(runtime.rclpy, 'ok', lambda: True)

    def spin(seconds=.05, check_deadline=True):
        clock.now += seconds
        if check_deadline:
            node._check_deadline()
    node._spin = spin
    node._current_pose = lambda: (0., 0., 0.)
    node._stationary = lambda: True
    node.waitUntilNav2Active = Mock()
    node._validate = lambda: ('BABA', POSITIONS, None)
    node.stop_task = Mock(return_value=True)

    def start():
        node._state['started_at_unix'] = runtime.time.time()
        node._deadline = clock.now + values['mission_timeout_sec']
    node._wait_for_start = start
    return node, clock


def test_every_goal_including_last_gets_three_second_dwell(tmp_path, monkeypatch):
    node, clock = make_node(tmp_path, monkeypatch)
    arrivals = []

    def move(target):
        arrivals.append((clock.now, target))
        node._current_pose = lambda: target
    node._navigate = move
    assert node.run_mission()
    assert len(arrivals) == 4
    assert all(b[0] - a[0] >= 3 for a, b in zip(arrivals, arrivals[1:]))
    assert clock.now - arrivals[-1][0] >= 3
    result = json.loads(Path(node._result_path).read_text())
    assert result['status'] == 'completed'
    assert all(v['status'] == 'completed' for v in result['visits'])


def test_global_deadline_during_final_dwell_is_not_success(tmp_path, monkeypatch):
    node, clock = make_node(tmp_path, monkeypatch, mission_timeout_sec=10.)
    node._navigate = lambda target: setattr(node, '_current_pose', lambda: target)
    with pytest.raises(runtime.MissionExpired):
        node.run_mission()
    assert node._state['visits'][-1]['status'] == 'dwelling'
    assert clock.now < 110.1
    node._stop_pub.publish.assert_called()


def test_retry_time_is_part_of_same_round_budget(tmp_path, monkeypatch):
    node, clock = make_node(tmp_path, monkeypatch, mission_timeout_sec=10.)
    attempts = []

    def move(target):
        attempts.append(target)
        clock.now += 6
        node._check_deadline()
        raise runtime.GoalFailed('blocked')
    node._navigate = move
    with pytest.raises(runtime.MissionExpired):
        node.run_mission()
    assert len(attempts) == 2
    assert node._deadline == 110


def test_failed_goal_stops_after_bounded_retries(tmp_path, monkeypatch):
    node, _ = make_node(tmp_path, monkeypatch)
    node._navigate = Mock(side_effect=runtime.GoalFailed('blocked'))
    assert not node.run_mission()
    assert node._navigate.call_count == 2
    assert node._state['status'] == 'failed'
    assert node._state['visits'][1]['status'] == 'pending'


def test_skipped_goal_is_reported_partial_not_success(tmp_path, monkeypatch):
    node, _ = make_node(tmp_path, monkeypatch, failure_policy='skip', max_retries=0)
    node._navigate = Mock(side_effect=runtime.GoalFailed('blocked'))
    assert not node.run_mission()
    assert node._navigate.call_count == 4
    assert node._state['status'] == 'partial'
    assert all(v['status'] == 'skipped' for v in node._state['visits'])


def test_unconfirmed_cancel_prevents_retry_or_skip(tmp_path, monkeypatch):
    node, _ = make_node(tmp_path, monkeypatch, failure_policy='skip')
    node._navigate = Mock(side_effect=runtime.GoalFailed('blocked'))
    node.stop_task.return_value = False
    with pytest.raises(RuntimeError, match='Cancellation unconfirmed'):
        node.run_mission()
    assert node._navigate.call_count == 1


def test_dwell_refuses_outside_position_even_if_stationary(tmp_path, monkeypatch):
    node, _ = make_node(tmp_path, monkeypatch, arrival_timeout_sec=3.1)
    node._deadline = 280.
    with pytest.raises(runtime.GoalFailed, match='verify'):
        node._dwell((2., 2., 0.))


def test_stale_odometry_and_nonzero_motion_do_not_count(tmp_path, monkeypatch):
    node, clock = make_node(tmp_path, monkeypatch)
    del node._stationary
    twist = SimpleNamespace(linear=SimpleNamespace(x=0., y=0.), angular=SimpleNamespace(z=0.))
    node._odom_sample = (clock.now - .6, twist)
    assert not node._stationary()
    node._odom_sample = (clock.now, twist)
    assert node._stationary()
    twist.angular.z = .1
    assert not node._stationary()


def test_start_service_rejects_early_requests(tmp_path, monkeypatch):
    node, _ = make_node(tmp_path, monkeypatch)
    response = SimpleNamespace()
    assert not node._start_callback(None, response).success
    assert not node._start_requested.is_set()
    node._ready = True
    assert node._start_callback(None, response).success
    assert node._start_requested.is_set()
    node._deadline = 280.
    assert not node._start_callback(None, response).success


def test_gate_wait_excluded_but_resume_downtime_included(tmp_path, monkeypatch):
    node, clock = make_node(tmp_path, monkeypatch)
    del node._wait_for_start
    monkeypatch.setattr(runtime.sys, 'stdin', SimpleNamespace(isatty=lambda: False))
    original_spin = node._spin

    def spin(*args, **kwargs):
        original_spin(*args, **kwargs)
        if clock.now >= 105:
            node._start_requested.set()
    node._spin = spin
    node._wait_for_start()
    assert node._deadline - clock.now == 180
    node._deadline = None
    node._state['started_at_unix'] = 1000.
    node._wait_for_start()
    assert abs(node._deadline - clock.now - (180 - clock.now)) < 1e-6


def test_resume_does_not_repeat_completed_duplicate_visit(tmp_path, monkeypatch):
    node, _ = make_node(tmp_path, monkeypatch)
    node._state['started_at_unix'] = 1000.
    node._state['visits'][0]['status'] = 'completed'
    rules.write_checkpoint(node._result_path, node._state)
    loaded = rules.read_checkpoint(node._result_path, 'BABA', DIGEST, 180.)
    node._state = loaded
    node._navigate = Mock(
        side_effect=lambda target: setattr(node, '_current_pose', lambda: target))
    assert node.run_mission()
    assert node._navigate.call_count == 3


def test_resume_mismatched_route_and_tampered_order_rejected(tmp_path, monkeypatch):
    node, _ = make_node(tmp_path, monkeypatch)
    node._state['started_at_unix'] = 1000.
    rules.write_checkpoint(node._result_path, node._state)
    with pytest.raises(ValueError):
        rules.read_checkpoint(node._result_path, 'ABAB', DIGEST, 180.)
    node._state['visits'][1]['status'] = 'completed'
    rules.write_checkpoint(node._result_path, node._state)
    with pytest.raises(ValueError, match='prefix'):
        rules.read_checkpoint(node._result_path, 'BABA', DIGEST, 180.)


@pytest.mark.parametrize('already_received', [True, False])
def test_rviz_pose_never_overwritten(tmp_path, monkeypatch, already_received):
    node, _ = make_node(tmp_path, monkeypatch)
    node.initial_pose_received = already_received
    node._setInitialPose = Mock()
    node._spin = lambda: setattr(node, 'initial_pose_received', True)
    node._waitForInitialPose()
    node._setInitialPose.assert_not_called()


def test_explicit_pose_keeps_parent_initialization(tmp_path, monkeypatch):
    node, _ = make_node(tmp_path, monkeypatch)
    node._explicit_initial_pose = True
    parent = Mock()
    monkeypatch.setattr(runtime.BasicNavigator, '_waitForInitialPose', parent)
    node._waitForInitialPose()
    parent.assert_called_once()
