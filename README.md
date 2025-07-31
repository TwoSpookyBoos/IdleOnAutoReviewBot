# IEAutoReviewBot

http://ieautoreview-scoli.pythonanywhere.com/

## Environment Setup

_This tool is created and tested using Python 3.10.5._
<hr/>

### Using github codespaces
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/TwoSpookyBoos/IdleOnAutoReviewBot)

Click the button above, wait for the environment to be created

### The manual way
Create and enable the virtual environment, and install the required packages.  
>Note that `coloredlogs` is commented in `mysite/requirements.txt`, as it doesn't work with the PythonAnywhere site. It's still needed for dev work though, so make sure it gets installed too, by uncommenting it. 

_Preferably create the virtual environment somewhere under the project root. 
`make test` command doesn't account for virtual environments located outside project scope_

#### Unix/MacOS:
``` bash
venv_dir="<venv/dir/name/here>"
python -m venv "$venv_dir"
source "$venv_dir"/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r mysite/requirements/dev.txt
```
#### Windows:
``` powershell
$venv_dir = "<venv/dir/name/here>"
python -m venv "$venv_dir"
"$venv_dir"/Scripts/Activate.ps1
pip install --upgrade pip setuptools wheel
pip install -r mysite/requirements/dev.txt
```
<hr/>

## Run

### Using github codespaces
Hit `Ctrl+Maj+D` or navigate to the debug tab, and run the included config.
A popup will give you a link to the now hosted app

### The manual way

To run the app, run:
#### Unix/MacOS:
``` bash
cd mysite
export PYTHONUNBUFFERED=1
export FLASK_APP=flask_app:app
export FLASK_ENV=development
export FLASK_RUN_PORT=5000
python -m flask run 
```
#### Windows:
``` powershell
cd mysite
$env:PYTHONUNBUFFERED = 1
$env:FLASK_APP = "flask_app:app"
$env:FLASK_ENV = "development"
$env:FLASK_RUN_PORT = 5000
python -m flask run 
```
#### Docker
Build and run the container, which mounts the local code.
Flask will auto-update files that are changed, so you shouldn't need to rebuild unless requirements change.
``` bash
docker build . -t idleon-auto-review-bot:latest
docker run --rm -d --name iarb -p 5000:5000 -v mysite:/usr/src/app idleon-auto-review-bot:1.0.3
```
To tail the webserver logs use
``` bash
docker logs -f iarb
```
#### PyCharm
Make sure that `mysite` is marked as `Sources Root`

Run one of the two saved run configurations.
<hr/>

## Test

To run tests, run:
``` bash
cd mysite
pytest -p no:warnings
```
or, using make:
``` bash
cd mysite
make test
```

## Image Maintenance Tools

`/utils/image_tools/` contains various scripts to help with maintenance of asset images.

- `check_duplicate_scss_variables.py`: scans files for scss variables with the same name and image reference
- `check_file_references.py`: scans files for image references and checks if any are missing

These can be executed by directly executing the file with Python.
