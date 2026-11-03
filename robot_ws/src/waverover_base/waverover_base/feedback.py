"""Feedback validation and wheel diagnostics, independent of ROS and serial IO."""
import math


def finite(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


class FeedbackTracker:
    """One update per received complete T=1001 packet; no cached timer samples.

    Equal values in separately received packets are valid stationary observations.
    Optional firmware sequence fields distinguish retransmission from new packets.
    Host monotonic receive time is used when no verified hardware clock is available.
    """

    def __init__(self, source='firmware_centre', yaw_unit='radians',
                 max_gap=.5, max_wheel_speed=1.5, max_yaw_rate=12.,
                 track_width=.125, wheel_yaw_rate_enabled=False, sequence_field=''):
        if source not in ('firmware_centre', 'wheel_mean'):
            raise ValueError('odom_distance_source must be firmware_centre or wheel_mean')
        if yaw_unit not in ('radians', 'degrees'):
            raise ValueError('yaw_odom_unit must be radians or degrees')
        for value in (max_gap, max_wheel_speed, max_yaw_rate, track_width):
            if not finite(value) or value <= 0:
                raise ValueError('Feedback limits and track_width must be finite and positive')
        self.source, self.yaw_unit = source, yaw_unit
        self.max_gap, self.max_wheel_speed = max_gap, max_wheel_speed
        self.max_yaw_rate, self.track_width = max_yaw_rate, track_width
        self.wheel_yaw_rate_enabled = wheel_yaw_rate_enabled
        self.sequence_field = sequence_field
        self.previous = None
        self.last_received = None
        self.last_valid = None
        self.last_sequence = None
        self.sequence = 0
        self.invalid_count = 0
        self.reset_count = 0
        self.last_error = 'waiting_for_feedback'
        self.x = self.y = 0.
        self.yaw = None
        self.latest = None

    def _reject(self, reason, rebase=None):
        self.invalid_count += 1
        self.last_error = reason
        self.last_valid = None
        if rebase is not None:
            self.previous = rebase
            self.yaw = rebase['yaw']
            self.reset_count += 1
        return None

    def update(self, data, received_at):
        if data.get('T') != 1001:
            return None
        self.last_received = received_at
        required = ('dist_L', 'dist_R', 'dist_centre', 'yaw_odom', 'voltage', 'encA', 'encB')
        if not finite(received_at) or any(not finite(data.get(k)) for k in required):
            return self._reject('incomplete_or_nonfinite_feedback')
        if any(int(data[k]) != data[k] for k in ('encA', 'encB')):
            return self._reject('invalid_encoder_count')
        if self.sequence_field:
            seq = data.get(self.sequence_field)
            if not finite(seq) or int(seq) != seq:
                return self._reject('invalid_firmware_sequence')
            if self.last_sequence is not None and seq <= self.last_sequence:
                # Invalidate and re-establish a baseline after restart/retransmit.
                self.last_sequence = seq
                self.previous = None
                return self._reject('duplicate_or_reset_firmware_sequence')
            self.last_sequence = seq
        yaw = float(data['yaw_odom'])
        if self.yaw_unit == 'degrees':
            yaw = math.radians(yaw)
        now = {'time': received_at, 'yaw': yaw, **{k: float(data[k]) for k in required if k != 'yaw_odom'}}
        self.sequence += 1
        prev = self.previous
        if prev is None:
            self.previous = now
            self.yaw = yaw
            self.last_error = 'baseline_only'
            return None
        dt = received_at - prev['time']
        if dt <= 0:
            return self._reject('nonpositive_interval', now)
        if dt > self.max_gap:
            return self._reject('feedback_gap_rebased', now)
        dl, dr, dc = (now[k] - prev[k] for k in ('dist_L', 'dist_R', 'dist_centre'))
        dyaw = math.atan2(math.sin(yaw - prev['yaw']), math.cos(yaw - prev['yaw']))
        if max(abs(dl), abs(dr), abs(dc)) > self.max_wheel_speed * dt or abs(dyaw) > self.max_yaw_rate * dt:
            return self._reject('implausible_increment_rebased', now)
        # Firmware encoder resets must not become even small fictitious motion.
        if ((now['encA'] == 0 and now['encB'] == 0)
                and (prev['encA'] != 0 or prev['encB'] != 0)):
            return self._reject('encoder_reset_rebased', now)
        wheel_ds = (dl + dr) / 2.
        ds = dc if self.source == 'firmware_centre' else wheel_ds
        heading = self.yaw + dyaw / 2.
        self.x += ds * math.cos(heading)
        self.y += ds * math.sin(heading)
        self.yaw += dyaw
        self.previous = now
        self.last_valid = received_at
        self.last_error = ''
        self.latest = {
            'sequence': self.sequence, 'received_monotonic': received_at, 'dt': dt,
            'x': self.x, 'y': self.y, 'yaw': self.yaw,
            'linear_velocity': ds / dt,
            'centre_velocity': dc / dt, 'wheel_mean_velocity': wheel_ds / dt,
            'distance_residual': dc - wheel_ds,
            'wheel_yaw_rate': (dr - dl) / (self.track_width * dt),
            'yaw_rate_valid': self.wheel_yaw_rate_enabled,
            'angular_velocity': (dr - dl) / (self.track_width * dt) if self.wheel_yaw_rate_enabled else 0.,
            'delta_left': dl, 'delta_right': dr, 'delta_centre': dc,
        }
        return dict(self.latest)

    def ready(self, now, timeout):
        return self.last_valid is not None and 0 <= now - self.last_valid <= timeout

    def reset(self, reason):
        self.previous = None
        self.last_valid = None
        self.last_error = reason
        self.reset_count += 1


class MotionGate:
    """Feedback loss discards the old command; recovery needs a NEW command."""

    def __init__(self, max_linear, max_angular):
        self.max_linear, self.max_angular = max_linear, max_angular
        self.command = (0., 0.)
        self.command_at = None
        self.reason = 'waiting_for_command'

    def receive(self, linear, angular, now, feedback_ready):
        if not all(finite(v) for v in (linear, angular, now)):
            self.invalidate('invalid_command')
            return self.command
        if not feedback_ready:
            self.invalidate('feedback_unavailable')
            return self.command
        self.command = (max(-self.max_linear, min(self.max_linear, linear)),
                        max(-self.max_angular, min(self.max_angular, angular)))
        self.command_at = now
        self.reason = 'clear'
        return self.command

    def invalidate(self, reason):
        self.command = (0., 0.)
        self.command_at = None
        self.reason = reason

    def output(self, now, timeout, feedback_ready):
        if not feedback_ready:
            self.invalidate('feedback_unavailable')
        elif self.command_at is None or not 0 <= now - self.command_at <= timeout:
            self.invalidate('command_timeout')
        return self.command
