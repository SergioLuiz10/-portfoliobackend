from pathlib import Path
from langchain_core.documents import Document # tem a funcao de criar um documento a partir de um texto e metadados

# Define o caminho para o diretório de dados, que é quatro níveis acima do arquivo atual e depois entra na pasta "data"
DATA_DIR = Path(__file__).parent.parent.parent.parent / "data"

#1. Olha dentro da pasta data/ e lista os arquivos .md
#2. Se não achar NENHUM → avisa com erro (algo tá errado)
#3. Pra CADA arquivo encontrado:
#      a. abre e lê o texto
#      b. coloca o texto numa "caixinha" Document (com a etiqueta de origem)
#      c. guarda essa caixinha numa lista
#4. No fim, devolve a lista com as 5 caixinhas
def carregar_documentos():
    documentos = [] 
    arquivos_pessoais = sorted(DATA_DIR.glob("*.md"))  # coloca os arquivos em ordem alfabética da pasta data 
    if not arquivos_pessoais:  # se a lista de arquivos estiver vazia, ou seja, não encontrou nenhum arquivo .md
        raise FileNotFoundError(f"Nenhum arquivo .md encontrado em {DATA_DIR}")  # avisa que não encontrou nenhum arquivo .md
    for percorredor_arquivo in arquivos_pessoais:
        conteudo_achado = percorredor_arquivo.read_text(encoding="utf-8")  #  le os acentos certinho (ã, ç, é) 
        #cria 
        documentos_pro_banco = Document(
            page_content=conteudo_achado,#enche o documento com o texto achado no arquivo .md
            metadata={"source": percorredor_arquivo.name}, #ele vai saber dizer "essa info veio do 03-projetos.md
        )
        documentos.append(documentos_pro_banco) #guarda o documento na lista de documentos q vao pro banco de dados
    return documentos   #devolve a lista de documentos para o processo de criação do banco de dados 
   