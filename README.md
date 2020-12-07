# Trip Calculator API

# Installation Guide

After pulling down the code for `trip_calculator_api`, the following commands must be run from the root project directory.

## Run the install script

The install script is an auxiliary shell script that first tries to remove the current environment if it exists, creates a new one using Python 3.7, activates it, upgrades pip, and then runs pip install against the `requirements.txt` file. Lastly, it deactivates the environment after installing the project dependencies.

```bash
./install.sh
```

## Starting the API

Starting the API is simply done by activating the Python environment and running the `app.py` file:

```bash
source .venv/bin/activate
python app.py
```

Please make sure these steps are done before running the iOS front-end.
