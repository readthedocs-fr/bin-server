FROM python:3.14-alpine
LABEL org.opencontainers.image.source=https://github.com/readthedocs-fr/bin-server

WORKDIR /usr/local/lib/rtd-bin
COPY . .

RUN pip install -e .

ENTRYPOINT [ "python", "-m", "bin" ]
