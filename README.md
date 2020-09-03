<img src="/codeanon/static/img/logo.svg" align="right" width="400" alt="CodeAnon logo" />

# CodeAnon Website

This is the website for the CodeAnon organization.

## Development

### Dependencies

- Python 3.8 with `poetry` installed
- Node v12 or v14 with `yarn` installed
- `docker` and `docker-compose` (optional; for testing the production environment only)

### Getting started

1. Setup the project with `poetry install`
2. Setup the front-end dependencies with `yarn install`
3. Open a shell with the python dependencies available with `poetry shell`:
    1. Create the SQLite database with `./manage.py migrate`
    2. Either:
        - Add a dump of the live site data with `./manage.py loaddata codeanon/fixtures/dump.json`
        - Create your local superuser account to manage the admin with `./manage.py createsuperuser`
        
        In either case the data will only be changed on your own computer and **not** in the live site.
    2. Run the development server with `./manage.py runserver`
    3. Open http://localhost:8080
    
### Modifying the CSS theme

The website uses Bulma as the CSS framework. It was chosen because it is most easily themeable.

The style files are written in Sass and are available in [/codeanon/static/css](/codeanon/static/css).

### More resources

- [Django documentation](https://docs.djangoproject.com/en/3.1/)
- [Wagtail documentation](https://docs.wagtail.io/en/stable/)
- [Bulma](https://bulma.io/)
- [Sass](https://sass-lang.com/)

## Deployment

### Deployment through Docker

Dockerfile-based development is supported through Wagtail's default Dockerfile. You need to fill in the required
 environment variables as environment when building the Docker image.
 
On top of the required environment variables below, there are two more variables required by the build script:

- `ADMIN_USER`: Username of the admin user
- `ADMIN_EMAIL`: Admin user email address
- `ADMIN_PASSWORD`: Admin user password
 
### Direct deployment

You can use the Dockerfile as a reference on how to deploy the project.

0. Install system dependencies: 
    - A recent C++ compiler as `libsass` needs GCC 4.7+ or any compatible compiler.
1. Install Python 3.8 and pipenv
2. Run `pipenv install --deploy` (add `--system` if the system's sole purpose is to run the web server)
3. Run `./manage.py migrate` from within the virtualenv if one was created
4. Run `./manage.py createsuperuser` to create the first user of the website - it will be given admin rights. Use a
 strong password!
5. Run `gunicorn codeanon.wsgi:application --bind 0.0.0.0:8000`

### Environment variables

#### Required environment variables

- `SECRET_KEY`: Sets the secret key used to encrypt cookies and generate CSRF tokens. Must be cryptographically
 generated, otherwise the security of the web server is compromised.
- `DATABASE_URL`: Database URL to use, in [Database URL](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING) format.
- `EMAIL_HOST`: Host name of the mail server
- `EMAIL_PORT`: Port to use when sending mails to the mail server
- `EMAIL_HOST_USER`: Mail server user
- `EMAIL_HOST_PASSWORD`: Mail server password

### Optional environment variables

- `EMAIL_USE_TLS`: (default false) - Use TLS when connecting to the mail server.
- `EMAIL_USE_SSL`: (default false) - Use SSL when connecting to the mail server.
- `EMAIL_TIMEOUT`: (default none)  - Set the connection timeout to the mail server.
- `EMAIL_SSL_KEYFILE`: (default none) - Set the file to the public keys to use.
- `EMAIL_SSL_CERTIFICATE`: (default none) - SSL certificate to use when connecting to the mail server.
