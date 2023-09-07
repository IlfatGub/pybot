FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.ini bot.ini
COPY bot.py bot.py

CMD [ "python", "./bot.py" ] 