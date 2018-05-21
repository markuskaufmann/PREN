import time

from flask import Flask, send_file

app = Flask(__name__)


class CommunicatorLocal:
    state = "RESPONE_PROCESS STARTED"
    loc_x = 650
    loc_z = 0
    running = False

    def run(self):
        if not communicator.running:
            app.run(host="localhost", port=8080)
            communicator.running = True


communicator = CommunicatorLocal()


@app.route('/')
def index():
    return send_file('index.html')


@app.route('/favicon.ico')
def icon():
    return send_file('static/favicon.ico')


@app.route("/start")
def start():
    return "REQUEST_START SENT"


@app.route("/stop")
def stop():
    return "REQUEST_STOP SENT"


@app.route("/location")
def location():
    loc = str(communicator.loc_x) + ";" + str(communicator.loc_z)
    if communicator.state is not None:
        loc += ";" + str(communicator.state)
    return loc


if __name__ == '__main__':
    communicator.run()
