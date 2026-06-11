from fastapi import APIRouter, Depends , Header, HTTPException # vai ler o token do header o token ta no config , se n bater lança erro
from app.rag.ingest import rodar_ingestao
from app.config import objeto_config_env #pega o token pra comparar com o que vem no header

#função que o endpoint vai chamar. Quando alguém bater em POST /ingest
router = APIRouter()



#confere o segredo antes de deixar o /ingest rodar
def conferir_token_admin(tokenAdmin: str = Header(default=None)): # espera receber um header chamado "tokenAdmin"
    if tokenAdmin != objeto_config_env.admin_token: #ve se o token do header é diferente do token q ta no .env(config)
        raise HTTPException(status_code=401, detail="Token de admin inválido") # se n bater, lança erro 401 (não autorizado)

#ingestao de docuemntos 
@router.post("/ingest",dependencies=[Depends(conferir_token_admin)]) #usa a função de conferir o token antes de executar o endpoint e bloqueia se o token for inválido
def endpoint_de_ingestao():
    quantidade_de_documentos_picados = rodar_ingestao()
    return {"quantidade_de_documentos_picados": quantidade_de_documentos_picados}



