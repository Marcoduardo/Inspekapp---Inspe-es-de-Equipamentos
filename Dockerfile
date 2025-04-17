# Usa uma imagem base do Python (versão slim para reduzir tamanho)
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos necessários para o container
COPY . /app

# Instala as dependências do Python
RUN pip install --no-cache-dir -r pendências.txt

# Expõe a porta que o Flask vai rodar (normalmente 5000)
EXPOSE 5000

# Comando para executar o aplicativo Flask usando Gunicorn (recomendado para produção)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
