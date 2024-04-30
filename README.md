# IEAutoReviewBot

http://ieautoreview-scoli.pythonanywhere.com/

## Environment Setup

_This tool is created and tested using Python 3.11._
<hr/>

Create and enable the virtual environment, and install the required packages:
``` bash
venv_dir="<venv/dir/name/here>"
python -m venv "$venv_dir"
source "$venv_dir"/bin/activate
pip install --upgrade pip setuptools wheel
pip istall -r requirements.txt
```
<hr/>

### Run

To run the app, run:
``` bash
cd mysite
export THONUNBUFFERED=1
export FLASK_APP=flask_app:app
export FLASK_ENV=development
export FLASK_RUN_PORT=5000
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
or
``` bash
cd mysite
make test
```

The provided configurations work on Linux/MacOS. Windows setup comming soon™ (maybe)
