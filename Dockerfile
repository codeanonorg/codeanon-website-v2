FROM node:alpine as node

WORKDIR /code/
COPY ./yarn.lock /code
COPY ./package.json /code

RUN yarn --frozen-lockfile

FROM python:3.8-alpine as builder
WORKDIR /code/

RUN apk update && apk --no-cache add python3 \
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
                       fribidi-dev \
                       # Postgres dependencies
                       postgresql-dev
# Install any needed packages specified in requirements.txt
COPY . /code/
RUN pip install poetry
RUN poetry export -f requirements.txt > requirements.txt
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

ARG ENV=production
FROM python:3.8-alpine as runner
LABEL maintainer="solarliner@gmail.com"

# Set environment varibles
ENV PYTHONUNBUFFERED 1
ARG ENV=dev
ARG DATABASE_URL=sqlite:///db.sqlite3
ENV DJANGO_ENV ${ENV}
ENV DJANGO_SETTINGS_MODULE codeanon.settings.${ENV}

COPY . /code/
COPY --from=node /code/node_modules /code/node_modules
COPY --from=builder /wheels /wheels
COPY --from=builder /code/requirements.txt /code
RUN pip install --no-cache /wheels/*

RUN adduser -S wagtail && chown -R wagtail /code
USER wagtail

EXPOSE 8000
CMD ["./docker_entry.sh", "gunicorn", "codeanon.server.wsgi:application", "--workers=3", "--bind=0.0.0.0:8000"]
