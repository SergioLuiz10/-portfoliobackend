 # usar o Chatopenai q recebe a pergunta do usuario , pega os chunks do retriver e gera a resposta 
from langchain_openai import ChatOpenAI  
from app.config import objeto_config_env # importa o .env pra pegar a chave da API e o modelo de linguagem escolhido
from langchain_core.messages import SystemMessage,HumanMessage # mensagens do langchain pra criar o prompt pro modelo de linguagem
#[ SystemMessage ]  →  as regras (a constante)
#[ HumanMessage  ]  →  o contexto + a pergunta do recrutador


#manda texto pro modelo e recebe texto de volta usando a API da OpenAI, já configurada com a chave e o modelo do .env
ferramenta_pra_gerar_resposta = ChatOpenAI(
    model=objeto_config_env.llm_model, # modelo de linguagem da OpenAI
    temperature = 0 , #gerar masi perto resposta 
    openai_api_key=objeto_config_env.openai_api_key, # chave da API da OpenAI
)

 # as regras  quem o modelo é e como ele deve responder (fixo, não muda)
INSTRUCOES_DO_SISTEMA = """Você é o Ask Sérgio, um assistente que responde perguntas sobre o Sérgio Luiz Teixeira Nunes Júnior para recrutadores.

Regras:
1. Responda sempre em terceira pessoa, falando sobre o Sérgio.
2. Use APENAS as informações do contexto fornecido. Não use conhecimento externo.
3. Se a resposta não estiver no contexto, diga educadamente que não tem essa informação sobre o Sérgio. Nunca invente.

Seja direto, profissional e cordial."""



#funcao vai recer a pergunta do usuario e os chunks parecidos do retriever , usar a ferramenta pra gerar a resposta e devolver só o texto da resposta pro chat.py devolver pro recrutador mandando pedaco por perdaco 
def gerar_resposta_streaming(pergunta_usuario, pedaços_parecidos , idioma ):
   #O retriever traz uma lista de objetos Document 
   #Ia n entende lista entende texto puro
   # .page_content (o texto cru) de cada chunk e junta numa string
    pedaços_juntos= "\n\n".join(chunk.page_content for chunk in pedaços_parecidos) 
    messagens_para_o_modelo = [
       SystemMessage(content=INSTRUCOES_DO_SISTEMA), # As regras fixas  quem o modelo é, como deve responder
       HumanMessage(content=f"Contexto:\n{pedaços_juntos}\n\nPergunta: {pergunta_usuario}\n\nResponda em: {idioma}") #A conversa do momento — contexto + pergunta + idioma
   ]
   
   #chama a ferramenta de geração de resposta passando as mensagens e recebe a resposta gerada e usa streaming pra mabnda pedacinho por pedacinho
    for pedacinho in ferramenta_pra_gerar_resposta.stream(messagens_para_o_modelo):
        yield pedacinho.content  # o texto puro do chunk , manda fatia por fatia mas guarda na memoria pq vai mandar mais  