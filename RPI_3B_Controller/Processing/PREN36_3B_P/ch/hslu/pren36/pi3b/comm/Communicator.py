from threading import Thread
from ch.hslu.pren36.pi3b.comm.CommunicatorEvent import CommunicatorEvent
from flask import Flask, send_file
from ch.hslu.pren36.pi3b.main.ControllerEvent import ControllerEvent

app = Flask(__name__)


class Communicator:
    proc_conn = None
    t_wait = None
    t_wait_running = True
    state = None
    loc_x = None
    loc_z = None
    running = False

    def run(self, conn):
        if not communicator.running:
            communicator.proc_conn = conn
            communicator.t_wait = Thread(target=communicator.wait, name="Communicator_Wait")
            communicator.t_wait.start()
            app.run(host="localhost", port=8080)
            communicator.running = True

    def send_signal_to_controller(self, args):
        event = CommunicatorEvent(args)
        communicator.notify_observers(event)

    def notify_observers(self, event):
        communicator.proc_conn.send(event)

    def wait(self):
        while communicator.t_wait_running:
            controllerevent = communicator.proc_conn.recv()
            args = controllerevent.args
            if args == ControllerEvent.event_args_main_start:
                communicator.state = "RESPONSE_PROCESS STARTED"
            elif args == ControllerEvent.event_args_improc_start:
                communicator.state = "Start ImageProcessing"
            elif args == ControllerEvent.event_args_main_stop:
                communicator.state = "RESPONSE_PROCESS STOPPED"
            elif args == ControllerEvent.event_args_improc_target_found:
                communicator.state = "Target found"
            elif args == ControllerEvent.event_args_loc_state:
                data = controllerevent.kwargs.split(";")
                communicator.loc_x = data[0]
                communicator.loc_z = data[1]


communicator = Communicator()


@app.route('/')
def index():
    return send_file('index.html')


@app.route('/favicon.ico')
def icon():
    return send_file('static/favicon.ico')


@app.route("/start")
def start():
    communicator.send_signal_to_controller(CommunicatorEvent.event_args_start)
    return "REQUEST_START SENT"


@app.route("/stop")
def stop():
    communicator.send_signal_to_controller(CommunicatorEvent.event_args_stop)
    return "REQUEST_STOP SENT"


@app.route("/location")
def location():
    loc = str(communicator.loc_x) + ";" + str(communicator.loc_z)
    if communicator.state is not None:
        loc += ";" + str(communicator.state)
    return loc
