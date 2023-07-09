FROM  python:3.12-rc-alpine
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
RUN apk update 
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev\
    && apk add python3
RUN apk add --no-cache --upgrade bash
RUN pip install mysqlclient
COPY requirements.txt /code/


RUN pip install -r requirements.txt
RUN rm requirements.txt
COPY . /code/
CMD ["sh","setup.sh"]

EXPOSE 8000
