"""Safety regression: command bounds, swept body and timeout/stop priority."""
import math
from pathlib import Path
import sys
from types import SimpleNamespace
import time

sys.path.insert(0, str(Path(__file__).parents[1]))
from competition_manager.velocity_guard import bound_axis, swept_collision, VelocityGuard
from geometry_msgs.msg import Twist


def test_request_cannot_be_amplified_by_feedback_or_smoother():
    assert bound_axis(.375, .05, .2) == .05
    assert bound_axis(.375, 0., .2) == 0.
    assert bound_axis(-.1, .1, .2) == 0.
    assert bound_axis(2., 2., .2) == .2
    assert bound_axis(math.nan, .1, .2) == 0.


def test_rectangular_body_and_turn_sweep():
    assert swept_collision([(.25, 0)], .2, 0)
    assert not swept_collision([(.45, 0)], .2, 0)
    assert swept_collision([(.15, 0)], 0, 1.)
    assert swept_collision([(-.25, 0)], -.2, 0)
    assert not swept_collision([(.0, .3)], .2, 0)


def test_gate_stop_and_data_loss():
    now = time.monotonic()
    raw, smooth = Twist(), Twist()
    raw.linear.x = .05
    smooth.linear.x = .375
    output = []
    params = {'command_timeout': .3, 'scan_timeout': .5, 'max_linear': .2,
              'max_angular': 1., 'horizon': .8}
    gate = SimpleNamespace(raw=raw, smooth=smooth, raw_at=now, smooth_at=now,
                           scan_at=now, stop_at=-math.inf, points=[], reason=None,
                           p=params.__getitem__, pub=SimpleNamespace(publish=output.append),
                           get_logger=lambda: SimpleNamespace(info=lambda _: None))
    VelocityGuard.tick(gate)
    assert output[-1].linear.x == .05
    gate.stop_at = now
    VelocityGuard.tick(gate)
    assert output[-1].linear.x == 0.
    gate.stop_at = -math.inf
    gate.scan_at = now - 1.
    VelocityGuard.tick(gate)
    assert output[-1].linear.x == 0.
    gate.scan_at = now
    gate.raw_at = now - 1.
    VelocityGuard.tick(gate)
    assert output[-1].linear.x == 0.
    gate.raw_at = now
    gate.points = [(.14, 0)]
    VelocityGuard.tick(gate)
    assert output[-1].linear.x == 0.
