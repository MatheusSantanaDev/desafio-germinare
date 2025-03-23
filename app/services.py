from .repositories import FlatPriceRepository
from .exceptions import InvalidBasis, ContractMonthNotFound, InternalServerError, InvalidInputError
from .schemas import FlatPriceResponse, FlatPriceResults
from typing import List, Dict, Any, Union

class FlatPriceService:
    def __init__(self, repository: FlatPriceRepository):
        self.repository = repository

    def validate_basis(self, basis: float) -> None:
        if not isinstance(basis, (float, int)):
            raise InvalidInputError()

        if not (-50 <= basis <= 50):
            raise InvalidBasis()


    def calculate_flat_prices(
            self, 
            basis: float, 
            contract_months: List[str],
            conversion_factor: float = 1.10231
        ) -> FlatPriceResults:
        try:
            self.validate_basis(basis)

            results: List[Union[FlatPriceResponse, Dict[str, Any]]] = []

            for contract_month in contract_months:
                try:
                    future_price = self.repository.get_price_by_contract_month(contract_month)

                    flat_price = (future_price + basis) * conversion_factor
                    results.append(FlatPriceResponse(
                        contract_month=contract_month,
                        cbot_price=future_price,
                        basis=basis,
                        flat_price=flat_price
                    ))
                except ContractMonthNotFound as e:
                    results.append({
                        "error": e.detail
                    })
                except Exception as e:
                    raise InternalServerError() from e
                
            return FlatPriceResults(results=results)
        
        except InvalidBasis as e:
            raise
        except InvalidInputError as e:
            raise
        except Exception as e:
            raise InternalServerError() from e