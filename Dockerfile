FROM python:3.11.3

WORKDIR /usr/src/app

COPY ./python/requirements.txt requirements.txt
COPY /opt/py/python/ ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade pip

CMD [ "python", "./_bot.py" ] 
# CMD [ "python" ] 