# Carrega os .md, pica em chunks e manda pro banco (que embedda sozinho).
# Roda como script:  python -m app.rag.ingest

from app.rag.loader import carregar_documentos # loader pra le os .md 
from app.rag.chunker import cortar_documentos # chunker pra picar os documentos em pedaços menores
from app.database import pegar_conexao_com_banco # função pra criar a conexão com o banco
 
#carrega -> pica -> salva no banco 
def rodar_ingestao():
    #carrega os documentos do .md e guardar numa lista de documento carregados
    documentos_carregados = carregar_documentos()
    #mostra quantos documentos foram carregados
    print(f"[1/3] Documentos carregados: {len(documentos_carregados)}")

    #cria uma nova lista pra guardar os documentos picados chamando o cortar do chunker passando a lista anterior     
    documentos_picados = cortar_documentos(documentos_carregados)
    #mostra quantos documentos picados foram criados
    print(f"[2/3] Documentos picados: {len(documentos_picados)}") 

    #pega a conexão com o banco para mandar os documentos picados pra lá
    conexao_com_banco = pegar_conexao_com_banco()
    #manda os documentos picados pro banco, que vai criar os vetores e guardar tudo lá
    conexao_com_banco.add_documents(documentos_picados)
    #mostra quantos documentos picados foram enviados pro banco
    print(f"[3/3] Documentos enviados para o banco: {len(documentos_picados)}")


# "botão de ligar": só roda a ingestão se o arquivo for executado direto
# (python -m app.rag.ingest). Se for importado por outro arquivo, NÃO roda sozinho.
# Roda como script:  python -m app.rag.ingest
if __name__ == "__main__":
   rodar_ingestao()