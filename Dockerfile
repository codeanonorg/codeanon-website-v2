FROM node:alpine as node

WORKDIR /code/
COPY ./yarn.lock /code
COPY ./package.json /code

RUN yarn --frozen-lockfile

ARG ENV=production
FROM python:3.8-alpine as runner
LABEL maintainer="solarliner@gmail.com"

# Set environment varibles
ENV PYTHONUNBUFFERED 1
ARG ENV
ARG DATABASE_URL
ENV DJANGO_ENV ${ENV}
ENV DATABASE_URL ${DATABASE_URL}
ENV DJANGO_SETTINGS_MODULE codeanon.settings.${ENV}

# Set the working directory to /code/
WORKDIR /code/

# System dependencies
RUN apk --no-cache add python3 \
                       build-base \
                       python3-dev \
                       # wget dependency
                       openssl \
                       openssl-dev \
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

RUN pip install --upgrade pip virtualenv poetry
# Install any needed packages specified in requirements.txt
COPY ./pyproject.toml /code/
COPY ./poetry.lock /code/
RUN virtualenv /code/.venv && . /code/.venv/bin/activate && poetry install

# Copy the current directory contents into the container at /code/
COPY . /code/
COPY --from=node /code/node_modules /code/node_modules


RUN export SECRET_KEY=ABCdefGHIjklMNOpqrSTUvwxYZ1234567890 \
	&& . /code/.venv/bin/activate \
	&& python manage.py migrate \
	&& python manage.py collectstatic --no-input \
	&& unset SECRET_KEY

RUN adduser -S wagtail
RUN chown -R wagtail /code
USER wagtail

EXPOSE 80
CMD exec gunicorn codeanon.wsgi:application --bind 0.0.0.0:80 --workers 3
