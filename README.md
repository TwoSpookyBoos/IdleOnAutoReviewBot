# IEAutoReviewBot

http://ieautoreview-scoli.pythonanywhere.com/

## Environment Setup

_This tool is created and tested using Python 3.11._
<hr/>

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
pip install -r requirements.txt
```
#### Windows:
``` powershell
$venv_dir = "<venv/dir/name/here>"
python -m venv "$venv_dir"
"$venv_dir"/Scripts/Activate.ps1
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

```
<hr/>

### Run

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
or, if you're using PyCharm, run one of the two saved run configurations.
<hr/>

### Test

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
