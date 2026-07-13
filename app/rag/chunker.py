from langchain_text_splitters import RecursiveCharacterTextSplitter#a ferramenta de picar texto do LangChain
from langchain_text_splitters import MarkdownHeaderTextSplitter# ferramenta que corta markdown q corta em cabeçalhos

#criar a ferramenta de picar texto ja configurada
cortador_de_texto = RecursiveCharacterTextSplitter(
    chunk_size=1000, #tamanho máximo de cada pedaço de texto
    chunk_overlap=150, #quantos caracteres de um pedaço vão se repetir no próximo pedaço (pra manter o contexto)
)

#cria a feramenta de picar cabeçalhos de markdown, pra cortar em tópicos
#como usa # no titulo e ## nas secao, ele vai cortar em cada título e secao
#titulo e secao sao apelidos para etiquetar, ficará guardada nos metadados de cada chunk.
cabecalhos_pra_dividir = [
  ("#", "titulo"),
  ("##", "secao")

]   

#cria a ferramenta de picar markdown ja configurada
#usando o cabecalhos_pra_dividir, ele vai cortar em cada título e secao, e vai guardar o apelido nos metadados de cada chunk
cortador_de_secoes = MarkdownHeaderTextSplitter(
    #receber a lista de cabeçalhos pra dividirando
    headers_to_split_on=cabecalhos_pra_dividir,
    #normalemtne joga a linha do cabecalho fora ai com o false mantem no chunk 
    strip_headers=False,
)


#vai receber a lista de documentos do loader e devolver a lista de documentos picados, prontos pra virar vetores
#vai usar junto o cortador_de_texto e o cortador_de_secoes pra cortar em pedaços menores, respeitando o chunk_size e o chunk_overlap configurados
#cortador_de_texto vai cortar em pedaços menores, respeitando o chunk_size e o chunk_overlap configurados
#cortador_de_secoes vai cortar em cada título e secao, e vai guardar o apelido nos metadados de cada chunk
def cortar_documentos(documentos_para_cortar):
    #caixa para guardar os documentos picados usando o cortador_de_texto 
    documentos_picados = []
    #caixa para guardar as secoes de cada documento picado usando o cortador_de_secoes
    pedacos_por_secao=[]
      
    #o cortador_de_secoes n aceita listas inteiras ent tem q cortar um documento por vez, então vai percorrer cada documento da lista de documentos_para_cortar  
    for documento in documentos_para_cortar:
      #corta por assunto e guarda a secao
      secoes = cortador_de_secoes.split_text(documento.page_content)
      #pega os pedaços de cada secao e guarda na lista pedacos_por_secao
      pedacos_por_secao.extend(secoes) 
    
    # pedacos_por_secao já tem tudo cortado por assunto mas alguma seção pode ter saído gigante ai usa o cortardor
    # pra quebrar só os que ficaram grandes demais
    documentos_picados=cortador_de_texto.split_documents(pedacos_por_secao)
    return documentos_picados 

        