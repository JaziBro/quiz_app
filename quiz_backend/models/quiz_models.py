from typing import Optional
from sqlmodel import SQLModel, Field

# QUIZ MODELS
class Category(SQLModel, table=True):
    catgory_id: Optional[int] = Field(None, primary_key=True)
    category_name: str
    category_description: str
 
class Quiz(SQLModel, table=True):
    question_id: Optional[int] = Field(None, primary_key=True)
    question: str

class Choices(SQLModel, table=True):
    choice_id: Optional[int] = Field(None, primary_key=True)
    quiz_id: int = Field(int, foreign_key="quiz.question_id")
    choice: str
    is_correct: bool = False

# USER MODELS
class LoginModel(SQLModel):
    user_email: str
    user_password: str  

class SignupModel(LoginModel):
    user_name: str

# Define User model
class User(SignupModel, table=True):
    user_id: Optional[int] = Field(None, primary_key=True)
    

# Define Token model
class Token(SQLModel, table=True):
    token_id: Optional[int] = Field(None, primary_key=True)
    user_id: int = Field(int, foreign_key="user.user_id")
    refresh_token: str  # Refresh token for authentication

# ADMIN MODELS
class Admin(SQLModel, table=True):
    admin_id: Optional[int] = Field(default=None, primary_key=True)
    admin_name: str
    admin_email: str
    admin_password: str
