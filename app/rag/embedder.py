# EMBEDDER — prepara a ferramenta de embeddings da OpenAI.
# Usada tanto na ingestão (embeddar chunks) quanto no chat (embeddar a pergunta)

from langchain_openai import OpenAIEmbeddings # embeddings da OpenAI, que transforma texto em vetores numéricos
from app.config import objeto_config_env # importa as o .env

#cria a ferramenta de embeddings já configurada com a chave da API e o modelo escolhido
ferramenta_pra_embeddar = OpenAIEmbeddings(
    model=objeto_config_env.embedding_model, #pega o nome do modelo de embedding 
    openai_api_key=objeto_config_env.openai_api_key, #pega a chave da API da OpenAI 
)