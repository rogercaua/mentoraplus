# Mentora+

Mentora+ é uma plataforma web de curadoria de conteúdos educacionais, que permite que usuários sugiram materiais (vídeos, cursos, artigos, etc.) e administradores aprovem ou rejeitem essas sugestões. O sistema também inclui autenticação de usuários e um painel para gerenciamento de conteúdos.

## 🚀 Funcionalidades

- ✅ Autenticação de usuários (login)
- ✅ Cadastro de sugestões de conteúdo (Recommendation)
- ✅ Moderação de sugestões pelos administradores (aprovar ou rejeitar)
- ✅ Criação automática de conteúdos aprovados
- ✅ CRUD de conteúdos (Content)
- 🔜 Fórum de discussão entre usuários
- 🔜 Moderação visual via painel

## 📦 Tecnologias utilizadas

- **Backend:** Django + Django Ninja (API REST)
- **Banco de dados:** PostgreSQL
- **Autenticação:** Token personalizado via header
- **ORM:** Django ORM
- **Deploy:** (em desenvolvimento)


## 🔐 Autenticação

A autenticação é feita via token customizado no header:

Authorization: Token <seu_token>


Os usuários possuem um campo `role`, que define se são comuns (`user`) ou administradores (`admin`). Apenas admins podem aprovar ou rejeitar sugestões de conteúdo.

## 🧪 Endpoints principais

### 🔐 Login

`POST /api/user/login`  
Recebe e-mail e senha e retorna o token de autenticação.

---

### 📥 Sugestões (Recommendation)

- `POST /api/recommendation/` – Cria uma nova sugestão (usuário autenticado)
- `GET /api/recommendation/` – Lista todas as sugestões (admin)
- `GET /api/recommendation/pending` – Lista apenas as sugestões pendentes (admin)
- `PATCH /api/recommendation/{id}` – Atualiza status de sugestão (admin)
- `DELETE /api/recommendation/delete_rejected` – Deleta sugestões rejeitadas (admin)

---

### 📚 Conteúdos (Content)

- `POST /api/content/` – Cria novo conteúdo (admin)
- `GET /api/content/` – Lista todos os conteúdos
- `PATCH /api/content/{id}` – Atualiza conteúdo (admin)
- `DELETE /api/content/{id}` – Remove conteúdo (admin)

---

## 👤 Usuários e papéis

- `user`: pode sugerir conteúdos
- `admin`: pode aprovar/rejeitar conteúdos e gerenciar o sistema

## ⚙️ Como rodar o projeto

1. Clone o repositório:

```bash
git clone https://github.com/seu-rogercaua/mentoraplus.git](https://github.com/rogercaua/Mentora-
cd mentoraplus
```

2.Crie um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```
3.instale as dependências:

```bash
pip install -r requirements.txt
```

4.Configure o .env com suas variáveis (ex: chave secreta, DB)

5.Execute as migrações:

```bash
python manage.py migrate
```




