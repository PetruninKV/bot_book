FROM python:3.10-bullseye

WORKDIR /app

COPY . /app

RUN python3.10 -m pip install -r requirements.txt

CMD ["python3.10", "bot.py"]