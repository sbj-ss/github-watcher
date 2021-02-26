FROM python:3.8-slim

MAINTAINER Denis Podkovyrin <dennis.podkovyrin@skybonds.com>

# install requirements & caching
ADD requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

ADD . .

WORKDIR .
ENTRYPOINT GITHUBWATCHER_GITHUB__REPO='whatever' ./main.py 
