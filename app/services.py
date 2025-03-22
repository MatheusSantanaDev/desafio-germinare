from .repositories import SoybeanMealRepository

class SoybeanMealService:
    def __init__(self, repository: SoybeanMealRepository):
        self.repository = repository

    def calculate_flat_prices(
            self, 
            basis: float, 
            contract_months: list,
            conversion_factor: float = 1.10231
        ):

        flat_prices = []

        for contract_month in contract_months:
            future_price = self.repository.get_price_by_contract_month(contract_month)

            if future_price is 0.0:
                raise ValueError(f"No future price found for contract month: {contract_month}")
            
            flat_price = (future_price + basis) * conversion_factor

            flat_prices.append({
                "contract_month": contract_month,
                "cbot_price": future_price,
                "basis": basis,
                "flat_price": flat_price
                }   
            )
        return flat_prices