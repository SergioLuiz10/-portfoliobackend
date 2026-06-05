from fastapi import FastAPI
from app.routers import ingest
from app.routers import chat
#Filtro que controla quem pode chamar a API  
from fastapi.middleware.cors import CORSMiddleware



#cria a aplicação FastAPI e registra o router de ingestão
app = FastAPI(title="Ask Sérgio API")

#Configura o CORS para permitir solicitações de qualquer origem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitações de qualquer origem
    allow_methods=["*"],  # Permite todos os métodos HTTP
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

#faz a rota /ingest passar a existir de verdade,bater em POST /ingest funciona
app.include_router(ingest.router)

#faz a rota /chat passar a existir de verdade,bater em POST /chat funciona
app.include_router(chat.router)

@app.get("/")
def raiz():
    return {"message": "Bem-vindo à API de Perguntas e Respostas do Sérgio!"}