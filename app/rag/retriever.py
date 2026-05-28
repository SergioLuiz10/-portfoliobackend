# RETRIEVER — busca no rag.
# Dado uma pergunta, e devolve chunks mais parecidos guardados no banco.

#se conecta com banco
from app.database import pegar_conexao_com_banco  


# quantos chunks q vai pegar do banco parecidos com a pergunta do usuario
QUANTIDADE_CHUNKS_PARECIDOS= 3


#funcao q pega os chunks mais parecidos do banco, recebendo a pergunta
def buscar_chunks_parecidos(pergunta_usuario):
    conexao_com_banco = pegar_conexao_com_banco() 
    
     #usa a função de busca por similaridade da conexão, passando a pergunta do usuário e a quantidade de chunks parecidos que queremos
    pedaços_parecidos = conexao_com_banco.similarity_search(
        pergunta_usuario, # a pergunta do usuário que queremos comparar com os chunks do banco
        k=QUANTIDADE_CHUNKS_PARECIDOS, # a quantidade de chunks parecidos que queremos receber do banco
    )
    return pedaços_parecidos