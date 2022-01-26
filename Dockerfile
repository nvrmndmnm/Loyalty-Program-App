FROM python
WORKDIR /code
COPY requirements.txt /code/
RUN  pip install --upgrade pip && pip install --no-cache -r requirements.txt
RUN apt-get update \
  && apt-get install -y \
  shared-mime-info \
  mime-support \
  libpq5 \
  default-libmysqlclient-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
COPY ./source /code
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
