FROM python:3.8

WORKDIR /rentiha

COPY requirements.txt /rentiha/
RUN pip install -r requirements.txt

COPY . /rentiha/

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
