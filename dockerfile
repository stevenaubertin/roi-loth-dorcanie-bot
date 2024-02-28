FROM python:3.10-bullseye
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
COPY ./src/ .
CMD ["python3", "main.py"]