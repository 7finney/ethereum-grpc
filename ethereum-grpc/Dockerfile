FROM python:3.7

WORKDIR /usr/src/app

COPY ./server/ .

RUN pip install --no-cache-dir -r requirements.txt --user


EXPOSE 50054

CMD [ "python", "-u", "server.py" ]