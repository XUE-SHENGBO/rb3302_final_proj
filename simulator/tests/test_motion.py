"""Regression tests for delayed callbacks and collision odometry."""
import sys
from pathlib import Path

import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from simulator import advance_motion


class FreeSpace:
    def collides(self, *args):
        return False


def test_delayed_callback_consumes_full_elapsed_time():
    pose, distance, blocked = advance_motion(FreeSpace(), (0., 0., 0.), (.3, 0.), .2, .18, .17)
    assert pose == pytest.approx((.06, 0., 0.))
    assert distance == pytest.approx(.06)
    assert not blocked


def test_delayed_turn_matches_regular_updates():
    whole, distance, _ = advance_motion(FreeSpace(), (0., 0., 0.), (.3, .5), .2, .18, .17)
    pose = (0., 0., 0.)
    for _ in range(10):
        pose, _, _ = advance_motion(FreeSpace(), pose, (.3, .5), .02, .18, .17)
    assert whole == pytest.approx(pose)
    assert distance == pytest.approx(.06)


def test_collision_does_not_report_commanded_distance_as_motion():
    class Wall:
        def collides(self, x, y, yaw, length, width):
            return x + length / 2 >= .12
    pose, distance, blocked = advance_motion(Wall(), (0., 0., 0.), (.3, 0.), .5, .18, .17)
    assert blocked
    assert pose[0] + .09 < .12
    assert 0 < distance < .03
    assert distance == pytest.approx(pose[0])
