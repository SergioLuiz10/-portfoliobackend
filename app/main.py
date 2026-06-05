from fastapi import FastAPI
from app.routers import ingest
from app.routers import chat

# Filtro que controla quem pode chamar a API
from fastapi.middleware.cors import CORSMiddleware


# cria a aplicação FastAPI e registra o router de ingestão
app = FastAPI(title="Ask Sérgio API")

# Lista de origens permitidas (dev local + prod na Vercel quando tiver a URL)
origens_permitidas = [
    "http://localhost:3000",  # frontend Next.js em dev
    # "https://seu-portfolio.vercel.app",  # adicionar no Dia 9
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origens_permitidas,
    allow_methods=["*"],
    allow_headers=["*"],
)

# faz a rota /ingest passar a existir de verdade,bater em POST /ingest funciona
app.include_router(ingest.router)

# faz a rota /chat passar a existir de verdade,bater em POST /chat funciona
app.include_router(chat.router)


@app.get("/")
def raiz():
    return {"message": "Bem-vindo à API de Perguntas e Respostas do Sérgio!"}
