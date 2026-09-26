"""Test route policy without requiring a running ROS graph or robot."""

import ast
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock
import math

import pytest


# Load the policy definitions without importing unavailable ROS dependencies.
source = Path(__file__).parents[1] / 'competition_manager' / 'mission_manager.py'
tree = ast.parse(source.read_text())
tree.body = [item for item in tree.body if isinstance(item, (ast.FunctionDef, ast.ClassDef))]
namespace = {
    'math': math, 'BasicNavigator': object,
    'TaskResult': SimpleNamespace(SUCCEEDED=1),
    'time': SimpleNamespace(monotonic=lambda: 0.0),
}
exec(compile(tree, str(source), 'exec'), namespace)
parse_poses = namespace['parse_poses']


def make_node(results):
    cls = namespace['MissionManager']
    node = cls.__new__(cls)
    values = {'goals': [1., 2., 0., 3., 4., 0.], 'goal_timeout_sec': 10.,
              'map_frame': 'map', 'set_initial_pose': False}
    node.get_parameter = lambda name: SimpleNamespace(value=values[name])
    node.get_logger = Mock(return_value=Mock())
    node.make_pose = lambda pose: pose
    node.waitUntilNav2Active = Mock()
    node.goToPose = Mock(return_value=True)
    node.isTaskComplete = Mock(return_value=True)
    node.getResult = Mock(side_effect=results)
    node.cancelTask = Mock()
    node._task_active = False
    return node


@pytest.mark.parametrize('values', [[], [1., 2.], [1., 2., float('nan')]])
def test_invalid_route(values):
    with pytest.raises(ValueError):
        parse_poses(values, 'goals')


def test_ordered_success():
    node = make_node([1, 1])
    assert node.run_mission()
    assert [call.args[0] for call in node.goToPose.call_args_list] == [
        (1., 2., 0.), (3., 4., 0.)]


def test_failure_stops_remaining_goals():
    node = make_node([2])
    assert not node.run_mission()
    assert node.goToPose.call_count == 1


def test_rejection_stops_remaining_goals():
    node = make_node([])
    node.goToPose.return_value = False
    assert not node.run_mission()
    node.getResult.assert_not_called()
    assert node.goToPose.call_count == 1


def test_timeout_cancels_and_stops(monkeypatch):
    clock = Mock(side_effect=[0., 11.])
    monkeypatch.setattr(namespace['time'], 'monotonic', clock)
    node = make_node([])
    node.isTaskComplete.return_value = False
    assert not node.run_mission()
    node.cancelTask.assert_called_once()
    assert node.goToPose.call_count == 1
