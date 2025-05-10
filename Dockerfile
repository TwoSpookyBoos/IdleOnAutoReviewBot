FROM python:3.11

WORKDIR /usr/src/app

COPY mysite/requirements /tmp/requirements
RUN pip install --no-cache-dir -r /tmp/requirements/dev.txt

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=flask_app:app
ENV FLASK_ENV=development
ENV FLASK_RUN_PORT=5000
ENV FLASK_DEBUG=1

CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]
