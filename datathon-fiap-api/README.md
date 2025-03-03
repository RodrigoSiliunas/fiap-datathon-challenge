# 🚀 API de Previsões

Este diretório contém a nossa **API**, que pode ser executada utilizando **FastAPI** ou **Flask**, conforme sua preferência.  

## ⚙️ Configuração do Ambiente

Para garantir que o código rode corretamente, é necessário criar um ambiente virtual (`venv`) e instalar as dependências.  

### 📌 Passo a passo:

1. **Crie um ambiente virtual dentro desta pasta**:  
   ```sh
   python -m venv venv
   ```
2. **Ative o ambiente virtual**:  
   - No **Windows**:  
     ```sh
     venv\Scripts\activate
     ```
   - No **Linux/Mac**:  
     ```sh
     source venv/bin/activate
     ```
3. **Atualize os pacotes essenciais**:  
   ```sh
   python -m pip install --upgrade wheel setuptools pip
   ```
4. **Instale as dependências do projeto**:  
   ```sh
   python -m pip install -r requirements.txt
   ```

---

## 📂 Estrutura dos Arquivos

Nesta pasta, temos três arquivos principais:

1. **`app_flask.py`** – API escrita em **Flask**.
2. **`app.py`** – API escrita em **FastAPI**.
3. **`tests.py`** – Testes automatizados com **pytest**.

🔹 **Por que temos duas versões?**  
Disponibilizamos tanto o **Flask** quanto o **FastAPI** para que o avaliador utilize a tecnologia com a qual se sentir mais confortável.  

🔹 **Sobre os testes (`tests.py`)**  
Criamos três testes simples para validar a API. Como se trata de um projeto pequeno, não há muitas variações de testes necessárias.

---

## ▶️ Executando a API

Para rodar a API utilizando **FastAPI**, use o seguinte comando:  
```sh
uvicorn app:app --host 0.0.0.0 --port 8000
```

⚠️ **Atenção!**
Para que o código funcione corretamente, o arquivo **`modelo_recomendacao.pkl`** deve estar **na raiz da API**, junto com os arquivos mencionados acima.

---

## 🌐 Como Consumir a API

A API possui dois endpoints principais:

### 📍 1. **Verificar se a API está rodando**
- **Rota:** `/`
- **Método:** `GET`
- **Resposta esperada:**
  ```json
  { "message": "API de Recomendação de Notícias está rodando!" }
  ```

### 📍 2. **Obter Recomendações de Notícias**
- **Rota:** `/predict/`
- **Método:** `GET`
- **Parâmetros:**
  - `user_id` (opcional) → ID do usuário para recomendações personalizadas.
  - `top_n` (opcional, padrão: `5`) → Número de recomendações desejadas.

- **Exemplo de chamadas:**
  - Obter **recomendações personalizadas** para um usuário específico:
    ```
    /predict/?user_id=user123&top_n=5
    ```
  - Obter **recomendações gerais** (sem um usuário específico):
    ```
    /predict/?top_n=5
    ```

- **Exemplo de resposta:**
  ```json
  [
    {
      "page": "noticia_123",
      "url": "https://site.com/noticia_123",
      "title": "Título da Notícia",
      "caption": "Resumo da notícia...",
      "recency_days": 2
    },
    {
      "page": "noticia_456",
      "url": "https://site.com/noticia_456",
      "title": "Outra Notícia",
      "caption": "Resumo...",
      "recency_days": 5
    }
  ]
  ```

---

## ✅ Como Rodar os Testes

O projeto inclui **testes automatizados** utilizando `pytest` e `FastAPI TestClient` para validar o funcionamento da API.

### 🔹 Como executar os testes:

1. **Certifique-se de que a API esteja configurada corretamente** e que todas as dependências estejam instaladas.
2. **Execute os testes** com o seguinte comando:  
   ```sh
   pytest tests.py
   ```
   Ou, se estiver dentro da pasta da API:
   ```sh
   pytest
   ```

### 📌 O que os testes verificam?
- **`test_predict_no_user()`**
  - Testa a recomendação para usuários anônimos (cold-start).
- **`test_predict_with_user()`**
  - Testa a recomendação para um usuário específico (mesmo que ele não exista).
- **`test_predict_invalid_user()`**
  - Testa a recomendação para um usuário que não está no dataset (também resultando em cold-start).

Se todos os testes passarem, você verá uma saída semelhante a esta:
```
============================= test session starts =============================
collected 3 items

tests.py ...                                                           [100%]

============================== 3 passed in 0.5s ==============================
```

Se algum teste falhar, verifique os logs para entender o problema e corrigir antes de rodar a API em produção. 🛠️

---

Agora, tudo pronto para rodar a API! 🚀🔥