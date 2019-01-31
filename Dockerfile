FROM python:3.7

WORKDIR /home

ADD . .

RUN pip install -r ./requirements.txt

CMD [ "python", "-u", "./main.py" ]

