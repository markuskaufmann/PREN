import logging
import time
from threading import Thread
from ch.hslu.pren36.pi3b.statemachine.StateMachine import StateMachine

logging.basicConfig(level=logging.INFO)
# logging.getLogger('transitions').setLevel(logging.INFO)


class ControllerStateMachine:
    idle = True
    t_fsm = None
    t_fz = None
    fsm = None

    def __init__(self):
        self.fsm = StateMachine()
        self.t_fsm = Thread(target=self.start_idle)
        self.t_fsm.start()

    def start_idle(self):
        while self.idle:
            time.sleep(0.02)
        self.fsm.init()
        # self.fsm.ready_to_drive()
        # self.fsm.cube_found()
        # self.fsm.go_down_woc()
        # self.fsm.reached_surface()
        # self.fsm.get_cube()
        # self.fsm.has_cube()
        # self.fsm.is_up_wc()
        # self.fsm.target_area_found()
        # self.fsm.go_down_wc()
        # self.fsm.reached_surface()
        # self.fsm.set_cube()
        # self.fsm.cube_is_set()
        # self.fsm.is_up_woc()
        # self.fsm.touched_end()
        # self.fsm.shut_down()

    def run(self):
        self.idle = False


if __name__ == '__main__':
    cst = ControllerStateMachine()
    cst.run()
