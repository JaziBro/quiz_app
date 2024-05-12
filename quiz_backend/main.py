from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from quiz_backend.db.db_connector import create_db_and_tables
from contextlib import asynccontextmanager
from quiz_backend.models.quiz_models import Quiz, Category, Choices, User, Token, Admin
from quiz_backend.utils.errors import NotFoundException, AlreadyExistsException, InvalidInputException
from typing import Annotated
from quiz_backend.controllers.user_controllers import signUp, login
from quiz_backend.settings import AccessTokenExpiryTime

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    print("Tables created...")
    yield

app = FastAPI(lifespan=lifespan)

# handling exceptions
@app.exception_handler(NotFoundException)
def not_found_exception_handler(request: Request, exception:NotFoundException):
    return JSONResponse(status_code=404, content=f"{exception.notFound} not found. Please Try Again")

@app.exception_handler(AlreadyExistsException)
def already_exists_exception_handler(request: Request, exception:AlreadyExistsException):
    return JSONResponse(status_code=404, content=f"This {exception.alreadyExists} already exists. Please try again")

@app.exception_handler(InvalidInputException)
def invalid_input_exception_handler(request: Request, exception:InvalidInputException):
    return JSONResponse(status_code=404, content=f"This {exception.invalidInput} not found. Please try again")

# handling routes
@app.get("/")
def home():
    return "Welcome Home"


@app.post("/api/userSignup")
def user_signup(tokensData: Annotated[dict, Depends(signUp)]):
    if not tokensData:
        raise NotFoundException("User")  # will give error: "user" not found
    return tokensData

@app.post("/api/userSignin")
def user_signin(tokensData: Annotated[dict, Depends(login)]):
    if tokensData:
        return tokensData
    raise NotFoundException("User") # will give error: "user" not found
    

@app.get("/api/user")
def user_login(user):
    return user


# @app.get("/api/getUser")
# def get_user(user: str):
#     if user == "Jazil":
#         raise NotFoundException("Username") # will give error: "Username" not found
#     return "User has been found"