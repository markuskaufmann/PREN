from threading import Thread
import time


class Simulation:
    lbound_x = 20
    ubound_x = 300
    lbound_z = 0
    ubound_z = 60
    current_x = lbound_x
    current_z = lbound_z
    running = False

    def start(self):
        self.running = True
        thread = Thread(target=self.simulate)
        thread.start()

    def simulate(self):
        factor_z = round(((self.ubound_z - self.lbound_x) / (self.ubound_x - self.lbound_x)), 2)
        while self.running:
            self.current_x = self.lbound_x
            self.current_z = self.lbound_z
            for i in range(0, self.lbound_x):
                time.sleep(0.02)
                self.current_z += 1
            time.sleep(1)
            for i in range(0, (self.ubound_x - self.lbound_x)):
                time.sleep(0.02)
                self.current_x += 1
                self.current_z = round((self.current_z + factor_z), 2)
            time.sleep(0.02)
            self.current_z += (self.ubound_z - self.current_z)
            time.sleep(1)
            for i in range(0, self.ubound_z):
                time.sleep(0.02)
                self.current_z -= 1
            time.sleep(1)

    def interrupt(self):
        self.running = False

    def location(self):
        return str(self.current_x) + ";" + str(self.current_z)


class SysPseudo:
    simulation = Simulation()
    queue = None
    t_loc = None
    t_loc_running = True

    def start(self, queue):
        self.queue = queue
        self.t_loc = Thread(target=self.location, name="SysPseudo_Location")
        self.t_loc.start()
        self.simulation.start()

    def stop(self):
        self.t_loc_running = False
        self.simulation.interrupt()

    def location(self):
        while self.t_loc_running:
            self.queue.put(self.simulation.location())
