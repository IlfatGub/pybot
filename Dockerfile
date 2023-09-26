FROM python:3.11.3

WORKDIR /usr/src/app

COPY ../* ./

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./_bot.py" ] 
# CMD [ "python" ] 