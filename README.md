# System requirements

According to my variant the project uses
- Python 3.8.x
- venv as a virtual environment manager 

# Project setup

1. Install python 3.8.13
   1. On Mac, install pyenv by running
      ```
      brew install pyenv
      ```
      Then use
      ```
      pyenv install 3.8.13
      ```
      On Mac M1 / 12.5.1 you may need to use
      ```
      SDKROOT=/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX12.3.sdk MACOSX_DEPLOYMENT_TARGET=12.3 pyenv install 3.8.13
      ```
   2. On Windows
   
      Open PowerShell as administrator and paste code below:
      ```PowerShell
      Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
      ```
      1. Add PYENV, PYENV_HOME and PYENV_ROOT to your Environment Variables:
         ```PowerShell
         [System.Environment]::SetEnvironmentVariable('PYENV',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")

         [System.Environment]::SetEnvironmentVariable('PYENV_ROOT',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")

         [System.Environment]::SetEnvironmentVariable('PYENV_HOME',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")
         ```
      2. Add the following paths to your USER PATH variable in order to access the pyenv command:
         ```PowerShell
         [System.Environment]::SetEnvironmentVariable('path', $env:USERPROFILE + "\.pyenv\pyenv-win\bin;" + $env:USERPROFILE + "\.pyenv\pyenv-win\shims;" + [System.Environment]::GetEnvironmentVariable('path', "User"),"User")
         ```
         Installation is done.
         Now install python 3.8.10 version using code below:
         ```PowerShell
         pyenv install 3.8.10
         ```
         Installation will take a lot of time, so don't worry. 
         Don't forget to add python.exe path to PATHs in System. 
         Copy python.exe file and create python3.8.10.exe file.

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
   pip install requirements.txt
   ```

5. Run project using gunicorn
   ```
   gunicorn -w 4 app:app
   ```

# Setup Database and Migrations to our project
1. Don`t forget to update requirements.txt opening project.
   ```
   pip install requirements.txt
   ```
2. After installing the requirements we need change the sqlalchemy.url in the alembic.ini file.
   ```
   sqlalchemy.url = postgresql://postgres:your_password@localhost:5432/Airport
   ```
3. Import db from models file to env.py
   ```
   from database.models import db
   ```
4. Change target_metadata = None to target_metadata = db.metadata
5. Now you are able to migrate db models using next command
   ```
   alembic upgrade head
   ```


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


