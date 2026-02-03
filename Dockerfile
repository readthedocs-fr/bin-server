FROM python:3.14-alpine
LABEL org.opencontainers.image.source=https://github.com/readthedocs-fr/bin

WORKDIR /usr/local/lib/rtd-bin
COPY . .
# todo remove requirement on drlazor's pypi
RUN pip install -q -i https://drlazor.be/pypi metrics && \ 
    pip install -e .

ENTRYPOINT [ "python", "-m", "bin" ]
