from langchain_postgres import PGVector # a ferramenta que fala com o banco e guarda vetores
from app.config import objeto_config_env # importa o .env e onde sai o database_url
from app.rag.embedder import ferramenta_pra_embeddar # como o texto vira vetor chama la o embedder 

# nome da coleção onde os vetores vão ser guardados no banco
NOME_COLECAO = "documentos_picados_sergio" 

def pegar_conexao_com_banco():
    # cria a conexão com o banco usando a URL do .env e a ferramenta de embeddings pra transformar texto em vetor
    conexao_com_banco = PGVector(
         embeddings=ferramenta_pra_embeddar, # a ferramenta de embeddings que transforma texto em vetor
         collection_name=NOME_COLECAO, #o nome da coleção onde os vetores ficam guardados no banco
         connection= objeto_config_env.database_url, # a URL de conexão com o banco do .env
    )
    # entrega o objeto pronto pra quem chamou a função
    return conexao_com_banco
 