ARG ENV=dev
FROM node:alpine as node

# RUN apk update && apk --no-cache add build-base python2 libsass

WORKDIR /code/
COPY ./yarn.lock /code
COPY ./package.json /code

RUN yarn --frozen-lockfile

FROM python:3.9-alpine as builder
ARG ENV
ENV DJANGO_ENV ${ENV}
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
	libsass-dev \
	lcms2-dev \
	openjpeg-dev \
	tiff-dev \
	tk-dev \
	tcl-dev \
	harfbuzz-dev \
	fribidi-dev \
	# cryptography dependencies
	cargo \
	# Postgres dependencies
	postgresql-dev
# Install any needed packages specified by Poetry
RUN pip install poetry
COPY ./pyproject.toml /code
COPY ./poetry.lock /code
RUN echo ${ENV}; [ "x${DJANGO_ENV}" = "xdev" ] \
	&& poetry export --dev -f requirements.txt > requirements.txt \
	|| poetry export -f requirements.txt  > requirements.txt
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

FROM python:3.9-alpine as runner
LABEL maintainer="solarliner@gmail.com"

# Set environment varibles
ARG ENV
ARG PORT=8000
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV ${ENV}
ENV DJANGO_SETTINGS_MODULE codeanon.settings.${ENV}
WORKDIR /code

RUN apk update && apk add --no-cache libpq jpeg zlib tiff tk tcl openjpeg libsass
COPY . /code/
COPY --from=node /code/node_modules /code/node_modules
COPY --from=builder /wheels /wheels
RUN pip install --no-cache --no-deps --no-index /wheels/*
RUN rm -rf /wheels

RUN SECRET_KEY="tempkey" sh -c "\
    python manage.py compilescss && \
    python manage.py collectstatic --noinput --clear --ignore='*.sass' --ignore='*.scss'"

RUN adduser -S wagtail && chown -R wagtail /code
USER wagtail

EXPOSE ${PORT}
CMD ./docker_entry.sh gunicorn codeanon.wsgi:application --workers=3 --bind=0.0.0.0:$PORT