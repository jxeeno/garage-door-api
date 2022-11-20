import threading
from flask import Flask, request
import subprocess

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
        f"--rolling={rolling}",
        f"--fixed={fixed}",
        f"--pin={pin}"
    ]

    try:
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

    sem.release()
    return response