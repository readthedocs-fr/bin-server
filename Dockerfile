FROM python:3.8-slim-buster

ENTRYPOINT python -m bin
WORKDIR /usr/local/lib/rtd-bin

# Install prerequisities
RUN pip install -i https://pypi.drlazor.be metrics
COPY . /usr/local/lib/rtd-bin
RUN python setup.py install