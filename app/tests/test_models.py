import pytest
from unittest.mock import Mock
from app.services import FlatPriceService
from app.repositories import FlatPriceRepository
from app.exceptions import InvalidBasis, ContractMonthNotFound, InternalServerError, InvalidInputError
from app.schemas import FlatPriceResults

# Mock do repositório para simular o comportamento do banco de dados
@pytest.fixture
def mock_repository():
    return Mock(spec=FlatPriceRepository)

# Fixture para o serviço, usando o mock do repositório
@pytest.fixture
def flat_price_service(mock_repository):
    return FlatPriceService(repository=mock_repository)

# Teste para cálculo correto do flat_price
def test_calculate_flat_prices_success(flat_price_service, mock_repository):
    mock_repository.get_price_by_contract_month.return_value = 100.0

    result = flat_price_service.calculate_flat_prices(
        basis=10.0,
        contract_months=["F2023"]
    )

    assert isinstance(result, FlatPriceResults)
    assert len(result.results) == 1
    assert result.results[0].contract_month == "F2023"
    assert result.results[0].cbot_price == 100.0
    assert result.results[0].basis == 10.0
    assert result.results[0].flat_price == pytest.approx(121.254, rel=1e-3)  # (100 + 10) * 1.10231

# Teste para validação do basis (valor fora do intervalo)
def test_validate_basis_invalid(flat_price_service):
    with pytest.raises(InvalidBasis):
        flat_price_service.validate_basis(60.0)

    with pytest.raises(InvalidBasis):
        flat_price_service.validate_basis(-60.0)

# Teste para contrato de mês não encontrado
def test_contract_month_not_found(flat_price_service, mock_repository):
    mock_repository.get_price_by_contract_month.side_effect = ContractMonthNotFound("F2023")

    result = flat_price_service.calculate_flat_prices(
        basis=10.0,
        contract_months=["F2023"]
    )

    assert isinstance(result, FlatPriceResults)
    assert len(result.results) == 1
    assert "error" in result.results[0]
    assert result.results[0]["error"] == "Contract month 'F2023' not found."

# Teste para erro interno no repositório
def test_internal_server_error(flat_price_service, mock_repository):
    mock_repository.get_price_by_contract_month.side_effect = Exception("Unexpected error")

    with pytest.raises(InternalServerError):
        flat_price_service.calculate_flat_prices(
            basis=10.0,
            contract_months=["F2023"]
        )

# Teste para cálculo com múltiplos contratos
def test_calculate_flat_prices_multiple_contracts(flat_price_service, mock_repository):
    mock_repository.get_price_by_contract_month.side_effect = [100.0, 105.0]

    result = flat_price_service.calculate_flat_prices(
        basis=10.0,
        contract_months=["F2023", "G2023"]
    )

    assert isinstance(result, FlatPriceResults)
    assert len(result.results) == 2

    assert result.results[0].contract_month == "F2023"
    assert result.results[0].cbot_price == 100.0
    assert result.results[0].basis == 10.0
    assert result.results[0].flat_price == pytest.approx(121.254 , rel=1e-3)  # (100 + 10) * 1.10231

    assert result.results[1].contract_month == "G2023"
    assert result.results[1].cbot_price == 105.0
    assert result.results[1].basis == 10.0
    assert result.results[1].flat_price == pytest.approx(126.766, rel=1e-3)  # (105 + 10) * 1.10231

# Teste com uma entrada de basis invalida
def test_basis_as_string(flat_price_service):
    with pytest.raises(InvalidInputError) as exc_info:
        flat_price_service.calculate_flat_prices(
            basis="not_a_number",
            contract_months=["F2023"]
        )
    assert str(exc_info.value.detail) == "Invalid data. Basis must be a number."

# Teste para lista de contratos com um contrato inválido
def test_multiple_contracts_one_invalid(flat_price_service, mock_repository):
    mock_repository.get_price_by_contract_month.side_effect = [
        100.0,
        ContractMonthNotFound("G2023")
    ]

    result = flat_price_service.calculate_flat_prices(
        basis=10.0,
        contract_months=["F2023", "G2023"]
    )

    assert isinstance(result, FlatPriceResults)
    assert len(result.results) == 2

    assert result.results[0].contract_month == "F2023"
    assert result.results[0].cbot_price == 100.0
    assert result.results[0].basis == 10.0
    assert result.results[0].flat_price == pytest.approx(121.254, rel=1e-3)  # (100 + 10) * 1.10231

    assert "error" in result.results[1]
    assert result.results[1]["error"] == "Contract month 'G2023' not found."

#  Teste para lista de contratos vazia
def test_empty_contract_months(flat_price_service):
    result = flat_price_service.calculate_flat_prices(
        basis=10.0,
        contract_months=[]
    )

    assert isinstance(result, FlatPriceResults)
    assert len(result.results) == 0

# Teste para conversion_factor personalizado
def test_custom_conversion_factor(flat_price_service, mock_repository):
    mock_repository.get_price_by_contract_month.return_value = 100.0

    result = flat_price_service.calculate_flat_prices(
        basis=10.0,
        contract_months=["F2023"],
        conversion_factor=1.5
    )

    assert isinstance(result, FlatPriceResults)
    assert len(result.results) == 1
    assert result.results[0].contract_month == "F2023"
    assert result.results[0].cbot_price == 100.0
    assert result.results[0].basis == 10.0
    assert result.results[0].flat_price == pytest.approx(165.0, rel=1e-3)  # (100 + 10) * 1.5