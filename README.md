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
pip install -r mysite/requirements.txt
pip install coloredlogs  # this breaks Python Anywhere at the moment, but is needed for local dev setup to run
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

### Contributions

To maintain consistency across the site, the following requirements will be checked before any contributions are accepted:
1) If a section is related to a skill, particular class, or other type of Unlock, check immediately for that unlock criteria. If unmet, return a "Come back after Unlocking XYZ" statement.
2) Load data which may be used in multiple files safely into the models/Account singleton. Use default values for unavailable data: Lava typically uses 0 or -1, sometimes other values. You'll sadly need to find someone with an updated JSON to find out what Lava chose in each particular instance.
3) At minimum, test changes against every JSON within tests/testing-data, plus some current-patch accounts if the JSON data is behind. The goal going forward is to have a JSON from the last 3 or so patches.
4) Maintain an aura of politeness in phrasing. This tool is intended to help without shaming the user for not having completed something yet, or not having encylcopedic knowledge of game mechanics.
5) This tool should not promote the use of autoclickers, cheats, scripts, or any other type of exploit that wouldn't be allowed to be discussed in the main IdleOn Discord.
6) Scoli has the final say, end of story.
