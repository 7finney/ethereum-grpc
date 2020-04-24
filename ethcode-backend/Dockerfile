FROM python:3.7

WORKDIR /usr/src/app

COPY requirements.txt .

# RUN pip install pipenv

# COPY Pipfile* ./

# RUN pipenv lock --requirements > requirements.txt

RUN pip install grpcio

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 50053

CMD [ "python", "-u", "server.py" ]