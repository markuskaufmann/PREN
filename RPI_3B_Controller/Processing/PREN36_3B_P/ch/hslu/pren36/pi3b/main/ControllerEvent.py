
class ControllerEvent:
    event_args_main_start = 1
    event_args_main_stop = 0
    event_args_improc_target_found = 2
    event_args_loc_state = 3
    args = None
    kwargs = None

    def __init__(self, args, kwargs=None):
        self.args = args
