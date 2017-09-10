FROM python:3
MAINTAINER tyanboot <tyanboot@outlook.com>

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt-get update && apt install -y tesseract-ocr-eng tesseract-ocr && apt-get clean && apt-get autoclean

COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt --no-cache-dir --disable-pip-version-check \
    && pip install uwsgi && rm -rf /tmp/requirements.txt

CMD ["uwsgi", "--ini", "/app/uwsgi.ini"]