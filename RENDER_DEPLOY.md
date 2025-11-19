# 🚀 Guia Definitivo - Deploy Backend no Render

## ✅ **Problemas Corrigidos**

- ✅ Removido `greenlet` que causava erro gcc
- ✅ Removido `ujson` que causava erro de compilação C
- ✅ `requirements.txt` otimizado para Render
- ✅ Validação obrigatória de `MONGO_URL`

---

## 📋 **Pré-Requisitos**

1. ✅ Conta no GitHub
2. ✅ Conta no Render.com (gratuita)
3. ✅ MongoDB Atlas configurado (connection string pronta)

---

## 🔧 **Opção 1: Repositório Separado (RECOMENDADO)**

### **Passo 1: Criar Repositório Backend Separado**

```bash
# 1. Criar nova pasta limpa
mkdir grandefamilia-backend
cd grandefamilia-backend

# 2. Copiar apenas arquivos do BACKEND/
# (Ajuste o caminho conforme a localização do seu projeto)
cp ../seu-projeto/BACKEND/* .
cp ../seu-projeto/BACKEND/routes/* ./routes/

# 3. Estrutura final deve ser:
# grandefamilia-backend/
# ├── main.py
# ├── database.py
# ├── models.py
# ├── requirements.txt  ← NA RAIZ
# ├── render.yaml
# ├── .env.example
# ├── .gitignore
# ├── README.md
# └── routes/
#     ├── __init__.py
#     ├── products.py
#     └── categories.py

# 4. Inicializar Git
git init
git add .
git commit -m "Backend FastAPI otimizado para Render - sem dependências C/C++"

# 5. Criar repositório no GitHub
# Acesse: https://github.com/new
# Nome sugerido: grandefamilia-backend
# Tipo: Public ou Private

# 6. Push para GitHub
git remote add origin https://github.com/SEU_USUARIO/grandefamilia-backend.git
git branch -M main
git push -u origin main
```

### **Passo 2: Configurar no Render**

1. **Login no Render**: https://dashboard.render.com/

2. **Criar Web Service**:
   - Clique em **"New +"** → **"Web Service"**
   - Clique em **"Connect a repository"**
   - Selecione `grandefamilia-backend`

3. **Configurações do Serviço**:
   ```
   Name: fashion-catalog-api
   Region: Oregon (US West) ou mais próximo
   Branch: main
   Root Directory: .  ← DEIXE VAZIO ou . (ponto)
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   Instance Type: Free
   ```

4. **Variáveis de Ambiente** (CRÍTICO):
   - Clique em **"Add Environment Variable"**
   
   **Variáveis obrigatórias:**
   ```
   MONGO_URL = mongodb+srv://usuario:senha@cluster.mongodb.net/?retryWrites=true&w=majority
   MONGO_DB_NAME = fashion_catalog
   CORS_ORIGINS = http://localhost:3000
   ```
   
   **⚠️ IMPORTANTE**: Substitua `usuario:senha@cluster` pelos seus dados do MongoDB Atlas!

5. **Deploy**:
   - Clique em **"Create Web Service"**
   - Aguarde 3-5 minutos
   - URL da API: `https://fashion-catalog-api.onrender.com`

---

## 🔧 **Opção 2: Monorepo com Root Directory**

Se preferir manter tudo em um repositório:

### **Configuração no Render**:

```
Root Directory: BACKEND  ← IMPORTANTE!
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

**⚠️ ATENÇÃO**: O `requirements.txt` DEVE estar em `BACKEND/requirements.txt` no seu repositório.

---

## 🧪 **Testar o Deploy**

### **1. Health Check**
```bash
curl https://fashion-catalog-api.onrender.com/health
```

**Resposta esperada:**
```json
{
  "status": "healthy",
  "service": "fastapi-backend"
}
```

### **2. Teste de API**
```bash
curl https://fashion-catalog-api.onrender.com/
```

**Resposta esperada:**
```json
{
  "message": "Fashion Catalog API - Loja A Grande Família",
  "version": "1.0.0",
  "docs": "/docs",
  "status": "running"
}
```

### **3. Documentação Interativa**
Abra no navegador:
```
https://fashion-catalog-api.onrender.com/docs
```

---

## 🔍 **Verificar Logs no Render**

1. Acesse o dashboard do Render
2. Clique no seu serviço
3. Vá em **"Logs"**
4. Verifique se há erros

**Logs esperados (sucesso):**
```
==> Building...
Collecting fastapi==0.115.12
Collecting uvicorn==0.34.0
...
Successfully installed fastapi-0.115.12 uvicorn-0.34.0
==> Build successful 🎉

==> Deploying...
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:10000
INFO:     Application startup complete
✅ Database indexes initialized successfully
```

**Erros comuns e soluções:**

| Erro | Causa | Solução |
|------|-------|---------|
| `KeyError: 'MONGO_URL'` | Variável não configurada | Adicionar `MONGO_URL` no Environment |
| `gcc exit code 1` | Dependências C/C++ | ✅ JÁ CORRIGIDO - use novo `requirements.txt` |
| `No such file 'requirements.txt'` | Root Directory errado | Configurar `Root Directory: BACKEND` |
| `502 Bad Gateway` | Porta errada | Usar `--port $PORT` no start command |

---

## 🔄 **Atualizar Frontend (Importante)**

Após deploy bem-sucedido, atualize a variável no **Vercel**:

1. Acesse: https://vercel.com/seu-projeto/settings/environment-variables
2. Edite `NEXT_PUBLIC_FASTAPI_URL`
3. Novo valor: `https://fashion-catalog-api.onrender.com`
4. Salve e faça redeploy do frontend

---

## 📊 **Monitoramento**

### **Free Tier do Render - Importante Saber**

- ⏱️ **Serviço hiberna** após 15 minutos de inatividade
- 🐌 **Primeira requisição** após hibernação demora ~30 segundos
- 💰 **750 horas/mês grátis** (suficiente para manter ativo 24/7)
- 📈 **Upgrade para paid** evita hibernação ($7/mês)

### **MongoDB Atlas Free Tier**

- 💾 **512MB de armazenamento** gratuito
- 👥 **Unlimited connections**
- 🌍 **Deployado em 3 regiões**

---

## ✅ **Checklist Final**

Antes de considerar o deploy bem-sucedido:

- [ ] `requirements.txt` otimizado (sem greenlet/ujson)
- [ ] Repositório criado no GitHub
- [ ] Serviço criado no Render
- [ ] Root Directory configurado corretamente
- [ ] Variáveis de ambiente adicionadas (`MONGO_URL`, `CORS_ORIGINS`)
- [ ] Build concluído sem erros gcc
- [ ] Health check retorna `200 OK`
- [ ] `/docs` acessível no navegador
- [ ] Frontend atualizado com nova URL
- [ ] Teste end-to-end funcionando

---

## 🎉 **Deploy Bem-Sucedido!**

Se todos os testes passaram:

```
✅ Backend FastAPI rodando no Render
✅ MongoDB Atlas conectado
✅ CORS configurado para o frontend
✅ API documentação acessível
✅ Pronto para produção!
```

---

## 📞 **Suporte**

**Problemas?**

1. Verifique os logs no Render Dashboard
2. Teste localmente: `python main.py`
3. Valide MongoDB connection string
4. Confirme variáveis de ambiente

**Render Docs**: https://render.com/docs/web-services

---

**Backend otimizado e pronto para deploy limpo!** 🚀
