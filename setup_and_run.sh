#!/bin/bash

# cor para echo ter destaque
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Instalando dependências...${NC}"
pip install -r requirements.txt

echo -e "${BLUE}Executando migrações...${NC}"
python manage.py makemigrations
python manage.py migrate

echo -e "${BLUE}Iniciando o servidor FastAPI...${NC}"
uvicorn app.main:app --reload &

sleep 2

echo -e "${BLUE}Servidor FastAPI está rodando!${NC}"
echo -e "${BLUE}Acesse a documentação da API em: http://127.0.0.1:8000/docs${NC}"
wait