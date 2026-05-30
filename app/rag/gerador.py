 # usar o Chatopenai q recebe a pergunta do usuario , pega os chunks do retriver e gera a resposta 
from langchain_openai import ChatOpenAI  
from app.config import objeto_config_env # importa o .env pra pegar a chave da API e o modelo de linguagem escolhido


#manda texto pro modelo e recebe texto de volta usando a API da OpenAI, já configurada com a chave e o modelo do .env
ferramenta_pra_gerar_resposta = ChatOpenAI(
    model=objeto_config_env.llm_model, # modelo de linguagem da OpenAI
    temperature = 0 , #gerar masi perto resposta 
    openai_api_key=objeto_config_env.openai_api_key, # chave da API da OpenAI
)


