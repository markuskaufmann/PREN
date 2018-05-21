import sys
import time
from ch.hslu.pren36.pi3b.servomotor.Servomotor import Servomotor


def start():
    if len(sys.argv) == 0:
        print("Missing argument 'direction': [1 (open), 0 (close)]")
        return
    direction = int(sys.argv[1])
    if direction != 0 and direction != 1:
        print("Wrong value for argument 'direction': [1 (open), 0 (close)]")
        return
    sm = Servomotor()
    try:
        sm.initialize()
        if direction == 1:
            sm.open()
        else:
            sm.close()
    except KeyboardInterrupt:
        sm.stop()
    time.sleep(3)
    sm.stop()


if __name__ == '__main__':
    start()
    # sm = Servomotor()
#     # try:
#     #     sm.initialize()
#     #     sm.reset()
#     #     while True:
#     #         sm.open()
#     #         time.sleep(Servomotor.dc_sleep)
#     #         sm.close()
#     #         time.sleep(Servomotor.dc_sleep)
#     # except KeyboardInterrupt:
#     #     sm.stop()
