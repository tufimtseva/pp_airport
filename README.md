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
   2. On Windows...
   
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

5. Run project using gunicorn
   ```
   gunicorn -w 4 app:app
   ```
   







# pp_airport

Написати сервіс для підтримки процесу реєстрації пасажирів та багажу в аеропорті. Є 4 типи користувачів : пасажир 
 (role_passenger), checkin менеджер (role_security_mgr), security менеджер (role_security_mgr), та менеджер рейсу 
 (role_flight_mgr). User має можливість купування білету на рейс шляхом створення сутності Booking а також оновлення 
 даних у Booking. Checkin менеджер проводить реєстрацію пасажира та Baggage на рейс, security менеджер перевіряє 
 пасажірів на пронесення на борт заборонених речей; менеджер рейсу відповідає за відкриття/закриття boarding gate та 
 перевіряє, чи всі пасажири здійснили посадку. Результатом роботи системи є звіт про наповненість рейсу пасажирами та 
 деталі про кожного пасажира та його Baggage. 

Ролі, які підтримує система для авторизації :
## Roles:
- role_checkin_mgr
- role_security_mgr
- role_flight_mgr
- role_user
- role_all

===============
## Сустність:
- операція над нею//роль користувача, який можк викнувати операцію

## User
- add // role_user
- login// role_user
- logout// role_user
- updateDetails//role_user
- getDetails//role_user, role_checkin_mgr, role_security_mgr, role_flight_mgr
- getAllUsersForFlight // role_flight_mgr
- checkIn // role_checkin_mgr
- securityCheck // role_security_mgr
- cancel//role_checkin_mgr, role_security_mgr
## Baggage
- add // role_checkin_mgr
- getDetails // role_checkin_mgr, role_security_mgr
- checkIn // role_checkin_mgr
- cancel//role_checkin_mgr, role_security_mgr

## Flight
- getAll //role_all
- getDetails // role_all
- getPublicStatus // role_all
- openGate // role_flight_mgr
- closeGate // role_flight_mgr

## Booking
- add//role_user
- setBaggage//role_user
- getDetails//role_user, role_checkin_mgr, role_security_mgr, role_flight_mgr
- cancel//role_user

 ## Manager
 - login//role_checkin_mgr, role_security_mgr, role_flight_mgr
 - logout//role_checkin_mgr, role_security_mgr, role_flight_mgr
