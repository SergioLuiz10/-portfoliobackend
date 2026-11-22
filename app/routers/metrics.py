from fastapi import APIRouter

from app.observability import (
    metricas,  # faz o registro de métricas de latência e contagem de perguntas, erros, etc.    
)

router = APIRouter()

@router.get("/metrics")
def obter_metricas():
    # retorna as métricas em formato JSON
    return metricas