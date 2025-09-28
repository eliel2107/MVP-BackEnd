#  API de Gestão de Ativos de TI 资产管理

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3-black?style=for-the-badge&logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Status](https://img.shields.io/badge/Status-Concluído-brightgreen?style=for-the-badge)

API RESTful desenvolvida em Python com o framework Flask para gerenciar o ciclo de vida de ativos de tecnologia da informação (TI). A aplicação permite o cadastro, consulta, atualização e exclusão de ativos e seus respectivos registros de manutenção.

---

## 🚀 Funcionalidades Principais

* **Gestão de Ativos (CRUD):**
    * `POST /ativo`: Adiciona um novo ativo.
    * `GET /ativos`: Lista todos os ativos, com suporte a filtros por nome, tipo e status.
    * `PUT /ativo`: Atualiza as informações de um ativo existente.
    * `DELETE /ativo`: Remove um ativo da base de dados.
* **Gestão de Manutenções (CRUD):**
    * `POST /manutencao`: Adiciona um novo registro de manutenção a um ativo.
    * `PUT /manutencao`: Atualiza um registro de manutenção.
    * `DELETE /manutencao`: Remove um registro de manutenção.
* **Documentação Automática:**
    * Interface Swagger UI interativa gerada automaticamente para teste e documentação dos endpoints.
* **Inicialização de Banco de Dados:**
    * Comando CLI para criar e popular o banco de dados com dados de exemplo, facilitando a configuração inicial.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.11+**
* **Flask:** Micro-framework web para a construção da API.
* **Flask-OpenAPI3:** Geração automática de documentação OpenAPI 3 (Swagger UI).
* **SQLAlchemy:** ORM para interação com o banco de dados relacional.
* **SQLite:** Banco de dados leve e embarcado, utilizado no projeto.
* **Flask-CORS:** Gerenciamento de Cross-Origin Resource Sharing para permitir a comunicação com o frontend.
* **Pydantic:** Validação de dados através de schemas e type hints.

---

## ⚙️ Instalação e Execução

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

### Pré-requisitos

* [Python 3.11](https://www.python.org/downloads/) ou superior instalado.
* [Git](https://git-scm.com/) instalado.

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone [URL_DO_SEU_REPOSITORIO_AQUI]
    cd [NOME_DA_PASTA_DO_PROJETO]
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Criar o ambiente
    python -m venv .venv

    # Ativar no Windows (PowerShell)
    .\.venv\Scripts\activate

    # Ativar no Linux/macOS
    # source .venv/bin/activate
    ```

3.  **Instale as dependências:**
    Com o ambiente virtual ativo, instale todas as bibliotecas listadas no `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Inicialize o Banco de Dados:**
    Este comando customizado irá criar o arquivo de banco de dados (`database.db`), definir as tabelas e popular com alguns dados de exemplo para facilitar os testes.
    ```bash
    flask init-db
    ```
    *Você só precisa executar este comando uma única vez.*

5.  **Inicie o servidor da API:**
    ```bash
    flask run
    ```
    O servidor estará rodando e acessível em `http://127.0.0.1:5000`.

---

## 📖 Documentação da API (Swagger)

A documentação completa e interativa da API é gerada automaticamente e pode ser acessada enquanto o servidor estiver rodando.

* **URL da Documentação:** [http://127.0.0.1:5000/openapi](http://127.0.0.1:5000/openapi)

Através dessa interface, é possível visualizar todos os endpoints, seus parâmetros, schemas de entrada/saída e executar requisições de teste diretamente do navegador.

---

## 👨‍💻 Autor

* **Eliel de Mesquita Cunha**
* **LinkedIn:** `[https://www.linkedin.com/in/eliel-mesquita0799/]`
* **GitHub:** `[https://github.com/eliel2107]`

---

## 📜 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.