# Define default value for port
port ?= 8080

all: install migrate lint server

server:
	DJANGO_SETTINGS_MODULE=app.settings.$(setting) && python manage.py runserver $(port)

clean:
	rm -rf env/

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	pre-commit install --hook-type commit-msg
	pre-commit autoupdate

migrate:
	DJANGO_SETTINGS_MODULE=app.settings.$(setting) && python manage.py migrate

migrations:
	DJANGO_SETTINGS_MODULE=app.settings.$(setting) && python manage.py makemigrations

superuser:
	DJANGO_SETTINGS_MODULE=app.settings.$(setting) && python manage.py createsuperuser

lint:
	sh pylint_score.sh

test:
	DJANGO_SETTINGS_MODULE=app.settings.${setting} && python manage.py test --pattern="*_test.py"

test_app:
	DJANGO_SETTINGS_MODULE=app.settings.${setting} && python manage.py test ${app} --pattern="*_test.py"

swagger-check:
	swagger-cli validate app/static/swagger/api.swagger.yml || echo 'You need to install swagger-cli first with npm'

makemessages:
	DJANGO_SETTINGS_MODULE=app.settings.$(setting) && python manage.py makemessages -l en --ignore env*
	DJANGO_SETTINGS_MODULE=app.settings.$(setting) && python manage.py makemessages -l fr --ignore env*

compilemessages:
	DJANGO_SETTINGS_MODULE=app.settings.$(setting) && python manage.py compilemessages -l en -l fr --ignore env*

celery:
	DJANGO_SETTINGS_MODULE=app.settings.$(setting) && celery -A app worker -E

greenkeeping:
	pur -r requirements.txt

shell:
	DJANGO_SETTINGS_MODULE=app.settings.$(setting) && python manage.py shell
