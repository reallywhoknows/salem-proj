FROM python:3.9

WORKDIR /
COPY requirements.txt .
COPY . .

RUN python3 -m pip install -r requirements.txt
CMD ["python", "./main.py"]