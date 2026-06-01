from fastapi import APIRouter
from app.schemas.chat import EntradaDoChat, RespostaDoChat
from app.rag.retriever import buscar_chunks_parecidos#BUSCAR contexto no banco   
from app.rag.gerador import gerar_resposta #GERAR a resposta do modelo usando o contexto

#função que o endpoint vai chamar. Quando alguém bater em POST /chat

router= APIRouter()


#endpoint de chat, recebe a pergunta do usuário, busca os chunks parecidos no banco e gera a resposta usando o modelo
@router.post("/chat", response_model=RespostaDoChat)


def conversar_com_sergioAI(entrada: EntradaDoChat):
    chunks_parecidos = buscar_chunks_parecidos(entrada.message) #BUSCAR contexto no banco usando a pergunta do usuário
    #GERAR a resposta do modelo usando o contexto , pergunta do usuário e idioma
    resposta_gerada = gerar_resposta(
        pergunta_usuario=entrada.message,
        pedaços_parecidos=chunks_parecidos,
        idioma=entrada.language,
    )
    return RespostaDoChat(response=resposta_gerada) #retorna a resposta gerada no formato definido pela resposta do chat