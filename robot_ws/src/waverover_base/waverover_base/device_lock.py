"""Process ownership held before service management and until serial cleanup."""
import fcntl
import hashlib
import os
from pathlib import Path
import tempfile


def existing_device_users(device):
    """Find legacy local owners that do not participate in our flock protocol."""
    identity = os.stat(device)
    owners = set()
    for process in Path('/proc').iterdir():
        if not process.name.isdigit() or int(process.name) == os.getpid():
            continue
        try:
            entries = (process / 'fd').iterdir()
            for fd in entries:
                try:
                    info = fd.stat()
                except OSError:
                    continue
                if info.st_dev == identity.st_dev and info.st_ino == identity.st_ino:
                    owners.add(int(process.name))
        except (OSError, PermissionError):
            continue
    return sorted(owners)


class DeviceLock:
    def __init__(self, device, directory=None):
        canonical = os.path.realpath(device)
        digest = hashlib.sha256(canonical.encode()).hexdigest()[:24]
        self.path = Path(directory or tempfile.gettempdir()) / ('waverover-' + digest + '.lock')
        self.fd = None

    def acquire(self):
        fd = os.open(self.path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BaseException:
            os.close(fd)
            raise RuntimeError('Another driver owns this device: ' + str(self.path))
        self.fd = fd
        return self

    def close(self):
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None
