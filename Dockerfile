# Use an official Python runtime as a parent image
ARG ENV=production
FROM python:3.8-alpine
LABEL maintainer="solarliner@gmail.com"

# TODO: Add secret management to Dockerfile

# Set environment varibles
ENV PYTHONUNBUFFERED 1
ARG ENV
ENV DJANGO_ENV ${ENV}
ENV DJANGO_SETTINGS_MODULE codeanon.settings.${ENV}
# Set the working directory to /code/
WORKDIR /code/

# System dependencies
RUN apk --no-cache add python3 \
                       build-base \
                       python3-dev \
                       # wget dependency
                       openssl \
                       # dev dependencies
                       git \
                       bash \
                       sudo \
                       py3-pip \
                       # Pillow dependencies
                       jpeg-dev \
                       zlib-dev \
                       freetype-dev \
                       lcms2-dev \
                       openjpeg-dev \
                       tiff-dev \
                       tk-dev \
                       tcl-dev \
                       harfbuzz-dev \
                       fribidi-dev

RUN pip install --upgrade pip pipenv
# Install any needed packages specified in requirements.txt
COPY ./Pipfile* /code/
RUN pipenv install --deploy --system

# Copy the current directory contents into the container at /code/
COPY . /code/


RUN python manage.py migrate && python manage.py collectstatic

RUN useradd wagtail
RUN chown -R wagtail /code
USER wagtail

EXPOSE 80
CMD exec gunicorn codeanon.wsgi:application --bind 0.0.0.0:80 --workers 3
