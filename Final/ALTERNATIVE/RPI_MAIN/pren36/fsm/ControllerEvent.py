
class ControllerEvent:
    event_args_none = -1
    event_args_main_stop = 0
    event_args_main_start = 1
    event_args_loc_state = 2
    event_args_improc_start = 3
    event_args_improc_target_found = 4
    event_args_main_finish = 5
    event_args_req_height = 6
    event_args_cube_loc_start = 7
    event_args_cube_loc_stop = 8

    def __init__(self, args, kwargs=None):
        self.args = args
        self.kwargs = kwargs
