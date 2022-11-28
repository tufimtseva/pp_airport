# System requirements

According to my variant the project uses
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







# pp_airport

Написати сервіс для підтримки процесу реєстрації пасажирів та багажу в аеропорті. Є 4 типи користувачів : пасажир 
 (role_passenger), checkin менеджер (role_security_mgr), security менеджер (role_security_mgr), та менеджер рейсу 
 (role_flight_mgr). User має можливість купування білету на рейс(Flight) шляхом створення сутності Booking а також оновлення 
 даних у Booking. Checkin менеджер проводить реєстрацію пасажира та Baggage(шляхом створення сутності Baggage) на рейс, security менеджер перевіряє 
 пасажірів на пронесення на борт заборонених речей; менеджер рейсу відповідає за відкриття/закриття boarding gate,
 перевіряє, чи всі пасажири здійснили посадку та може оновлювати офіційний статус рейсу(посадка, в повітрі, висадка). Результатом роботи системи є звіт про наповненість рейсу пасажирами та деталі про кожного пасажира(User) та його Baggage. 

Ролі, які підтримує система для авторизації :
## Roles:
- role_checkin_mgr
- role_security_mgr
- role_flight_mgr
- role_user
- role_all

===============
## Сустність:
- операція над нею // роль користувача, який можк викнувати операцію

## User
- add // role_all
- login // role_user
- logout // role_user
- update // role_user
- getDetails // role_user, role_checkin_mgr, role_security_mgr, role_flight_mgr

## Baggage
- add // role_checkin_mgr
- getDetails // role_checkin_mgr, role_security_mgr

## Flight
- getAll // role_all
- getDetails // role_all
- getPublicStatus // role_all
- setPublicStatus // role_flight_mgr
- openGate // role_flight_mgr
- closeGate // role_flight_mgr
- getAllUsersForFlight // role_flight_mgr
- getAllBaggageForFlight // role_flight_mgr

## Booking
- add // role_user
- update // role_user
- getDetails // role_user, role_checkin_mgr, role_security_mgr, role_flight_mgr
- getAllBoardingChecks // role_checkin_mgr, role_security_mgr, role_flight_mgr
- delete // role_user

## Manager
- login // role_checkin_mgr, role_security_mgr, role_flight_mgr
- logout // role_checkin_mgr, role_security_mgr, role_flight_mgr
- getDetails // role_checkin_mgr, role_security_mgr, role_flight_mgr

## Boarding check
- add // role_checkin_mgr, role_security_mgr
- getDetails // role_checkin_mgr, role_security_mgr, role_flight_mgr


