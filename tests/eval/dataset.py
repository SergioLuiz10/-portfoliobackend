from dataclasses import dataclass 

#serve pra representar um caso de avaliação
@dataclass
class CasoAvaliacao:
    #pergunta do recrutador 
    pergunta: str
    #Termos que o chunk CERTO precisa conter  
    palavras_chave: list[str]
    #resposta de referência do recrutador
    resposta_referencia: str


   # Lista com todos os casos de avaliação (as "fileiras do gabarito").
CASOS_AVALIACAO: list[CasoAvaliacao] = [
          # ── Caso 1 ──────────────────────────────
    CasoAvaliacao(
        pergunta="Onde o Sérgio trabalha atualmente?",
        palavras_chave=["MG3"],
        resposta_referencia="Sérgio trabalha atualmente na MG3."

    ),
       # ── Caso 2 ──────────────────────────────
    CasoAvaliacao(
        pergunta="Me fala sobre o projeto Crom.IA.",
        palavras_chave=["Crom.IA", "cromatografia"],
        resposta_referencia=(
            "Crom.IA é uma plataforma de IA pro setor de cromatografia "
            "analítica (HPLC/GC), com arquitetura multi-agente em n8n e "
            "pipeline RAG em FastAPI com LangChain, PGVector e OpenAI."
        ),
    ),

    # ── Caso 3 ──────────────────────────────
    CasoAvaliacao(
        pergunta="Qual a stack favorita do Sérgio pra construir RAG?",
        palavras_chave=["PGVector"],
        resposta_referencia=(
            "FastAPI no backend, LangChain pra orquestração, PostgreSQL "
            "com PGVector como vector store e OpenAI pros LLMs, tudo "
            "containerizado com Docker."
        ),
    ),

    # ── Caso 4 ──────────────────────────────
    CasoAvaliacao(
        pergunta="O Sérgio tem experiência com agentes de IA?",
        palavras_chave =["agente"],
        resposta_referencia=(
            "Sim. No Crom.IA ele construiu uma arquitetura multi-agente "
            "em n8n com um Orquestrador roteando pra agentes "
            "especializados (troubleshooting, estudo guiado, gestão)."
        ),
    ),

    # ── Caso 5 ──────────────────────────────
    CasoAvaliacao(
        pergunta="Quais certificações de IA o Sérgio tem?",
        palavras_chave=["LangChain"],
        resposta_referencia=(
            "Tem certificações em 'LangChain e Python' e 'Python: "
            "Inteligência Artificial Aplicada', ambas pela Alura."
        ),
    ),

    # ── Caso 6 ──────────────────────────────
    CasoAvaliacao(
        pergunta="Onde o Sérgio estuda e quando se forma?",
        palavras_chave=["UCSal"],
        resposta_referencia=(
            "Ele cursa Análise e Desenvolvimento de Sistemas na UCSal, "
            "com conclusão prevista pra dezembro de 2026."
        ),
    ),

    # ── Caso 7 ──────────────────────────────
    CasoAvaliacao(
        pergunta="Qual foi a experiência anterior do Sérgio?",
        palavras_chave=["Hunter"],
        resposta_referencia=(
            "Antes da MG3, ele foi estagiário de backend na Hunter "
            "Consultoria, entre março e junho de 2025."
        ),
    ),

 ] 