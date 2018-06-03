
class CommunicatorEvent:
    event_args_start = 1
    event_args_stop = 2
    args = None

    def __init__(self, args):
        self.args = args
