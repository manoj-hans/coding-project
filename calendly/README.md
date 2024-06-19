# Calendly

## Poetry

This project uses poetry. It's a modern dependency management
tool.

To setup poetry use this command. Asumming you already have python installed

```bash
python3 -m pip install poetry
```

To run the project use this set of commands:

```bash
poetry install
poetry run python -m calendly
```

This will start the server on the configured host.

You can find swagger documentation at `/api/docs`.


## Docker

Alternatively, You can start the project with docker using this command.    
Please ignore the .env file in code repository. Its and intentional commit to reduce the steps to setup.

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . up -d --build
```

## Demo

You can run the demo/test using below step.

```bash
poetry shell
python demo.py
```


## Project structure

```bash
$ tree "calendly"
calendly
|-- README.md
|-- alembic.ini
|-- calendly
|   |-- __init__.py
|   |-- __main__.py
|   |-- conftest.py
|   |-- db
|   |   |-- __init__.py
|   |   |-- base.py
|   |   |-- dao
|   |   |   |-- __init__.py
|   |   |   |-- availability_schedule_dao.py
|   |   |   |-- calendar_dao.py
|   |   |   |-- event_dao.py
|   |   |   |-- timeslot_dao.py
|   |   |   `-- user_dao.py
|   |   |-- dependencies.py
|   |   |-- meta.py
|   |   |-- migrations
|   |   |   |-- __init__.py
|   |   |   |-- env.py
|   |   |   |-- script.py.mako
|   |   |   `-- versions
|   |   |       |-- 2024-06-19-13-30_a85ca0487db3.py
|   |   |       `-- __init__.py
|   |   |-- models
|   |   |   |-- __init__.py
|   |   |   |-- availabilityschedule.py
|   |   |   |-- calendar.py
|   |   |   |-- event.py
|   |   |   |-- timeslot.py
|   |   |   `-- user.py
|   |   `-- utils.py
|   |-- gunicorn_runner.py
|   |-- services
|   |   `-- __init__.py
|   |-- settings.py
|   |-- tests
|   |   |-- __init__.py
|   |   |-- test_calendly.py
|   |   |-- test_dummy.py
|   |   `-- test_echo.py
|   `-- web
|       |-- __init__.py
|       |-- api
|       |   |-- __init__.py
|       |   |-- availability_schedules
|       |   |   |-- __init__.py
|       |   |   |-- schemas.py
|       |   |   `-- views.py
|       |   |-- calendar
|       |   |   |-- __init__.py
|       |   |   |-- schemas.py
|       |   |   `-- views.py
|       |   |-- events
|       |   |   |-- __init__.py
|       |   |   |-- schemas.py
|       |   |   `-- views.py
|       |   |-- router.py
|       |   `-- user
|       |       |-- __init__.py
|       |       |-- schemas.py
|       |       `-- views.py
|       |-- application.py
|       `-- lifetime.py
|-- demo.py
|-- deploy
|   |-- Dockerfile
|   `-- docker-compose.yml
|-- poetry.lock
`-- pyproject.toml
```

## Configuration

This application can be configured with environment variables.

You can create `.env` file in the root directory and place all
environment variables here.

All environment variables should start with "CALENDLY_" prefix.

For example if you see in your "calendly/settings.py" a variable named like
`random_parameter`, you should provide the "CALENDLY_RANDOM_PARAMETER"
variable to configure the value. This behaviour can be changed by overriding `env_prefix` property
in `calendly.settings.Settings.Config`.

An example of .env file:
```bash
CALENDLY_RELOAD="True"
CALENDLY_PORT="8000"
CALENDLY_ENVIRONMENT="dev"
```

You can read more about BaseSettings class here: https://pydantic-docs.helpmanual.io/usage/settings/

## Migrations

If you want to migrate your database, you should run following commands:
```bash
# To run all migrations until the migration with revision_id.
alembic upgrade "<revision_id>"

# To perform all pending migrations.
alembic upgrade "head"
```

### Reverting migrations

If you want to revert migrations, you should run:
```bash
# revert all migrations up to: revision_id.
alembic downgrade <revision_id>

# Revert everything.
 alembic downgrade base
```

### Migration generation

To generate migrations you should run:
```bash
# For automatic change detection.
alembic revision --autogenerate

# For empty file generation.
alembic revision
```
