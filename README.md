# Base django app

Requires Python 3.9, Django 3+, Postgresql 14+ and Redis 5+.

## Install

To install all dependencies:

```bash
make install
```

To delete all dependencies:

```bash
make clean
```

## Run

This django app has been setup for multi-settings mode (app/settings), two dummy settings have been created:

 * api
 * web

There are inheriting everything from app/settings/base.py, you are free to delete or modify them.

Here is an example of commands you can run for the `api` settings:

```bash
make setting=api server
make setting=api migrate
make setting=api migrations
```

The server will be ready on http://localhost:8080.

## API

### Swagger

To see the API swagger, you must launch the server.

```bash
make install
make setting=api server
```

Then goes on this URL:

```bash
http://127.0.0.1:8080/api/swagger
```

You can check the validity of the swagger by installing `swagger-cli` through the command:
```bash
npm install -g swagger-cli
```
Then you can launch the command:
```bash
make setting=api swagger-check
```

### Test

You can test the API by launching this commad:

```bash
make setting=api app=api test_app
```

## Code linting

```bash
make lint
```

In order to enforce a certain code quality, [pylint-fail-under](https://pypi.org/project/pylint-fail-under/) is used, and is configured to fail if the score is below 9.0 (see Makefile).

Before each Pull Request, we expect developers to run this command and fix most of errors or warnings displayed.

After creating a new module, it has to be added into the Makefile command.

As part of the linting, be aware you have to use [typings](https://docs.python.org/3/library/typing.html) in all the code you're creating.

## Other commands

Create a superuser:

```bash
make settings=xxx superuser
```

## i18N

The translation files (po) are in locale/<lang>/LC_MESSAGES/django.po.

### To generate them:

```bash
make setting=web makemessages
```

The setup is at the bottom of the app/settings.py.

The way to use it is:

In python code:

```python
from django.utils.translation import ugettext as _

return JsonResponse({'message': _('NoFortune')}, status=404)
```

In template:

```html
{% load i18n %}
<p>{% trans 'YourFortune' %}</p>
```

### To compile the messages (so that Django can use them) run:

```bash
make setting=web compilemessages
```

Note for the ops: the compiled files won't be kept in git, so they have to be re-generated at every deployment.

### API Example:

```bash
➜  django-seed git:(master) ✗ curl http://localhost:8080/sample/
{"message": "Success"}

➜  django-seed git:(master) ✗ curl http://localhost:8080/sample/ -H 'Accept-Language: fr'
{"message": "Succès"}
```

### Web Example:

Url code:

```python
from django.conf.urls.i18n import i18n_patterns

# This will set a /<lang> at the base of all URLs
urlpatterns += i18n_patterns(
    path('fortune/', include('fortune_web.urls'))
)
```

You can now call:

 * http://localhost:8080/en-us/fortune/
 * http://localhost:8080/fr/fortune/

Note: You can also use `i18n_patterns` for your API, but by default `Accept-Language` is there, so do as you want.

## OPS

## Celery

There is a Celery project embedded in this django project and it can be found in the following files:

 * app/__init__.py (imports the Celery config file)
 * app/main_celery.py (Celery config)
 * tasks/tasks.py (list of tasks)

### Run the server

```bash
make setting=api celery
```

### Tasks

In order to use your task (decorated with `@shared_task`), launch the celery server and in another console you can do the following:

```bash
make setting=api shell
from tasks.tasks import test
test.delay({'test': 'abc', 'true': 'yes'})
```

## Environment variables

| Name                          | Type    | Default                                      | Description                                                                                      |
| ----------------------------- | ------- | -------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| DEBUG                         | Boolean | True                                         | Should be False in production                                                                    |
| POSTGRESQL_ADDON_DB           | String  | base                                         | Name of the psql database                                                                        |
| POSTGRESQL_ADDON_USER         | String  | base                                         | Name of the psql user                                                                            |
| POSTGRESQL_ADDON_PASSWORD     | String  | base                                         | Password of the psql user                                                                        |
| POSTGRESQL_ADDON_HOST         | String  | localhost                                    | Domain/Ip of the psql database                                                                   |
| POSTGRESQL_ADDON_PORT         | Integer | 5432                                         | Port of the psql database                                                                        |
| SENTRY_DSN                    | String  | X                                            | Sentry's DSN (will only be enabled if the DEBUG flag is FALSE)                                   |
| CELERY_QUEUE                  | String  | celery                                       | Name of the default celery queue                                                                 |
| REDIS_URL                     | String  | redis://localhost:6379/0                     | Redis URL used by Celery                                                                         |
