import time
from ch.hslu.pren36.pi3b.servomotor.Servomotor import Servomotor

if __name__ == '__main__':
    sm = Servomotor()
    try:
        sm.initialize()
        sm.reset()
        while True:
            sm.open()
            time.sleep(Servomotor.dc_sleep)
            sm.close()
            time.sleep(Servomotor.dc_sleep)
    except KeyboardInterrupt:
        sm.stop()
