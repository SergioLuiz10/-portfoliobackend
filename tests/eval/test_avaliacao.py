from app.rag.retriever import buscar_chunks_parecidos#usa a funcao de buscar de vdd batendo no banco
from app.rag.gerador import gerar_resposta_streaming#usa a funcao de gerar resposta de vdd batendo na API da OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.config import objeto_config_env
from tests.eval.dataset import CASOS_AVALIACAO#chama os casos fakes pra comparar com a busca do banco
import pytest


#cria o modelo que vai atuar como juiz.
#ele vai receber a pergunta do caso, os chunks parecidos que o retriever trouxe e a resposta que o gerador deu e vai julgar se a resposta tá certa ou não
ferramenta_pra_julgar = ChatOpenAI(
   model=objeto_config_env.llm_model, # modelo de linguagem da OpenAI
    temperature = 0 , #gerar masi perto resposta
    openai_api_key=objeto_config_env.openai_api_key, # chave da API da OpenAI
)


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


INSTRUCOES_DO_JUIZ = """Sua tarefa é julgar se uma RESPOSTA está fielmente ancorada no CONTEXTO fornecido.

Critério:
- Responda SIM se TODAS as afirmações da resposta puderem ser verificadas no contexto.
- Responda NAO se a resposta contiver qualquer informação que não esteja no contexto, mesmo que seja verdadeira no mundo real.
- Se a resposta apenas diz que não tem a informação, e o contexto de fato não tem, isso conta como SIM (é o comportamento correto).

Não avalie se a resposta é útil, completa ou bem escrita. Avalie APENAS se ela está apoiada no contexto.

Responda com uma única palavra: SIM ou NAO."""



@pytest.mark.eval  # ficar de fora do ci
# teste de fidelidade
#compara a resposta do gerador com o contexto que o retriever trouxe e vê se a resposta tá de fato ancorada no contexto
def test_faithfulness():
    respostas_fieis= 0
     
    #passando de uma vez por cada um dos 7 casos
    for caso in CASOS_AVALIACAO:
        #joga no banco real a pergunta fake do teste
        chunks_parecidos=buscar_chunks_parecidos(caso.pergunta)
        
        #pega só o texto dos chunks parecidos que vieram do banco com streaming
        resposta_completa = ""
        #Esse for vai pegando cada pedacinho conforme ele sai.
        #pegando a pergunta , o contexto e so falta a resposta do gerador
        for pedacinho in gerar_resposta_streaming(caso.pergunta, chunks_parecidos,"português"):
            #vai juntando os pedacinhos num textão
            resposta_completa += pedacinho

        #junta os chunks parecidos num string só
        contexto_texto = " ".join([chunk.page_content for chunk in chunks_parecidos])    

        mensagens_pro_juiz = [
          #prompt criado pra o juiz
          SystemMessage(content=INSTRUCOES_DO_JUIZ),
          #passando o contexto, a pergunta e a resposta pro juiz analisar
          HumanMessage(content=f"CONTEXTO:\n{contexto_texto}\n\nPERGUNTA:\n{caso.pergunta}\n\nRESPOSTA:\n{resposta_completa}"),
        ]
        #manda pro juiz analisar e ele vai responder SIM ou NAO
        veredito = ferramenta_pra_julgar.invoke(mensagens_pro_juiz)
         
         #pega o veredito do juiz e tira os espaços e coloca em maiúsculo pra ficar só SIM ou NAO
        texto_veredito = veredito.content.strip().upper()


        #se o veredito for SIM, então a resposta foi fiel ao contexto
        status = "✅" if texto_veredito == "SIM" else "❌"
        print(f"{status} {caso.pergunta}")
   
        if texto_veredito == "SIM":
            respostas_fieis += 1
    # calcula a porcentagem de respostas fiéis
    total_de_casos = len(CASOS_AVALIACAO)
    score = respostas_fieis / total_de_casos
    print(f"\nFaithfulness: {respostas_fieis}/{total_de_casos} = {score:.2%}")

        


INSTRUCOES_DO_JUIZ_RELEVANCIA = """Você é um avaliador de sistemas RAG.
Sua tarefa é julgar se uma RESPOSTA de fato responde à PERGUNTA feita.

Critério:
- Responda SIM se a resposta aborda diretamente o que foi perguntado.
- Responda NAO se a resposta fala de outro assunto, foge do tema, ou não endereça a pergunta.
- Se a pergunta pede uma informação e a resposta diz educadamente que não a possui, isso conta como SIM (ela endereçou a pergunta de forma honesta).

Não avalie se a resposta é verdadeira ou se está apoiada em algum contexto. Avalie APENAS se ela responde à pergunta.

Responda com uma única palavra: SIM ou NAO."""

# também gera resposta + chama o juiz, então também é caro e também fica fora do CI.
@pytest.mark.eval
#vai testar se a resposta do gerador realmente responde a pergunta do caso
def test_relevance():
    respostas_relevantes = 0
    
    #pegar as pergunts de cada caso e ver se a resposta do gerador responde a pergunta
    for caso in CASOS_AVALIACAO:
        #joga no banco real a pergunta fake do teste
        chunks_parecidos=buscar_chunks_parecidos(caso.pergunta)
        
        #dps vai gerar a resposta do gerador com streaming
        resposta_completa = ""
        
         #Esse for vai pegando cada pedacinho conforme ele sai.
        for pedacinho in gerar_resposta_streaming(caso.pergunta, chunks_parecidos, "português"):
            resposta_completa += pedacinho

        mensagens_pro_juiz = [
            #prompt criado pra o juiz
            SystemMessage(content=INSTRUCOES_DO_JUIZ_RELEVANCIA),
            #passando a pergunta e a resposta pro juiz analisar
            HumanMessage(content=f"PERGUNTA:\n{caso.pergunta}\n\nRESPOSTA:\n{resposta_completa}"),
            ]    
        

        #manda pro juiz analisar e ele vai responder SIM ou NAO
        veredito = ferramenta_pra_julgar.invoke(mensagens_pro_juiz)
        #pega o veredito do juiz e tira os espaços e coloca em maiúsc
        texto_veredito = veredito.content.strip().upper()        #printa se a resposta do gerador respondeu a pergunta do caso ou não, com o status de ✅ ou ❌ 
        
        #printa a pergunta do caso junto com o status de relevância
        status = "✅" if texto_veredito == "SIM" else "❌"
        print(f"{status} {caso.pergunta}")

        if texto_veredito == "SIM":
            respostas_relevantes += 1
    
    # calcula a porcentagem de respostas relevantes
    total_de_casos = len(CASOS_AVALIACAO)
    score = respostas_relevantes / total_de_casos
    print(f"\nRelevance: {respostas_relevantes}/{total_de_casos} = {score:.2%}")
        