# System requirements

The project uses
- Python 3.8.x
- venv as a virtual environment manager 
- postgresql database

# Project setup

1. Install python 3.8.13
   1. Install pyenv by running
      ```
      brew install pyenv
      ```
   2.  Then use
      ```
      pyenv install 3.8.13
      ```
 
2. Create virtual environment 
    ```
   python3.8 -m venv ~/.venv/pp_airport-env
   ```
3. Then activate it
   ```
   ~/.venv/pp_airport-env/bin/activate
   ```
   In order to check which pythin version you are using 
   ```
   python --version
   ```
4. Install necessary modules by running 
   ```
   pip install requrements.txt
   ```
   
5. Initialize the alembic to our working project directory
   ```
   alembic init alembic
   ```
6. Change the sqlalchemy.url in your alembic.ini file
   ```
   sqlalchemy.url = mysql+mysqldb://root:root@localhost:3306/database_name
   ```
7.  In env.py in our alembic folder write :
    ```
    from model import Base
    target_metadata = [Base.metadata]   
    ```
8. To generate all tables in your database:
   ```
   alembic upgrade head
   ```
9. To populate the database with data run the addata.py file which is in 
database folder
 # Running project
   Run project using gunicorn
   ```
   PORT=5000 gunicorn -w 4 app:app
   ```
 # OpenApi Documentation
   The api documentation is in "api" folder - swagger.yaml







