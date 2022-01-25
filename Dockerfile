FROM python:3.10
WORKDIR /code
COPY requirements.txt /code/
RUN  pip install --upgrade pip && pip install --no-cache -r requirements.txt
COPY ./source /code
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
