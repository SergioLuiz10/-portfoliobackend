# quando rodarem o container ele vai baixar essa imagem do py 
FROM python:3.11-slim 

#pasta de trabalho , pros  arquivos cairiam soltos na raiz do container
WORKDIR /app

#copiar os arquivos do projeto para o container 
COPY requirements.txt .

#instalar as dependencias do projeto
RUN pip install --no-cache-dir -r requirements.txt


#copia todo o projeto para o container
COPY . .

#o comando que roda quando o container liga 
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
