import time
from threading import Thread

from pren36.endswitch.EndSwitch import EndSwitch


class Launcher:

    def __init__(self):
        self.end_switch_wait = True
        self.end_switch = EndSwitch()
        t_control = Thread(target=self.end_switch_control)
        t_control.start()

    def end_switch_control(self):
        while True:
            while self.end_switch_wait:
                time.sleep(0.05)
            while not self.end_switch_wait:
                signal = self.end_switch.signal()
                if signal == 1:
                    self.end_switch_wait = True
                    print("STOP")
                    break
                time.sleep(0.05)


if __name__ == '__main__':
    launcher = Launcher()
    launcher.end_switch_wait = False
