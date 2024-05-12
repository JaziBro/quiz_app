# exception raised when user inputs wrong data, like email, username, etc.
class InvalidInputException(Exception):
    def __init__(self, args: object) -> None:
        self.invalidInput = args
      
    

# exception raised when user tries to access a resource that does not exist like password
class NotFoundException(Exception):
    def __init__(self, args: object) -> None:
        self.notFound = args
       
    

# exception raised when user tries to create a resource that already exists like username
class AlreadyExistsException(Exception):
    def __init__(self, args: object) -> None:
        self.alreadyExists = args
       
    





# class NotAuthorizedException(Exception):
#     ...
    
# class InvalidCredentialsException(Exception):
#     ...
    
# class InvalidTokenException(Exception):
#     ...
    
# class InvalidPasswordException(Exception):
#     ...
    
# class InvalidEmailException(Exception):
#     ...
    
# class InvalidUsernameException(Exception):