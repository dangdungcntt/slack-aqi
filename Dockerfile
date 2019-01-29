FROM python:3.7

ADD aqi.py /
COPY requirements.txt /var/www/requirement.txt

RUN pip install -r /var/www/requirement.txt

CMD [ "python", "-u", "/aqi.py" ]

