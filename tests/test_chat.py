from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# n precisa de banco ent vai fingir a função de buscar chunks parecidos pra retornar um resultado fixo
def fake_buscar_chunks_parecidos(pergunta):
    return ["O Sérgio é dev backend focado em IA."]


# n precisa do modelo de linguagem ent vai fingir a função de gerar resposta pra retornar um resultado fixo, yield imita o streaming solta pedacos  
def fake_gerar_resposta(pergunta_usuario, pedaços_parecidos, idioma):
    yield "O Sérgio "
    yield "é dev backend."    

# monkeypatch substitui as funções reais pelas falsas durante o teste
def test_chat_endpoint(monkeypatch):
    monkeypatch.setattr("app.routers.chat.gerar_resposta_streaming", fake_gerar_resposta)# substitui a função de gerar resposta pela falsa
    monkeypatch.setattr("app.routers.chat.buscar_chunks_parecidos", fake_buscar_chunks_parecidos) # substitui a função de buscar chunks pela falsa
    response = client.post("/chat", json={"message": "Quem é o Sérgio?", "language": "Português"}) # faz uma requisição POST pro endpoint de chat com uma pergunta e idioma
    assert response.status_code == 200 # verifica se o status code da resposta é 200
    assert response.text == "O Sérgio é dev backend." # texto tem q ser igual 
    
