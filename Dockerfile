FROM python:3.7
RUN mkdir /app
COPY requirements.txt /app
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY api_yamdb/ /app
WORKDIR /app
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000"]