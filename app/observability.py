import json  # transformar os dados (pergunta, latência, chunks) em JSON
import logging  #traz timestamp,níveis(INFO/ERROR) e controle de formato
from datetime import datetime, timezone  #traz o timestamp atual em UTC

#cria o logger q faz o registro de logs 
logger = logging.getLogger("ask_sergio")
#nível de log como INFO( nívelpara mensagens informativas )
logger.setLevel(logging.INFO)  

#cria o handler que envia os logs para o stdout(terminal)
handler = logging.StreamHandler()

#define o formato do log como apenas a mensagem (sem timestamp, nível, etc.)
formatter = logging.Formatter("%(message)s")

#handler onde envia
#formatter define o formato do log
#agr cola o formatter no handler
handler.setFormatter(formatter)# usar esse formato(json) para mandar mensagens

#o logger adiciona o handler para que os logs sejam enviados para o terminal
logger.addHandler(handler) 

#para evitar que os logs sejam propagados para outros loggers, definimos propagate como False
logger.propagate = False


# feito para registrar métricas de latência e contagem de perguntas, erros, etc.
#placar , vai somando o total de perguntas, latência e erros
metricas = {
    "total_perguntas": 0, #ve quantas perguntas foram feitas

}

#registra os eventos no log, transformando os dados em JSON e enviando para o logger
#**dados aceita qualquer quantidade de argumentos nomeados
def registrar_evento(**dados):
    #adiciona o timestamp atual em UTC no dicionário de dados
    dados["timestamp"] = datetime.now(timezone.utc).isoformat()
    #se o evento for "chat_recebido", incrementa o contador de perguntas e adiciona o total de perguntas no dicionário de dados
    if dados.get("evento") == "chat_recebido":
        #incrementa o contador de perguntas
        metricas["total_perguntas"] += 1
       
    #transforma o dicionário de dados em uma string JSON e envia para o logger
    #pega o dicionário dados (com pergunta, latência, timestamp)
    #ensure_ascii=False garante que caracteres especiais sejam preservados no JSON
    #logger.info manda string JSON para o stdout (terminal) com o formato definido anteriormente
    logger.info(json.dumps(dados, ensure_ascii=False)) 

