from fastapi import APIRouter, HTTPException, Depends
from .services import SoybeanMealService
from .repositories import SoybeanMealRepository
from utils.db import get_db
from .schemas import FlatPriceRequest, FlatPriceResponse, FlatPriceResults

router = APIRouter()

@router.post("/api/flat_price", response_model=FlatPriceResults)
def calculate_flat_price(request: FlatPriceRequest, db=Depends(get_db)):
    
    repository = SoybeanMealRepository(db)
    service = SoybeanMealService(repository)

    try:
        results = service.calculate_flat_prices(request.basis, request.contract_months)
        return {"results": results}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))