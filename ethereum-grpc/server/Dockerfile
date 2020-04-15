FROM python:3.7

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install grpcio-status

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 50054

CMD [ "python", "-u", "server.py" ]