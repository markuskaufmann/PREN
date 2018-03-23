
from ch.hslu.pren36.pi3b.io.SysPseudo import SysPseudo
from flask import Flask, send_file

app = Flask(__name__)


class Communicator:
    sys = SysPseudo()
    callbacks = set()
    event_args_start = 1
    event_args_stop = 2
    state = None
    running = False

    def run(self):
        if not self.running:
            app.run(host="localhost", port=8080)
            self.running = True

    def send_signal_to_controller(self, args):
        event = CommunicatorEvent(args)
        self.notify_observers(event)

    def on_state_changed(self, controllerevent):
        self.state = controllerevent.args

    def add_callback(self, callback):
        self.callbacks.add(callback)

    def notify_observers(self, event):
        for callback in self.callbacks:
            callback(event)


class CommunicatorEvent:
    args = None

    def __init__(self, args):
        self.args = args


communicator = Communicator()


@app.route('/')
def index():
    return send_file('index.html')


@app.route('/favicon.ico')
def icon():
    return send_file('static/favicon.ico')


@app.route("/start")
def start():
    communicator.send_signal_to_controller(communicator.event_args_start)
    return communicator.sys.start()


@app.route("/stop")
def stop():
    communicator.send_signal_to_controller(communicator.event_args_stop)
    return communicator.sys.stop()


@app.route("/location")
def location():
    loc = communicator.sys.location()
    if communicator.state is not None:
        loc += ";" + communicator.state
    return loc
