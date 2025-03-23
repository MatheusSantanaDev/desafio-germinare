# Desafio: Criando um Endpoint para Cálculo do Flat Price da Soja

## Execuçao do Projeto

### Requisitos
* **Python 3.11**

No diretorio principal do projeto faça o ***.env*** pessoal seguindo o ***.example.env***, em seguida execute:

> ```bash
> chmod +x setup_and_run.sh
> ./setup_and_run.sh
> ```
Esse pipeline configura o ambiente com os pacotes necessarios, faz as migrations necessarias e coloca a aplicação up. **Sempre que quiser subir a aplicação pode executar** ```./setup_and_run.sh```, ou uma vez configurado é possivel usar:

```python
uvicorn app.main:app --reload
```

## Objetivo
O desafio consiste em criar um endpoint que receba dois valores, **Basis** (prêmio de exportação) e **Mês do contrato** (contract_month) e retorne o **Flat Price** do farelo de soja. O preço futuro do farelo de soja será obtido a partir de uma tabela armazenada no banco de dados. Você pode utilizar a linguagem que preferir.

## Regras do Cálculo
O **Flat Price** da soja é definido pela seguinte fórmula:

Flat Price = (Preço Futuro (CBOT) + Basis)*Fator de conversão

Onde:
- **Preço Futuro (CBOT)**: Cotação do contrato futuro de farelo soja, armazenada no banco de dados que é diferenciada pelo nome do contrato que é o contract_month.
- **Basis**: Valor informado pelo usuário no request.
- **Fator de conversão**: Valor padrão para calculo de conversão de 1.10231

---

## **📡 Requisitos do Endpoint**
- Deve ser um **endpoint HTTP POST** (REST API).
- Deve aceitar um JSON contendo:
  - `basis` (valor numérico que pode ser negativo ou positivo).
  - `contract_months` (lista de contratos futuros).
- Deve buscar o **último preço futuro disponível** no banco de dados para cada `contract_month`.
- Deve calcular e retornar o **Flat Price**.
- Deve fornecer respostas padronizadas e tratamento de erros.

---


### **📩 Requisição (HTTP POST)**
```http
POST /api/flat_price
Content-Type: application/json
```

```json
{
  "basis": -5.00,
  "contract_months": ["MAY24", "JUL24"]
}
```


### **Resposta (JSON)**
```json
{

  "results": [
    {
      "contract_month": "MAY24",
      "cbot_price": 450.00,
      "basis": -5.00,
      "flat_price": 403.74
    },
    {
      "contract_month": "JUL24",
      "cbot_price": 460.00,
      "basis": -5.00,
      "flat_price": 413.29
    }
  ]
}

```

## Banco de Dados
A tabela que armazena os preços futuros deve ter a seguinte estrutura:

```sql
CREATE TABLE soybean_meal_prices (
    id SERIAL PRIMARY KEY,
    contract_month VARCHAR(10) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

O endpoint deve buscar o **preço mais recente** inserido nesta tabela.

## **❌ Tratamento de Erros**
O sistema deve retornar respostas padronizadas para diferentes cenários de erro:

| **Cenário**                      | **Código HTTP**            | **Exemplo de Resposta** |
|----------------------------------|---------------------------|-------------------------|
| `contract_month` não encontrado | `404 Not Found`           | `{ "error": "Contract month MAY24 not found" }` |
| `basis` inválido                | `400 Bad Request`         | `{ "error": "Basis must be a number between -50 and 50" }` |
| Erro interno do servidor        | `500 Internal Server Error` | `{ "error": "Unexpected server error" }` |

## Bônus
Para aprimorar sua solução, você pode:
-  Utilizar python e fastapi para desenvolvimento
- Criar uma classe de flatprice que valide os tipos e possa ter outras funções para calculos
- Implementar um cache para evitar consultas repetitivas ao banco de dados.
- Criar testes unitários para validar o cálculo.

---

### **Entrega**
Suba seu código em um repositório público (GitHub, GitLab, etc.) e forneça instruções para execução.

Boa sorte! 🚀

