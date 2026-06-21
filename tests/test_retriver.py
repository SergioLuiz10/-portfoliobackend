from app.rag.retriever import buscar_chunks_parecidos #função de buscar chunks parecidos do retriever

# objeto fake que imita a conexão com o banco
class ConexaoFake:
    # imita o método similarity_search(q é a busca por similaridade) do banco real
    def similarity_search(self, pergunta_usuario, k):
        return ["Sérgio trabalha na MG3.", "Sérgio cursa ADS na UCSal.", "Sérgio é dev backend."]
 
# no lugar de criar a conexão real, devolve a conexão fake
def fake_pegar_conexao_com_banco():
    return ConexaoFake() 


def test_buscar_chunks_parecidos(monkeypatch):
    #vai trocar o pegar_conexao_com_banco real pela função fake que devolve a conexão fake
    monkeypatch.setattr("app.rag.retriever.pegar_conexao_com_banco", fake_pegar_conexao_com_banco)
    #chama a função de buscar chunks parecidos com uma pergunta de teste
    resposta = buscar_chunks_parecidos("onde o Sérgio trabalha?")
    #verifica se a resposta tem a quantidade de chunks parecidos esperada e se um dos chunks esperados está na resposta
    assert len(resposta) == 3
    assert "Sérgio trabalha na MG3." in resposta




