from transitions import Machine
from transitions.extensions.states import *
import logging
from threading import Thread
import time

logging.basicConfig(level=logging.INFO)
# logging.getLogger('transitions').setLevel(logging.INFO)

class StateMachine(object):
    targetIsFound = 0
    states = [
        State(name='on'),
        State(name='off'),
        State(name='init'),
        State(name='drive', on_enter=['driveForward']),
        State(name='driveWhileWaiting', on_enter=['findTarget']),
        State(name='stop', on_enter=['stopDriving']),
        State(name='drivingDown'),
        State(name='isDown'),
        State(name='gettingCube'),
        State(name='drivingUp'),
        State(name='settingCube'),
    ]

    def __init__(self):
        self.machine = Machine(model=self, states=StateMachine.states, initial='off')
        self.machine.add_transition(trigger='init', source='off', dest='on')
        self.machine.add_transition(trigger='readyToDrive', source='on', dest='drive')
        self.machine.add_transition(trigger='cubeFound', source='drive', dest='stop')
        self.machine.add_transition(trigger='goDown', source='stop', dest='drivingDown')
        self.machine.add_transition(trigger='reachedBottom', source='drivingDown', dest='isDown')
        self.machine.add_transition(trigger='getCube', source='isDown', dest='gettingCube')
        self.machine.add_transition(trigger='hasCube', source='gettingCube', dest='drivingUp')
        self.machine.add_transition(trigger='isUp', source='drivingUp', dest='driveWhileWaiting')
        self.machine.add_transition(trigger='targetFound', source='driveWhileWaiting', dest='stop')
        self.machine.add_transition(trigger='goDown', source='stop', dest='drivingDown')  # kommt 2x vor
        self.machine.add_transition(trigger='reachedBottom', source='drivingDown', dest='isDown')
        self.machine.add_transition(trigger='setCube', source='isDown', dest='settingCube')
        self.machine.add_transition(trigger='cubeIsSet', source='settingCube', dest='drivingUp')
        self.machine.add_transition(trigger='isUp', source='drivingUp', dest='drive')  # kommt 2x vor


    def stopDriving(self):
        pass
        #ToDo hier kommt die Motoransteuerung

    def driveForward(self):
        pass
        #ToDo hier kommt die Motoransteuerung

    def findTarget(self):
        while 1 != self.targetIsFound:
            # targetFound = self.ser.readline().rstrip()
            # print("read " + str(data.decode('utf-8')))
            time.sleep(0.1)
            print("Target not found")
        pass

    def control(self):
        while True:
            pass