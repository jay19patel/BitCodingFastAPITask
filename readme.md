##  Online Class Booking System : FastAPIs

### Key Points:
    - Fastapi,pytest,JWT,sqlite/postgresql
    - Create FastAPIs App
    - Create Models with Field
        1. User
        2. Classroom (Depends on User)
        3. Meeting (Depends on User and Classroom)
    -  Login Registartion
    - Teacher can Create Classroom
    - Student can schedul the meeting for this classrom

### Notes and Rerefence:
    - FastAPI app (https://fastapi.tiangolo.com/reference/fastapi/#fastapi.FastAPI--example)
    - Authentication using JWT (https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/?h=jwt)

### Run the code:
```cmd
uvicorn main:app --reload  #or
fastapi dev main.py   #or
docker-compose up --build -d
```

### Routes 

```cmd
<!-- Main Doc page  Swagger UI -->
http://127.0.0.1:8000/docs
```


```cmd
<!-- Registration -->
http://127.0.0.1:8000/auth/registration

{
  "first_name": "Jay",
  "last_name": "Patel",
  "email": "jay@gmail.com",
  "phone": "7069668308",
  "age": 24,
  "role": "Teacher",
  "password": "123456"
}
```


```cmd
<!-- Login -->
http://127.0.0.1:8000/auth/login

{
  "email": "jay@gmail.com",
  "password": "123456"
}
<!--  After loginc you get access token use this accesstoken in header for all protected api routes or add in authorize in swaager ui  -->
```


```cmd
<!--  Create class room by Teachers -->
http://127.0.0.1:8000/classroom/create_class

{
  "subject": "Mathematics",
  "start_time": "2025-01-28T07:53:04.953552",
  "end_time": "2025-01-28T12:53:04.953552"
}

```


```cmd
<!-- create meetng acrodig to classrom by Student -->
http://127.0.0.1:8000/classroom/book_meeting


{
  "class_id": 3,
  "start_time": "2025-01-28T07:53:04.955549",
  "end_time": "2025-01-28T08:53:04.955549"
}

```


```cmd
<!-- Classroom owner can see the all classess made by self -->
http://127.0.0.1:8000/classroom/my_classroom
```


```cmd
<!-- Student can see the all classrom  -->
http://127.0.0.1:8000/classroom/all_classroom


```
