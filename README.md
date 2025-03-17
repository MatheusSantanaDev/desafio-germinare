# Desafio: Criando um Endpoint para Cálculo do Flat Price da Soja

## Objetivo
O desafio consiste em criar um endpoint que receba o valor do **Basis** (prêmio de exportação) e retorne o **Flat Price** da soja. O preço futuro da soja será obtido a partir de uma tabela armazenada no banco de dados. Você pode utilizar a linguagem que preferir.

## Regras do Cálculo
O **Flat Price** da soja é definido pela seguinte fórmula:

Flat Price = (Preço Futuro (CBOT) + Basis)*Fator de conversão

Onde:
- **Preço Futuro (CBOT)**: Cotação do contrato futuro de farelo soja, armazenada no banco de dados.
- **Basis**: Valor informado pelo usuário no request.
- **Fator de conversão**: Valor padrão para calculo de conversão de 1.10231

## Requisitos do Endpoint
- Deve ser um **endpoint HTTP** (ex: REST API).
- Deve aceitar **apenas** um parâmetro: `basis`.
- Deve buscar o **último preço futuro disponível** na base de dados.
- Deve calcular e retornar o **Flat Price**.

## Exemplo de Requisição e Resposta
### **Requisição (HTTP POST ou GET)**
```http
GET /api/flat_price?basis=-0.50
```

### **Resposta (JSON)**
```json
{
  "cbot_price": 305.50,
  "basis": -5.0,
  "flat_price": 331.24
}
```

## Banco de Dados
A tabela que armazena os preços futuros deve ter a seguinte estrutura:

```sql
CREATE TABLE cbot_prices (
    id SERIAL PRIMARY KEY,
    contract_month VARCHAR(10),
    price DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

O endpoint deve buscar o **preço mais recente** inserido nesta tabela.

## Bônus
Para aprimorar sua solução, você pode:
-  Utilizar python e fastapi para desenvolvimento
- Criar uma validação para garantir que o **basis** seja um número válido.
- Criar uma classe de flatprice que valide os tipos e possa ter outras funções para calculos
- Implementar um cache para evitar consultas repetitivas ao banco de dados.
- Criar testes unitários para validar o cálculo.

---

### **Entrega**
Suba seu código em um repositório público (GitHub, GitLab, etc.) e forneça instruções para execução.

Boa sorte! 🚀

