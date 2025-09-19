FROM python:3.8-alpine

ENTRYPOINT python -m bin
WORKDIR /usr/local/lib/rtd-bin
LABEL org.opencontainers.image.source https://github.com/readthedocs-fr/bin

COPY . /usr/local/lib/rtd-bin
# todo remove requirement on drlazor's pypi
RUN pip install -q -i https://drlazor.be/pypi metrics && python setup.py -q install
