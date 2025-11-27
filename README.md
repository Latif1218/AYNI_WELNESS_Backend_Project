# AYNI WELNESS Backend Project

## AYNI WELNESS API
This is a REST API for a AYNI_WELNESS service built for fun and learning with FastAPI, SQLAlchemy and PostgreSQL.


## ROUTES TO IMPLEMENT 
| METHOD | ROUTE | FUNCTIONALITY |ACCESS|
| ------- | ----- | ------------- | ------------- |
| *POST* | ```/Registers``` | _Register new user_| _All users_|
| *POST* | ```/login``` | _Login user_|_All users_|
| *POST* | ```/forgot_password``` | _forgot password_|_All users_|
| *POST* | ```/verify-otp``` | _verify otp_|_All users_|
| *POST* | ```/reset-password/{email}/``` | _reset password_|_All users_|
| *NEXT DAY* | ```next day``` | _next day_| _next day_|
<!-- | *PUT* | ```/orders/order/status/{order_id}/``` | _Update order status_|_Superuser_|
| *PATCH* | ```/order/update/{order_id}``` | _Update_order_status_| _All users_|
| *DELETE* | ```/orders/order/delete/{order_id}/``` | _Delete/Remove an order_ |_All users_|
| *GET* | ```/orders/user/orders/``` | _Get user's orders_|_All users_|
| *GET* | ```/orders/orders/``` | _List all orders made_|_Superuser_|
| *GET* | ```/orders/orders/{order_id}/``` | _Retrieve an order_|_Superuser_|
| *GET* | ```/orders/user/order/{order_id}/``` | _Get user's specific order_|
| *GET* | ```/docs/``` | _View API documentation_|_All users_| -->

## How to run the Project
- Install Postgreql
- Install Python
- Git clone the project with ``` https://github.com/Latif1218/AYNI_WELNESS_Backend_Project.git```
- Create your virtualenv with `aynenv` and activate it.
- Install the requirements with ``` pip install -r requirements.txt ```
- Set Up your PostgreSQL database and set its URI in your ```database.py```
```
engine=create_engine('postgresql://postgres:<username>:<password>@localhost/<db_name>',
    echo=True
)
```
- Simple run fastapi dev main.py
- Create your database by running ``` python init_db.py ```
- Finally run the API
``` uvicorn main:app ``



### haw to learn
- create environment
- create requirements.txt
- create main.py 
- create database.py
- create models/user_model.py
- create schemas/user_schema.py
- create routes/user.py
- create routes/auth.py

###  architecter

fastapi_auth_app/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   │
│   ├── models/
│   │   └── user_model.py
│   │
│   ├── schemas/
│   │   └── user_schema.py
│   │
│   ├── routes/
│   │   ├── auth.py
│   │   └── user.py
│   │
│   ├── services/
│   │   └── auth_service.py
│   │
│   └── utils/
│       ├── hashing.py
│       ├── jwt_handler.py
│       ├── hashing.py
│       ├── email_sender.py
│       └── otp_sender.py
├── aynenv
└── requirements.txt
