import threading
from flask import Flask, request
import subprocess
import blinds

sem = threading.Semaphore()

app = Flask(__name__)

@app.route('/api/garage')
def secplus():
    args = request.args
    fixed = args.get("fixed", default=0, type=int)
    pin = args.get("pin", default=0, type=int)
    rolling = args.get("rolling", default=0, type=int)

    response = {}

    cmd = [
        "./openers",
        "secplus",
        "transmitv2",
        "--repeats=12",
        f"--rolling={rolling}",
        f"--fixed={fixed}",
        f"--pin={pin}"
    ]

    acquired = False

    try:
        sem.acquire()
        acquired = True

        p = subprocess.run(cmd, capture_output=True, text=True)

        response = {
            "result": p.stdout,
            "error": p.stderr,
            "fixed": fixed,
            "pin": pin,
            "rolling": rolling,
            "cmd": cmd
        }
    except subprocess.CalledProcessError as e:
        response = {
            "error": e.output,
            "fixed": fixed,
            "pin": pin,
            "rolling": rolling,
            "cmd": cmd
        }
    except Exception as e:
        response = {
            "error": str(e),
            "fixed": fixed,
            "pin": pin,
            "rolling": rolling,
            "cmd": cmd
        }

    if acquired:
        sem.release()
    
    return response


@app.route('/api/blinds')
def secplus():
    args = request.args
    state = args.get("state")

    response = {}
    acquired = False

    try:
        sem.acquire()
        acquired = True

        blinds.transmit([state])

        p = subprocess.run(cmd, capture_output=True, text=True)

        response = {
            "state": state,
        }
    except Exception as e:
        response = {
            "error": str(e),
            "state": state,
        }

    if acquired:
        sem.release()
    
    return response