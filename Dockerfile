FROM python:3.8-slim-buster

ENTRYPOINT python -m bin
WORKDIR /tmp/install

# Install prerequisities
RUN pip install -i https://pypi.drlazor.be metrics
COPY . /tmp/install
RUN python setup.py install