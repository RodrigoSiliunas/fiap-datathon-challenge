# 📊 Notebooks de Processamento e Treinamento

Nesta pasta, você encontrará **dois notebooks essenciais** para a preparação dos dados e o treinamento do modelo de Machine Learning.

---

## ⚙️ Configuração do Ambiente

Antes de executar os notebooks, é fundamental configurar corretamente o ambiente Python para evitar problemas de compatibilidade e garantir que todas as dependências estejam instaladas.

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

Após seguir esses passos, seu ambiente estará pronto para rodar os notebooks sem problemas! ✅

---

## 📝 1. Convertendo Arquivos CSV para Parquet

🔹 **Notebook:** `convert_to_parquet.ipynb`
🔹 **Objetivo:** Converter arquivos `.csv` em `.parquet` para otimizar o processamento de dados.

### ⚠️ Atenção!
Antes de executar este notebook, **certifique-se de que os arquivos CSV estão na pasta correta**. Se os dados não estiverem organizados corretamente, o código pode falhar.

---

## 🤖 2. Treinamento do Modelo de Machine Learning

🔹 **Notebook:** `datathon_fiap_machine_learning.ipynb`
🔹 **Objetivo:** Processar os dados e treinar o modelo de recomendação.

### 🔍 Etapas realizadas neste notebook:
1. **Tratamento e pré-processamento dos dados** 📊
2. **Aplicação do modelo TF-IDF** para transformar os textos
3. **Uso da métrica Cosine Similarity** para encontrar notícias semelhantes 🔗
4. **Salvamento do modelo** utilizando a biblioteca `pickle` 📦

---

## 📂 Salvando o Modelo

Após a execução do notebook de Machine Learning, será gerado um arquivo **`.pkl`** contendo o modelo treinado.

🔹 **O que fazer com este arquivo?**  
✅ **Mova o arquivo `.pkl` para a pasta** `datathon-fiap-api`
✅ **Leia o README.md dentro da pasta da API** para mais informações sobre como utilizá-lo.

---

Agora, siga os passos corretamente e execute os notebooks! 🚀📈
