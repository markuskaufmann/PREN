import time
from threading import Thread

from pren36.fsm.StateMachine import StateMachine


class Launcher:
    def __init__(self):
        self.fsm = StateMachine()
        self.idle = True
        t_fsm = Thread(target=self.start_idle)
        t_fsm.start()

    def start_idle(self):
        while self.idle:
            time.sleep(0.02)
        self.fsm.init()

    def run(self):
        self.idle = False


if __name__ == '__main__':
    launcher = Launcher()
    launcher.run()
