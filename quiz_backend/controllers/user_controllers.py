from typing import Annotated
from fastapi import Depends
from quiz_backend.db.db_connector import get_session
from quiz_backend.models.quiz_models import SignupModel, User, LoginModel, Token
from sqlmodel import Session, select
from quiz_backend.controllers.auth_controllers import generateHashedPassword, verifyPassword, generateToken, decodeToken, generateAccesAndRefreshToken
from quiz_backend.utils.errors import AlreadyExistsException, InvalidInputException, NotFoundException
from quiz_backend.settings import AccessTokenExpiryTime, RefreshTokenExpiryTime
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select

authSchema = OAuth2PasswordBearer(tokenUrl="")

DBSession = Annotated[Session, Depends(get_session)]


def signUp(user_form: SignupModel, session: DBSession):
    # Check if user already exists
    users = session.exec(select(User))
    for user in users:
        is_email_exist = user.user_email == user_form.user_email
        is_password_exist = verifyPassword(
            user.user_password  , user_form.user_password)

        if is_email_exist and is_password_exist:
            raise AlreadyExistsException("email and password")
        elif is_email_exist:
            raise AlreadyExistsException("email")
        elif is_password_exist:
            raise AlreadyExistsException("password")

    # Hash the user's password
    hashed_password = generateHashedPassword(user_form.user_password)
    # Create a new user
    user = User(user_name=user_form.user_name,
                user_email=user_form.user_email, user_password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)

    # Generate access and refresh tokens for the new user
    data = {
        "user_name": user.user_name,
        "user_email": user.user_email,
        "access_expiry_time": AccessTokenExpiryTime,
        "refresh_expiry_time": RefreshTokenExpiryTime
    }
    print(data)
    token_data = generateAccesAndRefreshToken(data)

    # Save the refresh token in the database
    token = Token(user_id=user.user_id,
                  refresh_token=token_data["refresh_token"]["token"])
    session.add(token)
    session.commit()

    return token_data


def login(login_form: LoginModel , session: DBSession):
    users = session.exec(select(User))
    for user in users:
        user_email = user.user_email
        verify_password = verifyPassword(user.user_password, login_form.user_password)
        if user_email == login_form.user_email and verify_password:
            data = {
                "user_name": user.user_name,
                "user_email": user.user_email,
                "access_expiry_time": AccessTokenExpiryTime,
                "refresh_exiry_time": RefreshTokenExpiryTime
            }
            token_data = generateAccesAndRefreshToken(data)

            # update the refresh token in the database
            token = session.exec(select(Token).where(Token.user_id == user.user_id)).one()
            token.refresh_token = token_data["refresh_token"]["token"]
            session.add(token)
            session.commit()
            session.refresh(token)
            return token_data
    else:
        raise InvalidInputException("email or password")


def getUser(token: Annotated[str, Depends(authSchema)], session: Session):
    try:
        if token:
            data = decodeToken(token)
            user_email = data["user_email"]
            user = session.exec(select(User).where(User.user_email == user_email)).one()
            return user
    except:
        raise NotFoundException("token")

