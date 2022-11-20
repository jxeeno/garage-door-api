# garage-door-api

This repository wraps https://github.com/zellyn/openers in a JSON API so that it can be called remotely.

The included `openers` binary is compiled for ARMv7 and is compatable with RPi2 or RPI-Zero.

### Dev setup
```bash
# setup virtual env if not available yet
python3 -m venv .venv

# enable venv
source .venv/bin/activate

# install requirements
pip install -r requirements.txt

FLASK_APP=server FLASK_ENV=development flask run
```

### Prod setup
```bash
# setup virtual env if not available yet
python3 -m venv .venv

# enable venv
source .venv/bin/activate

# install requirements
pip install -r requirements.txt

waitress-serve --port 8888 server:app
```