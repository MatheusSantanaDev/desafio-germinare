from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from .exceptions import ContractMonthNotFound, InvalidBasis, InternalServerError
from .views import router as fastapi_app
from utils.logging import logger

app = FastAPI()
app.include_router(fastapi_app)

@app.exception_handler(ContractMonthNotFound)
async def contract_month_not_found_handler(request: Request, exc: ContractMonthNotFound):
    logger.error(f"ContractMonthNotFound: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )

@app.exception_handler(InvalidBasis)
async def invalid_basis_handler(request: Request, exc: InvalidBasis):
    logger.error(f"InvalidBasis: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )

@app.exception_handler(InternalServerError)
async def internal_server_error_handler(request: Request, exc: InternalServerError):
    logger.error(f"InternalServerError: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )