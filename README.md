# GoGoMedia 

tracks a users list of media they would like to consume, and what they have already consumed

## REQUIREMENTS
PostgreSQL server

## SETUP
1. `mv alembic_template.ini alembic.ini`
and change the `sqlalchemy.url` to the correct values

2. once alembic is configured run `alembic upgrade head` to setup database
