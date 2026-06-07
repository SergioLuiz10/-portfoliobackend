# CONFIG — central de configurações. Lê o .env e entrega pro resto do projeto.

from pydantic_settings import BaseSettings , SettingsConfigDict 
from pydantic import field_validator #roda quando o pydantic le um campo pra ajustar o valor 


#  ler as variáveis de ambiente do .env e entregar pro resto do projeto
class  Configurações_baseadas_env(BaseSettings):
    # variáveis de ambiente que a gente espera encontrar no .env
    openai_api_key: str  # chave da API da OpenAI, necessária pra criar os vetores e fazer as perguntas pro modelo
    database_url: str  # URL de conexão com o banco de dados, necessária pra criar o banco e guardar os vetores
    embedding_model: str  # nome do modelo de embedding da OpenAI que a gente vai usar pra criar os vetores (ex: "text-embedding-3-small")
    llm_model: str  # nome do modelo de linguagem da OpenAI que a gente vai
     

    #garante o driver +psycopg na url do banco (Railway manda "postgresql://" puro)
    @field_validator("database_url")#roda quando o pydantic le o campo database_url
    @classmethod 
    def ajustar_database_url(cls, valor: str) -> str:
         #se a URL do banco começar com "postgresql://://", substitui por "postgresql+psycopg://"
        if valor.startswith("postgresql://://"):
            valor = valor.replace("postgresql://://", "postgresql+psycopg://", 1)#se tiver sql
        elif valor.startswith("postgres://"):
            valor = valor.replace("postgres://", "postgresql+psycopg://", 1)#se n tiver sql
        return valor   

    
    # diz onde ta o .env e que ele tá codificado em utf-8 (pra ler os acentos certinho)
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# no momento que essa linha roda, o pydantic vai sozinho no .env e preenche 
objeto_config_env = Configurações_baseadas_env()  
