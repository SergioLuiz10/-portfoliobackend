from app.rag.retriever import buscar_chunks_parecidos#usa a funcao de buscar de vdd batendo no banco
from tests.eval.dataset import CASOS_AVALIACAO#chama os casos fakes pra comparar com a busca do banco
import pytest


#pra cada caso o retrieval trouxe o chunk certo?
@pytest.mark.eval # 
def test_retriever():
    #quantos casos acertaram. Começa em zero
    acertos = 0

    #passa de uma vez por cada um dos 7
    #A cada volta, a variável caso vira um CasoAvaliacao
    for caso in CASOS_AVALIACAO:
        #joga no banco real a pergunta fake do teste
        chunks_parecidos=buscar_chunks_parecidos(caso.pergunta)
        #pega só o texto dos chunks parecidos que vieram do banco
        textos_chunks_parecidos=[chunk.page_content for chunk in chunks_parecidos]
       
       
        #junta os 3 textos num textao 
        textaofull_chunks=" ".join(textos_chunks_parecidos)
        # Deixa o textão todo em minúsculo 
        texto_completo_minusculo = textaofull_chunks.lower()

        # Pega a 1ª palavra-chave do caso
        palavra_chave = caso.palavras_chave[0].lower()

        # O caso "acerta" se a palavra-chave aparece em algum lugar do textão.
        acertou = palavra_chave in texto_completo_minusculo

          #printa se acertou ou não, com o status de ✅ ou ❌
        status = "✅" if acertou else "❌"
         
        #printa a pergunta do caso junto com o status de acerto 
        print(f"{status} {caso.pergunta}")


        #se acertou, soma 1 no total de acertos
        if acertou:
            acertos += 1
    # calcula a porcentagem de acertos
    total_de_casos = len(CASOS_AVALIACAO)   

    # Divide os acertos pelo total pra virar uma nota de 0 a 1
    score = acertos / total_de_casos 
    # printa a nota de acertos em porcentagem
    print(f"\nContext relevance: {acertos}/{total_de_casos} = {score:.2%}")