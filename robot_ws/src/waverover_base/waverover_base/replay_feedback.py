"""Offline protocol audit; opens a bag only, never opens serial or creates a node."""
import argparse
from collections import Counter
import json

from waverover_base.feedback import FeedbackTracker


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bag')
    parser.add_argument('--start', type=float, default=0., help='Unix receive time, seconds')
    parser.add_argument('--duration', type=float, default=float('inf'))
    parser.add_argument('--output')
    args = parser.parse_args()
    # ROS libraries are needed for deserialization, but no ROS graph is initialized.
    import rosbag2_py
    from rclpy.serialization import deserialize_message
    from rosidl_runtime_py.utilities import get_message
    reader = rosbag2_py.SequentialReader()
    reader.open(rosbag2_py.StorageOptions(uri=args.bag, storage_id='mcap'),
                rosbag2_py.ConverterOptions('', ''))
    types = {t.name: get_message(t.type) for t in reader.get_all_topics_and_types()}
    topic = '/waverover/json_feedback'
    if topic not in types:
        parser.error('Bag has no /waverover/json_feedback')
    reader.set_filter(rosbag2_py.StorageFilter(topics=[topic]))
    trackers = {s: FeedbackTracker(source=s) for s in ('firmware_centre', 'wheel_mean')}
    counts = Counter()
    distance = Counter()
    intervals = []
    last = None
    while reader.has_next():
        _, raw, ns = reader.read_next()
        t = ns / 1e9
        if not args.start <= t <= args.start + args.duration:
            continue
        msg = deserialize_message(raw, types[topic])
        try:
            packet = json.loads(msg.data)
        except (ValueError, TypeError):
            counts['invalid_json'] += 1
            continue
        if not isinstance(packet, dict) or packet.get('T') != 1001:
            continue
        counts['packets'] += 1
        if last is not None:
            intervals.append(t - last)
        last = t
        for source, tracker in trackers.items():
            sample = tracker.update(packet, t)
            if source == 'firmware_centre':
                counts[tracker.last_error or 'accepted'] += 1
            if sample is not None:
                distance[source] += sample['linear_velocity'] * sample['dt']
    intervals.sort()
    result = {'counts': dict(counts), 'integrated_signed_distance_m': dict(distance),
              'receive_intervals_sec': {str(q): intervals[min(len(intervals)-1, int(q*(len(intervals)-1)))]
                                        for q in (.5, .95, .99, 1.)} if intervals else {},
              'limitations': 'Recorded topic arrival times are not hardware sampling times. '
              'The old publisher may repeat cached feedback. This is an offline comparison, '
              'not validation of wheel scale or approval to switch the live source.'}
    text = json.dumps(result, indent=2)
    if args.output:
        from pathlib import Path
        Path(args.output).write_text(text + '\n')
    print(text)


if __name__ == '__main__':
    main()
