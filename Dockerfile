# Imagem base com Python 3.9 e compiladores necessários para bibliotecas como Pillow
FROM python:3.9-slim as builder

# Instala dependências de sistema necessárias
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Diretório de trabalho
WORKDIR /app

# Copia apenas os arquivos necessários para instalação de dependências
COPY requeriments.txt .

# Instala dependências do Python
RUN pip install --user --no-cache-dir -r requeriments.txt

# --- Fase final (imagem reduzida) ---
FROM python:3.9-slim

# Copia apenas as dependências instaladas da fase builder
COPY --from=builder /root/.local /root/.local
COPY --from=builder /usr/lib/x86_64-linux-gnu/libpq.so* /usr/lib/x86_64-linux-gnu/

# Garante que os scripts no .local estejam no PATH
ENV PATH=/root/.local/bin:$PATH

# Diretório de trabalho
WORKDIR /app

# Copia o restante da aplicação
COPY . .

# Configurações recomendadas para o Flask em produção
ENV FLASK_APP=main.py
ENV FLASK_ENV=production

# Porta do aplicativo
EXPOSE 5000

# Comando de execução com Gunicorn (ajuste o worker conforme seus recursos)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "main:app"]
