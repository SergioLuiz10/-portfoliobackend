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
    "https://portfoliofrontend-lovat-chi.vercel.app",  # frontend Next.js em produção
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origens_permitidas, # só permite chamadas dessas origens
    allow_credentials=False,  # não permite cookies ou credenciais de autenticação
    allow_methods=["*"], # permite todos os métodos HTTP (GET, POST, etc.) 
    allow_headers=["*"],# permite todos os headers (Content-Type, Authorization, etc.
)

# faz a rota /ingest passar a existir de verdade,bater em POST /ingest funciona
app.include_router(ingest.router)

# faz a rota /chat passar a existir de verdade,bater em POST /chat funciona
app.include_router(chat.router)


@app.get("/")
def raiz():
    return {"message": "Bem-vindo à API de Perguntas e Respostas do Sérgio!"}
