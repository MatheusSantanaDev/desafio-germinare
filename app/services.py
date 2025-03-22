from .repositories import FlatPriceRepository
from .exceptions import InvalidBasis, InternalServerError
from fastapi import HTTPException
from typing import List, Dict, Any

class FlatPriceService:
    def __init__(self, repository: FlatPriceRepository):
        self.repository = repository

    def validate_basis(self, basis: float) -> None:
        if not (-50 <= basis <= 50):
            raise InvalidBasis()

    def calculate_flat_prices(
            self, 
            basis: float, 
            contract_months: List[str],
            conversion_factor: float = 1.10231
        ) -> Dict[str, Any]:
        """Calcula os flat prices para os meses de contrato fornecidos."""
        try:
            self.validate_basis(basis)

            results = []
            all_months_invalid = True

            for contract_month in contract_months:
                try:

                    future_price = self.repository.get_price_by_contract_month(contract_month)

                    flat_price = (future_price + basis) * conversion_factor
                    results.append({
                        "contract_month": contract_month,
                        "cbot_price": future_price,
                        "basis": basis,
                        "flat_price": flat_price
                    })
                    all_months_invalid = False
                except HTTPException as e:
                    results.append({
                        "error": e.detail
                    })
            
            if all_months_invalid and results:
                return {"error": results[0]["error"]}
            
            return {"results": results}
        except Exception as e:
            raise InternalServerError() from e