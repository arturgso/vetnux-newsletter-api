# 🩺 Vetnux Newsletter API

Uma API FastAPI para gerenciamento de newsletters da Vetnux, com funcionalidades de inscrição e gerenciamento de assinantes.

## 🚀 Tecnologias

- **FastAPI** - Framework web moderno e rápido para Python
- **SQLAlchemy** - ORM para Python com suporte async
- **PostgreSQL** - Banco de dados relacional
- **Docker** - Containerização da aplicação
- **Pydantic** - Validação de dados e serialização

## 📁 Estrutura do Projeto

```
vetnux-newsletter-api/
├── main.py              # Aplicação principal FastAPI
├── config.py            # Configurações da aplicação
├── database.py          # Configuração do banco de dados
├── models.py            # Modelos SQLAlchemy
├── schemas.py           # Schemas Pydantic
├── requirements.txt     # Dependências Python
├── Dockerfile          # Configuração Docker
├── docker-compose.yml  # Orquestração de containers
├── .env.example        # Exemplo de variáveis de ambiente
└── README.md           # Documentação
```

## 🔧 Configuração Local

### Pré-requisitos

- Python 3.11+
- PostgreSQL (separado ou em container)
- Docker e Docker Compose
- Rede Docker externa `shared-network`

### 1. Clone o repositório

```bash
git clone <seu-repositorio>
cd vetnux-newsletter-api
```

### 2. Configure as variáveis de ambiente

```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

**Para Docker (rede compartilhada):**
```bash
# .env
DATABASE_URL=postgresql+asyncpg://postgres:root@postgres:5432/postgres
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development
```

**Para desenvolvimento local:**
```bash
# .env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/newsletter_db
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute a aplicação

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

A API estará disponível em `http://localhost:8000`

## 🐳 Execução com Docker

### Pré-requisitos Docker

Primeiro, crie a rede compartilhada:

```bash
# Criar rede externa compartilhada
docker network create shared-network
```

### Desenvolvimento com duas réplicas

```bash
# Configure o .env para Docker
cp .env.example .env
# Edite DATABASE_URL para: postgresql+asyncpg://postgres:root@postgres:5432/postgres

# Build e start dos containers
docker-compose up --build

# Em background
docker-compose up -d --build
```

> **Nota**: O PostgreSQL deve estar executando separadamente na rede `shared-network` ou acessível via hostname `postgres`.

### Comandos úteis

```bash
# Parar todos os containers
docker-compose down

# Visualizar logs
docker-compose logs -f

# Rebuild apenas a API
docker-compose build api-1 api-2

# Escalar manualmente
docker-compose up --scale api-1=3 --scale api-2=3
```

## 🌐 Endpoints da API

### Principais

- `GET /` - Informações básicas da API
- `GET /health` - Health check da aplicação
- `POST /subscribe` - Inscrever novo assinante
- `GET /docs` - Documentação interativa (Swagger UI)
- `GET /redoc` - Documentação alternativa (ReDoc)

### Exemplo de uso

```bash
# Health check - Instância 1
curl http://localhost:8001/health

# Health check - Instância 2
curl http://localhost:8002/health

# Inscrever assinante (Instância 1)
curl -X POST "http://localhost:8001/subscribe" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "email": "joao@exemplo.com",
    "veterinary_interest": "pequenos_animais"
  }'
```

## 🏗️ Arquitetura

A aplicação utiliza duas instâncias conectadas a uma rede compartilhada:

```
Internet → Load Balancer (Servidor) → API Instance 1 (porta 8001)
                                    → API Instance 2 (porta 8002)
                                           ↓
                                  PostgreSQL (rede compartilhada)
```

### Componentes

- **Load Balancer**: Configurado diretamente no servidor (Nginx/HAProxy)
- **API Instances**: Duas réplicas da aplicação FastAPI
- **PostgreSQL**: Banco de dados em rede compartilhada Docker
- **Shared Network**: Rede Docker externa para comunicação entre serviços

## 🔒 Segurança

- Validação de dados com Pydantic
- CORS configurado para origens específicas
- Containers executam com usuário não-root
- Health checks implementados
- Variáveis de ambiente para configurações sensíveis

## 📊 Monitoramento

### Health Checks

- **API**: `GET /health`
- **Database**: Verificação de conectividade automática
- **Docker**: Health checks configurados nos containers

### Logs

```bash
# Logs da aplicação
docker-compose logs api-1 api-2

# Verificar status da rede
docker network inspect shared-network
```

## 🧪 Desenvolvimento

### Estrutura de dados

```python
# Subscriber Model
{
    "id": int,
    "name": str,
    "email": str,
    "veterinary_interest": str,
    "is_active": bool,
    "created_at": datetime,
    "updated_at": datetime
}
```

### Adicionando novos endpoints

1. Defina o schema em `schemas.py`
2. Adicione o endpoint em `main.py`
3. Atualize a documentação se necessário

## 🚀 Deploy

### Variáveis de ambiente de produção

```bash
# .env
DATABASE_URL=postgresql+asyncpg://user:pass@prod-db:5432/newsletter
CORS_ORIGINS=https://seudominio.com,https://www.seudominio.com
ENVIRONMENT=production
```

### Comandos de deploy

```bash
# Build para produção
docker-compose -f docker-compose.yml build

# Deploy com logs
docker-compose up -d && docker-compose logs -f
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Add: nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença [MIT](LICENSE).

## 📞 Suporte

Para dúvidas ou suporte, entre em contato:

- Email: suporte@vetnux.com
- Issues: [GitHub Issues](link-para-issues)

---

Desenvolvido com ❤️ pela equipe Vetnux
