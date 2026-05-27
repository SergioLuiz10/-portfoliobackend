from fastapi import APIRouter 
from app.rag.ingest import rodar_ingestao

#função que o endpoint vai chamar. Quando alguém bater em POST /ingest
router = APIRouter()


#ingestao de docuemntos 
@router.post("/ingest")
def endpoint_de_ingestao():
    quantidade_de_documentos_picados = rodar_ingestao()
    return {"quantidade_de_documentos_picados": quantidade_de_documentos_picados}