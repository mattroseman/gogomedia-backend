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
                                                                                                             
5. `cp alembic_template.ini alembic.ini`                                                                     
change the `sqlalchemy.url` to the correct value                                                             

6. `cp config_template.ini config.ini`
change the `sqlalchemy.url` to the correct value
change the `sqlalchemy.test.url` to the correct value (optional)                                             
                                                                                                             
6. run `alembic upgrade head` to setup the production database                                               
                                                                                                             
## Running                                                                                                   
run `python app.py` to start the server                                                                      
                                                                                                             
## Testing                                                                                                   
run `python run_tests.py` to run the tests                                                                       
                                                                                                             
## Endpoints                                                                                                 

- **/register [POST]** adds a new user
	
    Request Body:
    
    ```
    {
    	'username': 'JohnSmith'
      'password': 'pass123'
    }
    ```

- **/login [POST]** logs in a user

  Request Body:

  ```
  {
    'username': 'JohnSmith'
    'password': 'pass123'
  }
  ```

  Response Body:

  ```
  {
    'success': True/False
    'message': 'description of failure of success
    'auth_token': 'an authentication token to be put in Header of requests that require login to access
  }
  ```

- **/logout [GET]** logs a user out
                                                                                                             
- **/user/\<username>/media [PUT]** add/update a media element for this user

	Request Body:
	
    ```
    {
    	'name': 'medianame',
      'consumed': true/false (optional)
    }
    ```
    
- **/user/\<username>/media [GET]** get all media elements for this user

- **/user/\<username>/media?consumed=yes [GET]** get all consumed media elements for this user

- **/user/\<username>/media?consumed=no [GET]** get all unconsumed media elements for this user

- **/user/\<username>/media [DELETE]** delete a media element for this user

	Request Body:
    
    ```
    {
    	'name': 'medianame'
    }
    ```
