# pull official base image
FROM python:3.11.4-slim-buster


# set work directory
WORKDIR /usr/src/app



# install dependencies
RUN pip install --upgrade pip
RUN apt-get update && \
    apt-get install -y build-essential
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .
