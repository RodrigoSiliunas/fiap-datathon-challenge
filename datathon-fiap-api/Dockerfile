# 🔹 Usar a imagem do Python 3.11
FROM python:3.11-rc-slim

# 🔹 Definir diretório de trabalho dentro do container
WORKDIR /app

# 🔹 Copiar arquivos para dentro do container
COPY app.py modelo_recomendacao.pkl requirements.txt /app/

# 🔹 Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# 🔹 Expor a porta 8000
EXPOSE 8000

# 🔹 Comando para rodar a API Flask
CMD ["python", "app.py"]
