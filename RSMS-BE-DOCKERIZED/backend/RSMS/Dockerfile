
FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ADD . /app/

EXPOSE 8080
# RUN apk add lsof

COPY requirements.txt /app

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . /app

COPY docker-entrypoint.sh /app

RUN chmod +x /app/docker-entrypoint.sh

ENTRYPOINT ["/app/docker-entrypoint.sh"]


# CMD ["manage.py", "runserver", "0.0.0.0:8000"]