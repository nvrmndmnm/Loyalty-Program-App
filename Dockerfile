### Build and install packages
FROM python:3.8 as build-python

# Install Python dependencies
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt


### Final image
FROM python:3.8-slim

RUN apt-get update \
  && apt-get install -y \
  shared-mime-info \
  mime-support \
  libpq5 \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

ARG STATIC_URL
ENV STATIC_URL ${STATIC_URL:-/static/}

RUN groupadd -r loyalty && useradd -r -g loyalty loyalty

COPY . /app
COPY --from=build-python /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/
COPY --from=build-python /usr/local/bin/ /usr/local/bin/

WORKDIR /app

RUN mkdir -p /app/media /app/static \
  && chown -R loyalty:loyalty /app/

RUN STATIC_URL=${STATIC_URL} python3 ./source/manage.py collectstatic --no-input

EXPOSE 8000
ENV PORT 8000
ENV PYTHONUNBUFFERED 1
ENV PROCESSES 4

USER loyalty
CMD ["uwsgi", "--ini", "/app/source/Loyalty_Program_App/wsgi/uwsgi.ini"]
