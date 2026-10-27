"""Validate mission inputs and track timing without ROS or robot hardware."""

import hashlib
import json
import math
from pathlib import Path

import yaml


def positive(value, name, minimum=0.0):
    """Require a finite number strictly above zero and at least minimum."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f'{name} must be a number')
    if not math.isfinite(value) or value <= 0.0 or value < minimum:
        raise ValueError(f'{name} must be finite, positive and >= {minimum}')
    return float(value)


def load_landmarks(filename, map_frame):
    """Read measured positions and optional surveyed compass alignment."""
    data = yaml.safe_load(Path(filename).expanduser().read_text())
    if not isinstance(data, dict) or data.get('map_frame') != map_frame:
        raise ValueError('Landmark map_frame must match the navigation map_frame')
    letters = data.get('letters')
    if not isinstance(letters, dict) or set(letters) != set('ABCDEFGHIJKLMNOPQRSTUVWX'):
        raise ValueError('Landmark file must contain every letter A through X exactly once')
    positions = {}
    for key, value in letters.items():
        if not isinstance(value, list) or len(value) != 2:
            raise ValueError(f'{key} must contain [x, y]')
        if not all(isinstance(v, (int, float)) and not isinstance(v, bool)
                   and math.isfinite(v) for v in value):
            raise ValueError(f'{key} must contain finite numeric coordinates')
        positions[key] = tuple(float(v) for v in value)
    north = data.get('map_north_yaw')
    if north is not None and (isinstance(north, bool)
                              or not isinstance(north, (int, float))
                              or not math.isfinite(north)):
        raise ValueError('map_north_yaw must be a finite number or null')
    digest = hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
    return positions, north, digest


def parse_route(value, positions, required_count=4):
    """Normalize ordered letters; repeated landmarks remain separate visits."""
    if not isinstance(required_count, int) or required_count < 0:
        raise ValueError('required_goal_count must be a nonnegative integer')
    if not isinstance(value, str):
        raise ValueError('goals must be a string of letters')
    route = ''.join(value.upper().replace(',', ' ').split())
    if not route or set(route) - positions.keys():
        raise ValueError('goals must contain only letters A through X')
    if required_count and len(route) != required_count:
        raise ValueError(f'Exactly {required_count} goals are required; got {len(route)}')
    return route


def initial_coordinates(letter, heading, positions, north):
    """Resolve a start cell and compass heading using surveyed map north."""
    letter, heading = letter.upper().strip(), heading.upper().strip()
    if letter not in positions or heading not in ('N', 'E', 'S', 'W'):
        raise ValueError('initial_letter must be A-X and initial_heading must be N/E/S/W')
    if north is None:
        raise ValueError('Survey map_north_yaw in landmarks.yaml before using compass headings')
    yaw = north + {'N': 0.0, 'E': -math.pi / 2, 'S': math.pi, 'W': math.pi / 2}[heading]
    return (*positions[letter], math.atan2(math.sin(yaw), math.cos(yaw)))


def approach_heading(current, target):
    """Face along the incoming leg; preserve yaw for repeated nearby goals."""
    dx, dy = target[0] - current[0], target[1] - current[1]
    return math.atan2(dy, dx) if math.hypot(dx, dy) > 0.01 else current[2]


class StopWindow:
    """Count only uninterrupted, measured stationary time inside the target."""

    def __init__(self, duration):
        self.duration = positive(duration, 'dwell_sec', minimum=3.0)
        self.since = None

    def update(self, now, valid):
        """Reset the clock on motion, stale telemetry or position error."""
        if not valid:
            self.since = None
            return False
        if self.since is None:
            self.since = now
        return now - self.since >= self.duration


def read_checkpoint(filename, route, digest, timeout):
    """Reject incompatible or malformed recovery records before navigation."""
    data = json.loads(Path(filename).expanduser().read_text())
    if (data.get('version') != 1 or data.get('route') != route
            or data.get('landmarks_sha256') != digest
            or data.get('mission_timeout_sec') != timeout):
        raise ValueError('Resume record does not match route, landmarks or mission timeout')
    start = data.get('started_at_unix')
    positive(start, 'checkpoint started_at_unix')
    visits = data.get('visits')
    if not isinstance(visits, list) or len(visits) != len(route):
        raise ValueError('Invalid checkpoint visits')
    for letter, visit in zip(route, visits):
        if (not isinstance(visit, dict) or visit.get('letter') != letter
                or visit.get('status') not in
                ('pending', 'moving', 'dwelling', 'completed', 'skipped', 'failed')):
            raise ValueError('Invalid checkpoint visit')
    # Completed/skipped visits must form a prefix; never silently omit later goals.
    pending_seen = False
    for visit in visits:
        if visit['status'] in ('completed', 'skipped'):
            if pending_seen:
                raise ValueError('Checkpoint completed visits must be an ordered prefix')
        else:
            pending_seen = True
    return data


def write_checkpoint(filename, data):
    """Atomically persist progress for explicit recovery after interruption."""
    path = Path(filename).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
    temporary.replace(path)
