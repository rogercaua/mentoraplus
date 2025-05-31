
# 🚀 Mentora+ API

API desenvolvida em Django + Django Ninja para gerenciamento de conteúdos educacionais, sugestões da comunidade, discussões e comentários.

## 📚 Funcionalidades

- Autenticação com **JWT** (Login, Registro e Logout)
- Gerenciamento de **Usuários** (`user`, `admin`)
- CRUD de **Conteúdos** (roadmaps, cursos, etc.)
- Sistema de **Recomendações** de conteúdos:
  - Usuários podem sugerir
  - Admins podem aprovar ou rejeitar
- Sistema de **Discussões**:
  - Discussões vinculadas a um conteúdo
  - Comentários nas discussões
- Sistema de **Tags** para organizar conteúdos
- Painel de documentação automática via **Swagger** ou **Redoc**

## 🛠️ Tecnologias e Bibliotecas

- **Python 3.13**
- **Django 5.2.1**
- **Django Ninja**
- **SQLite** 
- **JWT Authentication**
- **Swagger / Redoc Docs**

## ⚙️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/rogercaua/mentoraplus
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate   # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Realize as migrações:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Rode o servidor:
```bash
python manage.py runserver
```

## 🔑 Autenticação

A autenticação é feita via **JWT Token**.

### Rotas principais de autenticação:
- `POST /api/user/register` — Registro de usuário
- `POST /api/user/login` — Login (retorna JWT)

O token JWT deve ser enviado no header:
```
Authorization: Bearer <seu-token>
```

## 🌐 Documentação Interativa

- Swagger: [http://127.0.0.1:8000/api/docs](http://127.0.0.1:8000/api/docs)

## 📦 Principais Endpoints

### 🔸 Usuários
- Registro, login, logout
- Listagem (admins)
- Alteração e exclusão (admins)

### 🔸 Conteúdos
- CRUD completo
- Filtros por tipo e tags

### 🔸 Recomendações
- Usuários podem sugerir
- Admins podem aprovar, rejeitar ou excluir

### 🔸 Discussões
- Criar discussões sobre um conteúdo
- Fechar discussões (admin)

### 🔸 Comentários
- Comentários dentro de discussões

## 🏷️ Sistema de Tags

- Tags são automaticamente capitalizadas na criação.
- Ajudam na organização e busca de conteúdos.

## 💾 Banco de Dados

- Banco padrão: **SQLite** (desenvolvimento)
- Arquivo: `db.sqlite3`

## 👨‍💻 Autor

- **Mentora+ API**
- Feito por Roger 🎯
