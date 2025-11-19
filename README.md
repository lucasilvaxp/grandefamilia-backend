# 🐍 Fashion Catalog API - FastAPI Backend

Backend REST API para o catálogo de moda "Loja A Grande Família".

## 📁 Estrutura do Projeto

```
BACKEND/
├── main.py                 # Entry point da API FastAPI
├── database.py             # Configuração MongoDB
├── models.py               # Modelos Pydantic
├── routes/
│   ├── __init__.py
│   ├── products.py         # Rotas de produtos (CRUD)
│   └── categories.py       # Rotas de categorias
├── requirements.txt        # Dependências Python
├── render.yaml             # Configuração Render.com
├── .env.example            # Exemplo de variáveis de ambiente
├── .gitignore
└── README.md
```

## 🚀 Deploy no Render.com

### Passo 1: Preparar MongoDB

1. **Criar conta no MongoDB Atlas** (gratuito)
   - Acesse: https://www.mongodb.com/cloud/atlas/register
   - Crie um cluster gratuito (M0 Sandbox)

2. **Obter Connection String**
   - No MongoDB Atlas Dashboard, clique em "Connect"
   - Escolha "Connect your application"
   - Copie a connection string no formato:
     ```
     mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
     ```

### Passo 2: Deploy no Render

1. **Criar conta no Render** (gratuito)
   - Acesse: https://render.com/

2. **Criar novo repositório Git**
   ```bash
   cd BACKEND
   git init
   git add .
   git commit -m "Initial FastAPI backend"
   git remote add origin <seu-repositorio-github>
   git push -u origin main
   ```

3. **Conectar Repositório no Render**
   - No Render Dashboard, clique em "New +"
   - Selecione "Web Service"
   - Conecte seu repositório GitHub
   - Selecione o branch `main`

4. **Configurar Serviço**
   - **Name**: `fashion-catalog-api` (ou qualquer nome)
   - **Region**: Escolha a região mais próxima
   - **Branch**: `main`
   - **Root Directory**: `.` (ou `BACKEND` se dentro de monorepo)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

5. **Adicionar Variáveis de Ambiente** (CRÍTICO)
   - No painel do serviço, vá em "Environment"
   - Adicione as seguintes variáveis:
     ```
     MONGO_URL = mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
     MONGO_DB_NAME = fashion_catalog
     CORS_ORIGINS = https://seu-frontend.vercel.app
     ```

6. **Deploy**
   - Clique em "Create Web Service"
   - Aguarde o deploy (3-5 minutos)
   - URL da API: `https://fashion-catalog-api.onrender.com`

### Passo 3: Testar API

```bash
# Health Check
curl https://fashion-catalog-api.onrender.com/health

# Listar produtos
curl https://fashion-catalog-api.onrender.com/api/products

# Documentação interativa
https://fashion-catalog-api.onrender.com/docs
```

## 🔧 Desenvolvimento Local

### Pré-requisitos

- Python 3.11+
- MongoDB local ou MongoDB Atlas

### Setup

1. **Instalar dependências**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar variáveis de ambiente**
   ```bash
   cp .env.example .env
   # Editar .env com suas credenciais MongoDB
   ```

3. **Iniciar servidor**
   ```bash
   python main.py
   # ou
   uvicorn main:app --reload --port 8000
   ```

4. **Acessar**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
   - Redoc: http://localhost:8000/redoc

## 📡 Endpoints da API

### Produtos

- `GET /api/products` - Listar produtos com filtros e paginação
  - Query params: `page`, `pageSize`, `category`, `brand`, `minPrice`, `maxPrice`, `search`, `featured`, `sort`
- `GET /api/products/{id}` - Obter produto por ID
- `POST /api/products` - Criar novo produto
- `PUT /api/products/{id}` - Atualizar produto
- `DELETE /api/products/{id}` - Deletar produto

### Categorias

- `GET /api/categories` - Listar todas categorias
- `GET /api/categories/{id}` - Obter categoria por ID
- `POST /api/categories` - Criar nova categoria
- `DELETE /api/categories/{id}` - Deletar categoria

### Sistema

- `GET /` - Informações da API
- `GET /health` - Health check

## 🗄️ Schema MongoDB

### Products Collection

```json
{
  "_id": ObjectId,
  "name": "Camiseta Polo Masculina",
  "description": "Descrição do produto",
  "price": 49.90,
  "originalPrice": 89.90,
  "category": "Masculino",
  "subcategory": "Camisetas",
  "brand": "Marca X",
  "sizes": ["P", "M", "G", "GG"],
  "colors": [
    { "name": "Azul", "hex": "#0000FF" },
    { "name": "Branco", "hex": "#FFFFFF" }
  ],
  "images": ["https://example.com/image1.jpg"],
  "stock": 50,
  "featured": false,
  "tags": ["polo", "casual"],
  "rating": 4.5,
  "reviewCount": 10,
  "createdAt": ISODate("2024-01-01T00:00:00Z"),
  "updatedAt": ISODate("2024-01-01T00:00:00Z")
}
```

### Categories Collection

```json
{
  "_id": ObjectId,
  "name": "Feminino",
  "slug": "feminino",
  "subcategories": ["Blusas", "Calças", "Vestidos"],
  "image": "https://example.com/category.jpg"
}
```

## 🔐 Segurança

- CORS configurado para aceitar apenas domínios autorizados
- Validação de entrada com Pydantic
- Sanitização de ObjectIds
- Rate limiting (configurar em produção)

## 📊 Performance

- Indexes MongoDB configurados automaticamente
- Paginação eficiente
- Query optimization
- Async operations com Motor

## 🐛 Troubleshooting

### Erro: KeyError: 'MONGO_URL'

**Solução**: Certifique-se de que a variável de ambiente `MONGO_URL` está configurada no Render.

### Erro: CORS

**Solução**: Adicione a URL do frontend Vercel na variável `CORS_ORIGINS`.

### Erro: 502 Bad Gateway no Render

**Solução**: Verifique os logs no Render Dashboard. Geralmente é problema de variável de ambiente ou porta.

## 📝 Notas Importantes

- ✅ **MONGO_URL é obrigatória** - Configure antes de fazer deploy
- ✅ **Free tier do Render hiberna após 15min** - Primeira requisição pode demorar ~30s
- ✅ **MongoDB Atlas tem limite de 512MB** no tier gratuito
- ✅ **Configure CORS_ORIGINS** com a URL do frontend Vercel

## 🔗 Links Úteis

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Motor (MongoDB Async)](https://motor.readthedocs.io/)
- [Render Docs](https://render.com/docs)
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)

## 📞 Suporte

Para dúvidas ou problemas, consulte a documentação ou abra uma issue no repositório.

---

**Backend pronto para produção!** 🚀
