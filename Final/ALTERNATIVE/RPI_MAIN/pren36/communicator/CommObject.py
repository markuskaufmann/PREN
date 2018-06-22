import ctypes
from multiprocessing import Value, Array


class CommObject(object):
    started = False
    stopped = False
    state = b''
    x = 0
    z = 0

    def __init__(self):
        self.started = Value(ctypes.c_bool, False)
        self.stopped = Value(ctypes.c_bool, False)
        self.state = Array(ctypes.c_char, 100)
        self.x = Value(ctypes.c_float, 0)
        self.z = Value(ctypes.c_float, 0)

    def update_state(self, state):
        self.state.value = bytes(state, encoding='utf-8')

    def update_loc(self, x, z):
        self.x.value = x
        self.z.value = z

    def start(self):
        self.started.value = True

    def stop(self):
        self.stopped.value = True

    def is_started(self):
        return self.started.value

    def is_stopped(self):
        return self.stopped.value

    def loc(self):
        state = ""
        if self.state.value is not None:
            state = ";" + str(self.state.value, encoding='utf-8').strip()
        return str(self.x.value) + ";" + str(self.z.value) + state

    def reset(self):
        self.started.value = False
        self.stopped.value = False
        self.state.value = b''
        self.x.value = 0
        self.z.value = 0
