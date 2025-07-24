# Moto Clube API - Clean Architecture

Este projeto é uma API RESTful para gerenciamento de usuários de um Moto Clube, desenvolvida em Flask seguindo os princípios da Clean Architecture.

## Estrutura do Projeto

- **app.py**: Inicializa o Flask, configurações e registra as rotas.
- **entities/**: Modelos de dados (AuthUser, User).
- **use_cases/**: Casos de uso (lógica de negócio).
- **adapters/**: Adaptadores para rotas, autenticação e repositórios (acesso ao banco).

## Como funciona?

- **Cadastro e Login**: Usuários podem se registrar e fazer login. O login retorna um token JWT.
- **Autenticação**: As rotas protegidas usam o decorator `token_required` para validar o token JWT.
- **Gerenciamento de Perfil**: O usuário pode consultar, atualizar e deletar seu perfil. Admins podem listar e deletar outros usuários.

## Executando o projeto

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute a aplicação:
   ```bash
   python app.py
   ```
3. Acesse as rotas da API via Postman, Insomnia ou similar.

## Principais Rotas

- `POST /register` — Cadastro de usuário
- `POST /login` — Login (retorna JWT)
- `GET /profile` — Consulta o próprio perfil (token obrigatório)
- `PUT /profile` — Atualiza o próprio perfil (token obrigatório)
- `GET /users` — Lista todos os perfis (token obrigatório)
- `GET /users/<user_id>` — Consulta perfil por ID (token obrigatório)
- `DELETE /users/<auth_id>` — Deleta usuário (token obrigatório)

### Upload e acesso de imagens de perfil

- `POST /upload_image` — Upload de imagem de perfil do usuário autenticado (token obrigatório, multipart/form-data, campo `image`).
  - A imagem será otimizada e redimensionada para 500x500 pixels.
  - O arquivo será salvo em `static/profilePics/user_<id>.jpg`.
  - O campo `image_path` no perfil do usuário retorna o caminho relativo para a imagem.
- Imagens podem ser acessadas publicamente via:
  - `GET /static/profilePics/user_<id>.jpg`

#### Exemplo de upload via curl
```bash
curl -X POST http://localhost:5000/api/v1/upload_image \
  -H "Authorization: Bearer <SEU_TOKEN>" \
  -F "image=@/caminho/para/sua/imagem.jpg"
```

#### Exemplo de acesso à imagem
```
http://localhost:5000/static/profilePics/user_1.jpg
```

### Documentação interativa
- Acesse `/apidocs` para visualizar e testar todas as rotas via Swagger UI.

## Observações
- O banco usado é SQLite, criado automaticamente no primeiro run.
- O projeto está pronto para expansão, separando regras de negócio, modelos e rotas para facilitar manutenção e testes.

---

## Deploy com Gunicorn

Para rodar em produção com Gunicorn:

1. Instale o Gunicorn:
   ```bash
   pip install gunicorn
   ```
2. Execute:
   ```bash
   gunicorn --bind 0.0.0.0:5000 wsgi:app
   ```

## Deploy com Docker

1. Construa a imagem:
   ```bash
   docker build -t moto-clube-api .
   ```
2. Rode o container:
   ```bash
   docker run -p 5000:5000 moto-clube-api
   ```

A API estará disponível em `http://localhost:5000`.
