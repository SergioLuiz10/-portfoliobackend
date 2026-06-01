from fastapi import FastAPI
from app.routers import ingest
from app.routers import chat

#cria a aplicação FastAPI e registra o router de ingestão
app = FastAPI(title="Ask Sérgio API")

#faz a rota /ingest passar a existir de verdade,bater em POST /ingest funciona
app.include_router(ingest.router)

#faz a rota /chat passar a existir de verdade,bater em POST /chat funciona
app.include_router(chat.router)

@app.get("/")
def raiz():
    return {"message": "Bem-vindo à API de Perguntas e Respostas do Sérgio!"}