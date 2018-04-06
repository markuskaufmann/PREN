import logging
from threading import Thread
import time

from ch.hslu.pren36.pi3b.statemachine.StateMachine import StateMachine

logging.basicConfig(level=logging.INFO)
# logging.getLogger('transitions').setLevel(logging.INFO)


class ControllerStateMachine:
    idle = True
    running = False
    t_running = None
    t_fz = None
    fz = None

    def __init__(self):
        self.fz = StateMachine()
        self.t_running = Thread(target=self.start_idle)
        self.t_running.start()
        self.t_sm = Thread(target=self.fz.control)
        self.t_sm.start()

    def start_idle(self):
        self.fz.init()
        self.fz.readyToDrive()
        self.fz.cubeFound()
        self.fz.goDown()
        self.fz.reachedBottom()
        self.fz.getCube()
        self.fz.hasCube()
        self.fz.isUp()
        self.fz.targetFound()
        self.fz.goDown()
        self.fz.reachedBottom()
        self.fz.setCube()
        self.fz.cubeIsSet()
        self.fz.isUp()

    def run(self):
        self.running = True
        self.idle = False


if __name__ == '__main__':
    cst = ControllerStateMachine()
    cst.run()