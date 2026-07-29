import time

from fastapi import APIRouter
from fastapi.responses import (
    StreamingResponse,
)  # recebe um generator e manda os pedacinhos pro cliente enquanto sao gerados

from app.observability import (
    registrar_evento,
)  # registra eventos no log, transformando os dados em JSON e enviando para o logger
from app.rag.gerador import (
    gerar_resposta_streaming,
)  # GERAR a resposta do modelo usando o contexto , pergunta do usuário e idioma
from app.rag.retriever import buscar_chunks_parecidos  # BUSCAR contexto no banco
from app.schemas.chat import EntradaDoChat

# função que o endpoint vai chamar. Quando alguém bater em POST /chat

router = APIRouter()


# endpoint de chat, recebe a pergunta do usuário, busca os chunks parecidos no banco
@router.post("/chat")
def conversar_com_sergioAI(
    entrada: EntradaDoChat,
):  # recebe a pergunta do usuário e a linguagem escolhida no formato definido pela EntradaDoChat

    # conta o tempo de início da busca para medir a latência do processamento
    inicio_contagem_deBusca = time.time()

    try:
        chunks_parecidos = buscar_chunks_parecidos(
            entrada.message
        )  # BUSCAR contexto no banco usando a pergunta do usuário
    # captura qualquer falha e guarda na variavel erro
    except Exception as erro:
        # registra o erro no log, transformando os dados em JSON e enviando para o logger
        registrar_evento(
            # coloca o nome pra aparecer na vps
            evento="erro_retrieval",
            # ver qual pergunta foi feita e processada quando quebrou
            pergunta=entrada.message,
            # mostra o erro pela categoria
            tipo_erro=type(erro).__name__,
            # aqui pega a mensagem do erro e transforma em string pra mandar pro log
            erro=str(erro),
        )
        # faz com FastAPI capture e retorne pro cliente
        raise

    fim_contagem_deBusca = (
        time.time()
    )  # conta o tempo para medir a latência do processamento

    # calcula a latência do retrieval em milissegundos
    latencia_retrieval_ms = (fim_contagem_deBusca - inicio_contagem_deBusca) * 1000
    # pega a pergunta do usuário, latência e chunks encontrados
    # tem o rotulo pra registrar
    # e registra no log,
    #  transformando os dados em JSON
    # e enviando para o logger
    registrar_evento(
        evento="chat_recebido",
        pergunta=entrada.message,  # pergunta do usuário
        chunks_encontrados=len(chunks_parecidos),  # quantidade de chunks encontrados
        latencia_retrieval_ms=round(
            latencia_retrieval_ms, 2
        ),  # round para 2 casas decimais a latência do retrieval em milissegundos
        idioma=entrada.language,  # Registra em que idioma o recrutador pediu
    )

    # GERAR a resposta do modelo usando o contexto , pergunta do usuário e idioma
    resposta_gerada = gerar_resposta_streaming(
        pergunta_usuario=entrada.message,
        pedaços_parecidos=chunks_parecidos,
        idioma=entrada.language,
    )
    # StreamingResponse pega o generator e empurra os pedacinhos pela conexão HTTP aberta
    return StreamingResponse(resposta_gerada, media_type="text/plain")
