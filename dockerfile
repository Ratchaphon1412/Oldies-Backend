FROM  python:3.12-rc-alpine 
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev\
    && apk add python3\
    && apk add --no-cache --upgrade bash
RUN mkdir /code
WORKDIR /code
COPY poetry.lock pyproject.toml /code/
RUN apk add poetry
RUN poetry config virtualenvs.create false && poetry config installer.max-workers 10
RUN poetry install --no-root

COPY . /code/







EXPOSE 8000
