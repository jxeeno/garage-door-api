from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/api/garage')
def secplus():
    args = request.args
    fixed = args.get("fixed", default=0, type=int)
    pin = args.get("pin", default=0, type=int)
    rolling = args.get("rolling", default=0, type=int)

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

        return {
            "result": p.stdout,
            "error": p.stderr,
            "fixed": fixed,
            "pin": pin,
            "rolling": rolling,
            "cmd": cmd
        }
    except subprocess.CalledProcessError as e:
        return {
            "error": e.output,
            "fixed": fixed,
            "pin": pin,
            "rolling": rolling,
            "cmd": cmd
        }
    except Exception as e:
        return {
            "error": str(e),
            "fixed": fixed,
            "pin": pin,
            "rolling": rolling,
            "cmd": cmd
        }