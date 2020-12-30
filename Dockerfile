FROM python:3.8-alpine

ENTRYPOINT python -m bin
WORKDIR /usr/local/lib/rtd-bin
LABEL org.opencontainers.image.source https://github.com/readthedocs-fr/bin

COPY . /usr/local/lib/rtd-bin
RUN pip install -q -i https://pypi.drlazor.be metrics && python setup.py -q install
