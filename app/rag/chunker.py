from langchain_text_splitters import RecursiveCharacterTextSplitter#a ferramenta de picar texto do LangChain
 

#criar a ferramenta de picar texto ja configurada
cortador_de_texto = RecursiveCharacterTextSplitter(
    chunk_size=1000, #tamanho máximo de cada pedaço de texto
    chunk_overlap=150, #quantos caracteres de um pedaço vão se repetir no próximo pedaço (pra manter o contexto)
)

#vai receber a lista de documentos do loader e devolver a lista de documentos picados, prontos pra virar vetores
def cortar_documentos(documentos_para_cortar):
    documentos_picados = []
    #split vai pega cada documento e cortar ele em pedaços menores, respeitando o chunk_size e o chunk_overlap configurados
    documentos_picados = cortador_de_texto.split_documents(documentos_para_cortar) 
    return documentos_picados 

        