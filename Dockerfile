FROM python:3.10.11
WORKDIR /app

COPY setup.py setup.py

RUN pip install setuptools

RUN pip install .