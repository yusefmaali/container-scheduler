import signal


class GracefulHaltSignalReceiver:
    """Subscribe to SIGINT and SIGTERM signal and set to True"""

    def __init__(self):
        self.signal_caught: bool = False
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, *args):
        self.signal_caught = True

    @property
    def graceful_halt_requested(self):
        return self.signal_caught
