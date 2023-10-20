FROM python:3.11.4


WORKDIR /app


COPY requirements.txt .


RUN python -m pip install -r requirements.txt


COPY . /app


CMD flask --app project run -h 0.0.0.0 -p $PORT
