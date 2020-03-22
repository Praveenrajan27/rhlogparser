FROM python:3

MAINTAINER Praveen Rajan "praveenrajan27@gmail.com"


COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]