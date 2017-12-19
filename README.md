# GoGoMedia 

tracks a users list of media they would like to consume, and what they have already consumed

## REQUIREMENTS
PostgreSQL server set up

## SETUP
1. `mv config_template.ini config.ini`
and change the default settings to the correct settings for you setup

2. `mv alembic_template.ini alembic.ini`
and change the `sqlalchemy.url` to the correct values

3. once alembic is configured run `alembic upgrade head` to setup database
