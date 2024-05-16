class AppException(Exception):
    pass

class DatabaseException(AppException):
    pass

class ProcessingException(AppException):
    pass
