FROM python:3.10.5

WORKDIR /usr/src/app

COPY ./ ./
RUN pip install --upgrade pip setuptools wheel
RUN pip install .[dev]

WORKDIR mysite

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=flask_app:app
ENV FLASK_ENV=development
ENV FLASK_RUN_PORT=5000
ENV FLASK_DEBUG=1

CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]