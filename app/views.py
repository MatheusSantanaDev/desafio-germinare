from fastapi import APIRouter, Depends
from .services import FlatPriceService
from .repositories import FlatPriceRepository
from utils.db import get_db
from .schemas import FlatPriceRequest

router = APIRouter()

@router.post("/api/flat_price")
def calculate_flat_price(request: FlatPriceRequest, db=Depends(get_db)):
    repository = FlatPriceRepository(db)
    service = FlatPriceService(repository)

    response = service.calculate_flat_prices(request.basis, request.contract_months)
    return response