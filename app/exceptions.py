from fastapi import HTTPException, status

class ContractMonthNotFound(HTTPException):
    def __init__(self, contract_month: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contract month {contract_month} not found",
        )

class InvalidBasis(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Basis must be a number between -50 and 50",
        )

class InternalServerError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error",
        )