# GoGoMedia 

tracks a users list of media they would like to consume, and what they have already consumed

## REQUIREMENTS
PostgreSQL server
Python 3.6

## SETUP
1. `pip install -r requirements.txt` to install the python dependencies

2. Startup a PostgreSQL server

3. create a production database

4. create a test database (optional)

5. `mv alembic_template.ini alembic.ini`
change the `sqlalchemy.url` to the correct value
change the `sqlalchemy.test.url` to the correct value (optional)

6. run `alembic upgrade head` to setup the production database

## Running
run `python app.py` to start the server

## Testing
run `python tests.py` to run the tests

