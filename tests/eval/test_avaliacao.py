from app.rag.retriever import buscar_chunks_parecidos#usa a funcao de buscar de vdd batendo no banco
from tests.eval.dataset import CASOS_AVALIACAO#chama os casos fakes pra comparar com a busca do banco


#pra cada caso o retrieval trouxe o chunk certo?
def test_retriever():
    #passa de uma vez por cada um dos 7
    #A cada volta, a variável caso vira um CasoAvaliacao
    for caso in CASOS_AVALIACAO:
        #joga no banco real a pergunta fake do teste
        chunks_parecidos=buscar_chunks_parecidos(caso.pergunta)
        #pega só o texto dos chunks parecidos que vieram do banco
        textos_chunks_parecidos=[chunk.page_content for chunk in chunks_parecidos]
       
       
        #junta os 3 textos num textao pra facilitar a busca da palabra
        textaofull_chunks=" ".join(textos_chunks_parecidos)
        # Deixa o textão todo em minúsculo pra comparação não depender de maiúscula.
        texto_completo_minusculo = textaofull_chunks.lower()

        # Pega a 1ª palavra-chave do caso, também em minúsculo.
        palavra_chave = caso.palavras_chave[0].lower()

        # O caso "acerta" se a palavra-chave aparece em algum lugar do textão.
        acertou = palavra_chave in texto_completo_minusculo



