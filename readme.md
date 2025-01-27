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
'''py
uvicorn main:app --reload
'''