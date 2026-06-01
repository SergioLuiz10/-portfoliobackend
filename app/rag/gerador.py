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



#funcao vai recer a pergunta do usuario e os chunks parecidos do retriever , usar a ferramenta pra gerar a resposta e devolver só o texto da resposta pro chat.py devolver pro recrutador
def gerar_resposta(pergunta_usuario, pedaços_parecidos , idioma ):
    # junta os pedaços parecidos em um unico texto, separado por quebras de linha
    # pra cada Document da lista chamo de chunk e pego o texto dela 
    pedaços_juntos= "\n\n".join(chunk.page_content for chunk in pedaços_parecidos) 
    messagens_para_o_modelo = [
       SystemMessage(content=INSTRUCOES_DO_SISTEMA), # as regras do jogo
       HumanMessage(content=f"Contexto:\n{pedaços_juntos}\n\nPergunta: {pergunta_usuario}\n\nResponda em: {idioma}") # o contexto + a pergunta do recrutador+ o idioma que o recrutador quer a resposta (português ou inglês)
   ]
   # manda as mensagens pro modelo e recebe a resposta
   #invoke é o metodo que chama o modelo de linguagem, passando as mensagens como input e recebendo a resposta gerada
   resposta_gerada = ferramenta_pra_gerar_resposta.invoke(messagens_para_o_modelo)
   #content é o texto da resposta gerada pelo modelo, que é o que a gente quer retornar pro recrutador 
    return resposta_gerada.content