FROM python:3.7.13-slim-bullseye

# set work directory 
WORKDIR /app


# install dependencies

ENV FLASK_APP=run.py

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000

# copy files
COPY . .

CMD ["python" , "run.py"]