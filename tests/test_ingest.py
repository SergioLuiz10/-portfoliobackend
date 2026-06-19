from fastapi.testclient import TestClient# cria o client teste do fastApi
from app.main import app #chama o fastapi pra usar o client teste
from app.config import objeto_config_env #chama as variaveis de ambiente 

client = TestClient(app)

#testa o endpointe sem o token correto pra garantir que a autenticação tá funcionando
def test_ingest_endpoint_sem_token():
    resposta  = client.post("/ingest", headers={"tokenAdmin": "token_errado"})
    assert resposta.status_code == 401#verifica se o status code da resposta é 401 por conta do token

# não bate no banco retorna um número fixo de chunks
def fake_rodar_ingestao():
    return 17 #retorna um valor fixo pra simular a função de rodar ingestão

#testa o endpoint com o token correto e monkeypatch para garantir que a autenticação tá funcionando
def test_ingest_endpoint_com_token(monkeypatch):
    #monkeypatch para alterar o valor do token de admin para o valor de teste
    monkeypatch.setattr(objeto_config_env, "admin_token", "token_de_teste")
    #monkeypatch para alterar a função de rodar ingestão para uma função de teste que retorna um valor fixo
    monkeypatch.setattr("app.routers.ingest.rodar_ingestao", fake_rodar_ingestao)
    resposta  = client.post("/ingest", headers={"tokenAdmin": "token_de_teste"})
    assert resposta.status_code == 200 #verifica se o status code da resposta é 200 (sucesso)
    assert resposta.json() == {"quantidade_de_documentos_picados": 17} #verifica se a resposta tem o valor esperado