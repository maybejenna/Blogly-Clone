FROM python:3.12.1-bookworm

WORKDIR /code

COPY code/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# This isn't strictly necessary for developing, but is going to be very useful when deploying.
# COPY ./code /code
