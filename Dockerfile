FROM python:3

ARG VERSION
ENV VERSION ${VERSION:-master}

RUN pip install --upgrade pip

RUN python -m pip install git+https://github.com/eggplants/jason-json@${VERSION}

ENTRYPOINT ["jason.json"]
