from flask import Flask, send_file

app = Flask(__name__)


class Communicator:
    comm_object = None
    state = None
    running = False

    def run(self, comm_object):
        if not communicator.running:
            communicator.comm_object = comm_object
            app.run(host="192.168.2.1", port=8080)
            communicator.running = True

    # def set_fsm(self, fsm):
    #     communicator.fsm = fsm
    #
    # def update_state(self, state):
    #     communicator.state = state
    #
    # def send_signal_to_fsm(self, args):
    #     event = CommunicatorEvent(args)
    #     communicator.notify_observers(event)
    #
    # def notify_observers(self, event):
    #     communicator.fsm.comm_callback(event)


communicator = Communicator()


@app.route('/')
def index():
    return send_file('index.html')


@app.route('/favicon.ico')
def icon():
    return send_file('static/favicon.ico')


@app.route("/start")
def start():
    # communicator.send_signal_to_fsm(CommunicatorEvent.event_args_start)
    communicator.comm_object.start()
    return "REQUEST_START SENT"


@app.route("/stop")
def stop():
    # communicator.send_signal_to_fsm(CommunicatorEvent.event_args_stop)
    communicator.comm_object.stop()
    return "REQUEST_STOP SENT"


@app.route("/location")
def location():
    # loc = Locator.loc_cube()
    # loc = communicator.comm_object.loc()
    # if communicator.comm_object.state.value is not None:
    #     loc += ";" + str(communicator.comm_object.state.value)
    return communicator.comm_object.loc()
