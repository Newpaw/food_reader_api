from fastapi import HTTPException

class UniqueConstraintFailedException(HTTPException):
    def __init__(self, detail: str = "Unique constraint failed"):
        super().__init__(status_code=400, detail=detail)